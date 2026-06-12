#!/usr/bin/env python3
"""
221-KIMI-trackH-tv-rate-leading-term.py

Track H deliverable: decompose the quadrant-count deviation
    Delta_ell = Pr[t=ell] - Pr[Bin(2n,1/4)=ell]
as an alternating sum of delta_j = B_j - binom(2n,j) 4^{-j}, extract the
leading asymptotic term, and verify the exact TV table for n <= 10.

The B_j come from thm:mj-general (lsn-core.tex, sec:moments):
    B_j = [C(2n,j)(D_j^2/2 - D_j) + 1_{even j} C(n,j/2) D_j/2] / P,
    D_j = 2^{2n-j},  P = (2^{2n}-1)(2^{2n-1}-2) = (X-1)(X-4)/2,  X = 4^n.

The inclusion-exclusion/binomial inversion gives
    Pr[t=ell] = sum_{j=ell}^{2n} (-1)^{j-ell} C(j,ell) B_j,
and the same transform applied to C(2n,j) 4^{-j} yields Bin(2n,1/4).
Hence
    Delta_ell = sum_{j=ell}^{2n} (-1)^{j-ell} C(j,ell) delta_j.

We rewrite Delta_ell in closed form (splitting the B_j correction into
three binomial-inverse pieces) and identify the leading contribution.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from fractions import Fraction
from math import comb
import json
import sys
from pathlib import Path


def P_isotropic(n: int) -> int:
    """Number of ordered isotropic pairs."""
    N = 2 * n
    return (2 ** N - 1) * (2 ** (N - 1) - 2)


def B_j(n: int, j: int) -> Fraction:
    """B_j = E[C(t,j)] from thm:mj-general; valid for 1 <= j <= 2n."""
    N = 2 * n
    P = P_isotropic(n)
    Dj = 2 ** (N - j)
    num = comb(N, j) * (Fraction(Dj * Dj, 2) - Dj)
    if j % 2 == 0:
        num += comb(n, j // 2) * Fraction(Dj, 2)
    return Fraction(num, P)


def binomial_moment(n: int, j: int) -> Fraction:
    """j-th binomial moment of Bin(2n, 1/4)."""
    N = 2 * n
    return Fraction(comb(N, j), 4 ** j)


def delta_j(n: int, j: int) -> Fraction:
    """delta_j = B_j - C(2n,j) 4^{-j}.  By definition delta_0 = 0."""
    if j == 0:
        return Fraction(0)
    return B_j(n, j) - binomial_moment(n, j)


def Delta_ell_alternating(n: int, ell: int) -> Fraction:
    """Delta_ell via the alternating sum of delta_j."""
    N = 2 * n
    total = Fraction(0)
    for j in range(ell, N + 1):
        sign = -1 if (j - ell) & 1 else 1
        total += sign * comb(j, ell) * delta_j(n, j)
    return total


def binom_pmf(n: int, ell: int) -> Fraction:
    """Pr[Bin(2n,1/4) = ell]."""
    N = 2 * n
    return Fraction(comb(N, ell) * 3 ** (N - ell), 4 ** N)


def t_pmf(n: int, ell: int) -> Fraction:
    """Pr[t=ell] from the B_j inversion (equivalently Delta_ell + binomial pmf)."""
    return Delta_ell_alternating(n, ell) + binom_pmf(n, ell)


def total_variation(n: int) -> Fraction:
    """Exact TV(dist(t), Bin(2n,1/4))."""
    N = 2 * n
    return sum(abs(Delta_ell_alternating(n, ell)) for ell in range(N + 1)) / 2


def r_ell_direct(n: int, ell: int) -> Fraction:
    """r_ell = sum_k C(n,k) C(2k,ell) / 4^k (coefficients of ((5+2z+z^2)/4)^n)."""
    total = Fraction(0)
    for k in range((ell + 1) // 2, n + 1):
        total += Fraction(comb(n, k) * comb(2 * k, ell), 4 ** k)
    return total


def leading_term_approx(n: int, ell: int) -> Fraction:
    """
    Leading asymptotic term of Delta_ell in the bulk: (-1)^ell * X*C * r_ell,
    which is asymptotic to (-1)^ell * r_ell / 4^n.
    """
    N = 2 * n
    X = 4 ** n
    C = Fraction(1, (X - 1) * (X - 4))
    r = r_ell_direct(n, ell)
    return (-1) ** ell * C * X * r


def decompose_closed_form(n: int, ell: int):
    """
    Return the three closed-form pieces of Delta_ell.

    Writing X = 4^n, C = 1/[(X-1)(X-4)], P = (X-1)(X-4)/2, the exact
    B_j formula plus the binomial inversion gives, for ell >= 1:
        Delta_ell = (X^2*C - 1) * binom_ell  - 2X*C * q_ell  +  X*C * r_ell,
    and for ell = 0 the j=0 moment must be corrected by -4/(X-4):
        Delta_0   = (X^2*C - 1) * binom_0    - 2X*C * q_0    +  X*C * r_0  - 4/(X-4).
    Here
        binom_ell = Pr[Bin(2n,1/4)=ell],
        q_ell     = Pr[Bin(2n,1/2)=ell] = C(2n,ell)/2^{2n},
        r_ell     = [z^ell] ((5+2z+z^2)/4)^n
                  = sum_k C(n,k) C(2k,ell) / 4^k.
    The function returns (piece_D2, piece_D1, piece_even, j0_correction).
    """
    N = 2 * n
    X = 4 ** n
    C = Fraction(1, (X - 1) * (X - 4))
    binom_ell = binom_pmf(n, ell)
    q_ell = Fraction(comb(N, ell), 2 ** N)

    # r_ell = [z^ell] ((5+2z+z^2)/4)^n via the convolution
    #         (5+2z+z^2)^n = sum_i C(n,i) z^{2i} * (5+2z)^{n-i}.
    r = Fraction(0)
    for i in range(ell // 2 + 1):
        if i > n:
            continue
        # need j = ell - 2i from (5+2z)^{n-i}
        j = ell - 2 * i
        if j < 0 or j > n - i:
            continue
        term = comb(n, i) * comb(n - i, j) * 5 ** (n - i - j) * 2 ** j
        r += Fraction(term, 4 ** n)

    piece1 = (X * X * C - 1) * binom_ell   # D_j^2/2 part minus binomial
    piece2 = -C * 2 * X * q_ell            # -D_j part
    piece3 = (-1) ** ell * C * X * r       # even-j correction; sign = (-1)^ell
    correction = Fraction(0)
    if ell == 0:
        correction = -Fraction(4, X - 4)
    return piece1, piece2, piece3, correction


def main():
    out_dir = Path(__file__).with_suffix("").parent.parent / "experiments" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "221-KIMI-trackH-tv-rate-leading-term.json"

    results = {
        "track": "H",
        "experiment": 221,
        "purpose": "Delta_ell as alternating sum of delta_j; leading term; TV rate",
        "claims": {
            "alternating_sum": "THEOREM (exact identity from binomial inversion)",
            "closed_form_decomposition": "THEOREM (algebraic rewrite of the alternating sum)",
            "tv_table": "EVIDENCE (exact rational recomputation, n=2..10)",
            "r_ell_positivity": "THEOREM (r_ell > 0 for 0 <= ell <= 2n; explicit sum of non-negative terms)",
            "tv_limit": "THEOREM (2^n * TV -> 1/2 with explicit O(2^{-n}) remainder)",
            "leading_term_shape": "THEOREM (Delta_ell ~ (-1)^ell * r_ell / 4^n in the bulk; r_ell obeys a local LLT around ell=n/2)",
        },
        "interpretation_guard": {
            "comparison_distribution": "Bin(2n,1/4): exact law of t under unconstrained i.i.d. uniform rows",
            "scaling": "single secret pair (pairwise level); no m parameter",
            "hardness_implication": "structural distribution result only; rate is about a statistic, not SQ hardness",
        },
        "L1_L2_L3_guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON stores rationals as strings",
            "L2_duality_care": "N/A: this track uses the proven B_j formula; no new character sum over a subspace",
            "L3_query_class_hygiene": "N/A: no SQ theorem is invoked; this is a pairwise distribution statement",
        },
        "per_n": {},
    }

    # Verification: recomputed TV must match the 220/255 table.
    known_tv = {
        2: Fraction("707/5760"),
        3: Fraction("35183/645120"),
        4: Fraction("14891599/526417920"),
        5: Fraction("788813171/54707355648"),
        6: Fraction("129011724689/17570715402240"),
        7: Fraction("90177646929/23821297909760"),
        8: Fraction("8866562072659001/4611334179001466880"),
        9: Fraction("12710182327048981/13117434475422154752"),
        10: Fraction("29399506915728870947/60446002750575209349120"),
    }

    all_ok = True
    for n in range(2, 11):
        N = 2 * n
        tv = total_variation(n)
        two_n_tv = tv * 2 ** n
        match = tv == known_tv[n]
        all_ok &= match

        # Per-ell decomposition for this n.
        ell_data = []
        sum_abs_delta = Fraction(0)
        sum_abs_piece3 = Fraction(0)
        sum_r = Fraction(0)
        for ell in range(N + 1):
            delta_alt = Delta_ell_alternating(n, ell)
            p1, p2, p3, corr = decompose_closed_form(n, ell)
            closed = p1 + p2 + p3 + corr
            lead = leading_term_approx(n, ell)
            r_val = r_ell_direct(n, ell)
            sum_abs_delta += abs(delta_alt)
            sum_abs_piece3 += abs(p3)
            sum_r += r_val
            ell_data.append({
                "ell": ell,
                "Delta_ell_exact": str(delta_alt),
                "Delta_ell_float": float(delta_alt),
                "piece1_D2": str(p1),
                "piece2_D1": str(p2),
                "piece3_even": str(p3),
                "j0_correction": str(corr),
                "closed_form_check": str(closed),
                "closed_matches_alternating": delta_alt == closed,
                "r_ell": str(r_val),
                "leading_term_approx": str(lead),
                "leading_term_float": float(lead),
            })

        # Asymptotic check: sum_ell r_ell should equal p(1)^n = 2^n exactly.
        sum_r_check = (sum_r == Fraction(2 ** n))
        # The theorem predicts sum |Delta_ell| = 2^{-n} + O(4^{-n}).
        two_n_sum_abs = sum_abs_delta * 2 ** n
        two_n_piece3_sum_abs = sum_abs_piece3 * 2 ** n

        results["per_n"][str(n)] = {
            "N": N,
            "tv_exact": str(tv),
            "tv_float": float(tv),
            "2^n_TV": str(two_n_tv),
            "2^n_TV_float": float(two_n_tv),
            "matches_known_tv": match,
            "sum_abs_Delta": str(sum_abs_delta),
            "2^n_sum_abs_Delta": str(two_n_sum_abs),
            "2^n_sum_abs_piece3": str(two_n_piece3_sum_abs),
            "sum_r_ell": str(sum_r),
            "sum_r_ell_equals_2^n": sum_r_check,
            "per_ell": ell_data,
        }

        print(f"n={n:>2}: TV={tv}  2^n TV={float(two_n_tv):.6f}  "
              f"2^n sum|Delta|={float(two_n_sum_abs):.6f}  sum r={sum_r}==2^n?{sum_r_check}  "
              f"{'OK' if match else 'MISMATCH'}")

    results["verification"] = {"all_tv_match_220_255_table": all_ok}

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
