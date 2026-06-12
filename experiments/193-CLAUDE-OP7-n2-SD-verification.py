#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""193: CLAUDE independent verification of Kimi's OP7 n=2 sample-freshness SD (192).

From-scratch (no experiments/lib): exact SD between the symplectic-orbit transformed
distribution and two independent fresh samples, over all 720 pairs in Sp(4,F_2).

Finding: the SD is EXACTLY 123/128 for EVERY pair (constant), not a range.
Kimi's 192 reported min 123/128 (correct) but max 371/384 / mean 309/320 (wrong) due to a
membership bug: fresh sample 2 ~ D_{T.L} has membership 1_{T.L}(Tu) = 1_L(u), but 192 used
1_L(Tu). The min was right because at T=I, Tu=u, so the bug is invisible there. Corrected,
192 also yields the constant 123/128 -- matching this from-scratch computation.
"""
from fractions import Fraction
from itertools import product

def pc(x): return bin(x).count("1")
n = 2; N = 4
def om(u, v):
    lo = (1 << n) - 1
    return (pc((u & lo) & (v >> n)) ^ pc((u >> n) & (v & lo))) & 1

def lagrangians():
    out = set()
    for v1 in range(1, 1 << N):
        for v2 in range(1, 1 << N):
            if v2 != v1 and om(v1, v2) == 0:
                out.add(frozenset({0, v1, v2, v1 ^ v2}))
    return sorted(out, key=lambda s: tuple(sorted(s)))

basis = [1, 2, 4, 8]
def apply(cols, x):
    r = 0
    for i in range(4):
        if (x >> i) & 1: r ^= cols[i]
    return r
def is_sympl(cols):
    s = {0}
    for c in cols:
        if c in s: return False
        s |= {t ^ c for t in s}
    if len(s) != 16: return False
    for i in range(4):
        for j in range(i + 1, 4):
            if om(cols[i], cols[j]) != om(basis[i], basis[j]): return False
    return True

Ls = lagrangians(); assert len(Ls) == 15
Sp = [list(c) for c in product(range(1, 16), repeat=4) if is_sympl(list(c))]
assert len(Sp) == 720
pe = {0: Fraction(3, 4), 1: Fraction(1, 4)}
def memb(L, x): return 1 if x in L else 0

SDs = []
for T in Sp:
    P = {}; Q = {}
    wL = Fraction(1, 15)
    for L in Ls:
        TL = frozenset(apply(T, v) for v in L)   # sample 2 secret = T.L
        for x in range(16):
            mx = memb(L, x); Tx = apply(T, x)
            for e in (0, 1):
                b = mx ^ e
                P[(x, b, Tx, b)] = P.get((x, b, Tx, b), Fraction(0)) + wL * Fraction(1, 16) * pe[e]
        for q1 in range(16):
            m1 = memb(L, q1)
            for e1 in (0, 1):
                b1 = m1 ^ e1
                for q2 in range(16):
                    m2 = memb(TL, q2)            # correct: D_{T.L} membership
                    for e2 in (0, 1):
                        b2 = m2 ^ e2
                        Q[(q1, b1, q2, b2)] = Q.get((q1, b1, q2, b2), Fraction(0)) + \
                            wL * Fraction(1, 16) * pe[e1] * Fraction(1, 16) * pe[e2]
    keys = set(P) | set(Q)
    SDs.append(sum(abs(P.get(k, Fraction(0)) - Q.get(k, Fraction(0))) for k in keys) / 2)

mn, mx = min(SDs), max(SDs)
mean = sum(SDs, Fraction(0)) / len(SDs)
print(f"min={mn} max={mx} mean={mean}")
print(f"constant 123/128 for all 720 pairs: {all(s == Fraction(123,128) for s in SDs)}")
