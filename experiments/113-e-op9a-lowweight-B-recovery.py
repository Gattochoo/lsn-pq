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

E-OP9a: 저무게 B 구성 + x 복원 시도 (recoverability 타깃).



G-TARGET: 이 실험이 재는 것은 "x가 (C,y)에서 복원가능한가?"이다.

≠ "P0를 LPN과 구별가능한가?" (어젯밤 오류).



설계: A = [I; M] (isotropic basis)일 때,

  - 상단 블록(1..n) 지원 행: c_i = A_j = e_j (비균등, marginal-uniformity 위반).

  - 하단 블록(n+1..2n) 지원 행: c_i = M_j (균등, marginal-uniformity 유지).

  - 유효잡음 p_eff = (1 - (1/2)^w)/2 < 1/2 for any finite w.



따라서 하단-블록-저무게 행은 marginal-uniformity + 저무게를 동시에 만족할 수 있다.

질문: 이런 B로부터 x가 실제로 복원되는가? (복원가능성 = usable reduction 증거)



Families:

  - bottom_w1: 하단 블록 무게 1 (c_i = M_j, p_eff=1/4).

  - bottom_w2: 하단 블록 무게 2 (c_i = M_j+M_k, p_eff=3/8).

  - bottom_w3: 하단 블록 무게 3 (p_eff=7/16).

  - random_w1: 전체 2n 중 무게 1 (비교용, marginal-uniformity 위반 예상).

  - random_w2: 전체 2n 중 무게 2.

  - uniform: 기존 uniform B (비교용, p_eff=1/2).



측정:

  1. Marginal-uniformity: 각 c_i의 분포가 uniform한지 (chi-square on 1000 A samples).

  2. x 복원 성공률: max-agree (brute-force for n≤8).

  3. 평균 복원 시도 횟수 / 실패율.



Output: JSON.

"""



import random

import json

import sys

from collections import Counter

from math import log2



sys.path.insert(0, 'experiments')

with open('experiments/94-e1-distinguishing-game.py') as f:

    code = f.read().replace("if __name__ == '__main__':", "if False:")

exec(code)



# ---------------------------------------------------------------------------

# Helpers



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



def sample_B_row(family, n, w):

    """Sample one row of B (2n-bit vector) according to family.

    

    A = [e_0, M_0, e_1, M_1, ..., e_{n-1}, M_{n-1}] where e_j is at index 2j, M_j at index 2j+1.

    """

    if family == "bottom_w1":

        j = random.randrange(n)

        return 1 << (2 * j + 1)  # select M_j

    elif family == "bottom_w2":

        j, k = random.sample(range(n), 2)

        return (1 << (2 * j + 1)) | (1 << (2 * k + 1))  # select M_j + M_k

    elif family == "bottom_w3":

        js = random.sample(range(n), min(w, n))

        return sum(1 << (2 * j + 1) for j in js)  # select sum of M_j's

    elif family == "random_w1":

        j = random.randrange(2 * n)

        return 1 << j  # select random A[t]

    elif family == "random_w2":

        j, k = random.sample(range(2 * n), 2)

        return (1 << j) | (1 << k)

    elif family == "uniform":

        return random.getrandbits(2 * n)

    else:

        raise ValueError(family)



def generate_B(family, m, n, w=3):

    return [sample_B_row(family, n, w) for _ in range(m)]



def compute_C(B, A):

    """C = BA. A is list of 2n row-vectors (n-bit each)."""

    C = []

    for b in B:

        c = 0

        for t in range(len(A)):

            if (b >> t) & 1:

                c ^= A[t]

        C.append(c)

    return C



def sample_P0_with_B(n, m, B):

    """Generate P0 sample with given B. Returns (C, y, x)."""

    M_rows = random_symmetric_matrix_rows(n)

    A = isotropic_basis_from_symmetric(M_rows, n)

    C = compute_C(B, A)

    x = random.getrandbits(n)

    # Noise e (2n bits, Ber(1/4))

    e = 0

    for t in range(2 * n):

        if random.random() < 0.25:

            e |= (1 << t)

    # w = Ax + e

    w = 0

    for t in range(2 * n):

        if (dot_parity(A[t], x) ^ ((e >> t) & 1)):

            w |= (1 << t)

    # y = Bw

    y = 0

    for i in range(m):

        if dot_parity(B[i], w):

            y |= (1 << i)

    return C, y, x



def max_agreement_for_recovery(C, y):

    """Brute-force max x that maximizes agreement. Returns (best_x, max_agree)."""

    if not C:

        return 0, 0

    n_bits = max(c.bit_length() for c in C) if any(c for c in C) else 1

    best_x = 0

    best_agree = -1

    for x in range(1 << n_bits):

        agree = 0

        for i in range(len(C)):

            pred = dot_parity(C[i], x)

            actual = (y >> i) & 1

            if pred == actual:

                agree += 1

        if agree > best_agree:

            best_agree = agree

            best_x = x

    return best_x, best_agree



def marginal_uniformity_check(family, n, m, num_A_samples=1000):

    """Check if each row of C is marginally uniform over random A."""

    counters = [Counter() for _ in range(m)]

    for _ in range(num_A_samples):

        M_rows = random_symmetric_matrix_rows(n)

        A = isotropic_basis_from_symmetric(M_rows, n)

        B = generate_B(family, m, n)

        C = compute_C(B, A)

        for i in range(m):

            counters[i][C[i]] += 1

    # Entropy per row

    entropies = []

    for i in range(m):

        total = sum(counters[i].values())

        ent = 0.0

        for count in counters[i].values():

            p = count / total

            ent -= p * log2(p)

        entropies.append(ent)

    max_possible = n  # uniform over 2^n values

    avg_entropy = sum(entropies) / len(entropies)

    min_entropy = min(entropies)

    return {

        "avg_entropy": round(avg_entropy, 4),

        "min_entropy": round(min_entropy, 4),

        "max_possible": max_possible,

        "entropy_ratio": round(avg_entropy / max_possible, 4) if max_possible > 0 else 1.0,

    }



def recovery_experiment(n, m, family, num_trials=200):

    """Measure x recovery success with given B family."""

    successes = 0

    total_agree_when_correct = 0

    total_agree_when_wrong = 0

    wrong_count = 0

    for _ in range(num_trials):

        B = generate_B(family, m, n)

        C, y, true_x = sample_P0_with_B(n, m, B)

        recovered_x, max_agree = max_agreement_for_recovery(C, y)

        if recovered_x == true_x:

            successes += 1

            total_agree_when_correct += max_agree

        else:

            wrong_count += 1

            total_agree_when_wrong += max_agree

    return {

        "success_rate": successes / num_trials,

        "avg_agree_correct": total_agree_when_correct / max(successes, 1),

        "avg_agree_wrong": total_agree_when_wrong / max(wrong_count, 1),

    }



# ---------------------------------------------------------------------------

# Main



if __name__ == "__main__":

    random.seed(0x5E1F)

    configs = [

        # (n, m, family)

        (6, 24, "bottom_w1"),

        (6, 24, "bottom_w2"),

        (6, 24, "bottom_w3"),

        (6, 24, "random_w1"),

        (6, 24, "random_w2"),

        (6, 24, "uniform"),

        (8, 32, "bottom_w1"),

        (8, 32, "bottom_w2"),

        (8, 32, "uniform"),

    ]



    results = []

    for n, m, family in configs:

        print(f"Running n={n}, m={m}, family={family} ...", file=sys.stderr)

        

        # 1. Marginal-uniformity check

        mu = marginal_uniformity_check(family, n, m, num_A_samples=1000)

        

        # 2. Recovery experiment

        rec = recovery_experiment(n, m, family, num_trials=200)

        

        entry = {

            "n": n,

            "m": m,

            "family": family,

            "marginal_uniformity": mu,

            "recovery": rec,

        }

        results.append(entry)

        print(f"  entropy_ratio={mu['entropy_ratio']}, success_rate={rec['success_rate']:.2f}", file=sys.stderr)



    output = {

        "experiment": "113-e-op9a-lowweight-B-recovery",

        "description": "Low-weight B construction + x recovery (recoverability target)",

        "date": "2026-06-12",

        "results": results,

    }

    with open("experiments/113-e-op9a-results.json", "w") as f:

        json.dump(output, f, indent=2)

    print("Saved experiments/113-e-op9a-results.json", file=sys.stderr)
