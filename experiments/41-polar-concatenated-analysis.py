#!/usr/bin/env python3
"""
P0-fix: Concatenated Polar Code Analysis
Inner: Repetition code (length r)
Outer: Polar code (N=2048, K=256)
Effective BSC: p' = Pr[majority of r bits wrong | p=1/4]
"""

import numpy as np
import math
from math import comb

def majority_error_prob(p, r):
    """Pr[majority of r i.i.d. Bernoulli(p) bits is wrong]."""
    # Majority is wrong if more than r/2 errors
    threshold = r // 2 + 1
    prob = sum(comb(r, k) * (p ** k) * ((1-p) ** (r-k)) for k in range(threshold, r+1))
    return prob

def polarize_bec(z0, n):
    z_all = np.full(1, z0, dtype=np.float64)
    for _ in range(n):
        z_minus = 2 * z_all - z_all ** 2
        z_plus = z_all ** 2
        z_all = np.concatenate([z_minus, z_plus])
    return z_all

p = 0.25
N = 2048
K = 256
n_levels = 11

print("=" * 60)
print("CONCATENATED POLAR CODE ANALYSIS")
print("=" * 60)
print(f"Base noise: p = {p}")
print(f"Outer polar: N = {N}, K = {K}, R = {K/N}")
print()

for r in [3, 5, 7, 9, 11]:
    p_prime = majority_error_prob(p, r)
    z0_prime = 2 * math.sqrt(p_prime * (1 - p_prime))
    c_prime = 1 - (-p_prime * math.log2(p_prime) - (1-p_prime) * math.log2(1-p_prime)) if 0 < p_prime < 1 else 1
    
    z_all = polarize_bec(z0_prime, n_levels)
    info_set = np.argsort(z_all)[:K]
    z_info = z_all[info_set]
    
    sc_bound = np.sum(z_info) / 2
    scl_est = sc_bound / (2 ** 8)  # SCL L=8 heuristic
    
    samples_needed = N * r
    
    print(f"r = {r:2d}:  p' = {p_prime:.4f},  Z0' = {z0_prime:.4f},  C' = {c_prime:.4f}")
    print(f"       SC bound: {sc_bound:.2e} (log2={math.log2(sc_bound):.1f})")
    print(f"       SCL est:  {scl_est:.2e} (log2={math.log2(scl_est):.1f})")
    print(f"       Samples:  {samples_needed}")
    if scl_est < 2 ** (-128):
        print(f"       >>> SUFFICIENT for 128-bit security <<<")
    elif scl_est < 2 ** (-80):
        print(f"       >>> SUFFICIENT for 80-bit security <<<")
    print()
