#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""200: Track A — matched-rate SD monotonicity for uniform-B-per-A lem:m2.

Computes exact statistical-distance values between the reduction output (C,y)
and the matched-rate LPN target LPN_{p_eff}, where

    p_eff(n) = (1 - (3/4)^{2n}) / 2.

Tasks:
  A1. Exact matched-rate SD at n=3, m=6.
  A2. Monotonicity study: n=2 for m=2..8 and n=3 for m=2..6.

The output distribution admits the exact mixture decomposition

    P_out = q(n) * P_graph + (1 - q(n)) * P_full,

with
    q(n) = Pr[Ax+e in span(A)]
         = (3/4)^{2n} + (1 - (3/4)^{2n}) / (2^n + 1),

P_full uniform over the full (C,y) space, and P_graph the distribution where
C is uniform and y is uniform over the column space of C.  This decomposition
has been verified against the from-scratch enumeration in
experiments/lib/lem_m2_exact.py for n=2; this script includes a self-check
for n=2, m=2..4 before reporting the larger sweep.

PRE-REGISTER interpretation guards:
  * Comparison distribution: LPN_{p_eff(n)} at the output's own noise rate
    (matched, not LPN_{1/4}).
  * Scaling axis: m grows at fixed n; no fixed-small-m conclusion.
  * p_eff(n) -> 1/2 as n grows, so the LPN target approaches trivial noise-1/2;
    the SD numbers below measure detectability of correlation inside a vacuous
    LPN regime and do not imply a practical distinguisher for LPN_{1/2}.
"""
import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases_n,
    exact_sd_counts,
    lpn_target_counts_n,
    randomized_uniform_B_counts_n,
)


def p_eff(n: int) -> Fraction:
    """Output noise rate p_eff(n) = (1 - (3/4)^{2n}) / 2."""
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    """Pr[Ax + e in span(A)] for uniform A, x, e ~ Bernoulli(1/4)^{2n}."""
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def rank_f2_cols(cols: list[int], m: int) -> int:
    pivots = []
    for v in cols:
        x = v & ((1 << m) - 1)
        if x == 0:
            continue
        for p in pivots:
            if (x >> (p.bit_length() - 1)) & 1:
                x ^= p
        if x:
            pivots.append(x)
    return len(pivots)


def colspace_mask(cols: list[int], m: int) -> int:
    sp = [0]
    for v in cols:
        sp += [s ^ v for s in sp]
    mask = 0
    for y in sp:
        mask |= 1 << y
    return mask


def exact_matched_sd_mixture(n: int, m: int) -> dict:
    """Exact SD(P_out, LPN_{p_eff}) using the graph/full mixture form.

    Returns a dict with 'sd' (Fraction string), 'sd_float', and timing.
    """
    t_start = time.time()
    p = p_eff(n)
    q = q_graph(n)
    q_num, q_den = q.numerator, q.denominator

    lpn_counts, D = lpn_target_counts_n(m, n, p)
    t_lpn = time.time() - t_start

    size = 1 << ((n + 1) * m)
    num_C = 1 << (n * m)
    y_mask = (1 << m) - 1

    full_count = (q_den - q_num) * (D // (q_den * size))
    graph_base = [
        q_num * (D // (q_den * num_C * (1 << r))) for r in range(n + 1)
    ]

    ranks = [0] * num_C
    masks = [0] * num_C
    for C in range(num_C):
        cols = []
        tmp = C
        for _ in range(n):
            cols.append(tmp & y_mask)
            tmp >>= m
        ranks[C] = rank_f2_cols(cols, m)
        masks[C] = colspace_mask(cols, m)

    t0 = time.time()
    diff = 0
    for key in range(size):
        y = key & y_mask
        C = key >> m
        p_out = full_count
        if (masks[C] >> y) & 1:
            p_out += graph_base[ranks[C]]
        diff += abs(lpn_counts[key] - p_out)
    t_out = time.time() - t0

    sd = Fraction(diff, 2 * D)
    return {
        "n": n,
        "m": m,
        "p_eff": str(p),
        "q_graph": str(q),
        "sd": str(sd),
        "sd_float": float(sd),
        "time_lpn_counts_sec": t_lpn,
        "time_out_loop_sec": t_out,
    }


def verify_mixture_against_direct(n: int, max_m: int) -> list[dict]:
    """Self-check: mixture SD equals direct enumeration for small n,m."""
    results = []
    bases = list(enumerate_lagrangian_bases_n(n))
    for m in range(2, max_m + 1):
        t0 = time.time()
        red_counts, red_denom = randomized_uniform_B_counts_n(m, n, bases)
        p = p_eff(n)
        lpn_counts, lpn_denom = lpn_target_counts_n(m, n, p)
        sd_direct = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)
        t_direct = time.time() - t0

        mix = exact_matched_sd_mixture(n, m)
        sd_mix = Fraction(mix["sd"])
        ok = (sd_direct == sd_mix)
        results.append(
            {
                "n": n,
                "m": m,
                "sd_direct": str(sd_direct),
                "sd_mixture": str(sd_mix),
                "match": ok,
                "time_direct_sec": t_direct,
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verify-max-m",
        type=int,
        default=4,
        help="max m for direct-vs-mixture self-check (default 4)",
    )
    parser.add_argument(
        "--n2-max-m", type=int, default=8, help="max m for n=2 monotonicity sweep"
    )
    parser.add_argument(
        "--n3-max-m", type=int, default=6, help="max m for n=3 monotonicity sweep"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="experiments/output",
        help="directory for JSON outputs",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- Self-check: mixture form vs direct enumeration ----------------------
    print("== Direct-vs-mixture self-check (n=2) ==")
    verify_results = verify_mixture_against_direct(2, args.verify_max_m)
    for r in verify_results:
        status = "OK" if r["match"] else "MISMATCH"
        print(
            f"  n={r['n']} m={r['m']}: direct={r['sd_direct']} "
            f"mix={r['sd_mixture']} [{status}] ({r['time_direct_sec']:.2f}s)"
        )
    if not all(r["match"] for r in verify_results):
        raise RuntimeError("mixture self-check failed")

    verify_path = out_dir / "200-trackA-mixture-self-check.json"
    with open(verify_path, "w") as f:
        json.dump(verify_results, f, indent=2)
    print(f"Saved self-check: {verify_path}\n")

    # --- Task A1: n=3, m=6 exact matched SD ----------------------------------
    print("== Task A1: n=3, m=6 exact matched-rate SD ==")
    a1 = exact_matched_sd_mixture(3, 6)
    print(f"  p_eff = {a1['p_eff']} = {float(Fraction(a1['p_eff'])):.6f}")
    print(f"  q_graph = {a1['q_graph']} = {float(Fraction(a1['q_graph'])):.6f}")
    print(f"  SD = {a1['sd']} = {a1['sd_float']:.6f}")
    a1_path = out_dir / "200-trackA-n3-m6-exact.json"
    with open(a1_path, "w") as f:
        json.dump(a1, f, indent=2)
    print(f"Saved: {a1_path}\n")

    # --- Task A2: monotonicity sweeps ----------------------------------------
    print("== Task A2: monotonicity of matched-rate SD in m ==")
    sweep = []
    for n in (2, 3):
        max_m = args.n2_max_m if n == 2 else args.n3_max_m
        print(f"  n={n}:")
        for m in range(2, max_m + 1):
            res = exact_matched_sd_mixture(n, m)
            sweep.append(res)
            print(
                f"    m={m:2d}: SD={res['sd']} = {res['sd_float']:.6f} "
                f"(loop {res['time_out_loop_sec']:.2f}s)"
            )

    sweep_path = out_dir / "200-trackA-monotonicity-sweep.json"
    with open(sweep_path, "w") as f:
        json.dump(sweep, f, indent=2)
    print(f"Saved sweep: {sweep_path}\n")

    # --- Summary JSON --------------------------------------------------------
    summary = {
        "experiment": 200,
        "track": "A",
        "self_check": verify_results,
        "task_A1": a1,
        "task_A2_sweep": sweep,
        "claim_labels": {
            "mixture_decomposition": "THEOREM (verified by direct enumeration for n=2)",
            "n3_m6_sd": "EVIDENCE (exact finite computation)",
            "monotonicity_observation": "EVIDENCE (exact finite computation, no proof of general monotonicity)",
            "lem_m2_status": "OPEN",
        },
        "interpretation_guards": {
            "comparison_distribution": "LPN_{p_eff(n)}, matched rate",
            "scaling_axis": "m grows at fixed n (no fixed-small-m claim)",
            "p_eff_limit": "p_eff(n) -> 1/2 as n grows; SD measures correlation inside a vacuous LPN regime",
        },
    }
    summary_path = out_dir / "200-trackA-summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary: {summary_path}")


if __name__ == "__main__":
    main()
