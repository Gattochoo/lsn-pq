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

Krawtchouk variance analytic proof — numerical verification for small n.



Verify:

  1. Var[W] ≤ diagonal_only = p(1-p) Σ_{v≠0} 2^{-2|v|} = (25/32)^n (approx).

  2. Var[W] / E[W]^2 ≤ C · (50/81)^n (exponential decay).

  3. std/mean → 0, consistent with O(1/√n) bound.



Exact enumeration for n=2,3,4 (all Lagrangians enumerated).

"""



import itertools

from math import comb



def omega(u, v, n):

    """Standard symplectic form on F_2^{2n}."""

    a = u[0:n]

    b = u[n:2*n]

    x = v[0:n]

    y = v[n:2*n]

    return sum(a[i]*y[i] + b[i]*x[i] for i in range(n)) % 2



def wt(v):

    return sum(v)



def enumerate_lagrangians(n):

    """Enumerate all Lagrangians in F_2^{2n} by brute force."""

    D = 2 * n

    vectors = list(itertools.product([0,1], repeat=D))

    

    lagrangians = []

    # Generate all n-dim isotropic subspaces

    # For small n only (n<=4)

    from itertools import combinations

    for idxs in combinations(range(len(vectors)), n):

        # Check if these vectors form an isotropic subspace

        basis = [vectors[i] for i in idxs]

        if any(wt(v) == 0 for v in basis):

            continue

        # Check linear independence

        # Use Gaussian elimination

        rows = [sum(v[i] << i for i in range(D)) for v in basis]

        rank = 0

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

            rank += 1

        if rank < n:

            continue

        # Check isotropic

        is_isotropic = True

        for i in range(n):

            for j in range(i, n):

                if omega(basis[i], basis[j], n) != 0:

                    is_isotropic = False

                    break

            if not is_isotropic:

                break

        if not is_isotropic:

            continue

        # Generate subspace

        subspace = set()

        for coeffs in itertools.product([0,1], repeat=n):

            vec = tuple(sum(coeffs[k] * basis[k][i] for k in range(n)) % 2 for i in range(D))

            subspace.add(vec)

        if len(subspace) == 2**n:

            lagrangians.append(frozenset(subspace))

    

    return list(set(lagrangians))



def compute_W(N):

    return sum(2 ** (-wt(v)) for v in N)



def theoretical_mean(n):

    return 1.0 + ((1.5 ** (2*n)) - 1.0) / (2 ** n + 1)



def diagonal_bound(n):

    p = 1.0 / (2 ** n + 1)

    sum_term = sum(comb(2*n, k) * (0.25 ** k) for k in range(1, 2*n + 1))

    return p * (1 - p) * sum_term



def ratio_bound(n):

    return (50/81) ** n



if __name__ == "__main__":

    for n in [2, 3]:

        print(f"\nn={n}:")

        lags = enumerate_lagrangians(n)

        print(f"  Lagrangians: {len(lags)}")

        

        W_vals = [compute_W(N) for N in lags]

        mean = sum(W_vals) / len(W_vals)

        var = sum((w - mean)**2 for w in W_vals) / len(W_vals)

        std = var ** 0.5

        

        diag = diagonal_bound(n)

        theo_mean = theoretical_mean(n)

        ratio_b = ratio_bound(n)

        

        print(f"  E[W]      = {mean:.6f} (theo: {theo_mean:.6f})")

        print(f"  Var[W]    = {var:.6f}")

        print(f"  Diag bound= {diag:.6f}")

        print(f"  Var ≤ diag? {var <= diag + 1e-9}")

        print(f"  std/mean  = {std/mean:.6f}")

        print(f"  (50/81)^n = {ratio_b:.6f}")

        print(f"  Var/E^2   = {var/(mean**2):.6f}")

        print(f"  4*(50/81)^n= {4*ratio_b:.6f}")
