#!/usr/bin/env python3
"""187: lem:m2 randomized adaptive uniform B per A — exact joint SD.

For each Lagrangian A, B is drawn independently and uniformly from
F_2^{m x 4}.  Compute exact SD((C, y), LPN_{1/4}) for n=2.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    randomized_uniform_B_counts,
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

    red_counts, red_denom = randomized_uniform_B_counts(m, bases)
    lpn_counts, lpn_denom = lpn_target_counts(m, p)
    sd = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)

    result = {
        "n": 2,
        "m": m,
        "p_prime": str(p),
        "num_lagrangian": len(bases),
        "red_denom": red_denom,
        "lpn_denom": lpn_denom,
        "sd": str(sd),
        "sd_float": float(sd),
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"187-lem-m2-randomized-adaptive-uniform-B-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
