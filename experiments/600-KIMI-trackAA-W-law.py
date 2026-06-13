#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""600 (Track AA): exact law of min-syndrome-weight W for n=2, small m.

Baseline: Gemini's B-agnostic W=0 spike leaks at rate q_graph(n) -> 0.
Goal: quantify the full low-W tail for several marginal-uniform B families and
compare the W-law to matched LPN_{p_eff(2)}.  Ask whether TV(W-law) receives any
extra, non-vanishing contribution beyond q_graph(n).

Families examined:
  * uniform-per-A B          (randomized adaptive, lambda-coupled with lambda=0)
  * lambda-coupled B         (mixture: all rows equal with prob lambda, else iid uniform)
  * complementary-pair B     (NEW: rows paired as (r, r xor 1111); pairs independent)

All counts use exact integer arithmetic; probabilities are Fractions; JSON stores
string fractions.  The matched LPN rate is p_eff(2) = (1 - (3/4)^4)/2 = 175/512.

PRE-REGISTER interpretation guards
----------------------------------
* L1 exact arithmetic: every probability is a Fraction; counts are integers.
* L2 J-twist duality: W is evaluated directly on (C, y); no dual rewriting.
* L3 query-class hygiene: W is a single-sample structural statistic (membership /
  syndrome-decoding weight); the reported TV is over this one functional, not a
  claim about arbitrary SQ/lem:m2 distinguishers.
* L4 never transform the comparison distribution: LPN target is the standard
  matched-rate LPN_{175/512} distribution over (C, y), untransformed.
* CLOSURE-GRADE: n=2 exact computations at increasing m are fixed-n evidence.
  Any statement about asymptotic n is labeled OPEN.  A vanishing TV in m at fixed n
  does NOT imply the asymptotic case; conversely, a bounded-away TV at fixed n does
  NOT prove an n-dependent lower bound.
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import (
    apply_matrix,
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    randomized_uniform_B_counts,
    reduction_counts_for_B,
)


def p_eff_n2() -> Fraction:
    """Matched per-coordinate output noise rate for any marginal-uniform B at n=2."""
    return Fraction(1 - Fraction(3, 4) ** 4, 2)


def q_graph_n2() -> Fraction:
    """B-agnostic Pr[W=0] = Pr[Ax+e in span(A)] for n=2."""
    p_zero = Fraction(3, 4) ** 4
    return p_zero + (1 - p_zero) / (2 ** 2 + 1)


def w_law_from_counts(counts: list[int], denom: int, m: int, n: int = 2) -> list[Fraction]:
    """Exact distribution of W = min_w wt(y + Cw) over {0,...,m}."""
    y_mask = (1 << m) - 1
    dist = [Fraction(0) for _ in range(m + 1)]
    for key, c in enumerate(counts):
        if c == 0:
            continue
        y = key & y_mask
        C = key >> m
        c0 = (C >> m) & y_mask
        c1 = C & y_mask
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
        dist[best] += Fraction(c, denom)
    return dist


def tv_w_laws(a: list[Fraction], b: list[Fraction]) -> Fraction:
    """Exact total variation between two W-laws."""
    total = Fraction(0)
    for i in range(max(len(a), len(b))):
        av = a[i] if i < len(a) else Fraction(0)
        bv = b[i] if i < len(b) else Fraction(0)
        total += abs(av - bv)
    return total / 2


def low_w_tail(dist: list[Fraction], k: int) -> Fraction:
    """Pr[W <= k]."""
    return sum(dist[: k + 1], Fraction(0))


def constant_rows_equal_B_counts(m: int, bases) -> tuple[list[int], int]:
    """Integer counts for (C, y) when all m rows equal a uniform r in F_2^4."""
    mask = (1 << m) - 1

    def B_const(r: int) -> list[int]:
        return [mask if ((r >> j) & 1) else 0 for j in range(4)]

    total = None
    for r in range(1 << 4):
        counts = reduction_counts_for_B(B_const(r), bases, m)
        if total is None:
            total = counts
        else:
            for i, c in enumerate(counts):
                total[i] += c
    denom = 16 * 15360
    return total, denom


def lambda_coupled_counts(
    lam: Fraction,
    uniform_counts: list[int],
    uniform_denom: int,
    constant_counts: list[int],
    constant_denom: int,
) -> tuple[list[int], int]:
    """Exact integer counts for P_out = (1-lam) P_uniform_B + lam P_all-rows-equal."""
    if not (0 <= lam <= 1):
        raise ValueError("lam must be in [0,1]")
    scale = uniform_denom // constant_denom
    p = lam.numerator
    q = lam.denominator
    mixed = [(q - p) * u + p * (c * scale) for u, c in zip(uniform_counts, constant_counts)]
    denom = q * uniform_denom
    return mixed, denom


def complementary_pair_B_counts(m: int, bases) -> tuple[list[int], int]:
    """Integer counts for (C, y) when rows are paired as complements.

    For m = 2k  : k independent pairs (r_i, r_i xor 0b1111).
    For m = 2k+1: k pairs plus one trailing independent uniform row.

    Each row is uniform over F_2^4, so for every fixed A the entries of BA are
    marginally uniform (lem:m1 satisfied).  The family is new: it forces adjacent
    rows to differ in every coordinate, spreading the row pattern while keeping
    per-coordinate marginals at 1/2.
    """
    mask = (1 << m) - 1
    size = 1 << (3 * m)
    counts = [0] * size
    k = m // 2
    odd = m % 2
    num_r = 1 << (4 * k)
    num_last = 16 if odd else 1
    all_ones = 0b1111

    B_cols = [0] * 4
    for r_block in range(num_r):
        # first 2k rows as complementary pairs
        tmp = r_block
        for i in range(k):
            r = tmp & 0b1111
            tmp >>= 4
            comp = r ^ all_ones
            for j in range(4):
                if (r >> j) & 1:
                    B_cols[j] |= 1 << (2 * i)
                if (comp >> j) & 1:
                    B_cols[j] |= 1 << (2 * i + 1)
        for s in range(num_last):
            if odd:
                for j in range(4):
                    if (s >> j) & 1:
                        B_cols[j] |= 1 << (m - 1)
            Bx = [apply_matrix(B_cols, x) & mask for x in range(1 << 4)]
            for a0, a1 in bases:
                c0 = Bx[a0]
                c1 = Bx[a1]
                C_key = (c0 << m) | c1
                for x in range(1 << 2):
                    a = 0
                    if x & 1:
                        a ^= a0
                    if x & 2:
                        a ^= a1
                    for e in range(1 << 4):
                        w = e.bit_count()
                        weight = 3 ** (4 - w)
                        v = a ^ e
                        y = Bx[v]
                        key = (C_key << m) | y
                        counts[key] += weight
            if odd:
                for j in range(4):
                    B_cols[j] &= ~(1 << (m - 1))

    denom = (16 ** k) * (16 if odd else 1) * 15360
    return counts, denom


def compute_family_wlaws(
    m: int,
    bases,
    lpn_counts: list[int],
    lpn_denom: int,
    uniform_counts: list[int] | None = None,
    uniform_denom: int | None = None,
    constant_counts: list[int] | None = None,
    constant_denom: int | None = None,
) -> dict:
    """Compute W-laws and TVs for all B families at a given m."""
    y_mask = (1 << m) - 1
    p_eff = p_eff_n2()

    # Matched LPN W-law.
    lpn_w = w_law_from_counts(lpn_counts, lpn_denom, m)

    results = {
        "m": m,
        "p_eff": str(p_eff),
        "q_graph_n2": str(q_graph_n2()),
        "lpn_w_law": {str(w): str(p) for w, p in enumerate(lpn_w)},
        "lpn_tail": {str(k): str(low_w_tail(lpn_w, k)) for k in range(min(4, m + 1))},
        "families": [],
    }

    # Uniform-per-A B (lambda = 0).
    if uniform_counts is None:
        uniform_counts, uniform_denom = randomized_uniform_B_counts(m, bases)
    uni_w = w_law_from_counts(uniform_counts, uniform_denom, m)
    results["families"].append(
        {
            "family": "uniform-per-A",
            "lambda": "0",
            "w_law": {str(w): str(p) for w, p in enumerate(uni_w)},
            "tail": {str(k): str(low_w_tail(uni_w, k)) for k in range(min(4, m + 1))},
            "tv_to_lpn": str(tv_w_laws(uni_w, lpn_w)),
            "tv_float": float(tv_w_laws(uni_w, lpn_w)),
        }
    )

    # Lambda-coupled family.
    if constant_counts is None:
        constant_counts, constant_denom = constant_rows_equal_B_counts(m, bases)
    lambda_values = [Fraction(k, 4) for k in range(5)]  # 0, 1/4, 1/2, 3/4, 1
    for lam in lambda_values:
        mix_counts, mix_denom = lambda_coupled_counts(
            lam, uniform_counts, uniform_denom, constant_counts, constant_denom
        )
        mix_w = w_law_from_counts(mix_counts, mix_denom, m)
        results["families"].append(
            {
                "family": "lambda-coupled",
                "lambda": str(lam),
                "w_law": {str(w): str(p) for w, p in enumerate(mix_w)},
                "tail": {str(k): str(low_w_tail(mix_w, k)) for k in range(min(4, m + 1))},
                "tv_to_lpn": str(tv_w_laws(mix_w, lpn_w)),
                "tv_float": float(tv_w_laws(mix_w, lpn_w)),
            }
        )

    # Complementary-pair B (new family).
    cp_counts, cp_denom = complementary_pair_B_counts(m, bases)
    cp_w = w_law_from_counts(cp_counts, cp_denom, m)
    results["families"].append(
        {
            "family": "complementary-pair",
            "description": "rows paired as (r, r xor 1111); pairs independent; each row uniform",
            "w_law": {str(w): str(p) for w, p in enumerate(cp_w)},
            "tail": {str(k): str(low_w_tail(cp_w, k)) for k in range(min(4, m + 1))},
            "tv_to_lpn": str(tv_w_laws(cp_w, lpn_w)),
            "tv_float": float(tv_w_laws(cp_w, lpn_w)),
        }
    )

    return results


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--max-m", type=int, default=6, help="maximum m to compute")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    max_m = args.max_m
    if not 2 <= max_m <= 7:
        raise ValueError("this experiment supports 2 <= max-m <= 7")

    bases = list(enumerate_lagrangian_bases())
    p_eff = p_eff_n2()
    q_graph = q_graph_n2()

    per_m = []
    for m in range(2, max_m + 1):
        print(f"m = {m} ...", flush=True)
        t0 = time.time()
        lpn_counts, lpn_denom = lpn_target_counts(m, p_eff)
        uniform_counts, uniform_denom = randomized_uniform_B_counts(m, bases)
        constant_counts, constant_denom = constant_rows_equal_B_counts(m, bases)
        res = compute_family_wlaws(
            m, bases, lpn_counts, lpn_denom,
            uniform_counts, uniform_denom, constant_counts, constant_denom,
        )
        res["time_sec"] = time.time() - t0
        per_m.append(res)
        print(f"  done in {res['time_sec']:.2f}s", flush=True)
        for fam in res["families"]:
            print(
                f"    {fam['family']:22s} lambda={fam.get('lambda',''):5s} "
                f"TV(W)={fam['tv_float']:.6f}  W=0={float(Fraction(fam['w_law']['0'])):.6f}",
                flush=True,
            )

    # Summary statistics.
    summary = {
        "experiment": 600,
        "track": "AA",
        "n": 2,
        "max_m": max_m,
        "p_eff": str(p_eff),
        "q_graph_n2": str(q_graph),
        "q_graph_float": float(q_graph),
        "per_m": per_m,
        "claim_labels": {
            "W=0_spike_lower_bound": "THEOREM (B-agnostic: W=0 whenever e in span(A); Pr[e in span(A)] = q_graph(n))",
            "W=0_actual_probability": "EVIDENCE (depends on B and m; approaches q_graph(n) from above as m grows)",
            "W_laws_exact_finite": "EVIDENCE (exact integer enumeration for n=2, m<=7)",
            "TV_W_law_bounded_below_in_n": "OPEN (fixed-n evidence does not give n-dependent lower bound)",
            "TV_W_law_vanishes_in_n": "OPEN (cannot be tested at n=2)",
            "complementary_pair_marginal_uniform": "THEOREM (each row uniform by construction)",
        },
        "interpretation_guards": {
            "L1_exact_arithmetic": "all probabilities Fractions, JSON stores string fractions",
            "L2_J_twist_duality": "W evaluated directly on (C,y); no Fourier/J-twist dual",
            "L3_query_class": "single-sample structural statistic (min syndrome weight)",
            "L4_comparison_distribution": "LPN_{175/512} untransformed",
            "CLOSURE_GRADE": "fixed-n exact; asymptotic n statements are OPEN, not closed",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"600-trackAA-W-law-maxM{max_m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
