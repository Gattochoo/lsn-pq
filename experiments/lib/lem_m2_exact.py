"""Exact small-n helpers for lem:m2 noise-side enumeration."""
from fractions import Fraction


def symplectic_form(u: int, v: int) -> int:
    """Standard symplectic form on F_2^4: omega(u,v)."""
    return (
        ((u >> 0) & 1) * ((v >> 2) & 1)
        ^ ((u >> 1) & 1) * ((v >> 3) & 1)
        ^ ((u >> 2) & 1) * ((v >> 0) & 1)
        ^ ((u >> 3) & 1) * ((v >> 1) & 1)
    ) & 1


def enumerate_lagrangian_bases() -> list[tuple[int, int]]:
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


def apply_matrix(B_cols: list[int], x: int) -> int:
    """B * x over F_2; B_cols is list of m-bit column ints, x is 4-bit int."""
    y = 0
    for j, col in enumerate(B_cols):
        if (x >> j) & 1:
            y ^= col
    return y


def bernoulli_product(p: Fraction, m: int) -> dict[int, Fraction]:
    """Return dict {e_prime: probability} for Bernoulli(p)^m."""
    q = Fraction(1) - p
    dist = {}
    for v in range(1 << m):
        w = v.bit_count()
        dist[v] = (p ** w) * (q ** (m - w))
    return dist


def sd_to_product(dist: dict[int, Fraction], product_dist: dict[int, Fraction]) -> Fraction:
    """Exact SD between dict dist (sums to 1) and product_dist."""
    keys = set(dist.keys()) | set(product_dist.keys())
    total = Fraction(0)
    for k in keys:
        total += abs(Fraction(dist.get(k, 0)) - Fraction(product_dist.get(k, 0)))
    return total / 2


def lpn_target_counts(m: int, p: Fraction) -> tuple[list[int], int]:
    """Integer counts and denominator for LPN_p distribution over (C, y)."""
    mask = (1 << m) - 1
    num_C = 1 << (2 * m)
    num_y = 1 << m
    size = num_C * num_y
    counts = [0] * size
    D = p.denominator ** m
    total_denom = num_C * 4 * D
    for C_key in range(num_C):
        c0 = (C_key >> m) & mask
        c1 = C_key & mask
        for x in range(1 << 2):
            cx = 0
            if x & 1:
                cx ^= c0
            if x & 2:
                cx ^= c1
            for eprime in range(num_y):
                w = eprime.bit_count()
                num = (p.numerator ** w) * ((p.denominator - p.numerator) ** (m - w))
                y = cx ^ eprime
                key = (C_key << m) | y
                counts[key] += num
    return counts, total_denom


def reduction_counts_for_B(B_cols: list[int], bases: list[tuple[int, int]], m: int) -> list[int]:
    """Integer counts for reduction output (C, y) for a fixed B."""
    mask = (1 << m) - 1
    size = 1 << (3 * m)
    counts = [0] * size
    for a0, a1 in bases:
        c0 = apply_matrix(B_cols, a0) & mask
        c1 = apply_matrix(B_cols, a1) & mask
        C_key = (c0 << m) | c1
        for x in range(1 << 2):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):
                w = e.bit_count()
                v = a ^ e
                y = apply_matrix(B_cols, v) & mask
                key = (C_key << m) | y
                counts[key] += 3 ** (4 - w)
    return counts


def exact_sd_counts(counts1: list[int], denom1: int, counts2: list[int], denom2: int) -> Fraction:
    """Exact SD between two integer-count distributions with different denominators."""
    num = 0
    for c1, c2 in zip(counts1, counts2):
        num += abs(c1 * denom2 - c2 * denom1)
    return Fraction(num, 2 * denom1 * denom2)


def num_lagrangian_subspaces(n: int) -> int:
    """Number of Lagrangian subspaces of F_2^{2n}."""
    if n < 1:
        raise ValueError("n must be >= 1")
    total = 1
    for i in range(1, n + 1):
        total *= (2 ** i + 1)
    return total
