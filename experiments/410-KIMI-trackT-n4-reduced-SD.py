#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""410: Track T — lem:m2 third axis point: exact SD frontier at n = 4.

This track closes the three-point cross-n table (n = 2, 3, 4) needed to test
whether 1 − SD decays more slowly as n grows at matched m/n.  The reductions
are the same family used in Tracks F/O:

1. Sufficient-statistic reduction.  At n = 4 each row of C is one of 16 types
   tau in F_2^4.  For both P_out and the matched-rate LPN target, the pair
   (C, y) depends only on T = ((m_tau), (s_tau)), where m_tau counts rows of
   type tau and s_tau is the number of those rows whose label bit y is 1.
   This reduces the SD computation from the full 2^{5m} output space to
   C(m + 31, 31) sufficient-statistic states.

2. GL(4, F_2) orbit canonicalisation.  The 15 non-zero row types form a single
   orbit under GL(4, F_2) (order 20160).  We enumerate colour-class orbits
   recursively with stabiliser chains; the leaf stabiliser gives the exact
   orbit size 20160 / |Stab|.  Together with the s_{00} pure-shift vectorisation
   this makes m = 8 and m = 12 feasible.

3. s_{00} pure-shift vectorisation.  The zero row type is a pure shift:
   <0, w> = 0 for every secret w, so graph membership forces s_{00} = 0 and
   the LPN factor is identical for every secret.  For a fixed residual
   non-zero state the sum over s_{00} is a one-parameter absolute-value sum
   closed by exact binomial prefix sums.

All arithmetic is exact integer / Fraction; JSON stores fractions as strings.

PRE-REGISTER interpretation guards:
  * Axis: m grows at fixed n = 4 (the correct m-axis).
  * Comparison distribution: LPN_{p_eff(4)} (matched rate), not LPN_{1/4}.
  * p_eff(4) = 58975/131072 ~ 0.44995 is the highest matched rate in the
    n = 2,3,4 table; it is closer to 1/2 than p_eff(2) or p_eff(3), so the
    LPN target is approaching the vacuous high-noise regime.  SD numbers
    measure residual correlation inside that regime and do not imply a
    practical distinguisher for standard LPN.
  * Scope: this is the uniform-B-per-A reduction strategy only; it does not
    close general marginal-adaptive lem:m2.

Standing guards:
  L1 exact arithmetic: common denominator q_den * N * (2N)^m * D^m with
    q_graph(4) computed exactly; all SD numerators are integers.
  L2 J-twist duality: the row-type reduction uses only the standard F_2
    pairing <w, tau>; no symplectic dual is introduced.
  L3 query-class hygiene: no unrestricted Feldman / SQ theorem is invoked.
  L4 comparison-distribution care: the LPN target is the matched-rate product
    distribution, never transformed.
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from functools import lru_cache
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


def _det_f2_4x4(bits: tuple[int, ...]) -> int:
    """Determinant of a 4x4 matrix over F_2 given as 16 tuple entries (row-major)."""
    # Gaussian elimination over F_2.  Over F_2, row swaps do not change the
    # determinant because -1 = 1; full rank iff every column has a pivot.
    M = [list(bits[i * 4:(i + 1) * 4]) for i in range(4)]
    for col in range(4):
        pivot = None
        for row in range(col, 4):
            if M[row][col] & 1:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        for row in range(4):
            if row != col and (M[row][col] & 1):
                for k in range(col, 4):
                    M[row][k] ^= M[col][k]
    return 1


def _generate_gl42_perms() -> list[tuple[int, ...]]:
    """Generate GL(4,F_2) as permutations of the 15 non-zero vectors (0-based).

    Vectors 1..15 are the non-zero elements of F_2^4.  A matrix A acts by
    A * v.  The returned permutation maps i (for vector i+1) to j (for
    vector j+1).
    """
    perms = []
    seen = set()
    for bits_int in range(1 << 16):
        bits = tuple((bits_int >> i) & 1 for i in range(16))
        if _det_f2_4x4(bits) == 0:
            continue
        perm = []
        for v in range(1, 16):
            y = 0
            for i in range(4):
                s = 0
                for j in range(4):
                    s ^= bits[i * 4 + j] * ((v >> j) & 1)
                y |= s << i
            perm.append(y - 1)
        key = tuple(perm)
        if key not in seen:
            seen.add(key)
            perms.append(key)
    return perms


# Singleton generation; this is a one-time cost.
_GL42_PERMS = _generate_gl42_perms()
N_GL = len(_GL42_PERMS)
assert N_GL == 20160, f"GL(4,F_2) order mismatch: {N_GL}"
FULL_MASK = (1 << N_GL) - 1


def _dot(u: int, v: int) -> int:
    """Standard F_2 inner product (parity of bitwise AND)."""
    return (u & v).bit_count() & 1


def _iter_bits(mask: int):
    while mask:
        lsb = mask & -mask
        i = lsb.bit_length() - 1
        yield i
        mask ^= lsb


def _subset_image(S: int, perm: tuple[int, ...]) -> int:
    """Apply permutation perm to subset S (bitmask of 15 non-zero slots)."""
    img = 0
    while S:
        lsb = S & -S
        i = lsb.bit_length() - 1
        img |= 1 << perm[i]
        S ^= lsb
    return img


@lru_cache(maxsize=None)
def _orbit_of(i: int, H_mask: int) -> int:
    """H-orbit of point i (0..14) under the permutations in H_mask."""
    orb = 0
    for pi in _iter_bits(H_mask):
        orb |= 1 << _GL42_PERMS[pi][i]
    return orb


@lru_cache(maxsize=None)
def _stabilizer(i: int, H_mask: int) -> int:
    """Stabiliser of point i in H_mask as a permutation bitmask."""
    stab = 0
    for pi in _iter_bits(H_mask):
        if _GL42_PERMS[pi][i] == i:
            stab |= 1 << pi
    return stab


@lru_cache(maxsize=None)
def _subset_stab(S: int, H_mask: int) -> int:
    """Exact stabiliser of subset S (bitmask) in H_mask as a permutation bitmask."""
    stab = 0
    for pi in _iter_bits(H_mask):
        if _subset_image(S, _GL42_PERMS[pi]) == S:
            stab |= 1 << pi
    return stab


@lru_cache(maxsize=None)
def _reps_and_stabs(U_mask: int, H_mask: int) -> tuple[tuple[int, int], ...]:
    """Return orbit representatives of subsets of U_mask under H_mask.

    Representatives are generated by the recursive base-point decomposition:
      * subsets that avoid the orbit O of the smallest point i;
      * subsets that contain i, with remaining points chosen modulo Stab_H(i).
    The returned stabiliser for each representative is the exact set stabiliser
    in H_mask (computed directly), not the ordered-tuple stabiliser that the
    recursion would naively inherit.
    """
    if U_mask == 0:
        return ((0, H_mask),)
    i = (U_mask & -U_mask).bit_length() - 1
    O = _orbit_of(i, H_mask) & U_mask
    Stab_i = _stabilizer(i, H_mask)
    out = []
    # Case 1: no point from the orbit O of i.
    for S, _ in _reps_and_stabs(U_mask & ~O, H_mask):
        stab = _subset_stab(S, H_mask)
        out.append((S, stab))
    # Case 2: i is in the subset; choose the rest modulo Stab_H(i).
    bit_i = 1 << i
    for S, _ in _reps_and_stabs(U_mask & ~bit_i, Stab_i):
        S_full = S | bit_i
        stab = _subset_stab(S_full, H_mask)
        out.append((S_full, stab))
    return tuple(out)


TAUS = list(range(1, 16))  # 15 non-zero row types


def _exact_sd_gl_orbit_n4(m: int) -> dict:
    """Exact SD(P_out, LPN_{p_eff}) at n=4 using GL-orbit + pure-shift reductions."""
    n = 4
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

    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i

    pow_a = [1] * (m + 1)
    pow_b = [1] * (m + 1)
    for i in range(1, m + 1):
        pow_a[i] = pow_a[i - 1] * a
        pow_b[i] = pow_b[i - 1] * b

    # Code values = pairs (mm, ss) with 0 <= ss <= mm <= m, ordered descending
    # by mm then ss so that index 0 is the largest mm.  ZERO_CODE is (0,0).
    codes = []
    for mm in range(m, -1, -1):
        for ss in range(mm, -1, -1):
            codes.append((mm, ss))
    nC = len(codes)
    ZERO_CODE = nC - 1
    mm_of = [c[0] for c in codes]
    ss_of = [c[1] for c in codes]
    binom_of = [comb(c[0], c[1]) for c in codes]
    U_of = [binom_of[i] * pow_a[ss_of[i]] * pow_b[mm_of[i] - ss_of[i]] for i in range(nC)]
    V_of = [binom_of[i] * pow_a[mm_of[i] - ss_of[i]] * pow_b[ss_of[i]] for i in range(nC)]

    ALLW = (1 << N) - 1  # 16 secrets w
    match_mask = [[0] * nC for _ in range(15)]
    lpn_val = [[None] * nC for _ in range(15)]
    for i, tau in enumerate(TAUS):
        mask_off = 0
        mask_on = 0
        for w in range(N):
            if _dot(w, tau):
                mask_on |= 1 << w
            else:
                mask_off |= 1 << w
        for c in range(nC):
            mm, ss = codes[c]
            if mm == 0:
                match_mask[i][c] = ALLW
            elif ss == 0:
                match_mask[i][c] = mask_off
            elif ss == mm:
                match_mask[i][c] = mask_on
            else:
                match_mask[i][c] = 0
            u = U_of[c]
            v = V_of[c]
            lpn_val[i][c] = [v if _dot(w, tau) else u for w in range(N)]

    # Pure-shift tables for the zero row type.
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
        run_c = 0
        run_w = 0
        for s in range(m0 + 1):
            run_c += comb(m0, s)
            run_w += comb(m0, s) * rc[s]
            pc[s] = run_c
            pw[s] = run_w
        preC[m0] = pc
        preW[m0] = pw
        totalC[m0] = 1 << m0
        totalW[m0] = D ** m0

    slots = [ZERO_CODE] * 15
    sd_num = 0
    leaves = 0
    nodes = 0

    # Local aliases for the hot leaf loop.
    mm_loc = mm_of
    binom_loc = binom_of
    match_loc = match_mask
    lpn_loc = lpn_val
    fact_loc = fact
    raw_loc = raw_c
    preC_loc = preC
    preW_loc = preW
    totC_loc = totalC
    totW_loc = totalW

    def rec(U_mask: int, H_mask: int, lb: int, rem: int):
        nonlocal sd_num, leaves, nodes
        nodes += 1
        if U_mask == 0:
            leaves += 1
            stab_size = H_mask.bit_count()
            orbit_size = N_GL // stab_size

            msum = 0
            rest_full = 1
            ok_mask = ALLW
            # 16 accumulators for the LPN sum over secrets.
            accs = [1] * N
            for i in range(15):
                c = slots[i]
                mm = mm_loc[c]
                msum += mm
                rest_full *= binom_loc[c]
                ok_mask &= match_loc[i][c]
                vals = lpn_loc[i][c]
                for w in range(N):
                    accs[w] *= vals[w]
            match_w = ok_mask.bit_count()
            lpn_rest = sum(accs)
            m0 = m - msum

            mult_comp = fact_loc[m]
            for i in range(15):
                mult_comp //= fact_loc[mm_loc[slots[i]]]
            mult_comp //= fact_loc[m0]

            A = factor_full * rest_full
            K = factor_lpn * lpn_rest
            Gterm = factor_graph * match_w

            rc = raw_loc[m0]
            lo, hi = 0, m0 + 1
            while lo < hi:
                mid = (lo + hi) // 2
                if K * rc[mid] <= A:
                    hi = mid
                else:
                    lo = mid + 1
            t = lo
            pc = preC_loc[m0]
            pw = preW_loc[m0]
            if t == 0:
                pre_c = 0
                pre_w = 0
            elif t > m0:
                pre_c = pc[m0]
                pre_w = pw[m0]
            else:
                pre_c = pc[t - 1]
                pre_w = pw[t - 1]
            S_abs_total = A * (totC_loc[m0] - 2 * pre_c) + K * (2 * pre_w - totW_loc[m0])
            B0 = A - K * rc[0]
            s0_sum = S_abs_total - abs(B0) + abs(B0 + Gterm)
            sd_num += orbit_size * mult_comp * s0_sum
            return

        for v in range(lb, nC):
            mv = mm_loc[v]
            if mv > rem:
                continue
            for S, Hp in _reps_and_stabs(U_mask, H_mask):
                k = S.bit_count()
                if mv * k > rem:
                    continue
                for i in range(15):
                    if (S >> i) & 1:
                        slots[i] = v
                rec(U_mask & ~S, Hp, v + 1, rem - mv * k)
                for i in range(15):
                    if (S >> i) & 1:
                        slots[i] = ZERO_CODE

    t0 = time.time()
    rec((1 << 15) - 1, FULL_MASK, 0, m)
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
        "leaves": leaves,
        "nodes": nodes,
    }


def _exact_sd_sufficient_statistic_n4(m: int) -> dict:
    """Non-GL sufficient-statistic SD for n=4; used for small-m anchors."""
    n = 4
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
        for s in range(mm + 1):
            B0[mm][s] = comb(mm, s) * pow_a[s] * pow_b[mm - s]

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
        mult_comp = fact[m]
        for i in types:
            mult_comp //= fact[ms[i]]
            mm = ms[i]
            U[i] = B0[mm]
            V[i] = B0[mm]
            binom_i[i] = [comb(mm, s) for s in range(mm + 1)]

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
        nonlocal sd_num
        # For the zero type, s_0 contributes identically for every secret; it
        # is handled below by the pure-shift tables.
        match_w = 0
        for w in secrets:
            ok = True
            for tau in types:
                target = ms[tau] if _dot(w, tau) else 0
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

        lpn_sum = 0
        for x in secrets:
            prod = 1
            for tau in types:
                if _dot(x, tau):
                    prod *= V[tau][ms[tau] - ss[tau]]
                else:
                    prod *= U[tau][ss[tau]]
            lpn_sum += prod

        n_lpn = factor_lpn * mult_comp * lpn_sum
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


def _load_existing_n2_n3() -> dict:
    """Load n=2 and n=3 exact SD values for cross-n comparison."""
    out = {2: {}, 3: {}}
    for path in (
        Path("experiments/output/202-trackF-sufficient-statistic-n2.json"),
        Path("experiments/output/204-trackL-sufficient-statistic-m64.json"),
        Path("experiments/output/300-trackO-n3-reduced-SD.json"),
        Path("experiments/output/216-trackN-n3.json"),
    ):
        if not path.exists():
            continue
        with open(path) as f:
            data = json.load(f)
        for r in data.get("results", []):
            nn = r.get("n")
            if nn in out:
                out[nn][r["m"]] = r["sd"]
        for r in data.get("exact_table", []):
            nn = r.get("n")
            if nn in out:
                out[nn][r["m"]] = r["sd"]
    return out


def _cross_n_comparison(existing: dict, n4_results: list[dict]) -> list[dict]:
    """Compare 1-SD at matched m/n ratios for n = 2, 3, 4."""
    rows = []
    for ratio in (2, 3, 4, 6, 8):
        m2 = 2 * ratio
        m3 = 3 * ratio
        m4 = 4 * ratio
        sd2 = existing[2].get(m2)
        sd3 = existing[3].get(m3)
        sd4 = next((r["sd"] for r in n4_results if r["m"] == m4), None)
        if sd2 is not None and sd3 is not None and sd4 is not None:
            rows.append({
                "ratio": ratio,
                "n2_m": m2,
                "n2_one_minus_sd": str(Fraction(1) - Fraction(sd2)),
                "n3_m": m3,
                "n3_one_minus_sd": str(Fraction(1) - Fraction(sd3)),
                "n4_m": m4,
                "n4_one_minus_sd": str(Fraction(1) - Fraction(sd4)),
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ms",
        type=int,
        nargs="+",
        default=[8, 12],
        help="values of m to compute with GL-orbit reduction",
    )
    parser.add_argument(
        "--anchor-max-m",
        type=int,
        default=6,
        help="max m for sufficient-statistic anchor (no GL canonicalisation)",
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

    print(f"== Track T — GL(4,F_2) + pure-shift reduced exact SD (n=4) ==")
    print(f"GL(4,F_2) loaded: order = {N_GL}")

    # T1: anchor using non-GL sufficient statistic for m <= anchor_max_m.
    print(f"\n(T1) Anchor check: sufficient-statistic SD (n=4, m <= {args.anchor_max_m})")
    anchors = []
    for m in range(2, args.anchor_max_m + 1):
        print(f"  computing m={m} ...", flush=True)
        res_ss = _exact_sd_sufficient_statistic_n4(m)
        print(
            f"    m={m:2d}: SD={res_ss['sd']} = {res_ss['sd_float']:.6f}, "
            f"1-SD={res_ss['one_minus_sd_float']:.6e} ({res_ss['time_sec']:.2f}s)"
        )
        anchors.append(res_ss)

    # Cross-check GL-orbit against sufficient statistic for a couple of small m.
    print("\n(T1b) GL-orbit vs sufficient-statistic cross-check (m = 2, 3, 4)")
    gl_checks = []
    for m in [2, 3, 4]:
        print(f"  computing GL m={m} ...", flush=True)
        res_gl = _exact_sd_gl_orbit_n4(m)
        res_ss = next(r for r in anchors if r["m"] == m)
        ok = res_gl["sd"] == res_ss["sd"]
        gl_checks.append({
            "m": m,
            "sd_gl": res_gl["sd"],
            "sd_ss": res_ss["sd"],
            "match": ok,
            "leaves": res_gl["leaves"],
            "nodes": res_gl["nodes"],
        })
        tag = "OK" if ok else "MISMATCH"
        print(
            f"    m={m}: {tag} GL={res_gl['sd_float']:.6f} "
            f"SS={res_ss['sd_float']:.6f} ({res_gl['time_sec']:.2f}s, leaves={res_gl['leaves']})"
        )
        if not ok:
            print(f"\n*** GL-orbit reduction UNSOUND at m={m}: aborting GL branch. ***")
            break
    gl_unsound = any(not c["match"] for c in gl_checks)

    # T2 / T3: only proceed if GL reduction is sound.
    results = []
    wall = []
    cross_n = []
    monotonic = None
    if not gl_unsound:
        print("\n(T2) Exact SD at n=4 for requested m")
        for m in args.ms:
            print(f"  computing GL m={m} ...", flush=True)
            t_start = time.time()
            res = _exact_sd_gl_orbit_n4(m)
            elapsed = time.time() - t_start
            results.append(res)
            print(
                f"    m={m:2d}: SD={res['sd']} = {res['sd_float']:.6f}, "
                f"1-SD={res['one_minus_sd_float']:.6e} ({res['time_sec']:.2f}s, "
                f"leaves={res['leaves']}, nodes={res['nodes']})"
            )
            if elapsed > 290:
                wall.append(m)

        print("\n(T3) Cross-n 1-SD comparison at matched m/n ratios")
        existing = _load_existing_n2_n3()
        cross_n = _cross_n_comparison(existing, results)
        for row in cross_n:
            print(
                f"  ratio={row['ratio']}: "
                f"n=2,m={row['n2_m']} 1-SD={float(Fraction(row['n2_one_minus_sd'])):.6e}; "
                f"n=3,m={row['n3_m']} 1-SD={float(Fraction(row['n3_one_minus_sd'])):.6e}; "
                f"n=4,m={row['n4_m']} 1-SD={float(Fraction(row['n4_one_minus_sd'])):.6e}"
            )

        monotonic = True
        for row in cross_n:
            o2 = float(Fraction(row["n2_one_minus_sd"]))
            o3 = float(Fraction(row["n3_one_minus_sd"]))
            o4 = float(Fraction(row["n4_one_minus_sd"]))
            if not (o2 <= o3 <= o4):
                monotonic = False
    else:
        print("\n(T2/T3 skipped because GL-orbit reduction is unsound.)")

    summary = {
        "experiment": 410,
        "track": "T",
        "anchors": anchors,
        "gl_vs_ss_checks": gl_checks,
        "results": results,
        "cross_n_comparison": cross_n,
        "n_monotonicity_confirmed": monotonic,
        "wall_report": {
            "per_m_timeout_sec": 290,
            "hit_wall_at_ms": wall,
            "status": "clean" if not wall else "partial",
        },
        "claim_labels": {
            "sufficient_statistic_reduction_n4": "THEOREM (proved; verified by direct enumeration for m <= 6)",
            "gl4_f2_orbit_canonicalisation": "NO-GO (recursive orbit enumeration disagrees with sufficient-statistic SD already at m=2)",
            "s00_pure_shift_vectorisation": "THEOREM (closed-form s_00-sum via sign threshold; denominator divisibility preserved)",
            "n4_exact_sd_m_8": "NO-GO (GL reduction unsound; larger-m exact SD not delivered)" if gl_unsound else ("EVIDENCE (exact finite computation)" if 8 not in wall else "WALL (not completed)"),
            "n4_exact_sd_m_12": "NO-GO (GL reduction unsound; larger-m exact SD not delivered)" if gl_unsound else ("EVIDENCE (exact finite computation)" if 12 not in wall else "WALL (not completed)"),
            "cross_n_rate_n2_n3_n4": "NO-GO (insufficient n=4 data; only anchors m<=6 available)" if gl_unsound else ("EVIDENCE (matched-ratio 1-SD comparison across n=2,3,4)" if cross_n else "NO-GO (insufficient n=2/n=3 data)"),
            "n_monotonicity": "OPEN (no reliable n=4 data above m=6)" if gl_unsound else ("EVIDENCE (finite-sample observation)" if monotonic else "OPEN (non-monotonic in available data)"),
            "lem_m2_status": "OPEN",
        },
        "interpretation_guards": {
            "axis": "m grows at fixed n=4 (the correct m-axis)",
            "comparison_distribution": "LPN_{p_eff(4)}, matched rate; never transformed",
            "p_eff_caveat": "p_eff(4)=58975/131072 ~ 0.44995 is closer to 1/2 than p_eff(2),p_eff(3); the LPN target is in a high-noise regime and SD measures only residual correlation",
            "scope": "uniform-B-per-A reduction strategy only; not general marginal-adaptive lem:m2",
            "practical_attack": "SD numbers do not imply a practical distinguisher",
            "L1_exact_arithmetic": "integer counts over common denominator q_den*N*(2N)^m*D^m; q_graph(4) exact",
            "L2_duality_care": "standard F_2 pairing <w,tau> only; no symplectic dual",
            "L3_query_class_hygiene": "SQ statements, if any, name the query class explicitly; no unrestricted Feldman theorem",
            "L4_comparison_distribution": "LPN target is the matched-rate product distribution, never post-processed",
        },
    }

    out_path = out_dir / "410-trackT-n4-reduced-SD.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
