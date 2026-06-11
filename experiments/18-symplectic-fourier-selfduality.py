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
SEED research: is a Lagrangian's indicator 1_L self-dual under the SYMPLECTIC Fourier
transform -- the discrete-F2 analog of the Gaussian being self-dual under the ordinary
Fourier transform (the self-duality that powers LWE's worst->avg)?

  ordinary Fourier:    F[f](w)   = sum_v f(v) (-1)^{<w,v>}        (standard dot product)
  symplectic Fourier:  F_Ω[f](w) = sum_v f(v) (-1)^{Ω(w,v)}       (symplectic form)

Claim: F_Ω[1_L] = 2^n * 1_L  (eigenfunction, eigenvalue 2^n)  <=> L is Lagrangian (L=L^ω).
Contrast: ordinary F[1_L] is supported on L^perp_standard != L (NOT self-dual).
"""
import itertools
from functools import reduce

def omega(a, b, n):
    return reduce(lambda s, i: s ^ (a[i]&b[i+n]) ^ (a[i+n]&b[i]), range(n), 0) & 1
def dot(a, b):
    return reduce(lambda s, i: s ^ (a[i]&b[i]), range(len(a)), 0) & 1
def gf2_rank(rows):
    rows=[list(r) for r in rows]; n=len(rows[0]) if rows else 0; r=0
    for c in range(n):
        piv=next((i for i in range(r,len(rows)) if rows[i][c]),None)
        if piv is None: continue
        rows[r],rows[piv]=rows[piv],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i][c]: rows[i]=[x^y for x,y in zip(rows[i],rows[r])]
        r+=1
    return r

for n in [2, 3]:
    D = 2*n
    vecs = list(itertools.product((0,1), repeat=D))
    # build one Lagrangian L: greedy isotropic basis, then its span
    basis=[]
    for v in vecs:
        if any(v) and all(omega(v,b,n)==0 for b in basis) and gf2_rank(basis+[list(v)])==len(basis)+1:
            basis.append(list(v))
            if len(basis)==n: break
    L=set()
    for c in itertools.product((0,1),repeat=n):
        x=[0]*D
        for i in range(n):
            if c[i]:
                x=[a^b for a,b in zip(x,basis[i])]
        L.add(tuple(x))
    ind = {v:(1 if v in L else 0) for v in vecs}

    # L^omega = {w : Ω(w,v)=0 for all v in L} ; L^perp_std = {w : <w,v>=0 for all v in L}
    Lw   = set(w for w in vecs if all(omega(w,v,n)==0 for v in L))
    Lstd = set(w for w in vecs if all(dot(w,v)==0     for v in L))

    # symplectic Fourier of 1_L
    Fsymp = {w: sum((-1)**omega(w,v,n) for v in L) for w in vecs}
    # ordinary Fourier of 1_L
    Ford  = {w: sum((-1)**dot(w,v)     for v in L) for w in vecs}

    symp_selfdual = all(Fsymp[w]==(2**n if w in L else 0) for w in vecs)
    ord_supportLstd = all((Ford[w]!=0)==(w in Lstd) for w in vecs)

    print(f"n={n}: |L|={len(L)}, L^omega==L (Lagrangian): {Lw==L}, L^perp_std==L: {Lstd==L}")
    print(f"   SYMPLECTIC Fourier: F_Ω[1_L] = 2^n*1_L (self-dual eigenfunction)?  {symp_selfdual}  (eigval {2**n})")
    print(f"   ordinary  Fourier:  F[1_L] supported on L^perp_std (!= L)?         {ord_supportLstd}  (support==L? {set(w for w in vecs if Ford[w]!=0)==L})")
    print()

print("Reading: 1_L is the eigenfunction of the SYMPLECTIC Fourier transform with")
print("eigenvalue 2^n -- it is SYMPLECTICALLY SELF-DUAL, exactly because L=L^omega")
print("(Lagrangian). Under the ORDINARY Fourier transform it is NOT self-dual (supported")
print("on L^perp_std != L). This is the discrete-F2-symplectic analog of the Gaussian")
print("being self-dual under the ordinary Fourier transform -- the self-duality that")
print("powers LWE's worst->avg. So LSN/sympLPN is the SYMPLECTIC-over-F2 realization of")
print("the same self-duality principle that LWE realizes Gaussian-over-R.")
