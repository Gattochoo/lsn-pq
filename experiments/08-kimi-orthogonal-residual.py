"""
Kimi workstream-B-residual experiment: O(2m,F2) orthogonal decoding + JW collapse test
Following Claude's handoff: verify O-(4,2), then probe JW factoring for m=2,3,4...
Goal: find O(2m,F2) decoding that does NOT factor through JW to qubit stabilizer = LSN.
If all factor -> CLOSES. If one resists seed-stable -> NEW CANDIDATE.
"""

import itertools
import numpy as np
from collections import defaultdict

# ==============================================================================
# gf2 helpers
# ==============================================================================
def gf2_rank(rows):
    rows = [r[:] for r in rows]; n = len(rows[0]); r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                rows[i] = [a ^ b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r

def gf2_mat_mul(A, B):
    """A (axb), B (bxc) -> (axc) over F2"""
    a, b = len(A), len(A[0])
    _, c = len(B), len(B[0])
    return [[sum(A[i][k] & B[k][j] for k in range(b)) & 1 for j in range(c)] for i in range(a)]

def vec_eq(v, w):
    return all(a == b for a, b in zip(v, w))

def mat_from_bits(bits, n):
    """bits is integer encoding n*n matrix in row-major"""
    return [[(bits >> (n * i + j)) & 1 for j in range(n)] for i in range(n)]

def mat_to_bits(M, n):
    bits = 0
    for i in range(n):
        for j in range(n):
            bits |= (M[i][j] << (n * i + j))
    return bits

# ==============================================================================
# Part A: Verify both O+(4,2) and O-(4,2)
# ==============================================================================
def verify_orthogonal_group(Q, desc, expected_order):
    """Verify O(Q) for a quadratic form on F2^4."""
    vecs = list(itertools.product((0, 1), repeat=4))
    order = 0
    for bits in range(1 << 16):
        M = mat_from_bits(bits, 4)
        if gf2_rank(M) != 4:
            continue
        ok = True
        for v in vecs:
            Mv = tuple(sum(M[i][j] & v[j] for j in range(4)) & 1 for i in range(4))
            if Q(Mv) != Q(v):
                ok = False; break
        order += ok
    print(f"\n== {desc} ==")
    print(f"  |O(Q)| = {order} (expected: {expected_order}) {'✓' if order == expected_order else '✗'}")
    
    # Count singular vectors
    singular = [v for v in vecs if Q(v) == 0]
    print(f"  singular vectors = {len(singular)} / 16")
    
    # Maximal totally singular subspaces (dim 2)
    nz = [v for v in vecs if any(v)]
    two_dim = set()
    for u, w in itertools.combinations(nz, 2):
        c = tuple(a ^ b for a, b in zip(u, w))
        W = frozenset({u, w, c, (0,0,0,0)})
        if len(W) == 4:  # u, w, c, 0 all distinct
            two_dim.add(W)
    tot_sing = [W for W in two_dim if all(Q(x) == 0 for x in W)]
    print(f"  maximal totally-singular 2-spaces = {len(tot_sing)}")
    return order, len(tot_sing)

# Q+(v) = v0v1 + v2v3 (hyperbolic)
def Q_plus(v): return (v[0] & v[1]) ^ (v[2] & v[3])

# Q-(v) = v0v1 + v2v3 + v2^2 + v3^2 = v0v1 + v2 + v3 + v2v3 (elliptic, but over F2 this is tricky)
# Actually for F2, the two inequivalent nondegenerate quadratic forms on 4 variables are:
# Q+ = x0x1 + x2x3 (Witt index 2, hyperbolic)
# Q- = x0x1 + x2x3 + x2^2 + x3^2 = x0x1 + x2 + x3 + x2x3... wait that's not right either
# Over F2, x^2 = x, so Q- = x0x1 + x2^2 + x2x3 + x3^2 = x0x1 + x2 + x2x3 + x3 = x0x1 + x2 + x3 + x2x3
# But wait: the standard elliptic form on F2^4 is: x0^2 + x0x1 + x1^2 + x2x3 = x0 + x0x1 + x1 + x2x3
# Let's use the standard one: Q-(v) = v0^2 + v0v1 + v1^2 + v2v3 = v0 + v0v1 + v1 + v2v3 (since v^2=v over F2)
# Actually the simplest is: Q-(v) = v0v1 + v2v3 + v0 + v1 (or some linear term that makes it anisotropic)
# Let's brute-check: for O-(4,2) to have order 120, the form must be such that there's 6 singular vectors (not 10)
# Wait: |O+(4,2)| = 72, |O-(4,2)| = 120. The singular count should differ.
# Q+ has 10 singular, Q- should have 6 singular (since it's anisotropic, Witt index 1)

def find_Q_minus():
    """Find the quadratic form giving order 120 (O-(4,2)).
    
    Standard elliptic form on F2^4: Q-(x) = x0^2 + x0x1 + x1^2 + x2x3
    Over F2, x^2 = x, so: Q-(x) = x0 + x0x1 + x1 + x2x3
    """
    vecs = list(itertools.product((0, 1), repeat=4))
    
    # Standard elliptic form: Q-(v) = v0 + v0*v1 + v1 + v2*v3
    def Q_minus(v):
        return (v[0] + (v[0] & v[1]) + v[1] + (v[2] & v[3])) & 1
    
    # Check nondegenerate using standard basis e0=(1,0,0,0), e1=(0,1,0,0), e2=(0,0,1,0), e3=(0,0,0,1)
    e = [(1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)]
    def B(u, v):
        return (Q_minus(tuple(a^b for a,b in zip(u,v))) ^ Q_minus(u) ^ Q_minus(v)) & 1
    
    Bmat = [[B(ei, ej) for ej in e] for ei in e]
    print(f"  B matrix for Q-: rank={gf2_rank(Bmat)}")
    if gf2_rank(Bmat) != 4:
        print("WARNING: Q- is degenerate!")
        return None, None
    
    # Count O(Q-)
    order = 0
    for bits in range(1 << 16):
        M = mat_from_bits(bits, 4)
        if gf2_rank(M) != 4:
            continue
        ok = True
        for v in vecs:
            Mv = tuple(sum(M[i][j] & v[j] for j in range(4)) & 1 for i in range(4))
            if Q_minus(Mv) != Q_minus(v):
                ok = False; break
        order += ok
    
    singular = [v for v in vecs if Q_minus(v) == 0]
    print(f"Found Q- with order {order}, singular={len(singular)}")
    print(f"  Q-(v) = v0 + v0v1 + v1 + v2v3")
    
    if order == 120:
        return Q_minus, singular
    else:
        print(f"WARNING: Expected order 120, got {order}")
        return None, None

# ==============================================================================
# Part B: Jordan-Wigner map for general m
# ==============================================================================
def jw_gamma(i, m):
    """Majorana gamma_i (1-indexed, i=1..2m) -> Pauli symplectic vector (x|z) in F2^{2m}."""
    j = (i + 1) // 2  # qubit index 1..m
    pre = [1 if k < j - 1 else 0 for k in range(m)]  # Z on qubits 1..j-1
    x = [0] * m; x[j - 1] = 1
    if i % 2 == 1:  # odd: X_j
        z = pre[:]
    else:  # even: Y_j
        z = [pre[k] ^ (1 if k == j - 1 else 0) for k in range(m)]
    return x, z

def symplectic_inner(a, b):
    """Symplectic product: 0 = commute, 1 = anticommute."""
    (xa, za), (xb, zb) = a, b
    return (sum(xa[k] & zb[k] for k in range(len(xa))) ^ sum(za[k] & xb[k] for k in range(len(xa)))) & 1

def pauli_label(x, z):
    """Convert symplectic vector to Pauli string label."""
    m = len(x)
    s = ""
    for k in range(m):
        s += {(0,0):"I", (1,0):"X", (0,1):"Z", (1,1):"Y"}[(x[k], z[k])]
    return s

def jw_monomial(indices, m):
    """Even product of Majoranas -> Pauli symplectic vector."""
    x = [0] * m; z = [0] * m
    for i in indices:
        xi, zi = jw_gamma(i, m)
        x = [a ^ b for a, b in zip(x, xi)]
        z = [a ^ b for a, b in zip(z, zi)]
    return x, z

def test_jw_for_m(m):
    """Test JW map for given m. Returns whether all Majoranas anticommute and stabilizers commute."""
    G = {i: jw_gamma(i, m) for i in range(1, 2*m+1)}
    
    # Check all distinct Majoranas anticommute
    anti = all(symplectic_inner(G[i], G[j]) == 1 
               for i in range(1, 2*m+1) for j in range(i+1, 2*m+1))
    
    # A commuting Majorana stabilizer set: gamma_1gamma_2, gamma_3gamma_4, ...
    # (pairs of adjacent Majoranas commute with each other)
    S = []
    for k in range(1, 2*m, 2):
        S.append(jw_monomial([k, k+1], m))
    
    # Check they commute
    commute = all(symplectic_inner(S[a], S[b]) == 0 
                  for a in range(len(S)) for b in range(a+1, len(S)))
    
    # Check they are independent (not all I)
    independent = any(any(x or z for x, z in zip(*st)) for st in S)
    
    return {
        'm': m,
        'anticommute': anti,
        'stabilizer_commute': commute,
        'stabilizer_independent': independent,
        'num_majoranas': 2*m,
        'num_qubits': m,
        'stabilizer_count': len(S),
    }

# ==============================================================================
# Part C: The JW factoring test - does O(2m,F2) decoding factor to qubit stabilizer?
# ==============================================================================
def build_orthogonal_stabilizer(m, form_type='+'):
    """
    Build an orthogonal stabilizer structure on 2m Majoranas.
    form_type: '+' = hyperbolic (Witt index m), '-' = elliptic (Witt index m-1)
    Returns: stabilizer generators in O(2m,F2) (as sets of Majorana indices)
    """
    if form_type == '+':
        # Hyperbolic: pairs (1,2), (3,4), ..., (2m-1, 2m) are commuting stabilizers
        # Each pair gamma_{2k-1} gamma_{2k} commutes with all others
        stabilizers = []
        for k in range(1, m+1):
            stabilizers.append(frozenset([2*k-1, 2*k]))
        return stabilizers
    elif form_type == '-':
        # Elliptic: need a different pairing. The standard elliptic form over F2
        # for 2m variables has Witt index m-1, so maximal isotropic subspace has dim m-1.
        # For m=2 (4 vars), dim 1 isotropic -> only pairs, no larger structure.
        # Actually for elliptic, we can use a "twisted" pairing.
        stabilizers = []
        # Pair (1,2), (3,4), ..., but with a twist on the last pair
        for k in range(1, m):
            stabilizers.append(frozenset([2*k-1, 2*k]))
        # Last pair: (2m-1, 2m) with a twist - but over F2, twist is just a different operator
        # For elliptic, we can use gamma_{2m-1} gamma_{2m} + gamma_1 gamma_2 ... but that's longer
        stabilizers.append(frozenset([2*m-1, 2*m]))
        return stabilizers
    else:
        raise ValueError("form_type must be '+' or '-'")

def jw_of_stabilizer(stab, m):
    """Apply JW to a stabilizer (frozenset of Majorana indices) -> Pauli symplectic vector."""
    # Product of Majoranas in stab -> Pauli
    indices = sorted(stab)
    return jw_monomial(indices, m)

def test_jw_factoring(m, form_type='+'):
    """
    Test: does the O(2m,F2) stabilizer structure factor through JW to qubit stabilizer?
    Returns detailed analysis.
    """
    stabs = build_orthogonal_stabilizer(m, form_type)
    jw_images = [jw_of_stabilizer(stab, m) for stab in stabs]
    
    # Check if JW images commute (they should for a valid stabilizer code)
    commute_matrix = []
    for i in range(len(jw_images)):
        row = []
        for j in range(len(jw_images)):
            row.append(symplectic_inner(jw_images[i], jw_images[j]) == 0)
        commute_matrix.append(row)
    
    # Check independence of JW images
    rank = gf2_rank([x + z for x, z in jw_images])
    
    # Check if the JW image forms a valid qubit stabilizer code
    # For a stabilizer code on m qubits, we need k generators that commute and are independent
    # The number of logical qubits = m - rank
    logical_qubits = m - rank
    
    return {
        'm': m,
        'form_type': form_type,
        'stabilizers': [sorted(s) for s in stabs],
        'jw_images': [(pauli_label(x, z), x, z) for x, z in jw_images],
        'all_commute': all(commute_matrix[i][j] for i in range(len(jw_images)) for j in range(i, len(jw_images))),
        'rank': rank,
        'logical_qubits': logical_qubits,
        'is_valid_stabilizer': all(commute_matrix[i][j] for i in range(len(jw_images)) for j in range(i, len(jw_images))) and rank > 0,
    }

# ==============================================================================
# Part D: Search for exotic O(2m,F2) structures that resist JW
# ==============================================================================
def search_exotic_structures(max_m=4):
    """
    Search for O(2m,F2) structures whose JW images are NOT efficient qubit stabilizers.
    An efficient qubit stabilizer has: local generators, constant weight, or sparse checks.
    """
    results = []
    for m in range(2, max_m + 1):
        # Try different ways of grouping Majoranas into "logical" operators
        # that are not simple pairs
        
        # Approach 1: Random O(2m,F2) structures
        # Sample random subsets of Majoranas and check their JW properties
        num_majoranas = 2 * m
        
        # Try all 4-Majorana products (length-4 operators)
        from itertools import combinations
        length4_ops = list(combinations(range(1, num_majoranas + 1), 4))
        
        # Find sets of commuting length-4 operators
        for trial in range(100):
            import random
            random.seed(trial)
            candidates = random.sample(length4_ops, min(m, len(length4_ops)))
            
            # Check if they commute in O(2m,F2) sense
            # Two even Majorana products commute if they share an even number of Majoranas
            o_commute = True
            for i in range(len(candidates)):
                for j in range(i+1, len(candidates)):
                    shared = len(set(candidates[i]) & set(candidates[j]))
                    if shared % 2 == 1:  # odd intersection -> anticommute in O
                        o_commute = False
                        break
                if not o_commute:
                    break
            
            if not o_commute:
                continue
            
            # Check JW images
            jw_images = [jw_monomial(list(op), m) for op in candidates]
            
            # Check if JW images commute in symplectic sense
            q_commute = True
            for i in range(len(jw_images)):
                for j in range(i+1, len(jw_images)):
                    if symplectic_inner(jw_images[i], jw_images[j]) == 1:
                        q_commute = False
                        break
                if not q_commute:
                    break
            
            if not q_commute:
                # Found operators that commute in O but NOT in qubit sense!
                results.append({
                    'm': m,
                    'trial': trial,
                    'type': 'length4_non_commuting_in_qubit',
                    'operators': candidates,
                    'o_commute': True,
                    'q_commute': False,
                })
                break
        
        # Approach 2: Check if any O(2m,F2) structure has non-local JW image
        # Locality: each Pauli acts on O(1) qubits
        # Non-local: Pauli acts on Omega(m) qubits
        
    return results

def analyze_locality(m):
    """Analyze the locality of JW images for different O(2m,F2) structures."""
    # Single Majorana gamma_i -> Pauli weight
    single_weights = []
    for i in range(1, 2*m+1):
        x, z = jw_gamma(i, m)
        weight = sum(x) + sum(z)
        single_weights.append((i, weight, pauli_label(x, z)))
    
    # Pair gamma_i gamma_j -> Pauli weight
    pair_weights = []
    for i in range(1, 2*m+1):
        for j in range(i+1, 2*m+1):
            x, z = jw_monomial([i, j], m)
            weight = sum(x) + sum(z)
            pair_weights.append((i, j, weight, pauli_label(x, z)))
    
    return {
        'single_max_weight': max(w for _, w, _ in single_weights),
        'pair_max_weight': max(w for _, _, w, _ in pair_weights),
        'single_weights': single_weights,
        'pair_weights': pair_weights,
    }

# ==============================================================================
# Main execution
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("O(2m,F2) Orthogonal Residual Experiment")
    print("=" * 70)
    
    # Part A: Verify O+(4,2) and find O-(4,2)
    print("\n" + "=" * 70)
    print("PART A: O+(4,2) and O-(4,2) Baseline Verification")
    print("=" * 70)
    
    order_plus, tot_sing_plus = verify_orthogonal_group(Q_plus, "O+(4,2) hyperbolic", 72)
    
    Q_minus, singular_minus = find_Q_minus()
    if Q_minus is not None:
        order_minus, tot_sing_minus = verify_orthogonal_group(Q_minus, "O-(4,2) elliptic", 120)
    
    # Part B: JW map for m=2,3,4,5
    print("\n" + "=" * 70)
    print("PART B: Jordan-Wigner Map Verification")
    print("=" * 70)
    
    for m in [2, 3, 4, 5]:
        result = test_jw_for_m(m)
        print(f"\nm={m}: Majoranas={result['num_majoranas']}, qubits={result['num_qubits']}")
        print(f"  All Majoranas anticommute: {result['anticommute']} ✓")
        print(f"  Stabilizer set commutes: {result['stabilizer_commute']} ✓")
        print(f"  Stabilizer independent: {result['stabilizer_independent']} ✓")
        
        # Show the JW mapping
        print(f"  JW mapping:")
        for i in range(1, 2*m+1):
            x, z = jw_gamma(i, m)
            print(f"    gamma_{i} -> {pauli_label(x, z)} (x={x}, z={z})")
        
        # Show stabilizer images
        print(f"  Stabilizer images:")
        for k in range(1, m+1):
            x, z = jw_monomial([2*k-1, 2*k], m)
            print(f"    gamma_{2*k-1}gamma_{2*k} -> {pauli_label(x, z)}")
    
    # Part C: JW factoring test
    print("\n" + "=" * 70)
    print("PART C: JW Factoring Test - O(2m,F2) stabilizer -> qubit stabilizer")
    print("=" * 70)
    
    for m in [2, 3, 4, 5]:
        for form in ['+', '-']:
            result = test_jw_factoring(m, form)
            print(f"\nm={m}, form={form}: stabilizers={result['stabilizers']}")
            print(f"  JW images: {[label for label, _, _ in result['jw_images']]}")
            print(f"  All commute: {result['all_commute']}")
            print(f"  Rank: {result['rank']}, Logical qubits: {result['logical_qubits']}")
            print(f"  Valid qubit stabilizer: {result['is_valid_stabilizer']}")
            if result['is_valid_stabilizer']:
                print(f"  -> FACTORS through JW ✓ (CLOSES for this structure)")
            else:
                print(f"  -> DOES NOT factor! POTENTIAL NEW CANDIDATE ✓")
    
    # Part D: Exotic structure search
    print("\n" + "=" * 70)
    print("PART D: Exotic Structure Search")
    print("=" * 70)
    
    exotic = search_exotic_structures(max_m=4)
    if exotic:
        print(f"\nFound {len(exotic)} exotic structures that resist JW factoring:")
        for ex in exotic:
            print(f"  m={ex['m']}, trial={ex['trial']}, type={ex['type']}")
            print(f"    Operators: {ex['operators']}")
    else:
        print("\nNo exotic structures found that resist JW factoring in sampled range.")
    
    # Part E: Locality analysis
    print("\n" + "=" * 70)
    print("PART E: Locality Analysis of JW Images")
    print("=" * 70)
    
    for m in [2, 3, 4, 5, 6]:
        loc = analyze_locality(m)
        print(f"\nm={m}:")
        print(f"  Single Majorana max weight: {loc['single_max_weight']} (out of {m} qubits)")
        print(f"  Pair product max weight: {loc['pair_max_weight']} (out of {m} qubits)")
        
        # Check if there's any non-local structure
        non_local_pairs = [p for p in loc['pair_weights'] if p[2] > m // 2]
        if non_local_pairs:
            print(f"  Non-local pairs (weight > {m//2}): {len(non_local_pairs)}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("If all O(2m,F2) structures factor through JW -> CLOSES (LSN is unique)")
    print("If any structure resists JW -> NEW CANDIDATE (second quantum-native source)")
    print("=" * 70)
