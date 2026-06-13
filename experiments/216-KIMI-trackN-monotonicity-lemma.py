#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""216: Track N — monotonicity lemma for matched-rate SD in m (fixed n).

Task N1. Formalize and prove the monotonicity lemma.

    At fixed n, let P_out^{(m)} be the distribution of the reduction output
    (C,y) = (B A, B(Ax+e)) with B ~ Unif(F_2^{m x 2n}) drawn fresh per A,
    and let P_lpn^{(m)} be the matched-rate LPN_{p_eff(n)} distribution over
    F_2^{m x n} x F_2^m.  Let Pi_m be the deterministic channel that drops the
    last row of (C,y).

    Projection lemma.  Because the rows of B are i.i.d. and depend only on the
    shared (A,x,e), the first-m-rows marginal of P_out^{(m+1)} equals
    P_out^{(m)}.  Because the LPN samples are i.i.d. rows with secret x and
    per-coordinate noise p_eff(n), Pi_m(P_lpn^{(m+1)}) = P_lpn^{(m)}.

    Monotonicity theorem.  Data processing for statistical distance gives
        SD(Pi_m(P), Pi_m(Q)) <= SD(P, Q)
    for any channel Pi_m.  Applying it to P=P_out^{(m+1)}, Q=P_lpn^{(m+1)}
    yields
        SD(m) := SD(P_out^{(m)}, P_lpn^{(m)}) <= SD(P_out^{(m+1)}, P_lpn^{(m+1)}) = SD(m+1).

Task N2. Cross-check the inequality against exact SD tables.
    * n=2: values from experiments/202 (sufficient-statistic reduction) are
      loaded for m<=48; the script optionally extends to m=64 using the same
      exact method.  (m=80 is left to Track L because the straightforward
      enumeration is the same wall Track L is engineered to push.)
    * n=3: values from experiments/200 cover m<=6; this script computes the
      remaining m=7..12 with a general n sufficient-statistic reduction.

Task N3. Corollaries.
    * Bounded monotone => lim_{m->inf} SD(m) exists (THEOREM).
    * The entropy heuristic (correlated noise has <= 2n+n bits of structure)
      suggests the limit is 1 at fixed n; this is labelled EVIDENCE/OPEN until
      proved.

Standing guards:
  L1 exact arithmetic: all probabilities are Fractions; JSON stores string
    fractions.  The sufficient-statistic reduction uses a single integer common
    denominator q_den * N * (2N)^m * D^m.
  L2 J-twist duality: the row-type inner product is the standard F_2 pairing
    <w,tau>; no dual-space twist is introduced.
  L3 query-class hygiene: conclusions are about statistical distance only; no
    unrestricted Feldman/SQ inference is made.
  L4 never transform the comparison distribution: the projection channel Pi_m
    is applied to BOTH P_out^{(m+1)} and P_lpn^{(m+1)}; the comparison
    distribution is never bijected alone.

PRE-REGISTER interpretation guards:
  * Comparison distribution: matched-rate LPN_{p_eff(n)} with
      p_eff(n) = (1 - (3/4)^{2n}) / 2.
  * Scaling axis: m grows at fixed n; no fixed-small-m conclusion.
  * The LPN target becomes vacuous (p_eff -> 1/2) as n grows; SD numbers
    measure detectability of correlation inside a noise-1/2 LPN regime and do
    not imply a practical distinguisher for standard LPN.
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases_n,
    exact_sd_counts,
    lpn_target_counts_n,
    randomized_uniform_B_counts_n,
)


def p_eff(n: int) -> Fraction:
    """Matched LPN noise rate p_eff(n) = (1 - (3/4)^{2n}) / 2."""
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    """Pr[Ax + e in span(A)] for uniform Lagrangian A, x, e ~ Bernoulli(1/4)^{2n}."""
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def _dot(w: int, tau: int) -> int:
    """Parity of bitwise AND (standard F_2 pairing)."""
    return (w & tau).bit_count() & 1


def _exact_sd_sufficient_statistic_general(n: int, m: int) -> dict:
    """General n sufficient-statistic exact SD (used for n>=3)."""
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

    B_same = [[0] * (mm + 1) for mm in range(m + 1)]
    B_flip = [[0] * (mm + 1) for mm in range(m + 1)]
    for mm in range(m + 1):
        for s in range(mm + 1):
            c = comb(mm, s)
            B_same[mm][s] = c * pow_a[s] * pow_b[mm - s]
            B_flip[mm][s] = c * pow_a[mm - s] * pow_b[s]

    types = list(range(N))
    dot = [[_dot(w, tau) for tau in types] for w in types]

    ms = [0] * N
    ss = [0] * N

    t0 = time.time()
    sd_num = 0

    # Enumerate compositions recursively; keep a mutable cell for the
    # multinomial coefficient because Python nonlocal cannot see into siblings.
    state = {"mult_comp": 0}

    def rec_type(idx: int, rem: int):
        if idx == N - 1:
            ms[idx] = rem
            _process_composition()
            return
        for k in range(rem + 1):
            ms[idx] = k
            rec_type(idx + 1, rem - k)

    def _process_composition():
        denom = 1
        for mm in ms:
            denom *= fact[mm]
        state["mult_comp"] = fact[m] // denom
        rec_s(0)

    def rec_s(idx: int):
        if idx == N - 1:
            for k in range(ms[idx] + 1):
                ss[idx] = k
                _process_tuple()
            return
        for k in range(ms[idx] + 1):
            ss[idx] = k
            rec_s(idx + 1)

    def _process_tuple():
        nonlocal sd_num
        mult_comp = state["mult_comp"]

        match_w = 0
        for w in range(N):
            ok = True
            for tau in types:
                if ms[tau] == 0:
                    continue
                target = ms[tau] if dot[w][tau] else 0
                if ss[tau] != target:
                    ok = False
                    break
            if ok:
                match_w += 1

        n_graph = match_w * mult_comp

        n_full = mult_comp
        for tau in types:
            n_full *= comb(ms[tau], ss[tau])

        n_out = factor_graph * n_graph + factor_full * n_full

        lpn_sum = 0
        for x in range(N):
            prod = 1
            for tau in types:
                if dot[x][tau]:
                    prod *= B_flip[ms[tau]][ss[tau]]
                else:
                    prod *= B_same[ms[tau]][ss[tau]]
            lpn_sum += prod
        n_lpn = factor_lpn * mult_comp * lpn_sum

        sd_num += abs(n_out - n_lpn)

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


def _exact_sd_sufficient_statistic_n2(m: int) -> dict:
    """Specialised fast path for n=2 (four row types, unrolled loops)."""
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

    # Types 0..3; inner products with the four possible w are:
    #   w=0: [0,0,0,0]; w=1: [0,1,0,1]; w=2: [0,0,1,1]; w=3: [0,1,1,0]
    # Hard-code the four membership targets for speed.
    def dot(w: int, tau: int) -> int:
        return (w & tau).bit_count() & 1

    t0 = time.time()
    sd_num = 0

    for m0 in range(m + 1):
        for m1 in range(m - m0 + 1):
            for m2 in range(m - m0 - m1 + 1):
                m3 = m - m0 - m1 - m2
                ms = (m0, m1, m2, m3)
                mult_comp = fact[m] // (fact[m0] * fact[m1] * fact[m2] * fact[m3])
                U0 = B0[m0]
                U1 = B0[m1]
                U2 = B0[m2]
                U3 = B0[m3]

                for s0 in range(m0 + 1):
                    u0 = U0[s0]
                    v0 = U0[m0 - s0]
                    for s1 in range(m1 + 1):
                        u1 = U1[s1]
                        v1 = U1[m1 - s1]
                        for s2 in range(m2 + 1):
                            u2 = U2[s2]
                            v2 = U2[m2 - s2]
                            for s3 in range(m3 + 1):
                                ss = (s0, s1, s2, s3)
                                u3 = U3[s3]
                                v3 = U3[m3 - s3]

                                match_w = 0
                                for w in range(N):
                                    ok = True
                                    for tau in (0, 1, 2, 3):
                                        if ms[tau] == 0:
                                            continue
                                        target = ms[tau] if dot(w, tau) else 0
                                        if ss[tau] != target:
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

                                # LPN sum over x in F_2^2.
                                n_x0 = u0 * u1 * u2 * u3
                                n_x1 = u0 * v1 * u2 * v3
                                n_x2 = u0 * u1 * v2 * v3
                                n_x3 = u0 * v1 * v2 * u3
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


def exact_sd_sufficient_statistic(n: int, m: int) -> dict:
    """Exact SD(P_out, LPN_{p_eff}) at fixed n,m by row-type statistics."""
    if n == 2:
        return _exact_sd_sufficient_statistic_n2(m)
    return _exact_sd_sufficient_statistic_general(n, m)


def cross_check_against_direct(n: int, max_m: int) -> list[dict]:
    """Self-check: sufficient-statistic SD equals direct enumeration for small m."""
    p = p_eff(n)
    bases = list(enumerate_lagrangian_bases_n(n))
    checks = []
    for m in range(max(2, n), max_m + 1):
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


def load_existing_values(path: Path) -> dict:
    """Load a JSON output and return {(n,m): sd_string}."""
    if not path.exists():
        return {}
    with open(path) as f:
        data = json.load(f)
    out = {}
    for r in data.get("results", []):
        out[(r["n"], r["m"])] = r["sd"]
    for r in data.get("task_A2_sweep", []):
        out[(r["n"], r["m"])] = r["sd"]
    return out


def check_monotone(table: list[dict]) -> dict:
    """Return monotonicity check over a sorted list of {n,m,sd}."""
    by_n = {}
    for r in table:
        by_n.setdefault(r["n"], []).append(r)
    result = {}
    for n, rows in by_n.items():
        rows.sort(key=lambda r: r["m"])
        sds = [Fraction(r["sd"]) for r in rows]
        ms = [r["m"] for r in rows]
        violations = []
        for i in range(len(sds) - 1):
            if not (sds[i] <= sds[i + 1]):
                violations.append((ms[i], ms[i + 1], str(sds[i]), str(sds[i + 1])))
        strict = all(sds[i] < sds[i + 1] for i in range(len(sds) - 1))
        result[n] = {
            "m_range": (ms[0], ms[-1]),
            "num_points": len(rows),
            "monotone": len(violations) == 0,
            "strict": strict,
            "violations": violations,
            "first_sd": str(sds[0]),
            "last_sd": str(sds[-1]),
        }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n2-ms",
        type=int,
        nargs="+",
        default=[2, 3, 4, 5, 6, 7, 8, 12, 16, 24, 32, 48, 64],
        help="n=2 values of m to compute/verify",
    )
    parser.add_argument(
        "--n3-ms",
        type=int,
        nargs="+",
        default=list(range(2, 13)),
        help="n=3 values of m to compute/verify",
    )
    parser.add_argument(
        "--cross-check-n",
        type=int,
        nargs="+",
        default=[2, 3],
        help="values of n for direct-vs-sufficient-statistic self-check",
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
    parser.add_argument(
        "--output-name",
        type=str,
        default="216-trackN-monotonicity-lemma.json",
        help="filename for the JSON summary",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- N1/self-check: sufficient-statistic matches direct enumeration ------
    self_checks = {}
    for n in args.cross_check_n:
        print(f"== Self-check n={n}: sufficient-statistic vs direct enumeration ==")
        checks = cross_check_against_direct(n, args.cross_check_max_m)
        for c in checks:
            status = "OK" if c["match"] else "MISMATCH"
            print(f"  m={c['m']}: direct={c['sd_direct']} ss={c['sd_sufficient_statistic']} [{status}]")
        if not all(c["match"] for c in checks):
            raise RuntimeError(f"sufficient-statistic self-check failed for n={n}")
        self_checks[n] = checks

    # --- N2: build exact table -----------------------------------------------
    existing = {}
    existing.update(load_existing_values(Path("experiments/output/202-trackF-sufficient-statistic-n2.json")))
    existing.update(load_existing_values(Path("experiments/output/200-trackA-summary.json")))

    table = []
    for n, ms in ((2, args.n2_ms), (3, args.n3_ms)):
        print(f"\n== Exact SD table for n={n} ==")
        for m in ms:
            if (n, m) in existing:
                sd_str = existing[(n, m)]
                print(f"  m={m:2d}: loaded SD={sd_str} = {float(Fraction(sd_str)):.6f}")
                table.append({"n": n, "m": m, "sd": sd_str, "source": "existing"})
            else:
                print(f"  m={m:2d}: computing ...", flush=True)
                res = exact_sd_sufficient_statistic(n, m)
                print(
                    f"    SD={res['sd']} = {res['sd_float']:.6f}, "
                    f"1-SD={res['one_minus_sd_float']:.6e} ({res['time_sec']:.2f}s)"
                )
                table.append({"n": n, "m": m, "sd": res["sd"], "source": "computed"})

    # --- N2: monotonicity check ----------------------------------------------
    mono = check_monotone(table)
    print("\n== Monotonicity cross-check ==")
    for n, info in mono.items():
        print(
            f"  n={n}: m={info['m_range'][0]}..{info['m_range'][1]} "
            f"({info['num_points']} points): monotone={info['monotone']}, strict={info['strict']}"
        )
        if info["violations"]:
            print("    VIOLATIONS:", info["violations"])
    if not all(info["monotone"] for info in mono.values()):
        raise RuntimeError("monotonicity check failed on exact table")

    # --- N3: limit corollary -------------------------------------------------
    limit_evidence = {}
    for n in (2, 3):
        rows = [r for r in table if r["n"] == n]
        rows.sort(key=lambda r: r["m"])
        if len(rows) >= 2:
            last = rows[-1]
            prev = rows[-2]
            limit_evidence[n] = {
                "m_last": last["m"],
                "m_prev": prev["m"],
                "sd_last": last["sd"],
                "one_minus_sd_last": str(1 - Fraction(last["sd"])),
                "sd_prev": prev["sd"],
                "one_minus_sd_prev": str(1 - Fraction(prev["sd"])),
            }

    summary = {
        "experiment": 216,
        "track": "N",
        "self_checks": self_checks,
        "exact_table": table,
        "monotonicity_check": mono,
        "limit_corollary": {
            "existence": "THEOREM (bounded monotone sequence of real numbers has a limit)",
            "limit_value_claim": "EVIDENCE/OPEN (entropy heuristic suggests 1; not proved)",
            "limit_evidence": limit_evidence,
        },
        "claim_labels": {
            "projection_lemma": "THEOREM (row-i.i.d. coupling; proved in script header and meta note)",
            "monotonicity_theorem": "THEOREM (data processing under row-dropping channel)",
            "monotone_exact_table": "EVIDENCE (exact finite computation; strictness observed but not proven in general)",
            "limit_exists": "THEOREM",
            "limit_equals_one": "EVIDENCE / OPEN",
            "lem_m2_status": "OPEN",
        },
        "standing_guards": {
            "L1_exact_arithmetic": "Fractions and integer common denominator q_den*N*(2N)^m*D^m",
            "L2_J_twist_duality": "standard F_2 pairing; no dual-space twist",
            "L3_query_class_hygiene": "statistical-distance claims only; no Feldman inference",
            "L4_comparison_distribution": "projection channel applied to both P_out and P_lpn; no one-sided bijection",
        },
        "interpretation_guards": {
            "comparison_distribution": "LPN_{p_eff(n)}, matched rate",
            "scaling_axis": "m grows at fixed n",
            "p_eff_limit": "p_eff(n) -> 1/2 as n grows; SD measures correlation inside a vacuous LPN regime",
        },
    }
    out_path = out_dir / args.output_name
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
