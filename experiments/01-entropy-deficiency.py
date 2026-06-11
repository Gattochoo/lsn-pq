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
LSN grounding experiment #1 — verify the Appendix-D entropy deficiency of sympLPN.

The whole 7th-vs-6.5th question hinges on: is the symplectic-orthogonality
constraint on A a REMOVABLE artifact (→ 6.5th, tooling catches up) or an
ESSENTIAL information-theoretic barrier (→ 7th evidence)?  Appendix D (Thm D.1)
claims an isotropic A in F2^{2n x n} has only ~(3/2)n^2 bits vs uniform 2n^2.

Here we COUNT exactly (small n) the ordered n-tuples of pairwise
symplectically-orthogonal columns and compare to uniform. If the gap grows like
the number of pairwise constraints C(n,2)=n(n-1)/2, the deficiency is real and
structural (not a sampling fluke) -- the ground-truth fact both agents reason on.
"""
import itertools, math

def sform(u, v, n):
    # standard symplectic form over F2 on F2^{2n}: sum_i u_i v_{n+i} + u_{n+i} v_i
    s = 0
    for i in range(n):
        s ^= (u[i] & v[n + i]) ^ (u[n + i] & v[i])
    return s & 1

def selfcheck_self_isotropic(n):
    # over F2 every vector is self-symplectic-orthogonal (a^T Omega a = 0): verify
    dim = 2 * n
    return all(sform(v, v, n) == 0 for v in itertools.product([0, 1], repeat=dim))

print(f"{'n':>2} {'#isotropic tuples':>18} {'H_iso':>7} {'H_unif=2n^2':>11} "
      f"{'gap':>6} {'C(n,2)':>6} {'(3/2)n^2':>9}  self-isotropic?")
for n in [1, 2, 3]:
    dim = 2 * n
    vecs = list(itertools.product([0, 1], repeat=dim))
    if n == 1:
        count = len(vecs)            # no pairwise constraint yet
    else:
        count = 0
        for tup in itertools.product(vecs, repeat=n):
            ok = True
            for i in range(n):
                for j in range(i + 1, n):
                    if sform(tup[i], tup[j], n):
                        ok = False
                        break
                if not ok:
                    break
            count += ok
    H_iso = math.log2(count)
    H_unif = dim * n                 # 2n^2
    gap = H_unif - H_iso
    Cn2 = n * (n - 1) // 2
    print(f"{n:>2} {count:>18} {H_iso:>7.3f} {H_unif:>11} {gap:>6.3f} "
          f"{Cn2:>6} {1.5*n*n:>9.1f}  {selfcheck_self_isotropic(n)}")

print()
print("Reading: H_iso = log2(# pairwise-symplectically-orthogonal column tuples).")
print("If gap ~ C(n,2) bits, each orthogonality constraint costs ~1 bit ==> the")
print("isotropic A is information-theoretically far from uniform = the Appendix-D")
print("deficiency, EXACT (not a 'none-found-yet' gap). H_unif - C(n,2) = (3/2)n^2 + n/2.")
