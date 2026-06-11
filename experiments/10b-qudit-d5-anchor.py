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
Phase 1 extended: d=5 anchor verification for qudit-LSN baseline.
Expected: n=1: 6 Lagrangians, |Sp(2,Z_5)|=120, stabilizer=20.
"""
import itertools
from functools import reduce

def sform(a, b, n, d):
    return reduce(lambda s, i: (s + a[i]*b[n+i] - a[n+i]*b[i]) % d, range(n), 0) % d

def sp_order(n, q):
    return q**(n*n) * reduce(lambda a, i: a*(q**(2*i)-1), range(1, n+1), 1)

def lagr_formula(n, q):
    return reduce(lambda a, i: a*(q**i + 1), range(1, n+1), 1)

for (n, d) in [(1, 5)]:
    dim = 2*n
    vecs = list(itertools.product(range(d), repeat=dim))
    nonzero = [v for v in vecs if any(v)]
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
        if len(sp) != d**n:
            continue
        if sp in seen:
            continue
        seen.add(sp)
        total_sub += 1
        iso = all(sform(basis[i], basis[j], n, d) == 0 for i in range(n) for j in range(i+1, n))
        lagr += iso
    print(f"d={d}, n={n}:  #{n}-dim subspaces = {total_sub}, "
          f"#Lagrangians = {lagr} (formula prod(q^i+1) = {lagr_formula(n,d)}) "
          f"-> {'OK' if lagr==lagr_formula(n,d) else 'MISMATCH'}")
    print(f"            |Sp({dim},Z_{d})| = {sp_order(n,d)}  (formula)  "
          f"stabilizer = {sp_order(n,d)//lagr if lagr else '-'}")
    print(f"            every v self-isotropic over Z_{d}: {all(sform(v,v,n,d)==0 for v in vecs)}")
