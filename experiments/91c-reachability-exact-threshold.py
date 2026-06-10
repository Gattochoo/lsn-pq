"""
91c — Exact reachability threshold probe (§1b any-B counting theorem).

For a linear reduction making m' oracle queries, the output queries are
linear combinations of the m' input queries.  The set of reachable queries
using weight ≤ w is R_w, with |R_w| ≤ Σ_{j=0}^w C(m', j).

This probe finds the largest w such that this bound / 2^n ≤ 1/m'.
We compute log2(bound) exactly for small cases and via precise Stirling
for larger ones.
"""
import math
from math import comb

def log2_factorial(n):
    """Compute log2(n!) using exact values for small n, Stirling for large."""
    if n < 0:
        return float('-inf')
    if n <= 20:
        # Exact
        f = 1
        for i in range(2, n + 1):
            f *= i
        return math.log2(f) if f > 0 else 0.0
    # Stirling: log2(n!) ≈ n*log2(n/e) + log2(2πn)/2
    return n * math.log2(n / math.e) + 0.5 * math.log2(2 * math.pi * n)

def log2_comb_exact(D, j):
    """Exact log2(C(D,j)) using factorials."""
    if j < 0 or j > D:
        return float('-inf')
    if j == 0 or j == D:
        return 0.0
    return log2_factorial(D) - log2_factorial(j) - log2_factorial(D - j)

def log2_sum_comb(D, w):
    """Compute log2(Σ_{j=0}^w C(D,j)) exactly for small D, approximate for large."""
    if w < 0:
        return float('-inf')
    if w >= D:
        return D  # Σ_{j=0}^D C(D,j) = 2^D
    
    if D <= 200:
        # Direct summation in log-space
        total = 0.0
        for j in range(w + 1):
            c = comb(D, j)
            total += c
        return math.log2(total) if total > 0 else float('-inf')
    
    # For large D, find the maximum term and approximate the sum
    # The sum is at most (w+1) * max_term
    j_max = min(w, D // 2)
    log_max = log2_comb_exact(D, j_max)
    # Sum is roughly max_term * (1 + terms_before/ max + terms_after/max)
    # For w <= D/2, terms increase up to j_max, so sum <= (w+1) * C(D, j_max)
    # But for a better estimate, use the fact that the binomial tail can be bounded
    # We'll use: log2(sum) <= log_max + log2(w+1) as a safe upper bound
    return log_max + math.log2(w + 1)

def find_threshold(m_prime, n, target):
    """Find largest w such that Rw_bound(m', w) / 2^n ≤ target."""
    log_target = math.log2(target)
    lo, hi = 0, min(m_prime, 2 * n)  # w > 2n is not interesting
    best_w = 0
    best_ratio = float('inf')
    while lo <= hi:
        mid = (lo + hi) // 2
        log_bound = log2_sum_comb(m_prime, mid)
        log_ratio = log_bound - n
        if log_ratio <= log_target:
            best_w = mid
            best_ratio = 2 ** log_ratio if log_ratio > -1000 else 0.0
            lo = mid + 1
        else:
            hi = mid - 1
    return best_w, best_ratio

def main():
    print("Exact threshold table: largest w such that |R_w|/2^n ≤ 1/m'")
    print("(m' = number of oracle queries the reduction makes)")
    print()
    
    for n in [8, 16, 32, 64]:
        print(f"n={n}:")
        for c in [1, 2, 3, 4]:
            m_prime = n ** c
            target = 1.0 / m_prime
            w, ratio = find_threshold(m_prime, n, target)
            bias = (0.5) ** w
            m_lb = n / (bias ** 2) if bias > 0 else float('inf')
            log_m = math.log2(m_lb) if 0 < m_lb < float('inf') else (0 if m_lb == 0 else float('inf'))
            m_lb_str = f"2^{log_m:.1f}" if log_m != float('inf') else "∞"
            print(f"  m'=n^{c}={m_prime:>10}: w={w:>3}, ratio≤{ratio:.2e}, "
                  f"bias=2^{math.log2(bias):>7.2f}, m_lb={m_lb_str}")
        print()
    
    print("--- Detailed: n=64, varying m' ---")
    n = 64
    for m_prime in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536,
                     131072, 262144, 524288, 1048576]:
        target = 1.0 / m_prime
        w, ratio = find_threshold(m_prime, n, target)
        bias = (0.5) ** w
        m_lb = n / (bias ** 2) if bias > 0 else float('inf')
        log_m = math.log2(m_lb) if 0 < m_lb < float('inf') else float('inf')
        m_lb_str = f"2^{log_m:.1f}" if log_m != float('inf') else "∞"
        print(f"m'={m_prime:>8}: w={w:>3}, ratio≤{ratio:.2e}, "
              f"bias=2^{math.log2(bias):>7.2f}, m_lb={m_lb_str}")

if __name__ == "__main__":
    main()
