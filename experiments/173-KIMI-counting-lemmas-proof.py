#!/usr/bin/env python3
"""173: Verification of counting lemmas against exact enumeration data.

Cross-checks the closed-form expressions from 173-KIMI-counting-lemmas-proof.md
against the exact orbit counts from 172-CLAUDE-mj-closed-form-fit.json.

Status: verification script. If all assertions pass, the lemmas are data-verified.
"""
import json
from fractions import Fraction
from math import comb

# Load the exact enumeration data
with open("experiments/172-CLAUDE-mj-closed-form-fit.json") as f:
    data = json.load(f)

print("=" * 60)
print("Verification of Counting Lemmas (173)")
print("=" * 60)

all_ok = True

for n in (2, 3, 4, 5, 6):
    u = 1 << (2 * n - 2)
    orbit = data["orbit_data"][str(n)]
    P = int(orbit["P"])

    # Lemma 1: q_sym2 = u(u-1)/2
    q_sym2_formula = Fraction(u * (u - 1), 2)
    q_sym2_data = Fraction(orbit["q_sym2"])
    ok1 = q_sym2_formula == q_sym2_data
    all_ok &= ok1
    print(f"n={n}: q_sym2 = {q_sym2_formula} == {q_sym2_data} ? {ok1}")

    # Lemma 2: q_gen2 = u(u-2)/2
    q_gen2_formula = Fraction(u * (u - 2), 2)
    q_gen2_data = Fraction(orbit["q_gen2"])
    ok2 = q_gen2_formula == q_gen2_data
    all_ok &= ok2
    print(f"n={n}: q_gen2 = {q_gen2_formula} == {q_gen2_data} ? {ok2}")

    # Lemma 3: q_sym3 = q_gen3 = u(u-4)/8
    q3_formula = Fraction(u * (u - 4), 8)
    q_sym3_data = Fraction(orbit["q_sym3"]) if orbit["q_sym3"] != "None" else None
    q_gen3_data = Fraction(orbit["q_gen3"]) if orbit["q_gen3"] != "None" else None

    if q_sym3_data is not None:
        ok3a = q3_formula == q_sym3_data
        all_ok &= ok3a
        print(f"n={n}: q_sym3 = {q3_formula} == {q_sym3_data} ? {ok3a}")
    else:
        print(f"n={n}: q_sym3 = None (n=2, expected)")

    if q_gen3_data is not None:
        ok3b = q3_formula == q_gen3_data
        all_ok &= ok3b
        print(f"n={n}: q_gen3 = {q3_formula} == {q_gen3_data} ? {ok3b}")
    else:
        print(f"n={n}: q_gen3 = None (n=2, expected)")

    # Verify closed-form m2, m3 against data
    N = 2 * n
    P_frac = Fraction((2 ** N - 1) * (2 ** (N - 1) - 2))
    n_sym2, n_gen2 = n, comb(N, 2) - n
    n_sym3, n_gen3 = n * (N - 2), 8 * comb(n, 3)

    m2_formula = (n_sym2 * q_sym2_formula + n_gen2 * q_gen2_formula) / (comb(N, 2) * P_frac)
    m3_formula = (n_sym3 * q3_formula + n_gen3 * q3_formula) / (comb(N, 3) * P_frac) if N >= 3 else Fraction(0)

    # Compute from data
    m2_data = (n_sym2 * q_sym2_data + n_gen2 * q_gen2_data) / (comb(N, 2) * P_frac)
    m3_data = (n_sym3 * (q_sym3_data or 0) + n_gen3 * (q_gen3_data or 0)) / (comb(N, 3) * P_frac) if N >= 3 else Fraction(0)

    ok_m2 = m2_formula == m2_data
    ok_m3 = m3_formula == m3_data
    all_ok &= ok_m2
    all_ok &= ok_m3
    print(f"n={n}: m2 formula == data ? {ok_m2} ({m2_formula})")
    print(f"n={n}: m3 formula == data ? {ok_m3} ({m3_formula})")
    print("-" * 40)

# Blind n=7 check
n = 7
u = 1 << (2 * n - 2)
q_sym2 = Fraction(u * (u - 1), 2)
q_gen2 = Fraction(u * (u - 2), 2)
q3 = Fraction(u * (u - 4), 8)
N = 14
P = Fraction((2 ** N - 1) * (2 ** (N - 1) - 2))
m2_pred = (n * q_sym2 + (comb(N, 2) - n) * q_gen2) / (comb(N, 2) * P)
m3_pred = q3 / P  # both 3-orbits equal -> orbit-independent

blind = data["blind_n7"]
ok_m7 = m2_pred == Fraction(blind["m2_enumerated"]) and m3_pred == Fraction(blind["m3_enumerated"])
all_ok &= ok_m7
print(f"n=7 blind: m2={m2_pred}, m3={m3_pred}")
print(f"n=7 blind match ? {ok_m7}")
print("=" * 60)
print(f"ALL VERIFICATIONS PASSED: {all_ok}")
