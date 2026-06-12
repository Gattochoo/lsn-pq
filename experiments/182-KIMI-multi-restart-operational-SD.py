#!/usr/bin/env python3
"""182: Multi-restart operational SD search for (C,z) vs LPN.

Runs several independent SA restarts for a given m and reports the best SD.
Useful for both small-m robustness checks and m>2n scaling.

Usage: python3 experiments/182-KIMI-multi-restart-operational-SD.py <m> <restarts> <iters_per_restart>

Example: python3 experiments/182-KIMI-multi-restart-operational-SD.py 5 3 500000
"""
import random
import sys
import time
import json
from pathlib import Path

# Import machinery from 181
import importlib.util
spec = importlib.util.spec_from_file_location("sd181", "experiments/181-KIMI-operational-distinguishing-SD-search.py")
sd181 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sd181)


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 experiments/182-KIMI-multi-restart-operational-SD.py <m> <restarts> <iters_per_restart>")
        sys.exit(1)

    m = int(sys.argv[1])
    num_restarts = int(sys.argv[2])
    iters = int(sys.argv[3])

    n = 2
    N = 2 * n
    e_probs = {
        e: (1 / 4) ** sd181.popcount(e) * (3 / 4) ** (N - sd181.popcount(e))
        for e in range(1 << N)
    }

    print(f"n={n}, m={m}: Enumerating A matrices...")
    A_list = sd181.enumerate_all_A(n)
    print(f"  |A| = {len(A_list)}")

    # baseline random g
    state_rand = sd181.State(n, m, A_list, e_probs)
    state_rand.init_random(random.Random(42))
    sd_rand = state_rand.compute_SD()
    print(f"Random g baseline: SD={sd_rand:.6f}")

    results = []
    best_overall = None

    for r in range(num_restarts):
        seed = 1000 + r * 137
        print(f"\n{'='*60}")
        print(f"Restart {r+1}/{num_restarts}, seed={seed}")
        state = sd181.State(n, m, A_list, e_probs)
        it_mu = sd181.search_marginal_uniform(state, max_iters=2_000_000, seed=seed)
        print(
            f"  Marginal-uniform search done ({it_mu} iters), "
            f"SD={state.compute_SD():.6f}, marg={state.marginal_cost()}"
        )
        best_sd, best_marg, best_E = sd181.simulated_annealing(
            state, iters, 10.0, 0.05, 1e-5, seed=seed + 1
        )
        print(f"  Restart result: SD={best_sd:.6f}, marg={best_marg}")
        results.append({
            "restart": r,
            "seed": seed,
            "best_SD": best_sd,
            "best_marg": best_marg,
        })
        if best_overall is None or best_sd < best_overall["best_SD"]:
            best_overall = {
                "restart": r,
                "best_SD": best_sd,
                "best_marg": best_marg,
            }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"m={m}: random SD={sd_rand:.6f}")
    for r in results:
        print(f"  restart {r['restart']}: SD={r['best_SD']:.6f}, marg={r['best_marg']}")
    print(f"BEST: SD={best_overall['best_SD']:.6f} (restart {best_overall['restart']})")

    out_dir = Path("experiments/output")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"182-multi-restart-m{m}-SD.json"
    with open(out_file, "w") as f:
        json.dump({
            "n": n,
            "m": m,
            "restarts": num_restarts,
            "iters_per_restart": iters,
            "random_SD": sd_rand,
            "results": results,
            "best_overall": best_overall,
        }, f, indent=2)
    print(f"\nResults saved to {out_file}")


if __name__ == "__main__":
    main()
