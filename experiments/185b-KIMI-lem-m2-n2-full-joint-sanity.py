#!/usr/bin/env python3
"""185b: Sanity checks for full joint SD enumeration."""
from fractions import Fraction

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    reduction_counts_for_B,
)

# LEM parameters: n=2 (symplectic space F_2^{2n}), m=3 (small sanity size).
N = 2
AMBIENT_DIM = 2 * N  # dimension of F_2^{2n}, also number of columns of B
M = 3
LPN_NOISE = Fraction(1, 4)

# Reduction distribution denominator:
# 15 Lagrangian subspaces of F_2^4 * 2^n choices of x *
# sum over errors e in F_2^4 of 3^{4 - |e|}.
NUM_LAGRANGIAN_SUBSPACES = 15
NUM_X = 1 << N
_ERROR_WEIGHT_SUM = sum(
    3 ** (AMBIENT_DIM - e.bit_count()) for e in range(1 << AMBIENT_DIM)
)
REDUCTION_DENOM = NUM_LAGRANGIAN_SUBSPACES * NUM_X * _ERROR_WEIGHT_SUM

ZERO_B_FAR_THRESHOLD = Fraction(9, 10)

LAGRANGIAN_BASES = enumerate_lagrangian_bases()


def _sd_for_B(B_cols: list[int], lpn_counts: list[int], lpn_denom: int) -> Fraction:
    red_counts = reduction_counts_for_B(B_cols, LAGRANGIAN_BASES, M)
    return exact_sd_counts(red_counts, REDUCTION_DENOM, lpn_counts, lpn_denom)


def check_zero_B_is_far():
    lpn_counts, lpn_denom = lpn_target_counts(M, LPN_NOISE)
    B_cols = [0] * AMBIENT_DIM
    sd = _sd_for_B(B_cols, lpn_counts, lpn_denom)
    assert sd > ZERO_B_FAR_THRESHOLD, f"zero-B SD unexpectedly small: {sd}"
    print(f"zero-B SD for m={M}: {sd} (OK)")


def check_bounds():
    lpn_counts, lpn_denom = lpn_target_counts(M, LPN_NOISE)
    min_sd = Fraction(1)
    max_sd = Fraction(0)
    mask = (1 << M) - 1
    for bits in range(1 << (AMBIENT_DIM * M)):
        B_cols = [(bits >> (j * M)) & mask for j in range(AMBIENT_DIM)]
        sd = _sd_for_B(B_cols, lpn_counts, lpn_denom)
        assert 0 <= sd <= 1
        if sd < min_sd:
            min_sd = sd
        if sd > max_sd:
            max_sd = sd
    print(f"m={M} SD bounds: [{min_sd}, {max_sd}] (OK)")


if __name__ == "__main__":
    check_zero_B_is_far()
    check_bounds()
