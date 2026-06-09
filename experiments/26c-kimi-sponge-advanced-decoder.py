#!/usr/bin/env python3
"""
Experiment 26c: Advanced Decoder Attack on Sponge Noise (K2 final screen)

No scipy dependency — pure numpy implementation.
"""

import numpy as np
import hashlib
import struct

def sha256_prg(seed, length):
    """Generate pseudorandom bits using SHA-256 in CTR mode."""
    result = np.zeros(length, dtype=np.float32)
    seed_bytes = struct.pack('<I', int(seed) & 0xFFFFFFFF)
    
    for i in range(0, length, 32):
        counter = struct.pack('<I', i // 32)
        hash_input = seed_bytes + counter
        hash_output = hashlib.sha256(hash_input).digest()
        
        for j in range(min(32, length - i)):
            result[i + j] = hash_output[j] / 255.0
    
    return result

def sponge_noise(n, m, p, seed_val, rounds=3):
    """Sponge construction from 26b."""
    round1 = sha256_prg(seed_val, m)
    
    round2 = np.zeros(m, dtype=np.float32)
    for i in range(m):
        prev = round1[(i - 1) % m]
        curr = round1[i]
        next_val = round1[(i + 1) % m]
        round2[i] = (prev + curr + next_val) % 1.0
    
    sbox = np.arange(256, dtype=np.uint8)
    np.random.seed(seed_val + 1)
    np.random.shuffle(sbox)
    
    round3 = np.zeros(m, dtype=np.float32)
    for i in range(m):
        byte_val = int(round2[i] * 255) & 0xFF
        transformed = sbox[byte_val]
        round3[i] = transformed / 255.0
    
    noise = (round3 < p).astype(np.uint8)
    return noise

def test_higher_order_stats(noise):
    """Test higher-order statistical properties."""
    m = len(noise)
    results = {}
    
    # 1. Higher-order autocorrelation
    for lag in [1, 2, 3, 4, 5]:
        if m > lag:
            corr = np.corrcoef(noise[:-lag], noise[lag:])[0, 1]
            if np.isnan(corr):
                corr = 0.0
            results[f'autocorr_lag{lag}'] = corr
    
    # 2. Runs test (for randomness)
    runs, n1, n2 = 1, np.sum(noise), np.sum(1 - noise)
    for i in range(1, m):
        if noise[i] != noise[i-1]:
            runs += 1
    
    expected_runs = (2 * n1 * n2 / m) + 1 if m > 0 else 1
    var_runs = (2 * n1 * n2 * (2 * n1 * n2 - m)) / (m**2 * (m - 1)) if m > 1 and m**2 > 0 else 1
    z_score = (runs - expected_runs) / np.sqrt(var_runs) if var_runs > 0 else 0
    results['runs_z_score'] = z_score
    
    # 3. Higher-order moments
    noise_f = noise.astype(np.float64)
    mean = np.mean(noise_f)
    std = np.std(noise_f)
    if std > 0:
        skew = np.mean((noise_f - mean)**3) / (std**3)
        kurt = np.mean((noise_f - mean)**4) / (std**4) - 3.0
    else:
        skew = 0.0
        kurt = 0.0
    results['skewness'] = skew
    results['kurtosis'] = kurt
    
    # 4. Entropy estimation
    p_emp = np.mean(noise)
    if 0 < p_emp < 1:
        entropy = -p_emp * np.log2(p_emp) - (1 - p_emp) * np.log2(1 - p_emp)
    else:
        entropy = 0.0
    results['entropy'] = entropy
    results['entropy_ratio'] = entropy / 1.0
    
    # 5. Serial test (2-bit patterns)
    if m >= 2:
        patterns = {'00': 0, '01': 0, '10': 0, '11': 0}
        for i in range(m - 1):
            pattern = f"{noise[i]}{noise[i+1]}"
            patterns[pattern] += 1
        total = sum(patterns.values())
        if total > 0:
            expected = total / 4.0
            chi2 = sum((obs - expected)**2 / expected for obs in patterns.values() if expected > 0)
            results['serial_chi2'] = chi2
    
    # 6. Triple-bit patterns
    if m >= 3:
        triple_counts = []
        for a in [0, 1]:
            for b in [0, 1]:
                for c in [0, 1]:
                    count = 0
                    for i in range(m - 2):
                        if noise[i] == a and noise[i+1] == b and noise[i+2] == c:
                            count += 1
                    triple_counts.append(count)
        total = sum(triple_counts)
        if total > 0:
            expected = total / 8.0
            chi2 = sum((obs - expected)**2 / expected for obs in triple_counts if expected > 0)
            results['triple_chi2'] = chi2
    
    return results

def compare_to_random(n, m, p, num_trials=10):
    """Compare sponge noise to true random noise on statistical tests."""
    print(f"\n{'='*70}")
    print(f"Advanced Statistical Tests: n={n}, m={m}, p={p}")
    print(f"{'='*70}\n")
    
    sponge_stats = []
    random_stats = []
    
    for trial in range(num_trials):
        seed_val = trial + 7000
        sponge = sponge_noise(n, m, p, seed_val)
        sponge_results = test_higher_order_stats(sponge)
        sponge_stats.append(sponge_results)
        
        np.random.seed(trial + 8000)
        random_noise = (np.random.random(m) < p).astype(np.uint8)
        random_results = test_higher_order_stats(random_noise)
        random_stats.append(random_results)
    
    keys = sorted(sponge_stats[0].keys())
    
    print(f"{'Metric':<25} {'Sponge (mean±std)':<25} {'Random (mean±std)':<25} {'Diff (z-score)':<15}")
    print("-" * 90)
    
    significant_diffs = 0
    for key in keys:
        sponge_vals = [s[key] for s in sponge_stats]
        random_vals = [r[key] for r in random_stats]
        
        sponge_mean = np.mean(sponge_vals)
        sponge_std = np.std(sponge_vals)
        random_mean = np.mean(random_vals)
        random_std = np.std(random_vals)
        
        pooled_std = np.sqrt((sponge_std**2 + random_std**2) / 2) if len(sponge_vals) > 1 else 1.0
        z_score = abs(sponge_mean - random_mean) / pooled_std if pooled_std > 0 else 0
        
        flag = "⚠️" if z_score > 2.0 else "✓"
        if z_score > 2.0:
            significant_diffs += 1
        
        print(f"{key:<25} {sponge_mean:.4f}±{sponge_std:.4f}     {random_mean:.4f}±{random_std:.4f}     {z_score:.2f} {flag}")
    
    print(f"\n{'='*70}")
    print("Assessment")
    print(f"{'='*70}")
    print(f"Significant differences (z > 2.0): {significant_diffs}/{len(keys)}")
    
    if significant_diffs == 0:
        print("✓ PASS: Sponge noise is statistically indistinguishable from random")
        return True
    elif significant_diffs <= 1:
        print("⚠️ MARGINAL: Minor statistical deviation detected")
        return None
    else:
        print(f"⚠️ FAIL: {significant_diffs} statistical deviations detected")
        return False

def test_distinguisher(n, m, p, num_trials=50):
    """Test if a simple ML-style distinguisher can separate sponge from random."""
    print(f"\n{'='*70}")
    print(f"Distinguisher Test: n={n}, m={m}, p={p}")
    print(f"{'='*70}\n")
    
    features_sponge = []
    features_random = []
    
    for trial in range(num_trials):
        seed_val = trial + 9000
        sponge = sponge_noise(n, m, p, seed_val)
        stats_sponge = test_higher_order_stats(sponge)
        features_sponge.append(list(stats_sponge.values()))
        
        np.random.seed(trial + 10000)
        random_noise = (np.random.random(m) < p).astype(np.uint8)
        stats_random = test_higher_order_stats(random_noise)
        features_random.append(list(stats_random.values()))
    
    train_size = num_trials // 2
    
    X_train = np.array(features_sponge[:train_size] + features_random[:train_size])
    y_train = np.array([1] * train_size + [0] * train_size)
    X_test = np.array(features_sponge[train_size:] + features_random[train_size:])
    y_test = np.array([1] * (num_trials - train_size) + [0] * (num_trials - train_size))
    
    mean = np.mean(X_train, axis=0)
    std = np.std(X_train, axis=0)
    std[std == 0] = 1
    X_train_norm = (X_train - mean) / std
    X_test_norm = (X_test - mean) / std
    
    correlations = []
    for i in range(X_train_norm.shape[1]):
        corr = np.corrcoef(X_train_norm[:, i], y_train)[0, 1]
        if not np.isnan(corr):
            correlations.append((abs(corr), i, corr))
    
    correlations.sort(reverse=True)
    top_k = min(5, len(correlations))
    
    correct = 0
    for i in range(len(X_test_norm)):
        score = 0
        for _, feat_idx, full_corr in correlations[:top_k]:
            score += X_test_norm[i, feat_idx] * np.sign(full_corr)
        
        predicted = 1 if score > 0 else 0
        if predicted == y_test[i]:
            correct += 1
    
    accuracy = correct / len(X_test_norm)
    baseline = 0.5
    
    print(f"Distinguisher accuracy: {accuracy:.2%} (baseline: {baseline:.2%})")
    
    if accuracy > 0.6:
        print(f"⚠️ FAIL: Distinguisher achieves {accuracy:.2%} — structure detectable")
        return False
    elif accuracy > 0.55:
        print(f"⚠️ MARGINAL: Slight advantage over random")
        return None
    else:
        print(f"✓ PASS: No significant distinguishability")
        return True

def main():
    print("="*70)
    print("Experiment 26c: Advanced Decoder Attack on Sponge Noise")
    print("K2 final screen — can sophisticated attacks detect structure?")
    print("="*70)
    
    results = []
    for n in [4, 5]:
        m = n ** 3
        p = 0.10
        result = compare_to_random(n, m, p, num_trials=10)
        results.append((n, "stats", result))
    
    for n in [4, 5]:
        m = n ** 3
        p = 0.10
        result = test_distinguisher(n, m, p, num_trials=50)
        results.append((n, "distinguisher", result))
    
    print(f"\n{'='*70}")
    print("Summary")
    print(f"{'='*70}")
    
    for n, test_type, result in results:
        status = "PASS" if result == True else "FAIL" if result == False else "MARGINAL"
        print(f"  n={n}, {test_type}: {status}")
    
    all_pass = all(r == True for _, _, r in results)
    any_fail = any(r == False for _, _, r in results)
    
    print(f"\n{'='*70}")
    print("K2 Exotic Noise Final Verdict")
    print(f"{'='*70}")
    
    if all_pass:
        print("✓ SPONGE CONSTRUCTION: SURVIVES advanced statistical tests")
        print("  → K2 remains OPEN for further investigation")
    elif any_fail:
        print("⚠️ SPONGE CONSTRUCTION: DETECTED by advanced tests")
        print("  → K2 exotic noise route requires redesign")
    else:
        print("⚠️ SPONGE CONSTRUCTION: MARGINAL results")
        print("  → Needs more testing at larger scale")
    
    print("="*70)

if __name__ == '__main__':
    main()
