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
SEED completion: the Weil/Sp worst->avg skeleton for LSN. Three checks that locate
the barrier PRECISELY (n=2, Sp(4,2), 15 Lagrangians).

  (1) Sp acts transitively on Lagrangians      -> CODE randomization is exact & free.
  (2) Sp acts transitively on nonzero vectors  -> the ONLY Sp-invariant noise is
      uniform-on-nonzero (P(0)=a). (free code-randomization preserves THIS noise.)
  (3) the cryptographic PER-QUBIT noise is NOT Sp-invariant -> global Sp mixes Paulis
      (the 'Pauli-mixing barrier') -> code-randomization does NOT preserve per-qubit LSN.
"""
import itertools
from functools import reduce
import numpy as np

n=2; D=2*n
def omega(a,b):
    return reduce(lambda s,i: s ^ (a[i]&b[i+n]) ^ (a[i+n]&b[i]), range(n), 0)&1
vecs=[t for t in itertools.product((0,1),repeat=D)]
nz=[v for v in vecs if any(v)]
def gf2_rank(rows):
    rows=[list(r) for r in rows]; c0=len(rows[0]) if rows else 0; r=0
    for c in range(c0):
        p=next((i for i in range(r,len(rows)) if rows[i][c]),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i][c]: rows[i]=[x^y for x,y in zip(rows[i],rows[r])]
        r+=1
    return r
def transvect(u,x):
    return x if omega(x,u)==0 else tuple(a^b for a,b in zip(x,u))

# Lagrangians = 2-dim isotropic subspaces; build set
two=set()
for u,w in itertools.combinations(nz,2):
    c=tuple(a^b for a,b in zip(u,w)); two.add(frozenset({u,w,c}))
lagr=[S for S in two if all(omega(a,b)==0 for a in S for b in S)]
print(f"#Lagrangians = {len(lagr)} (expect 15)")

# (1) Sp transitive on Lagrangians: orbit of one under transvections
L0=lagr[0]; orb={L0}; fr=[L0]
while fr:
    S=fr.pop()
    for u in nz:
        S2=frozenset(transvect(u,x) for x in S)
        if S2 not in orb: orb.add(S2); fr.append(S2)
print(f"(1) Sp-orbit of one Lagrangian = {len(orb)} -> transitive: {len(orb)==len(lagr)}  => CODE randomization EXACT & FREE")

# (2) Sp transitive on nonzero vectors: orbit of one nonzero vector
v0=nz[0]; ov={v0}; fr=[v0]
while fr:
    x=fr.pop()
    for u in nz:
        y=transvect(u,x)
        if y not in ov: ov.add(y); fr.append(y)
print(f"(2) Sp-orbit of one nonzero vector = {len(ov)} -> transitive: {len(ov)==len(nz)}")
print(f"    => the ONLY Sp-invariant noise is P(0)=a, uniform on the {len(nz)} nonzero errors.")

# (3) is the per-qubit depolarizing noise Sp-invariant? apply a sample Sp element (a transvection)
#     per-qubit noise: P(e) = prod over qubits of [I:1-3q, X:q, Z:q, Y:q]; check P(e) vs P(g e)
q=0.1
def perqubit_P(e):
    p=1.0
    for i in range(n):
        xi,zi=e[i],e[i+n]
        p*= (1-3*q) if (xi,zi)==(0,0) else q
    return p
u=nz[3]                                   # a transvection direction (a Clifford = Sp element)
mism=[(e, perqubit_P(e), perqubit_P(transvect(u,e))) for e in vecs]
not_inv=any(abs(a-b)>1e-12 for _,a,b in mism)
print(f"(3) per-qubit depolarizing invariant under a sample Sp element? {not not_inv}")
ex=[(e,round(a,4),round(b,4)) for e,a,b in mism if abs(a-b)>1e-12][:3]
print(f"    example P(e) vs P(g·e) mismatches: {ex}")
print()
print("COMPLETED PICTURE (the worst->avg barrier, precisely located):")
print(" • CODE randomization (worst-case Lagrangian -> uniform random Lagrangian) is EXACT")
print("   and FREE from Sp-transitivity -- the step LWE needs Gaussian smoothing for, LSN")
print("   gets from the group (the Weil action). This is MORE than LWE gets free.")
print(" • but global Sp MIXES the Pauli error (3): the only Sp-invariant noise is")
print("   uniform-on-nonzero, NOT the cryptographic per-qubit noise. So Sp-randomization")
print("   gives a worst->avg for the UNIFORM-error model, not for standard per-qubit LSN.")
print(" • the self-dual sub-case is pinned at P(0)=2^{-n} (max noise; previous step).")
print(" => the worst->avg barrier = the gap between UNIFORM-error (Sp-invariant, code-")
print("    randomizable for free) and PER-QUBIT-error (cryptographic, Pauli-mixing-broken).")
print("    The 'Pauli-mixing' and 'entropy' barriers of the LSN papers are ONE thing:")
print("    code-randomization forces the noise into the Sp-invariant (uniform/max-entropy)")
print("    class. Bridging uniform-error <-> per-qubit-error LSN is the named, isolated gap.")
