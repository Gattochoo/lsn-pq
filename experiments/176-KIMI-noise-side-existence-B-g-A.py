#!/usr/bin/env python3
"""176: Search for B = g(A) with marginally-uniform BA + measure I(e';C).

Correct noise-side regime per Claude 2f81cb1:
  - m > 2n (confinement)
  - B = g(A) (deterministic, not independent)
  - C = BA marginally uniform
  - Measure: I(e'; C) = H(e') - H(e'|C)

Two phases:
  1. Local search for g with exact marginal uniformity.
  2. Exact computation of I(e';C) using the found g.

Status: DRAFT.
"""
import random
import math
from collections import Counter, defaultdict
from fractions import Fraction

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
            p = x.bit_length() - 1
            pivots[p] = x
    return len(pivots)

def enumerate_all_A(n):
    """Enumerate all full-rank isotropic 2n x n matrices A as list of row vectors."""
    N = 2 * n
    size = 1 << N
    
    # Generate all isotropic subspaces of dimension n
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
            ok = True
            for b in current:
                if symplectic_form(v, b, n) != 0:
                    ok = False
                    break
            if ok:
                extend_basis(temp)
    extend_basis([])
    
    # For each subspace, enumerate ordered bases
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

def mat_mul_mod2(B_rows, A_rows, n_rows_B, n_cols_B, n_cols_A):
    C_rows = []
    for i in range(n_rows_B):
        row = 0
        for j in range(n_cols_A):
            val = 0
            for k in range(n_cols_B):
                b_ik = (B_rows[i] >> k) & 1
                a_kj = (A_rows[k] >> j) & 1
                val ^= b_ik & a_kj
            if val:
                row |= (1 << j)
        C_rows.append(row)
    return C_rows

def search_g_of_A(n, m, max_iters=1_000_000, seed=42):
    rng = random.Random(seed)
    N = 2 * n
    
    print(f"n={n}, m={m}: Enumerating all A matrices...")
    A_list = enumerate_all_A(n)
    num_A = len(A_list)
    print(f"  |A| = {num_A}")
    
    target = num_A // 2
    if num_A % 2 != 0:
        print(f"  WARNING: |A|={num_A} is odd, exact marginal uniformity impossible")
        return None, A_list
    
    # Initialize random g
    g = {}
    for A in A_list:
        key = tuple(A)
        g[key] = [rng.randint(0, (1 << N) - 1) for _ in range(m)]
    
    def compute_counts():
        counts = [[0] * n for _ in range(m)]
        for A in A_list:
            key = tuple(A)
            B = g[key]
            C = mat_mul_mod2(B, A, m, N, n)
            for i in range(m):
                for j in range(n):
                    if (C[i] >> j) & 1:
                        counts[i][j] += 1
        return counts
    
    def cost(counts):
        return sum((counts[i][j] - target) ** 2 for i in range(m) for j in range(n))
    
    counts = compute_counts()
    current_cost = cost(counts)
    print(f"  Initial cost = {current_cost} (target = {target})")
    
    best_cost = current_cost
    best_g = {k: list(v) for k, v in g.items()}
    
    for it in range(max_iters):
        if current_cost == 0:
            print(f"  SUCCESS at iteration {it}")
            return g, A_list
        
        if it > 0 and it % 100_000 == 0:
            print(f"  ...iteration {it}, cost = {current_cost}, best = {best_cost}")
        
        A = rng.choice(A_list)
        key = tuple(A)
        row_idx = rng.randint(0, m - 1)
        bit_idx = rng.randint(0, N - 1)
        
        old_B_row = g[key][row_idx]
        new_B_row = old_B_row ^ (1 << bit_idx)
        g[key][row_idx] = new_B_row
        
        new_counts = compute_counts()
        new_cost = cost(new_counts)
        
        if new_cost <= current_cost:
            current_cost = new_cost
            counts = new_counts
            if new_cost < best_cost:
                best_cost = new_cost
                best_g = {k: list(v) for k, v in g.items()}
        else:
            g[key][row_idx] = old_B_row
    
    print(f"  FAILED after {max_iters} iterations. Best cost = {best_cost}")
    return None, A_list

def compute_mutual_info(n, m, g, A_list):
    """Exact computation of I(e'; C) using found g."""
    N = 2 * n
    
    # Precompute e probabilities: Bernoulli(1/4)^N
    e_probs = {}
    for e_int in range(1 << N):
        weight = bin(e_int).count('1')
        e_probs[e_int] = Fraction(1, 4) ** weight * Fraction(3, 4) ** (N - weight)
    
    # Build joint distribution P(C, e')
    joint = Counter()
    marginal_C = Counter()
    marginal_e_prime = Counter()
    total_prob = Fraction(0)
    
    for A in A_list:
        key = tuple(A)
        B = g[key]
        C = mat_mul_mod2(B, A, m, N, n)
        C_tuple = tuple(C)
        
        # A is uniform over |A| matrices
        p_A = Fraction(1, len(A_list))
        
        for e_int, p_e in e_probs.items():
            # Compute e' = B * e
            e_prime = 0
            for i in range(m):
                if bin(B[i] & e_int).count('1') & 1:
                    e_prime |= (1 << i)
            
            p = p_A * p_e
            joint[(C_tuple, e_prime)] += p
            marginal_C[C_tuple] += p
            marginal_e_prime[e_prime] += p
            total_prob += p
    
    # Normalize
    for k in joint:
        joint[k] /= total_prob
    for k in marginal_C:
        marginal_C[k] /= total_prob
    for k in marginal_e_prime:
        marginal_e_prime[k] /= total_prob
    
    # H(e')
    H_e_prime = 0.0
    for p in marginal_e_prime.values():
        if p > 0:
            H_e_prime -= float(p) * math.log2(float(p))
    
    # H(e'|C)
    H_e_prime_given_C = 0.0
    for C_tuple, p_C in marginal_C.items():
        conditional = {}
        for (C, e), p in joint.items():
            if C == C_tuple:
                conditional[e] = p / p_C
        H_cond = 0.0
        for p in conditional.values():
            if p > 0:
                H_cond -= float(p) * math.log2(float(p))
        H_e_prime_given_C += float(p_C) * H_cond
    
    I = H_e_prime - H_e_prime_given_C
    
    return {
        "n": n,
        "m": m,
        "num_A": len(A_list),
        "num_C": len(marginal_C),
        "num_e_prime": len(marginal_e_prime),
        "H_e_prime": H_e_prime,
        "H_e_prime_given_C": H_e_prime_given_C,
        "I_e_prime_C": I,
        "max_C_prob": float(max(marginal_C.values())),
        "max_e_prime_prob": float(max(marginal_e_prime.values())),
    }

if __name__ == "__main__":
    import json
    
    n, m = 2, 5
    g, A_list = search_g_of_A(n, m, max_iters=5_000_000, seed=42)
    
    if g:
        print("\nFound g with exact marginal uniformity!")
        result = compute_mutual_info(n, m, g, A_list)
        print(json.dumps(result, indent=2))
    else:
        print("\nNo g found in search budget.")
