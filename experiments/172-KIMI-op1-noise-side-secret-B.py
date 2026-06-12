#!/usr/bin/env python3
"""
Experiment 172: lem:m2 Step A — Noise side, SECRET-B regime (corrected formulation).

Core question: Is e' = Be detectably non-i.i.d. given ONLY C = BA (secret B)?

Model:
- A: public full-rank isotropic 2n x n matrix (enumerated or sampled)
- B: secret n x 2n matrix whose rows form an ordered basis of an isotropic subspace
- e: random noise vector ~ Bernoulli(1/4)^{2n}
- C = B * A (n x n, observed by adversary)
- e' = B * e (n-dim, the reduced noise)

Measurement: For each C, compare P(e' | C) vs P(e'). If they differ, C leaks info about e'.

Track A Step A3 per DIRECTIVE-KIMI-v3-frontier.md and adjudication ffeb134.
"""

import json
import random
from fractions import Fraction
from collections import defaultdict, Counter

def symplectic_form(v, w, n):
    """Omega(v,w) for standard symplectic form on F_2^{2n}."""
    low = ((1 << n) - 1)
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

def rref_canonical(rows, n_cols):
    rows = list(rows)
    pivots = {}
    pivot_rows = {}
    for i, v in enumerate(rows):
        x = v
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivot_rows[p]
        if x:
            p = x.bit_length() - 1
            pivots[p] = i
            pivot_rows[p] = x
            rows[i] = x
    for p in sorted(pivots.keys(), reverse=True):
        i = pivots[p]
        for k in range(len(rows)):
            if k != i and ((rows[k] >> p) & 1):
                rows[k] ^= rows[i]
    result = sorted([r for r in rows if r != 0])
    return tuple(result)

def enumerate_isotropic_subspaces(j, n):
    subspaces = set()
    dim_total = 2 * n
    def extend_basis(current):
        if len(current) == j:
            canonical = rref_canonical(current, dim_total)
            if len(canonical) == j:
                subspaces.add(canonical)
            return
        start = current[-1] + 1 if current else 1
        for v in range(start, 1 << dim_total):
            temp = list(current) + [v]
            if rank_rows(temp, dim_total) != len(temp):
                continue
            ok = True
            for b in current:
                if symplectic_form(v, b, n) != 0:
                    ok = False
                    break
            if ok:
                extend_basis(temp)
    extend_basis([])
    return [list(s) for s in sorted(subspaces)]

def enumerate_all_B(n):
    """Enumerate all n x 2n matrices B whose rows are ordered bases of isotropic subspaces."""
    # For lem:m2, B is typically an n x 2n matrix representing a Lagrangian basis
    # Actually, in the reduction B is m x 2n where m >= n. Let's use m = n for simplicity.
    # B's rows should be linearly independent and isotropic => B is a basis of an n-dim isotropic subspace
    subspaces = enumerate_isotropic_subspaces(n, n)
    B_list = []
    for basis in subspaces:
        # basis is n vectors in F_2^{2n}
        # Each ordered basis is a permutation of basis vectors
        from itertools import permutations
        for ordered in permutations(basis):
            B_list.append(list(ordered))
    return B_list

def mat_mul_mod2(B_rows, A_rows, n_rows_B, n_cols_B, n_cols_A):
    """Multiply B (n_rows_B x n_cols_B) by A (n_cols_B x n_cols_A) over F_2.
    B_rows[i] is n_cols_B-bit int, A_rows[j] is n_cols_A-bit int.
    Returns list of n_rows_B row vectors (each n_cols_A-bit int)."""
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

def mat_vec_mul_mod2(M_rows, v_int, n_rows, n_cols):
    """Multiply M (n_rows x n_cols) by vector v (n_cols bits) over F_2.
    M_rows[i] is n_cols-bit int."""
    res = 0
    for i in range(n_rows):
        val = 0
        for j in range(n_cols):
            if (M_rows[i] >> j) & 1 and (v_int >> j) & 1:
                val ^= 1
        if val:
            res |= (1 << i)
    return res

def vec_to_int(v):
    """Convert binary tuple to integer."""
    res = 0
    for i, b in enumerate(v):
        if b:
            res |= (1 << i)
    return res

def generate_gl(n):
    """Generate all GL(n,2) matrices as list of n row vectors (n-bit ints)."""
    from itertools import permutations
    gl = []
    for perm in permutations(range(2**n), n):
        if any(v == 0 for v in perm):
            continue
        # Check linear independence
        if rank_rows(list(perm), n) != n:
            continue
        gl.append(list(perm))
    return gl

def compute_A_from_G_R(G_rows, R_basis, n):
    """Compute A = (G * R)^T where G is n x n and R is n x 2n.
    Returns list of 2n row vectors (each is n-bit int)."""
    # G_rows[i] = i-th row of G as n-bit int
    # R_basis[k] = k-th row of R as 2n-bit int
    # (G*R)_{i,j} = sum_k G[i][k] * R[k][j]
    # A[j][i] = (G*R)_{i,j}
    dim = 2 * n
    A_rows = []
    for j in range(dim):
        # Column j of G*R
        col_j = 0
        for i in range(n):
            val = 0
            for k in range(n):
                g_ik = (G_rows[i] >> k) & 1
                r_kj = (R_basis[k] >> j) & 1
                val ^= g_ik & r_kj
            if val:
                col_j |= (1 << i)
        A_rows.append(col_j)
    return A_rows

def enumerate_all_A(n):
    """Enumerate all full-rank isotropic 2n x n matrices A."""
    # A = (G * R)^T where R is basis of Lagrangian, G in GL(n,2)
    subspaces = enumerate_isotropic_subspaces(n, n)
    gl_list = generate_gl(n)
    A_list = []
    for basis in subspaces:
        for G_rows in gl_list:
            A_rows = compute_A_from_G_R(G_rows, basis, n)
            A_list.append(A_rows)
    return A_list

def compute_secret_B_experiment(n, bernoulli_p=Fraction(1,4)):
    """Compute P(e' | C) vs P(e') for secret-B model at small n."""
    dim = 2 * n
    print(f"n={n}: Enumerating A and B matrices...")
    
    A_list = enumerate_all_A(n)
    B_list = enumerate_all_B(n)
    
    print(f"  |A| = {len(A_list)}, |B| = {len(B_list)}")
    
    # Joint distribution P(C, e')
    joint = Counter()  # (C_matrix, e_prime) -> count (weighted by e probability)
    marginal_e_prime = Counter()
    marginal_C = Counter()
    
    total_weight = Fraction(0)
    
    # Enumerate all e vectors with Bernoulli(1/4)^{2n} weight
    for e_int in range(1 << dim):
        # Weight of e under Bernoulli(p)^{2n}
        weight_num = 1
        weight_den = 1
        for coord in range(dim):
            if (e_int >> coord) & 1:
                weight_num *= bernoulli_p.numerator
                weight_den *= bernoulli_p.denominator
            else:
                weight_num *= (bernoulli_p.denominator - bernoulli_p.numerator)
                weight_den *= bernoulli_p.denominator
        weight = Fraction(weight_num, weight_den)
        
        for A_rows in A_list:
            for B_rows in B_list:
                # C = B * A (n x n), represented as n n-bit integers
                C_rows = mat_mul_mod2(B_rows, A_rows, n, dim, n)
                # e' = B * e, represented as n-bit integer
                e_prime_int = mat_vec_mul_mod2(B_rows, e_int, n, dim)
                
                C_tuple = tuple(C_rows)
                
                joint[(C_tuple, e_prime_int)] += weight
                marginal_e_prime[e_prime_int] += weight
                marginal_C[C_tuple] += weight
                total_weight += weight
    
    print(f"  Total weight = {total_weight} (should be |A|*|B|)")
    
    # Normalize
    for key in joint:
        joint[key] /= total_weight
    for key in marginal_e_prime:
        marginal_e_prime[key] /= total_weight
    for key in marginal_C:
        marginal_C[key] /= total_weight
    
    # Compute conditional P(e' | C)
    conditional = defaultdict(Counter)
    for (C_val, e_prime_val), prob in joint.items():
        conditional[C_val][e_prime_val] = prob / marginal_C[C_val]
    
    # Compute SD between P(e' | C) and P(e') for each C
    sd_by_C = {}
    for C_val in conditional:
        sd = Fraction(0)
        all_e_primes = set(conditional[C_val].keys()) | set(marginal_e_prime.keys())
        for e_prime_val in all_e_primes:
            p_cond = conditional[C_val].get(e_prime_val, Fraction(0))
            p_marg = marginal_e_prime.get(e_prime_val, Fraction(0))
            sd += abs(p_cond - p_marg)
        sd_by_C[C_val] = sd / 2
    
    # Average SD over C
    avg_sd = sum(sd_by_C[C_val] * marginal_C[C_val] for C_val in sd_by_C)
    
    # Max SD
    max_sd = max(sd_by_C.values()) if sd_by_C else Fraction(0)
    
    return {
        "n": n,
        "num_A": len(A_list),
        "num_B": len(B_list),
        "num_C_values": len(marginal_C),
        "num_e_prime_values": len(marginal_e_prime),
        "avg_sd": float(avg_sd),
        "max_sd": float(max_sd),
        "avg_sd_exact": str(avg_sd),
        "max_sd_exact": str(max_sd),
        "sd_by_C": {str(k): float(v) for k, v in sd_by_C.items()},
    }

if __name__ == "__main__":
    for n in [2, 3]:
        print(f"\n{'='*60}")
        print(f"Secret-B experiment: n={n}")
        print(f"{'='*60}")
        result = compute_secret_B_experiment(n)
        print(f"\nResults:")
        print(f"  Number of distinct C values: {result['num_C_values']}")
        print(f"  Number of distinct e' values: {result['num_e_prime_values']}")
        print(f"  Average SD(P(e'|C), P(e')): {result['avg_sd']:.10f}")
        print(f"  Max SD: {result['max_sd']:.10f}")
        print(f"  Average SD (exact): {result['avg_sd_exact']}")
        print(f"  Max SD (exact): {result['max_sd_exact']}")
        
        out_path = f"experiments/172-KIMI-op1-noise-side-secret-B-n{n}.json"
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Output written to {out_path}")
