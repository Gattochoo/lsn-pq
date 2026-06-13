#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""300: Track O — lem:m2 second axis point: exact SD frontier at n = 3.

Ports the two Track L reductions to n = 3:

1. GL(3,F_2) orbit canonicalisation.  The seven non-zero row types are the
   non-zero vectors of F_2^3; GL(3,F_2) (order 168) permutes them.  A state is
   a colouring of the seven points by code values (m_tau, s_tau).  We enumerate
   colour-class orbits recursively using the stabiliser chain of the Fano-plane
   automorphism group; the leaf stabiliser gives the exact orbit size
   168 / |Stab|.

2. s_00 pure-shift vectorisation.  The zero row type is a pure shift:
   <0,w> = 0, so the graph membership forces s_00 = 0 and the LPN factor is
   identical for every secret.  For a fixed residual non-zero state, the sum
   over s_00 is a one-parameter absolute-value sum closed by exact binomial
   prefix sums (no floating-point anywhere).

All arithmetic is exact integer / Fraction; JSON stores fractions as strings.

PRE-REGISTER interpretation guards:
  * Axis: m grows at fixed n = 3 (the correct m-axis).
  * Comparison distribution: LPN_{p_eff(3)} (matched rate), not LPN_{1/4}.
  * p_eff(3) = 3367/8192 is very close to 1/2; the SD measures detectability of
    correlation inside a nearly vacuous LPN regime and does not imply a
    practical distinguisher for standard LPN.

Standing guards:
  L1 exact arithmetic: common denominator q_den * N * (2N)^m * D^m with
    q_graph(3) = 1241/4608 = 2^{-9} * 9^{-1}; the odd factor 9 survives.
  L2 J-twist duality: n = 3 row-type reduction uses the standard F_2 pairing
    <w,tau> only; no symplectic dual is introduced.
  L3 query-class hygiene: no unrestricted Feldman/SQ theorem is invoked.
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


def _generate_gl32_perms() -> list[tuple[int, ...]]:
    """Generate GL(3,F_2) as permutations of the seven non-zero vectors (0-based)."""
    def mat_vec(A, v):
        r = 0
        for i in range(3):
            s = 0
            for j in range(3):
                s ^= A[i * 3 + j] * ((v >> j) & 1)
            r |= s << i
        return r

    perms = []
    for bits in __import__("itertools").product([0, 1], repeat=9):
        A = bits
        det = (
            A[0] * (A[4] * A[8] ^ A[5] * A[7])
            ^ A[1] * (A[3] * A[8] ^ A[5] * A[6])
            ^ A[2] * (A[3] * A[7] ^ A[4] * A[6])
        ) & 1
        if det:
            perms.append(tuple(mat_vec(A, vv) - 1 for vv in range(1, 8)))
    return list(set(perms))


PERMS = _generate_gl32_perms()
N_GL = len(PERMS)
FULL_MASK = (1 << N_GL) - 1

# Perm action on subsets 0..127 (bitmask of the seven non-zero slots).
_PERM_SUBSET_IMAGE = []
for p in PERMS:
    arr = [0] * 128
    for S in range(128):
        img = 0
        for i in range(7):
            if (S >> i) & 1:
                img |= 1 << p[i]
        arr[S] = img
    _PERM_SUBSET_IMAGE.append(arr)


def _iter_bits(mask: int):
    while mask:
        lsb = mask & -mask
        i = lsb.bit_length() - 1
        yield i
        mask ^= lsb


@lru_cache(maxsize=None)
def _reps_and_stabs(U_mask: int, H_mask: int) -> tuple[tuple[int, int], ...]:
    """Return orbit representatives of subsets of U_mask under H_mask, with stabilisers."""
    reps = {}
    for S in range(1 << 7):
        if S & ~U_mask:
            continue
        best = S
        for pi in _iter_bits(H_mask):
            img = _PERM_SUBSET_IMAGE[pi][S]
            if img < best:
                best = img
        reps.setdefault(best, S)
    out = []
    for S in reps.values():
        stab = 0
        for pi in _iter_bits(H_mask):
            if _PERM_SUBSET_IMAGE[pi][S] == S:
                stab |= 1 << pi
        out.append((S, stab))
    return tuple(out)


TAUS = list(range(1, 8))


def _dot(u: int, v: int) -> int:
    return (u & v).bit_count() & 1


def exact_sd_reduced_n3(m: int) -> dict:
    """Exact SD(P_out, LPN_{p_eff}) at n=3 using GL-orbit + pure-shift reductions."""
    n = 3
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
    # by (mm, ss) so that code index 0 is the largest value.
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

    ALLW = (1 << 8) - 1
    match_mask = [[0] * nC for _ in range(7)]
    lpn_val = [[None] * nC for _ in range(7)]
    for i, tau in enumerate(TAUS):
        mask_off = 0
        mask_on = 0
        for w in range(8):
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
            lpn_val[i][c] = [v if _dot(x, tau) else u for x in range(8)]

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

    slots = [ZERO_CODE] * 7
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
            p0 = p1 = p2 = p3 = p4 = p5 = p6 = p7 = 1
            for i in range(7):
                c = slots[i]
                mm = mm_loc[c]
                msum += mm
                rest_full *= binom_loc[c]
                ok_mask &= match_loc[i][c]
                vals = lpn_loc[i][c]
                p0 *= vals[0]
                p1 *= vals[1]
                p2 *= vals[2]
                p3 *= vals[3]
                p4 *= vals[4]
                p5 *= vals[5]
                p6 *= vals[6]
                p7 *= vals[7]
            match_w = ok_mask.bit_count()
            lpn_rest = p0 + p1 + p2 + p3 + p4 + p5 + p6 + p7
            m0 = m - msum

            mult_comp = fact_loc[m]
            for i in range(7):
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
                if S == 0:
                    continue
                k = S.bit_count()
                if mv * k > rem:
                    continue
                for i in range(7):
                    if (S >> i) & 1:
                        slots[i] = v
                rec(U_mask & ~S, Hp, v + 1, rem - mv * k)
                for i in range(7):
                    if (S >> i) & 1:
                        slots[i] = ZERO_CODE

    t0 = time.time()
    rec((1 << 7) - 1, FULL_MASK, 0, m)
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


def _load_existing_n3() -> dict[int, str]:
    """Load the exact n=3 table from Tracks F/N (203/216)."""
    out = {}
    for path in (
        Path("experiments/output/203-trackF-sufficient-statistic-n3.json"),
        Path("experiments/output/216-trackN-n3.json"),
    ):
        if not path.exists():
            continue
        with open(path) as f:
            data = json.load(f)
        for r in data.get("results", []):
            if r.get("n") == 3:
                out[r["m"]] = r["sd"]
        for r in data.get("exact_table", []):
            if r.get("n") == 3:
                out[r["m"]] = r["sd"]
    return out


def _load_n2_values() -> dict[int, str]:
    """Load n=2 exact SD values for cross-n comparison."""
    out = {}
    for path in (
        Path("experiments/output/202-trackF-sufficient-statistic-n2.json"),
        Path("experiments/output/204-trackL-sufficient-statistic-m64.json"),
    ):
        if not path.exists():
            continue
        with open(path) as f:
            data = json.load(f)
        for r in data.get("results", []):
            if r.get("n") == 2:
                out[r["m"]] = r["sd"]
    return out


def _cross_n_comparison(n2_vals: dict[int, str], n3_results: list[dict]) -> list[dict]:
    """Compare 1-SD at matched m/n ratios for available data."""
    rows = []
    for ratio in (2, 3, 4, 6, 8):
        m2 = 2 * ratio
        m3 = 3 * ratio
        if m2 in n2_vals and any(r["m"] == m3 for r in n3_results):
            sd2 = Fraction(n2_vals[m2])
            sd3 = Fraction(next(r["sd"] for r in n3_results if r["m"] == m3))
            rows.append({
                "ratio": ratio,
                "n2_m": m2,
                "n2_one_minus_sd": str(Fraction(1) - sd2),
                "n3_m": m3,
                "n3_one_minus_sd": str(Fraction(1) - sd3),
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ms",
        type=int,
        nargs="+",
        default=[16, 20, 24],
        help="values of m to compute at n=3",
    )
    parser.add_argument(
        "--anchor-max-m",
        type=int,
        default=12,
        help="max m for fraction-for-fraction anchor against Track F/N",
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

    existing = _load_existing_n3()
    print("== Track O — GL(3,F_2) + pure-shift reduced exact SD (n=3) ==")

    # O1: anchor against exact n=3 table m <= 12.
    print("\n(O1) Anchor check against Tracks 203/216 (exact n=3, m <= 12)")
    anchors = []
    for m in range(2, args.anchor_max_m + 1):
        if m not in existing:
            continue
        res = exact_sd_reduced_n3(m)
        computed = Fraction(res["sd"])
        expected = Fraction(existing[m])
        ok = computed == expected
        anchors.append({
            "m": m,
            "computed": str(computed),
            "expected": str(expected),
            "match": ok,
        })
        tag = "OK" if ok else "MISMATCH"
        print(f"  m={m:2d}: {tag} ({res['time_sec']:.3f}s)")
        if not ok:
            raise RuntimeError(f"anchor mismatch at m={m}")
    if not all(a["match"] for a in anchors):
        raise RuntimeError("anchor check failed")

    # O2: compute requested new points.
    print("\n(O2) Exact SD at n=3 for requested m")
    results = []
    wall = []
    for m in args.ms:
        print(f"  computing m={m} ...", flush=True)
        t_start = time.time()
        res = exact_sd_reduced_n3(m)
        elapsed = time.time() - t_start
        results.append(res)
        print(
            f"    m={m:2d}: SD={res['sd']} = {res['sd_float']:.6f}, "
            f"1-SD={res['one_minus_sd_float']:.6e} ({res['time_sec']:.2f}s, "
            f"leaves={res['leaves']}, nodes={res['nodes']})"
        )
        if elapsed > 290:
            wall.append(m)

    n2_vals = _load_n2_values()
    cross_n = _cross_n_comparison(n2_vals, results)
    print("\n(O3) Cross-n 1-SD comparison at matched m/n ratios")
    for row in cross_n:
        print(
            f"  ratio={row['ratio']}: n=2,m={row['n2_m']} 1-SD="
            f"{float(Fraction(row['n2_one_minus_sd'])):.6e}; "
            f"n=3,m={row['n3_m']} 1-SD={float(Fraction(row['n3_one_minus_sd'])):.6e}"
        )

    summary = {
        "experiment": 300,
        "track": "O",
        "anchors": anchors,
        "results": results,
        "cross_n_comparison": cross_n,
        "wall_report": {
            "per_m_timeout_sec": 290,
            "hit_wall_at_ms": wall,
            "status": "clean" if not wall else "partial",
        },
        "claim_labels": {
            "sufficient_statistic_reduction_n3": "THEOREM (proved; verified by direct enumeration for m<=12)",
            "gl3_f2_orbit_canonicalisation": "THEOREM (recursive colour-class orbit enumeration; stabiliser gives exact orbit size 168/|Stab|)",
            "s00_pure_shift_vectorisation": "THEOREM (closed-form s_00-sum via sign threshold; denominator divisibility proved)",
            "n3_exact_sd_m_16": "EVIDENCE (exact finite computation)" if 16 not in wall else "WALL (not completed)",
            "n3_exact_sd_m_20": "EVIDENCE (exact finite computation)" if 20 not in wall else "WALL (not completed)",
            "n3_exact_sd_m_24": "EVIDENCE (exact finite computation)" if 24 not in wall else "WALL (not completed)",
            "cross_n_rate": "EVIDENCE (first matched-ratio 1-SD comparison across n=2,3)",
            "lem_m2_status": "OPEN",
        },
        "interpretation_guards": {
            "axis": "m grows at fixed n=3 (the correct m-axis)",
            "comparison_distribution": "LPN_{p_eff(3)}, matched rate; never transformed",
            "p_eff_caveat": "p_eff(3)=3367/8192 ~ 0.4109 is close to 1/2; SD measures correlation inside a vacuous LPN regime",
            "practical_attack": "SD numbers do not imply a practical distinguisher",
            "L1_exact_arithmetic": "integer counts over common denominator q_den*N*(2N)^m*D^m; q_graph(3) odd factor 9 preserved",
            "L2_duality_care": "standard F_2 pairing only; no symplectic dual",
            "L3_query_class_hygiene": "SQ statements, if any, name the query class explicitly; no unrestricted Feldman theorem",
            "L4_comparison_distribution": "LPN target is the matched-rate product distribution, never post-processed",
        },
    }

    out_path = out_dir / "300-trackO-n3-reduced-SD.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
