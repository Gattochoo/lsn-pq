#!/usr/bin/env python3
"""191: matched-rate SD for uniform-B-per-A along the m = 2n scaling axis.

For each Lagrangian A in F_2^{2n}, B is drawn uniformly from F_2^{m x 2n}.
The output noise rate is p_eff(n) = (1 - (3/4)^{2n}) / 2, so the correct
lem:m2 comparison is against LPN_{p_eff} (not LPN_{1/4}).  This script computes
the exact total-variation distance for small n along m = 2n, using the analytic
mixture form of the reduction distribution:

  P_out = q(n) * P_graph + (1 - q(n)) * P_full,

where q(n) = Pr[Ax + e in span(A)] (averaged over A, x, e) and
P_graph / P_full are the graph / full-space components derived in the
lem:m2 design notes.

Currently feasible for n <= 3 exactly; larger n uses sampling (see --sample).
"""
import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import lpn_target_counts_n


def popcount(x: int) -> int:
    return x.bit_count()


def rank_f2_cols(cols: list[int], m: int) -> int:
    pivots = []
    for v in cols:
        x = v & ((1 << m) - 1)
        if x == 0:
            continue
        for p in pivots:
            if (x >> (p.bit_length() - 1)) & 1:
                x ^= p
        if x:
            pivots.append(x)
    return len(pivots)


def colspace_mask(cols: list[int], m: int) -> int:
    sp = [0]
    for v in cols:
        sp += [s ^ v for s in sp]
    mask = 0
    for y in sp:
        mask |= 1 << y
    return mask


def p_eff(n: int) -> Fraction:
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    """Average probability that v = Ax + e lies in span(A)."""
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def exact_matched_sd(n: int, m: int) -> tuple[Fraction, float]:
    """Exact SD((C,y), LPN_{p_eff}) for uniform B per A."""
    p = p_eff(n)
    q = q_graph(n)
    q_num = q.numerator
    q_den = q.denominator

    # LPN counts with denominator D.
    t0 = time.time()
    lpn_counts, D = lpn_target_counts_n(m, n, p)
    t_lpn = time.time() - t0

    size = 1 << ((n + 1) * m)
    num_C = 1 << (n * m)
    y_mask = (1 << m) - 1

    # Scaled P_out counts relative to the same denominator D.
    full_count = (q_den - q_num) * (D // (q_den * size))
    graph_base = [
        q_num * (D // (q_den * num_C * (1 << r)))
        for r in range(n + 1)
    ]

    # Precompute rank and column-space mask for every C.
    ranks = [0] * num_C
    masks = [0] * num_C
    for C in range(num_C):
        cols = []
        tmp = C
        for _ in range(n):
            cols.append(tmp & y_mask)
            tmp >>= m
        ranks[C] = rank_f2_cols(cols, m)
        masks[C] = colspace_mask(cols, m)

    t0 = time.time()
    diff = 0
    for key in range(size):
        y = key & y_mask
        C = key >> m
        p_out = full_count
        if (masks[C] >> y) & 1:
            p_out += graph_base[ranks[C]]
        diff += abs(lpn_counts[key] - p_out)
    t_out = time.time() - t0

    sd = Fraction(diff, 2 * D)
    return sd, t_lpn, t_out


def sample_matched_sd(n: int, m: int, samples: int = 1_000_000) -> tuple[float, float]:
    """Monte-Carlo estimate of SD((C,y), LPN_{p_eff}) for larger n."""
    import random

    p = float(p_eff(n))
    # Generate samples from reduction and LPN, then use empirical total variation.
    # This is a rough estimator; exact computation is preferred when feasible.
    # TODO: implement if needed.
    raise NotImplementedError("sampling mode not yet implemented")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, required=True, help="secret dimension")
    p.add_argument("--m", type=int, required=True, help="number of output rows")
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--sample", action="store_true", help="use sampling for large n")
    return p.parse_args()


def main():
    args = parse_args()
    n, m = args.n, args.m

    if args.sample:
        sd_float = sample_matched_sd(n, m)
        result = {
            "n": n,
            "m": m,
            "mode": "sample",
            "sd_float": sd_float,
        }
    else:
        if n > 3:
            raise ValueError(
                "exact computation is currently feasible only for n <= 3; "
                "use --sample for larger n"
            )
        sd, t_lpn, t_out = exact_matched_sd(n, m)
        result = {
            "n": n,
            "m": m,
            "mode": "exact",
            "p_eff": str(p_eff(n)),
            "q_graph": str(q_graph(n)),
            "sd": str(sd),
            "sd_float": float(sd),
            "time_lpn_counts_sec": t_lpn,
            "time_out_loop_sec": t_out,
        }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"191-lem-m2-uniform-B-matched-rate-m2n-n{n}-m{m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
