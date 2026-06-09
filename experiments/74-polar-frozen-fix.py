#!/usr/bin/env python3
"""Fix Bhattacharyya parameter indexing for komm's natural-order polar code."""
import json
import numpy as np
import komm


def build_frozen_natural(N, K, p):
    """Build frozen set using natural-order Bhattacharyya parameters.

    komm.PolarCode uses non-bit-reversed (natural-order) polar codes.
    The recursive step for natural order interleaves bad and good channels:
        z_new[2*i]   = 2*z[i] - z[i]**2   (bad channel)
        z_new[2*i+1] = z[i]**2            (good channel)
    """
    mu = int(np.log2(N))
    z0 = 2 * np.sqrt(p * (1 - p))
    z = np.array([z0])
    for _ in range(mu):
        z_new = np.empty(2 * len(z))
        z_new[0::2] = 2 * z - z ** 2
        z_new[1::2] = z ** 2
        z = z_new
    frozen = np.argsort(z)[K:].tolist()
    return frozen


def build_frozen_concat(N, K, p):
    """Original buggy construction (concatenates all bad then all good)."""
    mu = int(np.log2(N))
    z0 = 2 * np.sqrt(p * (1 - p))
    z = np.array([z0])
    for _ in range(mu):
        z = np.concatenate([2 * z - z ** 2, z ** 2])
    frozen = np.argsort(z)[K:].tolist()
    return frozen


def simulate(N, K, p, num_trials, frozen_builder, seed=42):
    np.random.seed(seed)
    mu = int(np.log2(N))
    frozen = frozen_builder(N, K, p)
    code = komm.PolarCode(mu, frozen)
    decoder = komm.SCDecoder(code, output_type='hard')

    errors = 0
    for t in range(num_trials):
        msg = np.random.randint(0, 2, K)
        x = code.encode(msg)
        noise = (np.random.random(N) < p).astype(int)
        y = (x + noise) % 2
        llr = np.where(y == 0, np.log((1 - p) / p), np.log(p / (1 - p)))
        u_hat = decoder.decode(llr)
        if not np.array_equal(msg, u_hat):
            errors += 1
    return errors / num_trials


def main():
    results = {}
    configs = [
        (128, 16, 0.0706, 200),
        (128, 16, 0.0343, 200),
        (256, 32, 0.0706, 200),
        (256, 32, 0.0343, 200),
        (512, 64, 0.0706, 200),
        (512, 64, 0.0343, 200),
    ]

    for N, K, p, trials in configs:
        key = f"N={N},K={K},p={p}"
        print(f"\n=== {key} ===")
        bler_concat = simulate(N, K, p, trials, build_frozen_concat)
        bler_natural = simulate(N, K, p, trials, build_frozen_natural)
        print(f"  concat:    BLER = {bler_concat:.4f}")
        print(f"  natural:   BLER = {bler_natural:.4f}")
        results[key] = {
            "concat": bler_concat,
            "natural": bler_natural,
            "trials": trials,
        }

    out = "/Users/gatto/projects/TRIARC-main/.claude/worktrees/hardness-7th-shared/lsn-experiments/74-polar-frozen-fix-results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out}")


if __name__ == "__main__":
    main()
