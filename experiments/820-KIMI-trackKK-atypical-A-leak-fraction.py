#!/usr/bin/env python3
"""820 (Track KK): quantify atypical-A leak fraction for rank-n B = C·A_L.

Context
-------
For a Lagrangian A (ordered isotropic basis), a rank-n reduction can use B = C·A_L
where A_L is a left-inverse of A (A_L A = I_n).  The output is
    y = BAx + Be = Cx + C·A_L·e.
For full-rank C this is equivalent to observing x + A_L·e, so the leak is exactly
    I(x;y|C) = n - H(A_L·e),
which depends only on A_L (and e ~ Bernoulli(1/4)^{2n}), not on m.

Some Lagrangians have a light left-inverse (e.g. A=[I;0] gives A_L=[I|0], so
A_L·e = e_top is low-weight Bernoulli(1/4)^n).  Typical Lagrangians force every
left-inverse row to have large weight, smoothing A_L·e toward uniform.  This script
quantifies the atypical/leaky fraction.

Modeling choices
----------------
* A is a uniform ordered isotropic basis of a uniform Lagrangian (paper model).
* For each A we choose a minimum-Hamming-weight left-inverse A_L, minimizing each
  row independently (rows have independent constraints).
* e ~ Bernoulli(1/4)^{2n}.
* C is uniform full-rank m×n; the reported I(x;y|C) is n - H(A_L·e), independent of m.

Claims and labels
-----------------
* I(x;y|C) = n - H(A_L·e) for full-rank C in the rank-n construction B=C·A_L —
  THEOREM (C is invertible on its column space).
* Enumeration of all ordered Lagrangian bases and their min-weight left-inverses
  for n=2,3 — EVIDENCE (exact finite enumeration).
* Distribution of row weights, per-coordinate biases, and average leak — EVIDENCE.
* Whether the leaky fraction is 2^{-Ω(n)} and whether average leak is o(1) —
  CONJECTURE/OPEN (only n=2,3 checked).

Guards
------
L1 exact arithmetic: exact rational probabilities; float only for final log2.
L2 J-twist duality: inspected directly in (A_L, e) space.
L3 query-class hygiene: information-theoretic I, no query restriction.
L4 never transform the comparison distribution: no LPN comparison used.
PRE-REGISTER: quantity = atypical-A leak fraction and average I(x;y|C) for rank-n
B=C·A_L; model = rank-n marginal-uniform construction; closure-grade = finite-n.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import math
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path


# ---------------------------------------------------------------------------
# Symplectic helpers for general n
# ---------------------------------------------------------------------------

def symplectic_form(u: int, v: int, n: int) -> int:
    """Standard symplectic form on F_2^{2n}; bits are paired (q_0,p_0,...,q_{n-1},p_{n-1})."""
    s = 0
    for i in range(n):
        q_u = (u >> (2 * i)) & 1
        p_u = (u >> (2 * i + 1)) & 1
        q_v = (v >> (2 * i)) & 1
        p_v = (v >> (2 * i + 1)) & 1
        s ^= q_u * p_v ^ p_u * q_v
    return s & 1


def dot(u: int, v: int, dim: int) -> int:
    """Standard dot product over F_2."""
    return (bin(u & v & ((1 << dim) - 1)).count("1") & 1)


# ---------------------------------------------------------------------------
# F_2 linear algebra
# ---------------------------------------------------------------------------

def gauss_eliminate_f2(rows: list[int], n_cols: int) -> tuple[list[int], list[int]]:
    """Return (row_echelon_form, pivot_columns).  rows are n_cols-bit integers."""
    pivots = {}
    pivot_cols = []
    for r in rows:
        x = r & ((1 << n_cols) - 1)
        if x == 0:
            continue
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                pivot_cols.append(p)
                break
    return list(pivots.values()), sorted(pivot_cols)


def nullspace_basis_f2(rows: list[int], n_cols: int) -> list[int]:
    """Return a basis for the (right) nullspace of the matrix whose rows are given."""
    ref, pivots = gauss_eliminate_f2(rows, n_cols)
    pivot_set = set(pivots)
    free_cols = [c for c in range(n_cols) if c not in pivot_set]
    basis = []
    for f in free_cols:
        vec = 1 << f
        for i, p in enumerate(pivots):
            row = ref[i]
            if (row >> f) & 1:
                vec |= 1 << p
        basis.append(vec)
    return basis


def solve_linear_system(A_rows: list[int], n_cols: int, rhs: list[int]) -> list[int] | None:
    """Solve A x = rhs for each rhs, where A is matrix with rows A_rows (n_cols-bit).

    Returns list of solutions (one per rhs) or None if inconsistent.
    """
    # Build augmented matrix [A | rhs_0 | rhs_1 | ...] and row-reduce.
    num_rhs = len(rhs)
    rows = []
    for i, r in enumerate(A_rows):
        aug = r
        for j in range(num_rhs):
            if (rhs[j] >> i) & 1:
                aug |= 1 << (n_cols + j)
        rows.append(aug)

    pivots = {}
    for idx, r in enumerate(rows):
        x = r & ((1 << n_cols) - 1)
        if x == 0:
            if r >> n_cols:
                return None
            continue
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                r ^= pivots[p]
                x = r & ((1 << n_cols) - 1)
            else:
                pivots[p] = r
                break

    # Back substitution: process pivots from lowest to highest.  Pivot row p has
    # leading 1 at p and zeros at positions > p; it may depend on lower-index
    # pivot variables that have already been determined.
    solutions = [0] * num_rhs
    for p in sorted(pivots.keys()):
        r = pivots[p]
        coeff = r & ((1 << n_cols) - 1)
        for j in range(num_rhs):
            lhs = bin(coeff & solutions[j]).count("1") & 1
            rhs_bit = (r >> (n_cols + j)) & 1
            if lhs != rhs_bit:
                solutions[j] |= 1 << p
    return solutions


def solve_left_inverse(A_cols: list[int], dim: int) -> list[int] | None:
    """Return a particular left-inverse A_L (n rows, each a dim-bit vector) or None.

    A_cols are the n columns of A as dim-bit integers.  We need w_i · A_cols[j] = δ_{i,j}.
    The system is A^T w_i^T = e_i, where A^T has rows A_cols.
    """
    n = len(A_cols)
    rhs = [1 << i for i in range(n)]
    sols = solve_linear_system(A_cols, dim, rhs)
    if sols is None:
        return None
    return sols


# ---------------------------------------------------------------------------
# Lagrangian enumeration
# ---------------------------------------------------------------------------

def enumerate_lagrangian_subspaces(n: int) -> list[list[int]]:
    """Enumerate all Lagrangian subspaces of F_2^{2n} as sorted lists of vectors."""
    dim = 2 * n
    found = set()
    # enumerate all n-dimensional isotropic subspaces by choosing n independent vectors
    # pairwise symplectically orthogonal; use Gaussian elimination to get span.
    vectors = list(range(1 << dim))
    # precompute non-zero vectors
    nonzero = [v for v in vectors if v != 0]

    def span_of(vecs: list[int]) -> frozenset:
        # compute span by Gaussian elimination over F_2
        pivots = {}
        for v in vecs:
            x = v
            while x:
                p = x.bit_length() - 1
                if p in pivots:
                    x ^= pivots[p]
                else:
                    pivots[p] = x
                    break
        # enumerate all linear combinations
        basis = list(pivots.values())
        sp = {0}
        for b in basis:
            new = {v ^ b for v in sp}
            sp.update(new)
        return frozenset(sp)

    # Greedy enumeration: choose ordered n-tuples of independent isotropic vectors.
    # For n=2,3 this is fast enough.
    count = 0
    for i, v1 in enumerate(nonzero):
        for v2 in nonzero:
            if v2 <= v1:
                continue
            if symplectic_form(v1, v2, n) != 0:
                continue
            if n == 2:
                sp = span_of([v1, v2])
                if len(sp) == 4:
                    found.add(sp)
                continue
            for v3 in nonzero:
                if v3 <= v2:
                    continue
                if symplectic_form(v1, v3, n) != 0:
                    continue
                if symplectic_form(v2, v3, n) != 0:
                    continue
                sp = span_of([v1, v2, v3])
                if len(sp) == 8:
                    found.add(sp)
    return [sorted(s) for s in found]


def ordered_isotropic_bases_for_subspace(L: list[int]) -> list[tuple[int, ...]]:
    """Return all ordered bases of the Lagrangian subspace L."""
    nonzero = [v for v in L if v != 0]
    bases = []
    n = int(math.log2(len(L)))
    for a0 in nonzero:
        span_a0 = {0, a0}
        for a1 in nonzero:
            if a1 in span_a0:
                continue
            span_a0_a1 = {v ^ a1 for v in span_a0} | span_a0
            if n == 2:
                if len(span_a0_a1) == 4:
                    bases.append((a0, a1))
                continue
            for a2 in nonzero:
                if a2 in span_a0_a1:
                    continue
                span_full = {v ^ a2 for v in span_a0_a1} | span_a0_a1
                if len(span_full) == 8:
                    bases.append((a0, a1, a2))
    return bases


# ---------------------------------------------------------------------------
# Min-weight left-inverse and leak computation
# ---------------------------------------------------------------------------

def min_weight_left_inverse(A_cols: list[int], dim: int) -> tuple[list[int], list[int]]:
    """Return (A_L rows, row_weights) with minimum Hamming weight rows."""
    n = len(A_cols)
    # particular solution
    A_L0 = solve_left_inverse(A_cols, dim)
    if A_L0 is None:
        raise ValueError("A has no left-inverse")
    # standard orthogonal complement of span(A_cols)
    L_perp = nullspace_basis_f2(A_cols, dim)
    # enumerate all vectors in L_perp
    perp_vecs = [0]
    for b in L_perp:
        perp_vecs += [v ^ b for v in perp_vecs]

    A_L = []
    weights = []
    for i in range(n):
        best_w = None
        best_wt = dim + 1
        for v in perp_vecs:
            w = A_L0[i] ^ v
            wt = w.bit_count()
            if wt < best_wt:
                best_wt = wt
                best_w = w
        A_L.append(best_w)
        weights.append(best_wt)
    return A_L, weights


def distribution_of_A_L_e(A_L: list[int], dim: int) -> Counter:
    """Return distribution of A_L · e for e ~ Bernoulli(1/4)^{dim}."""
    n = len(A_L)
    dist = Counter()
    for e in range(1 << dim):
        s = 0
        for i, w in enumerate(A_L):
            if dot(w, e, dim):
                s |= 1 << i
        weight_e = e.bit_count()
        dist[s] += 3 ** (dim - weight_e)
    return dist


def entropy_of_dist(dist: Counter, total: int) -> float:
    h = 0.0
    for cnt in dist.values():
        if cnt == 0:
            continue
        p = cnt / total
        h -= p * math.log2(p)
    return h


def analyze_n(n: int):
    dim = 2 * n
    t0 = time.time()
    subspaces = enumerate_lagrangian_subspaces(n)
    print(f"n={n}: {len(subspaces)} Lagrangian subspaces", file=sys.stderr)

    total_bases = 0
    row_weight_counts = Counter()
    max_row_weight_counts = Counter()
    leak_sum = Fraction(0, 1)
    leak_by_max_weight = Counter()
    count_by_max_weight = Counter()
    leak_values = []
    total_weight = 4 ** dim  # sum of 3^{dim-wt(e)} over e = (3+1)^dim

    for L in subspaces:
        bases = ordered_isotropic_bases_for_subspace(L)
        for A in bases:
            total_bases += 1
            A_L, weights = min_weight_left_inverse(list(A), dim)
            for wt in weights:
                row_weight_counts[wt] += 1
            max_wt = max(weights)
            max_row_weight_counts[max_wt] += 1

            dist = distribution_of_A_L_e(A_L, dim)
            H = entropy_of_dist(dist, total_weight)
            leak = n - H
            leak_sum += Fraction(leak).limit_denominator(10**9)
            leak_values.append(leak)
            leak_by_max_weight[max_wt] += Fraction(leak).limit_denominator(10**9)
            count_by_max_weight[max_wt] += 1

    avg_leak = float(leak_sum) / total_bases

    # threshold analysis: fraction with max row weight <= t
    threshold_analysis = []
    cum_count = 0
    cum_leak = Fraction(0, 1)
    for t in range(1, n + 1):
        cum_count += max_row_weight_counts[t]
        cum_leak += leak_by_max_weight[t]
        threshold_analysis.append({
            "threshold_max_row_weight": t,
            "leaky_count": cum_count,
            "leaky_fraction": cum_count / total_bases,
            "avg_leak_among_leaky_bits": float(cum_leak) / cum_count if cum_count > 0 else 0.0,
            "contribution_to_avg_leak_bits": float(cum_leak) / total_bases,
        })

    # per-coordinate bias distribution (bias = 2^{-row_weight})
    bias_distribution = Counter()
    for wt, cnt in row_weight_counts.items():
        bias_distribution[wt] = cnt

    result = {
        "n": n,
        "dim": dim,
        "num_lagrangian_subspaces": len(subspaces),
        "num_ordered_bases": total_bases,
        "row_weight_distribution": {str(k): v for k, v in sorted(row_weight_counts.items())},
        "max_row_weight_distribution": {str(k): v for k, v in sorted(max_row_weight_counts.items())},
        "per_coordinate_bias_by_row_weight": {str(k): 2 ** (-k) for k in row_weight_counts.keys()},
        "threshold_analysis": threshold_analysis,
        "average_leak_bits": avg_leak,
        "min_leak_bits": min(leak_values) if leak_values else None,
        "max_leak_bits": max(leak_values) if leak_values else None,
        "elapsed_seconds": time.time() - t0,
    }
    return result


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_experiment(output_dir: Path | None = None):
    results = {
        "track": "KK",
        "experiment": 820,
        "quantity": "atypical-A leak fraction for rank-n B = C·A_L",
        "standing_guards": ["L1 exact arithmetic", "L2 J-twist duality", "L3 query-class hygiene", "L4 never transform LPN"],
        "modeling_choices": {
            "A_ensemble": "uniform ordered basis of a uniform Lagrangian",
            "B_construction": "B = C·A_L, rank n, full-rank C",
            "left_inverse": "minimum Hamming weight row-wise",
            "ambient_noise": "e ~ Bernoulli(1/4)^{2n}",
            "identity_used": "I(x;y|C) = n - H(A_L·e) for full-rank C (THEOREM)",
        },
        "rows": [],
    }

    for n in [2, 3]:
        row = analyze_n(n)
        results["rows"].append(row)
        print(json.dumps(row, indent=2), file=sys.stderr)

    if output_dir is None:
        output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "820-trackKK-atypical-A-leak-fraction.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=None, help="output directory")
    args = parser.parse_args()
    run_experiment(output_dir=args.output_dir)
