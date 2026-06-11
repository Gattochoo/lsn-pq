#!/usr/bin/env python3

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
"""Verify character sum by direct enumeration for n=2,3."""



import itertools



def wt(v):

    return v.bit_count()



def omega(v, vp, n):

    a = v & ((1 << n) - 1)

    b = v >> n

    x = vp & ((1 << n) - 1)

    y = vp >> n

    return ((a & y).bit_count() + (b & x).bit_count()) & 1



def enumerate_all(n):

    N = 1 << (2 * n)

    nonzero = list(range(1, N))

    

    D = sum(2**(-2*wt(v)) for v in nonzero)

    T = 0.0

    S_0 = 0.0

    S_1 = 0.0

    C_full = 0.0

    

    for v in nonzero:

        for vp in nonzero:

            if v == vp:

                continue

            val = 2**(-wt(v) - wt(vp))

            T += val

            o = omega(v, vp, n)

            if o == 0:

                S_0 += val

            else:

                S_1 += val

            C_full += ((-1)**o) * val

    

    return D, T, S_0, S_1, C_full



for n in [2, 3]:

    D, T, S_0, S_1, C_full = enumerate_all(n)

    print(f"\nn={n}:")

    print(f"  D      = {D:.6f}")

    print(f"  T      = {T:.6f}")

    print(f"  S_0    = {S_0:.6f}")

    print(f"  S_1    = {S_1:.6f}")

    print(f"  C_full = {C_full:.6f}")

    print(f"  S_0+S_1= {S_0+S_1:.6f} (should = T)")

    print(f"  S_0-S_1= {S_0-S_1:.6f} (should = C_full)")

    print(f"  (T+C)/2= {(T+C_full)/2:.6f} (should = S_0)")

    

    all_sum = sum(((-1)**omega(v, vp, n)) * (2**(-wt(v)-wt(vp))) 

                  for v in range(1 << (2*n)) for vp in range(1 << (2*n)))

    print(f"  All-sum= {all_sum:.6f}")

    print(f"  (7/4)^({2*n}) = {(7/4)**(2*n):.6f}")

    print(f"  (3/2)^({2*n})*(7/6)^({2*n}) = {((3/2)*(7/6))**(2*n):.6f}")
