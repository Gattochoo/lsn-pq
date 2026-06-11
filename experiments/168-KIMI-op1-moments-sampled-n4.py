#!/usr/bin/env python3
"""
Experiment 168: OP1 moments m_2, m_3 sampled estimation for n=4.

Efficient sampling via rejection: random isotropic ordered basis by checking
orthogonality and independence incrementally; random GL(n,2) by column-wise
rejection against span of previous columns.

Track A Step 5 continuation per DIRECTIVE-KIMI-v3-frontier.md.
"""

import json
import random
import time
from collections import Counter

# --- Fast symplectic form ---
def omega(v, w, n):
    """Standard symplectic form Omega(v,w) on F_2^{2n}."""
    low = ((1 << n) - 1)
    return (bin((v & low) & (w >> n)).count('1') ^ bin((v >> n) & (w & low)).count('1')) & 1

# --- Check if vector is in span ---
def in_span(vectors, candidate, n):
    """Check if candidate is in span(vectors) over F_2."""
    # Gaussian elimination on [vectors | candidate]
    rows = list(vectors)
    rows.append(candidate)
    pivots = {}
    for v in rows:
        x = v
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            p = x.bit_length() - 1
            pivots[p] = x
    # Candidate is dependent if after elimination, the last row contributes nothing new
    # Actually, we can just check rank: if rank([vectors]) == rank([vectors, candidate])
    rank_with = len(pivots)
    
    # Recompute rank of vectors alone
    pivots2 = {}
    for v in vectors:
        x = v
        for p in sorted(pivots2.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots2[p]
        if x:
            p = x.bit_length() - 1
            pivots2[p] = x
    rank_without = len(pivots2)
    
    return rank_with == rank_without

# --- Random isotropic ordered basis via rejection ---
def random_isotropic_basis(n):
    """Generate uniform random ordered basis of uniform random Lagrangian."""
    basis = []
    for i in range(n):
        # W = span(basis), dim = i
        # Need v in W^perp \ W
        # W^perp has size 2^{2n-i}, W has size 2^i
        # P(v in W^perp \ W) = (2^{2n-i} - 2^i) / 2^{2n}
        while True:
            v = random.getrandbits(2 * n)
            if v == 0:
                continue
            # Check v in W^perp
            in_perp = True
            for b in basis:
                if omega(v, b, n) != 0:
                    in_perp = False
                    break
            if not in_perp:
                continue
            # Check v not in W
            if in_span(basis, v, 2*n):
                continue
            basis.append(v)
            break
    return basis

# --- Random GL(n,2) via column-wise rejection ---
def random_gl(n):
    """Generate uniform random n x n invertible matrix over F_2."""
    cols = []
    for i in range(n):
        span_size = (1 << i)  # 2^i
        while True:
            c = random.getrandbits(n)
            if c == 0:
                continue
            if in_span(cols, c, n):
                continue
            cols.append(c)
            break
    # cols[j] is column j as n-bit integer (row 0 = LSB)
    # Matrix M where M[i][j] = bit i of cols[j]
    return cols

# --- Compute A = (G * V)^T and count t ---
def sample_t(n, basis, cols):
    """Given basis (list of n vectors in F_2^{2n}) and GL columns cols,
    return t = number of rows j in A=(G*V)^T with a_j[0]=a_j[1]=1."""
    dim = 2 * n
    # For each row j of A (which is column j of G*V):
    # A[j][i] = sum_k G[i][k] * V[k][j] = dot(row i of G, column j of V)
    # row i of G: [bit_i(cols[0]), bit_i(cols[1]), ..., bit_i(cols[n-1])]
    # column j of V: [bit_j(basis[0]), bit_j(basis[1]), ..., bit_j(basis[n-1])]
    # So A[j][i] = sum_k ((cols[k]>>i)&1) * ((basis[k]>>j)&1)
    
    # Precompute bit j of each basis vector
    # basis_bits[k][j] = (basis[k] >> j) & 1
    
    t = 0
    for j in range(dim):
        # Compute column j of V as list of bits
        v_col = 0
        for k in range(n):
            if (basis[k] >> j) & 1:
                v_col |= (1 << k)
        
        # Row j of A = G * v_col (matrix-vector over F_2)
        # G's columns are cols[0..n-1], each is n-bit int.
        # (G * v_col)[i] = sum_k G[i][k] * v_col[k]
        #                = sum_k ((cols[k] >> i) & 1) * ((v_col >> k) & 1)
        # We need i=0 and i=1
        a0 = 0
        a1 = 0
        for k in range(n):
            if (v_col >> k) & 1:
                a0 ^= (cols[k] >> 0) & 1
                a1 ^= (cols[k] >> 1) & 1
        
        if a0 and a1:
            t += 1
    return t

# --- Main ---
def estimate_moments(n, num_samples, seed=42):
    random.seed(seed)
    dim = 2 * n
    
    sum_ct1 = 0
    sum_ct2 = 0
    sum_ct3 = 0
    t_counter = Counter()
    
    start = time.time()
    report_interval = max(1, num_samples // 20)
    
    for s in range(num_samples):
        basis = random_isotropic_basis(n)
        cols = random_gl(n)
        t = sample_t(n, basis, cols)
        
        sum_ct1 += t
        sum_ct2 += t * (t - 1) // 2
        sum_ct3 += t * (t - 1) * (t - 2) // 6 if t >= 3 else 0
        t_counter[t] += 1
        
        if (s + 1) % report_interval == 0:
            elapsed = time.time() - start
            rate = (s + 1) / elapsed
            print(f"  {s+1:,} / {num_samples:,} ({100*(s+1)/num_samples:.0f}%) | {elapsed:.1f}s | {rate:.0f} samp/s")
    
    elapsed = time.time() - start
    
    m1_est = sum_ct1 / (num_samples * dim)
    m2_est = sum_ct2 / (num_samples * dim * (dim - 1) // 2)
    m3_est = sum_ct3 / (num_samples * dim * (dim - 1) * (dim - 2) // 6)
    
    # Standard errors via sample variance
    mean_ct1 = sum_ct1 / num_samples
    mean_ct2 = sum_ct2 / num_samples
    mean_ct3 = sum_ct3 / num_samples
    
    var_ct1 = sum((t - mean_ct1)**2 * cnt for t, cnt in t_counter.items()) / num_samples
    var_ct2 = sum((t*(t-1)//2 - mean_ct2)**2 * cnt for t, cnt in t_counter.items()) / num_samples
    var_ct3 = sum((t*(t-1)*(t-2)//6 - mean_ct3)**2 * cnt for t, cnt in t_counter.items()) / num_samples
    
    se_m1 = (var_ct1 / num_samples)**0.5 / dim
    se_m2 = (var_ct2 / num_samples)**0.5 / (dim * (dim - 1) // 2)
    se_m3 = (var_ct3 / num_samples)**0.5 / (dim * (dim - 1) * (dim - 2) // 6)
    
    return {
        "n": n,
        "num_samples": num_samples,
        "m1_est": m1_est,
        "m2_est": m2_est,
        "m3_est": m3_est,
        "se_m1": se_m1,
        "se_m2": se_m2,
        "se_m3": se_m3,
        "t_distribution": {str(k): v for k, v in sorted(t_counter.items())},
        "time_seconds": elapsed
    }

if __name__ == "__main__":
    n = 4
    num_samples = 10_000_000
    print(f"Estimating moments for n={n} with {num_samples:,} samples...")
    result = estimate_moments(n, num_samples)
    print(f"\nResults:")
    m1_closed = (2**(2*n - 2)) / (2**(2*n) - 1)
    print(f"  m1 = {result['m1_est']:.10f} ± {result['se_m1']:.10f}  (closed: {m1_closed:.10f})")
    print(f"  m2 = {result['m2_est']:.10f} ± {result['se_m2']:.10f}")
    print(f"  m3 = {result['m3_est']:.10f} ± {result['se_m3']:.10f}")
    print(f"\nTime: {result['time_seconds']:.1f}s")
    
    out_path = f"experiments/168-KIMI-op1-moments-sampled-n{n}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Output written to {out_path}")
