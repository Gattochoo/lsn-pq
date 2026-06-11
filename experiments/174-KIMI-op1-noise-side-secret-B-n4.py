#!/usr/bin/env python3
"""174: Secret-B noise side — n=4 Monte Carlo sampling (OPTIMIZED).

Measures SD(P(e'|C), P(e')) where e'=Be, C=BA, B secret.
Optimized: bit-XOR matrix mult, parity lookup, pre-generated pools.
"""
import random
import time
from collections import defaultdict, Counter

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

def random_isotropic_basis(dim, n, rng):
    basis = []
    max_v = (1 << (2 * n)) - 1
    for _ in range(dim):
        while True:
            v = rng.randint(1, max_v)
            ok = True
            for b in basis:
                if symplectic_form(v, b, n) != 0:
                    ok = False
                    break
            if not ok:
                continue
            if rank_rows(basis + [v], 2 * n) == len(basis) + 1:
                basis.append(v)
                break
    return basis

def build_A_from_columns(cols, n):
    A_rows = []
    for j in range(2 * n):
        row = 0
        for k in range(n):
            if (cols[k] >> j) & 1:
                row |= (1 << k)
        A_rows.append(row)
    return A_rows

def compute_C_rows(B_rows, A_rows, n):
    """C = B * A where B is n x 2n, A is 2n x n. C_rows[i] = XOR of A_rows[k] where B_ik=1."""
    C_rows = []
    mask = (1 << n) - 1
    for i in range(n):
        row = 0
        b = B_rows[i]
        k = 0
        while b:
            if b & 1:
                row ^= A_rows[k]
            b >>= 1
            k += 1
        C_rows.append(row & mask)
    return C_rows

def compute_e_prime(B_rows, e_int, n):
    """e' = B * e where B is n x 2n, e is 2n-dim."""
    res = 0
    for i in range(n):
        if bin(B_rows[i] & e_int).count('1') & 1:
            res |= (1 << i)
    return res

def compute_sd(n, num_samples, pool_size, seed=42):
    rng = random.Random(seed)
    dim = 2 * n
    mask = (1 << n) - 1

    print(f"n={n}: Pre-generating pools of size {pool_size}...")
    A_pool = []
    for _ in range(pool_size):
        A_cols = random_isotropic_basis(n, n, rng)
        A_pool.append(build_A_from_columns(A_cols, n))

    B_pool = []
    for _ in range(pool_size):
        B_pool.append(random_isotropic_basis(n, n, rng))

    joint = Counter()
    marginal_e_prime = Counter()
    marginal_C = Counter()

    print(f"n={n}: Generating {num_samples} samples...")
    start = time.time()
    for idx in range(num_samples):
        if idx > 0 and idx % 1_000_000 == 0:
            elapsed = time.time() - start
            print(f"  ...{idx//1_000_000}M samples in {elapsed:.1f}s")

        A_rows = rng.choice(A_pool)
        B_rows = rng.choice(B_pool)

        # Sample e ~ Bernoulli(1/4)^{2n}
        e_int = 0
        for coord in range(dim):
            if rng.random() < 0.25:
                e_int |= (1 << coord)

        C_rows = compute_C_rows(B_rows, A_rows, n)
        e_prime_int = compute_e_prime(B_rows, e_int, n)
        C_tuple = tuple(C_rows)

        joint[(C_tuple, e_prime_int)] += 1
        marginal_e_prime[e_prime_int] += 1
        marginal_C[C_tuple] += 1

    # Normalize
    total = num_samples
    for key in joint:
        joint[key] /= total
    for key in marginal_e_prime:
        marginal_e_prime[key] /= total
    for key in marginal_C:
        marginal_C[key] /= total

    # Conditional P(e'|C)
    conditional = defaultdict(Counter)
    for (C_val, e_prime_val), prob in joint.items():
        conditional[C_val][e_prime_val] = prob / marginal_C[C_val]

    # SD for each C
    sd_by_C = {}
    for C_val in conditional:
        sd = 0.0
        all_e = set(conditional[C_val].keys()) | set(marginal_e_prime.keys())
        for e_prime_val in all_e:
            p_cond = conditional[C_val].get(e_prime_val, 0.0)
            p_marg = marginal_e_prime.get(e_prime_val, 0.0)
            sd += abs(p_cond - p_marg)
        sd_by_C[C_val] = sd / 2

    avg_sd = sum(sd_by_C[C_val] * marginal_C[C_val] for C_val in sd_by_C)
    max_sd = max(sd_by_C.values()) if sd_by_C else 0.0

    return {
        "n": n,
        "num_samples": num_samples,
        "pool_size": pool_size,
        "num_C": len(marginal_C),
        "num_e_prime": len(marginal_e_prime),
        "avg_sd": avg_sd,
        "max_sd": max_sd,
    }

if __name__ == "__main__":
    import json
    result = compute_sd(n=4, num_samples=20_000_000, pool_size=5000, seed=42)
    print(json.dumps(result, indent=2))
