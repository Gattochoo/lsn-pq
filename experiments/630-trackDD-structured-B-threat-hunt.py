#!/usr/bin/env python3
"""
630 (Track DD): threat-hunt exact SD for new structured marginal-uniform B families.

Standing baseline (Gemini W=0 spike): for every marginal-uniform B, SD to matched
LPN is at least q_graph(2) = 29/64, but q_graph(n) -> 0.  This script asks whether
any *structured* marginal-uniform B family can push SD *below* the uniform-B-per-A
baseline (the lem:m2-breaking direction).

Families examined:
  1. UCS-r  (uniform column-subspace of rank r):
     Choose an r-dimensional subspace S <= F_2^4 uniformly; rows of B are i.i.d.
     uniform over S.  r=4 is the uniform-B-per-A baseline; r<4 is structured.
     Exact marginal-uniformity holds because S is uniform.
  2. Block-b (identical rows inside blocks of size b):
     Partition the m rows into blocks of size b; each block has one uniform row
     repeated b times.  b=1 is the baseline; b=m is the constant-rows family.
     Exact marginal-uniformity holds row-wise.
  3. Parity-s (rows i.i.d. uniform conditioned on global row-XOR = s):
     A support-spreading / column-balance constraint.  s=0 is the even-parity
     case; a nonzero s is also included.  Exact marginal-uniformity holds for
     every row (the conditioning only ties rows together).

Comparison distributions (L4: never transform the comparison distribution):
  * primary:  LPN_{p_eff} with p_eff(2) = (1 - (3/4)^4)/2 = 175/512
              (matched per-coordinate output rate for n=2).
  * reference: LPN_{1/4} (ambient noise rate), reported for context only.

Guards:
  L1 exact arithmetic: all SDs are Fractions; JSON stores string fractions.
  L2 J-twist duality: output distribution inspected directly in (C,y) space.
  L3 query-class hygiene: unrestricted exact total-variation only.
  L4 comparison = matched-rate LPN, untransformed.

PRE-REGISTER interpretation guards:
  * n-axis: fixed n = 2 (exact finite regime).
  * m-axis: small m = 2,...,MAX_M; no asymptotic extrapolation.
  * Negative / no-go: if every structured family has SD >= uniform-B baseline,
    that is reported as a first-class negative result, not a lem:m2 theorem.
  * CLOSURE-GRADE: fixed-n constants are not conflated with asymptotic rates.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

import argparse
import json
import math
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    randomized_uniform_B_counts,
    reduction_counts_for_B,
)


# ---------------------------------------------------------------------------
# Small linear-algebra helpers
# ---------------------------------------------------------------------------

def independent(vecs):
    """Check whether a tuple/list of F_2^4 vectors is linearly independent."""
    span = {0}
    for v in vecs:
        if v in span:
            return False
        span = span | {x ^ v for x in span}
    return True


def span_set(vecs):
    """Return the sorted list of vectors in the span of vecs."""
    s = {0}
    for v in vecs:
        s = s | {x ^ v for x in s}
    return tuple(sorted(s))


def all_subspaces_of_dim(r):
    """Return one basis per r-dimensional subspace of F_2^4."""
    if r == 4:
        return [[1, 2, 4, 8]]
    seen = {}
    for combo in combinations(range(1, 16), r):
        if not independent(combo):
            continue
        key = frozenset(span_set(combo))
        if key not in seen:
            seen[key] = list(combo)
    return list(seen.values())


def dot_basis_for_subspace(basis):
    """
    For a subspace basis b_0,...,b_{r-1} return db[a] = r-bit integer whose
    j-th bit is b_j . a (dot product in F_2^4).
    """
    db = [0] * 16
    for a in range(16):
        val = 0
        for j, b in enumerate(basis):
            if bin(b & a).count("1") & 1:
                val |= 1 << j
        db[a] = val
    return db


def subspace_basis(patterns):
    """Given a set of vectors in F_2^3, return a basis for the span."""
    pat_list = sorted(patterns)
    b = []
    span_seen = {0}
    for p in pat_list:
        if p not in span_seen:
            b.append(p)
            span_seen = span_seen | {x ^ p for x in span_seen}
    return b


def place_pattern_at_row(p, i, m):
    """Place a 3-bit pattern p=(s0,s1,s2) into row i of the (C,y) key."""
    key = 0
    if p & 4:  # s0 -> c0 high block
        key |= 1 << (2 * m + i)
    if p & 2:  # s1 -> c1 middle block
        key |= 1 << (m + i)
    if p & 1:  # s2 -> y low block
        key |= 1 << i
    return key


# ---------------------------------------------------------------------------
# Triple enumeration shared by all families
# ---------------------------------------------------------------------------

def iter_triples(bases):
    """Yield (a0, a1, x, e, weight) for the n=2 reduction."""
    for a0, a1 in bases:
        for x in range(4):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(16):
                w = e.bit_count()
                weight = 3 ** (4 - w)
                v = a ^ e
                yield a0, a1, x, e, weight, v


# ---------------------------------------------------------------------------
# Family 1: uniform column-subspace of rank r (UCS-r)
# ---------------------------------------------------------------------------

def ucs_counts(r, m, bases):
    """
    Exact integer counts for (C,y) when B is generated by:
        S ~ Uniform(r-dimensional subspace of F_2^4),
        rows of B ~ i.i.d. Uniform(S).
    The distribution is exactly marginal-uniform because S is uniform.
    """
    size = 1 << (3 * m)
    counts = [0] * size
    subspaces = all_subspaces_of_dim(r)

    # Precompute dot-basis representations for every subspace.
    db_list = [dot_basis_for_subspace(basis) for basis in subspaces]

    # Aggregate weights W[I] where I is the per-row pattern subspace in F_2^3.
    W = {}
    for a0, a1, x, e, weight, v in iter_triples(bases):
        for db in db_list:
            f0 = db[a0]
            f1 = db[a1]
            fv = db[v]
            patterns = set()
            for u in range(1 << r):
                p = 0
                if bin(u & f0).count("1") & 1:
                    p |= 4
                if bin(u & f1).count("1") & 1:
                    p |= 2
                if bin(u & fv).count("1") & 1:
                    p |= 1
                patterns.add(p)
            d = (len(patterns) - 1).bit_length()
            I_key = tuple(sorted(patterns))
            W[I_key] = W.get(I_key, 0) + (weight << ((r - d) * m))

    # Expand each pattern subspace I to I^m and add its weight.
    for I_key, wt in W.items():
        bas = subspace_basis(set(I_key))
        all_pat = [0]
        for g in bas:
            all_pat = all_pat + [p ^ g for p in all_pat]
        placed = [[place_pattern_at_row(p, i, m) for p in all_pat] for i in range(m)]
        keys = [0]
        for i in range(m):
            keys = [k | placed[i][idx] for k in keys for idx in range(len(all_pat))]
        for k in keys:
            counts[k] += wt

    denom = len(subspaces) * (1 << (r * m)) * 15360
    return counts, denom


# ---------------------------------------------------------------------------
# Family 2: identical rows inside blocks of size b (Block-b)
# ---------------------------------------------------------------------------

def block_counts(b, m, bases):
    """
    Exact integer counts for (C,y) when rows are grouped into blocks of size b
    and all rows inside a block are equal (b must divide m).  Each block value
    is uniform over F_2^4.  b=1 is the i.i.d. uniform baseline.
    """
    if m % b != 0:
        raise ValueError(f"block size {b} must divide m={m}")
    t = m // b
    size = 1 << (3 * m)
    counts = [0] * size

    # Here rows range over the whole F_2^4, so r=4 and the pattern subspace I
    # is the image of a0, a1, v under the full dual.
    W = {}
    db = dot_basis_for_subspace([1, 2, 4, 8])  # full space
    for a0, a1, x, e, weight, v in iter_triples(bases):
        f0 = db[a0]
        f1 = db[a1]
        fv = db[v]
        patterns = set()
        for u in range(16):
            p = 0
            if bin(u & f0).count("1") & 1:
                p |= 4
            if bin(u & f1).count("1") & 1:
                p |= 2
            if bin(u & fv).count("1") & 1:
                p |= 1
            patterns.add(p)
        d = (len(patterns) - 1).bit_length()
        I_key = tuple(sorted(patterns))
        W[I_key] = W.get(I_key, 0) + (weight << ((4 - d) * t))

    # Place a pattern p repeated b times in block j.
    def place_block_pattern(p, j):
        key = 0
        base = j * b
        if p & 4:
            for k in range(b):
                key |= 1 << (2 * m + base + k)
        if p & 2:
            for k in range(b):
                key |= 1 << (m + base + k)
        if p & 1:
            for k in range(b):
                key |= 1 << (base + k)
        return key

    for I_key, wt in W.items():
        bas = subspace_basis(set(I_key))
        all_pat = [0]
        for g in bas:
            all_pat = all_pat + [p ^ g for p in all_pat]
        placed = [place_block_pattern(p, j) for p in all_pat for j in range(t)]
        # Build keys by choosing one pattern per block.
        keys = [0]
        for j in range(t):
            start = j * len(all_pat)
            block_placed = placed[start : start + len(all_pat)]
            keys = [k | block_placed[idx] for k in keys for idx in range(len(all_pat))]
        for k in keys:
            counts[k] += wt

    denom = (16 ** t) * 15360
    return counts, denom


# ---------------------------------------------------------------------------
# Family 3: rows i.i.d. uniform conditioned on global row-XOR = s (Parity-s)
# ---------------------------------------------------------------------------

def rows_to_columns(rows, n_cols):
    """Convert a list of row bitmasks to column bitmasks (m-bit ints)."""
    m = len(rows)
    cols = [0] * n_cols
    for j in range(n_cols):
        for i, r in enumerate(rows):
            if (r >> j) & 1:
                cols[j] |= 1 << i
    return cols


def parity_counts(s_target, m, bases):
    """
    Exact integer counts for (C,y) when B's rows are i.i.d. uniform over F_2^4
    conditioned on XOR_i row_i = s_target.  The row marginal is uniform for m>=2.
    Computed by enumerating the first m-1 rows and forcing the last row.
    """
    if m < 2:
        raise ValueError("parity family requires m >= 2")
    size = 1 << (3 * m)
    counts = [0] * size
    first = m - 1
    total = 0
    for assignment in range(16 ** first):
        rows = []
        tmp = assignment
        s_sum = 0
        for _ in range(first):
            r = tmp & 15
            tmp >>= 4
            rows.append(r)
            s_sum ^= r
        rows.append(s_target ^ s_sum)
        B_cols = rows_to_columns(rows, 4)
        c = reduction_counts_for_B(B_cols, bases, m)
        for i, val in enumerate(c):
            counts[i] += val
        total += 1
    denom = total * 15360
    return counts, denom


# ---------------------------------------------------------------------------
# SD evaluation
# ---------------------------------------------------------------------------

def p_eff_n2():
    """Matched per-coordinate output noise rate for uniform B at n=2."""
    return Fraction(1 - Fraction(3, 4) ** 4, 2)


def evaluate_family(name, counts, denom, lpn_counts, lpn_denom, baseline_counts, baseline_denom):
    sd_lpn = exact_sd_counts(counts, denom, lpn_counts, lpn_denom)
    sd_baseline = exact_sd_counts(counts, denom, baseline_counts, baseline_denom)
    return {
        "family": name,
        "sd_to_matched_lpn": str(sd_lpn),
        "sd_to_matched_lpn_float": float(sd_lpn),
        "delta_sd_vs_uniform_B": str(sd_baseline),
        "delta_sd_vs_uniform_B_float": float(sd_baseline),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--max-m", type=int, default=6, help="maximum m to compute")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    max_m = args.max_m
    if not 2 <= max_m <= 6:
        raise ValueError("this experiment supports 2 <= max-m <= 6")

    bases = list(enumerate_lagrangian_bases())
    p_matched = p_eff_n2()
    p_ambient = Fraction(1, 4)

    results = []

    for m in range(2, max_m + 1):
        print(f"m = {m}", flush=True)
        size = 1 << (3 * m)

        lpn_matched_counts, lpn_matched_denom = lpn_target_counts(m, p_matched)
        lpn_ambient_counts, lpn_ambient_denom = lpn_target_counts(m, p_ambient)
        baseline_counts, baseline_denom = randomized_uniform_B_counts(m, bases)

        # Sanity: baseline SD to matched LPN should equal itself.
        baseline_sd_check = exact_sd_counts(
            baseline_counts, baseline_denom, lpn_matched_counts, lpn_matched_denom
        )

        family_results = []

        # UCS-r families
        for r in (1, 2, 3, 4):
            print(f"  UCS-r = {r} ...", flush=True)
            counts, denom = ucs_counts(r, m, bases)
            family_results.append(
                evaluate_family(
                    f"UCS-r{r}", counts, denom,
                    lpn_matched_counts, lpn_matched_denom,
                    baseline_counts, baseline_denom,
                )
            )

        # Block-b families
        for b in (2, 3):
            if m % b == 0:
                print(f"  Block-b = {b} ...", flush=True)
                counts, denom = block_counts(b, m, bases)
                family_results.append(
                    evaluate_family(
                        f"Block-b{b}", counts, denom,
                        lpn_matched_counts, lpn_matched_denom,
                        baseline_counts, baseline_denom,
                    )
                )
        # Constant rows (b=m) is marginal-uniform and is a useful endpoint.
        print(f"  Block-b=m (constant rows) ...", flush=True)
        counts, denom = block_counts(m, m, bases)
        family_results.append(
            evaluate_family(
                "Block-b=m_constant_rows", counts, denom,
                lpn_matched_counts, lpn_matched_denom,
                baseline_counts, baseline_denom,
            )
        )

        # Parity-s families (direct enumeration; keep to m<=4 for tractability)
        if m <= 4:
            for s_label, s_val in (("s=0", 0), ("s!=0", 1)):
                print(f"  Parity-{s_label} ...", flush=True)
                counts, denom = parity_counts(s_val, m, bases)
                family_results.append(
                    evaluate_family(
                        f"Parity-{s_label}", counts, denom,
                        lpn_matched_counts, lpn_matched_denom,
                        baseline_counts, baseline_denom,
                    )
                )

        # Determine whether any family beat the baseline toward LPN.
        baseline_sd = exact_sd_counts(
            baseline_counts, baseline_denom,
            lpn_matched_counts, lpn_matched_denom,
        )
        min_row = min(
            family_results,
            key=lambda r: Fraction(r["sd_to_matched_lpn"]),
        )
        min_sd = Fraction(min_row["sd_to_matched_lpn"])
        threat = min_sd < baseline_sd

        results.append({
            "m": m,
            "baseline_sd_to_matched_lpn": str(baseline_sd),
            "baseline_sd_to_matched_lpn_float": float(baseline_sd),
            "baseline_sd_sanity_check": str(baseline_sd_check),
            "baseline_sd_sanity_check_float": float(baseline_sd_check),
            "families": family_results,
            "minimum_sd_family": min_row["family"],
            "minimum_sd_value": min_row["sd_to_matched_lpn"],
            "minimum_sd_value_float": min_row["sd_to_matched_lpn_float"],
            "threat_detected": threat,
        })

    final = {
        "experiment": "630-trackDD-structured-B-threat-hunt",
        "n": 2,
        "max_m": max_m,
        "p_eff_n2": str(p_matched),
        "p_ambient": str(p_ambient),
        "num_lagrangian": len(bases),
        "q_graph_n2": "29/64",
        "interpretation": {
            "comparison_primary": "LPN_{175/512} (matched per-coordinate output rate, L4)",
            "comparison_reference": "LPN_{1/4} (ambient noise rate, not used for primary claims)",
            "baseline": "uniform-B-per-A (UCS-r=4 / Block-b=1)",
            "threat_criterion": "any structured marginal-uniform family has SD < uniform-B baseline",
            "negative_result_criterion": "all structured families have SD >= uniform-B baseline",
            "closure_grade": "fixed-n exact results; q_graph(2)=29/64 is a constant, not an asymptotic rate",
        },
        "results": results,
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"630-trackDD-structured-B-threat-hunt-maxM{max_m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(final, f, indent=2)
    print(f"Saved: {out_path}", flush=True)


if __name__ == "__main__":
    main()
