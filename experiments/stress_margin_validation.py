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

Stress-Margin Decoder Validation for n=20, 30, 40



Tests the noise wall prediction: at constant noise p=0.10,

recovery rate should approach 0 as n increases (m=poly(n)).



Usage:

    python3 stress_margin_validation.py --n 20 --m 10000 --trials 10 --p 0.10

"""



import argparse

import random

import numpy as np

from collections import defaultdict

import time





def random_lagrangian(n):

    """Generate a random Lagrangian subspace of dimension n in F_2^{2n}."""

    # Build a symplectic basis. A simple way: random isotropic basis.

    # Standard symplectic form J: [[0, I], [-I, 0]]

    # We'll construct a random isotropic subspace by iteratively adding vectors

    # orthogonal (with respect to the symplectic form) to existing ones.

    

    dim = 2 * n

    basis = []

    attempts = 0

    while len(basis) < n and attempts < 10000:

        v = np.random.randint(0, 2, size=dim, dtype=np.uint8)

        if np.all(v == 0):

            attempts += 1

            continue

        # Check isotropy: v^T J w = 0 for all w in basis

        is_isotropic = True

        for w in basis:

            # symplectic form: sum_{i=0}^{n-1} (v[i]*w[n+i] + v[n+i]*w[i]) mod 2

            val = 0

            for i in range(n):

                val += int(v[i]) * int(w[n + i]) + int(v[n + i]) * int(w[i])

            if val % 2 != 0:

                is_isotropic = False

                break

        if is_isotropic:

            # Check linear independence

            mat = np.array(basis + [v], dtype=np.uint8)

            if np.linalg.matrix_rank(mat) == len(basis) + 1:

                basis.append(v)

        attempts += 1

    

    if len(basis) < n:

        # Fallback: use a standard Lagrangian (first n coordinates)

        basis = [np.array([1 if i == j else 0 for j in range(dim)], dtype=np.uint8) for i in range(n)]

    

    return np.array(basis, dtype=np.uint8)





def in_lagrangian(x, basis):

    """Check if x is in the subspace spanned by basis."""

    # Use Gaussian elimination over F_2

    mat = np.vstack([basis, x]).astype(np.int32)

    rank_basis = np.linalg.matrix_rank(basis.astype(np.int32))

    rank_full = np.linalg.matrix_rank(mat)

    return rank_full == rank_basis





def symplectic_form(a, b, n):

    """Omega(a, b) = sum_{i=0}^{n-1} (a[i]*b[n+i] + a[n+i]*b[i]) mod 2."""

    val = 0

    for i in range(n):

        val += int(a[i]) * int(b[n + i]) + int(a[n + i]) * int(b[i])

    return val % 2





def generate_sample(L_basis, n, p):

    """Generate one LSN sample (x, y)."""

    dim = 2 * n

    x = np.random.randint(0, 2, size=dim, dtype=np.uint8)

    true_label = 1 if in_lagrangian(x, L_basis) else 0

    if random.random() < p:

        y = 1 - true_label

    else:

        y = true_label

    return x, y





def stress_margin_decode(samples, n, top_k=None):

    """Stress-margin decoder."""

    # Collect all observed-positive pairs (a, b) where y_a = y_b = 1

    positive_samples = [x for x, y in samples if y == 1]

    

    if len(positive_samples) < 2:

        return None

    

    # Score each z = a + b by symplectic stress

    score = defaultdict(int)

    for i in range(len(positive_samples)):

        for j in range(i + 1, len(positive_samples)):

            a = positive_samples[i]

            b = positive_samples[j]

            z = (a + b) % 2

            z_tuple = tuple(z)

            omega_ab = symplectic_form(a, b, n)

            if omega_ab == 0:

                score[z_tuple] += 1  # isotropic

            else:

                score[z_tuple] -= 1  # non-isotropic

    

    # Sort by score, take top candidates for basis vectors

    if not score:

        return None

    

    sorted_z = sorted(score.items(), key=lambda x: x[1], reverse=True)

    

    # Try to build a subspace from top-scoring z's

    candidate_basis = []

    for z_tuple, s in sorted_z:

        if s <= 0:

            break

        z = np.array(z_tuple, dtype=np.uint8)

        if np.all(z == 0):

            continue

        # Check isotropy with existing candidates

        is_iso = True

        for w in candidate_basis:

            if symplectic_form(z, w, n) != 0:

                is_iso = False

                break

        if is_iso:

            mat = np.array(candidate_basis + [z], dtype=np.uint8)

            if np.linalg.matrix_rank(mat.astype(np.int32)) == len(candidate_basis) + 1:

                candidate_basis.append(z)

                if len(candidate_basis) == n:

                    break

    

    if len(candidate_basis) < n:

        return None

    

    return np.array(candidate_basis, dtype=np.uint8)





def subspace_equal(basis1, basis2, n):

    """Check if two subspaces are equal."""

    # Check that each basis vector of 1 is in 2 and vice versa

    for v in basis1:

        if not in_lagrangian(v, basis2):

            return False

    for v in basis2:

        if not in_lagrangian(v, basis1):

            return False

    return True





def trial(n, m, p, verbose=False):

    """Run one trial. Returns 1 if recovered, 0 otherwise."""

    L_true = random_lagrangian(n)

    samples = [generate_sample(L_true, n, p) for _ in range(m)]

    L_guess = stress_margin_decode(samples, n)

    

    if L_guess is None:

        return 0

    

    recovered = subspace_equal(L_true, L_guess, n)

    if verbose:

        print(f"  n={n}, m={m}, p={p}: recovered={recovered}")

    return 1 if recovered else 0





def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--n", type=int, default=6)

    parser.add_argument("--m", type=int, default=10000)

    parser.add_argument("--trials", type=int, default=10)

    parser.add_argument("--p", type=float, default=0.10)

    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    

    print(f"Stress-Margin Decoder Validation")

    print(f"n={args.n}, m={args.m}, p={args.p}, trials={args.trials}")

    print(f"Expected recovery rate: should approach 0 for n → ∞ at constant p")

    print(f"Noise wall prediction: m must be Ω(2^{2*args.n}) for recovery")

    print(f"For n={args.n}, threshold m ≈ {2**(2*args.n):.2e}")

    print()

    

    successes = 0

    for t in range(args.trials):

        start = time.time()

        s = trial(args.n, args.m, args.p, verbose=args.verbose)

        successes += s

        if args.verbose:

            print(f"  Trial {t+1}/{args.trials}: {s} (time: {time.time()-start:.2f}s)")

    

    rate = successes / args.trials

    print(f"\nResults: {successes}/{args.trials} = {rate:.2%}")

    

    if rate < 0.1:

        print("VERDICT: Decoder fails at this (n,m,p) — consistent with noise wall")

    elif rate > 0.5:

        print("VERDICT: Decoder succeeds — below noise wall or above threshold m")

    else:

        print("VERDICT: Marginal — near threshold")





if __name__ == "__main__":

    main()
