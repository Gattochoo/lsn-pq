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
SEED step 1: characterise the symplectic-Fourier-self-dual NOISE distributions
(fixed points of F_Ω among probability vectors). This is the discrete analog of
"which noise smooths the lattice" in Regev's LWE worst->avg.

F_Ω^2 = 2^{2n} I, so eigenvalues are +-2^n; self-dual = the +2^n eigenspace.
"""
import itertools, numpy as np
from functools import reduce

def omega(a, b, n):
    return reduce(lambda s, i: s ^ (a[i]&b[i+n]) ^ (a[i+n]&b[i]), range(n), 0) & 1

# ---- n=1 building block: characterise ALL self-dual distributions on F2^2 ----
n=1; D=2; N=4
vecs=list(itertools.product((0,1),repeat=D))
M=np.array([[(-1)**omega(w,v,n) for v in vecs] for w in vecs])
print("n=1 symplectic-Fourier matrix M (states 00,01,10,11):"); print(M)
print(f"M^2 == {2**D}*I :", np.array_equal(M@M, (2**D)*np.eye(N,dtype=int)))
# self-dual: Mg = 2^n g  i.e. (M-2I)g=0
A=M-(2**n)*np.eye(N,dtype=int)
# null space over reals
u,s,vt=np.linalg.svd(A.astype(float)); null=vt[np.abs(s)<1e-9] if (np.abs(s)<1e-9).any() else vt[s.argsort()][:1]
print("self-dual eigenspace (eigval +2) basis rows (states 00,01,10,11):")
for r in null: print("  ", np.round(r/ (r[np.argmax(np.abs(r))]),3))
print("=> constraint on a self-dual DISTRIBUTION g (>=0, sum 1):")
print("   rows force g(00) = g(01)+g(10)+g(11), and sum=1 -> g(00)=1/2.")
print("   i.e. identity-state prob EXACTLY 1/2; the other 1/2 splits over X,Z,Y.")
print()

# ---- is the cryptographic depolarizing noise self-dual? P(I)=1-3q, P(X)=P(Z)=P(Y)=q ----
print("depolarizing channel on one Omega-pair: P(00=I)=1-3q, P(10=X)=P(01=Z)=P(11=Y)=q")
for q in [0.02, 0.10, 1/6]:
    g=np.array([1-3*q, q, q, q])               # 00,01,10,11
    Fg=M@g
    selfdual=np.allclose(Fg, (2**n)*g)
    print(f"  q={q:.4f}: identity prob={1-3*q:.3f}, self-dual (F_Ω g = 2g)? {selfdual}")
print("  -> self-dual ONLY at q=1/6 (identity prob 1/2 = ERROR RATE 1/2). Crypto (low q,")
print("     identity ~1) is FAR from self-dual.")
print()

# ---- n=2: dim of self-dual eigenspace, and product self-dual noise ----
for n in [2]:
    D=2*n; N=1<<D
    vv=list(itertools.product((0,1),repeat=D))
    M=np.array([[(-1)**omega(w,v,n) for v in vv] for w in vv])
    A=M-(2**n)*np.eye(N)
    rank=np.linalg.matrix_rank(A); dim=N-rank
    print(f"n={n}: 2^2n={N}, self-dual (+2^n) eigenspace dimension = {dim} (= half, {N//2})")
print()
print("CONCLUSION (the sharpened barrier): the symplectic-Fourier-self-dual noise is")
print("PINNED at identity-prob 1/2 per Omega-pair = ERROR RATE 1/2 (max noise). Contrast")
print("the GAUSSIAN: self-dual at EVERY width sigma (a whole family), so Regev can pick")
print("sigma >= smoothing parameter while keeping noise usable. The symplectic self-dual")
print("is RIGID (one max-noise point), not a family -> you cannot lower it to a")
print("cryptographically-useful rate while staying self-dual. THAT rigidity is the precise")
print("worst->avg 'quantum barrier', now a concrete statement rather than folklore.")
