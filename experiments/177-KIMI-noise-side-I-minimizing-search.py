#!/usr/bin/env python3
"""177: Search for g minimizing I(e';C) in correct regime (incremental update, fast).

Phase 1: Find marginal-uniform g.
Phase 2: Minimize I(e';C) with incremental updates (only A0 changes per step).

Status: DRAFT.
"""
import random
import math
import time
from collections import Counter

def symplectic_form(v, w, n):
    low = (1 << n) - 1
    return (bin((v & low) & (w >> n)).count('1') ^ bin((v >> n) & (w & low)).count('1')) & 1

def rank_rows(rows, n_cols):
    pivots = {}
    for v in rows:
        x = v
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1: x ^= pivots[p]
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
            if rank_rows(temp, N) != len(temp): continue
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
        
        # Remove old contributions
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
        
        # Add new contributions
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
        return sum((self.counts[i][j] - self.target) ** 2
                   for i in range(self.m) for j in range(self.n))

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

def minimize_I(state, max_iters=1_000_000, lambda_penalty=0.0, seed=42):
    rng = random.Random(seed)
    I = state.compute_I()
    marg = state.marginal_cost()
    current_combined = I + lambda_penalty * marg
    
    best_I = I
    best_marg = marg
    best_it = 0
    
    start = time.time()
    for it in range(max_iters):
        if it > 0 and it % 100_000 == 0:
            elapsed = time.time() - start
            print(f"  ...it {it}, I={I:.6f}, marg={marg}, best_I={best_I:.6f}, t={elapsed:.1f}s")
        
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
        new_combined = new_I + lambda_penalty * new_marg
        
        if new_combined <= current_combined or rng.random() < 0.001:
            I = new_I
            marg = new_marg
            current_combined = new_combined
            if I < best_I:
                best_I = I
                best_marg = marg
                best_it = it
                print(f"  *** NEW BEST I={best_I:.8f} at it {it} (marg={best_marg})")
        else:
            state._update_A(A, new_B, old_B)
    
    return best_I, best_marg, best_it

if __name__ == "__main__":
    n, m = 2, 5
    N = 2 * n
    
    print(f"Phase 1: Finding marginal-uniform g (n={n}, m={m})...")
    A_list = enumerate_all_A(n)
    print(f"  |A| = {len(A_list)}")
    
    e_probs = {e: (1/4) ** bin(e).count('1') * (3/4) ** (N - bin(e).count('1'))
               for e in range(1 << N)}
    
    state = State(n, m, A_list, e_probs)
    it_mu = search_marginal_uniform(state, max_iters=5_000_000, seed=42)
    if it_mu < 0:
        print("  Failed to find marginal-uniform g")
        exit(1)
    print(f"  Marginal-uniform g found in {it_mu} iterations")
    
    I_start = state.compute_I()
    print(f"\nPhase 2: Minimizing I (start I={I_start:.6f})...")
    
    for lam in [0.0, 0.1]:
        print(f"\n--- lambda = {lam} ---")
        # Restore marginal-uniform state
        state = State(n, m, A_list, e_probs)
        search_marginal_uniform(state, max_iters=5_000_000, seed=42)
        best_I, best_marg, best_it = minimize_I(
            state, max_iters=500_000, lambda_penalty=lam, seed=42+int(lam*100)
        )
        print(f"  Final: I={best_I:.8f}, marginal_cost={best_marg} (found at it {best_it})")
        if best_marg <= 10:
            print(f"  >>> Near-marginal-uniform with I={best_I:.8f}")
    
    print("\n" + "=" * 50)
    print("Search complete.")
