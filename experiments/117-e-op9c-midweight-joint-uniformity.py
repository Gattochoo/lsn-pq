#!/usr/bin/env python3
"""
E-OP9c: Mid-weight B sweep — joint uniformity + recovery.

G-MEASURE compliance: JOINT deterministic tests only.
  - Symmetry: C == C^T ?
  - Rank deficiency: rank(C) < n ?
  - Row correlation structure: distribution of pairwise dot products
NO per-row entropy (round-2 trap).

G-TARGET compliance: measure recoverability of x from y = Bx + e.
  - Brute-force search for small n.

Sweep: B rows have weight w = 1, 2, ..., n.
For each w, sample random B (m=n rows, each weight w).
Compare against uniform-random C baseline.
"""

import random
import itertools
from collections import Counter

def random_weight_w_vector(n2, w):
    """Random vector in F_2^{n2} with exactly weight w. n2 = 2n."""
    bits = random.sample(range(n2), w)
    v = 0
    for b in bits:
        v |= 1 << b
    return v

def mat_from_rows(rows, n):
    """rows: list of ints (n rows, each 2n bits). Return n×n matrix C = B' M."""
    # M maps x (n bits) to (x, x) in 2n bits... wait.
    # Actually M is the n×2n matrix [0 | I_n] in the isotropic basis.
    # For standard basis, M = [I_n | I_n].
    # C[i][j] = row_i · col_j(M) = row_i[n+j] (the (n+j)-th bit of row_i).
    C = []
    for r in rows:
        row = []
        for j in range(n):
            row.append((r >> (n + j)) & 1)
        C.append(row)
    return C

def mat_add(A, B):
    return [[a ^ b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def mat_transpose(A):
    n = len(A)
    return [[A[i][j] for i in range(n)] for j in range(n)]

def is_symmetric(A):
    return all(A[i][j] == A[j][i] for i in range(len(A)) for j in range(i, len(A)))

def mat_rank(A):
    """Gaussian elimination over F_2."""
    if not A or not A[0]:
        return 0
    n = len(A)
    m = len(A[0])
    M = [row[:] for row in A]
    rank = 0
    row = 0
    for col in range(m):
        pivot = None
        for r in range(row, n):
            if M[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            continue
        M[row], M[pivot] = M[pivot], M[row]
        for r in range(n):
            if r != row and M[r][col] == 1:
                for c in range(col, m):
                    M[r][c] ^= M[row][c]
        row += 1
        rank += 1
        if row == n:
            break
    return rank

def row_dot_products(C):
    """All pairwise dot products of rows (over F_2)."""
    n = len(C)
    dots = []
    for i in range(n):
        for j in range(i+1, n):
            dp = sum(C[i][k] & C[j][k] for k in range(n)) & 1
            dots.append(dp)
    return dots

def sample_B_random_weight(n, w):
    """Sample n rows, each with weight w in 2n bits."""
    return [random_weight_w_vector(2*n, w) for _ in range(n)]

def sample_C_uniform(n):
    """Sample uniform random n×n matrix over F_2."""
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def recovery_success(B_rows, x, p_noise, n):
    """Sample y = Bx + e, try to recover x by brute force."""
    # Compute Bx
    Bx = [0] * n
    for i in range(n):
        val = 0
        for j in range(n):
            if (x >> j) & 1:
                # Check if B_rows[i] has bit j set in bottom block
                val ^= (B_rows[i] >> (n + j)) & 1
        Bx[i] = val
    
    # Add noise
    y = [Bx[i] ^ (1 if random.random() < p_noise else 0) for i in range(n)]
    
    # Brute force search for x'
    best_x = 0
    best_dist = n + 1
    for x_guess in range(1 << n):
        # Compute B x_guess
        guess = [0] * n
        for i in range(n):
            val = 0
            for j in range(n):
                if (x_guess >> j) & 1:
                    val ^= (B_rows[i] >> (n + j)) & 1
            guess[i] = val
        dist = sum(guess[i] != y[i] for i in range(n))
        if dist < best_dist:
            best_dist = dist
            best_x = x_guess
    
    return best_x == x

def run_trial(n, w, p_noise, num_trials=100):
    sym_count = 0
    rank_full_count = 0
    all_dots = []
    rec_success = 0
    
    for _ in range(num_trials):
        B_rows = sample_B_random_weight(n, w)
        C = mat_from_rows(B_rows, n)
        
        if is_symmetric(C):
            sym_count += 1
        if mat_rank(C) == n:
            rank_full_count += 1
        all_dots.extend(row_dot_products(C))
        
        x = random.randint(0, (1 << n) - 1)
        if recovery_success(B_rows, x, p_noise, n):
            rec_success += 1
    
    return {
        'sym_rate': sym_count / num_trials,
        'rank_full_rate': rank_full_count / num_trials,
        'dot_dist': Counter(all_dots),
        'rec_rate': rec_success / num_trials,
    }

def run_uniform_baseline(n, num_trials=100):
    sym_count = 0
    rank_full_count = 0
    all_dots = []
    
    for _ in range(num_trials):
        C = sample_C_uniform(n)
        if is_symmetric(C):
            sym_count += 1
        if mat_rank(C) == n:
            rank_full_count += 1
        all_dots.extend(row_dot_products(C))
    
    return {
        'sym_rate': sym_count / num_trials,
        'rank_full_rate': rank_full_count / num_trials,
        'dot_dist': Counter(all_dots),
    }

if __name__ == "__main__":
    n = 6
    p_noise = 0.25
    num_trials = 200
    
    print(f"E-OP9c: n={n}, p={p_noise}, trials={num_trials}")
    print(f"{'w':>3} {'sym%':>6} {'rank=n%':>8} {'dot0/dot1':>12} {'rec%':>6}")
    print("-" * 45)
    
    # Uniform baseline
    base = run_uniform_baseline(n, num_trials)
    d0 = base['dot_dist'].get(0, 0)
    d1 = base['dot_dist'].get(1, 0)
    print(f"{'uni':>3} {base['sym_rate']*100:>6.1f} {base['rank_full_rate']*100:>8.1f} "
          f"{d0}/{d1:>5} {'N/A':>6}")
    
    for w in range(1, n+1):
        res = run_trial(n, w, p_noise, num_trials)
        d0 = res['dot_dist'].get(0, 0)
        d1 = res['dot_dist'].get(1, 1)
        print(f"{w:>3} {res['sym_rate']*100:>6.1f} {res['rank_full_rate']*100:>8.1f} "
              f"{d0}/{d1:>5} {res['rec_rate']*100:>6.1f}")
