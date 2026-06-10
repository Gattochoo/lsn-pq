"""
88 — n=4 enrichment + pair-collision heuristic probe.

Uses the full Sp(8,F2)-orbit of 2295 Lagrangians (from experiments/85) and computes
exact Bayesian posteriors.  Two tests:

1. Baseline enrichment (same as 87): after m samples, what is max_a P(a ∈ L | samples)?
2. Pair-collision heuristic: among pairs with b_i = b_j = 1, query a_k = a_i + a_j.
   Does P(a_k ∈ L | samples) exceed the uniform baseline 2^{-n}?

The pair-collision heuristic is motivated by the subspace structure: if a_i, a_j ∈ L
then a_i+a_j ∈ L.  With noise, observing b_i=b_j=1 raises the posterior that both
are in L, which in turn raises the posterior that their sum is in L.

Discipline: No 7th; no break; no security claim. OPEN = LSN.
"""
import random
import math
from collections import defaultdict

random.seed(42)

n = 4
D = 2 * n
p = 0.25
baseline = 2 ** (-n)

def omega(a, b):
    s = 0
    for i in range(n):
        s ^= ((a >> i) & (b >> (i + n))) ^ ((a >> (i + n)) & (b >> i))
    return s & 1

# Build the Sp-orbit of Lagrangians (same logic as experiments/85)
L0 = frozenset(sum(((m >> i) & 1) << i for i in range(n)) for m in range(2 ** n))
def transvect(L, v):
    return frozenset((x ^ v) if omega(x, v) else x for x in L)

orbit = {L0}; frontier = [L0]
vs = [v for v in range(1, 2 ** D)]
while frontier:
    new = []
    for L in frontier:
        for v in vs:
            Lv = transvect(L, v)
            if Lv not in orbit:
                orbit.add(Lv); new.append(Lv)
    frontier = new
lagrs = sorted(orbit, key=sorted)
assert len(lagrs) == 2295, len(lagrs)

# Precompute membership: for each point a, list of Lagrangian indices
members = defaultdict(list)
for idx, L in enumerate(lagrs):
    for a in L:
        members[a].append(idx)

# Also precompute pairwise sums for all Lagrangians
# For each pair (a,b), count how many Lagrangians contain both a and b
pair_count = defaultdict(int)
for idx, L in enumerate(lagrs):
    L_list = list(L)
    for i in range(len(L_list)):
        for j in range(i, len(L_list)):
            a, b = L_list[i], L_list[j]
            if a <= b:
                pair_count[(a, b)] += 1
            else:
                pair_count[(b, a)] += 1

def run_trial(m):
    L_star = random.choice(lagrs)
    samples = []
    for _ in range(m):
        a = random.randint(0, (1 << D) - 1)
        e = 1 if random.random() < p else 0
        b = (1 if a in L_star else 0) ^ e
        samples.append((a, b))

    # Log-likelihood for each Lagrangian
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

    # Test 1: max posterior over all NON-ZERO points (a=0 is in every Lagrangian)
    best_all = 0.0
    for a in range(1, 1 << D):
        prob = sum(post[idx] for idx in members[a])
        if prob > best_all:
            best_all = prob

    # Test 2: pair-collision heuristic
    # For each pair with b_i = b_j = 1, compute P(a_i + a_j ∈ L | samples)
    best_pair = 0.0
    pair_hits = 0
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            a_i, b_i = samples[i]
            a_j, b_j = samples[j]
            if b_i == 1 and b_j == 1:
                a_k = a_i ^ a_j
                if a_k != 0:
                    prob = sum(post[idx] for idx in members[a_k])
                    if prob > best_pair:
                        best_pair = prob
                    pair_hits += 1

    # Test 3: pair-collision with b_i = b_j = 0
    best_pair0 = 0.0
    pair0_hits = 0
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            a_i, b_i = samples[i]
            a_j, b_j = samples[j]
            if b_i == 0 and b_j == 0:
                a_k = a_i ^ a_j
                if a_k != 0:
                    prob = sum(post[idx] for idx in members[a_k])
                    if prob > best_pair0:
                        best_pair0 = prob
                    pair0_hits += 1

    return best_all, best_pair, pair_hits, best_pair0, pair0_hits

def main():
    print(f"n={n}: {len(lagrs)} Lagrangians, baseline P(a∈L) = {baseline:.4f}")
    print()
    for m in [0, 20, 50, 100, 200, 500]:
        trials = 15
        all_best = []
        pair_best = []
        pair_counts = []
        pair0_best = []
        pair0_counts = []
        for _ in range(trials):
            b_all, b_pair, ph, b_pair0, ph0 = run_trial(m)
            all_best.append(b_all)
            pair_best.append(b_pair)
            pair_counts.append(ph)
            pair0_best.append(b_pair0)
            pair0_counts.append(ph0)
        print(f"m={m:3d}: max_posterior = {min(all_best):.4f}..{max(all_best):.4f} (mean {sum(all_best)/len(all_best):.4f})")
        print(f"       pair(1,1)_posterior = {min(pair_best):.4f}..{max(pair_best):.4f} (mean {sum(pair_best)/len(pair_best):.4f}, hits {sum(pair_counts)/len(pair_counts):.1f})")
        print(f"       pair(0,0)_posterior = {min(pair0_best):.4f}..{max(pair0_best):.4f} (mean {sum(pair0_best)/len(pair0_best):.4f}, hits {sum(pair0_counts)/len(pair0_counts):.1f})")
        print()

    print("Interpretation (REJECTED framing — see experiments/90 for corrected sub-floor n=5 data):")
    print("  - The m=100 '6.9x enrichment' is a generic past-floor posterior effect, not a")
    print("    pair-collision advantage.  At m=200/500 pair(1,1)_posterior ≈ plain Bayesian max.")
    print("  - See experiments/90 for sub-floor n=5 probe (m<32) with fresh/observed split:")
    print("    pair-collision gives NO advantage over Bayesian-optimal fresh-point selection.")
    print("  - All observed enrichment = past-floor posterior; negative = good-for-hardness.")

if __name__ == "__main__":
    main()
