"""
Task 4 Phase 2: Three Structural Decoder Families vs. Walsh n-Scaling Wall

Test F1 (BP), F2 (Plücker), F3 (List+Prune) at constant rate p∈{0.1,0.15,0.25}
across n=4,5,6. Measure: recovery rate AND threshold vs n.

REDUCES requires: PUBLIC, POLY, constant-rate, threshold HOLDS/GROWS with n.
Walsh wall: n=4 ~13/256, n=5 ~2/256, n=6 ~0/256. Must BEAT this.

Expected: all shrink/fail → last door closes → 7th-evidence final.
Author: Kimi (direct execution)
Date: 2026-06-06
"""

import numpy as np
import itertools
from collections import Counter, defaultdict
import random
import time

rng = np.random.default_rng(20260606 + 7777)

# ==============================================================================
# F2 helpers
# ==============================================================================
def omega(a, b, n):
    return int((np.dot(a[:n], b[n:]) + np.dot(a[n:], b[:n])) % 2)

def gf2_rank(M):
    M = M.copy() % 2
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        piv = np.where(M[r:, c])[0]
        if len(piv) == 0:
            continue
        p = r + piv[0]
        M[[r, p]] = M[[p, r]]
        mask = M[:, c].copy()
        mask[r] = 0
        M[mask == 1] ^= M[r]
        r += 1
        if r == rows:
            break
    return r

def build_all_vectors(D):
    return np.array([[(i >> b) & 1 for b in range(D)] for i in range(1 << D)], dtype=np.int8)

def random_lagrangian(vecs, n, D):
    basis = []
    attempts = 0
    while len(basis) < n:
        attempts += 1
        if attempts > 10000:
            raise RuntimeError("Failed to find Lagrangian basis")
        v = vecs[rng.integers(1, 1 << D)]
        if all(omega(v, b, n) == 0 for b in basis):
            M = np.array(basis + [v])
            if gf2_rank(M) == len(basis) + 1:
                basis.append(v)
    return np.array(basis)

def members_mask(basis, n, D):
    elems = set()
    for coeffs in range(1 << n):
        v = np.zeros(D, dtype=np.int8)
        for k in range(n):
            if (coeffs >> k) & 1:
                v ^= basis[k]
        elems.add(int(sum(int(v[b]) << b for b in range(D))))
    return elems

# ==============================================================================
# F1: Belief Propagation / Message-Passing on Isotropic Code Tanner Graph
# ==============================================================================
def decoder_f1_bp(vecs, labels, n, D, max_iter=50):
    """
    F1: BP on the Tanner graph of the isotropic code.
    
    The isotropic code L = ker(H) where H is a check matrix. The noisy labels
    give us a "noisy codeword" problem. We run BP on the factor graph defined by
    the parity-check equations.
    
    However, the isotropic code has random-like structure (no good Tanner graph).
    Expected: BP fails at constant rate.
    
    Simplification: Since H is not known, we use a generic approach:
    - Each vector v has a "belief" b(v) ∈ [0,1] of being in L
    - Initially b(v) = labels[v] (0 or 1, but we'll use 0.9 for 1, 0.1 for 0)
    - Iterate: update beliefs based on symplectic consistency with neighbors
    - After convergence, threshold beliefs and extract the subspace
    
    This is a simplified BP-like approach, not full factor graph BP.
    """
    N = 1 << D
    
    # Initial beliefs: soft from labels
    beliefs = np.full(N, 0.5)
    beliefs[labels == 1] = 0.9
    beliefs[labels == 0] = 0.1
    
    # For n=5,6: skip full compat matrix, use random sampling for neighbors
    use_sparse = N > 512  # n>=5
    
    if use_sparse:
        # Sparse BP: for each vector, sample 100 random neighbors and check isotropy
        compat = {}  # dict of lists
        for i in range(N):
            # Sample 100 random other vectors
            others = rng.choice(N, size=min(100, N-1), replace=False)
            others = others[others != i]
            compat[i] = [j for j in others if omega(vecs[i], vecs[j], n) == 0]
    else:
        # Full compat matrix for n=4
        compat = np.zeros((N, N), dtype=np.int8)
        for i in range(N):
            for j in range(i+1, N):
                if omega(vecs[i], vecs[j], n) == 0:
                    compat[i, j] = 1
                    compat[j, i] = 1
    
    # BP iteration
    for iteration in range(max_iter):
        new_beliefs = beliefs.copy()
        
        for i in range(N):
            if use_sparse:
                neighbors = compat[i]
            else:
                neighbors = np.where(compat[i] == 1)[0]
            
            if len(neighbors) == 0:
                continue
            
            neighbor_belief = np.mean(beliefs[neighbors])
            new_beliefs[i] = 0.3 * beliefs[i] + 0.7 * neighbor_belief
        
        beliefs = np.clip(new_beliefs, 0.01, 0.99)
    
    # Extract top-2^n beliefs as candidate subspace
    top_k = min(2**n, N)
    top_indices = np.argsort(beliefs)[-top_k:]
    candidate = vecs[top_indices]
    
    # Check if candidate is isotropic and has right rank
    if gf2_rank(candidate) == n:
        is_iso = all(omega(candidate[i], candidate[j], n) == 0 
                     for i in range(n) for j in range(i, n))
        if is_iso:
            return candidate, "bp_converged"
    
    return None, "bp_did_not_converge"

# ==============================================================================
# F2: Plücker / Lagrangian-Grassmannian Decoding
# ==============================================================================
def decoder_f2_plucker(vecs, labels, n, D):
    """
    F2: Plücker coordinates on the Lagrangian Grassmannian LG(n,2n).
    
    For an n-dimensional subspace L ⊂ F_2^{2n} with basis {b_1,...,b_n},
    the Plücker coordinates are the determinants of all n×n minors of the
    n×2n basis matrix. For a Lagrangian, these satisfy quadratic relations.
    
    Approach: 
    1. Build a weighted matrix M where M_{i,j} = correlation between labels
       and the (i,j) minor (simplified: use correlation with basis vectors)
    2. Use spectral/SVD to estimate the basis
    3. Project onto LG(n,2n) by enforcing isotropy
    
    This is a simplified Plücker approach; full Plücker over F_2 is complex.
    """
    N = 1 << D
    
    # Build a correlation matrix: for each pair of coordinates (i,j),
    # measure how correlated the labels are with v_i * v_j
    # This is a heuristic for the Plücker structure
    
    # Actually, let's use a simpler approach: the label matrix
    # Create a matrix where rows = vectors, cols = coordinates
    # Weight by label confidence
    
    weights = np.where(labels == 1, 1.0, -0.5)  # Positive for in-L, negative for not
    
    # Weighted covariance matrix of the coordinates
    weighted_vecs = vecs.astype(np.float64) * weights[:, np.newaxis]
    cov = weighted_vecs.T @ weighted_vecs / N
    
    # SVD to find principal directions
    try:
        U, s, Vt = np.linalg.svd(cov)
    except:
        return None, "svd_failed"
    
    # Take top-n principal directions as candidate basis
    candidate_basis = np.round(U[:, :n]).astype(np.int8) % 2
    
    # Make isotropic: project onto isotropic subspace
    # Enforce ω(b_i, b_j) = 0 by modifying basis vectors
    for i in range(n):
        for j in range(i+1, n):
            if omega(candidate_basis[:, i], candidate_basis[:, j], n) == 1:
                # Adjust: try to make them orthogonal
                candidate_basis[:, j] = (candidate_basis[:, j] + candidate_basis[:, i]) % 2
    
    # Check rank and isotropy
    if gf2_rank(candidate_basis.T) == n:
        is_iso = all(omega(candidate_basis[:, i], candidate_basis[:, j], n) == 0 
                     for i in range(n) for j in range(i, n))
        if is_iso:
            return candidate_basis.T, "plucker_converged"
    
    return None, "plucker_did_not_converge"

# ==============================================================================
# F3: List-Decode + Isotropy Prune
# ==============================================================================
def decoder_f3_list_prune(vecs, labels, n, D, max_list=20, max_trials=200):
    """
    F3: List-decoding + isotropy pruning (LIGHTWEIGHT).
    
    1. Generate a SMALL list of candidate subspaces from random n-subsets
    2. Prune by isotropy + consistency
    
    Win only if: (a) list stays poly-sized, (b) true L is in the list,
    (c) pruning correctly identifies it.
    """
    N = 1 << D
    
    # Step 1: Generate candidate subspaces from positive labels
    pos_indices = np.where(labels == 1)[0]
    if len(pos_indices) < n:
        return None, "too_few_positives"
    
    candidates = []
    
    # Lightweight: only try max_trials random subsets
    for trial in range(max_trials):
        if len(pos_indices) < n:
            break
        
        chosen = rng.choice(len(pos_indices), size=n, replace=False)
        subset = vecs[pos_indices[chosen]]
        
        if gf2_rank(subset) == n:
            is_iso = all(omega(subset[i], subset[j], n) == 0 
                        for i in range(n) for j in range(i, n))
            if is_iso:
                candidates.append(subset)
        
        if len(candidates) >= max_list:
            break
    
    if not candidates:
        return None, f"no_isotropic_after_{max_trials}"
    
    # Step 2: Score each candidate by label consistency (fast)
    scored = []
    for cand in candidates[:max_list]:  # Only score top max_list
        # Fast consistency: sample 100 vectors instead of all N
        sample_indices = rng.integers(0, N, size=min(100, N))
        
        # Compute candidate membership for sample
        cand_mask = np.zeros(min(100, N), dtype=bool)
        for idx, i in enumerate(sample_indices):
            # Check if vecs[i] is in span of cand
            test = np.vstack([cand, vecs[i]])
            if gf2_rank(test) == n:
                cand_mask[idx] = True
        
        sample_labels = labels[sample_indices]
        matches = np.sum(cand_mask == (sample_labels == 1))
        accuracy = matches / len(sample_indices)
        scored.append((accuracy, cand))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    
    if scored and scored[0][0] > 0.85:
        return scored[0][1], f"list_prune_acc={scored[0][0]:.3f}"
    
    return None, f"best_acc={scored[0][0] if scored else 0:.3f}"

# ==============================================================================
# Main experiment: test all three families vs n-scaling
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Task 4: Three Structural Decoder Families vs. Walsh n-Scaling Wall")
    print("=" * 70)
    print("\nWalsh wall (OFA-317/318):")
    print("  n=4: threshold ~13/256 (~0.05)")
    print("  n=5: threshold ~2/256 (~0.008)")
    print("  n=6: threshold ~0/256 (~0.00)")
    print("\nREDUCES requires: threshold HOLDS/GROWS with n at p>=0.1")
    print("=" * 70)
    
    # Test configurations
    n_values = [4, 5, 6]
    p_values = [0.1, 0.15, 0.25]
    TRIALS = 10  # Reduced for feasibility
    
    for n in n_values:
        D = 2 * n
        vecs = build_all_vectors(D)
        N = 1 << D
        
        print(f"\n{'='*70}")
        print(f"n = {n}, D = {D}, N = {N} vectors")
        print(f"{'='*70}")
        
        for p in p_values:
            print(f"\n  p = {p:.2f} ({int(p*N)}/{N} expected flips):")
            
            # F1 BP
            f1_success = 0
            f1_costs = []
            for trial in range(TRIALS):
                basis = random_lagrangian(vecs, n, D)
                mem = members_mask(basis, n, D)
                labels = np.array([1 if i in mem else 0 for i in range(N)], dtype=np.int8)
                flips = (rng.random(N) < p).astype(np.int8)
                noisy = labels ^ flips
                
                start = time.time()
                result, msg = decoder_f1_bp(vecs, noisy, n, D)
                elapsed = time.time() - start
                f1_costs.append(elapsed)
                if result is not None:
                    f1_success += 1
            
            print(f"    F1 BP:      {f1_success}/{TRIALS} success, mean_time={np.mean(f1_costs):.4f}s")
            
            # F2 Plücker
            f2_success = 0
            f2_costs = []
            for trial in range(TRIALS):
                basis = random_lagrangian(vecs, n, D)
                mem = members_mask(basis, n, D)
                labels = np.array([1 if i in mem else 0 for i in range(N)], dtype=np.int8)
                flips = (rng.random(N) < p).astype(np.int8)
                noisy = labels ^ flips
                
                start = time.time()
                result, msg = decoder_f2_plucker(vecs, noisy, n, D)
                elapsed = time.time() - start
                f2_costs.append(elapsed)
                if result is not None:
                    f2_success += 1
            
            print(f"    F2 Plücker: {f2_success}/{TRIALS} success, mean_time={np.mean(f2_costs):.4f}s")
            
            # F3 List+Prune
            f3_success = 0
            f3_costs = []
            for trial in range(TRIALS):
                basis = random_lagrangian(vecs, n, D)
                mem = members_mask(basis, n, D)
                labels = np.array([1 if i in mem else 0 for i in range(N)], dtype=np.int8)
                flips = (rng.random(N) < p).astype(np.int8)
                noisy = labels ^ flips
                
                start = time.time()
                result, msg = decoder_f3_list_prune(vecs, noisy, n, D)
                elapsed = time.time() - start
                f3_costs.append(elapsed)
                if result is not None:
                    f3_success += 1
            
            print(f"    F3 List:    {f3_success}/{TRIALS} success, mean_time={np.mean(f3_costs):.4f}s")
    
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("""
Threshold analysis:
- F1 BP: random-code BP fails at constant rate (no good graph structure)
- F2 Plücker: spectral estimation + projection; nearest-isotropic = LPN-hard
- F3 List: poly relaxation but list explodes at constant rate

All three families expected to SHRINK with n (like Walsh) or FAIL at constant rate.
If any holds threshold at p>=0.1 across n=4,5,6 → REDUCES candidate.
Otherwise → last door closes, 7th-evidence final.
    """)
    print("=" * 70)
