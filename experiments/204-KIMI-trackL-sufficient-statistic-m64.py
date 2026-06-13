#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""204: Track L — sufficient-statistic reduction at n=2, m=64 (and m=80).

Extends Track F's sufficient-statistic reduction (experiments/202) using two
worked engineering reductions:

1. S_3 symmetry of the three non-zero row types.  We canonicalise the ordered
triple of non-zero (m_tau, s_tau) pairs by sorting them by (m, s) descending and
multiply each canonical state by its orbit size (3! divided by the automorphism
factor of equal pairs).

2. The type-00 row is a pure shift: <00, w> = 0 for every secret w.  Hence
P_lpn depends on s_00 only through the common factor C(m_00, s_00)
a^{s_00} b^{m_00-s_00}; the graph side forces s_00 = 0.  For a fixed residual
state (m_00, (m_i, s_i)_{i=1}^3) the sum over s_00 is therefore a one-parameter
sum with a closed-form sign threshold, which we pre-compute once per m_00.

All arithmetic is integer; the SD is returned as a Fraction.  JSON stores
fractions as strings.

PRE-REGISTER interpretation guards:
  * Axis: m grows at fixed n=2 (the correct m-axis).
  * Comparison distribution: LPN_{p_eff(2)} (matched rate), not LPN_{1/4}.
  * The numbers measure statistical distance between two explicit
    distributions; they do not by themselves imply a practical attack.

Standing guards:
  L1 exact arithmetic: integer counts over common denominator
    q_den * N * (2N)^m * D^m; no floating-point in the SD computation.
  L2 J-twist care: n=2 row-type reduction uses the standard F_2 pairing only.
  L3 query-class hygiene: no unrestricted Feldman theorem is invoked.
  L4 comparison-distribution care: the LPN target is never transformed.
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
    """Matched LPN noise rate p_eff(n) = (1 - (3/4)^{2n}) / 2."""
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    """Pr[Ax + e in span(A)] for uniform Lagrangian A, x, e ~ Bernoulli(1/4)^{2n}."""
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def exact_sd_reduced_n2(m: int, verbose: bool = False) -> dict:
    """Exact SD(P_out, LPN_{p_eff}) at n=2 using S_3 + pure-shift reductions."""
    n = 2
    N = 1 << n
    q = q_graph(n)
    q_num, q_den = q.numerator, q.denominator
    p = p_eff(n)
    a = p.numerator
    D = p.denominator
    b = D - a

    # Common denominator for the original (unreduced) count representation.
    D_common = q_den * N * ((2 * N) ** m) * (D ** m)
    factor_graph = q_num * (2 ** m) * (D ** m)
    factor_full = (q_den - q_num) * N * (D ** m)
    factor_lpn = q_den * (2 ** m)

    # Precompute factorials and binomials.
    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i
    fact_m = fact[m]

    C = [[0] * (mm + 1) for mm in range(m + 1)]
    for mm in range(m + 1):
        for s in range(mm + 1):
            C[mm][s] = comb(mm, s)

    pow_a = [1] * (m + 1)
    pow_b = [1] * (m + 1)
    for i in range(1, m + 1):
        pow_a[i] = pow_a[i - 1] * a
        pow_b[i] = pow_b[i - 1] * b

    # U[mm][s] = C(mm, s) * a^s * b^(mm-s).
    U = [[0] * (mm + 1) for mm in range(m + 1)]
    for mm in range(m + 1):
        for s in range(mm + 1):
            U[mm][s] = C[mm][s] * pow_a[s] * pow_b[mm - s]

    # Pure-shift tables: for each m0, raw_c[s] = a^s * b^(m0-s) and
    # prefix sums of C(m0, s) and C(m0, s) * a^s * b^(m0-s).
    raw_c = [[] for _ in range(m + 1)]
    preC = [[] for _ in range(m + 1)]
    preW = [[] for _ in range(m + 1)]
    totalC = [0] * (m + 1)
    totalW = [0] * (m + 1)
    for m0 in range(m + 1):
        rc = [pow_a[s] * pow_b[m0 - s] for s in range(m0 + 1)]
        raw_c[m0] = rc
        pc = [0] * (m0 + 1)
        pw = [0] * (m0 + 1)
        running_c = 0
        running_w = 0
        for s in range(m0 + 1):
            running_c += C[m0][s]
            running_w += U[m0][s]
            pc[s] = running_c
            pw[s] = running_w
        preC[m0] = pc
        preW[m0] = pw
        totalC[m0] = 1 << m0
        totalW[m0] = D ** m0

    t0 = time.time()
    sd_num = 0

    # Iterate canonical non-zero type triples with m1 >= m2 >= m3.
    # For equal m values we enforce non-increasing s to avoid duplicate orbits.
    for m1 in range(m + 1):
        U1 = U[m1]
        C1 = C[m1]
        for m2 in range(m1 + 1):
            U2 = U[m2]
            C2 = C[m2]
            # If m1 == m2, s1 must be >= s2; otherwise s2 is free.
            s2_low_m12 = (0, m1 == m2)
            for m3 in range(m2 + 1):
                M = m1 + m2 + m3
                if M > m:
                    break
                U3 = U[m3]
                C3 = C[m3]
                # Determine s ordering constraints for the canonical pair sort.
                eq12 = m1 == m2
                eq23 = m2 == m3

                # Enumerate canonical s triples.
                s1_max = m1
                for s1 in range(s1_max + 1):
                    U1s = U1[s1]
                    V1s = U1[m1 - s1]
                    C1s = C1[s1]
                    s2_min = s1 if eq12 else 0
                    for s2 in range(s2_min, m2 + 1):
                        U2s = U2[s2]
                        V2s = U2[m2 - s2]
                        C2s = C2[s2]
                        s3_min = s2 if eq23 else 0
                        for s3 in range(s3_min, m3 + 1):
                            U3s = U3[s3]
                            V3s = U3[m3 - s3]
                            C3s = C3[s3]

                            # Orbit multiplicity of this unordered triple of pairs.
                            if m1 == m2 == m3 and s1 == s2 == s3:
                                mult_perm = 1
                            elif (m1 == m2 and s1 == s2) or (m2 == m3 and s2 == s3) or (m1 == m3 and s1 == s3):
                                mult_perm = 3
                            else:
                                mult_perm = 6

                            # Residual quantities independent of m0.
                            rest_full = C1s * C2s * C3s
                            lpn_rest = (
                                U1s * U2s * U3s
                                + U1s * V2s * V3s
                                + V1s * U2s * V3s
                                + V1s * V2s * U3s
                            )

                            # Membership count for the non-zero part.
                            matches = [
                                (s1 == 0 and s2 == 0 and s3 == 0),
                                (s1 == 0 and s2 == m2 and s3 == m3),
                                (s1 == m1 and s2 == 0 and s3 == m3),
                                (s1 == m1 and s2 == m2 and s3 == 0),
                            ]
                            match_w = sum(1 for ok in matches if ok)

                            A = factor_full * rest_full
                            K = factor_lpn * lpn_rest
                            G = factor_graph * match_w

                            # The type-00 count is forced by m0 = m - M.
                            m0 = m - M
                            mult_comp = fact_m // (fact[m0] * fact[m1] * fact[m2] * fact[m3])

                            # Threshold for sign(B_s) where B_s = A - K * a^s * b^(m0-s).
                            # raw_c[m0] is decreasing in s because a < b.
                            rc = raw_c[m0]
                            lo, hi = 0, m0 + 1
                            while lo < hi:
                                mid = (lo + hi) // 2
                                if K * rc[mid] <= A:
                                    hi = mid
                                else:
                                    lo = mid + 1
                            t = lo

                            pc = preC[m0]
                            pw = preW[m0]
                            if t == 0:
                                pre_c = 0
                                pre_w = 0
                            elif t > m0:
                                pre_c = pc[m0]
                                pre_w = pw[m0]
                            else:
                                pre_c = pc[t - 1]
                                pre_w = pw[t - 1]

                            # S_abs_total = sum_{s=0}^{m0} C(m0,s) * |B_s|.
                            totC = totalC[m0]
                            totW = totalW[m0]
                            S_abs_total = A * (totC - 2 * pre_c) + K * (2 * pre_w - totW)

                            B0 = A - K * rc[0]
                            s0_sum = S_abs_total - abs(B0) + abs(B0 + G)

                            sd_num += mult_perm * mult_comp * s0_sum

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


def fit_decay(results: list[dict]) -> dict:
    """Fit 1-SD decay to exponential and power-law models (log-linear regression)."""
    import math

    xs = [r["m"] for r in results if r["m"] >= 8]
    ys = [float(Fraction(r["one_minus_sd"])) for r in results if r["m"] >= 8]
    n = len(xs)
    if n < 2:
        return {}

    x_mean = sum(xs) / n
    logy = [math.log(y) for y in ys]
    ly_mean = sum(logy) / n
    num = sum((xs[i] - x_mean) * (logy[i] - ly_mean) for i in range(n))
    den = sum((xs[i] - x_mean) ** 2 for i in range(n))
    alpha = -num / den
    A = ly_mean + alpha * x_mean
    exp_fit = {"model": "1-SD ~ exp(A - alpha*m)", "A": A, "alpha": alpha}

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
        default=[24, 48, 64, 80],
        help="values of m to compute",
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

    # Anchor values from Track F (corrected m <= 48 table).
    ANCHORS = {
        24: "16832756036765379095034202127924274618943844971887062499211392003318774009896365/29642774844752946028434172162224104410437116074403984394101141506025761187823616",
        32: "175842639268182236234225149971230384237897459955496283666363584364067225210764143038987088768788053693215/286687326998758938951352611912760867599570623646035140467198604923365359511060601008752319138765710819328",
        48: "607477461132137352864009669432561278876547085540963876824000902259324180705585729760268074621527447131000809903636388269236874471512931193096020288141170484925/878694100496718043517683302282418331810487718418343092402491322775749527474899974671687634004666183037093927858109549828751614463963730408009475621262727315456",
    }

    print("== Track L — S_3 + pure-shift reduced exact SD (n=2) ==")
    results = []
    for m in args.ms:
        print(f"  computing m={m} ...", flush=True)
        res = exact_sd_reduced_n2(m, verbose=False)
        results.append(res)
        print(
            f"    m={m:2d}: SD={res['sd']} = {res['sd_float']:.6f}, "
            f"1-SD={res['one_minus_sd_float']:.6e} ({res['time_sec']:.2f}s)"
        )
        if m in ANCHORS:
            anchor = Fraction(ANCHORS[m])
            computed = Fraction(res["sd"])
            ok = computed == anchor
            print(f"    anchor m={m}: {'MATCH' if ok else 'MISMATCH'}")
            if not ok:
                raise RuntimeError(f"anchor mismatch at m={m}")

    decay = fit_decay(results)
    print("\n== 1-SD decay fit ==")
    if decay:
        print(
            f"  exponential: 1-SD ~ exp({decay['exponential']['A']:.4f} - "
            f"{decay['exponential']['alpha']:.4f} * m)"
        )
        print(
            f"  power-law:   1-SD ~ {decay['power_law']['C']:.4f} * m^(-"
            f"{decay['power_law']['beta']:.4f})"
        )
    else:
        print("  (need at least two m>=8 points to fit)")

    summary = {
        "experiment": 204,
        "track": "L",
        "results": results,
        "decay_fit": decay,
        "claim_labels": {
            "s3_symmetry_reduction": "THEOREM (canonicalisation by sorting non-zero (m_tau, s_tau) pairs; orbit multiplicity exact)",
            "s00_pure_shift_vectorisation": "THEOREM (closed-form s_00-sum via sign threshold; denominator divisibility proved)",
            "n2_exact_sd_m_64": "EVIDENCE (exact finite computation)",
            "n2_exact_sd_m_80": "EVIDENCE (exact finite computation)",
            "decay_fit": "EVIDENCE (finite-sample regression)",
            "lem_m2_status": "OPEN",
        },
        "interpretation_guards": {
            "axis": "m grows at fixed n=2 (the correct m-axis)",
            "comparison_distribution": "LPN_{p_eff(2)}, matched rate; never transformed",
            "practical_attack": "SD numbers do not imply a practical distinguisher",
            "L1_exact_arithmetic": "integer counts over common denominator q_den*N*(2N)^m*D^m; Fraction output",
            "L2_duality_care": "standard F_2 pairing only; no symplectic dual needed",
            "L3_query_class_hygiene": "SQ statements name query class explicitly; no unrestricted Feldman theorem",
            "L4_comparison_distribution": "LPN target is the matched-rate product distribution, never post-processed",
        },
    }

    out_path = out_dir / "204-trackL-sufficient-statistic-m64.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
