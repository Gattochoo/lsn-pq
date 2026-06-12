#!/usr/bin/env python3
"""188: Sweep randomized adaptive B distributions for lem:m2 exact SD.

Compares uniform full-rank, rank-deficient, and Bernoulli(p)-row distributions
against standard LPN_{1/4} for n=2, m=3,4.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import (
    bernoulli_rows_B_counts,
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    rank_conditioned_counts,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--output", type=str, default=None)
    return p


def main():
    p = parse_args()
    args = p.parse_args()
    m = args.m
    if m not in (3, 4):
        p.error("this experiment supports m=3 or m=4")

    bases = list(enumerate_lagrangian_bases())
    p_lpn = Fraction(1, 4)
    lpn_counts, lpn_denom = lpn_target_counts(m, p_lpn)

    cache: dict[Fraction, tuple[list[int], int]] = {}

    def bernoulli_counts_cached(p: Fraction) -> tuple[list[int], int]:
        if p not in cache:
            cache[p] = bernoulli_rows_B_counts(m, p, bases)
        return cache[p]

    # Uniform over all matrices == Bernoulli(1/2) rows.
    uniform_counts, uniform_denom = bernoulli_counts_cached(Fraction(1, 2))
    uniform_sd = exact_sd_counts(uniform_counts, uniform_denom, lpn_counts, lpn_denom)

    # Uniform full-rank.
    full_rank_counts, full_rank_denom = rank_conditioned_counts(m, rank=m, bases=bases)
    full_rank_sd = exact_sd_counts(
        full_rank_counts, full_rank_denom, lpn_counts, lpn_denom
    )

    # Rank-deficient only meaningful for m=4 (rank 3).
    rank3_sd = None
    if m == 4:
        rank3_counts, rank3_denom = rank_conditioned_counts(m, rank=3, bases=bases)
        rank3_sd = exact_sd_counts(
            rank3_counts, rank3_denom, lpn_counts, lpn_denom
        )

    # Bernoulli(p) rows for fixed p values.
    bernoulli_sd = {}
    for p_str in ("1/4", "1/3", "1/2"):
        p = Fraction(p_str)
        counts, denom = bernoulli_counts_cached(p)
        sd = exact_sd_counts(counts, denom, lpn_counts, lpn_denom)
        bernoulli_sd[p_str] = str(sd)

    # Search for best p in [0.05, 0.5] with step 0.05.
    best_p = None
    best_sd = Fraction(2)
    for k in range(1, 11):  # 0.05, 0.10, ..., 0.50
        p = Fraction(k, 20)
        counts, denom = bernoulli_counts_cached(p)
        sd = exact_sd_counts(counts, denom, lpn_counts, lpn_denom)
        if sd < best_sd:
            best_sd = sd
            best_p = p

    result = {
        "n": 2,
        "m": m,
        "p_lpn": str(p_lpn),
        "num_lagrangian": len(bases),
        "uniform_sd": str(uniform_sd),
        "uniform_sd_float": float(uniform_sd),
        "uniform_full_rank_sd": str(full_rank_sd),
        "uniform_full_rank_sd_float": float(full_rank_sd),
        "rank3_sd": str(rank3_sd) if rank3_sd is not None else None,
        "rank3_sd_float": float(rank3_sd) if rank3_sd is not None else None,
        "bernoulli_p_sd": bernoulli_sd,
        "best_p": str(best_p),
        "best_p_sd": str(best_sd),
        "best_p_sd_float": float(best_sd),
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"188-lem-m2-randomized-B-distribution-sweep-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
