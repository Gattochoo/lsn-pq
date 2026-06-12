#!/usr/bin/env python3
"""184b: Independent sanity checks for 184 exact enumeration."""
from collections import Counter
from fractions import Fraction

from experiments.lib.lem_m2_exact import apply_matrix, enumerate_lagrangian_bases


def check_zero_B():
    m = 3
    B_cols = [0, 0, 0, 0]
    eprime_counts = Counter()
    total = 0
    for a0, a1 in enumerate_lagrangian_bases():
        for e in range(1 << 4):
            w = e.bit_count()
            weight = 3 ** (4 - w)
            eprime = apply_matrix(B_cols, e)
            assert eprime == 0
            eprime_counts[eprime] += weight
            total += weight
    assert eprime_counts[0] == total
    print("zero-B sanity: OK")


def check_identity_B():
    m = 4
    B_cols = [1, 2, 4, 8]  # identity columns
    eprime_counts = Counter()
    total = 0
    for a0, a1 in enumerate_lagrangian_bases():
        for e in range(1 << 4):
            w = e.bit_count()
            weight = 3 ** (4 - w)
            eprime = apply_matrix(B_cols, e)
            eprime_counts[eprime] += weight
            total += weight
    # each e maps to itself; marginal should equal Bernoulli(1/4)^4
    for e in range(1 << 4):
        w = e.bit_count()
        expected = Fraction(3 ** (4 - w), 256)
        got = Fraction(eprime_counts[e], total)  # aggregated over 15 bases; total = 15*256
        assert got == expected, f"e={e}: got {got}, expected {expected}"
    print("identity-B sanity: OK")


if __name__ == "__main__":
    check_zero_B()
    check_identity_B()
