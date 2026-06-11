#!/usr/bin/env python3
"""Check if Var/E^2 * (81/50)^n converges to a constant."""

print(f"{'n':>3} {'V/E²':>10} {'(50/81)^n':>12} {'V/E²*(81/50)^n':>16}")
print("-" * 50)
for n in range(2, 21):
    p = 1.0 / (2**n + 1)
    q = 1.0 / ((2**(n-1) + 1) * (2**n + 1))
    
    D = (5/4)**(2*n) - 1
    T = ((3/2)**(2*n) - 1)**2 - D
    C_full = (7/4)**(2*n) - 2*(3/2)**(2*n) + 1 - D
    S_0 = (T + C_full) / 2
    
    diagonal = p * (1 - p) * D
    offdiag = q * S_0 - p * p * T
    var = diagonal + offdiag
    
    mean = 1.0 + p * ((3/2)**(2*n) - 1)
    ratio = var / (mean ** 2)
    
    scaled = ratio * ((81/50)**n)
    bound = (50/81)**n
    
    print(f"{n:>3} {ratio:>10.6f} {bound:>12.6f} {scaled:>16.4f}")
