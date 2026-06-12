#!/usr/bin/env python3
"""189: lem:m2 n=3 exact uniform-B-per-A joint SD.

For each Lagrangian A in F_2^6, B is drawn uniformly from F_2^{m x 6}.
Compute exact SD((C, y), LPN_{1/4}) for n=3, m=3,4.

WARNING: the output noise rate is p_eff = (1-(3/4)^{2n})/2 -> 1/2, not 1/4.
The values below are raw distances to LPN_{1/4}; the correct lem:m2 comparison
uses matched-rate LPN_{p_eff}.  See meta/2026-06-14-KIMI-lem-m2-n3-uniform-B-exact.md.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases_n,
    exact_sd_counts,
    lpn_target_counts_n,
    randomized_uniform_B_counts_n,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    m = args.m
    if m not in (3, 4):
        raise ValueError("this experiment supports m=3 or m=4")

    n = 3
    bases = list(enumerate_lagrangian_bases_n(n))
    p = Fraction(1, 4)

    red_counts, red_denom = randomized_uniform_B_counts_n(m, n, bases)
    lpn_counts, lpn_denom = lpn_target_counts_n(m, n, p)
    sd = exact_sd_counts(red_counts, red_denom, lpn_counts, lpn_denom)

    result = {
        "n": n,
        "m": m,
        "p_lpn": str(p),
        "num_lagrangian": len(bases),
        "red_denom": red_denom,
        "lpn_denom": lpn_denom,
        "sd": str(sd),
        "sd_float": float(sd),
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"189-lem-m2-n3-uniform-B-exact-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
