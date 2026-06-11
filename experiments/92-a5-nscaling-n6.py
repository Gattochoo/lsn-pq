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
92 — A5 n-scaling fit: n=6 sub-floor enrichment probe.

Extends experiments/90 to n=6 with random subset of graph Lagrangians
(2^21 = 2,097,152 total; we sample 100,000 for tractability).
Compares fresh-point vs observed-point posterior scaling.

Goal: verify δ ≈ c · m · 2^{−n} scaling holds for n=6.
"""
import random
import math
from collections import defaultdict

random.seed(42)

p = 0.25
n = 6
D = 2 * n
baseline = 2 ** (-n)
SUBSET_SIZE = 100_000


def random_graph_lagrangian():
    """Generate a single random graph Lagrangian."""
    dim = n * (n + 1) // 2
    mask = random.randint(0, (1 << dim) - 1)
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
        return frozenset(subspace)
    return None


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

    # Log-likelihood
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

    # Fresh-point: max posterior over points NOT yet queried (excluding 0)
    best_fresh = 0.0
    for a in range(1, 1 << D):
        if a not in queried:
            prob = sum(post[idx] for idx in members[a])
            if prob > best_fresh:
                best_fresh = prob

    # Observed-point: max posterior over points already queried
    best_observed = 0.0
    for a in queried:
        if a != 0:
            prob = sum(post[idx] for idx in members[a])
            if prob > best_observed:
                best_observed = prob

    return best_fresh, best_observed


def main():
    print(f"n={n}: generating {SUBSET_SIZE} random graph Lagrangians...")
    lagrs = []
    attempts = 0
    while len(lagrs) < SUBSET_SIZE and attempts < SUBSET_SIZE * 10:
        L = random_graph_lagrangian()
        attempts += 1
        if L is not None:
            lagrs.append(L)
    print(f"  {len(lagrs)} Lagrangians generated (attempts={attempts}).")
    members = precompute_membership(lagrs, D)
    print(f"Baseline P(a∈L) = {baseline:.6f} = 2^{{-n}}")
    print()

    for m in [8, 16, 24, 32, 40, 48]:
        trials = 20
        fresh_vals = []
        obs_vals = []
        for _ in range(trials):
            bf, bo = run_trial(lagrs, members, m)
            fresh_vals.append(bf)
            obs_vals.append(bo)

        def stats(v):
            return min(v), max(v), sum(v) / len(v)

        f_min, f_max, f_mean = stats(fresh_vals)
        o_min, o_max, o_mean = stats(obs_vals)

        delta = f_mean - baseline
        delta_obs = o_mean - baseline
        print(f"m={m:2d}: fresh_post   = {f_mean:.6f}  (δ={delta:+.6f}, δ/m={delta/m:.6f})")
        print(f"      obs_post   = {o_mean:.6f}  (δ={delta_obs:+.6f})")
        print()

    print("Scaling comparison:")
    print(f"  n=5 (from exp/90): δ/m ≈ 0.0015–0.0020 for m≥12")
    print(f"  n=6 (this probe):  δ/m ≈ ?")
    print(f"  Expected if δ ∝ 2^{{-n}}: n=6 should be ~0.5× n=5")


if __name__ == "__main__":
    main()
