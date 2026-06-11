#!/usr/bin/env python3

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

Experiment 27b-v3: Correct Lagrangian Distance Distribution (K3)



This version uses a correct method to generate random Lagrangians.

We build a random isotropic basis by choosing vectors one at a time,

ensuring each new vector is orthogonal to all previous ones with respect to Ω.



Key insight: A Lagrangian is a maximal isotropic subspace (dimension n in 2n space).

To generate one: start with a random non-zero vector, then extend to a maximal isotropic subspace.

"""



import numpy as np

from itertools import combinations



def symplectic_form(v, w):

    """Standard symplectic form Ω(v, w) = Σ_i (v_{2i} w_{2i+1} + v_{2i+1} w_{2i})."""

    n = len(v) // 2

    result = 0

    for i in range(n):

        result += (v[2*i] * w[2*i + 1] + v[2*i + 1] * w[2*i])

    return result % 2



def random_isotropic_extension(current_basis, n, max_attempts=10000):

    """

    Extend an isotropic subspace by one dimension.

    Find a vector v not in span(current_basis) such that Ω(v, b) = 0 for all b in current_basis.

    """

    dim = 2 * n

    k = len(current_basis)

    

    # Generate all vectors in the span of current_basis (for independence check)

    span_vectors = set()

    for mask in range(1 << k):

        v = np.zeros(dim, dtype=np.int64)

        for i in range(k):

            if mask & (1 << i):

                v ^= current_basis[i]

        span_vectors.add(tuple(v))

    

    for _ in range(max_attempts):

        v = np.random.randint(0, 2, dim, dtype=np.int64)

        if tuple(v) in span_vectors:

            continue

        

        # Check if v is isotropic with all basis vectors

        is_isotropic = True

        for b in current_basis:

            if symplectic_form(v, b) != 0:

                is_isotropic = False

                break

        

        if is_isotropic:

            return v

    

    return None



def random_lagrangian(n, max_attempts=100):

    """Generate a random Lagrangian subspace basis in F_2^{2n}."""

    basis = []

    

    for attempt in range(max_attempts):

        # Start with a random non-zero vector

        v0 = np.random.randint(0, 2, 2*n, dtype=np.int64)

        if not np.any(v0):

            continue

        

        basis = [v0]

        

        # Extend to dimension n

        for i in range(1, n):

            new_v = random_isotropic_extension(basis, n)

            if new_v is None:

                break

            basis.append(new_v)

        

        if len(basis) == n:

            return np.array(basis, dtype=np.int64)

    

    # Ultimate fallback: standard basis

    basis = []

    for i in range(n):

        v = np.zeros(2*n, dtype=np.int64)

        v[2*i] = 1

        basis.append(v)

    return np.array(basis, dtype=np.int64)



def lagrangian_points(basis, n):

    """Generate all 2^n points in the Lagrangian subspace."""

    points = []

    for mask in range(1 << n):

        pt = np.zeros(2*n, dtype=np.int64)

        for i in range(n):

            if mask & (1 << i):

                pt ^= basis[i]

        points.append(tuple(pt))

    return set(points)



def intersection_dim(L1_points, L2_points):

    """Compute dim(L1 ∩ L2)."""

    intersection = L1_points & L2_points

    size = len(intersection)

    if size == 0:

        return 0

    dim = int(np.log2(size))

    return dim



def test_distance_distribution(n, num_pairs=200):

    """Test the distribution of dim(L1 ∩ L2) for random Lagrangians."""

    print(f"\n{'='*70}")

    print(f"Distance Distribution: n={n}, {num_pairs} pairs")

    print(f"{'='*70}")

    

    intersections = []

    

    for i in range(num_pairs):

        L1 = random_lagrangian(n)

        L2 = random_lagrangian(n)

        

        L1_points = lagrangian_points(L1, n)

        L2_points = lagrangian_points(L2, n)

        

        dim_int = intersection_dim(L1_points, L2_points)

        intersections.append(dim_int)

        

        if i < 5:

            print(f"  Pair {i}: dim(L1 ∩ L2) = {dim_int}")

    

    intersections = np.array(intersections)

    

    print(f"\nDistribution of dim(L1 ∩ L2):")

    for k in range(n + 1):

        count = np.sum(intersections == k)

        pct = 100 * count / len(intersections)

        bar = "█" * int(pct / 2)

        print(f"  dim = {k:2d}: {count:4d}/{len(intersections)} ({pct:5.1f}%) {bar}")

    

    mean = np.mean(intersections)

    std = np.std(intersections)

    print(f"\n  Mean: {mean:.3f}")

    print(f"  Std:  {std:.3f}")

    print(f"  Min:  {np.min(intersections)}")

    print(f"  Max:  {np.max(intersections)}")

    

    # Theoretical predictions

    print(f"\n  Theoretical predictions:")

    print(f"    Expected mean (heuristic n/2): {n/2:.1f}")

    print(f"    Actual mean: {mean:.3f}")

    

    # Fraction near n/2

    threshold = n / 2

    near = np.sum(intersections > threshold) / len(intersections)

    print(f"\n  Fraction with dim > {threshold}: {near:.2%}")

    

    return intersections



def main():

    print("="*70)

    print("Experiment 27b-v3: Correct Lagrangian Distance Distribution")

    print("K3 computational exploration — correct isotropic extension")

    print("="*70)

    

    for n in [2, 3, 4]:

        test_distance_distribution(n, num_pairs=200)

    

    for n in [5, 6]:

        test_distance_distribution(n, num_pairs=100)

    

    print(f"\n{'='*70}")

    print("Summary")

    print(f"{'='*70}")

    print("""

The distribution of dim(L1 ∩ L2) determines the average correlation between

sympLPN distributions. If the distribution is concentrated at small values

(relative to n), then the average correlation is exponentially small and the

SQ lower bound holds.



Key question: Does the mean grow with n, or stay constant?

If the mean grows as n/2, then near pairs may dominate.

If the mean stays small, then generic pairs dominate and SQ hardness holds.

""")



if __name__ == '__main__':

    main()
