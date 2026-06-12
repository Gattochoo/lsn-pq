"""Exact small-n helpers for lem:m2 noise-side enumeration."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product


def symplectic_form(u: int, v: int) -> int:
    """Standard symplectic form on F_2^4: omega(u,v)."""
    return (
        ((u >> 0) & 1) * ((v >> 2) & 1)
        ^ ((u >> 1) & 1) * ((v >> 3) & 1)
        ^ ((u >> 2) & 1) * ((v >> 0) & 1)
        ^ ((u >> 3) & 1) * ((v >> 1) & 1)
    ) & 1


def enumerate_lagrangian_bases():
    """Return list of Lagrangian subspaces of F_2^4 as (col0,col1) basis pairs."""
    subspaces = {}
    for v1 in range(1, 1 << 4):
        for v2 in range(v1 + 1, 1 << 4):
            if symplectic_form(v1, v2) != 0:
                continue
            span = frozenset({0, v1, v2, v1 ^ v2})
            canon = tuple(sorted([v1, v2]))
            subspaces.setdefault(span, canon)
    return [c for _, c in sorted(subspaces.items())]


def apply_matrix(B_cols, x):
    """B * x over F_2; B_cols is list of m-bit column ints, x is 4-bit int."""
    y = 0
    for j, col in enumerate(B_cols):
        if (x >> j) & 1:
            y ^= col
    return y


def bernoulli_product(p: Fraction, m: int):
    """Return dict {e_prime: probability} for Bernoulli(p)^m."""
    q = Fraction(1) - p
    dist = {}
    for v in range(1 << m):
        w = v.bit_count()
        dist[v] = (p ** w) * (q ** (m - w))
    return dist


def sd_to_product(dist, product_dist):
    """Exact SD between dict dist (sums to 1) and product_dist."""
    keys = set(dist.keys()) | set(product_dist.keys())
    total = Fraction(0)
    for k in keys:
        total += abs(Fraction(dist.get(k, 0)) - Fraction(product_dist.get(k, 0)))
    return total / 2
