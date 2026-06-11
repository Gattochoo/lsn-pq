#!/usr/bin/env python3
"""178: Simulated annealing search for g minimizing I(e';C) under marginal-uniform C.

Extends 177 with SA to escape local minima. Explores trade-off between
I(e';C) and marginal-uniformity of C via penalty lambda * marginal_cost.

Run: python3 experiments/178-KIMI-noise-side-SA-search.py
Status: active.
"""
import random
import math
import time
import json
from collections import Counter
from pathlib import Path


def symplectic_form(v, w, n):
    low = (1 << n) - 1
    return (bin((v & low) & (w >> n)).count('1') ^ bin((v >> n) & (w & low)).count('1')) & 1


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


def compute_C_row(B_row, A_rows):
    row = 0
    b = B_row
    k = 0
    while b:
        if b & 1:
            row ^= A_rows[k]
        b >>= 1
        k += 1
    return row


def compute_e_prime_row(B_row, e_int):
    return bin(B_row & e_int).count('1') & 1


class State:
    def __init__(self, n, m, A_list, e_probs):
        self.n = n
        self.m = m
        self.N = 2 * n
        self.A_list = A_list
        self.e_probs = e_probs
        self.num_A = len(A_list)
        self.p_A = 1.0 / self.num_A
        self.target = self.num_A / 2
        self.g = {}
        self.joint = Counter()
        self.joint_by_C = {}
        self.marginal_C = Counter()
        self.marginal_e = Counter()
        self.counts = [[0] * n for _ in range(m)]

    def init_random(self, rng):
        for A in self.A_list:
            key = tuple(A)
            self.g[key] = [rng.randint(0, (1 << self.N) - 1) for _ in range(self.m)]
        self._recompute_all()

    def _recompute_all(self):
        self.joint.clear()
        self.joint_by_C = {}
        self.marginal_C.clear()
        self.marginal_e.clear()
        self.counts = [[0] * self.n for _ in range(self.m)]
        for A in self.A_list:
            key = tuple(A)
            B = self.g[key]
            C = [compute_C_row(B[i], A) for i in range(self.m)]
            C_tuple = tuple(C)
            for j in range(self.n):
                for i in range(self.m):
                    if (C[i] >> j) & 1:
                        self.counts[i][j] += 1
            for e_int, p_e in self.e_probs.items():
                p = self.p_A * p_e
                e_prime = 0
                for i in range(self.m):
                    if compute_e_prime_row(B[i], e_int):
                        e_prime |= (1 << i)
                self.joint[(C_tuple, e_prime)] += p
                if C_tuple not in self.joint_by_C:
                    self.joint_by_C[C_tuple] = Counter()
                self.joint_by_C[C_tuple][e_prime] += p
                self.marginal_C[C_tuple] += p
                self.marginal_e[e_prime] += p

    def _update_A(self, A, old_B, new_B):
        key = tuple(A)
        p_A = self.p_A
        old_C = [compute_C_row(old_B[i], A) for i in range(self.m)]
        old_C_tuple = tuple(old_C)
        for j in range(self.n):
            for i in range(self.m):
                if (old_C[i] >> j) & 1:
                    self.counts[i][j] -= 1
        for e_int, p_e in self.e_probs.items():
            p = p_A * p_e
            old_e_prime = 0
            for i in range(self.m):
                if compute_e_prime_row(old_B[i], e_int):
                    old_e_prime |= (1 << i)
            self.joint[(old_C_tuple, old_e_prime)] -= p
            self.marginal_C[old_C_tuple] -= p
            self.marginal_e[old_e_prime] -= p
            self.joint_by_C[old_C_tuple][old_e_prime] -= p
            if self.joint_by_C[old_C_tuple][old_e_prime] == 0:
                del self.joint_by_C[old_C_tuple][old_e_prime]
        new_C = [compute_C_row(new_B[i], A) for i in range(self.m)]
        new_C_tuple = tuple(new_C)
        for j in range(self.n):
            for i in range(self.m):
                if (new_C[i] >> j) & 1:
                    self.counts[i][j] += 1
        for e_int, p_e in self.e_probs.items():
            p = p_A * p_e
            new_e_prime = 0
            for i in range(self.m):
                if compute_e_prime_row(new_B[i], e_int):
                    new_e_prime |= (1 << i)
            self.joint[(new_C_tuple, new_e_prime)] += p
            self.marginal_C[new_C_tuple] += p
            self.marginal_e[new_e_prime] += p
            if new_C_tuple not in self.joint_by_C:
                self.joint_by_C[new_C_tuple] = Counter()
            self.joint_by_C[new_C_tuple][new_e_prime] += p
        self.g[key] = list(new_B)

    def compute_I(self):
        H_e = 0.0
        for p in self.marginal_e.values():
            if p > 0:
                H_e -= p * math.log2(p)
        H_e_given_C = 0.0
        for C_tuple, p_C in self.marginal_C.items():
            if p_C <= 0:
                continue
            H_cond = 0.0
            for e, p in self.joint_by_C.get(C_tuple, {}).items():
                if p > 0:
                    p_cond = p / p_C
                    H_cond -= p_cond * math.log2(p_cond)
            H_e_given_C += p_C * H_cond
        return H_e - H_e_given_C

    def marginal_cost(self):
        return sum(
            (self.counts[i][j] - self.target) ** 2
            for i in range(self.m)
            for j in range(self.n)
        )

    def get_g_dict(self):
        return {str(k): v for k, v in self.g.items()}


def search_marginal_uniform(state, max_iters=5_000_000, seed=42):
    rng = random.Random(seed)
    state.init_random(rng)
    current_cost = state.marginal_cost()
    for it in range(max_iters):
        if current_cost == 0:
            return it
        A = rng.choice(state.A_list)
        key = tuple(A)
        row_idx = rng.randint(0, state.m - 1)
        bit_idx = rng.randint(0, state.N - 1)
        old_B = list(state.g[key])
        new_B = list(old_B)
        new_B[row_idx] ^= (1 << bit_idx)
        state._update_A(A, old_B, new_B)
        new_cost = state.marginal_cost()
        if new_cost <= current_cost:
            current_cost = new_cost
        else:
            state._update_A(A, new_B, old_B)
    return -1


def simulated_annealing(state, max_iters, lam, T0, T_final, seed):
    rng = random.Random(seed)
    I = state.compute_I()
    marg = state.marginal_cost()
    E = I + lam * marg
    best_I = I
    best_marg = marg
    best_E = E
    best_g = state.get_g_dict()
    alpha = (T_final / T0) ** (1.0 / max_iters)
    T = T0
    start = time.time()

    for it in range(max_iters):
        if it > 0 and it % 500_000 == 0:
            elapsed = time.time() - start
            print(
                f"  ...it {it}, T={T:.6f}, I={I:.6f}, marg={marg}, "
                f"E={E:.6f}, best_I={best_I:.6f}, t={elapsed:.1f}s"
            )

        A = rng.choice(state.A_list)
        key = tuple(A)
        row_idx = rng.randint(0, state.m - 1)
        bit_idx = rng.randint(0, state.N - 1)

        old_B = list(state.g[key])
        new_B = list(old_B)
        new_B[row_idx] ^= (1 << bit_idx)

        state._update_A(A, old_B, new_B)
        new_I = state.compute_I()
        new_marg = state.marginal_cost()
        new_E = new_I + lam * new_marg
        dE = new_E - E

        if dE <= 0 or rng.random() < math.exp(-dE / T):
            I = new_I
            marg = new_marg
            E = new_E
            if I < best_I:
                best_I = I
                best_marg = marg
                best_E = new_E
                best_g = state.get_g_dict()
                print(f"  *** NEW BEST I={best_I:.8f}, marg={best_marg} at it {it}")
        else:
            state._update_A(A, new_B, old_B)

        T *= alpha

    return best_I, best_marg, best_E, best_g


def main():
    n, m = 2, 5
    N = 2 * n

    print(f"n={n}, m={m}: Enumerating A matrices...")
    A_list = enumerate_all_A(n)
    print(f"  |A| = {len(A_list)}")

    e_probs = {
        e: (1 / 4) ** bin(e).count('1') * (3 / 4) ** (N - bin(e).count('1'))
        for e in range(1 << N)
    }

    T0 = 0.1
    T_final = 1e-5
    max_iters = 1_000_000

    results = []
    best_overall = None

    # lambda=0 is unconstrained; for others we seed from a marginal-uniform g.
    for lam in [0.0, 0.05, 0.1, 0.2]:
        print(f"\n{'='*60}")
        print(f"lambda = {lam}")
        state = State(n, m, A_list, e_probs)
        if lam > 0:
            it_mu = search_marginal_uniform(state, max_iters=5_000_000, seed=42)
            print(
                f"  Marginal-uniform g found in {it_mu} iters, I={state.compute_I():.6f}"
            )
        else:
            state.init_random(random.Random(42))
            print(f"  Random init, I={state.compute_I():.6f}, marg={state.marginal_cost()}")

        seed = 1000 + int(lam * 1000)
        best_I, best_marg, best_E, best_g = simulated_annealing(
            state, max_iters, lam, T0, T_final, seed
        )
        print(f"  SA result: I={best_I:.8f}, marg={best_marg}, E={best_E:.8f}")
        results.append(
            {
                "lambda": lam,
                "best_I": best_I,
                "best_marg": best_marg,
                "best_E": best_E,
            }
        )
        if best_overall is None or best_I < best_overall["best_I"]:
            best_overall = {
                "lambda": lam,
                "best_I": best_I,
                "best_marg": best_marg,
                "best_g": best_g,
            }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for r in results:
        print(
            f"lambda={r['lambda']}: I={r['best_I']:.8f}, marg={r['best_marg']}"
        )

    print(
        f"\nOverall best I = {best_overall['best_I']:.8f} "
        f"(lambda={best_overall['lambda']}, marg={best_overall['best_marg']})"
    )

    out_dir = Path("experiments/output")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "178-sa-results.json"
    with open(out_file, "w") as f:
        json.dump(
            {
                "n": n,
                "m": m,
                "num_A": len(A_list),
                "results": results,
                "best_overall": {
                    k: v for k, v in best_overall.items() if k != "best_g"
                },
            },
            f,
            indent=2,
        )
    print(f"\nResults saved to {out_file}")


if __name__ == "__main__":
    main()
