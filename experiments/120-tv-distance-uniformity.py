#!/usr/bin/env python3
"""
E-OP9e part 2: TV distance between BA distribution and uniform for n=4,5.

For n=4:
  - Exact enumeration for w=1,2 (feasible: 8^4=4096, 28^4=614K)
  - Sampling for w=3,4
For n=5:
  - Sampling for all w

TV(P, Uniform) = (1/2) * sum_C |P(C) - 2^{-n^2}|
"""

import random
import math
from collections import Counter
from itertools import product, combinations

def all_weight_w_vectors(n2, w):
    """Generate all vectors in F_2^{n2} with weight w."""
    return [sum(1 << b for b in comb) for comb in combinations(range(n2), w)]

def C_from_B_rows(B_rows, n):
    """C[i] = bottom-n bits of B_rows[i], as int."""
    return [(row >> n) & ((1 << n) - 1) for row in B_rows]

def C_to_int(C_rows, n):
    """Flatten n rows of n bits each into a single n^2-bit int."""
    val = 0
    for i, row in enumerate(C_rows):
        val |= row << (i * n)
    return val

def tv_distance_exact(n, w):
    """Exact TV distance by enumerating all B matrices."""
    n2 = 2 * n
    rows_pool = all_weight_w_vectors(n2, w)
    total_B = len(rows_pool) ** n
    
    freq = Counter()
    for B_rows in product(rows_pool, repeat=n):
        C_rows = C_from_B_rows(B_rows, n)
        c_int = C_to_int(C_rows, n)
        freq[c_int] += 1
    
    total_C = 1 << (n * n)
    tv = 0.0
    for c_int, count in freq.items():
        p = count / total_B
        tv += abs(p - 1.0 / total_C)
    # Unobserved C matrices
    unobserved = total_C - len(freq)
    tv += unobserved * (1.0 / total_C)
    tv *= 0.5
    
    return tv, len(freq), total_C, total_B

def tv_distance_sample(n, w, num_samples):
    """Estimate TV distance by sampling."""
    n2 = 2 * n
    freq = Counter()
    
    for _ in range(num_samples):
        bits_pool = list(range(n2))
        B_rows = []
        for _ in range(n):
            bits = random.sample(bits_pool, w)
            v = sum(1 << b for b in bits)
            B_rows.append(v)
        C_rows = C_from_B_rows(B_rows, n)
        c_int = C_to_int(C_rows, n)
        freq[c_int] += 1
    
    total_C = 1 << (n * n)
    tv = 0.0
    for c_int, count in freq.items():
        p = count / num_samples
        tv += abs(p - 1.0 / total_C)
    # Unobserved: we don't know their exact empirical prob, but we can lower-bound TV
    # by assuming they have p=0 in the sample
    unobserved = total_C - len(freq)
    tv += unobserved * (1.0 / total_C)
    tv *= 0.5
    
    # Also compute an upper bound by adding the missing mass
    observed_mass = sum(freq.values()) / num_samples
    # Actually observed_mass = 1 by definition
    # The sampling error is hard to bound exactly, so we report the plug-in estimate
    return tv, len(freq), total_C

if __name__ == "__main__":
    print("TV distance between BA distribution and uniform random matrix")
    print("=" * 60)
    
    # n=4 exact for w=1,2
    n = 4
    for w in [1, 2]:
        print(f"\nn={n}, w={w} (exact enumeration)...")
        tv, num_distinct, total_C, total_B = tv_distance_exact(n, w)
        print(f"  TV distance = {tv:.6f}")
        print(f"  Distinct C observed = {num_distinct} / {total_C}")
        print(f"  Total B matrices = {total_B}")
    
    # n=4 sampling for w=3,4
    for w in [3, 4]:
        print(f"\nn={n}, w={w} (sampling 2M)...")
        tv, num_distinct, total_C = tv_distance_sample(n, w, 2_000_000)
        print(f"  TV distance (plug-in) = {tv:.6f}")
        print(f"  Distinct C observed = {num_distinct} / {total_C}")
    
    # n=5 sampling for representative w
    n = 5
    for w in [1, 2, 3, 5, 10]:
        print(f"\nn={n}, w={w} (sampling 5M)...")
        tv, num_distinct, total_C = tv_distance_sample(n, w, 5_000_000)
        print(f"  TV distance (plug-in) = {tv:.6f}")
        print(f"  Distinct C observed = {num_distinct} / {total_C}")
