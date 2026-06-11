#!/usr/bin/env python3
"""
Experiment 170: lem:m2 Step A — Noise side, single row, public B.

Compute exact statistical distance SD(mu_row, Bernoulli(1/2)^n).

mu_row = (1/(2^n+1)) * delta_0 + (2^n/(2^n+1)) * Unif(F_2^n \\{0\\})
nu = Bernoulli(1/2)^n = Unif(F_2^n) = (1/2^n) * delta_0 + ((2^n-1)/2^n) * Unif(F_2^n \\{0\\})

Track A Step A1 per DIRECTIVE-KIMI-v3-frontier.md and adjudication 1dbfee8.
"""

from fractions import Fraction

def sd_single_row(n):
    """Compute SD(mu_row, Bernoulli(1/2)^n) exactly."""
    # x = 0:
    mu_0 = Fraction(1, 2**n + 1)
    nu_0 = Fraction(1, 2**n)
    diff_0 = abs(mu_0 - nu_0)
    
    # x != 0:
    mu_nonzero = Fraction(2**n, (2**n + 1) * (2**n - 1))
    nu_nonzero = Fraction(1, 2**n)
    diff_nonzero = abs(mu_nonzero - nu_nonzero)
    
    sd = Fraction(1, 2) * (diff_0 + (2**n - 1) * diff_nonzero)
    return sd

def sd_closed_form(n):
    """Closed form: SD = 1 / (2^n * (2^n + 1)) = 1 / (2^{2n} + 2^n)."""
    return Fraction(1, (2**n) * (2**n + 1))

print("lem:m2 Step A1: SD(mu_row, Bernoulli(1/2)^n)")
print("=" * 50)

for n in range(2, 9):
    sd1 = sd_single_row(n)
    sd2 = sd_closed_form(n)
    assert sd1 == sd2, f"Mismatch at n={n}: {sd1} != {sd2}"
    print(f"n={n}: SD = {sd1} = {float(sd1):.10f}")

print("\n" + "=" * 50)
print("Closed form: SD = 1 / (2^n * (2^n + 1)) = O(4^{-n})")
print("=" * 50)

# Batch bound via union bound / data processing inequality
print("\nBatch (2n rows) upper bound via union bound:")
for n in range(2, 9):
    batch_sd_bound = Fraction(2 * n, (2**n) * (2**n + 1))
    print(f"n={n}: SD_batch <= 2n * SD_single = {batch_sd_bound} = {float(batch_sd_bound):.10f}")

print("\nBatch SD is O(n * 4^{-n}) — still negligible in n.")
