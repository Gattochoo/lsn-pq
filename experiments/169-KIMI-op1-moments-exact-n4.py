#!/usr/bin/env python3
"""
Experiment 169: Exact moments m_1, m_2, m_3 for n=4 via direct enumeration of
2-dimensional isotropic subspaces and their ordered bases.

Key insight: (c_1,c_2) — the first two columns of A — is uniformly distributed over 
all ordered bases of all 2-dimensional isotropic subspaces of F_2^{2n}. This follows 
from Sp(2n) symmetry and the fact that each 2D isotropic W is contained in the same 
number of Lagrangians.

For each ordered basis (b_1,b_2), t = |supp(b_1) ∩ supp(b_2)|.
m_j = E[ C(t,j) ] / C(2n, j).

Track A Step 5 continuation per DIRECTIVE-KIMI-v3-frontier.md.
"""

import time
from fractions import Fraction
from itertools import permutations

def symplectic_form(v, w, n):
    """Omega(v,w) for standard symplectic form on F_2^{2n}."""
    low = ((1 << n) - 1)
    return (bin((v & low) & (w >> n)).count('1') ^ bin((v >> n) & (w & low)).count('1')) & 1

def num_isotropic_subspaces(j, n):
    """Number of j-dimensional isotropic subspaces of F_2^{2n}."""
    num = 1
    den = 1
    for i in range(j):
        num *= (2**(2*n - i) - 2**i)
        den *= (2**j - 2**i)
    return num // den

def num_ordered_bases(j):
    """Number of ordered bases of a j-dim vector space over F_2."""
    res = 1
    for i in range(j):
        res *= (2**j - 2**i)
    return res

def rref_canonical(rows, n_cols):
    """Compute RREF over F_2 and return canonical tuple of rows."""
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
    """Enumerate all j-dim isotropic subspaces of F_2^{2n}.
    Returns list of subspaces, each as a list of basis vectors (RREF form)."""
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

def rank_rows(rows, n_cols):
    """Compute rank of a list of row vectors."""
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

def compute_all_moments(n):
    """Compute m_1, m_2, m_3 exactly for given n."""
    dim = 2 * n
    j = 2  # We always enumerate 2D isotropic subspaces since t uses two columns
    print(f"Enumerating {j}-dim isotropic subspaces for n={n}...")
    
    subspaces = enumerate_isotropic_subspaces(j, n)
    expected = num_isotropic_subspaces(j, n)
    print(f"  Found {len(subspaces)} subspaces (expected: {expected})")
    assert len(subspaces) == expected, f"Mismatch: {len(subspaces)} != {expected}"
    
    num_bases = num_ordered_bases(j)
    total = expected * num_bases
    print(f"  Ordered bases per subspace: {num_bases}, total: {total}")
    
    sum_ct1 = Fraction(0)
    sum_ct2 = Fraction(0)
    sum_ct3 = Fraction(0)
    
    start = time.time()
    report_interval = max(1, expected // 10)
    
    print("  Computing C(t,j)...")
    for idx, basis in enumerate(subspaces):
        # Generate all vectors in the subspace
        vectors = [0]
        for v in basis:
            new_vecs = []
            for existing in vectors:
                new_vecs.append(existing ^ v)
            vectors.extend(new_vecs)
        vectors = list(set(vectors))
        
        # Generate all ordered 2-tuples of linearly independent vectors
        for ordered in permutations(vectors, 2):
            if 0 in ordered:
                continue
            if rank_rows(list(ordered), dim) != 2:
                continue
            t = 0
            for coord in range(dim):
                if all((v >> coord) & 1 for v in ordered):
                    t += 1
            sum_ct1 += Fraction(t)
            sum_ct2 += Fraction(t * (t - 1), 2)
            sum_ct3 += Fraction(t * (t - 1) * (t - 2), 6)
        if (idx + 1) % report_interval == 0:
            print(f"    Subspace {idx+1}/{expected}")
    
    elapsed = time.time() - start
    print(f"  Done in {elapsed:.1f}s")
    
    m1 = (sum_ct1 / total) / Fraction(dim)
    m2 = (sum_ct2 / total) / Fraction(dim * (dim - 1), 2)
    m3 = (sum_ct3 / total) / Fraction(dim * (dim - 1) * (dim - 2), 6)
    
    return m1, m2, m3, sum_ct1, sum_ct2, sum_ct3, total

if __name__ == "__main__":
    for n in [2, 3, 4]:
        print(f"\n{'='*50}")
        print(f"n = {n}")
        print(f"{'='*50}")
        m1, m2, m3, s1, s2, s3, total = compute_all_moments(n)
        print(f"\nm_1 = {m1} = {float(m1):.10f}")
        print(f"  closed form = {Fraction(2**(2*n-2), 2**(2*n)-1)} = {float(Fraction(2**(2*n-2), 2**(2*n)-1)):.10f}")
        print(f"m_2 = {m2} = {float(m2):.10f}")
        print(f"m_3 = {m3} = {float(m3):.10f}")
