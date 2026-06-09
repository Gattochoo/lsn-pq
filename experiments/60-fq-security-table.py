#!/usr/bin/env python3
"""
A1: Recompute F_q security table with corrected formula.
Uses the exact correlation formula with noise-only D_0 base.
"""

import math

def q_binomial(n, k, q):
    if k < 0 or k > n: return 0
    if k == 0: return 1
    num = den = 1
    for i in range(k):
        num *= (q**(n-i) - 1)
        den *= (q**(k-i) - 1)
    return num // den

def lagr_count(n, q):
    total = 1
    for i in range(1, n+1):
        total *= (q**i + 1)
    return total

def compute_constants(n, q, p):
    N = lagr_count(n, q)
    distinct = N - 1
    E = 0
    for j in range(n+1):
        Nj = q_binomial(n, j, q) * q**((n-j)*(n-j+1)//2)
        prob = Nj / N  # Use N, not distinct, for E[q^j] over ALL Lagrangians including self
        E += prob * (q**j)
    
    eps = 1 - 2*p
    # Corrected formula: rho = eps^2 * E / (p*(1-p) * q^(2n))
    rho = (eps**2) * E / (p * (1-p) * q**(2*n))
    # SDA = q^(2n), q_min = SDA / 3 = q^(2n) / 3
    qmin = q**(2*n) / 3
    
    # Bit security: log_2(q_min)
    bit_security = math.log2(qmin)
    
    return E, rho, qmin, bit_security

def find_n_for_security(target_bits, q, p=0.25):
    """Find minimum n such that bit_security >= target_bits."""
    for n in range(1, 200):
        _, _, _, bits = compute_constants(n, q, p)
        if bits >= target_bits:
            return n, bits
    return None, None

print("=" * 80)
print("F_q SECURITY TABLE (corrected formula with D_0 base)")
print("=" * 80)
print(f"Formula: q_min = q^(2n) / 3,  bit_security = log_2(q_min) = 2n*log_2(q) - log_2(3)")
print()

p = 0.25
qs = [2, 3, 5, 7]
security_levels = [80, 128, 192, 256]

# Header
header = "| Security |"
for q in qs:
    header += f" F_{q}: n (bits) |"
print(header)
print("|" + "-" * 10 + "|" + "".join(f"{'-' * 15}|" for _ in qs))

for lam in security_levels:
    row = f"| {lam}-bit   |"
    for q in qs:
        n, bits = find_n_for_security(lam, q, p)
        row += f" {n:3d} ({bits:.1f}) |"
    print(row)

print()
print("Verification for q=2 (should match K3 n=41/65):")
for n in [40, 41, 42, 64, 65, 66]:
    E, rho, qmin, bits = compute_constants(n, 2, p)
    print(f"  n={n:3d}: E[2^j]={E:.4f}, log2(q_min)={bits:.2f}")

print()
print("Verification for q=3,5,7 (sample n values):")
for q in [3, 5, 7]:
    print(f"  q={q}:")
    for n in [20, 25, 30, 40]:
        E, rho, qmin, bits = compute_constants(n, q, p)
        print(f"    n={n:3d}: E[{q}^j]={E:.4f}, log2(q_min)={bits:.2f}")
