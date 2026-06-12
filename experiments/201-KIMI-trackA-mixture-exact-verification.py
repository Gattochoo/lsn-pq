#!/usr/bin/env python3
"""Independent exact verification of Track A mixture SD using integer arithmetic.

This script recomputes the matched-rate SD for the uniform-B-per-A reduction via
the exact mixture decomposition, but avoids the floor-division shortcut that
contaminates experiments/200 for n=3.  The output probability for each key is
kept as a rational with denominator q_den*D, and the LPN counts are scaled by
q_den, so no rounding occurs.
"""
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import lpn_target_counts_n


def p_eff(n: int) -> Fraction:
    return Fraction(1 - Fraction(3, 4) ** (2 * n), 2)


def q_graph(n: int) -> Fraction:
    p_zero = Fraction(3, 4) ** (2 * n)
    return p_zero + (1 - p_zero) / (2 ** n + 1)


def rank_f2_cols(cols: list[int], m: int) -> int:
    rows = cols.copy()
    rank = 0
    mask = (1 << m) - 1
    for col_idx in range(m):
        bit = 1 << col_idx
        pivot = None
        for r in range(rank, len(rows)):
            if rows[r] & bit:
                pivot = r
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and (rows[r] & bit):
                rows[r] ^= rows[rank]
        rank += 1
    return rank


def colspace_mask(cols: list[int], m: int) -> int:
    mask = (1 << m) - 1
    space = {0}
    for c in cols:
        new = [s ^ c for s in space]
        space.update(new)
    return sum(1 << (y & mask) for y in space)


def exact_matched_sd_mixture_fixed(n: int, m: int):
    p = p_eff(n)
    q = q_graph(n)
    q_num, q_den = q.numerator, q.denominator

    lpn_counts, D = lpn_target_counts_n(m, n, p)
    size = 1 << ((n + 1) * m)
    num_C = 1 << (n * m)
    y_mask = (1 << m) - 1

    # Integer contributions after clearing denominator q_den.
    # LPN term: lpn_counts[key] * q_den
    # Full term: D * (q_den - q_num) / size  (integer because D/size is)
    # Graph term: D * q_num / (num_C * 2^rank) (integer because D/(num_C*2^rank) is)
    full_term = D * (q_den - q_num) // size

    ranks = [0] * num_C
    masks = [0] * num_C
    graph_terms = [0] * num_C
    for C in range(num_C):
        cols = []
        tmp = C
        for _ in range(n):
            cols.append(tmp & y_mask)
            tmp >>= m
        ranks[C] = rank_f2_cols(cols, m)
        masks[C] = colspace_mask(cols, m)
        graph_terms[C] = D * q_num // (num_C * (1 << ranks[C]))

    diff_num = 0
    for key in range(size):
        y = key & y_mask
        C = key >> m
        target = lpn_counts[key] * q_den - full_term
        if (masks[C] >> y) & 1:
            target -= graph_terms[C]
        diff_num += abs(target)

    sd = Fraction(diff_num, 2 * D * q_den)
    return {
        "n": n,
        "m": m,
        "p_eff": str(p),
        "q_graph": str(q),
        "sd": str(sd),
        "sd_float": float(sd),
    }


if __name__ == "__main__":
    print("n=2 direct-known exact (m=4): 277825754675/1099511627776")
    for m in [2, 3, 4]:
        res = exact_matched_sd_mixture_fixed(2, m)
        print(f"  n=2 m={m}: {res['sd']} = {res['sd_float']:.6f}")
    print()
    print("Claude-corrected n=3 values (for comparison):")
    print("  m=2: 60016775/2415919104")
    print("  m=3: 27456165227309/422212465065984")
    print("  m=4: 2606451312633458017/20752587082923245568")
    print("  m=5: 1948309423583462892421105/10880332376531662572355584")
    print("  m=6: 154465747684542391975435825813/713053462628379038341895553024")
    print()
    for m in [2, 3, 4, 5, 6]:
        res = exact_matched_sd_mixture_fixed(3, m)
        print(f"  n=3 m={m}: {res['sd']} = {res['sd_float']:.9f}")
