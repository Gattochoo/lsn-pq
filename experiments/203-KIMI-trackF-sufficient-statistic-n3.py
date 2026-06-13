#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""203: Track F stretch — sufficient-statistic reduction for n=3.

Generalises experiments/202 to arbitrary n.  At n=3 there are 8 row types,
so the state space is O(m^{15}); m=12 is the first feasible extension of the
exact frontier.  The same proof obligations and guard labels apply as in 202.
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def p_eff(n: int) -> Fraction:
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def dot(u: int, v: int) -> int:
    """Standard F_2 inner product (parity of bitwise AND)."""
    return (u & v).bit_count() & 1


def exact_sd_sufficient_statistic(n: int, m: int) -> dict:
    N = 1 << n
    q = q_graph(n)
    q_num, q_den = q.numerator, q.denominator
    p = p_eff(n)
    a = p.numerator
    D = p.denominator
    b = D - a

    D_common = q_den * N * ((2 * N) ** m) * (D ** m)
    factor_graph = q_num * (2 ** m) * (D ** m)
    factor_full = (q_den - q_num) * N * (D ** m)
    factor_lpn = q_den * (2 ** m)

    fact = [1]
    for i in range(1, m + 1):
        fact.append(fact[-1] * i)

    pow_a = [1] * (m + 1)
    pow_b = [1] * (m + 1)
    for i in range(1, m + 1):
        pow_a[i] = pow_a[i - 1] * a
        pow_b[i] = pow_b[i - 1] * b

    B0 = [[0] * (mm + 1) for mm in range(m + 1)]
    for mm in range(m + 1):
        row = B0[mm]
        for s in range(mm + 1):
            row[s] = comb(mm, s) * pow_a[s] * pow_b[mm - s]

    types = list(range(N))
    secrets = list(range(N))

    ms = [0] * N
    ss = [0] * N
    U = [None] * N
    V = [None] * N
    binom_i = [None] * N

    t0 = time.time()
    sd_num = 0

    def process_composition():
        # Precompute per-type tables for the current composition.
        mult_comp = fact[m]
        for i in types:
            mult_comp //= fact[ms[i]]
            mm = ms[i]
            U[i] = B0[mm]
            # V[i][s] = B0[mm][mm - s]
            V[i] = B0[mm]
            binom_i[i] = [comb(mm, s) for s in range(mm + 1)]

        # Now enumerate all s vectors.
        def rec_s(idx: int):
            if idx == N - 1:
                mm = ms[idx]
                for s in range(mm + 1):
                    ss[idx] = s
                    evaluate(mult_comp)
            else:
                mm = ms[idx]
                for s in range(mm + 1):
                    ss[idx] = s
                    rec_s(idx + 1)

        rec_s(0)

    def evaluate(mult_comp: int):
        # n_graph: number of w with s_tau = m_tau iff <w,tau>=1.
        match_w = 0
        for w in secrets:
            ok = True
            for tau in types:
                target = ms[tau] if dot(w, tau) else 0
                if ss[tau] != target:
                    ok = False
                    break
            if ok:
                match_w += 1

        n_graph = match_w * mult_comp

        n_full = mult_comp
        for tau in types:
            n_full *= binom_i[tau][ss[tau]]

        n_out = factor_graph * n_graph + factor_full * n_full

        # n_lpn: sum over secrets x of prod_tau U/V.
        lpn_sum = 0
        for x in secrets:
            prod = 1
            for tau in types:
                if dot(x, tau):
                    prod *= V[tau][ms[tau] - ss[tau]]
                else:
                    prod *= U[tau][ss[tau]]
            lpn_sum += prod

        n_lpn = factor_lpn * mult_comp * lpn_sum
        nonlocal sd_num
        sd_num += abs(n_out - n_lpn)

    def rec_type(idx: int, rem: int):
        if idx == N - 1:
            ms[idx] = rem
            process_composition()
        else:
            for mm in range(rem + 1):
                ms[idx] = mm
                rec_type(idx + 1, rem - mm)

    rec_type(0, m)

    sd = Fraction(sd_num, 2 * D_common)
    t_elapsed = time.time() - t0
    return {
        "n": n,
        "m": m,
        "p_eff": str(p),
        "q_graph": str(q),
        "sd": str(sd),
        "sd_float": float(sd),
        "one_minus_sd": str(Fraction(1) - sd),
        "one_minus_sd_float": float(Fraction(1) - sd),
        "time_sec": t_elapsed,
    }


def cross_check_against_direct(n: int, max_m: int) -> list[dict]:
    from experiments.lib.lem_m2_exact import (
        enumerate_lagrangian_bases_n,
        exact_sd_counts,
        lpn_target_counts_n,
        randomized_uniform_B_counts_n,
    )

    p = p_eff(n)
    bases = list(enumerate_lagrangian_bases_n(n))
    checks = []
    for m in range(2, max_m + 1):
        red_counts, red_denom = randomized_uniform_B_counts_n(m, n, bases)
        lpn_counts, lpn_denom = lpn_target_counts_n(m, n, p)
        sd_direct = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)
        sd_ss = Fraction(exact_sd_sufficient_statistic(n, m)["sd"])
        checks.append(
            {
                "n": n,
                "m": m,
                "sd_direct": str(sd_direct),
                "sd_sufficient_statistic": str(sd_ss),
                "match": sd_direct == sd_ss,
            }
        )
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument(
        "--ms",
        type=int,
        nargs="+",
        default=[2, 3, 4, 5, 6, 8, 10, 12],
        help="values of m to compute",
    )
    parser.add_argument(
        "--cross-check-max-m",
        type=int,
        default=4,
        help="max m for direct-vs-sufficient-statistic self-check",
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

    print(f"== Track F sufficient-statistic exact SD (n={args.n}) ==")
    if args.cross_check_max_m >= 2:
        print("  cross-check against direct enumeration ...")
        checks = cross_check_against_direct(args.n, args.cross_check_max_m)
        for c in checks:
            status = "OK" if c["match"] else "MISMATCH"
            print(
                f"    n={c['n']} m={c['m']}: direct={c['sd_direct']} "
                f"ss={c['sd_sufficient_statistic']} [{status}]"
            )
        if not all(c["match"] for c in checks):
            raise RuntimeError("sufficient-statistic cross-check failed")
    else:
        checks = []

    results = []
    for m in args.ms:
        print(f"  computing m={m} ...", flush=True)
        res = exact_sd_sufficient_statistic(args.n, m)
        results.append(res)
        print(
            f"    m={m:2d}: SD={res['sd']} = {res['sd_float']:.6f}, "
            f"1-SD={res['one_minus_sd_float']:.6e} ({res['time_sec']:.2f}s)"
        )

    summary = {
        "experiment": 203,
        "track": "F",
        "n": args.n,
        "cross_check": checks,
        "results": results,
        "claim_labels": {
            "sufficient_statistic_reduction_general_n": "THEOREM (proved; verified by direct enumeration for small m)",
            f"n{args.n}_exact_sd": "EVIDENCE (exact finite computation)",
            "lem_m2_status": "OPEN",
        },
        "interpretation_guards": {
            "axis": f"m grows at fixed n={args.n} (the correct m-axis)",
            "comparison_distribution": f"LPN_{{p_eff({args.n})}}, matched rate",
            "L1_exact_arithmetic": "integer counts over common denominator q_den*N*(2N)^m*D^m",
            "L2_duality_care": "not applicable; standard F_2 pairing",
            "L3_query_class_hygiene": "SQ statements name the query class explicitly",
        },
    }

    out_path = out_dir / f"203-trackF-sufficient-statistic-n{args.n}.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
