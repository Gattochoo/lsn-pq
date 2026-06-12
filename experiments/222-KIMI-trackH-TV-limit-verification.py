#!/usr/bin/env python3
"""
222-KIMI-trackH-TV-limit-verification.py

Track H follow-up: verify the TV-limit theorem numerically to larger n using
only the closed-form decomposition (no per-ell JSON dump; just the aggregate
remainders).

Theorem from 221:
    Delta_ell = (X^2*C - 1) beta_ell - 2XC q_ell + (-1)^ell X C r_ell
                - 1_{ell=0} * 4/(X-4),
    with X = 4^n, C = 1/[(X-1)(X-4)],
    beta_ell = Pr[Bin(2n,1/4)=ell],
    q_ell    = Pr[Bin(2n,1/2)=ell],
    r_ell    = [z^ell] ((5+2z+z^2)/4)^n.

Consequences used here:
  * sum_ell r_ell = p(1)^n = 2^n exactly.
  * sum_ell |Delta_ell| = 2^{-n} + O(4^{-n}).
  * TV_n = 1/2 sum_ell |Delta_ell|, so 2^n TV_n = 1/2 + O(2^{-n}).

This script computes exact TV_n and the remainders for n = 2..15, showing the
O(2^{-n}) convergence to 1/2.  All arithmetic uses fractions.Fraction.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from fractions import Fraction
from math import comb
import json
from pathlib import Path


def tv_and_remainders(n: int):
    """Return exact TV_n, 2^n TV_n, and the theorem remainders."""
    N = 2 * n
    X = 4 ** n
    C = Fraction(1, (X - 1) * (X - 4))

    # r_ell for all ell via convolution (5+2z+z^2)^n / 4^n.
    # (5+2z+z^2)^n = sum_i C(n,i) z^{2i} (5+2z)^{n-i}.
    r = [Fraction(0) for _ in range(N + 1)]
    for ell in range(N + 1):
        total = Fraction(0)
        for i in range(ell // 2 + 1):
            if i > n:
                continue
            j = ell - 2 * i
            if j < 0 or j > n - i:
                continue
            total += Fraction(
                comb(n, i) * comb(n - i, j) * 5 ** (n - i - j) * 2 ** j,
                4 ** n,
            )
        r[ell] = total

    sum_abs_delta = Fraction(0)
    sum_abs_piece3 = Fraction(0)
    for ell in range(N + 1):
        beta = Fraction(comb(N, ell) * 3 ** (N - ell), 4 ** N)
        q = Fraction(comb(N, ell), 2 ** N)
        piece1 = (X * X * C - 1) * beta
        piece2 = -C * 2 * X * q
        piece3 = (-1) ** ell * C * X * r[ell]
        correction = -Fraction(4, X - 4) if ell == 0 else Fraction(0)
        delta = piece1 + piece2 + piece3 + correction
        sum_abs_delta += abs(delta)
        sum_abs_piece3 += abs(piece3)

    tv = sum_abs_delta / 2
    two_n_tv = tv * 2 ** n
    two_n_sum_abs_delta = sum_abs_delta * 2 ** n
    two_n_sum_abs_piece3 = sum_abs_piece3 * 2 ** n
    two_n_tv_minus_half = two_n_tv - Fraction(1, 2)
    sum_r = sum(r)

    return {
        "n": n,
        "N": N,
        "tv_exact": str(tv),
        "tv_float": float(tv),
        "2^n_TV": str(two_n_tv),
        "2^n_TV_float": float(two_n_tv),
        "2^n_TV_minus_1/2": str(two_n_tv_minus_half),
        "2^n_TV_minus_1/2_float": float(two_n_tv_minus_half),
        "2^n_sum_abs_Delta": str(two_n_sum_abs_delta),
        "2^n_sum_abs_piece3": str(two_n_sum_abs_piece3),
        "sum_r_ell": str(sum_r),
        "sum_r_ell_equals_2^n": sum_r == Fraction(2 ** n),
    }


def main():
    out_dir = Path(__file__).with_suffix("").parent.parent / "experiments" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "222-KIMI-trackH-TV-limit-verification.json"

    results = {
        "track": "H",
        "experiment": 222,
        "purpose": "verify 2^n TV -> 1/2 to larger n via closed form",
        "claims": {
            "limit_verification": "EVIDENCE (exact rational computation, n=2..15)",
            "remainder_decay": "EVIDENCE (2^n TV - 1/2 decays like O(2^{-n}))",
            "sum_r_identity": "THEOREM (sum r_ell = 2^n by evaluation at z=1)",
        },
        "interpretation_guard": {
            "comparison_distribution": "Bin(2n,1/4): unconstrained i.i.d. row benchmark",
            "scaling": "pairwise level; no m parameter",
            "hardness_implication": "structural distribution result only",
        },
        "L1_L2_L3_guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; rationals stored as strings",
            "L2_duality_care": "N/A: uses established B_j formula",
            "L3_query_class_hygiene": "N/A: no SQ theorem invoked",
        },
        "per_n": {},
    }

    print(f"{'n':>2} {'2^n TV':>12} {'2^n TV - 1/2':>14} {'2^n sum|Delta|':>16} {'sum r=2^n?':>10}")
    for n in range(2, 16):
        row = tv_and_remainders(n)
        results["per_n"][str(n)] = row
        print(f"{n:>2} {row['2^n_TV_float']:>12.6f} {row['2^n_TV_minus_1/2_float']:>14.4e} "
              f"{float(Fraction(row['2^n_sum_abs_Delta'])):>16.6f} {row['sum_r_ell_equals_2^n']!s:>10}")

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")


if __name__ == "__main__":
    main()
