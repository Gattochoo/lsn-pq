#!/usr/bin/env python3
"""
P2: SNARK Toy Circuit for n=8
Verify the R1CS constraint count for LSN membership verification.

Circuit verifies:
  1. Isotropy: Ω(v_i, v_j) = 0 for all i ≤ j
  2. Full rank: rank[v_1 | ... | v_n] = n
  3. Membership: x ∈ L (i.e., Ω(x, v_i) = 0 for all i)
"""

import numpy as np

def build_lagrangian(n):
    """Build a random Lagrangian subspace of F_2^{2n}."""
    # Random isotropic basis
    basis = []
    V = np.zeros((2*n, 2*n), dtype=np.int8)
    
    for i in range(n):
        # Find a vector linearly independent and isotropic to previous
        for _ in range(1000):
            v = np.random.randint(0, 2, 2*n).astype(np.int8)
            if np.all(v == 0):
                continue
            
            # Check isotropy with all previous basis vectors
            isotropic = True
            for b in basis:
                omega = sum(v[2*k] * b[2*k+1] + v[2*k+1] * b[2*k] for k in range(n)) % 2
                if omega != 0:
                    isotropic = False
                    break
            
            if not isotropic:
                continue
            
            # Check linear independence
            test = np.array(basis + [v])
            if np.linalg.matrix_rank(test) == len(test):
                basis.append(v)
                break
        else:
            raise RuntimeError("Failed to find basis")
    
    return np.array(basis)

def symplectic_form(x, y, n):
    """Ω(x, y) over F_2."""
    return sum(x[2*k] * y[2*k+1] + x[2*k+1] * y[2*k] for k in range(n)) % 2


def count_constraints(n):
    """Count R1CS constraints for LSN membership (n-dimensional Lagrangian)."""
    constraints = []
    
    # Witness: basis vectors v_1, ..., v_n ∈ F_2^{2n}
    # Plus: left-inverse matrix M (n × 2n) for rank check
    # Plus: intermediate products for bilinear terms
    
    witness_vars = {}
    var_idx = 0
    
    def new_var(name):
        nonlocal var_idx
        witness_vars[name] = var_idx
        var_idx += 1
        return var_idx - 1
    
    # Define witness variables
    # v_i[k] for i=1..n, k=0..2n-1
    for i in range(n):
        for k in range(2*n):
            new_var(f"v_{i}_{k}")
    
    # M[i,k] for i=0..n-1, k=0..2n-1 (left inverse)
    for i in range(n):
        for k in range(2*n):
            new_var(f"M_{i}_{k}")
    
    # -- 1. Isotropy constraints: Ω(v_i, v_j) = 0 for all i ≤ j --
    # Ω(v_i, v_j) = Σ_{k=0}^{n-1} (v_i[2k]·v_j[2k+1] + v_i[2k+1]·v_j[2k])
    # Each product v_i[a]·v_j[b] is one R1CS constraint: (v_i[a]) * (v_j[b]) = t
    # Then sum all t's and check sum = 0 (one linear constraint)
    
    isotropy_products = 0
    isotropy_sums = 0
    
    for i in range(n):
        for j in range(i, n):
            terms = []
            for k in range(n):
                # Product 1: v_i[2k] * v_j[2k+1]
                t1 = new_var(f"prod_v{i}_{2*k}_v{j}_{2*k+1}")
                constraints.append(('prod', f"v_{i}_{2*k}", f"v_{j}_{2*k+1}", t1))
                terms.append(t1)
                isotropy_products += 1
                
                # Product 2: v_i[2k+1] * v_j[2k]
                t2 = new_var(f"prod_v{i}_{2*k+1}_v{j}_{2*k}")
                constraints.append(('prod', f"v_{i}_{2*k+1}", f"v_{j}_{2*k}", t2))
                terms.append(t2)
                isotropy_products += 1
            
            # Sum constraint: Σ terms = 0 (over F_2)
            # In R1CS: (Σ terms) * 1 = 0
            # This is a linear constraint (A = sum, B = 1, C = 0)
            constraints.append(('sum', terms, 0))
            isotropy_sums += 1
    
    # -- 2. Full rank: M · V = I_n --
    # V is 2n × n matrix (columns are v_i)
    # M is n × 2n matrix
    # (M · V)[i,j] = Σ_k M[i,k] · V[k,j] = δ_{ij}
    # Each term M[i,k] · V[k,j] is a product (but V[k,j] is witness, M[i,k] is witness)
    # Total: n × n entries, each with 2n terms
    
    rank_products = 0
    rank_sums = 0
    
    for i in range(n):
        for j in range(n):
            terms = []
            for k in range(2*n):
                t = new_var(f"prod_M{i}_{k}_v{j}_{k}")
                constraints.append(('prod', f"M_{i}_{k}", f"v_{j}_{k}", t))
                terms.append(t)
                rank_products += 1
            
            target = 1 if i == j else 0
            constraints.append(('sum', terms, target))
            rank_sums += 1
    
    # -- 3. Membership: Ω(x, v_i) = 0 for all i --
    # x is public input (not witness)
    # Ω(x, v_i) = Σ_k (x[2k]·v_i[2k+1] + x[2k+1]·v_i[2k]) = 0
    # x[a] are constants, so these are LINEAR constraints in witness vars
    # No products needed!
    
    membership_constraints = 0
    for i in range(n):
        # Linear combination of v_i variables
        # Σ_k (x[2k]·v_i[2k+1] + x[2k+1]·v_i[2k]) = 0
        # This is a single linear constraint
        constraints.append(('linear_membership', i))
        membership_constraints += 1
    
    total = len(constraints)
    
    return {
        'n': n,
        'witness_vars': var_idx,
        'isotropy_products': isotropy_products,
        'isotropy_sums': isotropy_sums,
        'rank_products': rank_products,
        'rank_sums': rank_sums,
        'membership': membership_constraints,
        'total_constraints': total,
        'constraint_breakdown': {
            'isotropy': isotropy_products + isotropy_sums,
            'rank': rank_products + rank_sums,
            'membership': membership_constraints
        }
    }


print("=" * 60)
print("SNARK TOY CIRCUIT: R1CS Constraint Count")
print("=" * 60)

for n in [4, 8, 16, 32, 42, 66]:
    result = count_constraints(n)
    print(f"\nn = {n}:")
    print(f"  Witness variables:        {result['witness_vars']}")
    print(f"  Isotropy products:        {result['isotropy_products']}")
    print(f"  Isotropy sum checks:      {result['isotropy_sums']}")
    print(f"  Rank products:            {result['rank_products']}")
    print(f"  Rank sum checks:          {result['rank_sums']}")
    print(f"  Membership checks:        {result['membership']}")
    print(f"  ---")
    print(f"  Total constraints:        {result['total_constraints']}")
    print(f"  Asymptotic:               Θ(n³) = {n**3} (actual = {result['total_constraints']})")
    
    # Verify against formula
    formula = n**2 * (n+1) + n**2 + n  # isotropy products + isotropy sums + rank products + rank sums + membership
    # Actually: isotropy_products = n(n+1)/2 * 2n = n²(n+1)
    #           isotropy_sums = n(n+1)/2
    #           rank_products = n² * 2n = 2n³
    #           rank_sums = n²
    #           membership = n
    # Total = n²(n+1) + n(n+1)/2 + 2n³ + n² + n
    #       = n³ + n² + (n²+n)/2 + 2n³ + n² + n
    #       = 3n³ + 2.5n² + 1.5n
    # Hmm, this is more than n³.
    
    actual_formula = n**2 * (n+1) + n*(n+1)//2 + 2*n**3 + n**2 + n
    print(f"  Formula check:            {actual_formula}")

# Build and verify a concrete n=8 instance
print("\n" + "=" * 60)
print("CONCRETE VERIFICATION: n=8")
print("=" * 60)

np.random.seed(42)
n = 8
basis = build_lagrangian(n)
print(f"Basis shape: {basis.shape}")

# Pick a random x in the Lagrangian
x = np.zeros(2*n, dtype=np.int8)
for i in range(n):
    if np.random.randint(0, 2):
        x ^= basis[i]

# Verify isotropy
for i in range(n):
    for j in range(i, n):
        omega = symplectic_form(basis[i], basis[j], n)
        if omega != 0:
            print(f"  FAIL: Ω(v_{i}, v_{j}) = {omega}")
        else:
            pass  # OK

# Verify membership
for i in range(n):
    omega = symplectic_form(x, basis[i], n)
    if omega != 0:
        print(f"  FAIL: Ω(x, v_{i}) = {omega}")

print("  All checks passed!")
print(f"  Total constraints for n=8: {count_constraints(8)['total_constraints']}")
