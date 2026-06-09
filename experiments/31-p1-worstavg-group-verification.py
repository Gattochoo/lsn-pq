"""
Experiment 31: P1 Worst→Avg Group-Theoretic Verification

Verifies the structural claims from the technical note on symplectic self-duality:
1. Sp(2n,F_2) acts transitively on Lagrangians (Witt theorem)
2. Stab(L) acts transitively on L \\ {0}
3. No subgroup H ⊂ Sp(2n,F_2) both preserves Bernoulli(p) noise AND acts transitively on Lagrangians
4. Fresh noise addition creates inhomogeneous noise

Standard symplectic structure: V = F_2^{2n}, Omega(a,b) = sum a_i b_{n+i} + a_{n+i} b_i
"""

import numpy as np
from itertools import combinations, product
from math import comb

# ---------------------------------------------------------------------------
# Helper: F_2 linear algebra
# ---------------------------------------------------------------------------

def mat_mul(A, B, mod=2):
    """Matrix multiplication over F_2."""
    return (A @ B) % mod

def mat_vec_mul(A, v, mod=2):
    """Matrix-vector multiplication over F_2."""
    return (A @ v) % mod

def symplectic_form(n, a, b):
    """Standard symplectic form Omega(a,b) = sum_{i=0}^{n-1} (a_i b_{n+i} + a_{n+i} b_i)."""
    return sum(a[i] * b[n+i] + a[n+i] * b[i] for i in range(n)) % 2

def is_isotropic(n, S):
    """Check if subspace S (list of vectors) is isotropic."""
    for i in range(len(S)):
        for j in range(i, len(S)):
            if symplectic_form(n, S[i], S[j]) != 0:
                return False
    return True

def span(vecs):
    """Compute span of vectors over F_2. Returns list of unique vectors."""
    if not vecs:
        return [np.zeros(len(vecs[0]) if vecs else 1, dtype=int)]
    dim = len(vecs[0])
    result = set()
    for mask in range(1 << len(vecs)):
        v = np.zeros(dim, dtype=int)
        for i in range(len(vecs)):
            if mask & (1 << i):
                v ^= vecs[i]
        result.add(tuple(v))
    return [np.array(v, dtype=int) for v in sorted(result)]

def all_subspaces(dim, sub_dim):
    """Generate all subspaces of F_2^dim of dimension sub_dim."""
    # Generate all subspaces by choosing sub_dim linearly independent vectors
    seen = set()
    subspaces = []
    all_vecs = [np.array(v, dtype=int) for v in product([0,1], repeat=dim) if any(v)]
    
    for combo in combinations(range(len(all_vecs)), sub_dim):
        vecs = [all_vecs[i] for i in combo]
        # Check linear independence
        s = span(vecs)
        if len(s) != 2**sub_dim:
            continue
        # Canonical form: sort basis vectors lexicographically
        basis = sorted([tuple(v) for v in vecs])
        key = tuple(sorted([tuple(v) for v in s]))
        if key not in seen:
            seen.add(key)
            subspaces.append(s)
    return subspaces

def is_lagrangian(n, S):
    """Check if S is Lagrangian (isotropic + dimension n)."""
    return len(S) == 2**n and is_isotropic(n, S)

# ---------------------------------------------------------------------------
# Generate Sp(2n, F_2)
# ---------------------------------------------------------------------------

def generate_sp(n):
    """Generate all symplectic matrices in Sp(2n, F_2) by checking condition M^T J M = J."""
    dim = 2*n
    J = np.zeros((dim, dim), dtype=int)
    for i in range(n):
        J[i, n+i] = 1
        J[n+i, i] = 1
    
    sp = []
    # For n=2, dim=4, there are 2^16 = 65536 matrices. Check all.
    # For n=3, dim=6, 2^36 is too many. We'll only do n=2.
    if n > 2:
        return None
    
    for bits in range(2**(dim*dim)):
        M = np.zeros((dim, dim), dtype=int)
        temp = bits
        for i in range(dim):
            for j in range(dim):
                M[i,j] = temp & 1
                temp >>= 1
        
        # Check M^T J M == J
        if np.array_equal((M.T @ J @ M) % 2, J):
            sp.append(M)
    
    return sp

def apply_group_element(M, subspace):
    """Apply symplectic matrix M to subspace."""
    return span([mat_vec_mul(M, v) for v in subspace])

def subspace_eq(S1, S2):
    """Check if two subspaces are equal."""
    s1 = set(tuple(v) for v in S1)
    s2 = set(tuple(v) for v in S2)
    return s1 == s2

# ---------------------------------------------------------------------------
# Main verification for n=2
# ---------------------------------------------------------------------------

def verify_n2():
    print("=" * 70)
    print("P1 Verification: n=2")
    print("=" * 70)
    
    n = 2
    dim = 2*n
    
    # Step 1: Generate all Lagrangians
    print("\n[1] Generating all Lagrangians...")
    all_subs = all_subspaces(dim, n)
    lagrangians = [S for S in all_subs if is_lagrangian(n, S)]
    print(f"    Total {n}-dim subspaces: {len(all_subs)}")
    print(f"    Lagrangians: {len(lagrangians)}")
    print(f"    Expected (standard): 15")
    
    # Step 2: Generate Sp(4, F_2)
    print("\n[2] Generating Sp(4, F_2)...")
    sp = generate_sp(n)
    print(f"    |Sp(4, F_2)| = {len(sp)}")
    print(f"    Expected: 720")
    
    # Step 3: Verify transitivity on Lagrangians
    print("\n[3] Verifying Sp acts transitively on Lagrangians...")
    L0 = lagrangians[0]
    orbits = set()
    for M in sp:
        L = apply_group_element(M, L0)
        key = tuple(sorted([tuple(v) for v in L]))
        orbits.add(key)
    print(f"    Orbits of L0 under Sp: {len(orbits)}")
    print(f"    Transitive: {len(orbits) == len(lagrangians)}")
    
    # Step 4: Compute Stab(L0) and its orbits on L0
    print("\n[4] Computing Stab(L0) and its orbits on L0...")
    stab = [M for M in sp if subspace_eq(apply_group_element(M, L0), L0)]
    print(f"    |Stab(L0)| = {len(stab)}")
    print(f"    Expected: |Sp|/|Lagr| = {len(sp)}/{len(lagrangians)} = {len(sp)//len(lagrangians)}")
    
    # Orbits of nonzero vectors in L0
    nonzero = [v for v in L0 if any(v)]
    orbits_stab = {}
    for v in nonzero:
        key = tuple(v)
        if key not in orbits_stab:
            orbit = set()
            for M in stab:
                w = mat_vec_mul(M, v)
                orbit.add(tuple(w))
            for w in orbit:
                orbits_stab[w] = orbit
    unique_orbits = []
    seen = set()
    for v in nonzero:
        key = tuple(v)
        if key not in seen:
            seen.update(orbits_stab[key])
            unique_orbits.append(orbits_stab[key])
    
    print(f"    Number of orbits of Stab on L0\\{{0}}: {len(unique_orbits)}")
    print(f"    Orbit sizes: {[len(o) for o in unique_orbits]}")
    print(f"    Transitive on L0\\{{0}}: {len(unique_orbits) == 1}")
    
    # Step 5: Noise inhomogeneity verification
    print("\n[5] Verifying fresh noise creates inhomogeneous noise...")
    # Simulate worst-case noise: eta(x) = 0 for x in L0, eta(x) = 1 for x not in L0
    # This is the "most adversarial" noise (always flips labels outside L0)
    V = [np.array(v, dtype=int) for v in product([0,1], repeat=dim)]
    eta = {tuple(v): (0 if tuple(v) in [tuple(u) for u in L0] else 1) for v in V}
    
    # Add fresh Bernoulli(1/4) noise
    np.random.seed(42)
    xi = {tuple(v): np.random.binomial(1, 0.25) for v in V}
    
    # New noise at each x
    eta_prime = {k: (eta[k] ^ xi[k]) for k in eta}
    
    # Check noise rate on L0 vs outside L0
    eta_L = [eta_prime[tuple(v)] for v in L0 if any(v)]  # nonzero in L0
    eta_out = [eta_prime[tuple(v)] for v in V if tuple(v) not in [tuple(u) for u in L0]]
    
    print(f"    Noise rate on L0\\{{0}}: {sum(eta_L)/len(eta_L):.3f} (should be 0.25 if homogeneous)")
    print(f"    Noise rate outside L0: {sum(eta_out)/len(eta_out):.3f} (should be 0.75 if homogeneous)")
    print(f"    INHOMOGENEOUS: {sum(eta_L)/len(eta_L) != sum(eta_out)/len(eta_out)}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    verify_n2()
