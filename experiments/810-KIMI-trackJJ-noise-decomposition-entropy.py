#!/usr/bin/env python3
"""810 (Track JJ): direct attack on H(C_L·Be | HBe, C).

Context
-------
Gemini reframed the lem:m2 open core as: for typical marginal-uniform C,
    I(x;y|C) = o(n)  ⟺  H(C_L·Be | HBe, C) ≥ n - o(n),
where C = BA, C_L is a left-inverse of C (C_L C = I_n), and H is a parity-check
matrix for C (HC = 0).  The vector C_L·Be ∈ F_2^n is the message-part noise that
corrupts x; HBe ∈ F_2^{m-n} is the syndrome.  If the message-part noise remains
uniform even given the syndrome, then x is protected; any drop below n is a leak.

Modeling choices
----------------
Same as Track II / paper/lsn-core.tex line 602: A is a uniform ordered isotropic
basis of a uniform Lagrangian (90 ordered bases for n=2).  B is marginal-uniform
over rows.  e ~ Bernoulli(1/4)^{2n}.  We condition on C having full column rank n
("typical"); rank-deficient C is reported separately but not included in the
entropy figure, because C_L and H are only well-defined there.

Method
------
For full-rank C the map y ↦ (C_L y, H y) is an F_2-linear bijection and
    C_L y = x + C_L·Be,   H y = HBe.
Since x is uniform and independent of (C, Be), conditioning on (y, C) is
information-equivalent to conditioning on (C_L·Be, HBe, C).  Hence
    H(C_L·Be | HBe, C) = H(x | y, C)      (THEOREM, for full-rank C).
We therefore compute H(x|y,C) restricted to full-rank C.  This is the same as
n - I(x;y|C) on the same restricted distribution.

The computation is exact integer-count based, row-factored (never enumerating
2^{4m} matrices), and uses the 90-ordered-basis model established in Track II.

Families
--------
* uniform-B-per-A            : B ~ Unif(F_2^{m x 4}) per A.
* lambda-coupled rows        : with prob λ all rows equal a uniform r;
                               with prob 1-λ rows i.i.d. uniform.
* lambda-column-pair-coupled : with prob λ columns satisfy col0=col1=s,
                               col2=col3=t (s,t uniform i.i.d.);
                               with prob 1-λ rows i.i.d. uniform.

Claims and labels
-----------------
* H(C_L·Be|HBe,C) = H(x|y,C) for full-rank C — THEOREM (linear bijection + x uniform).
* Exact values at n=2, m≤7 for uniform-B and the two marginal-uniform families —
  EVIDENCE.
* The entropy stays bounded away from n=2 as m grows at fixed n=2 (it decreases
  toward ≈1.5 bits for uniform-B).  Whether it approaches n when n grows is OPEN.
* lem:m1's heavy-row bound is per-coordinate; it does not directly imply the
  joint entropy H(C_L·Be|HBe,C) is ≥ n - o(n) — CONJECTURE/OPEN.

Guards
------
L1 exact arithmetic: integer-count ratios; probabilities exact rationals.
L2 J-twist duality: inspected directly in (C,y) space.
L3 query-class hygiene: information-theoretic entropy, no query-class restriction.
L4 never transform the comparison distribution: no LPN comparison used.
PRE-REGISTER: quantity = H(C_L·Be | HBe, C) in bits conditioned on full-rank C;
model = single-block reduction noise decomposition; closure-grade = fixed-n.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import apply_matrix


# ---------------------------------------------------------------------------
# Symplectic helpers (n=2)
# ---------------------------------------------------------------------------

def symplectic_form(u: int, v: int) -> int:
    return (
        ((u >> 0) & 1) * ((v >> 2) & 1)
        ^ ((u >> 1) & 1) * ((v >> 3) & 1)
        ^ ((u >> 2) & 1) * ((v >> 0) & 1)
        ^ ((u >> 3) & 1) * ((v >> 1) & 1)
    ) & 1


def all_lagrangian_subspaces() -> list[list[int]]:
    found = set()
    for v1 in range(1, 1 << 4):
        for v2 in range(v1 + 1, 1 << 4):
            if symplectic_form(v1, v2) != 0:
                continue
            span = frozenset({0, v1, v2, v1 ^ v2})
            found.add(span)
    return [sorted(s) for s in found]


def ordered_isotropic_bases() -> list[tuple[int, int]]:
    bases = []
    for L in all_lagrangian_subspaces():
        nz = [v for v in L if v != 0]
        for a0 in nz:
            for a1 in nz:
                if a0 != a1 and {0, a0, a1, a0 ^ a1} == set(L):
                    bases.append((a0, a1))
    return bases


# ---------------------------------------------------------------------------
# F_2 linear algebra helpers
# ---------------------------------------------------------------------------

def matrix_rank_f2(rows: list[int], n_cols: int) -> int:
    pivots = {}
    for r in rows:
        x = r & ((1 << n_cols) - 1)
        if x == 0:
            continue
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return len(pivots)


def c_rows_from_key(C_key: int, m: int, n: int) -> list[int]:
    """Return the m rows of C as n-bit integers; C_key encodes columns low-bit-first."""
    rows = []
    for i in range(m):
        row = 0
        for j in range(n):
            if (C_key >> (j * m + i)) & 1:
                row |= 1 << j
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Conditional mutual information helpers
# ---------------------------------------------------------------------------

def conditional_mi_bits(counts_by_x: list[list[int]], denom: int, m: int, n: int) -> float:
    nx = 1 << n
    size = 1 << ((n + 1) * m)
    mask_y = (1 << m) - 1
    num_c = 1 << (n * m)
    inv_denom = 1.0 / float(denom)
    joint = [[0.0] * size for _ in range(nx)]
    p_c = [0.0] * num_c
    p_cx = [[0.0] * num_c for _ in range(nx)]
    p_cy = [[0.0] * (1 << m) for _ in range(num_c)]
    for x in range(nx):
        row = counts_by_x[x]
        jx = joint[x]
        pcx_x = p_cx[x]
        for key, cnt in enumerate(row):
            if cnt == 0:
                continue
            prob = cnt * inv_denom
            jx[key] = prob
            c_key = key >> m
            y = key & mask_y
            p_c[c_key] += prob
            pcx_x[c_key] += prob
            p_cy[c_key][y] += prob
    mi = 0.0
    for x in range(nx):
        jx = joint[x]
        pcx_x = p_cx[x]
        for key, prob in enumerate(jx):
            if prob == 0.0:
                continue
            c_key = key >> m
            y = key & mask_y
            denom_term = pcx_x[c_key] * p_cy[c_key][y]
            if denom_term == 0.0:
                continue
            mi += prob * math.log2(prob * p_c[c_key] / denom_term)
    return mi


def mi_and_entropy_restricted_fullrank(
    counts_by_x: list[list[int]], m: int, n: int
) -> dict:
    """Compute I(x;y|C) and H(x|y,C) conditioned on C full-rank."""
    nx = 1 << n
    size = 1 << ((n + 1) * m)
    num_c = 1 << (n * m)

    full_counts = [[0] * size for _ in range(nx)]
    rank_full = 0
    rank_deficient = 0
    for x in range(nx):
        row = counts_by_x[x]
        full_row = full_counts[x]
        for key, cnt in enumerate(row):
            if cnt == 0:
                continue
            C_key = key >> m
            C_rows = c_rows_from_key(C_key, m, n)
            if matrix_rank_f2(C_rows, n) == n:
                full_row[key] += cnt
                rank_full += cnt
            else:
                rank_deficient += cnt

    denom_full = sum(sum(row) for row in full_counts)
    total = rank_full + rank_deficient
    P_full = rank_full / total if total > 0 else 0.0
    if denom_full == 0:
        return {
            "I_xy_given_C_fullrank_bits": None,
            "H_x_given_y_C_fullrank_bits": None,
            "H_equiv_C_L_Be_given_H_Be_C_fullrank_bits": None,
            "rank_full": rank_full,
            "rank_deficient": rank_deficient,
            "P_fullrank": P_full,
        }

    I_full = conditional_mi_bits(full_counts, denom_full, m, n)
    H_x_given_y_C = n - I_full

    return {
        "I_xy_given_C_fullrank_bits": I_full,
        "H_x_given_y_C_fullrank_bits": H_x_given_y_C,
        "H_equiv_C_L_Be_given_H_Be_C_fullrank_bits": H_x_given_y_C,
        "rank_full": rank_full,
        "rank_deficient": rank_deficient,
        "P_fullrank": P_full,
    }


# ---------------------------------------------------------------------------
# Uniform-B-per-A counts P(x,C,y), n=2
# ---------------------------------------------------------------------------

def uniform_B_per_A_counts_by_x(
    m: int, bases: list[tuple[int, int]]
) -> tuple[list[list[int]], int]:
    nx = 1 << 2
    size = 1 << (3 * m)
    mask = (1 << m) - 1
    num_c = 1 << (2 * m)
    counts = [[0] * size for _ in range(nx)]

    c_lists = [[0] * num_c for _ in range(2)]
    for C_key in range(num_c):
        tmp = C_key
        c_lists[0][C_key] = tmp & mask
        tmp >>= m
        c_lists[1][C_key] = tmp & mask

    two_to_2m = 1 << (2 * m)
    two_to_m = 1 << m
    total_error_weight = 256

    for a0, a1 in bases:
        span_map = {0: (0, 0), a0: (1, 0), a1: (0, 1), a0 ^ a1: (1, 1)}
        for x in range(nx):
            case3_weight_sum = 0
            for e in range(1 << 4):
                w_e = 3 ** (4 - e.bit_count())
                a = 0
                if x & 1:
                    a ^= a0
                if x & 2:
                    a ^= a1
                v = a ^ e
                if v == 0:
                    add = w_e * two_to_2m
                    for C_key in range(num_c):
                        counts[x][(C_key << m)] += add
                elif v in span_map:
                    alpha, beta = span_map[v]
                    add = w_e * two_to_2m
                    for C_key in range(num_c):
                        y = 0
                        if alpha:
                            y ^= c_lists[1][C_key]
                        if beta:
                            y ^= c_lists[0][C_key]
                        counts[x][(C_key << m) | y] += add
                else:
                    case3_weight_sum += w_e
            case3_add = case3_weight_sum * two_to_m
            for key in range(size):
                counts[x][key] += case3_add

    denom = len(bases) * nx * total_error_weight * (1 << (4 * m))
    return counts, denom


# ---------------------------------------------------------------------------
# Track-BB marginal-uniform families, n=2
# ---------------------------------------------------------------------------

def constant_rows_B_counts_by_x(
    m: int, bases: list[tuple[int, int]]
) -> tuple[list[list[int]], int]:
    nx = 1 << 2
    size = 1 << (3 * m)
    mask = (1 << m) - 1
    counts = [[0] * size for _ in range(nx)]

    for r in range(1 << 4):
        B_cols = [mask if ((r >> j) & 1) else 0 for j in range(4)]
        Bx = [apply_matrix(B_cols, v) & mask for v in range(1 << 4)]
        for a0, a1 in bases:
            c0 = Bx[a0]
            c1 = Bx[a1]
            C_key = (c0 << m) | c1
            for x in range(nx):
                a = 0
                if x & 1:
                    a ^= a0
                if x & 2:
                    a ^= a1
                for e in range(1 << 4):
                    v = a ^ e
                    y = Bx[v]
                    key = (C_key << m) | y
                    counts[x][key] += 3 ** (4 - e.bit_count())

    denom = (1 << 4) * len(bases) * nx * (1 << 4)
    return counts, denom


def column_pair_coupled_B_counts_by_x(
    m: int, bases: list[tuple[int, int]]
) -> tuple[list[list[int]], int]:
    nx = 1 << 2
    size = 1 << (3 * m)
    mask = (1 << m) - 1
    counts = [[0] * size for _ in range(nx)]

    for s in range(1 << m):
        for t in range(1 << m):
            B_cols = [s, s, t, t]
            Bx = [apply_matrix(B_cols, v) & mask for v in range(1 << 4)]
            for a0, a1 in bases:
                c0 = Bx[a0]
                c1 = Bx[a1]
                C_key = (c0 << m) | c1
                for x in range(nx):
                    a = 0
                    if x & 1:
                        a ^= a0
                    if x & 2:
                        a ^= a1
                    for e in range(1 << 4):
                        v = a ^ e
                        y = Bx[v]
                        key = (C_key << m) | y
                        counts[x][key] += 3 ** (4 - e.bit_count())

    denom = (1 << (2 * m)) * len(bases) * nx * (1 << 4)
    return counts, denom


def mix_counts_by_x(
    lam: Fraction,
    counts_a: list[list[int]],
    denom_a: int,
    counts_b: list[list[int]],
    denom_b: int,
) -> tuple[list[list[int]], int]:
    if not (0 <= lam <= 1):
        raise ValueError("lam must be in [0,1]")
    scale = denom_a // denom_b
    p = lam.numerator
    q = lam.denominator
    mixed = [
        [(q - p) * u + p * (c * scale) for u, c in zip(ux, cx)]
        for ux, cx in zip(counts_a, counts_b)
    ]
    denom = q * denom_a
    return mixed, denom


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_experiment(max_m: int = 7, output_dir: Path | None = None):
    n = 2
    bases = ordered_isotropic_bases()
    lambda_values = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]

    results = {
        "track": "JJ",
        "experiment": 810,
        "quantity": "H(C_L·Be | HBe, C) bits (full-rank C)",
        "standing_guards": ["L1 exact arithmetic", "L2 J-twist duality", "L3 query-class hygiene", "L4 never transform LPN"],
        "modeling_choices": {
            "A_ensemble": "uniform ordered basis of a uniform Lagrangian (90 ordered bases for n=2)",
            "rank_condition": "conditioned on C full column rank",
            "ambient_noise": "Bernoulli(1/4)^{2n}",
            "identity_used": "H(C_L·Be|HBe,C) = H(x|y,C) for full-rank C (THEOREM)",
        },
        "n": n,
        "num_ordered_bases": len(bases),
        "rows": [],
    }

    for m in range(n, max_m + 1):
        print(f"n={n}, m={m}", file=sys.stderr)
        t0 = time.time()

        uniform_counts, uniform_denom = uniform_B_per_A_counts_by_x(m, bases)
        uniform_res = mi_and_entropy_restricted_fullrank(uniform_counts, m, n)

        constant_counts, constant_denom = constant_rows_B_counts_by_x(m, bases)
        coupled_counts, coupled_denom = column_pair_coupled_B_counts_by_x(m, bases)

        row = {
            "m": m,
            "uniform_B_per_A": uniform_res,
            "lambda_coupled_rows": [],
            "lambda_column_pair_coupled": [],
        }

        for lam in lambda_values:
            mixed_counts, mixed_denom = mix_counts_by_x(
                lam, uniform_counts, uniform_denom, constant_counts, constant_denom
            )
            lam_res = mi_and_entropy_restricted_fullrank(mixed_counts, m, n)
            row["lambda_coupled_rows"].append({
                "lambda": str(lam),
                "H_C_L_Be_given_H_Be_C_fullrank_bits": lam_res["H_equiv_C_L_Be_given_H_Be_C_fullrank_bits"],
                "I_xy_given_C_fullrank_bits": lam_res["I_xy_given_C_fullrank_bits"],
                "P_fullrank": lam_res["P_fullrank"],
            })
            del mixed_counts

        for lam in lambda_values:
            mixed_counts, mixed_denom = mix_counts_by_x(
                lam, uniform_counts, uniform_denom, coupled_counts, coupled_denom
            )
            lam_res = mi_and_entropy_restricted_fullrank(mixed_counts, m, n)
            row["lambda_column_pair_coupled"].append({
                "lambda": str(lam),
                "H_C_L_Be_given_H_Be_C_fullrank_bits": lam_res["H_equiv_C_L_Be_given_H_Be_C_fullrank_bits"],
                "I_xy_given_C_fullrank_bits": lam_res["I_xy_given_C_fullrank_bits"],
                "P_fullrank": lam_res["P_fullrank"],
            })
            del mixed_counts

        row["elapsed_seconds"] = time.time() - t0
        results["rows"].append(row)
        print(json.dumps(row, indent=2), file=sys.stderr)
        del uniform_counts, constant_counts, coupled_counts

    if output_dir is None:
        output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "810-trackJJ-noise-decomposition-entropy.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-m", type=int, default=7, help="maximum m to compute")
    parser.add_argument("--output-dir", type=Path, default=None, help="output directory")
    args = parser.parse_args()
    run_experiment(max_m=args.max_m, output_dir=args.output_dir)
