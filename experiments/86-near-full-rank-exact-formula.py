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
86 — Near-full-rank EXACT formula (resolves the Kimi dilemma; Claude derivation).

Question (A3 near-full-rank stratum): for P in F2^{rho x 2n} of rank rho = 2n-c,
what is  min_Q rank(Omega + P^T Q P)?

Answer (THEOREM, classical minimal-rank completion):
  The forms N = P^T Q P are exactly the bilinear forms vanishing on K = ker P
  (dim c) from both sides. In a (K,V)-adapted basis the matrix E = Omega' + N'
  has fixed blocks E_KK = Om_KK, E_KV = Om_KV, E_VK = Om_VK and a FREE block
  E_VV. The minimal-rank-completion formula gives
      min rank(E) = rank[Om_KK Om_KV] + rank[Om_KK; Om_VK] - rank(Om_KK)
                  = c + c - rank(Om_KK)          (rows/cols of invertible Om')
                  = 2c - rank(Omega|_K),
  achieved CONSTRUCTIVELY by E_VV = Om_VK * G * Om_KV with G any g-inverse of
  Om_KK (over F2: G from rank factorization, A G A = A).

Consequences:
  * c = 1: Omega alternating => Omega|_K = 0 always => min rank(E) = 2 exactly
    (Kimi's n=4,c=1 "best found 4" was a probe artifact: a single canonical
     Q = R^T Omega R per P, no minimization over Q).
  * Adversarial reduction picks K ISOTROPIC (Omega|_K = 0, possible iff c<=n)
    => max_K min_Q = exactly 2c. So "rank(E) <= 2c" is a THEOREM (tight).
  * Detection: output Gram (BA)^T M (BA) = A^T E A has rank <= 2c; uniform C
    has Gram rank ~ n  => blocked whenever 2c < n - O(1), i.e. rho > 3n/2.

This run verifies formula == achieved rank on random P, n=3..5, c=1..3.
No 7th; no break; no security claim. OPEN = LSN.
"""
import random
from collections import Counter
random.seed(42)

def rank(M):
    if not M or not M[0]: return 0
    A = [r[:] for r in M]; rows, cols = len(A), len(A[0]); piv = 0
    for c_ in range(cols):
        r_ = next((r for r in range(piv, rows) if A[r][c_]), None)
        if r_ is None: continue
        A[piv], A[r_] = A[r_], A[piv]
        for rr in range(rows):
            if rr != piv and A[rr][c_]:
                A[rr] = [x ^ y for x, y in zip(A[rr], A[piv])]
        piv += 1
    return piv

def matmul(X, Y):
    q, r = len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][j] for k in range(q)) % 2 for j in range(r)]
            for i in range(len(X))]

def transpose(X):
    return [list(r) for r in zip(*X)]

def ginverse(A):
    """G with A G A = A over F2, via rank factorization A = U V."""
    rows, cols = len(A), len(A[0]); r = rank(A)
    if r == 0:
        return [[0] * rows for _ in range(cols)]
    M = [row[:] for row in A]; piv = 0; pivcols = []
    for c_ in range(cols):
        r_ = next((rr for rr in range(piv, rows) if M[rr][c_]), None)
        if r_ is None: continue
        M[piv], M[r_] = M[r_], M[piv]
        for rr in range(rows):
            if rr != piv and M[rr][c_]:
                M[rr] = [x ^ y for x, y in zip(M[rr], M[piv])]
        pivcols.append(c_); piv += 1
        if piv == r: break
    V = M[:r]
    Vr = [[0] * r for _ in range(cols)]
    for i in range(r):
        Vr[pivcols[i]][i] = 1
    assert matmul(V, Vr) == [[int(i == j) for j in range(r)] for i in range(r)]
    U = matmul(A, Vr)
    UT = transpose(U)
    A2 = [UT[i][:] + [int(j == i) for j in range(r)] for i in range(r)]
    piv = 0; pc = []
    for c_ in range(rows):
        r_ = next((rr for rr in range(piv, r) if A2[rr][c_]), None)
        if r_ is None: continue
        A2[piv], A2[r_] = A2[r_], A2[piv]
        for rr in range(r):
            if rr != piv and A2[rr][c_]:
                A2[rr] = [x ^ y for x, y in zip(A2[rr], A2[piv])]
        pc.append(c_); piv += 1
        if piv == r: break
    Xr = [[0] * r for _ in range(rows)]
    for k, c_ in enumerate(pc):
        for j in range(r):
            Xr[c_][j] = A2[k][rows + j]
    Ulp = transpose(Xr)
    assert matmul(Ulp, U) == [[int(i == j) for j in range(r)] for i in range(r)]
    G = matmul(Vr, Ulp)
    assert matmul(matmul(A, G), A) == A
    return G

def run(n, c, trials):
    D = 2 * n; rho = D - c
    Om = [[0] * D for _ in range(D)]
    for i in range(n):
        Om[i][i + n] = 1; Om[i + n][i] = 1
    out = []
    for _ in range(trials):
        while True:
            P = [[random.randint(0, 1) for _ in range(D)] for _ in range(rho)]
            if rank(P) == rho: break
        M = [row[:] for row in P]; piv = 0; pivcol = {}
        for c_ in range(D):
            r_ = next((rr for rr in range(piv, rho) if M[rr][c_]), None)
            if r_ is None: continue
            M[piv], M[r_] = M[r_], M[piv]
            for rr in range(rho):
                if rr != piv and M[rr][c_]:
                    M[rr] = [x ^ y for x, y in zip(M[rr], M[piv])]
            pivcol[c_] = piv; piv += 1
        K = []
        for f in [c_ for c_ in range(D) if c_ not in pivcol]:
            v = [0] * D; v[f] = 1
            for c_, p_ in pivcol.items():
                v[c_] = M[p_][f]
            K.append(v)
        assert len(K) == c
        S = [k[:] for k in K]
        for e in range(D):
            cand = [0] * D; cand[e] = 1
            if rank(S + [cand]) > len(S): S.append(cand)
            if len(S) == D: break
        Sm = transpose(S)
        Omp = matmul(matmul(transpose(Sm), Om), Sm)
        OKK = [r[:c] for r in Omp[:c]]; OKV = [r[c:] for r in Omp[:c]]
        OVK = [r[:c] for r in Omp[c:]]
        rKK = rank(OKK)
        G = ginverse(OKK)
        EVV = matmul(matmul(OVK, G), OKV)
        E = [[(OKK[i][j] if j < c else OKV[i][j - c]) if i < c else
              (OVK[i - c][j] if j < c else EVV[i - c][j - c])
              for j in range(D)] for i in range(D)]
        out.append((rKK, 2 * c - rKK, rank(E)))
    return out

print(f"{'n':>3} {'c':>3} {'rank(Om_K) dist':>18} {'formula':>9} {'achieved':>9} {'match':>6}")
ok = True
for n in (3, 4, 5):
    for c in (1, 2, 3):
        res = run(n, c, 60)
        match = all(f == r for _, f, r in res)
        ok &= match
        dist = dict(Counter(k for k, _, _ in res))
        print(f"{n:>3} {c:>3} {str(dist):>18} {str(sorted(set(f for _, f, _ in res))):>9} "
              f"{str(sorted(set(r for _, _, r in res))):>9} {str(match):>6}")
assert ok
print("\nmin_Q rank(Omega + P^T Q P) = 2c - rank(Omega|_K)  — confirmed constructively.")
print("c=1 => exactly 2 (alternating). Adversarial K isotropic => exactly 2c. Threshold rho > 3n/2.")
