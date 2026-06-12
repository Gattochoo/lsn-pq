#!/usr/bin/env python3
"""185b: Sanity checks for full joint SD enumeration."""
from fractions import Fraction

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    reduction_counts_for_B,
)


def reduction_denom():
    return 15 * (1 << 2) * sum(3 ** (4 - e.bit_count()) for e in range(1 << 4))


def check_zero_B_is_far():
    m = 3
    B_cols = [0, 0, 0, 0]
    red_counts = reduction_counts_for_B(B_cols, enumerate_lagrangian_bases(), m)
    lpn_counts, lpn_denom = lpn_target_counts(m, Fraction(1, 4))
    sd = exact_sd_counts(red_counts, reduction_denom(), lpn_counts, lpn_denom)
    assert sd > Fraction(9, 10), f"zero-B SD unexpectedly small: {sd}"
    print(f"zero-B SD for m={m}: {sd} (OK)")


def check_bounds():
    m = 3
    lpn_counts, lpn_denom = lpn_target_counts(m, Fraction(1, 4))
    best = Fraction(2)
    worst = Fraction(-1)
    mask = (1 << m) - 1
    for bits in range(1 << (4 * m)):
        B_cols = [((bits >> (j * m)) & mask) for j in range(4)]
        red_counts = reduction_counts_for_B(B_cols, enumerate_lagrangian_bases(), m)
        sd = exact_sd_counts(red_counts, reduction_denom(), lpn_counts, lpn_denom)
        assert 0 <= sd <= 1
        if sd < best:
            best = sd
        if sd > worst:
            worst = sd
    print(f"m={m} SD bounds: [{best}, {worst}] (OK)")


if __name__ == "__main__":
    check_zero_B_is_far()
    check_bounds()
