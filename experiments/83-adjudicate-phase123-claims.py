# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
83 — Adjudication of Kimi's Phase 1+2+3 commits (0da3e1c, cc8f7d0): independent
re-verification of every computational claim (no code was committed with them).

 [1] F2-linear query advantage at n=3, EXACT, correct metric (D_L vs D_0 deviation):
     max = (1-2p)*2^{-n} = 2^{-n-1} at p=1/4  -> confirms Kimi's commit-message number,
     and EXPOSES that thm:linear-sq's "zero advantage" only holds for REAL-linear
     queries' L-identification; q=b alone already deviates from D_0 by 2^{-n-1}
     (L-independently), and XOR queries <w,a>+b deviate L-DEPENDENTLY (w in L-perp).
 [2] XOR-combining no-go (C2/limitation #4): E[(-1)^{1L(a1)+1L(a2)+1L(a1+a2)}] = 20/64
     at n=3 (exact), -> 1 as n grows: the combined pair is NOT a fresh LSN sample;
     for LPN the same expectation is identically 1. Confirms the no-go reason.
 [3] POSITIVE complement Kimi missed: (a,b) -> (Sa,b) for symplectic S is an EXACT
     secret-rerandomizing self-reduction (S.L Lagrangian, 1_{SL}(Sa)=1_L(a), noise
     untouched; S.L uniform by transitivity). What LSN lacks vs LPN is SAMPLE
     freshness (combining), not secret rerandomization.
 [4] Entropy floor + win-win numbers: H(L) = n(n+1)/2 + 1.2535; the paper's
     "(100-bit) k>=1432" row is PHANTOM (no n=53 / 100-bit set in tab:parameters).
     Correct table: 80/128/192/256-bit -> k >= 863/2147/4755/8387, BKW 2^{k/log2 k}
     = 2^{88.5}/2^{194.0}/2^{389.3}/2^{643.5}.
 [5] B2 arithmetic: C(65,2)=2080; Nr*H(1/4) = 22528*0.8113 = 18278 (~1.8e4). OK.

No 7th; no break; no security claim. OPEN = LSN.
"""
import itertools
from fractions import Fraction

n = 3
D = 2 * n
P = Fraction(1, 4)

def omega(a, b):
    s = 0
    for i in range(n):
        s ^= (a[i] & b[i + n]) ^ (a[i + n] & b[i])
    return s & 1

def span(basis):
    S = {tuple([0] * D)}
    for v in basis:
        S |= {tuple(x ^ y for x, y in zip(s, v)) for s in S}
    return frozenset(S)

vecs = list(itertools.product((0, 1), repeat=D))
Ls, seen = [], set()
for c in itertools.combinations([v for v in vecs if any(v)], n):
    sp = span(c)
    if len(sp) == 2 ** n and sp not in seen and \
       all(omega(a, b) == 0 for a in c for b in c):
        seen.add(sp); Ls.append(sp)
assert len(Ls) == 135

def E_q(L, w, beta, c0):
    """E_{D_L}[q] for q(a,b) = <w,a> xor beta*b xor c0, exact (Fraction).
       L=None means D_0 (b ~ Ber(p) independent of a)."""
    tot = Fraction(0)
    for a in vecs:
        base = sum(wi * ai for wi, ai in zip(w, a)) % 2
        if beta == 0:
            tot += (base ^ c0)
        else:
            pb1 = P + (1 - 2 * P) * (1 if (L is not None and a in L) else 0) \
                  if L is not None else P          # Pr[b=1 | a]
            # q = base ^ b ^ c0 -> E[q|a] = pb1 if base^c0==0 else 1-pb1
            tot += pb1 if (base ^ c0) == 0 else 1 - pb1
    return tot / len(vecs)

# ------------------------------------------------------------------ [1]
L = Ls[0]
dev_dist = Fraction(0); dev_ident = Fraction(0)
L2 = Ls[1]
for w in vecs:
    for beta in (0, 1):
        d0 = E_q(None, w, beta, 0)
        dL = E_q(L, w, beta, 0)
        dL2 = E_q(L2, w, beta, 0)
        dev_dist = max(dev_dist, abs(dL - d0))
        dev_ident = max(dev_ident, abs(dL - dL2))
claim = (1 - 2 * P) * Fraction(1, 2 ** n)
print(f"[1] F2-linear queries, n=3, p=1/4 (exact rationals):")
print(f"    max |E_DL[q]-E_D0[q]|  = {dev_dist}  (= (1-2p)2^-n = {claim} = 2^-(n+1): {dev_dist == claim})")
print(f"    max |E_DL[q]-E_DL'[q]| = {dev_ident} (L-identification, also 2^-(n+1): {dev_ident == claim})")
b_only = abs(E_q(L, tuple([0] * D), 1, 0) - E_q(None, tuple([0] * D), 1, 0))
print(f"    q=b alone (REAL/F2-linear both): deviation {b_only} != 0  -> thm:linear-sq's")
print(f"    'zero advantage' is wrong for the D_L-vs-D_0 task; right claim: E_DL[q] is")
print(f"    L-INDEPENDENT for real-linear q (no L-identification), and all F2-linear")
print(f"    advantages are <= 2^-(n+1) (exponentially small, NOT zero).")
assert dev_dist == claim and dev_ident == claim and b_only == claim

# ------------------------------------------------------------------ [2]
L = Ls[7]
s = Fraction(0)
for a1 in vecs:
    for a2 in vecs:
        a3 = tuple(x ^ y for x, y in zip(a1, a2))
        t = (a1 in L) ^ (a2 in L) ^ (a3 in L)
        s += (-1) ** t
s /= len(vecs) ** 2
print(f"\n[2] XOR-combine: E[(-1)^(1L(a1)+1L(a2)+1L(a1+a2))] = {s} (= 20/64: {s == Fraction(20, 64)})")
print(f"    LPN analogue is identically 1 -> combining samples does NOT yield a fresh")
print(f"    LSN sample; confirms limitation-#4's no-go reason (non-linearity of 1_L).")
assert s == Fraction(20, 64)

# ------------------------------------------------------------------ [3]
import random
random.seed(7)
def app(M, v): return tuple(sum(M[i][j] * v[j] for j in range(D)) % 2 for i in range(D))
def invertible(M):
    A = [list(r) for r in M]; piv = 0
    for col in range(D):
        r = next((r for r in range(piv, D) if A[r][col]), None)
        if r is None: continue
        A[piv], A[r] = A[r], A[piv]
        for rr in range(D):
            if rr != piv and A[rr][col]:
                A[rr] = [x ^ y for x, y in zip(A[rr], A[piv])]
        piv += 1
    return piv == D
def is_sympl(M):
    bas = [tuple(1 if i == k else 0 for i in range(D)) for k in range(D)]
    return all(omega(app(M, u), app(M, v)) == omega(u, v) for u in bas for v in bas)
found = 0; tries = 0
while found < 8 and tries < 300000:
    tries += 1
    M = [tuple(random.randint(0, 1) for _ in range(D)) for _ in range(D)]
    if invertible(M) and is_sympl(M):
        found += 1
        L = Ls[found * 13 % 135]
        SL = frozenset(app(M, v) for v in L)
        assert SL in seen                                   # image is Lagrangian
        assert all((app(M, a) in SL) == (a in L) for a in vecs)   # label identity
print(f"\n[3] secret rerandomization (a,b)->(Sa,b): {found} random symplectic S verified —")
print(f"    S.L always Lagrangian and 1_(SL)(Sa)=1_L(a) (noise untouched). Sp-transitivity")
print(f"    => S.L uniform: EXACT worst-case-secret -> average-case-secret self-reduction.")
print(f"    Missing piece for tight multi-user is SAMPLE freshness only ([2]).")

# ------------------------------------------------------------------ [4]
import math
const = math.log2(math.prod(1 + 2.0 ** -i for i in range(1, 80)))
print(f"\n[4] entropy floor: H(L) = n(n+1)/2 + {const:.4f}")
print(f"    {'sec':>7} {'n':>4} {'H(L)':>9} {'k_min':>6} {'BKW k/log2k':>12}")
for sec, m in [(80, 41), (128, 65), (192, 97), (256, 129)]:
    H = m * (m + 1) / 2 + const
    k = math.ceil(H)
    print(f"    {sec:>4}-bit {m:>4} {H:>9.2f} {k:>6} {k / math.log2(k):>12.1f}")
print(f"    -> paper's '(100-bit) k>=1432' row is PHANTOM (no 100-bit / n=53 set in")
print(f"       tab:parameters); 2^136.6 used phantom k=1432; correct pairs above.")

# ------------------------------------------------------------------ [5]
H4 = -(0.25 * math.log2(0.25) + 0.75 * math.log2(0.75))
print(f"\n[5] B2 arithmetic: C(65,2) = {65 * 64 // 2}; Nr*H(1/4) = 22528*{H4:.4f} = {22528 * H4:.0f} (~1.8e4) OK")

print("\nAll checks passed.")
