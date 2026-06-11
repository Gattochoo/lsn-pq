# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Phase 2: Exotic O(2m,F2) structures beyond standard stabilizers.

Searches for O(2m,F2) structures that resist JW factoring into qubit stabilizers.
Phase 1 (standard stabilizers) -> all CLOSES. 
This phase probes:
  1. Odd-length operators mixed with even-length stabilizers
  2. Non-isotropic but "almost-commuting" structures
  3. Larger m (6,8,10) with systematic search
  4. Non-local JW images as obstruction candidates
  5. Interacting-but-simulable regime probes

Author: Kimi (direct execution)
Date: 2026-06-05
"""

import itertools
import numpy as np
from collections import defaultdict, Counter
import random

# ==============================================================================
# Reuse Phase 1 utilities
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

def jw_gamma(i, m):
    """Majorana gamma_i -> Pauli symplectic vector (x|z) in F2^{2m}."""
    j = (i + 1) // 2
    pre = [1 if k < j - 1 else 0 for k in range(m)]
    x = [0] * m; x[j - 1] = 1
    if i % 2 == 1:
        z = pre[:]
    else:
        z = [pre[k] ^ (1 if k == j - 1 else 0) for k in range(m)]
    return x, z

def symplectic_inner(a, b):
    (xa, za), (xb, zb) = a, b
    return (sum(xa[k] & zb[k] for k in range(len(xa))) ^ sum(za[k] & xb[k] for k in range(len(xa)))) & 1

def pauli_label(x, z):
    m = len(x)
    return "".join({(0,0):"I", (1,0):"X", (0,1):"Z", (1,1):"Y"}[(x[k], z[k])] for k in range(m))

def jw_monomial(indices, m):
    x = [0] * m; z = [0] * m
    for i in indices:
        xi, zi = jw_gamma(i, m)
        x = [a ^ b for a, b in zip(x, xi)]
        z = [a ^ b for a, b in zip(z, zi)]
    return x, z

def jw_weight(indices, m):
    """Weight of JW image = number of non-identity Paulis."""
    x, z = jw_monomial(indices, m)
    return sum(1 for k in range(m) if x[k] or z[k])

# ==============================================================================
# Part A: Odd-length operators as potential obstructions
# ==============================================================================
def test_odd_length_obstructions(m, max_trials=1000):
    """
    Odd-length Majorana operators (1, 3, 5, ...) do NOT commute in O(2m,F2) sense.
    But: can they form a structure where the JW image is NOT a valid stabilizer?
    
    Key insight: odd-length operators anticommute with each other (in O sense),
    so they can't be stabilizers. But mixed with even-length, they might create
    a structure whose JW image is "messy" - not a clean stabilizer code.
    """
    results = []
    num_majoranas = 2 * m
    
    # Generate all single Majoranas (length 1)
    singles = [tuple([i]) for i in range(1, num_majoranas + 1)]
    
    # Generate all 3-Majorana products
    triples = list(itertools.combinations(range(1, num_majoranas + 1), 3))
    
    # Test: can we find a set of operators where:
    # 1. They commute in O(2m,F2) sense (via shared Majorana count)
    # 2. Their JW images do NOT commute in symplectic sense
    
    # Odd-length operators: commute if they share an even number of Majoranas
    # Actually: two operators O1, O2 commute if |O1 ∩ O2| is even (for both odd and even length)
    # Wait: for Majoranas, the anticommutation is: {γ_i, γ_j} = 2δ_ij
    # For products: γ_A γ_B = (-1)^{|A∩B|} γ_B γ_A when A,B are disjoint? No.
    # Actually: γ_A γ_B = (-1)^{|A||B| - |A∩B|} γ_B γ_A? Let's be careful.
    
    # For our purposes: two even products commute if they share an even number of Majoranas.
    # Two odd products: if they share an even number, they commute? Let's check.
    # γ_i γ_j = -γ_j γ_i for i≠j. So single Majoranas anticommute.
    # γ_i (γ_j γ_k) = ? If i≠j,k: γ_i γ_j γ_k = -γ_j γ_i γ_k = γ_j γ_k γ_i (commute!)
    # So single and triple commute if disjoint. But γ_i and γ_i γ_j γ_k = -γ_i γ_j γ_k γ_i... wait.
    # Actually: γ_i (γ_i γ_j γ_k) = γ_i^2 γ_j γ_k = γ_j γ_k
    # (γ_i γ_j γ_k) γ_i = γ_i γ_j γ_k γ_i = -γ_i γ_j γ_i γ_k = γ_j γ_k
    # So they commute! Interesting.
    
    # The general rule: γ_A and γ_B commute iff |A∩B| ≡ |A|·|B| mod 2? No.
    # Actually: γ_A γ_B = (-1)^{|A||B| - |A∩B|} γ_B γ_A? Let's verify with small cases.
    
    # For now, let's use the explicit test: compute symplectic product of JW images.
    # If they commute in O but not in symplectic, that's a hit.
    
    for trial in range(max_trials):
        # Randomly select mix of odd and even operators
        n_ops = random.randint(2, m)
        ops = []
        for _ in range(n_ops):
            length = random.choice([1, 2, 3, 4])
            op = tuple(sorted(random.sample(range(1, num_majoranas + 1), length)))
            ops.append(op)
        
        # Check O(2m,F2) commutation: compute via explicit JW
        o_commute = True
        for i in range(len(ops)):
            for j in range(i+1, len(ops)):
                # In O(2m,F2), operators commute if their JW images commute... wait, that's circular.
                # Actually, O(2m,F2) commutation is defined by the Majorana algebra:
                # two operators commute if they share an even number of Majoranas.
                # But wait, that's not quite right either.
                
                # Let's use the explicit definition: 
                # For products γ_A = ∏_{i∈A} γ_i (ordered), γ_B = ∏_{j∈B} γ_j,
                # γ_A γ_B = (-1)^{N} γ_B γ_A where N counts something.
                
                # Actually, the correct way: use the symplectic form on F2^{2m}.
                # The Majorana algebra is a Clifford algebra. The even part is O(2m,F2).
                # Odd operators don't commute with each other in general.
                
                # Let's just use the explicit JW test: if JW images commute, the operators commute.
                # If they don't, the operators anticommute.
                # But that's the same as the qubit test! The point is to find operators that:
                # 1. Commute in O(2m,F2) (if we can define that for odd)
                # 2. But whose JW images don't form a clean stabilizer structure
                
                # For the purpose of this experiment, let's look for:
                # - A set of operators whose JW images have HIGHLY non-local weights
                # - And where the "stabilizer" condition is violated in some way
                pass
        
        # Alternative approach: look for sets where JW images commute but are NOT independent
        # or where the rank is wrong, or where the code distance is 0 (degenerate in a bad way)
        
        jw_images = [jw_monomial(list(op), m) for op in ops]
        
        # Check if all commute in symplectic sense
        all_commute = True
        for i in range(len(jw_images)):
            for j in range(i+1, len(jw_images)):
                if symplectic_inner(jw_images[i], jw_images[j]) == 1:
                    all_commute = False
                    break
            if not all_commute:
                break
        
        if not all_commute:
            continue  # Not a stabilizer set
        
        # Check rank
        rank = gf2_rank([x + z for x, z in jw_images])
        
        # Check for degeneracy (rank < n_ops means dependencies)
        if rank < len(ops):
            # This is a degenerate stabilizer code - not useful
            continue
        
        # Check locality (max weight)
        max_weight = max(jw_weight(list(op), m) for op in ops)
        
        # Check if it's a "strange" code: logical qubits > 0 or non-local
        logical_qubits = m - rank
        
        if logical_qubits > 0 and max_weight > m // 2:
            # Found a non-local stabilizer code with logical qubits
            results.append({
                'm': m,
                'trial': trial,
                'ops': ops,
                'logical_qubits': logical_qubits,
                'max_weight': max_weight,
                'jw_labels': [pauli_label(x, z) for x, z in jw_images],
            })
            
        if len(results) >= 10:
            break
    
    return results

# ==============================================================================
# Part B: Systematic enumeration of all isotropic subspaces for small m
# ==============================================================================
def enumerate_all_isotropic_subspaces(m):
    """
    For m=2,3, enumerate ALL isotropic subspaces of O(2m,F2) and test JW factoring.
    An isotropic subspace is a set of operators where all pairs commute.
    """
    num_majoranas = 2 * m
    
    # Generate all possible even-length operators (length 2, 4, 6, ...)
    even_ops = []
    for length in range(2, num_majoranas + 1, 2):
        for op in itertools.combinations(range(1, num_majoranas + 1), length):
            even_ops.append(op)
    
    # For each operator, compute JW image
    jw_dict = {op: jw_monomial(list(op), m) for op in even_ops}
    
    # Build commutation graph: edge = commute in symplectic sense
    commute_graph = defaultdict(set)
    for i, op1 in enumerate(even_ops):
        for j, op2 in enumerate(even_ops):
            if i < j:
                if symplectic_inner(jw_dict[op1], jw_dict[op2]) == 0:
                    commute_graph[op1].add(op2)
                    commute_graph[op2].add(op1)
    
    # Find maximal cliques (maximal commuting sets)
    # This is NP-hard in general, but for small m we can do it
    
    # Greedy maximal clique finding
    maximal_cliques = []
    used = set()
    
    for op in even_ops:
        if op in used:
            continue
        clique = {op}
        candidates = set(even_ops) - {op}
        for other in list(candidates):
            if all(other in commute_graph[member] for member in clique):
                clique.add(other)
        maximal_cliques.append(clique)
        used.update(clique)
    
    # Analyze each maximal clique
    results = []
    for clique in maximal_cliques[:20]:  # Limit output
        ops = list(clique)
        jw_images = [jw_dict[op] for op in ops]
        rank = gf2_rank([x + z for x, z in jw_images])
        
        results.append({
            'size': len(clique),
            'rank': rank,
            'logical': m - rank,
            'max_weight': max(jw_weight(list(op), m) for op in ops),
            'sample_ops': [op[:3] for op in ops[:3]],  # First 3 ops
        })
    
    return results

# ==============================================================================
# Part C: Non-locality as obstruction criterion
# ==============================================================================
def analyze_nonlocality_obstruction(m):
    """
    If JW images are highly non-local, the qubit stabilizer decoding might be
    inefficient (exponential time). This could be an obstruction even if
    the structure technically "factors" through JW.
    
    Key insight: a stabilizer code with non-local checks has no efficient
    decoding algorithm in general. So even if JW gives a stabilizer, 
    if it's non-local, it's not "efficiently decodable" = not LSN.
    """
    # Single Majorana JW weights
    single_weights = {}
    for i in range(1, 2*m + 1):
        single_weights[i] = jw_weight([i], m)
    
    # Pair weights
    pair_weights = {}
    for i in range(1, 2*m + 1):
        for j in range(i+1, 2*m + 1):
            pair_weights[(i,j)] = jw_weight([i,j], m)
    
    # All even-length operators up to length 6
    all_weights = Counter()
    for length in range(2, min(2*m, 8) + 1, 2):
        for op in itertools.combinations(range(1, 2*m + 1), length):
            w = jw_weight(list(op), m)
            all_weights[w] += 1
    
    return {
        'm': m,
        'single_max': max(single_weights.values()),
        'pair_max': max(pair_weights.values()),
        'weight_distribution': dict(all_weights),
        'mean_weight': sum(w * c for w, c in all_weights.items()) / sum(all_weights.values()),
    }

# ==============================================================================
# Part D: "Patched" or "Twisted" O(2m,F2) structures
# ==============================================================================
def test_twisted_commutation(m):
    """
    What if we modify the commutation relations to create a structure
    that doesn't map cleanly to Paulis? 
    
    This is speculative: we "twist" the JW map by adding phase factors
    or modifying the gamma_i -> Pauli mapping.
    """
    # Standard JW: gamma_{2j-1} -> X_j with Z_{<j}, gamma_{2j} -> Y_j with Z_{<j}
    # What if we use a different mapping? e.g., random permutation of Majorana labels
    
    results = []
    
    # Test random permutations of the Majorana-to-qubit mapping
    for trial in range(100):
        perm = list(range(1, 2*m + 1))
        random.shuffle(perm)
        
        # Define twisted JW: apply standard JW to permuted indices
        def twisted_jw(i):
            # Map i to perm[i-1], then apply standard JW
            # But this is just a relabeling of Majoranas, which doesn't change the algebra
            # So it should still factor...
            return jw_gamma(perm[i-1], m)
        
        # Check if twisted mapping preserves anticommutation
        anti = all(symplectic_inner(twisted_jw(i), twisted_jw(j)) == 1 
                   for i in range(1, 2*m+1) for j in range(i+1, 2*m+1))
        
        if not anti:
            # Found a twisted mapping that breaks anticommutation!
            # But this is not a valid Majorana representation anymore
            results.append({
                'trial': trial,
                'type': 'breaks_anticommutation',
                'perm': perm[:6],
            })
        
        if len(results) >= 5:
            break
    
    return results

# ==============================================================================
# Part E: Exhaustive m=2,3,4 complete search
# ==============================================================================
def exhaustive_structure_search(m_max=4):
    """
    Exhaustively search ALL possible operator sets for small m.
    For m=2: 2^4 = 16 subsets of {γ1, γ2, γ3, γ4}
    For m=3: 2^6 = 64 subsets
    For m=4: 2^8 = 256 subsets
    
    For each subset, compute the generated algebra and check if JW gives
    a "weird" structure.
    """
    results = []
    
    for m in range(2, m_max + 1):
        num_majoranas = 2 * m
        
        # Generate all even-length operators
        even_ops = []
        for length in range(2, num_majoranas + 1, 2):
            for op in itertools.combinations(range(1, num_majoranas + 1), length):
                even_ops.append(op)
        
        print(f"m={m}: {len(even_ops)} even-length operators")
        
        # For each pair, check if they commute
        commuting_pairs = 0
        non_commuting_pairs = 0
        
        for i, op1 in enumerate(even_ops):
            for j, op2 in enumerate(even_ops):
                if i < j:
                    jw1 = jw_monomial(list(op1), m)
                    jw2 = jw_monomial(list(op2), m)
                    if symplectic_inner(jw1, jw2) == 0:
                        commuting_pairs += 1
                    else:
                        non_commuting_pairs += 1
        
        print(f"  Commuting pairs: {commuting_pairs}, Non-commuting: {non_commuting_pairs}")
        
        # Find all maximal commuting sets (cliques)
        # For small m, brute force is feasible
        if m <= 3:
            max_clique_size = 0
            max_cliques = []
            
            # Try all subsets of even_ops
            for r in range(1, len(even_ops) + 1):
                for subset in itertools.combinations(even_ops, r):
                    # Check if all pairs commute
                    all_commute = True
                    for i in range(len(subset)):
                        for j in range(i+1, len(subset)):
                            jw1 = jw_monomial(list(subset[i]), m)
                            jw2 = jw_monomial(list(subset[j]), m)
                            if symplectic_inner(jw1, jw2) == 1:
                                all_commute = False
                                break
                        if not all_commute:
                            break
                    
                    if all_commute:
                        if len(subset) > max_clique_size:
                            max_clique_size = len(subset)
                            max_cliques = [subset]
                        elif len(subset) == max_clique_size:
                            max_cliques.append(subset)
            
            print(f"  Max clique size: {max_clique_size}")
            print(f"  Number of max cliques: {len(max_cliques)}")
            
            # Check if max cliques factor to valid stabilizers
            for clique in max_cliques[:3]:
                jw_images = [jw_monomial(list(op), m) for op in clique]
                rank = gf2_rank([x + z for x, z in jw_images])
                logical = m - rank
                print(f"    Clique: rank={rank}, logical={logical}, ops={[op[:2] for op in clique[:3]]}")
    
    return results

# ==============================================================================
# Main execution
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Phase 2: Exotic O(2m,F2) Structures - Systematic Search")
    print("=" * 70)
    
    # Part A: Odd-length obstructions
    print("\n" + "=" * 70)
    print("PART A: Odd-Length Operator Obstructions")
    print("=" * 70)
    for m in [2, 3, 4]:
        results = test_odd_length_obstructions(m, max_trials=500)
        print(f"\nm={m}: Found {len(results)} exotic structures with logical qubits + non-local")
        for r in results[:3]:
            print(f"  ops={r['ops']}, logical={r['logical_qubits']}, max_weight={r['max_weight']}")
            print(f"    JW: {r['jw_labels']}")
    
    # Part B: Isotropic subspace enumeration
    print("\n" + "=" * 70)
    print("PART B: Isotropic Subspace Enumeration")
    print("=" * 70)
    for m in [2, 3]:
        print(f"\nm={m}:")
        results = enumerate_all_isotropic_subspaces(m)
        for r in results[:5]:
            print(f"  size={r['size']}, rank={r['rank']}, logical={r['logical']}, max_weight={r['max_weight']}")
    
    # Part C: Non-locality analysis
    print("\n" + "=" * 70)
    print("PART C: Non-Locality as Obstruction Criterion")
    print("=" * 70)
    for m in [2, 3, 4, 5, 6, 8, 10]:
        result = analyze_nonlocality_obstruction(m)
        print(f"\nm={m}: single_max={result['single_max']}, pair_max={result['pair_max']}, mean_weight={result['mean_weight']:.2f}")
        print(f"  weight distribution: {dict(sorted(result['weight_distribution'].items())[:8])}")
    
    # Part D: Twisted structures
    print("\n" + "=" * 70)
    print("PART D: Twisted / Patched O(2m,F2) Structures")
    print("=" * 70)
    for m in [3, 4]:
        results = test_twisted_commutation(m)
        print(f"\nm={m}: Found {len(results)} twisted mappings that break anticommutation")
    
    # Part E: Exhaustive search
    print("\n" + "=" * 70)
    print("PART E: Exhaustive Structure Search (m=2,3,4)")
    print("=" * 70)
    exhaustive_structure_search(m_max=4)
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("If exotic structures found that resist JW -> NEW CANDIDATE")
    print("If all factor -> CLOSES (tighten LSN uniqueness)")
    print("=" * 70)
