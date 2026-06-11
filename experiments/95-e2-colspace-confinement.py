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

P2 E2: Colspace confinement measurement for Open Problem 9.



P0: y = Bw where w in F_2^{2n}, B is m×2n. Thus y lives in colspace(B), dim ≤ 2n.

The adversary sees (C,y) = (BA, Bw) but not B.

Question: Does the ≤2n-dimensional confinement of y manifest in single-sample

statistics detectable without knowing B?



We sweep m around the 2n threshold (below, near, above) and measure:

  (a) Fraction where y ∈ colspace(C)  [rank(Cy) == rank(C)]

  (b) Effective dimension gap: m - rank(C,y)  [codimension of (C,y) span]

  (c) Syndrome weight distribution vs m/2n ratio

  (d) P1 comparison for same m



The m vs 2n threshold is critical: for m ≤ 2n, random B may have full rank m,

so colspace(B) = F_2^m and confinement is invisible. For m > 2n, confinement

forces rank(B) ≤ 2n < m, creating structure.

"""



import random

import json

import sys



# Reuse helpers from 94-e1-distinguishing-game.py

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



def syndrome_weight(C, y):

    m = len(C)

    if m == 0:

        return 0

    n = max((x.bit_length() for x in C), default=0)

    aug = list(C)

    for i in range(m):

        if (y >> i) & 1:

            aug[i] |= (1 << n)

    rank = 0

    row = 0

    for c in range(n - 1, -1, -1):

        pivot = None

        for r in range(row, m):

            if (aug[r] >> c) & 1:

                pivot = r

                break

        if pivot is None:

            continue

        aug[row], aug[pivot] = aug[pivot], aug[row]

        for r in range(m):

            if r != row and ((aug[r] >> c) & 1):

                aug[r] ^= aug[row]

        row += 1

        rank += 1

        if row >= m:

            break

    weight = 0

    for i in range(rank, m):

        if (aug[i] >> n) & 1:

            weight += 1

    return weight



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



def sample_P0(n, m, p, B_family="uniform"):

    M_rows = random_symmetric_matrix_rows(n)

    A = isotropic_basis_from_symmetric(M_rows, n)

    x = random.getrandbits(n)

    e = 0

    for k in range(2 * n):

        if random.random() < p:

            e |= (1 << k)

    w = 0

    for k in range(2 * n):

        if (dot_parity(A[k], x) ^ ((e >> k) & 1)):

            w |= (1 << k)



    if B_family == "uniform":

        B = [random.getrandbits(2 * n) for _ in range(m)]

    elif B_family == "low_weight":

        B = []

        for _ in range(m):

            row = 0

            positions = random.sample(range(2 * n), min(3, 2 * n))

            for pos in positions:

                row |= (1 << pos)

            B.append(row)

    else:

        raise ValueError(B_family)



    C = []

    for i in range(m):

        c_row = 0

        for k in range(2 * n):

            if (B[i] >> k) & 1:

                c_row ^= A[k]

        C.append(c_row)



    y = 0

    for i in range(m):

        if dot_parity(B[i], w):

            y |= (1 << i)



    # Also compute rank of B itself (oracle only, for analysis)

    rank_B = gf2_rank(B)

    return C, y, rank_B



def sample_P1(m, n, p_prime):

    C_prime = [random.getrandbits(n) for _ in range(m)]

    x_prime = random.getrandbits(n)

    y_prime = 0

    for i in range(m):

        val = dot_parity(C_prime[i], x_prime)

        if random.random() < p_prime:

            val ^= 1

        if val:

            y_prime |= (1 << i)

    return C_prime, y_prime



def run_confinement_experiment(n, m_values, p_prime, B_family, num_samples=2000):

    results = []

    for m in m_values:

        print(f"  m={m} ...", file=sys.stderr)

        P0_stats = {"in_C": 0, "rank_Cy_minus_rank_C": [], "syndrome": [], "rank_B": []}

        P1_stats = {"in_C": 0, "rank_Cy_minus_rank_C": [], "syndrome": []}



        for _ in range(num_samples):

            C0, y0, rank_B = sample_P0(n, m, 0.25, B_family)

            r0 = gf2_rank(C0)

            r0y = gf2_rank(C0 + [y0 | (1 << max((x.bit_length() for x in C0), default=0))]) if C0 else 0

            # Actually rank_Cy needs careful handling; use the same aug logic

            # Simpler: just compute rank of C + [y with extra col]

            aug0 = list(C0)

            n0 = max((x.bit_length() for x in C0), default=0)

            aug0.append(y0 | (1 << n0))

            r0y = gf2_rank(aug0)



            P0_stats["in_C"] += (1 if r0y == r0 else 0)

            P0_stats["rank_Cy_minus_rank_C"].append(r0y - r0)

            P0_stats["syndrome"].append(syndrome_weight(C0, y0))

            P0_stats["rank_B"].append(rank_B)



            C1, y1 = sample_P1(m, n, p_prime)

            r1 = gf2_rank(C1)

            aug1 = list(C1)

            n1 = max((x.bit_length() for x in C1), default=0)

            aug1.append(y1 | (1 << n1))

            r1y = gf2_rank(aug1)



            P1_stats["in_C"] += (1 if r1y == r1 else 0)

            P1_stats["rank_Cy_minus_rank_C"].append(r1y - r1)

            P1_stats["syndrome"].append(syndrome_weight(C1, y1))



        results.append({

            "n": n,

            "m": m,

            "p_prime": p_prime,

            "B_family": B_family,

            "num_samples": num_samples,

            "threshold_2n": 2 * n,

            "P0": {

                "frac_in_C": round(P0_stats["in_C"] / num_samples, 4),

                "rank_diff_mean": round(sum(P0_stats["rank_Cy_minus_rank_C"]) / num_samples, 4),

                "syndrome_mean": round(sum(P0_stats["syndrome"]) / num_samples, 4),

                "rank_B_mean": round(sum(P0_stats["rank_B"]) / num_samples, 4),

            },

            "P1": {

                "frac_in_C": round(P1_stats["in_C"] / num_samples, 4),

                "rank_diff_mean": round(sum(P1_stats["rank_Cy_minus_rank_C"]) / num_samples, 4),

                "syndrome_mean": round(sum(P1_stats["syndrome"]) / num_samples, 4),

            },

        })

    return results



def main():

    random.seed(0xE2C0)

    all_results = []



    configs = [

        (4, [4, 6, 8, 10, 12], 0.2, "uniform"),

        (5, [6, 8, 10, 12, 14, 16], 0.2, "uniform"),

        (6, [8, 10, 12, 14, 16, 20], 0.2, "uniform"),

    ]



    for n, m_values, p_prime, B_family in configs:

        print(f"Running n={n}, p'={p_prime}, B={B_family} ...", file=sys.stderr)

        results = run_confinement_experiment(n, m_values, p_prime, B_family, num_samples=2000)

        all_results.extend(results)



    output = {

        "experiment": "95-e2-colspace-confinement",

        "description": "m-sweep around 2n threshold; measures confinement visibility",

        "results": all_results,

    }



    with open("experiments/95-e2-results.json", "w") as f:

        json.dump(output, f, indent=2)



    print("Saved experiments/95-e2-results.json", file=sys.stderr)



    print("\n=== SUMMARY: P0 frac_in_C vs m/2n ===", file=sys.stderr)

    for r in all_results:

        ratio = r["m"] / r["threshold_2n"]

        print(f"n={r['n']} m={r['m']:2} (m/2n={ratio:.2f}) | P0 in_C={r['P0']['frac_in_C']:.3f} "

              f"rank_B={r['P0']['rank_B_mean']:.1f} | P1 in_C={r['P1']['frac_in_C']:.3f}", file=sys.stderr)



if __name__ == "__main__":

    main()
