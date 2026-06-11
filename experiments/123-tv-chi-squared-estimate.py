#!/usr/bin/env python3
"""
TV distance precise estimation via chi-squared divergence.

For C = B'M with i.i.d. weight-n rows, the chi-squared divergence from uniform is:
  chi^2 = (sum_d C(n,d) * phi_n(d)^2)^n - 1
where phi_n(d) = K_n(d; 2n) / C(2n, n).

TV lower bounds:
  (a) TV >= (1/2) * sqrt(chi^2 / (1 + chi^2))   [Le-Cam type]
  (b) TV >= max_{d>=1} |phi_n(d)| / 2            [single linear test]
"""

import math

def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)

def krawtchouk(w, d, N):
    s = 0
    for j in range(0, min(d, w) + 1):
        s += ((-1)**j) * nCr(d, j) * nCr(N - d, w - j)
    return s

def analyze(n, w):
    N = 2 * n
    Cn_w = nCr(N, w)
    
    S = 0.0  # sum_d C(n,d) * phi(d)^2
    max_phi = 0.0
    details = []
    
    for d in range(0, n + 1):
        K = krawtchouk(w, d, N)
        phi = K / Cn_w
        f = phi ** 2
        count = nCr(n, d)
        contrib = count * f
        S += contrib
        if d >= 1:
            max_phi = max(max_phi, abs(phi))
        if d <= 6 or d == n or abs(phi) > 0.001:
            details.append((d, K, phi, count, contrib))
    
    chi_sq = S ** n - 1
    tv_le_cam = 0.5 * math.sqrt(chi_sq / (1 + chi_sq)) if chi_sq > 0 else 0
    tv_single = max_phi / 2
    
    return {
        'n': n,
        'w': w,
        'S': S,
        'chi_sq': chi_sq,
        'tv_le_cam': tv_le_cam,
        'tv_single': tv_single,
        'details': details,
    }

print(f"{'n':>3} {'w':>3} {'S':>10} {'chi^2':>12} {'TV>=LeCam':>10} {'TV>=single':>10}")
print("-" * 60)

results = []
for n in range(2, 31):
    w = n
    res = analyze(n, w)
    results.append(res)
    print(f"{n:>3} {w:>3} {res['S']:>10.6f} {res['chi_sq']:>12.4f} {res['tv_le_cam']:>10.4f} {res['tv_single']:>10.4f}")

# Print details for selected n
for n in [4, 6, 8, 10, 15, 20, 25, 30]:
    res = results[n-2]
    print(f"\nn={n}, w={n}: S={res['S']:.6f}, chi^2={res['chi_sq']:.2f}")
    print(f"  d<=6 or d=n or |phi|>0.001:")
    for d, K, phi, count, contrib in res['details']:
        print(f"    d={d:2d}: phi={phi:10.6f}, C(n,d)={count:6d}, contrib={contrib:.6f}")
