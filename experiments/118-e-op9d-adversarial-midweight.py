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

E-OP9d: Adversarial mid-weight B construction.



Goal: Construct B such that:

  1. C = B' M looks uniform (full rank, no symmetry, balanced correlations)

  2. Yet x recovery from y = Bx + e remains hard.



Method: Rejection sampling — sample random weight-w B rows until C has full rank.

Measure joint uniformity deterministically and recovery rate.



G-MEASURE: JOINT tests only (symmetry, rank, row-correlation).

G-TARGET: Measure recoverability.

"""



import random

from collections import Counter



def random_weight_w_vector(n2, w):

    bits = random.sample(range(n2), w)

    v = 0

    for b in bits:

        v |= 1 << b

    return v



def mat_from_rows(rows, n):

    C = []

    for r in rows:

        row = [(r >> (n + j)) & 1 for j in range(n)]

        C.append(row)

    return C



def is_symmetric(A):

    return all(A[i][j] == A[j][i] for i in range(len(A)) for j in range(i, len(A)))



def mat_rank(A):

    if not A or not A[0]:

        return 0

    n = len(A)

    m = len(A[0])

    M = [row[:] for row in A]

    rank = 0

    row = 0

    for col in range(m):

        pivot = None

        for r in range(row, n):

            if M[r][col] == 1:

                pivot = r

                break

        if pivot is None:

            continue

        M[row], M[pivot] = M[pivot], M[row]

        for r in range(n):

            if r != row and M[r][col] == 1:

                for c in range(col, m):

                    M[r][c] ^= M[row][c]

        row += 1

        rank += 1

        if row == n:

            break

    return rank



def row_dot_products(C):

    n = len(C)

    dots = []

    for i in range(n):

        for j in range(i+1, n):

            dp = sum(C[i][k] & C[j][k] for k in range(n)) & 1

            dots.append(dp)

    return dots



def recovery_success(B_rows, x, p_noise, n):

    Bx = [0] * n

    for i in range(n):

        val = 0

        for j in range(n):

            if (x >> j) & 1:

                val ^= (B_rows[i] >> (n + j)) & 1

        Bx[i] = val

    y = [Bx[i] ^ (1 if random.random() < p_noise else 0) for i in range(n)]

    

    best_x = 0

    best_dist = n + 1

    for x_guess in range(1 << n):

        guess = [0] * n

        for i in range(n):

            val = 0

            for j in range(n):

                if (x_guess >> j) & 1:

                    val ^= (B_rows[i] >> (n + j)) & 1

            guess[i] = val

        dist = sum(guess[i] != y[i] for i in range(n))

        if dist < best_dist:

            best_dist = dist

            best_x = x_guess

    return best_x == x



def sample_B_fullrank(n, w, max_rejects=1000):

    """Sample B with full-rank C via rejection sampling."""

    for attempt in range(max_rejects):

        rows = [random_weight_w_vector(2*n, w) for _ in range(n)]

        C = mat_from_rows(rows, n)

        if mat_rank(C) == n:

            return rows, attempt + 1

    return None, max_rejects



def run_trial(n, w, p_noise, num_trials=100):

    sym_count = 0

    rank_full_count = 0

    all_dots = []

    rec_success = 0

    total_rejects = 0

    

    for _ in range(num_trials):

        result = sample_B_fullrank(n, w)

        if result[0] is None:

            continue

        B_rows, rejects = result

        total_rejects += rejects

        

        C = mat_from_rows(B_rows, n)

        if is_symmetric(C):

            sym_count += 1

        if mat_rank(C) == n:

            rank_full_count += 1

        all_dots.extend(row_dot_products(C))

        

        x = random.randint(0, (1 << n) - 1)

        if recovery_success(B_rows, x, p_noise, n):

            rec_success += 1

    

    return {

        'sym_rate': sym_count / num_trials,

        'rank_full_rate': rank_full_count / num_trials,

        'dot_dist': Counter(all_dots),

        'rec_rate': rec_success / num_trials,

        'avg_rejects': total_rejects / num_trials,

    }



def run_uniform_baseline(n, num_trials=100):

    sym_count = 0

    rank_full_count = 0

    all_dots = []

    

    for _ in range(num_trials):

        C = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

        if is_symmetric(C):

            sym_count += 1

        if mat_rank(C) == n:

            rank_full_count += 1

        all_dots.extend(row_dot_products(C))

    

    return {

        'sym_rate': sym_count / num_trials,

        'rank_full_rate': rank_full_count / num_trials,

        'dot_dist': Counter(all_dots),

    }



if __name__ == "__main__":

    n = 8

    p_noise = 0.25

    num_trials = 100

    

    print(f"E-OP9d: n={n}, p={p_noise}, trials={num_trials}")

    print(f"{'w':>3} {'sym%':>6} {'rank=n%':>8} {'dot0/dot1':>12} {'rec%':>6} {'rejects':>8}")

    print("-" * 55)

    

    base = run_uniform_baseline(n, num_trials)

    d0 = base['dot_dist'].get(0, 0)

    d1 = base['dot_dist'].get(1, 1)

    print(f"{'uni':>3} {base['sym_rate']*100:>6.1f} {base['rank_full_rate']*100:>8.1f} "

          f"{d0}/{d1:>5} {'N/A':>6} {'N/A':>8}")

    

    for w in [2, 3, 4, 5, 6, 7, 8]:

        res = run_trial(n, w, p_noise, num_trials)

        d0 = res['dot_dist'].get(0, 0)

        d1 = res['dot_dist'].get(1, 1)

        print(f"{w:>3} {res['sym_rate']*100:>6.1f} {res['rank_full_rate']*100:>8.1f} "

              f"{d0}/{d1:>5} {res['rec_rate']*100:>6.1f} {res['avg_rejects']:>8.1f}")
