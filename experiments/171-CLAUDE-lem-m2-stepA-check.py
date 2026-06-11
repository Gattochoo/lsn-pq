#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""171: CLAUDE adjudication of Kimi's lem:m2 Step A comprehensive report (503c89c).

Two independent checks:

(A) Correlation side (Kimi §2): recompute m_2,m_3 for n=2..5 via the (c_1,c_2)
    uniformity reduction (= Kimi's exp/169 method, independently). Confirms the
    exact fractions AND the 169 methodological claim (m_j depends only on the
    first two columns, uniform over ordered isotropic pairs).

(B) Noise side (Kimi §3): verify the closed form SD(mu_row, Uniform) = 1/(2^n(2^n+1))
    AND demonstrate the CATEGORY ERROR — mu_row is the distribution of a ROW of A
    (the LPN query point c_i in the B=I single-row case), NOT the noise e'=Be that
    lem:m2 is about. Concretely: in the B=I, m=2n case, the noise is e itself
    (Bernoulli(p=1/4)), whose SD to Uniform is a CONSTANT, not O(4^-n) — so the
    §3.2 "batch noise ~ uniform" reading is false as a noise statement. The whole
    §3 re-derives the QUERY/matrix-uniformity side, which is the OPEN-corner
    hypothesis (B=g(A) makes BA uniform), not a closure of it.

Output: experiments/171-CLAUDE-lem-m2-stepA-check.json
"""
import json
from fractions import Fraction
from math import comb

def popcount(x): return bin(x).count("1")

def make_omega(n):
    mask = (1 << n) - 1
    def om(u, v):
        ua, ub = u & mask, u >> n
        va, vb = v & mask, v >> n
        return (popcount(ua & vb) ^ popcount(ub & va)) & 1
    return om

out = {"experiment": "171-CLAUDE-lem-m2-stepA-check", "A_correlation": {}, "B_noise": {},
       "verdict": {}}

# (A) m_j via (c1,c2) uniformity, independent of Kimi's code
KIMI = {2: ("7/135", "0"), 3: ("284/4725", "4/315"),
        4: ("464/7497", "16/1071"), 5: ("146368/2347785", "448/28985")}
for n in (2, 3, 4, 5):
    N = 2 * n; om = make_omega(n)
    cnt = 0; acc = {2: Fraction(0), 3: Fraction(0)}
    for c1 in range(1, 1 << N):
        for c2 in range(1, 1 << N):
            if c2 == c1 or om(c1, c2) != 0:
                continue
            t = popcount(c1 & c2); cnt += 1
            for j in (2, 3):
                if t >= j:
                    acc[j] += Fraction(comb(t, j), comb(N, j))
    m2 = acc[2] / cnt; m3 = acc[3] / cnt
    out["A_correlation"][n] = {
        "ordered_isotropic_pairs": cnt,
        "m2": str(m2), "m3": str(m3),
        "m2_matches_kimi": str(m2) == KIMI[n][0],
        "m3_matches_kimi": str(m3) == KIMI[n][1],
        "m2_float": float(m2), "m2_err_from_1/16": float(Fraction(1, 16) - m2),
    }

# (B) noise-side SD closed form + category-error demonstration
for n in (2, 3, 4):
    q = 2 ** n
    mu0 = Fraction(1, q + 1)
    munz = Fraction(q, q + 1) / (q - 1)
    u = Fraction(1, q)
    sd_query = Fraction(1, 2) * (abs(mu0 - u) + (q - 1) * abs(munz - u))
    # actual noise in B=I, m=2n case: e ~ Bernoulli(1/4)^{2n}; SD to Uniform^{2n}:
    # per-coordinate SD(Bernoulli(1/4), Bernoulli(1/2)) = 1/4; for product it -> 1 fast,
    # but even ONE coordinate already 1/4 (constant), not O(4^-n).
    p = Fraction(1, 4)
    sd_noise_one_coord = abs(p - Fraction(1, 2))  # = 1/4, constant
    out["B_noise"][n] = {
        "SD(mu_row,Uniform)": str(sd_query),
        "closed_form_1/(2^n(2^n+1))": str(Fraction(1, q * (q + 1))),
        "closed_form_matches": sd_query == Fraction(1, q * (q + 1)),
        "but_this_is": "the QUERY/row distribution of A, not the noise e'=Be",
        "actual_noise_B=I_per_coord_SD_to_uniform": str(sd_noise_one_coord),
        "actual_noise_is_constant_not_O(4^-n)": float(sd_noise_one_coord) == 0.25,
    }

out["verdict"] = {
    "A_correlation_side": "VERIFIED — m_j exact n=2..5 match; (c1,c2)-uniformity reduction (169) confirmed; m_j -> (1/4)^j",
    "B_noise_side": ("CATEGORY ERROR — SD(mu_row,Uniform)=1/(2^n(2^n+1)) is correct arithmetic "
                     "but mu_row is the QUERY/row distribution (B=I gives noise=e=Bernoulli(1/4), "
                     "constant SD to uniform), NOT e'=Be. The actual noise side is UNTOUCHED."),
    "lem_m2_TRUE_claim": ("NOT SUPPORTED — built on the category error. The matrix-uniformity "
                          "facts re-derived ARE the open-corner hypothesis (B=g(A) makes BA "
                          "uniform), not a closure. lem:m2 status unchanged: OPEN."),
    "correct_noise_side": ("does e'=Be (<=2n-dim image of fixed 2n-bit e) stay DETECTABLY "
                           "non-i.i.d. given only C=BA (secret-B)? = I(e';C)/OP9 structure, "
                           "not SD(mu_row,Uniform)."),
}

with open("experiments/171-CLAUDE-lem-m2-stepA-check.json", "w") as f:
    json.dump(out, f, indent=1)

print("(A) correlation side:")
for n, r in out["A_correlation"].items():
    print(f"  n={n}: m2={r['m2']} (kimi {r['m2_matches_kimi']}), m3={r['m3']} (kimi {r['m3_matches_kimi']})")
print("(B) noise side:")
for n, r in out["B_noise"].items():
    print(f"  n={n}: SD(mu_row,Unif)={r['SD(mu_row,Uniform)']} matches={r['closed_form_matches']}; "
          f"actual B=I noise per-coord SD={r['actual_noise_B=I_per_coord_SD_to_uniform']} (constant)")
print("VERDICT:", json.dumps(out["verdict"], indent=1))
