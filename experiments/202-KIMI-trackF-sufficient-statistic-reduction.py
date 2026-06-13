#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""202: Track F — sufficient-statistic reduction for lem:m2 SD (n=2).

At n=2 each row of C is one of four types tau in F_2^2.  For both the
reduction output P_out and the matched-rate LPN target P_lpn, the pair
(C,y) depends only on

    T = ((m_tau)_{tau}, (s_tau)_{tau}),

where m_tau is the number of rows of type tau and s_tau is the number of
those rows whose label bit y is 1.

Proof obligations (implemented / verified):
  (i)   rank(C) and the event y in col(C) are functions of T.
        Membership holds iff there exists a w in F_2^2 such that for every
        tau with m_tau>0 we have s_tau = m_tau * <w,tau>.
  (ii)  For a fixed secret w, wt(y + Cw) = sum_tau [
        <w,tau>=0 ] s_tau + [<w,tau>=1] (m_tau - s_tau), hence P_lpn
        depends on y only through T.
  (iii) The mixture theorem (experiments 200/201) gives P_out through
        rank/membership only, hence through T.

The SD is therefore

    SD = (1/2) sum_T |P_out(T) - P_lpn(T)|.

This script computes the exact rational SD by enumerating T.  All
arithmetic is integer; the final SD is returned as a Fraction.

PRE-REGISTER interpretation guards:
  * Axis: m grows at fixed n=2 (the correct m-axis).
  * Comparison distribution: LPN_{p_eff(2)} (matched rate), not LPN_{1/4}.
  * The numbers measure statistical distance between two explicit
    distributions; they do not by themselves imply a practical attack.

Standing guards:
  L1 exact arithmetic: every probability is kept as an integer count over a
    common denominator q_den * N * D^m with p_eff = a/D in lowest terms.
  L2 J-twist care: not needed for this n=2 row-type reduction (the dual
    appears implicitly through the inner product <w,tau>).
  L3 query-class hygiene: the SD is between the exact output distribution
    and the exact matched-rate LPN target; no unrestricted Feldman theorem
    is invoked.
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

# Script lives in experiments/; imports need project root on sys.path.
sys.path.insert(0, str(Path(__file__).parent.parent))


def p_eff(n: int) -> Fraction:
    """Matched LPN noise rate p_eff(n) = (1 - (3/4)^{2n}) / 2."""
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    """Pr[Ax + e in span(A)] for uniform Lagrangian A, x, e ~ Bernoulli(1/4)^{2n}."""
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def exact_sd_sufficient_statistic_n2(m: int) -> dict:
    """Exact SD(P_out, LPN_{p_eff}) at n=2 by enumerating T."""
    n = 2
    N = 1 << n                      # number of row types
    q = q_graph(n)
    q_num, q_den = q.numerator, q.denominator
    p = p_eff(n)
    a = p.numerator                 # p_eff = a/D
    D = p.denominator
    b = D - a

    # Common denominator D_common = q_den * N * (2N)^m * D^m.
    # This clears denominators for the graph component (N^{m+1}), the full
    # component ((2N)^m), and the LPN noise component (D^m), including the
    # odd factor of q_den from the graph/full mixture weight q_graph.
    D_common = q_den * N * ((2 * N) ** m) * (D ** m)
    factor_graph = q_num * (2 ** m) * (D ** m)
    factor_full = (q_den - q_num) * N * (D ** m)
    factor_lpn = q_den * (2 ** m)                   # scales the unnormalised LPN counts

    # Precompute factorials and B0[m][s] = C(m,s) * a^s * b^(m-s).
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

    # Row types as integer indices 0..3; inner product <w,tau> over F_2^2.
    def dot(w: int, tau: int) -> int:
        return ((w >> 0) & (tau >> 0) ^ (w >> 1) & (tau >> 1)) & 1

    types = list(range(N))

    t0 = time.time()
    sd_num = 0

    # Enumerate compositions m0+m1+m2+m3 = m.
    for m0 in range(m + 1):
        for m1 in range(m - m0 + 1):
            for m2 in range(m - m0 - m1 + 1):
                m3 = m - m0 - m1 - m2
                mult_comp = fact[m] // (fact[m0] * fact[m1] * fact[m2] * fact[m3])
                ms = (m0, m1, m2, m3)

                # Precompute U_tau(s) and V_tau(s) arrays for this composition.
                U = [B0[mm] for mm in ms]

                for s0 in range(m0 + 1):
                    u0 = U[0][s0]
                    v0 = U[0][m0 - s0]
                    for s1 in range(m1 + 1):
                        u1 = U[1][s1]
                        v1 = U[1][m1 - s1]
                        for s2 in range(m2 + 1):
                            u2 = U[2][s2]
                            v2 = U[2][m2 - s2]
                            for s3 in range(m3 + 1):
                                s = (s0, s1, s2, s3)

                                # n_graph(T): count w with s_tau = m_tau * <w,tau>.
                                match_w = 0
                                for w in range(N):
                                    ok = True
                                    for tau in types:
                                        target = ms[tau] if dot(w, tau) else 0
                                        if s[tau] != target:
                                            ok = False
                                            break
                                    if ok:
                                        match_w += 1

                                n_graph = match_w * mult_comp

                                # n_full(T) = mult_comp * prod C(m_tau, s_tau).
                                n_full = (
                                    mult_comp
                                    * comb(m0, s0)
                                    * comb(m1, s1)
                                    * comb(m2, s2)
                                    * comb(m3, s3)
                                )

                                n_out = factor_graph * n_graph + factor_full * n_full

                                # n_lpn(T) = q_den * sum_x prod_tau B_{<x,tau>}(m_tau,s_tau)
                                # Unrolled for the four secrets x in F_2^2.
                                u3 = U[3][s3]
                                v3 = U[3][m3 - s3]

                                n_x0 = u0 * u1 * u2 * u3
                                # x=(1,0): <x,tau>=tau0 -> types 1,3 are in the kernel's complement
                                n_x1 = u0 * v1 * u2 * v3
                                # x=(0,1): <x,tau>=tau1 -> types 2,3 are flipped
                                n_x2 = u0 * u1 * v2 * v3
                                # x=(1,1): <x,tau>=tau0+tau1 -> types 1,2 are flipped
                                n_x3 = u0 * v1 * v2 * u3

                                # n_lpn_x already contains the per-type noise counts; multiply by
                                # the row-type multinomial to obtain the unnormalised probability
                                # of the ordered row composition.
                                n_lpn = factor_lpn * mult_comp * (n_x0 + n_x1 + n_x2 + n_x3)

                                sd_num += abs(n_out - n_lpn)

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


def cross_check_against_direct(max_m: int = 6) -> list[dict]:
    """Self-check: sufficient-statistic SD equals direct enumeration for small m."""
    from experiments.lib.lem_m2_exact import (
        enumerate_lagrangian_bases_n,
        exact_sd_counts,
        lpn_target_counts_n,
        randomized_uniform_B_counts_n,
    )

    n = 2
    p = p_eff(n)
    bases = list(enumerate_lagrangian_bases_n(n))
    checks = []
    for m in range(2, max_m + 1):
        red_counts, red_denom = randomized_uniform_B_counts_n(m, n, bases)
        lpn_counts, lpn_denom = lpn_target_counts_n(m, n, p)
        sd_direct = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)
        sd_ss = Fraction(exact_sd_sufficient_statistic_n2(m)["sd"])
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


def fit_decay(results: list[dict]) -> dict:
    """Fit 1-SD decay to exponential and power-law models (log-linear regression)."""
    import math

    xs = [r["m"] for r in results if r["m"] >= 8]
    ys = [float(Fraction(r["one_minus_sd"])) for r in results if r["m"] >= 8]
    n = len(xs)
    if n < 2:
        return {}

    # Exponential fit: log(1-SD) = A - alpha * m
    x_mean = sum(xs) / n
    logy = [math.log(y) for y in ys]
    ly_mean = sum(logy) / n
    num = sum((xs[i] - x_mean) * (logy[i] - ly_mean) for i in range(n))
    den = sum((xs[i] - x_mean) ** 2 for i in range(n))
    alpha = -num / den
    A = ly_mean + alpha * x_mean
    exp_fit = {"model": "1-SD ~ exp(A - alpha*m)", "A": A, "alpha": alpha}

    # Power-law fit: log(1-SD) = logC - beta * log(m)
    logx = [math.log(x) for x in xs]
    lx_mean = sum(logx) / n
    num2 = sum((logx[i] - lx_mean) * (logy[i] - ly_mean) for i in range(n))
    den2 = sum((logx[i] - lx_mean) ** 2 for i in range(n))
    beta = -num2 / den2
    logC = ly_mean + beta * lx_mean
    pow_fit = {"model": "1-SD ~ C * m^{-beta}", "C": math.exp(logC), "beta": beta}

    return {"exponential": exp_fit, "power_law": pow_fit}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ms",
        type=int,
        nargs="+",
        default=[2, 3, 4, 5, 6, 7, 8, 12, 16, 24, 32, 48],
        help="values of m to compute",
    )
    parser.add_argument(
        "--cross-check-max-m",
        type=int,
        default=6,
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

    # --- F1: cross-check against the corrected 200 sweep ----------------------
    print("== F1: cross-check against direct enumeration (experiments 200/201) ==")
    checks = cross_check_against_direct(args.cross_check_max_m)
    for c in checks:
        status = "OK" if c["match"] else "MISMATCH"
        print(
            f"  n={c['n']} m={c['m']}: direct={c['sd_direct']} "
            f"ss={c['sd_sufficient_statistic']} [{status}]"
        )
    if not all(c["match"] for c in checks):
        raise RuntimeError("sufficient-statistic cross-check failed")

    # --- F2: large-m exact SD -------------------------------------------------
    results = []
    print("\n== F2: Track F sufficient-statistic exact SD (n=2) ==")
    for m in args.ms:
        print(f"  computing m={m} ...", flush=True)
        res = exact_sd_sufficient_statistic_n2(m)
        results.append(res)
        print(
            f"    m={m:2d}: SD={res['sd']} = {res['sd_float']:.6f}, "
            f"1-SD={res['one_minus_sd_float']:.6e} ({res['time_sec']:.2f}s)"
        )

    decay = fit_decay(results)
    print("\n== 1-SD decay fit ==")
    if decay:
        print(f"  exponential: 1-SD ~ exp({decay['exponential']['A']:.4f} - "
              f"{decay['exponential']['alpha']:.4f} * m)")
        print(f"  power-law:   1-SD ~ {decay['power_law']['C']:.4f} * m^(-"
              f"{decay['power_law']['beta']:.4f})")
    else:
        print("  (need at least two m>=8 points to fit)")

    summary = {
        "experiment": 202,
        "track": "F",
        "cross_check": checks,
        "results": results,
        "decay_fit": decay,
        "claim_labels": {
            "sufficient_statistic_reduction": "THEOREM (proved; verified by direct enumeration for m<=6)",
            "n2_exact_sd_m_le_48": "EVIDENCE (exact finite computation)",
            "decay_fit": "EVIDENCE (finite-sample regression)",
            "lem_m2_status": "OPEN",
        },
        "interpretation_guards": {
            "axis": "m grows at fixed n=2 (the correct m-axis)",
            "comparison_distribution": "LPN_{p_eff(2)}, matched rate",
            "practical_attack": "SD numbers do not imply a practical distinguisher",
            "L1_exact_arithmetic": "integer counts over common denominator q_den*N*(2N)^m*D^m",
            "L2_duality_care": "not applicable; inner product is the standard F_2 pairing",
            "L3_query_class_hygiene": "SQ statements, if any, name the query class explicitly",
        },
    }

    out_path = out_dir / "202-trackF-sufficient-statistic-n2.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
