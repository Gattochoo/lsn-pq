"""
91e — Uniform-output barrier via reachability counting.

Core argument: Symplectic LPN oracle queries are isotropic (constrained),
not uniform in F2^{2n}.  A linear reduction outputs c_i = Σ_j b_{ij} s_j.
If output queries are uniform in F2^{2n}, they must be reachable by many b.
The set R_w = {Σ_j b_j s_j : |b| ≤ w} has |R_w| ≤ Σ_{j≤w} C(m',j).
For |R_w| / 2^{2n} to be non-negligible, w must be large.

This probe computes the minimum w such that |R_w| ≥ 2^{2n} / poly(n),
showing w = Θ(n / log n) for m' = poly(n).  The resulting noise bias
and recovery lower bound are super-polynomial.
"""
import math

def log2_factorial(n):
    if n < 0:
        return float('-inf')
    if n <= 20:
        f = 1
        for i in range(2, n + 1):
            f *= i
        return math.log2(f) if f > 0 else 0.0
    return n * math.log2(n / math.e) + 0.5 * math.log2(2 * math.pi * n)

def log2_comb(D, j):
    if j < 0 or j > D:
        return float('-inf')
    if j == 0 or j == D:
        return 0.0
    return log2_factorial(D) - log2_factorial(j) - log2_factorial(D - j)

def log2_sum_comb(D, w):
    if w < 0:
        return float('-inf')
    if w >= D:
        return D
    if D <= 200:
        from math import comb
        total = sum(comb(D, j) for j in range(w + 1))
        return math.log2(total) if total > 0 else float('-inf')
    j_max = min(w, D // 2)
    log_max = log2_comb(D, j_max)
    return log_max + math.log2(w + 1)

def find_min_w_for_coverage(m_prime, dim, fraction):
    """Find minimum w such that |R_w| / 2^{dim} >= fraction."""
    target = fraction
    log_target = math.log2(target)
    for w in range(dim + 1):
        log_bound = log2_sum_comb(m_prime, w)
        log_ratio = log_bound - dim
        if log_ratio >= log_target:
            return w, 2 ** log_ratio if log_ratio > -1000 else 0.0
    return m_prime, 1.0

def main():
    print("Minimum w for |R_w| / 2^{2n} ≥ 1/m' (non-negligible coverage)")
    print("Format: w_min, coverage_ratio, bias=(1/2)^w, recovery_m_lb")
    print()
    
    for n in [8, 16, 32, 64, 128]:
        dim = 2 * n
        print(f"n={n}, dim={dim}:")
        for c in [1, 2, 3, 4, 5]:
            m_prime = n ** c
            target = 1.0 / m_prime
            w, ratio = find_min_w_for_coverage(m_prime, dim, target)
            bias = (0.5) ** w
            m_lb = dim / (bias ** 2) if bias > 0 else float('inf')
            log_m = math.log2(m_lb) if 0 < m_lb < float('inf') else float('inf')
            m_lb_str = f"2^{log_m:.1f}" if log_m != float('inf') else "∞"
            print(f"  m'=n^{c}={m_prime:>12}: w_min={w:>4}, coverage={ratio:.2e}, "
                  f"bias=2^{math.log2(bias):>8.2f}, m_lb={m_lb_str}")
        print()
    
    print("--- Asymptotic trend for n=64 ---")
    n = 64
    dim = 128
    for c in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        m_prime = n ** c
        target = 1.0 / m_prime
        w, ratio = find_min_w_for_coverage(m_prime, dim, target)
        bias = (0.5) ** w
        print(f"c={c:>2} (m'={m_prime:>15}): w={w:>4}, bias=2^{math.log2(bias):>8.2f}")

if __name__ == "__main__":
    main()
