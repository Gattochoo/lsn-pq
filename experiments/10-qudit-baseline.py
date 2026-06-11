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
Verified anchor for Kimi's next task: the QUDIT stabilizer baseline (d=3, qutrits).
The thin-band census asks: is there a THIRD simulable formalism with a discrete
hard-decoding layer? Qudit/normalizer-circuit stabilizers (generalized
Gottesman-Knill simulable) are the first target -- "qudit-LSN over Z_d". Verify the
Sp(2n,Z_d) Lagrangian baseline so Kimi anchors on correct numbers.
"""
import itertools
from functools import reduce

def sform(a, b, n, d):
    # symplectic form over Z_d on Z_d^{2n}: sum a_i b_{n+i} - a_{n+i} b_i
    return reduce(lambda s, i: (s + a[i]*b[n+i] - a[n+i]*b[i]) % d, range(n), 0) % d

def sp_order(n, q):
    return q**(n*n) * reduce(lambda a, i: a*(q**(2*i)-1), range(1, n+1), 1)

def lagr_formula(n, q):
    return reduce(lambda a, i: a*(q**i + 1), range(1, n+1), 1)

for (n, d) in [(1, 3), (2, 3)]:
    dim = 2*n
    vecs = list(itertools.product(range(d), repeat=dim))
    nonzero = [v for v in vecs if any(v)]
    # enumerate k=n-dim subspaces, dedup by canonical span (frozenset of all elements)
    subs = {}
    # build n-dim subspaces by choosing n independent vectors; dedup by span set
    def span(basis):
        elts = set()
        for coeffs in itertools.product(range(d), repeat=len(basis)):
            v = tuple(sum(coeffs[k]*basis[k][i] for k in range(len(basis))) % d for i in range(dim))
            elts.add(v)
        return frozenset(elts)
    seen = set()
    lagr = 0
    total_sub = 0
    for basis in itertools.combinations(nonzero, n):
        sp = span(basis)
        if len(sp) != d**n:           # not independent (wrong size) -> skip
            continue
        if sp in seen:
            continue
        seen.add(sp)
        total_sub += 1
        # isotropic iff sform vanishes on all basis pairs (self auto-zero)
        iso = all(sform(basis[i], basis[j], n, d) == 0 for i in range(n) for j in range(i+1, n))
        lagr += iso
    print(f"d={d}, n={n}:  #{n}-dim subspaces = {total_sub}, "
          f"#Lagrangians = {lagr} (formula prod(q^i+1) = {lagr_formula(n,d)}) "
          f"-> {'OK' if lagr==lagr_formula(n,d) else 'MISMATCH'}")
    print(f"            |Sp({dim},Z_{d})| = {sp_order(n,d)}  (formula)  "
          f"stabilizer = {sp_order(n,d)//lagr if lagr else '-'}")
    print(f"            every v self-isotropic over Z_{d}: {all(sform(v,v,n,d)==0 for v in vecs)}")
print()
print("Structural note: qudit Pauli commutation = the SAME symplectic form, now over")
print("Z_d instead of F2. Clifford = Sp(2n,Z_d) |x Pauli; generalized Gottesman-Knill")
print("makes it simulable. So 'qudit-LSN' = learn a Lagrangian of Z_d^{2n} with noise =")
print("the DIRECT generalization of LSN to a larger ring -- the prima facie expectation")
print("is 'same source, different ring' (cf. LWE over Z_q is still lattice). Kimi's job:")
print("screen whether the Z_d-symplectic structure REDUCES to qubit-LSN / code-over-Z_d,")
print("or genuinely resists (the only way it is a new source).")
