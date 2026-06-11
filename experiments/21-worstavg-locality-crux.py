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
Fix checks (3a)/(3b): the decisive crux of the worst->avg barrier.
(3a) per-qubit noise is NOT invariant under an ENTANGLING Sp element.
(3b) the LOCAL-Clifford subgroup (which DOES preserve per-qubit noise) is NOT
     transitive on Lagrangians -> you cannot randomise the code with only
     noise-preserving elements. THIS is the precise barrier.
"""
import itertools
from functools import reduce
n=2; D=2*n
def omega(a,b):
    return reduce(lambda s,i: s ^ (a[i]&b[i+n]) ^ (a[i+n]&b[i]), range(n),0)&1
vecs=[t for t in itertools.product((0,1),repeat=D)]
nz=[v for v in vecs if any(v)]
def transvect(u,x):
    return x if omega(x,u)==0 else tuple(a^b for a,b in zip(x,u))
def qubit_support(e):                  # # qubits where (x_i,z_i)!=(0,0)
    return sum(1 for i in range(n) if (e[i],e[i+n])!=(0,0))

# Lagrangians
two=set()
for u,w in itertools.combinations(nz,2):
    c=tuple(a^b for a,b in zip(u,w)); two.add(frozenset({u,w,c}))
lagr=[S for S in two if all(omega(a,b)==0 for a in S for b in S)]

# (3a) entangling transvection u=(1,1,0,0): does it change qubit-support (=> noise weight)?
q=0.1
def P(e): return reduce(lambda p,i: p*((1-3*q) if (e[i],e[i+n])==(0,0) else q), range(n), 1.0)
u_ent=(1,1,0,0)
changed=[(e, qubit_support(e), qubit_support(transvect(u_ent,e))) for e in vecs]
mismP=[(e, round(P(e),4), round(P(transvect(u_ent,e)),4)) for e in vecs if abs(P(e)-P(transvect(u_ent,e)))>1e-12]
print(f"(3a) entangling transvection u={u_ent}: per-qubit noise NOT invariant? {len(mismP)>0}")
print(f"     e.g. {mismP[:3]}  (support changes: {[(e,a,b) for e,a,b in changed if a!=b][:3]})")

# (3b) LOCAL subgroup (per-qubit transvections + swap) orbits on the 15 Lagrangians
local_u = [(1,0,0,0),(0,0,1,0),(1,0,1,0),   # qubit 1: X1,Z1,Y1
           (0,1,0,0),(0,0,0,1),(0,1,0,1)]   # qubit 2: X2,Z2,Y2
def swap(x): return (x[1],x[0],x[3],x[2])   # qubit1<->qubit2
def apply_gen_to_L(S):
    outs=[]
    for u in local_u: outs.append(frozenset(transvect(u,x) for x in S))
    outs.append(frozenset(swap(x) for x in S))
    return outs
# orbit of each Lagrangian under the local subgroup
seen=set(); orbits=[]
for L in lagr:
    if L in seen: continue
    orb={L}; fr=[L]
    while fr:
        S=fr.pop()
        for S2 in apply_gen_to_L(S):
            if S2 not in orb: orb.add(S2); fr.append(S2)
    seen|=orb; orbits.append(len(orb))
print(f"(3b) LOCAL-Clifford+swap subgroup orbits on {len(lagr)} Lagrangians: sizes {sorted(orbits)}")
print(f"     transitive (single orbit of 15)? {len(orbits)==1}")
print()
print("CRUX: full Sp is transitive on Lagrangians (free code-randomisation) but its")
print("entangling elements (3a) destroy the per-qubit noise; the LOCAL subgroup that")
print("PRESERVES per-qubit noise is NOT transitive on Lagrangians (3b: it splits into")
print(f"{len(orbits)} orbits). So there is NO noise-preserving transitive randomisation of")
print("the code -> no free Sp worst->avg for PER-QUBIT LSN. The barrier is exactly this")
print("transitivity-vs-locality conflict (= the papers' Pauli-mixing/entropy barrier,")
print("now a concrete group-theoretic statement). Free worst->avg holds only for the")
print("UNIFORM-error model (Sp-invariant); bridging to per-qubit LSN is the isolated gap.")
