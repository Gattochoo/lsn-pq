"""
91d — Reachability threshold probe for output dimension 2n.

In symplectic LPN, the secret z ∈ F2^{2n} and queries s ∈ F2^{2n}.
A linear reduction to standard LPN outputs queries c_i ∈ F2^{2n}.
If the reduction makes m' oracle queries and uses row weight w_i,
the output query lies in R_w = {Σ_j b_j s_j : |b| ≤ w}.

|R_w| ≤ Σ_{j=0}^w C(m', j).  For uniform output in F2^{2n}, we need
|R_w| / 2^{2n} to be non-negligible.  This probe finds the threshold w
where |R_w| ≈ 2^{2n}.
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

def find_threshold(m_prime, dim, target):
    """Find largest w such that log2_sum_comb(m', w) - dim <= log2(target)."""
    log_target = math.log2(target)
    lo, hi = 0, min(m_prime, 2 * dim)
    best_w = 0
    best_ratio = float('inf')
    while lo <= hi:
        mid = (lo + hi) // 2
        log_bound = log2_sum_comb(m_prime, mid)
        log_ratio = log_bound - dim
        if log_ratio <= log_target:
            best_w = mid
            best_ratio = 2 ** log_ratio if log_ratio > -1000 else 0.0
            lo = mid + 1
        else:
            hi = mid - 1
    return best_w, best_ratio

def main():
    print("Threshold for uniform output in F2^{2n}:")
    print("Find largest w such that |R_w| / 2^{2n} ≤ 1/m'")
    print()
    
    for n in [8, 16, 32, 64, 128]:
        dim = 2 * n
        print(f"n={n}, dim=2n={dim}:")
        for c in [1, 2, 3, 4, 5]:
            m_prime = n ** c
            target = 1.0 / m_prime
            w, ratio = find_threshold(m_prime, dim, target)
            bias = (0.5) ** w
            m_lb = dim / (bias ** 2) if bias > 0 else float('inf')
            log_m = math.log2(m_lb) if 0 < m_lb < float('inf') else float('inf')
            m_lb_str = f"2^{log_m:.1f}" if log_m != float('inf') else "∞"
            print(f"  m'=n^{c}={m_prime:>12}: w={w:>4}, ratio≤{ratio:.2e}, "
                  f"bias=2^{math.log2(bias):>8.2f}, m_lb={m_lb_str}")
        print()

if __name__ == "__main__":
    main()
