#!/usr/bin/env python3
"""184b: Independent sanity checks for 184 exact enumeration."""
from collections import Counter
from fractions import Fraction

from experiments.lib.lem_m2_exact import apply_matrix, enumerate_lagrangian_bases


N = 4  # number of bits/columns


def check_zero_B():
    """Check that the zero matrix maps every error to 0, aggregated over all bases."""
    B_cols = [0] * N
    eprime_counts = Counter()
    total = 0
    # Result must be independent of the Lagrangian basis, so aggregate over all bases.
    for _ in enumerate_lagrangian_bases():
        for e in range(1 << N):
            w = e.bit_count()
            weight = 3 ** (N - w)
            eprime = apply_matrix(B_cols, e)
            assert eprime == 0
            eprime_counts[eprime] += weight
            total += weight
    assert eprime_counts[0] == total
    print("zero-B sanity: OK")


def check_identity_B():
    """Check that the identity matrix preserves each error with Bernoulli(1/4)^N marginal."""
    B_cols = [1 << i for i in range(N)]  # identity columns
    eprime_counts = Counter()
    total = 0
    # Result must be independent of the Lagrangian basis, so aggregate over all bases.
    for _ in enumerate_lagrangian_bases():
        for e in range(1 << N):
            w = e.bit_count()
            weight = 3 ** (N - w)
            eprime = apply_matrix(B_cols, e)
            eprime_counts[eprime] += weight
            total += weight
    # each e maps to itself; marginal should equal Bernoulli(1/4)^N
    for e in range(1 << N):
        w = e.bit_count()
        expected = Fraction(3 ** (N - w), 1 << (2 * N))
        got = Fraction(eprime_counts[e], total)  # aggregated over 15 bases; total = 15*4**N
        assert got == expected, f"e={e}: got {got}, expected {expected}"
    print("identity-B sanity: OK")


if __name__ == "__main__":
    check_zero_B()
    check_identity_B()
