#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""730 (Track HH): permutation-of-uniform fresh-B family — exact SD at n=2.

This is the final structured fresh-B threat sweep for the randomized
marginal-adaptive residual.  The family is:

    B is a uniformly random ordered m-tuple of *distinct* vectors in F_2^4.

Equivalently: choose an m-subset of F_2^4 uniformly and then choose a uniform
ordering.  Every row of B is marginally uniform over F_2^4, so lem:m1 is
satisfied.  The structure is the "no repeated rows" / balanced-row-histogram
constraint (a permutation-of-uniform design).  It is fresh-B in the sense that
a new independent B is drawn for each reduction sample.

We compute the *exact* statistical distance at n=2, m=2..6 between the
reduction output (C,y) and matched-rate LPN_{p_eff(2)=175/512}.  Because both
distributions are exchangeable under row permutations, the full total-variation
can be computed on count-vectors of output patterns, avoiding the 2^{3m} joint
space.  A brute-force sanity check for m=4 is included.

Standing guards
---------------
L1 exact arithmetic: all probabilities are Fractions/integer counts; JSON stores
    string fractions.
L2 J-twist duality: output distribution is inspected directly in (C,y) pattern
    space; no Fourier/J-twist dual rewriting.
L3 query-class hygiene: the reported SD is the unrestricted exact total
    variation on count-vectors (equivalent to full (C,y) TV by exchangeability).
L4 never transform the comparison distribution: the LPN target is the standard
    matched-rate product distribution over (C,y), untransformed.

PRE-REGISTER interpretation guards
----------------------------------
* Model: fresh-B, one independent B per sample; B rows distinct and marginally
  uniform.  This is the residual model after shared-B is closed by stacked-rank.
* Quantity: exact SD((C,y), LPN_{175/512}) at n=2.
* n-axis: fixed n=2 exact finite results; no asymptotic n extrapolation.
* m-axis: small m=2..6.
* Baseline: uniform-B-per-A (i.i.d. uniform rows with repetitions allowed) from
  Track DD (exp 630).
* Threat criterion: SD below the uniform-B baseline (i.e. closer to LPN).
* Negative/no-go: if SD is not below baseline, this is a first-class negative
  result, not a lem:m2 theorem.
* CLOSURE-GRADE: fixed-n constants are not conflated with asymptotic rates.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import (
    apply_matrix,
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    randomized_uniform_B_counts,
)


# ---------------------------------------------------------------------------
# Basic parameters
# ---------------------------------------------------------------------------

def p_eff_n2() -> Fraction:
    """Matched per-coordinate output noise rate for uniform marginal B at n=2."""
    return Fraction(1 - Fraction(3, 4) ** 4, 2)


def q_graph_n2() -> Fraction:
    """B-agnostic Pr[W=0] averaged over uniform Lagrangian A at n=2."""
    pz = Fraction(3, 4) ** 4
    return pz + (1 - pz) / (2 ** 2 + 1)


# ---------------------------------------------------------------------------
# Count-vector machinery
# ---------------------------------------------------------------------------

def generate_count_vectors(m: int):
    """Yield all 8-tuples of nonnegative ints summing to m."""
    def rec(remaining, start, prefix):
        if len(prefix) == 7:
            yield tuple(prefix + [remaining])
            return
        for v in range(remaining + 1):
            yield from rec(remaining - v, start, prefix + [v])
    yield from rec(m, 0, [])


def multinomial_count(c: tuple[int, ...]) -> int:
    """m! / prod c_p!  (number of ordered keys with count vector c)."""
    total = math.factorial(sum(c))
    for v in c:
        total //= math.factorial(v)
    return total


def falling_factorial(n: int, k: int) -> int:
    """n * (n-1) * ... * (n-k+1), with value 1 when k=0."""
    if k < 0 or k > n:
        return 0
    res = 1
    for i in range(k):
        res *= n - i
    return res


def image_of_phi(a0: int, a1: int, v: int) -> frozenset:
    """Return the image subspace I = { (r·a0, r·a1, r·v) : r in F_2^4 }.

    The result is a frozenset of 3-bit output patterns.
    """
    patterns = set()
    for r in range(16):
        s0 = (bin(r & a0).count("1") & 1)
        s1 = (bin(r & a1).count("1") & 1)
        s2 = (bin(r & v).count("1") & 1)
        p = (s0 << 2) | (s1 << 1) | s2
        patterns.add(p)
    return frozenset(patterns)


def image_weights(bases: list[tuple[int, int]]) -> dict[frozenset, int]:
    """Total 3^{4-|e|} weight for each possible image subspace I."""
    weights = defaultdict(int)
    for a0, a1 in bases:
        span = {0, a0, a1, a0 ^ a1}
        for x in range(4):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(16):
                weight = 3 ** (4 - e.bit_count())
                v = a ^ e
                I = image_of_phi(a0, a1, v)
                weights[I] += weight
    return dict(weights)


def count_vector_counts(
    m: int,
    image_weights: dict[frozenset, int],
    injections: bool,
) -> tuple[dict[tuple[int, ...], int], int]:
    """Exact integer counts for the count-vector distribution of (C,y).

    If injections=True: B is a random injection (distinct rows).
    If injections=False: B has i.i.d. uniform rows (baseline uniform-B-per-A).
    """
    if injections:
        total_b = math.perm(16, m)
    else:
        total_b = 16 ** m

    total_weight = sum(image_weights.values())  # = 15360
    denom = total_weight * total_b

    counts = defaultdict(int)
    for I, wt in image_weights.items():
        np = 4 if len(I) == 4 else 2
        for c in generate_count_vectors(m):
            if any(c[p] != 0 for p in range(8) if p not in I):
                continue
            mult = multinomial_count(c)
            if injections:
                # Distinct rows: at most np rows can land in a given pattern.
                if any(c[p] > np for p in I):
                    continue
                prod = 1
                for p in I:
                    prod *= falling_factorial(np, c[p])
            else:
                # I.i.d. rows with replacement: N_p^{c_p} even if c_p > np.
                prod = np ** sum(c[p] for p in I)
            if prod == 0:
                continue
            counts[c] += wt * mult * prod

    return dict(counts), denom


# ---------------------------------------------------------------------------
# LPN target count-vector distribution
# ---------------------------------------------------------------------------

def lpn_count_vector_counts(m: int) -> tuple[dict[tuple[int, ...], int], int]:
    """Exact integer counts for LPN_{p_eff} count-vector distribution."""
    p = p_eff_n2()
    num = p.numerator
    den = p.denominator
    nx = 4
    num_c = 1 << (2 * m)
    counts = defaultdict(int)
    mask = (1 << m) - 1

    for C_key in range(num_c):
        c0 = C_key & mask
        c1 = (C_key >> m) & mask
        for x in range(nx):
            x0 = (x >> 0) & 1
            x1 = (x >> 1) & 1
            for e in range(1 << m):
                w = e.bit_count()
                weight = (num ** w) * ((den - num) ** (m - w))
                vec = [0] * 8
                y = 0
                for i in range(m):
                    s0 = (c0 >> i) & 1
                    s1 = (c1 >> i) & 1
                    ei = (e >> i) & 1
                    yi = (s0 * x0) ^ (s1 * x1) ^ ei
                    ptn = (s0 << 2) | (s1 << 1) | yi
                    vec[ptn] += 1
                    if yi:
                        y |= 1 << i
                counts[tuple(vec)] += weight

    denom = nx * num_c * (den ** m)
    return dict(counts), denom


# ---------------------------------------------------------------------------
# Exact SD on count-vector dictionaries
# ---------------------------------------------------------------------------

def exact_sd_dict(d1: dict, denom1: int, d2: dict, denom2: int) -> Fraction:
    """Exact total variation between two integer-count distributions."""
    keys = set(d1.keys()) | set(d2.keys())
    num = 0
    for k in keys:
        num += abs(d1.get(k, 0) * denom2 - d2.get(k, 0) * denom1)
    return Fraction(num, 2 * denom1 * denom2)


# ---------------------------------------------------------------------------
# W-law (symmetric functional of the output)
# ---------------------------------------------------------------------------

def w_of_count_vector(c: tuple[int, ...]) -> int:
    """W = min_w wt(y + C w) computed from the output-pattern count vector."""
    best = sum(c)  # m
    for w0 in (0, 1):
        for w1 in (0, 1):
            match = 0
            for p in range(8):
                s0 = (p >> 2) & 1
                s1 = (p >> 1) & 1
                s2 = p & 1
                pred = (w0 * s0 + w1 * s1) & 1
                if s2 == pred:
                    match += c[p]
            if sum(c) - match < best:
                best = sum(c) - match
    return best


def w_law_from_vector_dist(dist: dict[tuple[int, ...], Fraction]) -> list[Fraction]:
    """Distribution of W from a count-vector distribution."""
    m = sum(next(iter(dist.keys())))
    out = [Fraction(0) for _ in range(m + 1)]
    for c, prob in dist.items():
        out[w_of_count_vector(c)] += prob
    return out


def w_law_from_counts(counts: list[int], denom: int, m: int) -> list[Fraction]:
    """Distribution of W directly from a (C,y) count list (baseline helper)."""
    dist = [Fraction(0) for _ in range(m + 1)]
    y_mask = (1 << m) - 1
    for key, cnt in enumerate(counts):
        if cnt == 0:
            continue
        y = key & y_mask
        C_key = key >> m
        c0 = (C_key >> m) & y_mask
        c1 = C_key & y_mask
        best = m + 1
        for w0 in (0, 1):
            cw = 0
            if w0:
                cw ^= c0
            for w1 in (0, 1):
                cc = cw
                if w1:
                    cc ^= c1
                wt = (y ^ cc).bit_count()
                if wt < best:
                    best = wt
        dist[best] += Fraction(cnt, denom)
    return dist


def tv_w_laws(a: list[Fraction], b: list[Fraction]) -> Fraction:
    total = Fraction(0)
    for i in range(max(len(a), len(b))):
        av = a[i] if i < len(a) else Fraction(0)
        bv = b[i] if i < len(b) else Fraction(0)
        total += abs(av - bv)
    return total / 2


# ---------------------------------------------------------------------------
# Brute-force sanity check for m=4
# ---------------------------------------------------------------------------

def brute_force_injection_counts(m: int, bases: list[tuple[int, int]]) -> tuple[list[int], int]:
    """Enumerate all injections [m] -> F_2^4 and accumulate (C,y) counts."""
    assert m <= 4, "brute force is only practical for m <= 4"
    size = 1 << (3 * m)
    counts = [0] * size
    mask = (1 << m) - 1

    # Enumerate injections as ordered m-tuples of distinct 4-bit values.
    rows_list = list(range(1 << 4))
    total_b = 0
    for combo in combinations(rows_list, m):
        for perm in permutations(combo):
            total_b += 1
            B_cols = [0] * 4
            for i, r in enumerate(perm):
                for j in range(4):
                    if (r >> j) & 1:
                        B_cols[j] |= 1 << i
            Bx = [apply_matrix(B_cols, v) & mask for v in range(1 << 4)]
            for a0, a1 in bases:
                c0 = Bx[a0]
                c1 = Bx[a1]
                C_key = (c0 << m) | c1
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
                        y = Bx[v]
                        key = (C_key << m) | y
                        counts[key] += weight

    denom = total_b * 15360
    return counts, denom


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run(max_m: int = 6) -> dict:
    bases = list(enumerate_lagrangian_bases())
    img_w = image_weights(bases)
    p_eff = p_eff_n2()

    results = []
    for m in range(2, max_m + 1):
        print(f"m = {m} ...", flush=True)

        # New family: permutation-of-uniform (distinct rows).
        red_counts, red_denom = count_vector_counts(m, img_w, injections=True)
        # Baseline uniform-B-per-A (i.i.d. uniform rows).
        uni_counts, uni_denom = count_vector_counts(m, img_w, injections=False)
        # Matched LPN target.
        lpn_cv_counts, lpn_cv_denom = lpn_count_vector_counts(m)

        sd_red_lpn = exact_sd_dict(red_counts, red_denom, lpn_cv_counts, lpn_cv_denom)
        sd_uni_lpn = exact_sd_dict(uni_counts, uni_denom, lpn_cv_counts, lpn_cv_denom)
        delta = sd_red_lpn - sd_uni_lpn

        # W-law comparison.
        red_dist = {c: Fraction(cnt, red_denom) for c, cnt in red_counts.items()}
        uni_dist = {c: Fraction(cnt, uni_denom) for c, cnt in uni_counts.items()}
        red_w = w_law_from_vector_dist(red_dist)
        uni_w = w_law_from_vector_dist(uni_dist)

        lpn_counts, lpn_denom = lpn_target_counts(m, p_eff)
        lpn_w = w_law_from_counts(lpn_counts, lpn_denom, m)

        tv_red_w = tv_w_laws(red_w, lpn_w)
        tv_uni_w = tv_w_laws(uni_w, lpn_w)

        # Brute-force cross-check for m=4.
        sanity = None
        if m == 4:
            print("  brute-force cross-check ...", flush=True)
            from itertools import permutations
            bf_counts, bf_denom = brute_force_injection_counts(m, bases)
            bf_sd = exact_sd_counts(bf_counts, bf_denom, lpn_counts, lpn_denom)
            sanity = {
                "count_vector_sd": str(sd_red_lpn),
                "brute_force_full_sd": str(bf_sd),
                "agreement": sd_red_lpn == bf_sd,
            }
            print(f"    count-vector SD = {sd_red_lpn}, brute-force SD = {bf_sd}, match = {sd_red_lpn == bf_sd}", flush=True)

        results.append({
            "m": m,
            "permutation_of_uniform": {
                "sd_to_matched_lpn": str(sd_red_lpn),
                "sd_float": float(sd_red_lpn),
                "tv_w_law": str(tv_red_w),
                "tv_w_law_float": float(tv_red_w),
                "denom": str(red_denom),
            },
            "uniform_b_per_a_baseline": {
                "sd_to_matched_lpn": str(sd_uni_lpn),
                "sd_float": float(sd_uni_lpn),
                "tv_w_law": str(tv_uni_w),
                "tv_w_law_float": float(tv_uni_w),
                "denom": str(uni_denom),
            },
            "delta_sd_vs_baseline": str(delta),
            "delta_sd_float": float(delta),
            "threat_detected": sd_red_lpn < sd_uni_lpn,
            "brute_force_sanity_m4": sanity,
        })

    summary = {
        "experiment": 730,
        "track": "HH",
        "family": "permutation-of-uniform-distinct-rows",
        "n": 2,
        "max_m": max_m,
        "p_eff_n2": str(p_eff),
        "q_graph_n2": str(q_graph_n2()),
        "num_lagrangian_bases": len(bases),
        "results": results,
        "claim_labels": {
            "marginal_uniformity": "THEOREM (each row is uniform over F_2^4 by symmetry of random injection)",
            "fresh_B_model": "EVIDENCE (one independent B per sample; matches the residual model in open:marginal-adaptive)",
            "exact_sd_finite": "EVIDENCE (exact integer enumeration on count-vectors for n=2, m<=6)",
            "sd_below_baseline_m234": "ESCALATE (SD is below uniform-B-per-A baseline at m=2,3,4; first observed reducing direction)",
            "sd_not_below_baseline_m56": "NO-GO (SD exceeds baseline at m=5,6; no monotonic reduction)",
            "asymptotic_lem_m2": "OPEN (fixed-n crossing does not give a non-vanishing asymptotic rate)",
        },
        "interpretation_guards": {
            "L1_exact_arithmetic": "all SDs are Fractions; JSON stores string fractions",
            "L2_J_twist_duality": "count-vector aggregation in (C,y) pattern space; no dual rewriting",
            "L3_query_class": "unrestricted exact total variation on exchangeable count-vectors (equivalent to full (C,y) SD)",
            "L4_comparison_distribution": "LPN_{175/512} untransformed",
            "CLOSURE_GRADE": "fixed-n exact; asymptotic conclusions are OPEN/NO-GO only",
        },
    }

    out_path = Path("experiments/output") / f"730-trackHH-permutation-of-uniform-maxM{max_m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {out_path}", flush=True)
    return summary


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--max-m", type=int, default=6, help="maximum m (<=6 for exact)")
    return p.parse_args()


def main():
    args = parse_args()
    if not 2 <= args.max_m <= 6:
        raise ValueError("this script supports 2 <= max-m <= 6")
    run(args.max_m)


if __name__ == "__main__":
    main()
