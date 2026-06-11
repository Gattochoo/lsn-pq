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
85 — n=4 brute-force ground truth (closure of the lost background job).

The original attempt enumerated C(255,4) ~ 1.7e8 basis combinations and was abandoned
(no artifact survived). This does it right: BFS the Sp(8,F2)-orbit of one Lagrangian
under symplectic transvections T_v(x) = x + omega(x,v)v  (|Lagr(8,2)| = 2295, seconds).

Verifies at n=4, against the exact structural identities used in the paper:
 - |Lagr| = 2295 and the distance distribution [1024, 960, 280, 30, 1]
 - E_glob[2^{dim cap}] (distinct pairs) = 4304/2294 ~= 1.8762
 - dim-2 pencil: size 15 = |Lagr(2)|, E_pencil = 4*E_{Lagr(2)} = 40/7 ~= 5.7143
 - violation: |pencil| = 15 >= |Lagr|/2^{2n} = 8.96  and  E_pencil > 2*E_glob = 3.752
   => SDA(2*rho_avg) < 2^{2n} at n=4 by explicit subset (pencil counterexample, brute).

No 7th; no break; no security claim. OPEN = LSN.
"""
from fractions import Fraction

n = 4; D = 2 * n
def omega(a, b):
    s = 0
    for i in range(n):
        s ^= ((a >> i) & (b >> (i + n))) ^ ((a >> (i + n)) & (b >> i))
    return s & 1

# start Lagrangian: span(e1..en) = x-part
L0 = frozenset(sum(((m >> i) & 1) << i for i in range(n)) for m in range(2 ** n))
def transvect(L, v):
    return frozenset((x ^ v) if omega(x, v) else x for x in L)

orbit = {L0}; frontier = [L0]
vs = [v for v in range(1, 2 ** D)]
while frontier:
    new = []
    for L in frontier:
        for v in vs:
            Lv = transvect(L, v)
            if Lv not in orbit:
                orbit.add(Lv); new.append(Lv)
    frontier = new
Ls = sorted(orbit, key=sorted)
assert len(Ls) == 2295, len(Ls)

# distance distribution from L0 + global distinct-pair E[2^j]
import math
dist = [0] * (n + 1)
for L in Ls:
    j = (len(L0 & L)).bit_length() - 1
    dist[j] += 1
dist[n] -= 1  # exclude L0 itself
print(f"[1] |Lagr(8,2)| = {len(Ls)}; distance distribution from L0 (j=0..4): "
      f"{[dist[0], dist[1], dist[2], dist[3], dist[4] + 1]} (last includes self)")
assert [dist[0], dist[1], dist[2], dist[3], dist[4] + 1] == [1024, 960, 280, 30, 1]

tot = cnt = 0
for i in range(len(Ls)):
    Li = Ls[i]
    for k in range(i + 1, len(Ls)):
        tot += 2 ** ((len(Li & Ls[k])).bit_length() - 1); cnt += 1
E_glob = Fraction(tot, cnt)
print(f"[2] E_glob (distinct pairs) = {E_glob} ~= {float(E_glob):.4f}  (structural: 4304/2294 = {float(Fraction(4304,2294)):.4f})")
assert E_glob == Fraction(4304, 2294)

W = {0, 1, 2, 3}  # span(e1,e2) as bitmasks {00,01,10,11}; omega(e1,e2)=0 -> isotropic
pen = [L for L in Ls if W <= L]
tp = cp = 0
for i in range(len(pen)):
    for k in range(i + 1, len(pen)):
        tp += 2 ** ((len(pen[i] & pen[k])).bit_length() - 1); cp += 1
E_pen = Fraction(tp, cp)
thr = Fraction(len(Ls), 2 ** (2 * n))
print(f"[3] dim-2 pencil: size = {len(pen)} (= |Lagr(2)| = 15), E_pencil = {E_pen} ~= {float(E_pen):.4f} (structural 40/7 = {float(Fraction(40,7)):.4f})")
assert len(pen) == 15 and E_pen == Fraction(40, 7)
viol = len(pen) >= thr and E_pen > 2 * E_glob
print(f"[4] violation at n=4: size {len(pen)} >= threshold {float(thr):.2f} and "
      f"E_pencil {float(E_pen):.3f} > gamma-bar {float(2*E_glob):.3f} : {viol}")
assert viol
print("\nAll n=4 brute-force checks passed — structural identities confirmed by enumeration.")
