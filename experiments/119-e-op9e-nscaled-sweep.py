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

E-OP9e: Full weight × n-scale sweep with G-FLAG compliance.



G-FLAG: any rec% > chance(1/2^n) MUST be n-scaled (n=6..14) and reported as

rec% + rec/chance before any conclusion.



Measures:

  - Recovery success rate (brute-force ML decoder)

  - rec/chance = rec% * 2^n

  - Joint uniformity: symmetry, rank=n, row-dot-product distribution



n-values: 6 (all w), 8 (all w), 10 (w=1,3,5,7,10), 12 (w=1,4,6,8,12), 14 (w=1,5,7,9,14)

"""



import random

import math

import json

from collections import Counter

from datetime import datetime



def random_weight_w_vector(n2, w):

    bits = random.sample(range(n2), w)

    v = 0

    for b in bits:

        v |= 1 << b

    return v



def extract_C_rows(B_rows, n):

    """Extract bottom-n bits of each B row as int."""

    return [(row >> n) & ((1 << n) - 1) for row in B_rows]



def is_symmetric(C_rows, n):

    """C_rows[i] is the i-th row as int. C[i][j] = bit j of C_rows[i]."""

    for i in range(n):

        for j in range(i + 1, n):

            ci_j = (C_rows[i] >> j) & 1

            cj_i = (C_rows[j] >> i) & 1

            if ci_j != cj_i:

                return False

    return True



def mat_rank_from_rows(C_rows, n):

    """Gaussian elimination over F_2 on rows-as-ints."""

    rows = list(C_rows)

    rank = 0

    row_idx = 0

    for col in range(n - 1, -1, -1):

        pivot = None

        for r in range(row_idx, n):

            if (rows[r] >> col) & 1:

                pivot = r

                break

        if pivot is None:

            continue

        rows[row_idx], rows[pivot] = rows[pivot], rows[row_idx]

        for r in range(n):

            if r != row_idx and ((rows[r] >> col) & 1):

                rows[r] ^= rows[row_idx]

        row_idx += 1

        rank += 1

        if row_idx == n:

            break

    return rank



def row_dot_products(C_rows, n):

    dots = []

    for i in range(n):

        for j in range(i + 1, n):

            dp = (C_rows[i] & C_rows[j]).bit_count() & 1

            dots.append(dp)

    return dots



def recovery_success(C_rows, x, p_noise, n):

    """Brute-force ML decoder. C_rows: bottom-n bits of B rows."""

    # Compute Cx

    Cx = 0

    for j in range(n):

        if (x >> j) & 1:

            Cx ^= C_rows[j]

    

    # Add noise to each bit

    y = Cx

    for i in range(n):

        if random.random() < p_noise:

            y ^= (1 << i)

    

    best_dist = n + 1

    for x_guess in range(1 << n):

        guess = 0

        for j in range(n):

            if (x_guess >> j) & 1:

                guess ^= C_rows[j]

        dist = (guess ^ y).bit_count()

        if dist < best_dist:

            best_dist = dist

            best_x = x_guess

    

    return best_x == x



def run_single(n, w, p_noise, num_trials):

    sym_count = 0

    rank_full_count = 0

    all_dots = []

    rec_success = 0

    

    for _ in range(num_trials):

        B_rows = [random_weight_w_vector(2 * n, w) for _ in range(n)]

        C_rows = extract_C_rows(B_rows, n)

        

        if is_symmetric(C_rows, n):

            sym_count += 1

        if mat_rank_from_rows(C_rows, n) == n:

            rank_full_count += 1

        all_dots.extend(row_dot_products(C_rows, n))

        

        x = random.randint(0, (1 << n) - 1)

        if recovery_success(C_rows, x, p_noise, n):

            rec_success += 1

    

    chance = 1.0 / (1 << n)

    rec_rate = rec_success / num_trials

    

    return {

        'n': n,

        'w': w,

        'trials': num_trials,

        'sym_rate': sym_count / num_trials,

        'rank_full_rate': rank_full_count / num_trials,

        'dot_dist': dict(Counter(all_dots)),

        'rec_success': rec_success,

        'rec_rate': rec_rate,

        'chance': chance,

        'rec_over_chance': rec_rate / chance,

    }



def run_uniform_baseline(n, num_trials):

    sym_count = 0

    rank_full_count = 0

    all_dots = []

    

    for _ in range(num_trials):

        C_rows = [random.randint(0, (1 << n) - 1) for _ in range(n)]

        if is_symmetric(C_rows, n):

            sym_count += 1

        if mat_rank_from_rows(C_rows, n) == n:

            rank_full_count += 1

        all_dots.extend(row_dot_products(C_rows, n))

    

    return {

        'sym_rate': sym_count / num_trials,

        'rank_full_rate': rank_full_count / num_trials,

        'dot_dist': dict(Counter(all_dots)),

    }



if __name__ == "__main__":

    p_noise = 0.25

    

    # (n, list of w values, num_trials)

    configs = [

        (6, list(range(1, 7)), 200),

        (8, list(range(1, 9)), 100),

        (10, [1, 3, 5, 7, 10], 50),

        (12, [1, 4, 6, 8, 12], 30),

        (14, [1, 5, 7, 9, 14], 20),

    ]

    

    results = []

    

    for n, ws, num_trials in configs:

        print(f"\n=== n={n}, trials={num_trials} ===")

        

        # Uniform baseline

        base = run_uniform_baseline(n, num_trials)

        d0 = base['dot_dist'].get('0', base['dot_dist'].get(0, 0))

        d1 = base['dot_dist'].get('1', base['dot_dist'].get(1, 0))

        print(f"uniform | sym={base['sym_rate']:.2f} rank={base['rank_full_rate']:.2f} dots={d0}/{d1}")

        

        print(f"{'w':>3} | {'sym':>4} {'rank':>4} {'dots':>10} {'rec%':>6} {'rec/ch':>8}")

        print("-" * 45)

        

        for w in ws:

            res = run_single(n, w, p_noise, num_trials)

            results.append(res)

            

            dd = res['dot_dist']

            d0 = dd.get('0', dd.get(0, 0))

            d1 = dd.get('1', dd.get(1, 0))

            

            print(f"{w:>3} | {res['sym_rate']:>4.2f} {res['rank_full_rate']:>4.2f} "

                  f"{d0:>4}/{d1:<4} {res['rec_rate']*100:>6.1f} {res['rec_over_chance']:>8.1f}")

    

    # Save results

    out = {

        'timestamp': datetime.now().isoformat(),

        'p_noise': p_noise,

        'configs': [{'n': n, 'ws': ws, 'trials': t} for n, ws, t in configs],

        'results': results,

    }

    with open('experiments/119-e-op9e-results.json', 'w') as f:

        json.dump(out, f, indent=2)

    print(f"\nResults saved to experiments/119-e-op9e-results.json")
