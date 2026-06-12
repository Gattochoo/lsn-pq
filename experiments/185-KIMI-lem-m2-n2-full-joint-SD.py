#!/usr/bin/env python3
"""185: lem:m2 exact full joint SD((C,y), LPN_{1/4}) for n=2, arbitrary m.

Enumerates all B in F_2^{m x 4} and computes the exact statistical distance
between the reduction output distribution and standard LPN.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    reduction_counts_for_B,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    m = args.m
    if m < 1:
        raise ValueError("m must be >= 1")

    bases = list(enumerate_lagrangian_bases())
    p = Fraction(1, 4)

    lpn_counts, lpn_denom = lpn_target_counts(m, p)

    # Total weight denominator for reduction_counts_for_B:
    # len(bases) choices * 4 x-values * sum over e of 3^(4-|e|).
    red_denom = len(bases) * (1 << 2) * sum(
        3 ** (4 - e.bit_count()) for e in range(1 << 4)
    )

    num_B = 1 << (4 * m)
    mask = (1 << m) - 1

    best_B = None
    best_sd = Fraction(2)
    worst_B = None
    worst_sd = Fraction(-1)
    sd_sum = Fraction(0)

    for bits in range(num_B):
        B_cols = [((bits >> (j * m)) & mask) for j in range(4)]
        red_counts = reduction_counts_for_B(B_cols, bases, m)
        sd = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)
        sd_sum += sd
        if sd < best_sd:
            best_sd = sd
            best_B = B_cols[:]
        if sd > worst_sd:
            worst_sd = sd
            worst_B = B_cols[:]

    result = {
        "n": 2,
        "m": m,
        "p_prime": str(p),
        "num_lagrangian": len(bases),
        "num_B": num_B,
        "min_sd": str(best_sd),
        "max_sd": str(worst_sd),
        "avg_sd": str(Fraction(sd_sum, num_B)),
        "best_B": best_B,
        "worst_B": worst_B,
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"185-lem-m2-n2-full-joint-SD-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
