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
"""Debug Lagrangian generation for n=2."""



from itertools import combinations



def wt(v):

    return v.bit_count()



def omega(v, vp, n):

    a = v & ((1 << n) - 1)

    b = v >> n

    x = vp & ((1 << n) - 1)

    y = vp >> n

    return ((a & y).bit_count() + (b & x).bit_count()) & 1



def generate_lagrangians(n):

    N = 1 << (2 * n)

    all_vectors = list(range(N))

    

    def is_isotropic(S):

        for i in range(len(S)):

            for j in range(i + 1, len(S)):

                if omega(S[i], S[j], n) != 0:

                    return False

        return True

    

    def closure(S):

        S = set(S)

        changed = True

        while changed:

            changed = False

            current = list(S)

            for i in range(len(current)):

                for j in range(i + 1, len(current)):

                    s = current[i] ^ current[j]

                    if s not in S:

                        S.add(s)

                        changed = True

        return sorted(S)

    

    def rank(vecs, n):

        m = len(vecs)

        if m == 0:

            return 0

        M = [list(map(int, format(v, f'0{2*n}b'))) for v in vecs]

        r = 0

        for col in range(2 * n):

            pivot = None

            for i in range(r, m):

                if M[i][col] == 1:

                    pivot = i

                    break

            if pivot is None:

                continue

            M[r], M[pivot] = M[pivot], M[r]

            for i in range(m):

                if i != r and M[i][col] == 1:

                    for j in range(col, 2 * n):

                        M[i][j] ^= M[r][j]

            r += 1

            if r == m:

                break

        return r

    

    lagrangians = []

    for basis in combinations(range(1, N), n):

        if not is_isotropic(basis):

            continue

        closed = closure(basis)

        if len(closed) != (1 << n):

            continue

        if rank(closed, n) != n:

            continue

        lagrangians.append(tuple(closed))

    

    return list(set(lagrangians))



n = 2

lags = generate_lagrangians(n)

print(f"n={n}, num_lagrangians={len(lags)}")

for i, N in enumerate(lags[:3]):

    print(f"  L{i}: {N}")
