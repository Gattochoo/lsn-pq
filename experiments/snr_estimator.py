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

SNR Estimator for Stress-Margin Decoder



Directly estimates the signal-to-noise ratio without running the full decoder.

This avoids decoder implementation bugs and focuses on the theoretical prediction.



Usage:

    python3 snr_estimator.py --n 6 8 10 12 15 20 --m 10000 --p 0.10 --trials 100

"""



import argparse

import random

import numpy as np

from collections import defaultdict

import time





def random_lagrangian(n):

    """Generate a random Lagrangian subspace of dimension n in F_2^{2n}."""

    dim = 2 * n

    basis = []

    attempts = 0

    while len(basis) < n and attempts < 10000:

        v = np.random.randint(0, 2, size=dim, dtype=np.uint8)

        if np.all(v == 0):

            attempts += 1

            continue

        is_isotropic = True

        for w in basis:

            val = 0

            for i in range(n):

                val += int(v[i]) * int(w[n + i]) + int(v[n + i]) * int(w[i])

            if val % 2 != 0:

                is_isotropic = False

                break

        if is_isotropic:

            mat = np.array(basis + [v], dtype=np.uint8)

            if np.linalg.matrix_rank(mat) == len(basis) + 1:

                basis.append(v)

        attempts += 1

    if len(basis) < n:

        basis = [np.array([1 if i == j else 0 for j in range(dim)], dtype=np.uint8) for i in range(n)]

    return np.array(basis, dtype=np.uint8)





def in_lagrangian(x, basis):

    """Check if x is in the subspace spanned by basis."""

    mat = np.vstack([basis, x]).astype(np.int32)

    rank_basis = np.linalg.matrix_rank(basis.astype(np.int32))

    rank_full = np.linalg.matrix_rank(mat)

    return rank_full == rank_basis





def symplectic_form(a, b, n):

    val = 0

    for i in range(n):

        val += int(a[i]) * int(b[n + i]) + int(a[n + i]) * int(b[i])

    return val % 2





def estimate_snr(n, m, p, trials=100):

    """Estimate SNR for stress-margin decoder."""

    dim = 2 * n

    

    # Expected values (theoretical)

    P_y1 = p + (1 - 2*p) / (2 ** (2*n))

    m_tp = m * (1 - p) / (2 ** n)

    m_fp = m * p * (1 - 1 / (2 ** (2*n)))

    m_pos = m_tp + m_fp

    

    true_true_pairs = m_tp * m_tp / 2

    total_pairs = m_pos * m_pos / 2

    

    # Number of z values in V

    num_z = 2 ** (2 * n)

    

    # Expected pairs per z (uniform)

    pairs_per_z = total_pairs / num_z if num_z > 0 else 0

    

    # True-true pairs per z (for z in L, approx 2^{n-1} of the 2^n pairs)

    # Actually for random z, fraction of true-true pairs that hit z is 1/2^n for z in L, 0 for z not in L

    # But expected per z (averaging over random L): 

    # Each true-true pair (a,b) generates z = a+b. Since a,b uniform in L, z is uniform in L.

    # So for a random z in V, P(z in L) = 1/2^n.

    # Expected true-true pairs per z = true_true_pairs * (1/2^n) if we average over z.

    true_true_per_z = true_true_pairs / (2 ** n) if 2**n > 0 else 0

    

    # Signal per z: true_true_per_z * (+1) + noise_pairs_per_z * (0 expected)

    signal_per_z = true_true_per_z

    

    # Variance: noise_pairs_per_z * 1 (each noise pair contributes ±1 with var 1)

    noise_pairs_per_z = pairs_per_z - true_true_per_z

    variance_per_z = noise_pairs_per_z

    

    # SNR per z

    snr_per_z = (signal_per_z ** 2) / variance_per_z if variance_per_z > 0 else float('inf')

    

    # Empirical verification (sample-based)

    empirical_signal = 0

    empirical_variance = 0

    for _ in range(trials):

        L = random_lagrangian(n)

        samples = []

        for _ in range(m):

            x = np.random.randint(0, 2, size=dim, dtype=np.uint8)

            true_label = 1 if in_lagrangian(x, L) else 0

            if random.random() < p:

                y = 1 - true_label

            else:

                y = true_label

            if y == 1:

                samples.append(x)

        

        # Count true-true pairs and total pairs

        true_positives = [x for x in samples if in_lagrangian(x, L)]

        false_positives = [x for x in samples if not in_lagrangian(x, L)]

        

        tt_pairs = len(true_positives) * (len(true_positives) - 1) / 2

        tf_pairs = len(true_positives) * len(false_positives)

        ff_pairs = len(false_positives) * (len(false_positives) - 1) / 2

        total_pairs_emp = len(samples) * (len(samples) - 1) / 2

        

        empirical_signal += tt_pairs / trials

        empirical_variance += (tf_pairs + ff_pairs) / trials

    

    empirical_snr = (empirical_signal ** 2) / empirical_variance if empirical_variance > 0 else float('inf')

    

    return {

        'n': n,

        'm': m,

        'p': p,

        'm_tp': m_tp,

        'm_fp': m_fp,

        'm_pos': m_pos,

        'true_true_pairs': true_true_pairs,

        'total_pairs': total_pairs,

        'pairs_per_z': pairs_per_z,

        'true_true_per_z': true_true_per_z,

        'signal_per_z': signal_per_z,

        'variance_per_z': variance_per_z,

        'snr_per_z': snr_per_z,

        'empirical_snr': empirical_snr,

        'empirical_signal': empirical_signal,

        'empirical_variance': empirical_variance,

        'threshold_m': (2 ** (2*n)) * p / ((1-p)**2) if p > 0 else float('inf')

    }





def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--n", type=int, nargs='+', default=[6, 8, 10, 12, 15])

    parser.add_argument("--m", type=int, default=10000)

    parser.add_argument("--p", type=float, default=0.10)

    parser.add_argument("--trials", type=int, default=100)

    args = parser.parse_args()

    

    print("SNR Estimation for Stress-Margin Decoder")

    print(f"m={args.m}, p={args.p}, trials={args.trials}")

    print()

    print(f"{'n':>3} {'m_tp':>10} {'m_fp':>10} {'m_pos':>10} {'tt_pairs':>12} {'tot_pairs':>12} {'pairs/z':>10} {'tt/z':>10} {'SNR/z':>12} {'emp_SNR':>12} {'threshold_m':>15}")

    print("-" * 120)

    

    for n in args.n:

        start = time.time()

        result = estimate_snr(n, args.m, args.p, args.trials)

        elapsed = time.time() - start

        

        print(f"{n:>3} {result['m_tp']:>10.1f} {result['m_fp']:>10.1f} {result['m_pos']:>10.1f} "

              f"{result['true_true_pairs']:>12.1f} {result['total_pairs']:>12.1f} "

              f"{result['pairs_per_z']:>10.2e} {result['true_true_per_z']:>10.2e} "

              f"{result['snr_per_z']:>12.2e} {result['empirical_snr']:>12.2e} "

              f"{result['threshold_m']:>15.2e} ({elapsed:.1f}s)")

        

        if result['snr_per_z'] < 1:

            print(f"  → SNR < 1: decoder likely FAILS (below threshold)")

        elif result['snr_per_z'] > 10:

            print(f"  → SNR > 10: decoder likely SUCCEEDS")

        else:

            print(f"  → SNR ≈ 1: marginal, near threshold")

        print()





if __name__ == "__main__":

    main()
