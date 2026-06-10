"""
87 — Enrichment probe: can past samples beat the 2^{-n} dilution?

For small n, we enumerate all Lagrangians, draw samples from a random secret L,
compute the exact posterior P(L | samples), and measure the maximum posterior
probability that any query point a lies in L.

If max_a P(a in L | samples) ≈ 2^{-n} even after many samples, then Bayesian
optimal selection cannot enrich the dilution — strong evidence against enrichment.

Discipline: No 7th; no break; no security claim. OPEN = LSN.
"""
import random
import math
from collections import defaultdict


def lagr_filter_basis(n):
    """All Lagrangian subspaces of F_2^{2n} as frozensets of vectors (ints)."""
    D = 2 * n
    def omega(u, v):
        return sum(((u >> i) & 1) * ((v >> (i + n)) & 1) +
                   ((u >> (i + n)) & 1) * ((v >> i) & 1)
                   for i in range(n)) % 2

    def rank(vecs):
        M = [[int(c) for c in format(v, f'0{D}b')] for v in vecs]
        r = 0
        for c in range(D):
            pivot = next((i for i in range(r, len(M)) if M[i][c]), None)
            if pivot is None:
                continue
            M[r], M[pivot] = M[pivot], M[r]
            for i in range(len(M)):
                if i != r and M[i][c]:
                    M[i] = [a ^ b for a, b in zip(M[i], M[r])]
            r += 1
        return r

    all_vecs = list(range(1, 1 << D))
    def extend(subspace, start_idx):
        if len(subspace) == n:
            yield frozenset(subspace)
            return
        for i in range(start_idx, len(all_vecs)):
            v = all_vecs[i]
            if all(omega(v, w) == 0 for w in subspace) and rank(subspace + [v]) > rank(subspace):
                yield from extend(subspace + [v], i + 1)

    seen = set()
    for basis in extend([], 0):
        vecs = list(basis)
        subspace = {0}
        for mask in range(1, 1 << len(vecs)):
            s = 0
            for j in range(len(vecs)):
                if (mask >> j) & 1:
                    s ^= vecs[j]
            subspace.add(s)
        if len(subspace) == (1 << n):
            f = frozenset(subspace)
            if f not in seen:
                seen.add(f)
                yield f


def graph_lagrangians(n):
    """Graph Lagrangians L = {(x, Mx)} for symmetric M."""
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
    """For each query point a, list indices of Lagrangians that contain a."""
    members = defaultdict(list)
    for idx, L in enumerate(lagrs):
        for a in L:
            members[a].append(idx)
    # Points not in any Lagrangian (only 0 is in all, but we enumerate all a)
    for a in range(1 << D):
        if a not in members:
            members[a] = []
    return members


def run_trial(lagrs, members, D, p, m):
    L_star = random.choice(lagrs)
    samples = []
    for _ in range(m):
        a = random.randint(0, (1 << D) - 1)
        e = 1 if random.random() < p else 0
        b = (1 if a in L_star else 0) ^ e
        samples.append((a, b))

    # Compute log-likelihood for each L
    log_lik = [0.0] * len(lagrs)
    for a, b in samples:
        for idx, L in enumerate(lagrs):
            true_label = 1 if a in L else 0
            if b == true_label:
                log_lik[idx] += math.log(1 - p)
            else:
                log_lik[idx] += math.log(p)

    # Normalize posterior
    max_log = max(log_lik)
    w = [math.exp(ll - max_log) for ll in log_lik]
    Z = sum(w)
    post = [v / Z for v in w]

    # Find max_a P(a in L | samples)
    best = 0.0
    for a in range(1 << D):
        prob = sum(post[idx] for idx in members[a])
        if prob > best:
            best = prob
    return best


def main():
    p = 0.25
    random.seed(42)

    for n in [3, 4]:
        D = 2 * n
        baseline = 2 ** (-n)
        lagrs = list(lagr_filter_basis(n))
        members = precompute_membership(lagrs, D)
        print(f"\nn={n}: {len(lagrs)} Lagrangians, space size {2**D}, baseline {baseline:.4f}")

        for m in [0, 10, 20, 50, 100, 200]:
            probs = []
            for _ in range(20):
                probs.append(run_trial(lagrs, members, D, p, m))
            print(f"  m={m:3d}: max posterior = {min(probs):.4f} .. {max(probs):.4f}  (mean {sum(probs)/len(probs):.4f})")

    # n=5 graph Lagrangians only
    n = 5
    D = 2 * n
    baseline = 2 ** (-n)
    lagrs = list(graph_lagrangians(n))
    members = precompute_membership(lagrs, D)
    print(f"\nn={n} (graph Lagrangians): {len(lagrs)} secrets, baseline {baseline:.4f}")
    for m in [0, 100, 500, 1000]:
        probs = []
        for _ in range(5):
            probs.append(run_trial(lagrs, members, D, p, m))
        print(f"  m={m:4d}: max posterior = {min(probs):.4f} .. {max(probs):.4f}  (mean {sum(probs)/len(probs):.4f})")

    print("\nInterpretation: if max posterior stays near baseline, Bayesian-optimal selection cannot enrich.")


if __name__ == "__main__":
    main()
