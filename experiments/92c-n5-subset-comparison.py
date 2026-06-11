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
92c — A5 n=5 subset comparison: reconcile 90 (full) vs 92 (subset) discrepancy.

Runs the same estimator as 90/92 on n=5 with varying subset sizes
to measure subset-size effect and identify the estimator discrepancy.

Output: JSON with subset-size sweep.
"""
import json
import random
import math
from collections import defaultdict

random.seed(42)

p = 0.25
n = 5
D = 2 * n
baseline = 2 ** (-n)

def graph_lagrangians(n):
    dim = n * (n + 1) // 2
    for mask in range(1 << dim):
        M = [[0] * n for _ in range(n)]
        k = 0
        for i in range(n):
            for j in range(i, n):
                M[i][j] = M[j][i] = (mask >> k) & 1
                k += 1
        subspace = set()
        for x in range(1 << n):
            v = 0
            for i in range(n):
                bit = sum(M[i][j] * ((x >> j) & 1) for j in range(n)) % 2
                v |= (bit << i)
            vec = x | (v << n)
            subspace.add(vec)
        if len(subspace) == (1 << n):
            yield frozenset(subspace)

def precompute_membership(lagrs, D):
    members = defaultdict(list)
    for idx, L in enumerate(lagrs):
        for a in L:
            members[a].append(idx)
    return members

def run_trial(lagrs, members, m):
    L_star = random.choice(lagrs)
    samples = []
    queried = set()
    for _ in range(m):
        a = random.randint(0, (1 << D) - 1)
        e = 1 if random.random() < p else 0
        b = (1 if a in L_star else 0) ^ e
        samples.append((a, b))
        queried.add(a)

    log_lik = [0.0] * len(lagrs)
    for a, b in samples:
        for idx, L in enumerate(lagrs):
            true_label = 1 if a in L else 0
            if b == true_label:
                log_lik[idx] += math.log(1 - p)
            else:
                log_lik[idx] += math.log(p)

    max_log = max(log_lik)
    w = [math.exp(ll - max_log) for ll in log_lik]
    Z = sum(w)
    post = [v / Z for v in w]

    best_fresh = 0.0
    for a in range(1, 1 << D):
        if a not in queried:
            prob = sum(post[idx] for idx in members[a])
            if prob > best_fresh:
                best_fresh = prob

    return best_fresh

def main():
    print("Generating full n=5 graph Lagrangians...")
    all_lagrs = list(graph_lagrangians(n))
    print(f"  Full: {len(all_lagrs)} Lagrangians.")
    full_members = precompute_membership(all_lagrs, D)

    subset_sizes = [1000, 5000, 10000, 20000, 32768]
    m_vals = [8, 12, 16, 20, 24]
    trials = 50

    results = []

    for subset_size in subset_sizes:
        if subset_size == 32768:
            lagrs = all_lagrs
            members = full_members
        else:
            lagrs = random.sample(all_lagrs, subset_size)
            members = precompute_membership(lagrs, D)

        print(f"\nSubset size = {subset_size}:")
        for m in m_vals:
            vals = [run_trial(lagrs, members, m) for _ in range(trials)]
            mean = sum(vals) / len(vals)
            delta = mean - baseline
            print(f"  m={m:2d}: post={mean:.4f}  δ={delta:+.4f}  δ/m={delta/m:.5f}")
            results.append({
                "subset_size": subset_size,
                "m": m,
                "mean_post": mean,
                "delta": delta,
                "delta_over_m": delta / m,
            })

    with open("experiments/92c-n5-subset-comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiments/92c-n5-subset-comparison.json")

if __name__ == "__main__":
    main()
