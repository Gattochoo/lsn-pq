#!/usr/bin/env python3
"""186: Verify deterministic adaptive B lower bound for lem:m2.

Theorem: for deterministic B=g(A), SD((C,y), LPN) >= 1 - |Lagr(2n,F2)| / 2^{mn}.
For n=2 this is 1 - 15 / 4^m.
"""
import json
from fractions import Fraction
from pathlib import Path

from experiments.lib.lem_m2_exact import num_lagrangian_subspaces


def main():
    n = 2
    num_lag = num_lagrangian_subspaces(n)

    results = {
        "n": n,
        "num_lagrangian": num_lag,
        "theorem": "SD((C,y), LPN) >= 1 - |Lagr| / 2^{mn} for deterministic B=g(A)",
        "bounds": [],
    }

    for m in range(2, 7):
        C_space_size = 1 << (m * n)
        bound = Fraction(C_space_size - num_lag, C_space_size)
        entry = {
            "m": m,
            "C_space_size": C_space_size,
            "lower_bound": str(bound),
            "lower_bound_float": float(bound),
        }

        json_path = Path("experiments/output") / f"185-lem-m2-n2-full-joint-SD-m{m}.json"
        if json_path.exists():
            data = json.loads(json_path.read_text())
            entry["exp185_min_sd"] = data.get("min_sd")
            entry["matches_bound"] = (data.get("min_sd") == str(bound))

        results["bounds"].append(entry)

    out_path = Path("experiments/output") / "186-lem-m2-deterministic-adaptive-bound.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
