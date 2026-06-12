#!/usr/bin/env python3
"""181: Operational distinguishing advantage on (C,z) vs LPN.

PRE-REGISTER (Claude adjudication 109c6c1):
- Disproof target for lem:m2: exhibit g making SD((C,z)_red, LPN_{p'}) = o(1).
- Metric sign: SD -> 0 means working reduction = DISPROVES lem:m2.
              SD bounded away from 0 means reduction fails = SUPPORTS lem:m2.
- Adversary sees only (C,z); B=g(A) and x are unknown/marginalized.

This script searches g(A) to minimize SD((C,z), LPN) for n=2, m in {2,3,4}.
It uses exact enumeration and incremental updates so full SD can be recomputed
at every SA step.

Run: python3 experiments/181-KIMI-operational-distinguishing-SD-search.py
"""
import random
import math
import time
import json
from collections import Counter
from pathlib import Path


def popcount(x):
    return bin(x).count("1")


def symplectic_form(v, w, n):
    low = (1 << n) - 1
    return (
        popcount((v & low) & (w >> n))
        ^ popcount((v >> n) & (w & low))
    ) & 1


def rank_rows(rows, n_cols):
    pivots = {}
    for v in rows:
        x = v
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return len(pivots)


def enumerate_all_A(n):
    N = 2 * n
    size = 1 << N
    subspaces = []

    def extend_basis(current):
        if len(current) == n:
            if rank_rows(current, N) == n:
                subspaces.append(tuple(current))
            return
        start = current[-1] + 1 if current else 1
        for v in range(start, size):
            temp = list(current) + [v]
            if rank_rows(temp, N) != len(temp):
                continue
            if all(symplectic_form(v, b, n) == 0 for b in current):
                extend_basis(temp)

    extend_basis([])
    from itertools import permutations

    A_matrices = set()
    for sub in subspaces:
        for perm in permutations(sub):
            A_rows = []
            for j in range(N):
                row = 0
                for k in range(n):
                    if (perm[k] >> j) & 1:
                        row |= (1 << k)
                A_rows.append(row)
            A_matrices.add(tuple(A_rows))
    return [list(a) for a in sorted(A_matrices)]


def compute_C(B, A_rows):
    """C = B * A as tuple of m rows, each an n-bit integer."""
    m = len(B)
    N = len(A_rows)
    C = []
    for i in range(m):
        row = 0
        b = B[i]
        k = 0
        while b:
            if b & 1:
                row ^= A_rows[k]
            b >>= 1
            k += 1
        C.append(row)
    return tuple(C)


def compute_e_prime(B, e):
    """e' = B e as m-bit integer."""
    ep = 0
    for i, b in enumerate(B):
        if popcount(b & e) & 1:
            ep |= 1 << i
    return ep


def matvec(C_rows, x):
    """C * x as m-bit integer."""
    z = 0
    for i, row in enumerate(C_rows):
        if popcount(row & x) & 1:
            z |= 1 << i
    return z


def row_noise_prob(row, p=0.25):
    """P((B e)_i = 1) for a row with Hamming weight k, e ~ Bernoulli(p)^{2n}."""
    k = popcount(row)
    return 0.5 * (1.0 - (1.0 - 2 * p) ** k)


class State:
    """Incremental state for P_red(C,z), marginal uniformity, and noise rate."""

    def __init__(self, n, m, A_list, e_probs):
        self.n = n
        self.m = m
        self.N = 2 * n
        self.A_list = A_list
        self.e_probs = e_probs
        self.num_A = len(A_list)
        self.p_A = 1.0 / self.num_A
        self.p_x = 1.0 / (1 << n)
        self.target = self.num_A / 2.0
        self.g = {}
        self.P_red = Counter()  # (C_tuple, z) -> prob
        self.P_C = Counter()    # C_tuple -> prob
        self.counts = [[0] * n for _ in range(m)]
        self.noise_sum_per_row = [0.0] * m  # sum over A of P(e'_i=1 | A)

    def init_random(self, rng):
        max_row = (1 << self.N) - 1
        for A in self.A_list:
            self.g[tuple(A)] = [rng.randint(0, max_row) for _ in range(self.m)]
        self._recompute_all()

    def _recompute_all(self):
        self.P_red.clear()
        self.P_C.clear()
        self.counts = [[0] * self.n for _ in range(self.m)]
        self.noise_sum_per_row = [0.0] * self.m
        for A in self.A_list:
            self._add_A(A, self.g[tuple(A)])

    def _add_A(self, A, B):
        key = tuple(A)
        A_rows = A
        C = compute_C(B, A_rows)
        p_A = self.p_A
        for j in range(self.n):
            for i in range(self.m):
                if (C[i] >> j) & 1:
                    self.counts[i][j] += 1
        for i, row in enumerate(B):
            self.noise_sum_per_row[i] += row_noise_prob(row)
        for e, p_e in self.e_probs.items():
            ep = compute_e_prime(B, e)
            p_base = p_A * p_e
            for x in range(1 << self.n):
                z = matvec(C, x) ^ ep
                p = p_base * self.p_x
                self.P_red[(C, z)] += p
                self.P_C[C] += p

    def _remove_A(self, A, B):
        key = tuple(A)
        A_rows = A
        C = compute_C(B, A_rows)
        p_A = self.p_A
        for j in range(self.n):
            for i in range(self.m):
                if (C[i] >> j) & 1:
                    self.counts[i][j] -= 1
        for i, row in enumerate(B):
            self.noise_sum_per_row[i] -= row_noise_prob(row)
        for e, p_e in self.e_probs.items():
            ep = compute_e_prime(B, e)
            p_base = p_A * p_e
            for x in range(1 << self.n):
                z = matvec(C, x) ^ ep
                p = p_base * self.p_x
                self.P_red[(C, z)] -= p
                if self.P_red[(C, z)] == 0:
                    del self.P_red[(C, z)]
                self.P_C[C] -= p
                if self.P_C[C] == 0:
                    del self.P_C[C]

    def update_A(self, A, old_B, new_B):
        self._remove_A(A, old_B)
        self._add_A(A, new_B)
        self.g[tuple(A)] = list(new_B)

    def marginal_cost(self):
        return sum(
            (self.counts[i][j] - self.target) ** 2
            for i in range(self.m)
            for j in range(self.n)
        )

    def noise_rates(self):
        return [s / self.num_A for s in self.noise_sum_per_row]

    def compute_SD(self):
        """SD(P_red(C,z), P_LPN(C,z)) with per-coordinate noise rates."""
        p_eta_per_coord = self.noise_rates()
        # precompute P_eta for all eta patterns
        eta_probs = {}
        for eta in range(1 << self.m):
            pr = 1.0
            for i in range(self.m):
                p = p_eta_per_coord[i]
                if (eta >> i) & 1:
                    pr *= p
                else:
                    pr *= (1 - p)
            eta_probs[eta] = pr

        P_LPN = Counter()
        for C, p_C in self.P_C.items():
            for x in range(1 << self.n):
                Cx = matvec(C, x)
                for eta, p_eta in eta_probs.items():
                    z = Cx ^ eta
                    P_LPN[(C, z)] += p_C * p_eta * self.p_x

        keys = set(self.P_red.keys()) | set(P_LPN.keys())
        sd = 0.0
        for key in keys:
            sd += abs(self.P_red.get(key, 0.0) - P_LPN.get(key, 0.0))
        return 0.5 * sd


def search_marginal_uniform(state, max_iters=2_000_000, seed=42):
    rng = random.Random(seed)
    state.init_random(rng)
    current_cost = state.marginal_cost()
    best_cost = current_cost
    for it in range(max_iters):
        if current_cost == 0:
            print(f"  Exact marginal uniformity reached at it {it}")
            return it
        A = rng.choice(state.A_list)
        row_idx = rng.randint(0, state.m - 1)
        bit_idx = rng.randint(0, state.N - 1)
        old_B = list(state.g[tuple(A)])
        new_B = list(old_B)
        new_B[row_idx] ^= (1 << bit_idx)
        state.update_A(A, old_B, new_B)
        new_cost = state.marginal_cost()
        if new_cost <= current_cost:
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                if it % 500_000 == 0:
                    print(f"  ...it {it}, cost={best_cost}")
        else:
            state.update_A(A, new_B, old_B)
    print(f"  Did not reach 0. Best cost={best_cost}")
    return -1


def simulated_annealing(state, max_iters, lam, T0, T_final, seed):
    rng = random.Random(seed)
    sd = state.compute_SD()
    marg = state.marginal_cost()
    E = sd + lam * marg
    best_sd = sd
    best_marg = marg
    best_E = E
    alpha = (T_final / T0) ** (1.0 / max_iters)
    T = T0
    start = time.time()

    for it in range(max_iters):
        if it > 0 and it % 100_000 == 0:
            elapsed = time.time() - start
            print(
                f"  ...it {it}, T={T:.6f}, SD={sd:.6f}, marg={marg:.1f}, "
                f"E={E:.6f}, best_SD={best_sd:.6f}, t={elapsed:.1f}s"
            )

        A = rng.choice(state.A_list)
        row_idx = rng.randint(0, state.m - 1)
        bit_idx = rng.randint(0, state.N - 1)

        old_B = list(state.g[tuple(A)])
        new_B = list(old_B)
        new_B[row_idx] ^= (1 << bit_idx)

        state.update_A(A, old_B, new_B)
        new_sd = state.compute_SD()
        new_marg = state.marginal_cost()
        new_E = new_sd + lam * new_marg
        dE = new_E - E

        if dE <= 0 or rng.random() < math.exp(-dE / T):
            sd = new_sd
            marg = new_marg
            E = new_E
            if sd < best_sd:
                improvement = best_sd - sd
                best_sd = sd
                best_marg = new_marg
                best_E = new_E
                if improvement > 0.001 or it % 50_000 == 0:
                    print(
                        f"  *** NEW BEST SD={best_sd:.6f}, marg={best_marg:.1f} at it {it}"
                    )
        else:
            state.update_A(A, new_B, old_B)

        T *= alpha

    return best_sd, best_marg, best_E


def main():
    import sys

    n = 2
    N = 2 * n
    e_probs = {
        e: (1 / 4) ** popcount(e) * (3 / 4) ** (N - popcount(e))
        for e in range(1 << N)
    }

    # Optional command-line: m and SA iterations
    if len(sys.argv) >= 2:
        ms = [int(sys.argv[1])]
    else:
        ms = [2, 3, 4]
    if len(sys.argv) >= 3:
        sa_iters = int(sys.argv[2])
    else:
        sa_iters = 500_000

    print(f"n={n}: Enumerating A matrices...")
    A_list = enumerate_all_A(n)
    print(f"  |A| = {len(A_list)}")

    results = []

    for m in ms:
        print(f"\n{'='*60}")
        print(f"m = {m} (hard window n <= m <= 2n)")

        # Baseline: random g
        state_rand = State(n, m, A_list, e_probs)
        state_rand.init_random(random.Random(42))
        sd_rand = state_rand.compute_SD()
        print(f"  Random g: SD={sd_rand:.6f}, marg={state_rand.marginal_cost()}")

        # Constrained search: marginal-uniform g, minimize SD
        print(f"\n  Constrained SA (lambda=10.0, marginal-uniform C), iters={sa_iters}")
        state = State(n, m, A_list, e_probs)
        it_mu = search_marginal_uniform(state, max_iters=2_000_000, seed=42)
        print(
            f"  Marginal-uniform search done ({it_mu} iters), "
            f"SD={state.compute_SD():.6f}, marg={state.marginal_cost()}"
        )
        best_sd, best_marg, best_E = simulated_annealing(
            state, sa_iters, 10.0, 0.05, 1e-5, seed=100
        )
        print(f"  SA result: SD={best_sd:.6f}, marg={best_marg}")

        results.append(
            {
                "m": m,
                "random_SD": sd_rand,
                "best_constrained_SD": best_sd,
                "best_marg": best_marg,
            }
        )

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for r in results:
        print(
            f"m={r['m']}: random SD={r['random_SD']:.6f}, "
            f"best constrained SD={r['best_constrained_SD']:.6f} "
            f"(marg={r['best_marg']})"
        )

    out_dir = Path("experiments/output")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "181-operational-distinguishing-SD-results.json"
    with open(out_file, "w") as f:
        json.dump({"n": n, "results": results}, f, indent=2)
    print(f"\nResults saved to {out_file}")


if __name__ == "__main__":
    main()
