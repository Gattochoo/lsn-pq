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

Multi-sample detector for Open Problem 9.



Setting: adversary receives k samples with the SAME C (P0) or independent C'_i (P1).

P0: y_i = C x_i + B e_i for i=1..k, same C=BA, same B.

P1: y'_i = C'_i x'_i + e'_i, independent C'_i.



Detector: compute rank of Y = [y_1 | ... | y_k] (m x k matrix).

P0: rank(Y) <= rank(B) <= 2n.

P1: rank(Y) ≈ min(k, m) (independent noise dominates).



If k > 2n and m > 2n, this should perfectly separate.

"""



import random

import json

import sys



# Reuse helpers from earlier experiments

def dot_parity(a, b):

    return (a & b).bit_count() & 1



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



def sample_P0_multi(n, m, k, p):

    """Generate k P0 samples with same C."""

    M_rows = random_symmetric_matrix_rows(n)

    A = isotropic_basis_from_symmetric(M_rows, n)

    B = [random.getrandbits(2 * n) for _ in range(m)]



    C = []

    for i in range(m):

        c_row = 0

        for t in range(2 * n):

            if (B[i] >> t) & 1:

                c_row ^= A[t]

        C.append(c_row)



    Y = []

    for _ in range(k):

        x = random.getrandbits(n)

        e = 0

        for t in range(2 * n):

            if random.random() < p:

                e |= (1 << t)

        y = 0

        for i in range(m):

            val = dot_parity(C[i], x)

            val ^= dot_parity(B[i], e)

            if val:

                y |= (1 << i)

        Y.append(y)



    return Y



def sample_P1_multi(m, n, k, p_prime):

    """Generate k P1 samples with fixed C' and fixed x' (standard multi-sample LPN)."""

    C_prime = [random.getrandbits(n) for _ in range(m)]

    x_prime = random.getrandbits(n)

    Y = []

    for _ in range(k):

        y = 0

        for i in range(m):

            val = dot_parity(C_prime[i], x_prime)

            if random.random() < p_prime:

                val ^= 1

            if val:

                y |= (1 << i)

        Y.append(y)

    return Y



def rank_of_Y(Y, m, k):

    """Y is list of k integers (m-bit each). Form m x k matrix and compute rank."""

    rows = []

    for i in range(m):

        row = 0

        for j in range(k):

            if (Y[j] >> i) & 1:

                row |= (1 << j)

        rows.append(row)

    return gf2_rank(rows)



def run_experiment(n, m, k, p_prime, num_trials=200):

    P0_ranks = []

    P1_ranks = []

    for _ in range(num_trials):

        Y0 = sample_P0_multi(n, m, k, 0.25)

        P0_ranks.append(rank_of_Y(Y0, m, k))



        Y1 = sample_P1_multi(m, n, k, p_prime)

        P1_ranks.append(rank_of_Y(Y1, m, k))



    return P0_ranks, P1_ranks



def main():

    random.seed(0x99D3)

    configs = [

        (4, 12, 8, 0.2),   # n=4, m=12, k=8 (>2n=8)

        (5, 15, 12, 0.2),  # n=5, m=15, k=12 (>2n=10)

        (6, 18, 14, 0.2),  # n=6, m=18, k=14 (>2n=12)

        (6, 30, 20, 0.2),  # n=6, m=30, k=20 (large margin)

    ]



    all_results = []

    for n, m, k, p_prime in configs:

        print(f"Running n={n}, m={m}, k={k} ...", file=sys.stderr)

        P0_ranks, P1_ranks = run_experiment(n, m, k, p_prime, num_trials=200)



        P0_mean = sum(P0_ranks) / len(P0_ranks)

        P1_mean = sum(P1_ranks) / len(P1_ranks)



        all_results.append({

            "n": n, "m": m, "k": k, "p_prime": p_prime,

            "P0_rank_mean": round(P0_mean, 2),

            "P1_rank_mean": round(P1_mean, 2),

            "P0_ranks": P0_ranks,

            "P1_ranks": P1_ranks,

        })



    output = {

        "experiment": "99-multisample-detector",

        "description": "Multi-sample rank detector: rank(Y) for k samples",

        "results": all_results,

    }

    with open("experiments/99-multisample-results.json", "w") as f:

        json.dump(output, f, indent=2)



    print("\n=== MULTI-SAMPLE DETECTOR ===", file=sys.stderr)

    print("n | m  | k  | P0 rank mean | P1 rank mean | bound 2n", file=sys.stderr)

    for r in all_results:

        print(f"{r['n']} | {r['m']:2} | {r['k']:2} | {r['P0_rank_mean']:12.1f} | {r['P1_rank_mean']:12.1f} | {2*r['n']:6}", file=sys.stderr)



if __name__ == "__main__":

    main()
