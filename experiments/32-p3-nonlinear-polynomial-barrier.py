"""
Experiment 32: P3 Non-Linear Reduction — Polynomial Representation Barrier

Core insight: 1_L(x) = prod_{i=1}^n (1 + <w_i, x>) is a degree-n polynomial.
Any LPN reduction must write 1_L(x) = <s, phi(x)> + error.
If phi has degree D < n, exact representation is impossible.
If phi has degree n, secret dimension M = C(2n, <=n) ~ 2^{2n-1}, exponential blowup.

This script verifies the polynomial structure and computes approximation errors.
"""

import numpy as np
from itertools import combinations, product
from math import comb

def dot(a, b):
    return sum(x * y for x, y in zip(a, b)) % 2

def find_orthogonal_complement(n, L_basis):
    """
    Find basis of L^perp (standard dot product) for L = span(L_basis).
    V = F_2^{2n}.
    """
    dim = 2 * n
    # Gaussian elimination to find nullspace of matrix with rows = L_basis
    M = np.array(L_basis, dtype=int)
    # Row reduce
    rows, cols = M.shape
    r = 0
    pivots = []
    for c in range(cols):
        # Find pivot
        pivot = None
        for i in range(r, rows):
            if M[i, c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        # Swap
        M[[r, pivot]] = M[[pivot, r]]
        pivots.append(c)
        # Eliminate
        for i in range(rows):
            if i != r and M[i, c] == 1:
                M[i] ^= M[r]
        r += 1
    
    # Nullspace basis: for each free variable, set it to 1 and solve
    free_vars = [c for c in range(cols) if c not in pivots]
    null_basis = []
    for fv in free_vars:
        vec = np.zeros(cols, dtype=int)
        vec[fv] = 1
        for i, p in enumerate(pivots):
            if M[i, fv] == 1:
                vec[p] = 1
        null_basis.append(vec)
    return null_basis

def lagrangian_to_polynomial(n, L_basis):
    """
    1_L(x) = prod_{i=1}^n (1 + <w_i, x>) where {w_i} is basis of L^perp.
    Returns: dict mapping monomial (tuple of variable indices) to coefficient.
    """
    w_basis = find_orthogonal_complement(n, L_basis)
    assert len(w_basis) == n, f"Expected {n} basis vectors, got {len(w_basis)}"
    
    # Expand product
    poly = {}
    for mask in range(1 << n):
        # Term: prod_{i in mask} <w_i, x>
        # Each <w_i, x> = sum_j w_i[j] x_j
        # Product is sum over all combinations of picking one x_j from each factor
        # But since we're over F_2, x_j^2 = x_j, so we track which variables appear odd number of times
        from itertools import product as itproduct
        factors = []
        for i in range(n):
            if mask & (1 << i):
                w = w_basis[i]
                vars_in_factor = [j for j in range(2*n) if w[j] == 1]
                factors.append(vars_in_factor)
        
        if not factors:
            # Empty product = 1
            monomial = tuple()
            poly[monomial] = poly.get(monomial, 0) ^ 1
            continue
        
        # Cartesian product of factors
        for combo in itproduct(*factors):
            # Count occurrences of each variable mod 2
            var_count = {}
            for v in combo:
                var_count[v] = var_count.get(v, 0) + 1
            monomial = tuple(sorted([v for v, c in var_count.items() if c % 2 == 1]))
            poly[monomial] = poly.get(monomial, 0) ^ 1
    
    # Remove zero coefficients
    poly = {m: c for m, c in poly.items() if c == 1}
    return poly

def evaluate_polynomial(poly, x):
    """Evaluate polynomial at point x (mod 2)."""
    result = 0
    for monomial, coeff in poly.items():
        if coeff == 1:
            term = 1
            for v in monomial:
                term &= x[v]
            result ^= term
    return result

def test_exactness(n, L_basis):
    """Verify that the polynomial exactly equals 1_L."""
    poly = lagrangian_to_polynomial(n, L_basis)
    
    # Compute L
    L = set()
    for mask in range(1 << len(L_basis)):
        vec = np.zeros(2*n, dtype=int)
        for i in range(len(L_basis)):
            if mask & (1 << i):
                vec ^= L_basis[i]
        L.add(tuple(vec))
    
    errors = 0
    for x_bits in product([0, 1], repeat=2*n):
        x = list(x_bits)
        poly_val = evaluate_polynomial(poly, x)
        indicator = 1 if x_bits in L else 0
        if poly_val != indicator:
            errors += 1
    
    return errors, poly

def low_degree_approximation_error(n, poly, max_degree):
    """
    Compute truncation error: drop all terms of degree > max_degree.
    Also try greedy selection of most-correlated monomials.
    """
    dim = 2 * n
    
    # Target truth table
    target = []
    for x_bits in product([0, 1], repeat=dim):
        x = list(x_bits)
        target.append(evaluate_polynomial(poly, x))
    
    # Method 1: Truncation (drop high-degree terms)
    trunc_poly = {m: c for m, c in poly.items() if len(m) <= max_degree}
    trunc_tt = []
    for x_bits in product([0, 1], repeat=dim):
        x = list(x_bits)
        trunc_tt.append(evaluate_polynomial(trunc_poly, x))
    trunc_error = sum(a != t for a, t in zip(trunc_tt, target))
    
    # Method 2: Greedy selection of monomials (up to 100 iterations)
    all_monomials = []
    for d in range(max_degree + 1):
        for combo in combinations(range(dim), d):
            all_monomials.append(combo)
    
    # Precompute truth tables
    truth_tables = {}
    for mono in all_monomials:
        tt = []
        for x_bits in product([0, 1], repeat=dim):
            x = list(x_bits)
            val = 1
            for v in mono:
                val &= x[v]
            tt.append(val)
        truth_tables[mono] = tt
    
    # Greedy: start with empty, add monomial that most reduces error
    current_tt = [0] * len(target)
    selected = set()
    greedy_error = sum(a != t for a, t in zip(current_tt, target))
    
    for _ in range(min(100, len(all_monomials))):
        best_mono = None
        best_improvement = 0
        for mono in all_monomials:
            if mono in selected:
                continue
            tt = truth_tables[mono]
            # Compute new error if we add this monomial
            new_tt = [c ^ t for c, t in zip(current_tt, tt)]
            new_error = sum(a != t for a, t in zip(new_tt, target))
            improvement = greedy_error - new_error
            if improvement > best_improvement:
                best_improvement = improvement
                best_mono = mono
        
        if best_mono is None or best_improvement <= 0:
            break
        
        selected.add(best_mono)
        current_tt = [c ^ t for c, t in zip(current_tt, truth_tables[best_mono])]
        greedy_error = sum(a != t for a, t in zip(current_tt, target))
    
    return trunc_error, greedy_error, len(all_monomials)

def main():
    print("=" * 70)
    print("P3: Non-Linear Reduction — Polynomial Representation Barrier")
    print("=" * 70)
    
    for n in range(2, 5):
        print(f"\n--- n = {n} ---")
        dim = 2 * n
        
        # Standard Lagrangian: L = span{e_1, ..., e_n}
        L_basis = []
        for i in range(n):
            vec = np.zeros(dim, dtype=int)
            vec[i] = 1
            L_basis.append(vec)
        
        # Compute polynomial
        print("Computing 1_L(x) as polynomial...")
        errors, poly = test_exactness(n, L_basis)
        print(f"  Exact representation errors: {errors}")
        
        # Polynomial stats
        degrees = [len(m) for m in poly.keys()]
        max_deg = max(degrees)
        num_terms = len(poly)
        print(f"  Number of terms: {num_terms}")
        print(f"  Max degree: {max_deg}")
        print(f"  Degree distribution: {[degrees.count(d) for d in range(max_deg+1)]}")
        
        # Low-degree approximations
        for D in range(1, max_deg):
            print(f"\n  Best degree-<={D} approximation:")
            trunc_err, greedy_err, num_monos = low_degree_approximation_error(n, poly, D)
            print(f"    Truncation error: {trunc_err} / {2**dim} ({trunc_err / (2**dim):.4f})")
            print(f"    Greedy error: {greedy_err} / {2**dim} ({greedy_err / (2**dim):.4f})")
            print(f"    Available monomials: {num_monos}")
    
    print("\n" + "=" * 70)
    print("Interpretation:")
    print("  - 1_L(x) is exactly a degree-n polynomial")
    print("  - Low-degree approximations have NONZERO error")
    print("  - For LPN reduction: exact rep needs M = C(2n,<=n) ~ 2^{2n} monomials")
    print("  - Approximate rep introduces error → noise inflation")
    print("=" * 70)

if __name__ == "__main__":
    main()
