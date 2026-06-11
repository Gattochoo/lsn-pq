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

Experiment 26b: Advanced Exotic Fresh-Noise Encoding (K2 follow-up)



Date: 2026-06-07

Task: Test stronger exotic noise structures that resist simple statistical decoders.



Hypothesis: Previous exotic encodings (correlated_pairs, subset_sum, block_correlated)

were broken because their LOW-LEVEL structure (adjacent correlations, low-weight subsets,

block boundaries) was exploitable by simple statistical tests. 



If we use:

1. Cryptographically strong PRG (SHA-256, not LCG)

2. Pairwise-independent hash family (universal hashing)

3. Multiple rounds of non-linear mixing



Then the noise should have NO detectable statistical structure that a simple decoder

can exploit. However, the adversary still knows the public seed, so this becomes a

question of computational vs statistical hardness.



The key question: Can exotic noise be BOTH publicly encodable AND statistically

indistinguishable from random noise to a simple decoder?

"""



import numpy as np

import hashlib

import struct

from itertools import combinations



def sha256_prg(seed, length):

    """Generate pseudorandom bits using SHA-256 in CTR mode."""

    result = np.zeros(length, dtype=np.float32)

    seed_bytes = struct.pack('<I', int(seed) & 0xFFFFFFFF)

    

    for i in range(0, length, 32):  # SHA-256 produces 32 bytes

        counter = struct.pack('<I', i // 32)

        hash_input = seed_bytes + counter

        hash_output = hashlib.sha256(hash_input).digest()

        

        for j in range(min(32, length - i)):

            result[i + j] = hash_output[j] / 255.0

    

    return result



def pairwise_independent_noise(n, m, p, seed_val):

    """Generate noise using pairwise-independent hash family."""

    # Use a finite field approach: h(x) = (a*x + b) mod q

    # For pairwise independence, a and b are random field elements

    q = 2**31 - 1  # Mersenne prime

    

    prg = sha256_prg(seed_val, 2)

    a = int(prg[0] * q) + 1  # Non-zero

    b = int(prg[1] * q)

    

    noise = np.zeros(m, dtype=np.uint8)

    for i in range(m):

        # h(i) = (a*i + b) mod q, then threshold

        val = (a * i + b) % q

        noise[i] = 1 if val < int(p * q) else 0

    

    return noise



def sponge_noise(n, m, p, seed_val, rounds=3):

    """Generate noise using a sponge-like construction with multiple rounds."""

    # Round 1: SHA-256

    round1 = sha256_prg(seed_val, m)

    

    # Round 2: XOR with shifted version

    round2 = np.zeros(m, dtype=np.float32)

    for i in range(m):

        prev = round1[(i - 1) % m]

        curr = round1[i]

        next_val = round1[(i + 1) % m]

        # Non-linear mixing: XOR-like operation on floats (approximated)

        round2[i] = (prev + curr + next_val) % 1.0

    

    # Round 3: S-box-like transformation

    sbox = np.arange(256, dtype=np.uint8)

    np.random.seed(seed_val + 1)

    np.random.shuffle(sbox)

    

    round3 = np.zeros(m, dtype=np.float32)

    for i in range(m):

        byte_val = int(round2[i] * 255) & 0xFF

        transformed = sbox[byte_val]

        round3[i] = transformed / 255.0

    

    # Final threshold

    noise = (round3 < p).astype(np.uint8)

    return noise



def entropy_smoothed_noise(n, m, p, seed_val):

    """Generate noise using entropy smoothing (extractor-like)."""

    # Generate more bits than needed, then extract

    oversample = 4 * m

    raw = sha256_prg(seed_val, oversample)

    

    # Extractor: XOR pairs of bits (von Neumann-like, simplified)

    extracted = np.zeros(m, dtype=np.float32)

    for i in range(m):

        b1 = 1 if raw[2*i] < 0.5 else 0

        b2 = 1 if raw[2*i + 1] < 0.5 else 0

        # XOR two independent bits

        extracted[i] = (b1 ^ b2) / 1.0  # 0 or 1

    

    # Apply threshold

    noise = np.zeros(m, dtype=np.uint8)

    for i in range(m):

        noise[i] = 1 if extracted[i] < p else 0

    

    return noise



def test_advanced_noise_properties(n, m, p, num_trials=5):

    """Test advanced exotic noise for statistical properties."""

    print(f"\n{'='*70}")

    print(f"Advanced Exotic Noise Screen: n={n}, m={m}, p={p}")

    print(f"{'='*70}\n")

    

    for encoding_type in ['pairwise_independent', 'sponge', 'entropy_smoothed']:

        print(f"\n--- Encoding: {encoding_type} ---")

        

        rates = []

        autocorrs = []

        

        for trial in range(num_trials):

            seed_val = trial + 5000

            

            if encoding_type == 'pairwise_independent':

                noise = pairwise_independent_noise(n, m, p, seed_val)

            elif encoding_type == 'sponge':

                noise = sponge_noise(n, m, p, seed_val)

            elif encoding_type == 'entropy_smoothed':

                noise = entropy_smoothed_noise(n, m, p, seed_val)

            

            rate = np.mean(noise)

            rates.append(rate)

            

            # Autocorrelation at lag 1

            if m > 1:

                autocorr = np.corrcoef(noise[:-1], noise[1:])[0, 1] if len(noise) > 1 else 0

            else:

                autocorr = 0

            autocorrs.append(autocorr)

            

            print(f"  Trial {trial}: rate={rate:.4f}, autocorr(lag1)={autocorr:.4f}")

        

        avg_rate = np.mean(rates)

        avg_autocorr = np.mean(autocorrs)

        

        print(f"  Average rate: {avg_rate:.4f}")

        print(f"  Average autocorr: {avg_autocorr:.4f}")

        

        # Check if rate is near 0.5 (high entropy, hard to predict)

        if abs(avg_rate - 0.5) < 0.1:

            print(f"  ⚠️ Rate near 0.5 — high entropy but may be near unusable")

        elif avg_rate < 0.01:

            print(f"  ⚠️ Rate near 0 — no noise added")

        else:

            print(f"  ✓ Rate in usable range")

        

        # Check autocorrelation

        if abs(avg_autocorr) > 0.1:

            print(f"  ⚠️ Significant autocorrelation detected — structure present")

        else:

            print(f"  ✓ Low autocorrelation — looks pairwise independent")



def advanced_lpn_test(n, m, p, encoding_type='sponge', num_trials=10):

    """Test if advanced exotic noise resists simple statistical decoder."""

    print(f"\n{'='*70}")

    print(f"Advanced LPN Test: n={n}, m={m}, p={p}, encoding={encoding_type}")

    print(f"{'='*70}\n")

    

    # Generate a random Lagrangian subspace (simplified: standard basis)

    basis = np.eye(n, 2*n, dtype=np.uint8)

    

    success_count = 0

    random_success_count = 0

    

    for trial in range(num_trials):

        seed_val = trial + 6000

        

        # Generate random samples

        samples = np.random.randint(0, 2, size=(m, 2*n), dtype=np.uint8)

        

        # Compute Lagrangian indicator

        indicators = np.zeros(m, dtype=np.uint8)

        for i in range(m):

            is_in = True

            for j in range(n):

                if np.dot(samples[i], basis[j]) % 2 == 1:

                    is_in = False

                    break

            indicators[i] = 1 if is_in else 0

        

        # Add advanced exotic noise

        if encoding_type == 'pairwise_independent':

            noise = pairwise_independent_noise(n, m, p, seed_val)

        elif encoding_type == 'sponge':

            noise = sponge_noise(n, m, p, seed_val)

        elif encoding_type == 'entropy_smoothed':

            noise = entropy_smoothed_noise(n, m, p, seed_val)

        else:

            # Standard i.i.d. Bernoulli for comparison

            np.random.seed(seed_val)

            noise = (np.random.random(m) < p).astype(np.uint8)

        

        noisy_indicators = indicators ^ noise

        

        # Simple statistical decoder (same as before)

        best_direction = None

        best_score = -1

        

        for d in range(2*n):

            direction = np.zeros(2*n, dtype=np.uint8)

            direction[d] = 1

            

            dots = np.dot(samples, direction) % 2

            count_0 = np.sum(noisy_indicators[dots == 0])

            count_1 = np.sum(noisy_indicators[dots == 1])

            total_0 = np.sum(dots == 0)

            total_1 = np.sum(dots == 1)

            

            if total_0 > 0 and total_1 > 0:

                rate_0 = count_0 / total_0

                rate_1 = count_1 / total_1

                score = abs(rate_0 - rate_1)

                

                if score > best_score:

                    best_score = score

                    best_direction = direction

        

        # Check if true direction found

        is_true = False

        if best_direction is not None:

            for j in range(n):

                if np.array_equal(best_direction, basis[j]):

                    is_true = True

                    break

        

        # Random guessing baseline

        random_guess = np.random.randint(0, 2*n)

        random_is_true = (random_guess < n)

        

        if is_true and best_score > 0.05:

            success_count += 1

        if random_is_true:

            random_success_count += 1

        

        print(f"  Trial {trial}: score={best_score:.4f}, found_true={is_true}, random_true={random_is_true}")

    

    print(f"\n  Decoder success: {success_count}/{num_trials} ({100*success_count/num_trials:.0f}%)")

    print(f"  Random baseline: {random_success_count}/{num_trials} ({100*random_success_count/num_trials:.0f}%)")

    

    if success_count > random_success_count + 2:

        print(f"  ⚠️ Decoder significantly outperforms random — structure leaked")

        return False

    elif success_count <= random_success_count + 1:

        print(f"  ✓ Decoder at random baseline — no detectable structure")

        return True

    else:

        print(f"  ⚠️ Marginal — may need more trials")

        return None



def main():

    print("="*70)

    print("Experiment 26b: Advanced Exotic Fresh-Noise Encoding")

    print("K2 follow-up — stronger PRG and non-linear mixing")

    print("="*70)

    

    # Test 1: Noise properties (autocorrelation, rate)

    for n in [4, 5]:

        m = n ** 3

        p = 0.10

        test_advanced_noise_properties(n, m, p, num_trials=5)

    

    # Test 2: LPN hardness with advanced noise

    print("\n" + "="*70)

    print("LPN-Hardness Tests with Advanced Noise")

    print("="*70)

    

    results = {}

    for encoding in ['pairwise_independent', 'sponge', 'entropy_smoothed']:

        results[encoding] = advanced_lpn_test(4, 64, 0.10, encoding, num_trials=20)

    

    # Test 3: Standard i.i.d. for comparison

    print("\n" + "="*70)

    print("Baseline: Standard i.i.d. Bernoulli")

    print("="*70)

    results['iid'] = advanced_lpn_test(4, 64, 0.10, 'iid', num_trials=20)

    

    print("\n" + "="*70)

    print("Summary")

    print("="*70)

    for enc, result in results.items():

        status = "PASS" if result == True else "FAIL" if result == False else "UNCLEAR"

        print(f"  {enc}: {status}")

    

    print("\n" + "="*70)

    print("Experiment 26b Complete")

    print("="*70)



if __name__ == '__main__':

    main()
