#!/usr/bin/env python3
"""
P10: Multi-sample rank detector when A is randomized per output.
Tests whether rank detection still works if each sample uses fresh (A_i, B_i).
If randomized A defeats the detector, multi-sample detection requires fixed (A,B).
"""

import random
import sys
sys.path.insert(0, 'experiments')

# Reuse helpers from 99-multisample-detector.py
exec(open('experiments/99-multisample-detector.py').read().replace('if __name__ == "__main__":', 'if False:'))

def sample_P0_randomized_A(n, m, p):
    """P0 with fresh A per output. Returns single (C, y) pair."""
    M_rows = random_symmetric_matrix_rows(n)
    A = isotropic_basis_from_symmetric(M_rows, n)
    B = [random.getrandbits(2 * n) for _ in range(m)]
    C = []
    for i in range(m):
        c_row = 0
        for t in range(2 * n):
            if (B[i] >> t) & 1:
                c_row ^= A[t]
        C.append(c_row)
    x = random.getrandbits(n)
    e = 0
    for t in range(2 * n):
        if random.random() < p:
            e |= (1 << t)
    y = 0
    for i in range(m):
        val = dot_parity(C[i], x)
        val ^= dot_parity(B[i], e)
        if val:
            y |= (1 << i)
    return C, y

def sample_P1(m, n, p):
    """Standard LPN single sample."""
    C_prime = [random.getrandbits(n) for _ in range(m)]
    x_prime = random.getrandbits(n)
    e = 0
    for t in range(m):
        if random.random() < p:
            e |= (1 << t)
    y_prime = 0
    for i in range(m):
        val = dot_parity(C_prime[i], x_prime)
        if (e >> i) & 1:
            val ^= 1
        if val:
            y_prime |= (1 << i)
    return C_prime, y_prime

def multi_sample_rank_P0_randomized(n, m, p, k):
    """Collect k P0 samples with independent A each, return rank of [y_1 | ... | y_k]."""
    ys = []
    for _ in range(k):
        _, y = sample_P0_randomized_A(n, m, p)
        ys.append(y)
    matrix_rows = []
    for bit in range(m):
        row = 0
        for sample_idx, y in enumerate(ys):
            if (y >> bit) & 1:
                row |= (1 << sample_idx)
        matrix_rows.append(row)
    return gf2_rank(matrix_rows)

def multi_sample_rank_P1(m, n, p, k):
    """Collect k P1 samples, return rank of [y_1 | ... | y_k]."""
    ys = []
    for _ in range(k):
        _, y = sample_P1(m, n, p)
        ys.append(y)
    matrix_rows = []
    for bit in range(m):
        row = 0
        for sample_idx, y in enumerate(ys):
            if (y >> bit) & 1:
                row |= (1 << sample_idx)
        matrix_rows.append(row)
    return gf2_rank(matrix_rows)

def run_test(n, m, p, k, trials=200):
    ranks_P0 = [multi_sample_rank_P0_randomized(n, m, p, k) for _ in range(trials)]
    ranks_P1 = [multi_sample_rank_P1(m, n, p, k) for _ in range(trials)]
    return ranks_P0, ranks_P1

if __name__ == "__main__":
    random.seed(0x5E1F)
    n, m, p, k = 6, 30, 0.25, 20
    print(f"Multi-sample rank detection with RANDOMIZED A per output")
    print(f"n={n}, m={m}, p={p}, k={k}, trials=200")
    ranks_P0, ranks_P1 = run_test(n, m, p, k, 200)
    print(f"P0 rank: mean={sum(ranks_P0)/len(ranks_P0):.1f}, max={max(ranks_P0)}, min={min(ranks_P0)}")
    print(f"P1 rank: mean={sum(ranks_P1)/len(ranks_P1):.1f}, max={max(ranks_P1)}, min={min(ranks_P1)}")
    
    # Compare to fixed-A case (from 99-multisample-detector.py)
    print("\nFor comparison, fixed-A case from 99-multisample-detector.py:")
    print("P0 rank: mean=12.0, max=12, min=12")
    print("P1 rank: mean=20.0, max=20, min=20")
