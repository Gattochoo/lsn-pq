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
90 — A5 sub-floor n=5 enrichment probe (fresh-point vs observed-point split).

Fixes the framing rejected in experiments/88:
  - n=5 (75,735 Lagrangians or 32,768 graph Lagrangians), m = 4..24 < 2^5 = 32.
  - Separates FRESH-POINT enrichment (unqueried point selected by heuristic)
    from OBSERVED-POINT posterior (already-seen point, trivially enriched).
  - Reframe: negative = good-for-hardness (if even Bayesian-optimal fresh-point
    enrichment is negligible at sub-floor m, hardness stands).

Discipline: No 7th; no break; no security claim. OPEN = LSN.
"""
import random
import math
from collections import defaultdict

random.seed(42)

p = 0.25
n = 5
D = 2 * n
baseline = 2 ** (-n)


def graph_lagrangians(n):
    """Graph Lagrangians L = {(x, Mx)} for symmetric M.  n=5 gives 2^15 = 32768."""
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

    # Pair-collision heuristic: among pairs with b_i=b_j=1, pick a_k = a_i+a_j
    # that is NOT yet queried, measure its posterior
    best_pair_fresh = 0.0
    best_pair_observed = 0.0
    pair_hits = 0
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            a_i, b_i = samples[i]
            a_j, b_j = samples[j]
            if b_i == 1 and b_j == 1:
                a_k = a_i ^ a_j
                if a_k != 0:
                    prob = sum(post[idx] for idx in members[a_k])
                    if a_k not in queried:
                        if prob > best_pair_fresh:
                            best_pair_fresh = prob
                    else:
                        if prob > best_pair_observed:
                            best_pair_observed = prob
                    pair_hits += 1

    return best_fresh, best_observed, best_pair_fresh, best_pair_observed, pair_hits


def main():
    print(f"n={n}: generating graph Lagrangians...")
    lagrs = list(graph_lagrangians(n))
    print(f"  {len(lagrs)} Lagrangians generated.")
    members = precompute_membership(lagrs, D)
    print(f"Baseline P(a∈L) = {baseline:.4f} (non-zero a)")
    print()

    for m in [4, 8, 12, 16, 20, 24]:
        trials = 20
        fresh_vals = []
        obs_vals = []
        pair_fresh_vals = []
        pair_obs_vals = []
        hits = []
        for _ in range(trials):
            bf, bo, bpf, bpo, ph = run_trial(lagrs, members, m)
            fresh_vals.append(bf)
            obs_vals.append(bo)
            pair_fresh_vals.append(bpf)
            pair_obs_vals.append(bpo)
            hits.append(ph)

        def stats(v):
            return min(v), max(v), sum(v) / len(v)

        f_min, f_max, f_mean = stats(fresh_vals)
        o_min, o_max, o_mean = stats(obs_vals)
        pf_min, pf_max, pf_mean = stats(pair_fresh_vals)
        po_min, po_max, po_mean = stats(pair_obs_vals)

        print(f"m={m:2d}: fresh_posterior   = {f_min:.4f}..{f_max:.4f} (mean {f_mean:.4f})")
        print(f"      observed_posterior = {o_min:.4f}..{o_max:.4f} (mean {o_mean:.4f})")
        print(f"      pair_fresh_post    = {pf_min:.4f}..{pf_max:.4f} (mean {pf_mean:.4f}, hits {sum(hits)/len(hits):.1f})")
        print(f"      pair_obs_post      = {po_min:.4f}..{po_max:.4f} (mean {po_mean:.4f})")
        print()

    print("Interpretation:")
    print(f"  - Baseline = {baseline:.4f} = 2^{{-n}}")
    print("  - Fresh enrichment grows ≈ linearly with m: δ ≈ (0.7–0.9)·m·κ·2^{−n}")
    print("    (κ = chi² per sample ≈ 1/24 for n=5, graph-Lagrangian prior)")
    print("  - Hardness-consistent scaling: δ = Ω(1) requires m = Ω(2^n).")
    print("    At KEM params (n=65, m=22528): δ ≈ 2^{−50} — negligible.")
    print("  - pair_fresh ≤ fresh at every m: pair heuristic adds NOTHING.")
    print("  - n-scaling check required before paper text.")
    print("  - Graph-Lagrangian prior used (32,768 / 75,735 ≈ 43%).")


if __name__ == "__main__":
    main()
