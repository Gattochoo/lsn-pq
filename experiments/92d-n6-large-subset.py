"""
92d — A5 n=6 large-subset enrichment probe (200K subset).

Addresses the subset-size effect identified in 92c:
  - n=5: 1000-subset δ/m ≈ 0.0025, full δ/m ≈ 0.0010 (2.5× inflation)
  - n=6: 100K-subset δ/m ≈ 0.0003, extrapolated full δ/m ≈ 0.00012?

This probe uses 200K random graph Lagrangians (≈10% of 2M) to reduce
the subset-size artifact and get a cleaner n=6 baseline.

Output: JSON.
"""
import json
import random
import math
from collections import defaultdict

random.seed(42)

p = 0.25
n = 6
D = 2 * n
baseline = 2 ** (-n)
SUBSET_SIZE = 200_000

def random_graph_lagrangian():
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

    results = []
    for m in [8, 16, 24, 32, 40, 48]:
        trials = 20
        vals = [run_trial(lagrs, members, m) for _ in range(trials)]
        mean = sum(vals) / len(vals)
        delta = mean - baseline
        print(f"m={m:2d}: post={mean:.6f}  δ={delta:+.6f}  δ/m={delta/m:.6f}  δ·2^n/m={delta * (2**n) / m:.3f}")
        results.append({"m": m, "post": mean, "delta": delta, "delta_over_m": delta / m})

    with open("experiments/92d-n6-large-subset.json", "w") as f:
        json.dump({"n": n, "subset_size": len(lagrs), "baseline": baseline, "results": results}, f, indent=2)
    print("\nSaved to experiments/92d-n6-large-subset.json")

if __name__ == "__main__":
    main()
