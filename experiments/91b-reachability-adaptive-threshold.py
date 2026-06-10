"""
91b — Adaptive reachability threshold probe (§1b any-B counting theorem).

In a linear reduction making m' oracle queries, the output query c_i' is a
linear combination of the m' input queries.  If the reduction wants c_i' to be
uniform in F2^n, and only low-weight combinations (|b_i| ≤ w) are used, then
c_i' must lie in R_w = {Σ_j b_j c_j' : |b| ≤ w}.

For fixed input queries c_j' spanning F2^n, |R_w| ≤ Σ_{j≤w} C(m', j).
If |R_w|/2^n ≪ 1/m, then uniformity forces w.h.p. |b_i| > w for all i.

Probe: for varying m', n, find the largest w such that |R_w|/2^n ≤ 1/m'.
Then compute the resulting effective noise bias = (1-2p)^w for p=1/4,
and the recovery lower bound m ≥ n / bias^2.

Output: threshold table showing super-polynomial lower bound for all poly(m').
"""
import math

def log2_C_approx(D, j):
    """Approximate log2(C(D,j)) using Stirling."""
    if j < 0 or j > D:
        return float('-inf')
    if j == 0 or j == D:
        return 0.0
    if j == 1 or j == D - 1:
        return math.log2(D)
    # Stirling: log2(C(D,j)) ≈ D*H(j/D) - 0.5*log2(2π*j*(1-j/D))
    p = j / D
    h = -(p * math.log2(p) + (1 - p) * math.log2(1 - p)) if 0 < p < 1 else 0
    denom = 2 * math.pi * j * (1 - p)
    correction = 0.5 * math.log2(denom) if denom > 0 else 0
    return D * h - correction

def log2_sum_C(D, w):
    """Approximate log2(Σ_{j=0}^w C(D,j)).  Uses max term + small correction."""
    if w < 0:
        return float('-inf')
    if w >= D:
        return D
    # Find j* in [0,w] that maximizes C(D,j)
    j_star = min(w, D // 2)
    log_max = log2_C_approx(D, j_star)
    # Sum is at most (w+1) * max, at least max
    # log2(sum) ≈ log_max + log2(w+1) for crude upper bound
    # But for w << D/2, the sum is dominated by the last few terms
    # We'll use: log2(sum) ≤ log_max + log2(w+1)
    return log_max + math.log2(w + 1)

def find_threshold(m_prime, n, target):
    """Find largest w such that Rw_bound(m', w) / 2^n ≤ target."""
    log_target = math.log2(target)
    lo, hi = 0, m_prime
    best_w = 0
    best_ratio = float('inf')
    while lo <= hi:
        mid = (lo + hi) // 2
        log_bound = log2_sum_C(m_prime, mid)
        log_ratio = log_bound - n
        if log_ratio <= log_target:
            best_w = mid
            best_ratio = 2 ** log_ratio
            lo = mid + 1
        else:
            hi = mid - 1
    return best_w, best_ratio

def main():
    print("Threshold table: largest w such that |R_w|/2^n ≤ 1/m'")
    print("Format: for each (n, m'=n^c), shows w, ratio, bias=(1/2)^w, m_lb=n/bias^2")
    
    for n in [8, 16, 32, 64, 128]:
        print(f"\nn={n}:")
        for c in [1, 2, 3, 4, 5]:
            m_prime = n ** c
            target = 1.0 / m_prime
            w, ratio = find_threshold(m_prime, n, target)
            bias = (0.5) ** w
            m_lb = n / (bias ** 2) if bias > 0 else float('inf')
            if m_lb > 1e300 or m_lb == float('inf'):
                m_lb_str = "∞"
            else:
                log_m = math.log2(m_lb) if m_lb > 0 else 0
                m_lb_str = f"2^{log_m:.1f}"
            print(f"  c={c} (m'={m_prime}): w={w:>3}, ratio≤{ratio:.2e}, bias=2^{math.log2(bias):>7.2f}, m_lb={m_lb_str}")
    
    print("\n--- Detailed: n=64, varying m' ---")
    n = 64
    for m_prime in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]:
        target = 1.0 / m_prime
        w, ratio = find_threshold(m_prime, n, target)
        bias = (0.5) ** w
        m_lb = n / (bias ** 2) if bias > 0 else float('inf')
        if m_lb > 1e300 or m_lb == float('inf'):
            m_lb_str = "∞"
        else:
            log_m = math.log2(m_lb)
            m_lb_str = f"2^{log_m:.1f}"
        print(f"m'={m_prime:>6}: w={w:>3}, ratio≤{ratio:.2e}, bias=2^{math.log2(bias):>7.2f}, m_lb={m_lb_str}")

if __name__ == "__main__":
    main()
