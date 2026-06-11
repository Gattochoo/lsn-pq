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

P5b: Krawtchouk concentration for W_N(1/2).



For random isotropic A, N = nullspace(A^T) = Omega * L where L is random Lagrangian.

W_N(1/2) = sum_{v in N} 2^{-wt(v)}.



Theory predicts:

  E[W_N(1/2)] = 1 + ((3/2)^{2n} - 1) / (2^n + 1)

              = 1 + (9/8)^n * (1 - o(1)).



We measure empirical mean and variance for n=4..10, and verify concentration.

If variance / mean^2 -> 0, then w.h.p. bound follows by Chebyshev.

"""



import random

import json

import sys

from math import comb



def random_symmetric_matrix_rows(n):

    rows = []

    for i in range(n):

        row = random.getrandbits(n)

        for j in range(i):

            if (rows[j] >> i) & 1:

                row |= (1 << j)

            else:

                row &= ~(1 << j)

        rows.append(row)

    return rows



def isotropic_basis_from_symmetric(M_rows, n):

    A = []

    for j in range(n):

        A.append(1 << j)

        b_row = 0

        for i in range(n):

            if (M_rows[j] >> i) & 1:

                b_row |= (1 << i)

        A.append(b_row)

    return A



def gf2_rank(matrix_rows):

    m = list(matrix_rows)

    rank = 0

    row = 0

    if not m:

        return 0

    col = max((x.bit_length() for x in m), default=0)

    for c in range(col - 1, -1, -1):

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

        if row >= len(m):

            break

    return rank



def nullspace_basis(A, n):

    """

    A: list of D rows, each n bits. D = 2n.

    Returns basis of nullspace(A^T): vectors in F_2^D orthogonal to all rows of A.

    """

    D = len(A)

    # We want v in F_2^D such that v^T A = 0, i.e., dot(v, A[:, j]) = 0 for all j.

    # Equivalent to: for each column j of A, sum_i v_i A[i][j] = 0.

    # Build matrix M where M[j][i] = A[i][j] (n rows, D columns).

    M = []

    for j in range(n):

        row = 0

        for i in range(D):

            if (A[i] >> j) & 1:

                row |= (1 << i)

        M.append(row)



    # Find nullspace of M (n × D)

    m = list(M)

    rank = 0

    row_idx = 0

    pivot_cols = []

    free_cols = []

    for c in range(D - 1, -1, -1):

        if row_idx >= n:

            free_cols.append(c)

            continue

        pivot = None

        for r in range(row_idx, n):

            if (m[r] >> c) & 1:

                pivot = r

                break

        if pivot is None:

            free_cols.append(c)

            continue

        m[row_idx], m[pivot] = m[pivot], m[row_idx]

        for r in range(n):

            if r != row_idx and ((m[r] >> c) & 1):

                m[r] ^= m[row_idx]

        pivot_cols.append(c)

        row_idx += 1

        rank += 1



    # Nullspace basis: for each free variable, set it to 1 and solve

    basis = []

    for free_c in free_cols:

        vec = 1 << free_c

        for pc in pivot_cols:

            # Find row with pivot at pc

            for r in range(n):

                if (m[r] >> pc) & 1:

                    if (m[r] >> free_c) & 1:

                        vec |= (1 << pc)

                    break

        basis.append(vec)



    return basis



def enumerate_subspace(basis):

    """Enumerate all vectors in span(basis)."""

    vectors = [0]

    for b in basis:

        new = []

        for v in vectors:

            new.append(v ^ b)

        vectors.extend(new)

    return vectors



def compute_WN_half(basis):

    """W_N(1/2) = sum_{v in span(basis)} 2^{-wt(v)}."""

    total = 0.0

    for v in enumerate_subspace(basis):

        total += 2.0 ** (-v.bit_count())

    return total



def theoretical_mean(n):

    D = 2 * n

    return 1.0 + ((1.5 ** D) - 1.0) / (2 ** n + 1)



def theoretical_variance_diagonal_only(n):

    """

    Var ~ sum_{v != 0} Var(1_{v in N}) 2^{-2wt(v)}

    = (1/(2^n+1))(1 - 1/(2^n+1)) * sum_{k=1}^{2n} C(2n,k) 2^{-2k}

    """

    p = 1.0 / (2 ** n + 1)

    sum_term = sum(comb(2*n, k) * (0.25 ** k) for k in range(1, 2*n + 1))

    return p * (1 - p) * sum_term



def main():

    random.seed(0x5B98)

    results = []



    for n in range(4, 11):

        D = 2 * n

        num_samples = 5000 if n <= 8 else 2000

        print(f"n={n}, D={D}, samples={num_samples} ...", file=sys.stderr)



        values = []

        for _ in range(num_samples):

            M_rows = random_symmetric_matrix_rows(n)

            A = isotropic_basis_from_symmetric(M_rows, n)

            basis = nullspace_basis(A, n)

            W = compute_WN_half(basis)

            values.append(W)



        mean = sum(values) / len(values)

        var = sum((v - mean) ** 2 for v in values) / len(values)

        std = var ** 0.5

        min_v = min(values)

        max_v = max(values)



        theo_mean = theoretical_mean(n)

        theo_var = theoretical_variance_diagonal_only(n)



        results.append({

            "n": n,

            "D": D,

            "num_samples": num_samples,

            "empirical": {

                "mean": round(mean, 6),

                "std": round(std, 6),

                "var": round(var, 6),

                "min": round(min_v, 6),

                "max": round(max_v, 6),

            },

            "theoretical": {

                "mean": round(theo_mean, 6),

                "var_diagonal_only": round(theo_var, 6),

                "std_diagonal_only": round(theo_var ** 0.5, 6),

            },

            "concentration": {

                "std_over_mean": round(std / mean, 6),

                "theo_std_over_mean": round((theo_var ** 0.5) / theo_mean, 6),

            },

        })



        print(f"  emp mean={mean:.4f} std={std:.4f} | theo mean={theo_mean:.4f} std_diag={theo_var**0.5:.4f}", file=sys.stderr)



    output = {

        "experiment": "98-krawtchouk-concentration",

        "description": "Empirical concentration of W_N(1/2) for random isotropic A",

        "results": results,

    }



    with open("experiments/98-krawtchouk-results.json", "w") as f:

        json.dump(output, f, indent=2)



    print("\n=== CONCENTRATION TABLE ===", file=sys.stderr)

    print("n | emp_mean | emp_std | std/mean | theo_mean | theo_std/mean", file=sys.stderr)

    for r in results:

        e = r["empirical"]

        t = r["theoretical"]

        c = r["concentration"]

        print(f"{r['n']:2} | {e['mean']:8.4f} | {e['std']:7.4f} | {c['std_over_mean']:8.4f} | "

              f"{t['mean']:9.4f} | {c['theo_std_over_mean']:13.4f}", file=sys.stderr)



if __name__ == "__main__":

    main()
