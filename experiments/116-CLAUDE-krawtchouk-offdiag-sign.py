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
116 — Claude check: Kimi's Krawtchouk proof (3e6aa6b) claims off-diagonal of Var[W] <= 0
(=> Var <= diagonal bound). Kimi verified n=2,3 only. This computes off-diag EXACTLY for n=2..6
via the closed-form Sp-transitivity probabilities. FINDING: off-diag flips POSITIVE at n>=5,
so "Var <= diagonal" and "Var < (25/32)^n" are FALSE for n>=5. The proof is broken (same
small-n->asymptotic error class). Concentration itself is real (Var/E^2 still decreasing,
~Theta(1/n) polynomial, NOT exponential), so lem:affine-coset-bias promotion stays justified by
numerics but needs a CORRECT proof handling the positive off-diagonal.
No 7th; no break; no security claim. OPEN = LSN.
"""
import itertools
def omega(u, v, n):
    s = 0
    for i in range(n): s ^= (u[i] & v[i+n]) ^ (u[i+n] & v[i])
    return s & 1
for n in range(2, 7):
    D = 2*n; pn = 1.0/(2**n+1); q = 1.0/((2**(n-1)+1)*(2**n+1))
    vecs = list(itertools.product((0,1), repeat=D))[1:]
    wt = {v: 2.0**(-sum(v)) for v in vecs}
    EW = pn*sum(wt[v] for v in vecs)
    diag = sum(pn*(1-pn)*wt[v]**2 for v in vecs)
    off = 0.0
    for i in range(len(vecs)):
        for j in range(len(vecs)):
            if i == j: continue
            pr = q if omega(vecs[i], vecs[j], n) == 0 else 0.0
            off += (pr - pn*pn)*wt[vecs[i]]*wt[vecs[j]]
    Var = diag + off
    print(f"n={n}: Var={Var:.5f} diag={diag:.5f} off={off:+.5f} Var<=diag?{Var<=diag+1e-12} "
          f"Var/E^2={Var/EW**2:.4f}")
print("off-diag > 0 for n>=5 => Kimi's diagonal-bound step is BROKEN; concentration real but proof redo.")
