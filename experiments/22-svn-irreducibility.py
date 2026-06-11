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
Lane (math/adjudicator) track of the worst->avg handoff: does the Weil representation
give a code/noise DECOUPLING (-> worst->avg without self-dual noise), or does
Stone-von Neumann rigidity re-impose the barrier?

Decoupling "randomise the code by Sp while leaving the noise fixed" requires an
Sp-equivariant split V = (code part) (+) (noise part). The finite shadow of
Stone-von Neumann is: V = F2^{2n} is an IRREDUCIBLE Sp(2n,F2)-module, so NO such split
exists. Test it (n=2,3): Sp transitive on nonzero <=> no proper nonzero invariant
subspace <=> irreducible.
"""
import itertools
from functools import reduce

def omega(a, b, n):
    return reduce(lambda s, i: s ^ (a[i]&b[i+n]) ^ (a[i+n]&b[i]), range(n), 0) & 1
def transvect(u, x, n):
    return x if omega(x, u, n) == 0 else tuple(a^b for a, b in zip(x, u))

for n in [2, 3]:
    D = 2*n; N = 1 << D
    vecs = [t for t in itertools.product((0,1), repeat=D)]
    nz = [v for v in vecs if any(v)]
    # orbit of a single nonzero vector under symplectic transvections (these generate Sp)
    v0 = nz[0]; orb = {v0}; fr = [v0]
    while fr:
        x = fr.pop()
        for u in nz:
            y = transvect(u, x, n)
            if y not in orb: orb.add(y); fr.append(y)
    transitive = (orb == set(nz))
    print(f"n={n}: Sp-orbit of a nonzero vector = {len(orb)} of {len(nz)} nonzero  ->  transitive: {transitive}")
    print(f"      => F2^{{{D}}} is an IRREDUCIBLE Sp({D},F2)-module: the only invariant")
    print(f"         subspaces are {{0}} and the whole space (any invariant subspace with a")
    print(f"         nonzero vector contains its entire orbit = all nonzero = everything).")
print()
print("ADJUDICATION (this track's question):")
print(" • DECOUPLING at the SUBSPACE level is IMPOSSIBLE. There is no Sp-equivariant")
print("   decomposition V = code (+) noise, because V is Sp-irreducible (the finite-field")
print("   Stone-von Neumann rigidity). So you cannot apply a code-randomising symplectic")
print("   element while fixing a 'noise subspace' -- any g acts on all of V, mixing the")
print("   per-qubit error (Prop 4a). The Weil action does NOT factor.")
print(" • This re-imposes the barrier for the NAIVE 'rotate code, hold noise' decoupling")
print("   = the code-side mirror of the noise-side g(0)=2^{-n} rigidity. Both are one")
print("   irreducibility/SvN fact: the symplectic structure is rigid and does not split.")
print(" • HONEST LIMIT (OPEN, not BROKEN): a worst->avg need not rotate the worst-case")
print("   error at all -- a Regev-style reduction ADDS FRESH noise to encode the worst")
print("   instance into average samples. Subspace-irreducibility does NOT rule that out.")
print("   So: subspace-decoupling is CLOSED (named obstruction = Sp-irreducibility/SvN);")
print("   reduction-level decoupling (fresh-noise encoding) stays OPEN (~0). Report OPEN.")
