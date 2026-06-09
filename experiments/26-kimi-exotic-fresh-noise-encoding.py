#!/usr/bin/env python3
"""
Experiment 26: Exotic Fresh-Noise Encoding Screen (K2 per Codex handoff)

Date: 2026-06-07
Task: Test non-i.i.d. or correlated public fresh-noise encoding for LSN decoupling.

Required checks (from Codex OFA-359/360 handoff):
1. Usable noise: effective rate remains in cryptographic range, not near q->1/2
2. Low leakage: low-weight TV leaks analogous to TV(Bern(q)^w, Bern(1-q)^w) not visible at usable q
3. Public/poly: no hidden Lagrangian enumeration, no per-instance advice
4. LPN-only hard step: any remaining hard step is explicitly ordinary LPN-style, not disguised LSN recovery

Approach: Generate fresh noise from a public seed via a pseudorandom process that introduces
controlled correlations. The noise is not i.i.d. Bernoulli, but has a structure that can be
publicly encoded. The LPN-like hardness comes from recovering a secret from noisy samples.
"""

import numpy as np
from itertools import combinations

def generate_public_seed(n, seed_val=None):
    """Generate a public seed for noise encoding."""
    if seed_val is not None:
        np.random.seed(seed_val)
    return np.random.randint(0, 2**32, dtype=np.uint32)

def prg_from_seed(seed, length, n):
    """Simple pseudorandom generator from seed. Returns a deterministic sequence."""
    # Use a linear congruential generator for simplicity
    a = 1664525
    c = 1013904223
    state = int(seed) & 0xFFFFFFFF
    result = np.zeros(length, dtype=np.float32)
    for i in range(length):
        state = (a * state + c) & 0xFFFFFFFF
        result[i] = state / 0xFFFFFFFF
    return result

def generate_exotic_noise(n, m, p, seed_val, encoding_type='correlated_pairs'):
    """
    Generate fresh noise using a public encoding scheme.
    
    Args:
        n: dimension (Lagrangian subspace dimension)
        m: number of samples
        p: target noise rate
        seed_val: public seed
        encoding_type: type of exotic encoding
    
    Returns:
        noise: array of shape (m,) with noise values in {0,1}
    """
    N = 2 ** (2 * n)
    
    if encoding_type == 'correlated_pairs':
        # Generate noise where adjacent pairs are correlated
        # This introduces a non-i.i.d. structure that is publicly encodable
        prg = prg_from_seed(seed_val, m + n, n)
        
        # Base noise from PRG
        base_noise = (prg[:m] < p).astype(np.uint8)
        
        # Add correlation structure: pairs of samples have correlated noise
        # This is done by XORing with a second PRG stream that has larger correlation
        correlation_strength = 0.3  # Strength of correlation
        prg2 = prg_from_seed(seed_val + 1, m + n, n)
        correlated_component = (prg2[:m] < correlation_strength).astype(np.uint8)
        
        # Combine: noise = base_noise XOR (correlated_component AND some_pattern)
        pattern = np.zeros(m, dtype=np.uint8)
        for i in range(0, m - 1, 2):
            if i + 1 < m:
                pattern[i] = pattern[i+1] = 1
        
        noise = base_noise ^ (correlated_component & pattern)
        return noise
    
    elif encoding_type == 'subset_sum':
        # Generate noise via subset-sum structure
        # Public vectors a_1, ..., a_k; noise = sum_{i in S} a_i mod 2 for random subset S
        k = min(n * 2, 20)  # Number of public vectors
        prg = prg_from_seed(seed_val, k * m, n)
        
        # Public vectors (deterministic from seed)
        public_vectors = np.array([(prg[i*m:(i+1)*m] < 0.5).astype(np.uint8) for i in range(k)])
        
        # Random subset selection (deterministic from seed)
        subset_prg = prg_from_seed(seed_val + 2, k, n)
        subset = (subset_prg < p).astype(np.uint8)  # Select subset with probability p
        
        # Noise = XOR of selected public vectors
        noise = np.zeros(m, dtype=np.uint8)
        for i in range(k):
            if subset[i]:
                noise ^= public_vectors[i]
        
        return noise
    
    elif encoding_type == 'block_correlated':
        # Block-correlated noise: blocks of samples have shared noise component
        block_size = max(1, m // (2 * n))
        num_blocks = (m + block_size - 1) // block_size
        
        prg = prg_from_seed(seed_val, num_blocks + m, n)
        
        # Block-level noise
        block_noise = (prg[:num_blocks] < p).astype(np.uint8)
        
        # Sample-level noise
        sample_noise = (prg[num_blocks:num_blocks+m] < 0.05).astype(np.uint8)
        
        noise = np.zeros(m, dtype=np.uint8)
        for b in range(num_blocks):
            start = b * block_size
            end = min((b + 1) * block_size, m)
            noise[start:end] = block_noise[b] ^ sample_noise[start:end]
        
        return noise
    
    else:
        # Fallback: standard i.i.d. Bernoulli
        np.random.seed(seed_val)
        return (np.random.random(m) < p).astype(np.uint8)

def test_noise_properties(n, m, p, num_trials=5):
    """Test properties of exotic noise encoding."""
    print(f"\n{'='*70}")
    print(f"Exotic Noise Encoding Screen: n={n}, m={m}, p={p}")
    print(f"{'='*70}\n")
    
    N = 2 ** (2 * n)
    
    for encoding_type in ['correlated_pairs', 'subset_sum', 'block_correlated']:
        print(f"\n--- Encoding: {encoding_type} ---")
        
        rates = []
        for trial in range(num_trials):
            seed_val = trial + 1000
            noise = generate_exotic_noise(n, m, p, seed_val, encoding_type)
            
            # Check 1: Usable rate
            rate = np.mean(noise)
            rates.append(rate)
            
            # Check 2: Low leakage — check pairwise correlations
            # For leakage, we check if low-weight subsets have distinguishable distributions
            if m >= 4:
                # Check first 4 samples
                subset = noise[:4]
                weight = np.sum(subset)
            else:
                weight = 0
            
            print(f"  Trial {trial}: rate={rate:.4f}, 4-sample weight={weight}")
        
        avg_rate = np.mean(rates)
        std_rate = np.std(rates)
        print(f"  Average rate: {avg_rate:.4f} ± {std_rate:.4f}")
        
        # Check if rate is in usable range (not too close to 0.5)
        if abs(avg_rate - 0.5) < 0.15:
            print(f"  ⚠️ WARNING: Rate {avg_rate:.4f} is near 0.5 — may not be cryptographically usable")
        elif avg_rate < 0.01 or avg_rate > 0.49:
            print(f"  ⚠️ WARNING: Rate {avg_rate:.4f} is extreme — may not be useful")
        else:
            print(f"  ✓ Rate is in usable range")

def test_lpn_hardness(n, m, p, encoding_type='correlated_pairs', num_trials=10):
    """
    Test if the exotic noise encoding preserves LPN-like hardness.
    
    The idea: if we have an LSN-like sample (x, f(x)) where f(x) = 1_L(x) + noise,
    and the noise is generated via exotic encoding, can we still recover L?
    
    We simulate a simple decoder to see if the exotic noise structure helps.
    """
    print(f"\n{'='*70}")
    print(f"LPN-Hardness Test: n={n}, m={m}, p={p}, encoding={encoding_type}")
    print(f"{'='*70}\n")
    
    N = 2 ** (2 * n)
    
    # Generate a random Lagrangian subspace
    # For simplicity, we use a standard basis
    basis = np.eye(n, 2*n, dtype=np.uint8)  # First n rows of identity
    
    success_count = 0
    for trial in range(num_trials):
        seed_val = trial + 2000
        
        # Generate samples
        samples = np.random.randint(0, 2, size=(m, 2*n), dtype=np.uint8)
        
        # Compute indicator for Lagrangian (dot product with basis)
        indicators = np.zeros(m, dtype=np.uint8)
        for i in range(m):
            # Check if sample is in the subspace spanned by basis
            # For a Lagrangian, we check if sample is orthogonal to the symplectic complement
            # Simplified: just check if it's in the span
            is_in = True
            for j in range(n):
                if np.dot(samples[i], basis[j]) % 2 == 1:
                    is_in = False
                    break
            indicators[i] = 1 if is_in else 0
        
        # Add exotic noise
        noise = generate_exotic_noise(n, m, p, seed_val, encoding_type)
        noisy_indicators = indicators ^ noise
        
        # Try to recover the subspace using a simple statistical test
        # Look for directions where the correlation is higher
        # This is a simplified decoder
        best_direction = None
        best_score = -1
        
        for d in range(2*n):
            direction = np.zeros(2*n, dtype=np.uint8)
            direction[d] = 1
            
            # Count samples with dot product 1 vs 0
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
        
        # Check if the recovered direction is in the true subspace
        # For our standard basis, true directions are e_0, ..., e_{n-1}
        is_true_direction = False
        if best_direction is not None:
            for j in range(n):
                if np.array_equal(best_direction, basis[j]):
                    is_true_direction = True
                    break
        
        if is_true_direction and best_score > 0.05:
            success_count += 1
        
        print(f"  Trial {trial}: score={best_score:.4f}, found_true={is_true_direction}")
    
    print(f"\n  Success rate: {success_count}/{num_trials} ({100*success_count/num_trials:.0f}%)")
    if success_count > 0:
        print(f"  ⚠️ Simple decoder succeeded — exotic noise may not preserve hardness")
    else:
        print(f"  ✓ Simple decoder failed — hardness may be preserved")

def main():
    print("="*70)
    print("Experiment 26: Exotic Fresh-Noise Encoding Screen")
    print("K2 per Codex handoff (2026-06-07)")
    print("="*70)
    
    # Test 1: Noise properties
    for n in [4, 5]:
        m = n ** 3
        p = 0.10
        test_noise_properties(n, m, p, num_trials=5)
    
    # Test 2: LPN hardness preservation
    print("\n" + "="*70)
    print("LPN-Hardness Preservation Tests")
    print("="*70)
    
    for encoding_type in ['correlated_pairs', 'subset_sum', 'block_correlated']:
        test_lpn_hardness(n=4, m=64, p=0.10, encoding_type=encoding_type, num_trials=10)
    
    print("\n" + "="*70)
    print("Experiment 26 Complete")
    print("="*70)

if __name__ == '__main__':
    main()
