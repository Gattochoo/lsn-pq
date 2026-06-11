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
Independent verification of the n=3 (Sp(6,2)) baseline before Codex's OFA-307
runs its noisy/public breaker there. Mirrors the Sp(4,2) check: count Lagrangians
+ prove transitivity via a transvection orbit, cross-check the group order.
"""
import itertools
from functools import reduce

n = 3
dim = 2 * n  # 6

def omega(u, v):
    return reduce(lambda a, i: a ^ (u[i] & v[i+n]) ^ (u[i+n] & v[i]), range(n), 0) & 1

# one known Lagrangian: the x-space span(e0,e1,e2) -> all (a,b,c,0,0,0)
def xspace():
    elts = set()
    for a, b, c in itertools.product((0,1), repeat=3):
        if a or b or c:
            elts.add((a, b, c, 0, 0, 0))
    return frozenset(elts)

# sanity: xspace is isotropic
L0 = xspace()
assert all(omega(u, v) == 0 for u in L0 for v in L0), "x-space not isotropic!"
print(f"x-space is isotropic, |nonzero elts| = {len(L0)} (expect 7 = 2^3-1)")

# transvections t_v(x)=x+omega(x,v)v for the 63 nonzero v generate Sp(6,2)
vecs = [t for t in itertools.product((0,1), repeat=dim)]
nonzero = [v for v in vecs if any(v)]
def transvect(v, x):
    return x if omega(x, v) == 0 else tuple(a ^ b for a, b in zip(x, v))

# BFS the orbit of L0 under all transvections == count Lagrangians (transitivity)
orbit, frontier = {L0}, [L0]
while frontier:
    S = frontier.pop()
    for v in nonzero:
        S2 = frozenset(transvect(v, x) for x in S)
        if S2 not in orbit:
            orbit.add(S2); frontier.append(S2)

formula_lagr = reduce(lambda a, i: a * (2**i + 1), range(1, n+1), 1)   # prod (2^i+1)
sp_order = 2**(n*n) * reduce(lambda a, i: a * (2**(2*i) - 1), range(1, n+1), 1)
print(f"orbit size (= #Lagrangians) = {len(orbit)}   formula prod(2^i+1) = {formula_lagr}  -> {'OK' if len(orbit)==formula_lagr else 'MISMATCH'}")
print(f"single orbit => action TRANSITIVE on all {len(orbit)} Lagrangians: {len(orbit)==formula_lagr}")
print(f"|Sp(6,2)|                    = {sp_order}   (expect 1,451,520)  -> {'OK' if sp_order==1451520 else 'MISMATCH'}")
print(f"stabilizer of a Lagrangian  = {sp_order}//{len(orbit)} = {sp_order//len(orbit)}")
print(f"entropy deficiency C(n,2)   = {n*(n-1)//2} bits  (n=3: the first real reduction gap)")
print()
print("baseline confirmed: 135 Lagrangians, transitive, |Sp(6,2)|=1,451,520.")
print("As at n=2, the bare action is TRANSITIVE => secret/hardness lives only in the")
print("noise layer; OFA-307's public breaker must run on noisy instances.")
