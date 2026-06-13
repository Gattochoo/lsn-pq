#!/usr/bin/env python3
"""500: Track W — rigorous m→∞ limit theorem for uniform-B-per-A.

W-a. Full-component separation.  For fixed n, let P_full^{(m)} be uniform on
F_2^{m(n+1)} and P_lpn^{(m)} the matched LPN distribution.  We prove
    SD(P_full^{(m)}, P_lpn^{(m)}) ≥ 1 - ρ(n)^m,
where ρ(n) is the per-row Bhattacharyya/Hellinger affinity
    ρ(n) = 1 - H^2(P_full^{(1)}, P_lpn^{(1)})
         = 1 - (1/2^n)[1 - sqrt((1-p_eff(n))/2) - sqrt(p_eff(n)/2)] < 1.
The proof uses Hellinger tensorization and the inequality SD ≥ H^2.

W-b. Graph-component separation.  Under P_lpn^{(m)} the event
S = {y ∈ col(C)} has mass at most 2^n (1-p_eff(n))^m → 0.

W-c. Mixture combination.  P_out^{(m)} = q(n)·P_graph + (1-q(n))·P_full.
Using the disjoint-union test S ∪ E' (E' the full-component test restricted to
S^c), we obtain the explicit rate
    1 - SD(P_out^{(m)}, P_lpn^{(m)})
      ≤ (2-q(n)) ρ(n)^m + (1-q(n)) 2^{n-m} + 2^n (1-p_eff(n))^m.
For fixed n the RHS is O(ρ(n)^m) because ρ(n) > max(1-p_eff(n), 1/2).

Cross-checks:
  * Exact full-component SD at n=2 (m≤80) vs W-a bound.
  * Exact SD(P_out,P_lpn) at n=2 (m≤80, Track S table) vs W-c bound.

Scope: uniform-B-per-A only.  General randomized marginal-adaptive B remains OPEN.

PRE-REGISTER interpretation guards:
  * Strategy scope: uniform-B-per-A (one explicit reduction strategy), not all
    marginal-adaptive B.
  * Axis: m grows at fixed n (the correct m-axis).
  * Comparison distribution: LPN_{p_eff(n)} (matched rate), never transformed.
  * The SD numbers measure statistical distance between two explicit
    distributions; they do not by themselves imply a practical attack.

Standing guards:
  L1 exact arithmetic: p_eff, q_graph, and exact SD values are Fractions; the
      theorem constants are explicit rational combinations plus square roots
      of rational numbers (stored as exact formulas and high-precision decimals).
  L2 J-twist duality: the per-row channel uses the standard F_2 pairing only.
  L3 query-class hygiene: no unrestricted Feldman/SQ theorem is invoked.
  L4 comparison-distribution care: the LPN target is the matched-rate product
      distribution, never post-processed.
"""
import argparse
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

getcontext().prec = 120


def p_eff(n: int) -> Fraction:
    """Matched LPN noise rate p_eff(n) = (1 - (3/4)^{2n}) / 2."""
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    """Pr[Ax + e in span(A)] for uniform Lagrangian A, x, e ~ Bernoulli(1/4)^{2n}."""
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def rho_hellinger(n: int) -> Decimal:
    """Per-row Hellinger-based rate ρ(n) = 1 - H^2(P_full^{(1)}, P_lpn^{(1)}).

    H^2 = (1/2^n)[1 - sqrt((1-p_eff)/2) - sqrt(p_eff/2)].
    """
    pe = p_eff(n)
    pe_dec = Decimal(pe.numerator) / Decimal(pe.denominator)
    one_m_pe_dec = Decimal(1) - pe_dec
    beta = Decimal(1) - (one_m_pe_dec / Decimal(2)).sqrt() - (pe_dec / Decimal(2)).sqrt()
    h2 = beta / Decimal(2 ** n)
    return Decimal(1) - h2


def rho_hellinger_formula(n: int) -> str:
    """Exact symbolic expression for ρ(n)."""
    pe = p_eff(n)
    return (
        f"1 - (1/{2**n}) * [1 - sqrt((1 - {pe})/2) - sqrt(({pe})/2)]"
    )


def exact_full_component_sd(m: int, n: int) -> Fraction:
    """Exact SD(P_full^{(m)}, P_lpn^{(m)}) for fixed n.

    Conditioning on the m public row-vectors, only rows with c=0 distinguish.
    If K ~ Bin(m, 1/2^n) is the number of zero rows, then
        SD = E_K[ SD(Bernoulli(p_eff)^K, Uniform^K) ].
    """
    pe = p_eff(n)
    tot = Fraction(0)
    for k in range(m + 1):
        wk = Fraction(comb(m, k), 2 ** (n * m)) * (2 ** n - 1) ** (m - k)
        s = Fraction(0)
        for j in range(k + 1):
            pj = pe ** j * (Fraction(1) - pe) ** (k - j)
            s += abs(pj - Fraction(1, 2 ** k)) * comb(k, j)
        tot += wk * s / 2
    return tot


def graph_membership_bound(m: int, n: int) -> Fraction:
    """Upper bound on Pr_{P_lpn}[y ∈ col(C)].

    For any fixed C, |col(C)| ≤ 2^n.  The largest point mass of e ~ Bern(p_eff)^m
    is (1-p_eff)^m (attained at e=0), so Pr[e ∈ col(C)] ≤ 2^n (1-p_eff)^m.
    Since y = Cx + e and Cx ∈ col(C), y ∈ col(C) iff e ∈ col(C).
    """
    return Fraction(2 ** n) * (Fraction(1) - p_eff(n)) ** m


def combination_bound(m: int, n: int) -> Decimal:
    """Explicit W-c upper bound on 1 - SD(P_out^{(m)}, P_lpn^{(m)}).

    1 - SD ≤ (2-q) ρ^m + (1-q) 2^{n-m} + 2^n (1-p_eff)^m.
    """
    q = q_graph(n)
    rho = rho_hellinger(n)
    one_m_pe = Fraction(1) - p_eff(n)
    q_dec = Decimal(q.numerator) / Decimal(q.denominator)
    term1 = (Decimal(2) - q_dec) * (rho ** m)
    term2 = (Decimal(1) - q_dec) * (Decimal(2) ** n) / (Decimal(2) ** m)
    term3 = Decimal(2 ** n) * (Decimal(one_m_pe.numerator) / Decimal(one_m_pe.denominator)) ** m
    return term1 + term2 + term3


def load_track_s_results(path: Path) -> list[dict]:
    with open(path) as f:
        data = json.load(f)
    return data["results"]


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

    print("=" * 78)
    print("500-Track W — rigorous m→∞ limit theorem for uniform-B-per-A")
    print("=" * 78)

    # --- Theorem constants ---------------------------------------------------
    print("\n(0) Explicit theorem constants")
    constants = {}
    for n in (2, 3, 4):
        pe = p_eff(n)
        q = q_graph(n)
        rho = rho_hellinger(n)
        constants[n] = {
            "p_eff": str(pe),
            "q_graph": str(q),
            "rho_formula": rho_hellinger_formula(n),
            "rho_decimal": str(rho),
            "rho_float": float(rho),
            "one_minus_p_eff": str(Fraction(1) - pe),
        }
        print(
            f"  n={n}: p_eff={pe} ({float(pe):.6f}), q_graph={q} ({float(q):.6f}), "
            f"ρ={float(rho):.10f}"
        )

    # --- W-a verification: full-component SD ---------------------------------
    print("\n(1) W-a: full-component SD lower bound vs exact values (n=2)")
    wa_checks = []
    for m in (1, 2, 4, 8, 16, 32, 64, 80):
        exact_sd = exact_full_component_sd(m, n=2)
        one_minus_exact = Fraction(1) - exact_sd
        bound_one_minus = rho_hellinger(2) ** m
        valid = bound_one_minus >= Decimal(one_minus_exact.numerator) / Decimal(one_minus_exact.denominator)
        wa_checks.append({
            "m": m,
            "exact_sd": str(exact_sd),
            "one_minus_exact": str(one_minus_exact),
            "bound_one_minus": str(bound_one_minus),
            "valid": valid,
        })
        print(
            f"  m={m:2d}: exact SD={float(exact_sd):.6f}, "
            f"1-SD={float(one_minus_exact):.6f}, bound 1-SD={float(bound_one_minus):.6f} "
            f"[{'OK' if valid else 'FAIL'}]"
        )
    assert all(c["valid"] for c in wa_checks), "W-a bound failed"

    # --- W-b verification: graph membership bound ----------------------------
    print("\n(2) W-b: Pr_{P_lpn}[y ∈ col(C)] upper bound (n=2)")
    wb_checks = []
    for m in (8, 16, 32, 64, 80):
        bound = graph_membership_bound(m, n=2)
        wb_checks.append({
            "m": m,
            "bound": str(bound),
            "bound_float": float(bound),
        })
        print(f"  m={m:2d}: Pr[y∈col(C)] ≤ {float(bound):.6e}")

    # --- W-c verification: combination bound vs exact SD(P_out,P_lpn) --------
    print("\n(3) W-c: mixture-combination bound vs exact SD(P_out,P_lpn) (n=2)")
    track_s_path = Path("experiments/output/400-trackS-optimal-LR-and-named-tests.json")
    if not track_s_path.exists():
        raise FileNotFoundError(f"Track S output not found: {track_s_path}")
    track_s_results = load_track_s_results(track_s_path)

    wc_checks = []
    for res in track_s_results:
        m = res["m"]
        exact_sd = Fraction(res["sd"])
        one_minus_exact = Fraction(1) - exact_sd
        bound = combination_bound(m, n=2)
        valid = bound >= Decimal(one_minus_exact.numerator) / Decimal(one_minus_exact.denominator)
        wc_checks.append({
            "m": m,
            "exact_sd": str(exact_sd),
            "one_minus_exact": str(one_minus_exact),
            "combination_bound": str(bound),
            "valid": valid,
        })
        print(
            f"  m={m:2d}: exact SD={float(exact_sd):.6f}, "
            f"1-SD={float(one_minus_exact):.6f}, bound 1-SD={float(bound):.6f} "
            f"[{'OK' if valid else 'FAIL'}]"
        )
    assert all(c["valid"] for c in wc_checks), "W-c bound failed"

    # --- Asymptotic threshold -------------------------------------------------
    n = 2
    rho = rho_hellinger(n)
    q = Decimal(q_graph(n).numerator) / Decimal(q_graph(n).denominator)
    # Conservative single-ρ form: C ρ^m with C = (2-q) + 2^n.
    C_single = (Decimal(2) - q) + Decimal(2 ** n)
    # Smallest m with C_single ρ^m < 1.
    m0 = 0
    while C_single * (rho ** m0) >= Decimal(1):
        m0 += 1
        if m0 > 10000:
            raise RuntimeError("m0 search exceeded limit")

    print(f"\n(4) Asymptotic threshold for non-trivial single-ρ bound (n=2)")
    print(f"  C = (2-q) + 2^n = {float(C_single):.4f}")
    print(f"  ρ = {float(rho):.10f}")
    print(f"  bound 1-SD < 1 first at m = {m0}")
    print(f"  bound 1-SD at m={m0}: {float(C_single * (rho ** m0)):.6f}")

    # --- Save output ---------------------------------------------------------
    summary = {
        "experiment": 500,
        "track": "W",
        "constants": constants,
        "w_a_full_component": {
            "theorem": "SD(P_full^{(m)}, P_lpn^{(m)}) ≥ 1 - ρ(n)^m",
            "rho_formula_general": "1 - (1/2^n)[1 - sqrt((1-p_eff(n))/2) - sqrt(p_eff(n)/2)]",
            "checks": wa_checks,
            "label": "THEOREM (explicit rate; verified against exact full-component SD)",
        },
        "w_b_graph_membership": {
            "theorem": "Pr_{P_lpn}[y ∈ col(C)] ≤ 2^n (1-p_eff(n))^m → 0",
            "checks": wb_checks,
            "label": "THEOREM (explicit exponential decay)",
        },
        "w_c_mixture_combination": {
            "theorem": (
                "1 - SD(P_out^{(m)}, P_lpn^{(m)}) ≤ "
                "(2-q(n)) ρ(n)^m + (1-q(n)) 2^{n-m} + 2^n (1-p_eff(n))^m"
            ),
            "checks": wc_checks,
            "asymptotic_single_rho": {
                "C": str(C_single),
                "C_float": float(C_single),
                "rho": str(rho),
                "rho_float": float(rho),
                "m0_first_nontrivial": m0,
            },
            "label": "THEOREM (explicit overall rate; verified against exact SD table)",
        },
        "claim_labels": {
            "w_a_full_component_separation": "THEOREM (explicit ρ(n) < 1)",
            "w_b_graph_component_separation": "THEOREM (explicit exponential decay)",
            "w_c_mixture_combination": "THEOREM (explicit C(n), ρ(n); verified numerically)",
            "limit_sd_to_one_uniform_B_per_A": "THEOREM (fixed n, m→∞)",
            "general_randomized_B": "NO-GO / OPEN (result does not bound general marginal-adaptive B)",
        },
        "interpretation_guards": {
            "strategy_scope": "uniform-B-per-A marginal-adaptive strategy only",
            "axis": "m grows at fixed n",
            "comparison_distribution": "LPN_{p_eff(n)}, matched rate; never transformed",
            "practical_attack": "SD numbers do not imply a practical distinguisher",
            "L1_exact_arithmetic": "p_eff, q_graph, exact SD are Fractions; theorem constants explicit rational+sqrt formulas",
            "L2_J_twist_duality": "standard F_2 pairing only; no symplectic dual",
            "L3_query_class_hygiene": "statistical-distance claims only; no unrestricted Feldman theorem",
            "L4_comparison_distribution": "LPN target is the matched-rate product distribution, never post-processed",
        },
    }

    out_path = out_dir / "500-trackW-limit-theorem.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {out_path}")

    print("\n" + "=" * 78)
    print("VERDICT: W-a/W-b/W-c proved with explicit rates; exact cross-checks pass.")
    print("Scope: uniform-B-per-A only.  General B remains OPEN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
