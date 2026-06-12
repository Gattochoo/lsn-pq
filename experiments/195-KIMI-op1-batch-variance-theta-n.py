#!/usr/bin/env python3
"""195: Batch-variance multiplier V_{2n} for j = Theta(n) (OP1).

Using the exact closed form for all subset moments

    m_j^{(n)} = E_A[ binom(t,j) / binom(2n,j) ],

we compute the bundle variance multiplier

    V_k = sum_{j=0}^k binom(k,j) sigma^{2j} m_j^{(n)}

for k = 2n and compare it to the i.i.d. Bernoulli(1/4) multiplier

    V_k^{iid} = (1 + sigma^2/4)^k = (16/9)^n,

since p = 1/4 and sigma^2 = (1-2p)^2/(p(1-p)) = 4/3.

The script implements two independent exact formulas:

1. Direct summation using the general-j moment closure.
2. A closed form obtained by summing the binomial series:

    V_{2n} = [X^4 - 2 X * 25^n + X * 13^n - 4 X * 9^n + 4 * 9^n]
             / [9^n (X-1)(X-4)],

   with X = 4^n.

Output is written to experiments/output/195-op1-batch-variance-theta-n.json.
"""
import argparse
import json
import math
from fractions import Fraction
from math import comb
from pathlib import Path


SIGMA2 = Fraction(4, 3)
IID_BASE = Fraction(16, 9)


def general_moment(n: int, j: int) -> Fraction:
    """Exact closed-form moment m_j^{(n)} from experiments/193."""
    if not (1 <= j <= 2 * n):
        raise ValueError("j must satisfy 1 <= j <= 2n")
    D = Fraction(1 << (2 * n - j))
    P = Fraction((1 << (2 * n)) - 1) * Fraction((1 << (2 * n - 1)) - 2)
    T = comb(2 * n, j)
    A = comb(n, j // 2) if j % 2 == 0 else 0
    num = T * (D * D / 2 - D) + A * (D / 2)
    return num / (T * P)


def V_direct(n: int) -> Fraction:
    """V_{2n} by direct summation (cross-check)."""
    N = 2 * n
    s = Fraction(1, 1)  # j = 0 contribution
    for j in range(1, N + 1):
        s += comb(N, j) * (SIGMA2 ** j) * general_moment(n, j)
    return s


def V_closed(n: int) -> Fraction:
    """Exact closed form for V_{2n} derived from the moment closure."""
    X = Fraction(4) ** n
    num = (
        X ** 4
        - 2 * X * (Fraction(25) ** n)
        + X * (Fraction(13) ** n)
        - 4 * X * (Fraction(9) ** n)
        + 4 * (Fraction(9) ** n)
    )
    den = (Fraction(9) ** n) * (X - 1) * (X - 4)
    return num / den


def V_iid(n: int) -> Fraction:
    """i.i.d. Bernoulli(1/4) variance multiplier."""
    return IID_BASE ** n


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--max-n", type=int, default=12)
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    max_n = args.max_n

    results = []
    cross_checks = []

    for n in range(2, max_n + 1):
        V = V_closed(n)
        # Cross-check against direct summation for modest n.
        if n <= 10:
            direct = V_direct(n)
            cross_checks.append({
                "n": n,
                "closed_form": str(V),
                "direct_sum": str(direct),
                "match": V == direct,
            })
            if V != direct:
                raise RuntimeError(f"Closed form mismatch at n={n}")

        Viid = V_iid(n)
        Vf = float(V)
        Vif = float(Viid)
        abs_dev = Vf - Vif
        rel_dev = abs_dev / Vif if Vif != 0 else None
        log_ratio = math.log(Vf / Vif) if Vif != 0 and Vf > 0 else None

        results.append({
            "n": n,
            "V": str(V),
            "V_iid": str(Viid),
            "V_float": Vf,
            "V_iid_float": Vif,
            "abs_dev": abs_dev,
            "rel_dev": rel_dev,
            "log_ratio": log_ratio,
        })

    summary = {
        "experiment": "op1-batch-variance-theta-n",
        "parameters": {
            "p": "1/4",
            "sigma2": "4/3",
            "a": "sigma2",
            "k": "2n",
            "V_iid_formula": "(1 + sigma2/4)^{2n} = (16/9)^n",
            "V_closed_form": "[X^4 - 2 X 25^n + X 13^n - 4 X 9^n + 4 9^n] / [9^n (X-1)(X-4)], X=4^n",
        },
        "max_n": max_n,
        "results": results,
        "cross_checks": cross_checks,
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "195-op1-batch-variance-theta-n.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved: {out_path}\n")
    print("n     V_{2n}              V_iid              abs_dev        rel_dev        log_ratio")
    print("-" * 90)
    for r in results:
        print(f"{r['n']:<5} {r['V_float']:<19.12f} {r['V_iid_float']:<19.12f} "
              f"{r['abs_dev']:<14.6e} {r['rel_dev']:<14.6e} {r['log_ratio']:<14.6e}")


if __name__ == "__main__":
    main()
