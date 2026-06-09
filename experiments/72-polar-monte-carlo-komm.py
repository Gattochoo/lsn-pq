#!/usr/bin/env python3
"""
R2b: Polar Monte-Carlo using komm (verified SC decoder).
Validate concatenated code BLER against Bhattacharyya design point.
"""

import numpy as np
import math
import json
import sys
sys.path.insert(0, '/Users/gatto/projects/TRIARC-main/.claude/worktrees/hardness-7th-shared/lsn-experiments/venv/lib/python3.13/site-packages')

import komm

def build_frozen_set(N, K, p):
    """Select N-K worst channels (largest Z) as frozen.

    komm.PolarCode uses non-bit-reversed (natural-order) polar codes.
    The Bhattacharyya parameters must be computed in natural order:
        z_new[2*i]   = 2*z[i] - z[i]**2   (bad channel)
        z_new[2*i+1] = z[i]**2            (good channel)
    """
    mu = int(np.log2(N))
    z0 = 2 * math.sqrt(p * (1 - p))
    z = np.array([z0])
    for _ in range(mu):
        z_new = np.empty(2 * len(z))
        z_new[0::2] = 2 * z - z ** 2
        z_new[1::2] = z ** 2
        z = z_new
    # Frozen = channels with largest Z
    frozen = np.argsort(z)[K:].tolist()
    return frozen

def simulate_sc(N, K, p, num_trials=200):
    mu = int(np.log2(N))
    frozen = build_frozen_set(N, K, p)
    info_set = [i for i in range(N) if i not in frozen]
    
    code = komm.PolarCode(mu, frozen)
    decoder = komm.SCDecoder(code, output_type='hard')
    
    llr0 = math.log((1 - p) / p)
    llr1 = math.log(p / (1 - p))
    
    errors = 0
    for trial in range(num_trials):
        msg = np.random.randint(0, 2, K)
        x = code.encode(msg)
        # BSC(p) channel
        noise = (np.random.random(N) < p).astype(int)
        y = x ^ noise
        llr = np.where(y == 0, llr0, llr1).astype(float)
        u_hat = decoder.decode(llr)
        if not np.array_equal(msg, u_hat):
            errors += 1
        if (trial + 1) % 50 == 0:
            print(f"    N={N}, trial {trial+1}/{num_trials}, BLER={errors/(trial+1):.4f}")
    
    return errors / num_trials

def main():
    results = {}
    
    # Test parameters: concatenated code effective noise
    test_cases = [
        # (N, K, p_eff, label)
        (128, 16, 0.0706, "N=128,K=16,p'=0.0706"),
        (256, 32, 0.0706, "N=256,K=32,p'=0.0706"),
        (512, 64, 0.0706, "N=512,K=64,p'=0.0706"),
        (128, 16, 0.0343, "N=128,K=16,p'=0.0343"),
        (256, 32, 0.0343, "N=256,K=32,p'=0.0343"),
        (512, 64, 0.0343, "N=512,K=64,p'=0.0343"),
    ]
    
    for N, K, p, label in test_cases:
        print(f"\n=== {label} ===")
        bler = simulate_sc(N, K, p, num_trials=200)
        print(f"  Final BLER = {bler:.4f} ({bler:.2e})")
        results[label] = {
            "N": N, "K": K, "p": p,
            "BLER": bler,
            "num_trials": 200
        }
    
    out = "/Users/gatto/projects/TRIARC-main/.claude/worktrees/hardness-7th-shared/lsn-experiments/72-polar-monte-carlo-results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out}")

if __name__ == "__main__":
    main()
