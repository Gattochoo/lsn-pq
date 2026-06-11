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
"""

Verify closed-form Krawtchouk variance formula via direct enumeration.



Corrected closed form:

  Var = p(1-p) * D + q * S_0 - p^2 * T

where:

  D  = sum_{v!=0} 2^{-2|v|}             = (5/4)^{2n} - 1

  T  = sum_{v!=v', v,v'!=0} 2^{-|v|-|v'|} = ((3/2)^{2n} - 1)^2 - D

  C_full = sum_{v!=v', v,v'!=0} (-1)^{Omega(v,v')} 2^{-|v|-|v'|}

         = (7/4)^{2n} - 2*(3/2)^{2n} + 1 - D

  S_0 = (T + C_full) / 2



Verify for n = 2, 3, 4 by direct enumeration over all Lagrangians.

"""



import math

from itertools import combinations, product



def wt(v):

    return v.bit_count()



def omega(v, vp, n):

    """Standard symplectic form on F_2^{2n}. v, vp are tuples of length 2n."""

    a = v[0:n]

    b = v[n:2*n]

    x = vp[0:n]

    y = vp[n:2*n]

    return sum(a[i]*y[i] + b[i]*x[i] for i in range(n)) % 2



def enumerate_lagrangians(n):

    """Enumerate all isotropic subspaces of dimension n in F_2^{2n}."""

    D = 2 * n

    vectors = list(product([0,1], repeat=D))

    lagrangians = []

    

    for idxs in combinations(range(len(vectors)), n):

        basis = [vectors[i] for i in idxs]

        if any(wt_vec == 0 for wt_vec in basis):

            continue

        

        # Check linear independence

        rows = [sum(v[i] << i for i in range(D)) for v in basis]

        rank_val = 0

        row = 0

        m = list(rows)

        for c in range(D-1, -1, -1):

            pivot = None

            for r in range(row, len(m)):

                if (m[r] >> c) & 1:

                    pivot = r

                    break

            if pivot is None:

                continue

            m[row], m[pivot] = m[pivot], m[row]

            for r in range(len(m)):

                if r != row and ((m[r] >> c) & 1):

                    m[r] ^= m[row]

            row += 1

            rank_val += 1

        if rank_val < n:

            continue

        

        # Check isotropic

        is_iso = True

        for i in range(n):

            for j in range(i, n):

                if omega(basis[i], basis[j], n) != 0:

                    is_iso = False

                    break

            if not is_iso:

                break

        if not is_iso:

            continue

        

        # Generate subspace

        subspace = set()

        for coeffs in product([0,1], repeat=n):

            vec = tuple(sum(coeffs[k] * basis[k][i] for k in range(n)) % 2 for i in range(D))

            subspace.add(vec)

        if len(subspace) == 2**n:

            lagrangians.append(frozenset(subspace))

    

    return list(set(lagrangians))



def exact_variance(n):

    lags = enumerate_lagrangians(n)

    W_vals = []

    for N in lags:

        W = sum(2.0 ** (-sum(v)) for v in N if sum(v) != 0)

        W_vals.append(W)

    mean = sum(W_vals) / len(W_vals)

    var = sum((W - mean) ** 2 for W in W_vals) / len(W_vals)

    return var, mean, len(lags)



def closed_form_variance(n):

    p = 1.0 / (2**n + 1)

    q = 1.0 / ((2**(n-1) + 1) * (2**n + 1))

    

    D = (5/4)**(2*n) - 1

    T = ((3/2)**(2*n) - 1)**2 - D

    C_full = (7/4)**(2*n) - 2*(3/2)**(2*n) + 1 - D

    S_0 = (T + C_full) / 2

    

    var = p * (1 - p) * D + q * S_0 - p * p * T

    return var, D, T, C_full, S_0



print(f"{'n':>3} {'exact_Var':>14} {'closed_Var':>14} {'diff':>14} {'num_lags':>10}")

print("-" * 60)

for n in range(2, 4):

    try:

        exact_var, exact_mean, num_lags = exact_variance(n)

        closed_var, D, T, C_full, S_0 = closed_form_variance(n)

        diff = exact_var - closed_var

        print(f"{n:>3} {exact_var:>14.6f} {closed_var:>14.6f} {diff:>14.6f} {num_lags:>10}")

    except Exception as e:

        print(f"{n:>3} ERROR: {e}")
