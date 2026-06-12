#!/usr/bin/env python3
"""193: General-j moment closure for OP1.

The moments

  m_j^{(n)} = E_A[ C(t,j) / C(2n,j) ]

where t = |supp(c_1) ∩ supp(c_2)| for two random non-zero vectors c_1,c_2 in a
random Lagrangian subspace L ⊂ F_2^{2n}, have the exact closed form

  m_j^{(n)} = ( T_j (D_j^2/2 - D_j) + A_j D_j/2 ) / ( T_j P ),

with
  D_j = 2^{2n-j},
  P   = (2^{2n}-1)(2^{2n-1}-2),
  T_j = binom(2n,j),
  A_j = binom(n,j/2) if j is even, else 0.

This script computes the table of exact values and cross-checks the j=2,3
cases against the previously established closed forms.
"""
import argparse
import json
from fractions import Fraction
from math import comb
from pathlib import Path


def general_moment(n: int, j: int) -> Fraction:
    """Exact closed-form moment m_j^{(n)}."""
    if not (1 <= j <= 2 * n):
        raise ValueError("j must satisfy 1 <= j <= 2n")
    D = Fraction(1 << (2 * n - j))
    P = Fraction((1 << (2 * n)) - 1) * Fraction((1 << (2 * n - 1)) - 2)
    T = comb(2 * n, j)
    A = comb(n, j // 2) if j % 2 == 0 else 0
    num = T * (D * D / 2 - D) + A * (D / 2)
    return num / (T * P)


def closed_m2(n: int) -> Fraction:
    """Previously known m_2 closed form (from counting lemmas)."""
    u = Fraction(1 << (2 * n - 2))
    num = (2 * n - 1) * u * u - (4 * n - 3) * u
    den = 4 * (2 * n - 1) * (4 * u * u - 5 * u + 1)
    return num / den


def closed_m3(n: int) -> Fraction:
    """Previously known m_3 closed form (from counting lemmas)."""
    u = Fraction(1 << (2 * n - 2))
    num = u * (u - 4)
    den = 16 * (4 * u * u - 5 * u + 1)
    return num / den


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--max-n", type=int, default=8)
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    max_n = args.max_n

    table = {}
    for n in range(2, max_n + 1):
        row = {}
        for j in range(1, 2 * n + 1):
            row[str(j)] = str(general_moment(n, j))
        table[str(n)] = row

    # Cross-checks
    checks = []
    for n in range(2, max_n + 1):
        checks.append({
            "n": n,
            "m2_match": general_moment(n, 2) == closed_m2(n),
            "m3_match": general_moment(n, 3) == closed_m3(n),
        })

    result = {
        "experiment": "op1-general-j-moment-closure",
        "formula": "m_j = (T_j (D_j^2/2 - D_j) + A_j D_j/2) / (T_j P)",
        "max_n": max_n,
        "table": table,
        "cross_checks": checks,
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "193-op1-general-j-moment-closure.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
