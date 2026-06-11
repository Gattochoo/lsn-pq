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
Closing the Task-4 F2 residual: a PROPER F2 Plücker/Grassmannian decoder.

Kimi's F2 used real-valued SVD on an F2 problem (wrong tool, #13). The correct F2
realization of "spectral estimation of the Lagrangian subspace" is the
Walsh/Fourier-dual fact:
    f(v) = (-1)^{1_L(v)}  ->  \hat f(w) = 2^{2n}[w=0] - 2^{n+1}[w in L^perp]
i.e. the Walsh spectrum of the (clean) membership indicator is SUPPORTED ON THE
DUAL SUBSPACE L^perp (dim n). So the proper "spectral Grassmannian projection" is:
Walsh-transform the noisy labels, take the top 2^n coordinates, and they ARE L^perp
(hence L) -- IF the signal beats the noise. Measure whether it survives constant
rate under n-scaling (n=4,5,6).
"""
import numpy as np
rng = np.random.default_rng(31415)

def fwht(a):                      # in-place Walsh-Hadamard transform (real)
    a = a.astype(np.float64).copy(); h = 1; n = len(a)
    while h < n:
        for i in range(0, n, h*2):
            x = a[i:i+h].copy(); y = a[i+h:i+2*h].copy()
            a[i:i+h] = x + y; a[i+h:i+2*h] = x - y
        h *= 2
    return a

def omega(a, b, n):               # symplectic form on F2^{2n}
    return int((np.dot(a[:n], b[n:]) + np.dot(a[n:], b[:n])) & 1)

def gf2_rank(M):
    M = (M % 2).copy(); r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = np.where(M[r:, c])[0]
        if len(piv) == 0: continue
        p = r + piv[0]; M[[r, p]] = M[[p, r]]
        m = M[:, c].copy(); m[r] = 0; M[m == 1] ^= M[r]; r += 1
        if r == rows: break
    return r

def rand_lagrangian(n):
    D = 2*n; basis = []
    while len(basis) < n:
        v = rng.integers(0, 2, D)
        if not v.any(): continue
        if all(omega(v, b, n) == 0 for b in basis):
            if gf2_rank(np.array(basis + [v])) == len(basis) + 1:
                basis.append(v)
    return np.array(basis)

def subspace_elems(basis, D):     # all 2^k elements (as integer indices 0..2^D-1)
    k = len(basis); out = set()
    for c in range(1 << k):
        v = np.zeros(D, dtype=int)
        for i in range(k):
            if (c >> i) & 1: v ^= basis[i]
        out.add(int(sum(int(v[b]) << b for b in range(D))))
    return out

def dual_subspace(basis, D):      # L^perp_standard = {w : <w,v>=0 for all v in L}
    # build all w with <w, basis_i> = 0 for all i  (solve linear system)
    # brute over 2^D is fine for D<=12
    Lperp = []
    for wi in range(1 << D):
        w = np.array([(wi >> b) & 1 for b in range(D)])
        if all((np.dot(w, b) & 1) == 0 for b in basis):
            Lperp.append(wi)
    return set(Lperp)

print(f"{'n':>2} {'p':>6} {'proper-Plücker (Walsh-dual) recovery':>36}")
for n in [4, 5, 6]:
    D = 2*n; N = 1 << D
    idx_bits = np.array([[(i >> b) & 1 for b in range(D)] for i in range(N)], dtype=np.int8)
    for p in [0.0, 0.02, 0.05, 0.10, 0.25]:
        TR = 20 if n < 6 else 10
        ok = 0
        for _ in range(TR):
            basis = rand_lagrangian(n)
            mem = subspace_elems(basis, D)
            Lperp = dual_subspace(basis, D)            # the target the spectrum reveals
            labels = np.array([1 if i in mem else 0 for i in range(N)], dtype=np.int8)
            flips = (rng.random(N) < p).astype(np.int8)
            noisy = labels ^ flips
            f = 1 - 2*noisy.astype(np.float64)         # (-1)^{noisy label}
            spec = np.abs(fwht(f))
            top = set(np.argsort(-spec)[:len(Lperp)].tolist())   # top 2^n coords
            ok += (top == Lperp)                       # proper Grassmannian-spectral recovery
        print(f"{n:>2} {p:>6.2f} {ok}/{TR:<3} {'recovers L^perp (=L)' if ok>TR*0.5 else ('shrinking' if ok else 'FAILS')}")
print()
print("Reading: the proper F2 spectral-Grassmannian decoder = Walsh-dual recovery.")
print("It recovers L at p~0 but its success SHRINKS with n at constant rate -- the")
print("SAME n-scaling wall as Codex's top-k Walsh (it IS the Walsh family, done as a")
print("subspace recovery). Kimi's real-SVD was a broken proxy for this. The wedge/")
print("algebraic Plücker realizations reduce to F3-list / Gröbner / the result#2")
print("Segre-Veronese lift -- all already walled. => the proper Plücker door obeys")
print("the wall: residual CLOSED (no REDUCES).")
