#!/usr/bin/env python3
"""
R2a: LSN sample-complexity brute-force curve for n=3,4,5.
Measures empirical recovery threshold vs the theoretical 2^{2n} floor.
"""

import itertools
import random
import numpy as np
from collections import defaultdict
import json
import sys

def bits(x, width):
    """Return list of bits of x, LSB first."""
    return [(x >> i) & 1 for i in range(width)]

def symplectic_form(x, y, n):
    """Omega(x,y) over F_2^{2n}."""
    s = 0
    for i in range(n):
        b1 = ((x >> (2*i)) & 1) * ((y >> (2*i + 1)) & 1)
        b2 = ((x >> (2*i + 1)) & 1) * ((y >> (2*i)) & 1)
        s ^= b1 ^ b2
    return s

def gf2_rank(matrix):
    """Compute rank of binary matrix (list of int bitmasks)."""
    m = list(matrix)
    rank = 0
    row = 0
    col = max(m).bit_length() if m else 0
    for c in range(col - 1, -1, -1):
        pivot = None
        for r in range(row, len(m)):
            if (m[r] >> c) & 1:
                pivot = r
                break
        if pivot is None:
            continue
        m[row], m[pivot] = m[pivot], m[row]
        for r in range(len(m)):
            if r != row and ((m[r] >> c) & 1):
                m[r] ^= m[row]
        rank += 1
        row += 1
        if row >= len(m):
            break
    return rank

def span_of(vectors, total_dim):
    """Return set of all vectors in the span of given vectors."""
    span_set = {0}
    for v in vectors:
        new = set()
        for s in span_set:
            new.add(s ^ v)
        span_set.update(new)
    return span_set

def is_isotropic(subspace_set, n):
    """Check if all pairs in subspace are orthogonal."""
    vecs = list(subspace_set)
    for i in range(len(vecs)):
        for j in range(i, len(vecs)):
            if symplectic_form(vecs[i], vecs[j], n) != 0:
                return False
    return True

def canonical_basis(subspace_set, total_dim):
    """Return canonical basis (RREF rows) for subspace."""
    vecs = sorted(subspace_set)
    # Gaussian elimination to get basis
    basis = []
    used = set()
    for col in range(total_dim - 1, -1, -1):
        for v in vecs:
            if v in used:
                continue
            if (v >> col) & 1:
                # Make pivot
                pivot = v
                basis.append(pivot)
                used.add(pivot)
                # Eliminate this column from others
                new_vecs = []
                for w in vecs:
                    if w != pivot and ((w >> col) & 1):
                        new_vecs.append(w ^ pivot)
                    else:
                        new_vecs.append(w)
                vecs = new_vecs
                break
    # Sort and clean
    basis = sorted(set(basis))
    return tuple(basis)

def enumerate_lagrangians(n):
    """Enumerate all Lagrangians in F_2^{2n}."""
    total_dim = 2 * n
    all_nonzero = list(range(1, 2 ** total_dim))
    lagrangians = []
    seen = set()
    
    count = 0
    for combo in itertools.combinations(all_nonzero, n):
        count += 1
        # Check independence
        if gf2_rank(list(combo)) < n:
            continue
        span = span_of(combo, total_dim)
        if len(span) != 2 ** n:
            continue
        can = canonical_basis(span, total_dim)
        if can in seen:
            continue
        seen.add(can)
        if is_isotropic(span, n):
            lagrangians.append(frozenset(span))
    
    print(f"  n={n}: checked {count} combos, found {len(lagrangians)} Lagrangians (expected {lagr_count(n)})")
    return lagrangians

def lagr_count(n):
    """|Lagr(2n, F_2)| = prod(2^i + 1)."""
    total = 1
    for i in range(1, n + 1):
        total *= (2 ** i + 1)
    return total

def sample_lsn(L_set, m, p, n, total_dim):
    """Generate m LSN samples for secret L."""
    samples = []
    for _ in range(m):
        a = random.randint(0, 2 ** total_dim - 1)
        e = 1 if random.random() < p else 0
        b = (1 if a in L_set else 0) ^ e
        samples.append((a, b))
    return samples

def brute_force_decode(samples, lagrangians, n):
    """Find Lagrangian with max agreement."""
    best_L = None
    best_score = -1
    for L in lagrangians:
        score = 0
        for a, b in samples:
            pred = 1 if a in L else 0
            if pred == b:
                score += 1
        if score > best_score:
            best_score = score
            best_L = L
    return best_L, best_score

def run_trials(n, m, num_trials, p, lagrangians):
    total_dim = 2 * n
    success = 0
    for t in range(num_trials):
        L_secret = random.choice(lagrangians)
        samples = sample_lsn(L_secret, m, p, n, total_dim)
        L_guess, score = brute_force_decode(samples, lagrangians, n)
        if L_guess == L_secret:
            success += 1
    return success / num_trials

def main():
    random.seed(42)
    p = 0.25
    
    results = {}
    
    for n in [3, 4]:
        print(f"\n=== n={n} ===")
        print("  Enumerating Lagrangians...")
        lagrangians = enumerate_lagrangians(n)
        expected = lagr_count(n)
        assert len(lagrangians) == expected, f"Mismatch: {len(lagrangians)} != {expected}"
        
        # Convert to list of sets for fast membership
        lagrangians = [frozenset(L) for L in lagrangians]
        
        # Sample complexity sweep
        m_values = []
        base = 2 ** (2 * n)
        for k in [-2, -1, 0, 1, 2]:
            m_values.append(int(base * (2 ** k)))
        
        print(f"  Testing m values: {m_values}")
        num_trials = 50 if n == 3 else 20
        
        success_rates = []
        for m in m_values:
            rate = run_trials(n, m, num_trials, p, lagrangians)
            success_rates.append(rate)
            print(f"    m={m:5d} (={m/base:.2f}*2^{{2n}}): success={rate:.2%}")
        
        results[n] = {
            "m_values": m_values,
            "success_rates": success_rates,
            "num_trials": num_trials,
            "p": p,
            "num_lagrangians": len(lagrangians)
        }
    
    # Save results
    out_path = "/Users/gatto/projects/TRIARC-main/.claude/worktrees/hardness-7th-shared/lsn-experiments/71-lsn-sample-complexity-results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    for n, data in results.items():
        print(f"n={n}: |Lagr|={data['num_lagrangians']}")
        for m, rate in zip(data["m_values"], data["success_rates"]):
            ratio = m / (2 ** (2*n))
            print(f"  m={m:5d} (ratio={ratio:.2f}): {rate:.1%}")

if __name__ == "__main__":
    main()
