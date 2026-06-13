#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""205: Track L — independent verification of the two reductions.

Checks:
  (V1) S_3 orbit counting: the canonical loop of experiments/204 visits each
       unordered orbit of non-zero type slots exactly once, and the orbit-size
       factor recovers the full ordered state count.
  (V2) S_3 invariance: for small m, summing over canonical states with the
       orbit factor equals the direct ordered T-level sum.
  (V3) s_00 pure-shift formula: for random residual states the closed-form
       s_00-sum (sign threshold) agrees with brute-force summation.
  (V4) Anchor check: the reduced code reproduces the corrected Track F values
       at m = 24, 32, 48.
"""
import argparse
import json
import random
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


def exact_sd_direct_n2(m: int) -> Fraction:
    """Direct T-level SD (no reductions), for small m only."""
    n = 2
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

    B0 = [[0] * (mm + 1) for mm in range(m + 1)]
    for mm in range(m + 1):
        for s in range(mm + 1):
            B0[mm][s] = comb(mm, s) * pow_a[s] * pow_b[mm - s]

    def dot(w: int, tau: int) -> int:
        return (w & tau).bit_count() & 1

    sd_num = 0
    for m0 in range(m + 1):
        for m1 in range(m + 1 - m0):
            for m2 in range(m + 1 - m0 - m1):
                m3 = m - m0 - m1 - m2
                ms = (m0, m1, m2, m3)
                mult_comp = fact[m] // (fact[m0] * fact[m1] * fact[m2] * fact[m3])
                U = [B0[mm] for mm in ms]
                for s0 in range(m0 + 1):
                    u0 = U[0][s0]
                    for s1 in range(m1 + 1):
                        u1 = U[1][s1]
                        v1 = U[1][m1 - s1]
                        for s2 in range(m2 + 1):
                            u2 = U[2][s2]
                            v2 = U[2][m2 - s2]
                            for s3 in range(m3 + 1):
                                s = (s0, s1, s2, s3)
                                match_w = 0
                                for w in range(N):
                                    ok = True
                                    for tau in range(N):
                                        target = ms[tau] if dot(w, tau) else 0
                                        if s[tau] != target:
                                            ok = False
                                            break
                                    if ok:
                                        match_w += 1
                                n_graph = match_w * mult_comp
                                n_full = (
                                    mult_comp
                                    * comb(m0, s0)
                                    * comb(m1, s1)
                                    * comb(m2, s2)
                                    * comb(m3, s3)
                                )
                                n_out = factor_graph * n_graph + factor_full * n_full
                                u3 = U[3][s3]
                                v3 = U[3][m3 - s3]
                                n_x0 = u0 * u1 * u2 * u3
                                n_x1 = u0 * v1 * u2 * v3
                                n_x2 = u0 * u1 * v2 * v3
                                n_x3 = u0 * v1 * v2 * u3
                                n_lpn = factor_lpn * mult_comp * (n_x0 + n_x1 + n_x2 + n_x3)
                                sd_num += abs(n_out - n_lpn)
    return Fraction(sd_num, 2 * D_common)


def canonical_state_count(m: int) -> dict:
    """Count canonical states and weighted orbit count."""
    canonical = 0
    weighted = 0
    for m1 in range(m + 1):
        for m2 in range(m1 + 1):
            for m3 in range(m2 + 1):
                M = m1 + m2 + m3
                if M > m:
                    break
                eq12 = m1 == m2
                eq23 = m2 == m3
                for s1 in range(m1 + 1):
                    s2_min = s1 if eq12 else 0
                    for s2 in range(s2_min, m2 + 1):
                        s3_min = s2 if eq23 else 0
                        for s3 in range(s3_min, m3 + 1):
                            m0 = m - M
                            canonical += 1
                            if m1 == m2 == m3 and s1 == s2 == s3:
                                mult = 1
                            elif (
                                (m1 == m2 and s1 == s2)
                                or (m2 == m3 and s2 == s3)
                                or (m1 == m3 and s1 == s3)
                            ):
                                mult = 3
                            else:
                                mult = 6
                            weighted += mult
    # The s_00 coordinate is vectorised away, so the weighted canonical count
    # should equal the number of ordered triples (m_1,m_2,m_3,s_1,s_2,s_3)
    # with m_i >= s_i >= 0 and m_1+m_2+m_3 <= m, i.e. C(m+6, 6).
    return {"canonical_states": canonical, "weighted_orbit_count": weighted, "expected_ordered_states": comb(m + 6, 6)}


def verify_s3_orbit_counting(max_m: int = 12) -> list[dict]:
    checks = []
    for m in range(1, max_m + 1):
        cnt = canonical_state_count(m)
        ok = cnt["weighted_orbit_count"] == cnt["expected_ordered_states"]
        checks.append({"m": m, **cnt, "match": ok})
    return checks


def verify_s3_independence(max_m: int = 6) -> list[dict]:
    """Compare reduced SD with the orbit factor to direct ordered enumeration."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "trackL204", "experiments/204-KIMI-trackL-sufficient-statistic-m64.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    checks = []
    for m in range(2, max_m + 1):
        direct = exact_sd_direct_n2(m)
        reduced = Fraction(mod.exact_sd_reduced_n2(m)["sd"])
        checks.append(
            {
                "m": m,
                "direct": str(direct),
                "reduced": str(reduced),
                "match": direct == reduced,
            }
        )
    return checks


def verify_s00_pure_shift(trials: int = 200, seed: int = 0) -> list[dict]:
    """Check the closed-form s_00-sum against brute force on random residuals."""
    n = 2
    p = p_eff(n)
    a = p.numerator
    D = p.denominator
    b = D - a
    rng = random.Random(seed)

    # Precompute binomials and weights up to a generous bound.
    max_m0 = 30
    C = [[comb(mm, s) for s in range(mm + 1)] for mm in range(max_m0 + 1)]
    pow_a = [1] * (max_m0 + 1)
    pow_b = [1] * (max_m0 + 1)
    for i in range(1, max_m0 + 1):
        pow_a[i] = pow_a[i - 1] * a
        pow_b[i] = pow_b[i - 1] * b

    checks = []
    for _ in range(trials):
        m0 = rng.randrange(0, max_m0 + 1)
        A = rng.randrange(0, 10 ** 30)
        K = rng.randrange(1, 10 ** 30)
        G = rng.randrange(0, 10 ** 30)
        brute = abs(G + A - K * pow_b[m0]) + sum(
            C[m0][s] * abs(A - K * pow_a[s] * pow_b[m0 - s]) for s in range(1, m0 + 1)
        )
        # Reproduce the threshold formula from experiments/204.
        rc = [pow_a[s] * pow_b[m0 - s] for s in range(m0 + 1)]
        lo, hi = 0, m0 + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if K * rc[mid] <= A:
                hi = mid
            else:
                lo = mid + 1
        t = lo
        pc = [sum(C[m0][: k + 1]) for k in range(m0 + 1)]
        pw = [sum(C[m0][s] * rc[s] for s in range(k + 1)) for k in range(m0 + 1)]
        pre_c = pc[t - 1] if 0 < t <= m0 else (pc[m0] if t > m0 else 0)
        pre_w = pw[t - 1] if 0 < t <= m0 else (pw[m0] if t > m0 else 0)
        totC = 1 << m0
        totW = D ** m0
        S_abs_total = A * (totC - 2 * pre_c) + K * (2 * pre_w - totW)
        B0 = A - K * rc[0]
        formula = S_abs_total - abs(B0) + abs(B0 + G)
        checks.append({"m0": m0, "match": brute == formula})
    return checks


def verify_anchors() -> list[dict]:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "trackL204", "experiments/204-KIMI-trackL-sufficient-statistic-m64.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    ANCHORS = {
        24: "16832756036765379095034202127924274618943844971887062499211392003318774009896365/29642774844752946028434172162224104410437116074403984394101141506025761187823616",
        32: "175842639268182236234225149971230384237897459955496283666363584364067225210764143038987088768788053693215/286687326998758938951352611912760867599570623646035140467198604923365359511060601008752319138765710819328",
        48: "607477461132137352864009669432561278876547085540963876824000902259324180705585729760268074621527447131000809903636388269236874471512931193096020288141170484925/878694100496718043517683302282418331810487718418343092402491322775749527474899974671687634004666183037093927858109549828751614463963730408009475621262727315456",
    }
    checks = []
    for m, val in ANCHORS.items():
        reduced = Fraction(mod.exact_sd_reduced_n2(m)["sd"])
        checks.append({"m": m, "anchor": val, "reduced": str(reduced), "match": reduced == Fraction(val)})
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=str,
        default="experiments/output",
        help="directory for JSON outputs",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    print("== Track L reduction verification ==")

    print("\n(V1) S_3 orbit counting")
    v1 = verify_s3_orbit_counting(12)
    for c in v1:
        print(
            f"  m={c['m']:2d}: canonical={c['canonical_states']}, "
            f"weighted={c['weighted_orbit_count']}, expected={c['expected_ordered_states']} "
            f"[{'OK' if c['match'] else 'FAIL'}]"
        )
    if not all(c["match"] for c in v1):
        raise RuntimeError("S_3 orbit counting failed")

    print("\n(V2) S_3 invariance vs direct T-level enumeration")
    v2 = verify_s3_independence(6)
    for c in v2:
        print(f"  m={c['m']}: direct={c['direct']} reduced={c['reduced']} [{'OK' if c['match'] else 'FAIL'}]")
    if not all(c["match"] for c in v2):
        raise RuntimeError("S_3 independence check failed")

    print("\n(V3) s_00 pure-shift closed form vs brute force")
    v3 = verify_s00_pure_shift(200)
    ok3 = all(c["match"] for c in v3)
    print(f"  200 random residual states: {'ALL OK' if ok3 else 'FAIL'}")
    if not ok3:
        raise RuntimeError("s_00 pure-shift check failed")

    print("\n(V4) Anchor check against corrected Track F values")
    v4 = verify_anchors()
    for c in v4:
        print(f"  m={c['m']}: {'OK' if c['match'] else 'FAIL'}")
    if not all(c["match"] for c in v4):
        raise RuntimeError("anchor check failed")

    summary = {
        "experiment": 205,
        "track": "L",
        "checks": {
            "s3_orbit_counting": v1,
            "s3_invariance": v2,
            "s00_pure_shift": {"trials": 200, "all_ok": ok3},
            "anchors": v4,
        },
        "claim_labels": {
            "s3_orbit_counting": "THEOREM (verified computationally for m<=12)",
            "s3_invariance": "THEOREM (verified against direct enumeration for m<=6)",
            "s00_pure_shift": "THEOREM (verified numerically on random residuals)",
            "anchor_m_24_32_48": "EVIDENCE (exact fraction match)",
        },
        "interpretation_guards": {
            "L1_exact_arithmetic": "all cross-checks use integer arithmetic; Fractions stored as strings",
            "L2_duality_care": "standard F_2 pairing only",
            "L3_query_class_hygiene": "no Feldman theorem used",
            "L4_comparison_distribution": "LPN target is the matched-rate product distribution",
        },
        "time_sec": time.time() - t0,
    }

    out_path = out_dir / "205-trackL-reduction-verification.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
