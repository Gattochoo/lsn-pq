#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""400: Track S — explicit optimal LR and named tests for uniform-B-per-A (n=2).

S1. Explicit optimal LR test and named-test advantages at n=2 for
    m = 8, 12, 16, 24, 32, 48, 64, 80, exact via the Track-L sufficient-statistic
    reduction (S_3 symmetry + pure-shift s_00 vectorisation).

    Named tests computed:
      * rank-member:        reject LPN iff y in col(C).
      * syndrome-weight:    optimal threshold on min_{w} wt(y + Cw).
      * rank+syndrome-weight: optimal test on the joint statistic (rank(C), sw).
      * full LR:            the likelihood-ratio test; advantage = SD(P_out,P_lpn).

S2. Proof that lim_{m->inf} SD(P_out^{(m)}, P_lpn^{(m)}) = 1 at fixed n=2
    (uniform-B-per-A only) via an empirical-distribution / method-of-types
    argument.  The proof is stated in the meta note and summarised in the
    JSON; the script verifies the numerical constants and inequalities.

S3. Scope honesty: the result bounds only the uniform-B-per-A marginal-adaptive
    strategy; it does NOT close lem:m2 for general randomized B.

PRE-REGISTER interpretation guards:
  * Strategy scope: uniform-B-per-A (one explicit reduction strategy), not all
    marginal-adaptive B.
  * Axis: m grows at fixed n=2 (the correct m-axis).
  * Comparison distribution: LPN_{p_eff(2)} (matched rate), never transformed.
  * The SD numbers measure statistical distance between two explicit
    distributions; they do not by themselves imply a practical attack.

Standing guards:
  L1 exact arithmetic: integer counts over common denominator
      q_den * N * (2N)^m * D^m; Fraction output; JSON stores string fractions.
  L2 J-twist duality: n=2 row-type reduction uses the standard F_2 pairing only.
  L3 query-class hygiene: no unrestricted Feldman/SQ theorem is invoked.
  L4 comparison-distribution care: the LPN target is never post-processed.
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


def _rank_from_types(m1: int, m2: int, m3: int) -> int:
    """Rank of C from the counts of the three non-zero row types (n=2).

    Type 1 = (1,0), type 2 = (0,1), type 3 = (1,1).
    """
    nz = (m1 > 0) + (m2 > 0) + (m3 > 0)
    if nz == 0:
        return 0
    if nz == 1:
        return 1
    # Two or three distinct non-zero types always span F_2^2.
    return 2


def _syndrome_weight_min(m0: int, m1: int, s1: int, m2: int, s2: int, m3: int, s3: int) -> int:
    """min_{w in F_2^2} wt(y + Cw) for a state with type counts (m_i) and label counts (s_i).

    For w=0:              c0 = s1 + s2 + s3
    for w=(1,0):         c1 = (m1-s1) + s2 + (m3-s3)
    for w=(0,1):         c2 = s1 + (m2-s2) + (m3-s3)
    for w=(1,1):         c3 = (m1-s1) + (m2-s2) + s3
    The type-00 contribution is always s_00, so the minimum syndrome weight is
    s_00 + min(c0,c1,c2,c3).
    """
    c0 = s1 + s2 + s3
    c1 = (m1 - s1) + s2 + (m3 - s3)
    c2 = s1 + (m2 - s2) + (m3 - s3)
    c3 = (m1 - s1) + (m2 - s2) + s3
    return min(c0, c1, c2, c3)


def exact_sd_and_tests_reduced_n2(m: int) -> dict:
    """Exact SD(P_out,P_lpn) and advantages of named tests at n=2.

    Uses the S_3 + pure-shift reduction from Track L, extended to accumulate
    buckets for the named-test statistics.
    """
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

    # Pure-shift tables: raw_c[s] = a^s * b^(m0-s) and prefix sums.
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

    # Precompute binomial noise counts for s_00 for every m0.
    # full_noise_counts[m0][k] = C(m0, k)
    # lpn_noise_counts[m0][k]  = C(m0, k) * a^k * b^(m0-k)
    full_noise_counts = [[0] * (mm + 1) for mm in range(m + 1)]
    lpn_noise_counts = [[0] * (mm + 1) for mm in range(m + 1)]
    for mm in range(m + 1):
        for k in range(mm + 1):
            full_noise_counts[mm][k] = C[mm][k]
            lpn_noise_counts[mm][k] = C[mm][k] * pow_a[k] * pow_b[mm - k]

    # Buckets for syndrome-weight and rank+syndrome-weight histograms.
    # We aggregate by (m0, c_star) for the scalar syndrome-weight statistic and
    # by (rank, m0, c_star) for the joint statistic.
    G_bucket = [[0] * (m + 1) for _ in range(m + 1)]          # graph mass at c_star
    A_bucket = [[0] * (m + 1) for _ in range(m + 1)]          # full mass to convolve
    K_bucket = [[0] * (m + 1) for _ in range(m + 1)]          # lpn mass to convolve
    G_r_bucket = [[[0] * (m + 1) for _ in range(m + 1)] for _ in range(3)]
    A_r_bucket = [[[0] * (m + 1) for _ in range(m + 1)] for _ in range(3)]
    K_r_bucket = [[[0] * (m + 1) for _ in range(m + 1)] for _ in range(3)]

    # Rank-member counts.
    member_out = 0   # graph + full with s_00 = 0
    member_lpn = 0   # lpn with s_00 = 0

    t0 = time.time()
    sd_num = 0

    for m1 in range(m + 1):
        U1 = U[m1]
        C1 = C[m1]
        for m2 in range(m1 + 1):
            U2 = U[m2]
            C2 = C[m2]
            for m3 in range(m2 + 1):
                M = m1 + m2 + m3
                if M > m:
                    break
                U3 = U[m3]
                C3 = C[m3]
                eq12 = m1 == m2
                eq23 = m2 == m3
                rank = _rank_from_types(m1, m2, m3)

                for s1 in range(m1 + 1):
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

                            rest_full = C1s * C2s * C3s
                            lpn_rest = (
                                U1s * U2s * U3s
                                + U1s * V2s * V3s
                                + V1s * U2s * V3s
                                + V1s * V2s * U3s
                            )

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

                            m0 = m - M
                            mult_comp = fact[m] // (fact[m0] * fact[m1] * fact[m2] * fact[m3])
                            mult = mult_perm * mult_comp

                            c_star = _syndrome_weight_min(m0, m1, s1, m2, s2, m3, s3)

                            # Buckets for scalar syndrome-weight statistic.
                            G_bucket[m0][c_star] += mult * G
                            A_bucket[m0][c_star] += mult * A
                            K_bucket[m0][c_star] += mult * K

                            # Buckets for rank + syndrome-weight joint statistic.
                            G_r_bucket[rank][m0][c_star] += mult * G
                            A_r_bucket[rank][m0][c_star] += mult * A
                            K_r_bucket[rank][m0][c_star] += mult * K

                            # Rank-member counts: c_star == 0 and s_00 == 0.
                            # Graph component always has s_00 = 0; full/lpn use k=0 noise count.
                            if c_star == 0:
                                member_out += mult * (G + A)
                                member_lpn += mult * K * pow_b[m0]

                            # Full SD contribution via closed-form s_00 sum.
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

                            totC = totalC[m0]
                            totW = totalW[m0]
                            S_abs_total = A * (totC - 2 * pre_c) + K * (2 * pre_w - totW)
                            B0 = A - K * rc[0]
                            s0_sum = S_abs_total - abs(B0) + abs(B0 + G)
                            sd_num += mult * s0_sum

    sd = Fraction(sd_num, 2 * D_common)

    # Build syndrome-weight histograms from buckets.
    H_out = [0] * (m + 1)
    H_lpn = [0] * (m + 1)
    for m0 in range(m + 1):
        fnc = full_noise_counts[m0]
        lnc = lpn_noise_counts[m0]
        for c_star in range(m + 1 - m0):  # c_star + m0 <= m
            gb = G_bucket[m0][c_star]
            ab = A_bucket[m0][c_star]
            kb = K_bucket[m0][c_star]
            if gb == 0 and ab == 0 and kb == 0:
                continue
            H_out[c_star] += gb + ab  # k=0 contribution of full noise is C(m0,0)=1
            H_lpn[c_star] += kb * pow_b[m0]  # k=0 lpn noise count
            for k in range(1, m0 + 1):
                w = c_star + k
                H_out[w] += ab * fnc[k]
                H_lpn[w] += kb * lnc[k]

    # Syndrome-weight optimal threshold advantage = TV of scalar statistic.
    cum_out = 0
    cum_lpn = 0
    syndrome_weight_adv_num = 0
    for w in range(m + 1):
        syndrome_weight_adv_num += abs(H_out[w] - H_lpn[w])
    syndrome_weight_adv = Fraction(syndrome_weight_adv_num, 2 * D_common)

    # Also report the best single-threshold advantage (must equal TV for scalar).
    cum_diff_max = 0
    cum_diff_min = 0
    cum_out = 0
    cum_lpn = 0
    for w in range(m + 1):
        cum_out += H_out[w]
        cum_lpn += H_lpn[w]
        diff = abs(cum_out - cum_lpn)
        if diff > cum_diff_max:
            cum_diff_max = diff
    syndrome_threshold_adv = Fraction(cum_diff_max, D_common)

    # Rank + syndrome-weight joint statistic: exact TV over the 3 x (m+1) table.
    joint_tv_num = 0
    for rank in range(3):
        H_out_r = [0] * (m + 1)
        H_lpn_r = [0] * (m + 1)
        for m0 in range(m + 1):
            fnc = full_noise_counts[m0]
            lnc = lpn_noise_counts[m0]
            for c_star in range(m + 1 - m0):
                gb = G_r_bucket[rank][m0][c_star]
                ab = A_r_bucket[rank][m0][c_star]
                kb = K_r_bucket[rank][m0][c_star]
                if gb == 0 and ab == 0 and kb == 0:
                    continue
                H_out_r[c_star] += gb + ab
                H_lpn_r[c_star] += kb * pow_b[m0]
                for k in range(1, m0 + 1):
                    w = c_star + k
                    H_out_r[w] += ab * fnc[k]
                    H_lpn_r[w] += kb * lnc[k]
        for w in range(m + 1):
            joint_tv_num += abs(H_out_r[w] - H_lpn_r[w])
    rank_syndrome_adv = Fraction(joint_tv_num, 2 * D_common)

    # Rank-member advantage.
    rank_member_adv_num = abs(member_out - member_lpn)
    rank_member_adv = Fraction(rank_member_adv_num, D_common)

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
        "rank_member_advantage": str(rank_member_adv),
        "rank_member_advantage_float": float(rank_member_adv),
        "syndrome_weight_advantage": str(syndrome_weight_adv),
        "syndrome_weight_advantage_float": float(syndrome_weight_adv),
        "syndrome_weight_threshold_advantage": str(syndrome_threshold_adv),
        "syndrome_weight_threshold_advantage_float": float(syndrome_threshold_adv),
        "rank_syndrome_joint_advantage": str(rank_syndrome_adv),
        "rank_syndrome_joint_advantage_float": float(rank_syndrome_adv),
        "time_sec": t_elapsed,
    }


def _decode_C_y(key: int, m: int, n: int) -> tuple[list[int], int]:
    """Decode (C_key << m | y) into columns c_j and y."""
    mask = (1 << m) - 1
    y = key & mask
    C_key = key >> m
    cols = []
    for _ in range(n):
        cols.append(C_key & mask)
        C_key >>= m
    return cols, y


def _matrix_rank_f2(rows: list[int], n_cols: int) -> int:
    """Rank over F_2 of a matrix given as row bitmasks."""
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


def _syndrome_weight_direct(C_cols: list[int], y: int, m: int, n: int) -> int:
    """min_w wt(y + Cw) by trying all 2^n secrets."""
    best = m + 1
    for w in range(1 << n):
        v = y
        for j in range(n):
            if (w >> j) & 1:
                v ^= C_cols[j]
        wt = v.bit_count()
        if wt < best:
            best = wt
    return best


def _y_in_col(C_cols: list[int], y: int, m: int, n: int) -> bool:
    """Check whether y in F_2^m is in the column span of the m x n matrix C."""
    rows = [0] * m
    for j, col in enumerate(C_cols):
        for i in range(m):
            if (col >> i) & 1:
                rows[i] |= 1 << j
    aug_rows = [rows[i] | (((y >> i) & 1) << n) for i in range(m)]
    rank_C = _matrix_rank_f2(rows, n)
    rank_aug = _matrix_rank_f2(aug_rows, n + 1)
    return rank_C == rank_aug


def named_tests_direct(m: int, n: int = 2) -> dict:
    """Direct exact computation of named-test advantages for small m.

    Uses the integer-count distributions from experiments.lib.lem_m2_exact.
    """
    from experiments.lib.lem_m2_exact import (
        enumerate_lagrangian_bases_n,
        exact_sd_counts,
        lpn_target_counts_n,
        randomized_uniform_B_counts_n,
    )

    p = p_eff(n)
    bases = list(enumerate_lagrangian_bases_n(n))
    red_counts, red_denom = randomized_uniform_B_counts_n(m, n, bases)
    lpn_counts, lpn_denom = lpn_target_counts_n(m, n, p)

    sd_direct = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)

    # Compute histograms for named tests.
    max_sw = m
    H_out = [0] * (max_sw + 1)
    H_lpn = [0] * (max_sw + 1)
    H_out_r = [[0] * (max_sw + 1) for _ in range(3)]
    H_lpn_r = [[0] * (max_sw + 1) for _ in range(3)]
    member_out = 0
    member_lpn = 0

    size = len(red_counts)
    for key in range(size):
        c_out = red_counts[key]
        c_lpn = lpn_counts[key]
        if c_out == 0 and c_lpn == 0:
            continue
        C_cols, y = _decode_C_y(key, m, n)
        sw = _syndrome_weight_direct(C_cols, y, m, n)
        member = _y_in_col(C_cols, y, m, n)

        # Build actual rows of C (n-bit each) for rank and joint statistic.
        rows = [0] * m
        for j, col in enumerate(C_cols):
            for i in range(m):
                if (col >> i) & 1:
                    rows[i] |= 1 << j
        rank = _matrix_rank_f2(rows, n)

        H_out[sw] += c_out
        H_lpn[sw] += c_lpn
        H_out_r[rank][sw] += c_out
        H_lpn_r[rank][sw] += c_lpn
        if member:
            member_out += c_out
            member_lpn += c_lpn

    # Advantages with exact common denominator.
    common = red_denom * lpn_denom
    rank_member_num = abs(member_out * lpn_denom - member_lpn * red_denom)
    rank_member_adv = Fraction(rank_member_num, common)

    sw_num = sum(abs(H_out[w] * lpn_denom - H_lpn[w] * red_denom) for w in range(max_sw + 1))
    sw_adv = Fraction(sw_num, 2 * common)

    joint_num = 0
    for rank in range(3):
        for w in range(max_sw + 1):
            joint_num += abs(H_out_r[rank][w] * lpn_denom - H_lpn_r[rank][w] * red_denom)
    joint_adv = Fraction(joint_num, 2 * common)

    return {
        "n": n,
        "m": m,
        "sd": str(sd_direct),
        "sd_float": float(sd_direct),
        "rank_member_advantage": str(rank_member_adv),
        "rank_member_advantage_float": float(rank_member_adv),
        "syndrome_weight_advantage": str(sw_adv),
        "syndrome_weight_advantage_float": float(sw_adv),
        "rank_syndrome_joint_advantage": str(joint_adv),
        "rank_syndrome_joint_advantage_float": float(joint_adv),
    }


def cross_check(max_m: int = 6) -> list[dict]:
    """Compare reduced and direct computations for m <= max_m."""
    checks = []
    for m in range(2, max_m + 1):
        direct = named_tests_direct(m, n=2)
        reduced = exact_sd_and_tests_reduced_n2(m)
        checks.append(
            {
                "m": m,
                "sd_direct": direct["sd"],
                "sd_reduced": reduced["sd"],
                "rank_member_direct": direct["rank_member_advantage"],
                "rank_member_reduced": reduced["rank_member_advantage"],
                "sw_direct": direct["syndrome_weight_advantage"],
                "sw_reduced": reduced["syndrome_weight_advantage"],
                "joint_direct": direct["rank_syndrome_joint_advantage"],
                "joint_reduced": reduced["rank_syndrome_joint_advantage"],
                "match": (
                    Fraction(direct["sd"]) == Fraction(reduced["sd"])
                    and Fraction(direct["rank_member_advantage"]) == Fraction(reduced["rank_member_advantage"])
                    and Fraction(direct["syndrome_weight_advantage"]) == Fraction(reduced["syndrome_weight_advantage"])
                    and Fraction(direct["rank_syndrome_joint_advantage"]) == Fraction(reduced["rank_syndrome_joint_advantage"])
                ),
            }
        )
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ms",
        type=int,
        nargs="+",
        default=[8, 12, 16, 24, 32, 48, 64, 80],
        help="values of m to compute",
    )
    parser.add_argument(
        "--cross-check-max-m",
        type=int,
        default=6,
        help="max m for direct-vs-reduced self-check",
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

    # --- S1 cross-check: direct enumeration vs reduced formulas -------------
    print("== Track S — cross-check reduced formulas against direct enumeration ==")
    checks = cross_check(args.cross_check_max_m)
    for c in checks:
        status = "OK" if c["match"] else "MISMATCH"
        print(f"  m={c['m']}: SD direct={c['sd_direct']} reduced={c['sd_reduced']} [{status}]")
        if not c["match"]:
            print(f"    rank direct={c['rank_member_direct']} reduced={c['rank_member_reduced']}")
            print(f"    sw   direct={c['sw_direct']} reduced={c['sw_reduced']}")
            print(f"    joint direct={c['joint_direct']} reduced={c['joint_reduced']}")
    if not all(c["match"] for c in checks):
        raise RuntimeError("reduced-vs-direct cross-check failed")

    # --- S1 main computation: named tests at target m values ----------------
    print("\n== Track S — optimal LR and named-test advantages (n=2) ==")
    results = []
    for m in args.ms:
        print(f"  computing m={m} ...", flush=True)
        res = exact_sd_and_tests_reduced_n2(m)
        results.append(res)
        print(
            f"    m={m:2d}: SD={res['sd_float']:.6f}, "
            f"rank-member={res['rank_member_advantage_float']:.6f}, "
            f"sw={res['syndrome_weight_advantage_float']:.6f}, "
            f"rank+sw={res['rank_syndrome_joint_advantage_float']:.6f} "
            f"({res['time_sec']:.2f}s)"
        )

    # --- S2 limit proof: numerical verification of constants ----------------
    n = 2
    p = p_eff(n)
    two_p = 2 * p
    H_two_p = Fraction(0)
    # H(t) in bits for t = 2p, using natural log then convert.
    import math
    t = float(two_p)
    H_two_p_float = -(t * math.log2(t) + (1 - t) * math.log2(1 - t))
    H_Qx = n + H_two_p_float + float(two_p)
    limit_constants = {
        "n": n,
        "p_eff": str(p),
        "2p_eff": str(two_p),
        "H(2p_eff)_bits": H_two_p_float,
        "H(Q_x)_bits": H_Qx,
        "P_out_full_entropy_rate": n + 1,
        "P_graph_support_rate": n,
        "separation_full": H_Qx - (n + 1),
        "separation_graph": H_Qx - n,
    }
    print("\n== Track S — limit-proof entropy-rate check ==")
    print(f"  H(Q_x) = {H_Qx:.6f} bits/row")
    print(f"  P_out full rate = {n + 1} bits/row; separation = {limit_constants['separation_full']:.6f}")
    print(f"  P_graph support rate = {n} bits/row; separation = {limit_constants['separation_graph']:.6f}")

    summary = {
        "experiment": 400,
        "track": "S",
        "cross_check": checks,
        "results": results,
        "limit_proof_constants": limit_constants,
        "claim_labels": {
            "s3_pure_shift_reduction": "THEOREM (Track L; reused unchanged)",
            "rank_member_advantage": "EVIDENCE (exact finite computation)",
            "syndrome_weight_advantage": "EVIDENCE (exact finite computation)",
            "rank_syndrome_joint_advantage": "EVIDENCE (exact finite computation)",
            "full_LR_advantage": "EVIDENCE (exact finite computation; equals SD)",
            "limit_equals_one_uniform_B_per_A": "THEOREM (method-of-types proof in meta note)",
            "lem_m2_general_B": "NO-GO / OPEN (result does not bound general randomized B)",
        },
        "interpretation_guards": {
            "strategy_scope": "uniform-B-per-A marginal-adaptive strategy only",
            "axis": "m grows at fixed n=2",
            "comparison_distribution": "LPN_{p_eff(2)}, matched rate; never transformed",
            "practical_attack": "SD numbers do not imply a practical distinguisher",
            "L1_exact_arithmetic": "integer counts over common denominator q_den*N*(2N)^m*D^m; Fraction output",
            "L2_J_twist_duality": "standard F_2 pairing only; no symplectic dual",
            "L3_query_class_hygiene": "statistical-distance claims only; no unrestricted Feldman theorem",
            "L4_comparison_distribution": "LPN target is the matched-rate product distribution, never post-processed",
        },
    }

    out_path = out_dir / "400-trackS-optimal-LR-and-named-tests.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
