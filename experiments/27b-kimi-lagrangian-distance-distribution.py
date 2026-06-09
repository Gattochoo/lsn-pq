#!/usr/bin/env python3
"""
Experiment 27b: Lagrangian Pairwise Distance Distribution (K3 computational exploration)

Date: 2026-06-07
Task: Compute the distribution of dim(L ∩ L') for random Lagrangians L, L' in 𝔽₂²ⁿ.

This is the critical missing piece for the SQ lower bound proof (K3).
The intersection dimension determines the correlation between sympLPN distributions.

Key question: Is the distribution concentrated around n/2, or are there many "near" pairs?
"""

import numpy as np
from itertools import combinations
import json

def symplectic_form(v, w):
    """Standard symplectic form Ω(v, w) = Σ_{i=0}^{n-1} (v_{2i} w_{2i+1} + v_{2i+1} w_{2i})."""
    n = len(v) // 2
    result = 0
    for i in range(n):
        result += (v[2*i] * w[2*i + 1] + v[2*i + 1] * w[2*i])
    return result % 2

def is_isotropic(subspace):
    """Check if a subspace is isotropic (Ω vanishes on all pairs)."""
    basis = subspace
    for i in range(len(basis)):
        for j in range(i, len(basis)):
            if symplectic_form(basis[i], basis[j]) != 0:
                return False
    return True

def extend_to_lagrangian(isotropic_basis, n):
    """Extend an isotropic basis to a Lagrangian basis."""
    basis = list(isotropic_basis)
    dim = 2 * n
    
    # Start with the given isotropic basis
    # Try to add vectors one by one
    for attempt in range(1000):
        candidate = np.random.randint(0, 2, dim, dtype=np.uint8)
        
        # Check if candidate is linearly independent from current basis
        if len(basis) > 0:
            # Check linear independence by row reduction
            mat = np.array(basis + [candidate], dtype=np.uint8)
            rank = np.linalg.matrix_rank(mat) % 2  # This is not correct for 𝔽₂, but for small n it's a heuristic
            # Actually, let's just check if candidate is in the span
            is_in_span = False
            for mask in range(1, 1 << len(basis)):
                combo = np.zeros(dim, dtype=np.uint8)
                for i in range(len(basis)):
                    if mask & (1 << i):
                        combo ^= basis[i]
                if np.array_equal(candidate, combo):
                    is_in_span = True
                    break
            if is_in_span:
                continue
        
        # Check if candidate is isotropic with the current basis
        is_isotropic_with_basis = True
        for b in basis:
            if symplectic_form(b, candidate) != 0:
                is_isotropic_with_basis = False
                break
        
        if is_isotropic_with_basis:
            basis.append(candidate)
            if len(basis) == n:
                return np.array(basis, dtype=np.uint8)
    
    return None  # Failed to extend

def generate_random_lagrangian(n):
    """Generate a random Lagrangian subspace basis in 𝔽₂²ⁿ."""
    dim = 2 * n
    
    # Try a simple approach: generate random isotropic vectors and extend
    for attempt in range(100):
        # Start with a random isotropic vector
        v1 = np.random.randint(0, 2, dim, dtype=np.uint8)
        if np.all(v1 == 0):
            continue
        
        # Find another isotropic vector orthogonal to v1
        for _ in range(100):
            v2 = np.random.randint(0, 2, dim, dtype=np.uint8)
            if np.all(v2 == 0):
                continue
            if symplectic_form(v1, v2) == 0 and not np.array_equal(v1, v2):
                # Check if v2 is independent of v1
                if not np.array_equal(v2, v1):
                    basis = [v1, v2]
                    
                    # Extend to full Lagrangian
                    result = extend_to_lagrangian(basis, n)
                    if result is not None:
                        return result
    
    # Fallback: use standard basis
    basis = []
    for i in range(n):
        v = np.zeros(dim, dtype=np.uint8)
        v[2*i] = 1
        basis.append(v)
    return np.array(basis, dtype=np.uint8)

def lagrangian_from_basis(basis, n):
    """Generate all points in the Lagrangian subspace from a basis."""
    points = []
    for mask in range(1 << n):
        point = np.zeros(2*n, dtype=np.uint8)
        for i in range(n):
            if mask & (1 << i):
                point ^= basis[i]
        points.append(point)
    return np.array(points)

def intersection_dim(L1_points, L2_points):
    """Compute dim(L1 ∩ L2) by finding the dimension of the intersection."""
    # Convert to sets of tuples for fast lookup
    set1 = set(map(tuple, L1_points))
    set2 = set(map(tuple, L2_points))
    intersection = set1 & set2
    
    # The intersection is a subspace, so its size is 2^dim
    size = len(intersection)
    if size == 0:
        return 0
    
    # Find dimension: 2^dim = size
    dim = int(np.log2(size))
    assert 2**dim == size, f"Intersection size {size} is not a power of 2"
    return dim

def test_lagrangian_distance_distribution(n, num_pairs=100):
    """Test the distribution of dim(L1 ∩ L2) for random Lagrangians."""
    print(f"\n{'='*70}")
    print(f"Lagrangian Distance Distribution: n={n}, {num_pairs} pairs")
    print(f"{'='*70}")
    
    intersections = []
    
    for i in range(num_pairs):
        L1_basis = generate_random_lagrangian(n)
        L2_basis = generate_random_lagrangian(n)
        
        L1_points = lagrangian_from_basis(L1_basis, n)
        L2_points = lagrangian_from_basis(L2_basis, n)
        
        dim_int = intersection_dim(L1_points, L2_points)
        intersections.append(dim_int)
        
        if i < 5:
            print(f"  Pair {i}: dim(L1 ∩ L2) = {dim_int}")
    
    intersections = np.array(intersections)
    
    # Distribution
    print(f"\nDistribution of dim(L1 ∩ L2):")
    for k in range(n + 1):
        count = np.sum(intersections == k)
        pct = 100 * count / len(intersections)
        bar = "█" * int(pct / 2)
        print(f"  dim = {k:2d}: {count:3d}/{len(intersections)} ({pct:5.1f}%) {bar}")
    
    # Statistics
    mean = np.mean(intersections)
    std = np.std(intersections)
    print(f"\n  Mean: {mean:.2f}")
    print(f"  Std:  {std:.2f}")
    print(f"  Min:  {np.min(intersections)}")
    print(f"  Max:  {np.max(intersections)}")
    
    # Fraction of "near" pairs (dim > n/2)
    threshold = n / 2
    near_pairs = np.sum(intersections > threshold) / len(intersections)
    print(f"\n  Fraction with dim > {threshold}: {near_pairs:.2%}")
    
    # Fraction of "very near" pairs (dim > n/2 + sqrt(n))
    if n >= 4:
        threshold2 = n / 2 + np.sqrt(n)
        very_near = np.sum(intersections > threshold2) / len(intersections)
        print(f"  Fraction with dim > {threshold2:.1f}: {very_near:.2%}")
    
    return intersections

def test_small_n_exact(n, num_pairs=200):
    """For small n, generate more pairs for better statistics."""
    print(f"\n{'='*70}")
    print(f"Extended Distribution: n={n}, {num_pairs} pairs")
    print(f"{'='*70}")
    
    intersections = []
    
    for i in range(num_pairs):
        L1_basis = generate_random_lagrangian(n)
        L2_basis = generate_random_lagrangian(n)
        
        L1_points = lagrangian_from_basis(L1_basis, n)
        L2_points = lagrangian_from_basis(L2_basis, n)
        
        dim_int = intersection_dim(L1_points, L2_points)
        intersections.append(dim_int)
    
    intersections = np.array(intersections)
    
    # Distribution
    for k in range(n + 1):
        count = np.sum(intersections == k)
        pct = 100 * count / len(intersections)
        bar = "█" * int(pct / 2)
        print(f"  dim = {k:2d}: {count:4d}/{len(intersections)} ({pct:5.1f}%) {bar}")
    
    mean = np.mean(intersections)
    std = np.std(intersections)
    print(f"\n  Mean: {mean:.3f}")
    print(f"  Std:  {std:.3f}")
    
    # Compute expected value if uniform over all Lagrangians
    # The number of Lagrangians with intersection dimension k with a fixed L
    # This is related to the q-binomial coefficients
    
    return intersections

def theoretical_prediction(n):
    """Print theoretical predictions about the intersection distribution."""
    print(f"\n{'='*70}")
    print(f"Theoretical Predictions for n={n}")
    print(f"{'='*70}")
    
    # The number of k-dimensional isotropic subspaces in a fixed Lagrangian L
    # is given by the Gaussian binomial coefficient [n choose k]_2
    
    # For the intersection of two random Lagrangians:
    # The expected dimension is roughly n/2 (heuristic: random subspaces)
    
    # Actually, the exact distribution is known for the Lagrangian Grassmannian
    # The Schubert cells give the intersection structure
    
    # A rough heuristic: the intersection dimension is like a binomial(n, 1/2)
    # but with constraints from the symplectic form
    
    print(f"  Heuristic: dim(L1 ∩ L2) ~ Binomial(n, 1/2) with constraints")
    print(f"  Expected value: ~{n/2:.1f}")
    print(f"  Standard deviation: ~{np.sqrt(n)/2:.1f}")
    print(f"  (If binomial-like, variance = n/4)")
    
    # More precise: the number of Lagrangians intersecting a fixed L in dimension k
    # is related to the number of k-dimensional subspaces of L and their symplectic complements
    
    print(f"\n  Number of Lagrangians: ~2^{n**2 + n} (asymptotic)")
    print(f"  Number of k-dim subspaces of a Lagrangian: Gaussian binomial coeff [n choose k]_2")

def main():
    print("="*70)
    print("Experiment 27b: Lagrangian Pairwise Distance Distribution")
    print("K3 computational exploration — critical gap for SQ lower bound")
    print("="*70)
    
    # Test small n
    for n in [2, 3, 4]:
        test_small_n_exact(n, num_pairs=200)
        theoretical_prediction(n)
    
    # Test larger n
    for n in [5, 6]:
        test_lagrangian_distance_distribution(n, num_pairs=100)
    
    print(f"\n{'='*70}")
    print("Summary and Implications")
    print(f"{'='*70}")
    print("""
Key observations:
1. If dim(L1 ∩ L2) is concentrated around n/2 with small variance,
   then most pairs are "generic" and correlations are exponentially small.

2. If there is a significant tail (many pairs with dim > n/2 + O(1)),
   then near pairs may dominate the average correlation.

3. The SQ lower bound depends on the average correlation over ALL pairs,
   weighted by the distance distribution. Near pairs (high intersection)
   have higher correlation and can dominate if sufficiently frequent.

4. The critical question: Is the fraction of near pairs (dim > n/2 + c*sqrt(n))
   exponentially small in n? If yes, then the average correlation is
   dominated by generic pairs and is exponentially small.

5. If the distribution is roughly binomial(n, 1/2), then by Chernoff bound,
   the fraction of pairs with dim > n/2 + c*sqrt(n) is O(exp(-c²)) —
   exponentially small in c², but for c = O(1), it's a constant fraction.
   However, for the average correlation, we need the weighted sum.
""")

if __name__ == '__main__':
    main()
