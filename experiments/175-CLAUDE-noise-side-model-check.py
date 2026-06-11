#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""175: CLAUDE adjudication of the noise side of Kimi's Step-A report (7e498e4, exp/174).

Two facts established at n=2 (exact, full enumeration):

(1) REPRODUCE: with Kimi's ensemble (B = random Lagrangian basis, n x 2n, independent
    of A; e ~ Bern(1/4)^{2n}), the joint P(C, e') factorizes EXACTLY (90x90x16 grid).
    Kimi's measurement is correct.

(2) MECHANISM (this is the adjudication point): P(C|B) is IDENTICAL for every B in
    that ensemble — verified for all 90 B's. Reason: any two Lagrangian bases are
    related by a symplectic S (B' = BS), and S*A ~ uniform isotropic when A is, so
    C = B'A = B(SA) has the same distribution. Then
        P(C, e') = E_B[P(C|B) P(e'|B)] = P(C) * E_B[P(e'|B)] = P(C) P(e')
    for ANY family P(e'|B) — independence is FORCED by the ensemble, carrying zero
    evidence about noise detectability.

REGIME NOTE (a-priori, no computation needed): lem:m2's obstacle is the confinement
of e' = Be to a <= 2^{2n}-point support inside F_2^m, which requires m > 2n. At
m = n (exp/174's choice) a full-rank B maps F_2^{2n} ONTO F_2^m — full support, no
confinement; and B independent of A is the already-DEAD conditional cell, not the
open marginal-adaptive corner (B = g(A)). Hence the noise side of lem:m2 remains
untouched by exp/174.

Output: experiments/175-CLAUDE-noise-side-model-check.json
"""
import json
from fractions import Fraction
from collections import Counter

def popcount(x): return bin(x).count("1")

def om(v, w, n):
    lo = (1 << n) - 1
    return (popcount((v & lo) & (w >> n)) ^ popcount((v >> n) & (w & lo))) & 1

def rank(rows):
    piv = {}
    for v in rows:
        x = v
        for p in sorted(piv, reverse=True):
            if (x >> p) & 1:
                x ^= piv[p]
        if x:
            piv[x.bit_length() - 1] = x
    return len(piv)

n = 2; N = 4
bases = []
for c1 in range(1, 1 << N):
    for c2 in range(1, 1 << N):
        if c2 != c1 and om(c1, c2, n) == 0 and rank([c1, c2]) == 2:
            bases.append((c1, c2))
assert len(bases) == 90

def C_of(Brows, Acols):
    C = []
    for b in Brows:
        row = 0
        for j, a in enumerate(Acols):
            if popcount(b & a) & 1:
                row |= (1 << j)
        C.append(row)
    return tuple(C)

# (2) mechanism: P(C|B) identical for ALL 90 B
dists = set()
for B in bases:
    cnt = Counter()
    for A in bases:
        cnt[C_of(B, A)] += 1
    dists.add(tuple(sorted(cnt.items())))
mechanism_ok = (len(dists) == 1)

# (1) exact factorization on the full grid
pe = {e: Fraction(1, 4) ** popcount(e) * Fraction(3, 4) ** (4 - popcount(e))
      for e in range(16)}
joint = Counter(); mC = Counter(); mE = Counter(); tot = Fraction(0)
for B in bases:
    for A in bases:
        C = C_of(B, A)
        for e in range(16):
            ep = 0
            for i, b in enumerate(B):
                if popcount(b & e) & 1:
                    ep |= (1 << i)
            p = pe[e]
            joint[(C, ep)] += p; mC[C] += p; mE[ep] += p; tot += p
fact_ok = all(joint.get((c, e), Fraction(0)) * tot == mC[c] * mE[e]
              for c in mC for e in mE)

out = {
    "experiment": "175-CLAUDE-noise-side-model-check",
    "reproduce_exact_factorization_n2": bool(fact_ok),
    "P(C|B)_distinct_distributions_over_all_90_B": len(dists),
    "mechanism_transitivity_forces_independence": bool(mechanism_ok),
    "regime_note": ("lem:m2 confinement needs m > 2n; exp/174 uses m=n (full support, "
                    "no confinement) and B independent of A (closed conditional cell, "
                    "not the open marginal-adaptive corner)."),
    "verdict": ("174's measurement is correct but its independence finding is FORCED by "
                "the ensemble (P(C|B) identical for all B); noise side of lem:m2 remains "
                "OPEN and untouched."),
}
with open("experiments/175-CLAUDE-noise-side-model-check.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
