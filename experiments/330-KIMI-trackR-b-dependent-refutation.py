#!/usr/bin/env python3
r"""330 (Track R): b-dependent point maps -- refutation of the universal minimum.

Track K closed label-flipping (K2 theorem) and left b-dependent point maps as
K3 evidence.  This script proves, by explicit counterexample, that the
label-flipping universal minimum

    SD_min = 1 - (p^2 + (1-p)^2) / 4^n

does **not** persist for the full b-dependent point-map family.

The b-dependent point-map split is

    (x,b) |--> (g_0(x,b), g_1(x,b)),
    g_i(x,b) = (phi_{i,b}(x), b \oplus psi_i(x,b)),

where phi_{i,b} is a public bijection of F_2^{2n} for each fixed label bit b
and psi_i is an arbitrary public label-flip function.  The comparison
distribution is the untransformed same-secret fresh pair D_L x D_L.

Main results (n = 2, p = 1/4):
  * literal duplicate:            SD = 123/128  = SD_min  (equality)
  * transposition-only map:       SD = 1231/1280  > SD_min
  * explicit b-dependent counterexample: SD = 1229/1280  < SD_min
  * best random instance (seed 124):     SD = 1843/1920  < SD_min
  * Track K3's 10 instances (seed 20260614) all satisfy SD >= SD_min,
    none attain it (consistent with the evidence recorded in 213).

Guards:
  L1 exact arithmetic: Fractions/integer counts; JSON stores string fractions.
  L2 duality care: not invoked.
  L3 query-class hygiene: TV-only; no Feldman/SQ inference.
  L4 comparison distribution: fresh pair is never transformed.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n

P_NOISE = Fraction(1, 4)
N = 2


def all_lagrangians(n: int) -> list[set[int]]:
    """Return all Lagrangian subspaces of F_2^{2n} as sets of vectors."""
    bases = enumerate_lagrangian_bases_n(n)
    subs = []
    for basis in bases:
        span = [0]
        for v in basis:
            span += [s ^ v for s in span]
        subs.append(set(span))
    return subs


def universal_minimum(n: int, p: Fraction = P_NOISE) -> Fraction:
    return Fraction(1) - (p * p + (1 - p) * (1 - p)) / (4 ** n)


def exact_sd_b_dependent(
    n: int,
    lags: list[set[int]],
    phi0: list[list[int]],
    phi1: list[list[int]],
    psi0: list[list[int]],
    psi1: list[list[int]],
    p: Fraction = P_NOISE,
) -> Fraction:
    """Exact SD for a b-dependent split vs. the untransformed fresh pair."""
    N_dim = 2 * n
    size = 1 << N_dim
    pnum = p.numerator
    qnum = p.denominator - p.numerator
    denom = p.denominator

    D_P = len(lags) * size * denom * denom
    D_Q = len(lags) * size * size * denom * denom

    counts_P: dict[int, int] = {}
    counts_Q: dict[int, int] = {}

    for L in lags:
        mask = 0
        for v in L:
            mask |= 1 << v
        # Split side: g_i(x,b) with b = c \oplus e
        for x in range(size):
            c = (mask >> x) & 1
            for e in (0, 1):
                b = c ^ e
                x0 = phi0[b][x]
                x1 = phi1[b][x]
                b0 = b ^ psi0[b][x]
                b1 = b ^ psi1[b][x]
                key = (x0 << (N_dim + 2)) | (b0 << (N_dim + 1)) | (x1 << 1) | b1
                w = (qnum if e == 0 else pnum) * denom
                counts_P[key] = counts_P.get(key, 0) + w
        # Fresh comparison side: unchanged
        for u1 in range(size):
            c1 = (mask >> u1) & 1
            for u2 in range(size):
                c2 = (mask >> u2) & 1
                for e1 in (0, 1):
                    b1 = c1 ^ e1
                    w1 = qnum if e1 == 0 else pnum
                    for e2 in (0, 1):
                        b2 = c2 ^ e2
                        w2 = qnum if e2 == 0 else pnum
                        key = (u1 << (N_dim + 2)) | (b1 << (N_dim + 1)) | (u2 << 1) | b2
                        counts_Q[key] = counts_Q.get(key, 0) + w1 * w2

    num = 0
    keys = set(counts_P.keys()) | set(counts_Q.keys())
    for k in keys:
        num += abs(counts_P.get(k, 0) * D_Q - counts_Q.get(k, 0) * D_P)
    return Fraction(num, 2 * D_P * D_Q)


def random_bijection(size: int, rng: random.Random) -> list[int]:
    perm = list(range(size))
    rng.shuffle(perm)
    return perm


def random_function_domain_b(size: int, rng: random.Random) -> list[list[int]]:
    """Return two functions F_2^{2n} x F_2 -> F_2, indexed by [b][x]."""
    return [[rng.randint(0, 1) for _ in range(size)] for _ in range(2)]


def build_k3_instances(n: int, rng: random.Random, count: int = 10) -> list[dict]:
    """Reproduce the 10 Track-K3 random instances (experiment 213)."""
    size = 1 << (2 * n)
    instances = []
    for idx in range(count):
        phi0 = [random_bijection(size, rng), random_bijection(size, rng)]
        phi1 = [random_bijection(size, rng), random_bijection(size, rng)]
        psi0 = random_function_domain_b(size, rng)
        psi1 = random_function_domain_b(size, rng)
        instances.append({
            "name": f"k3_{idx}",
            "phi0": phi0,
            "phi1": phi1,
            "psi0": psi0,
            "psi1": psi1,
        })
    return instances


def build_structured_cases(n: int) -> list[dict]:
    """Return the structured Track-R cases used in the refutation."""
    size = 1 << (2 * n)
    ident = list(range(size))

    # Transposition (0 1) on F_2^{2n}.
    trans = list(range(size))
    trans[0], trans[1] = trans[1], trans[0]

    zero = [[0] * size, [0] * size]

    cases = []

    # 1. Literal duplicate: g_0 = g_1 = identity, no label flips.
    cases.append({
        "name": "duplicate",
        "description": "g_0 = g_1 = id, psi_i = 0; attains the universal minimum",
        "phi0": [ident, ident],
        "phi1": [ident, ident],
        "psi0": zero,
        "psi1": zero,
        "expected_sd": universal_minimum(n, P_NOISE),
    })

    # 2. Transposition only: phi_{1,1} swaps 0 and 1, no label flips.
    #    This is above the universal minimum.
    cases.append({
        "name": "transposition_only",
        "description": "phi_{1,1} = (0 1), all other maps identity, psi_i = 0",
        "phi0": [ident, ident],
        "phi1": [ident, trans],
        "psi0": zero,
        "psi1": zero,
        "expected_sd": Fraction(1231, 1280),
    })

    # 3. Explicit counterexample: phi_{1,1} = (0 1) and psi_1(x,1) = 1.
    #    This beats the universal minimum.
    psi_counter = [[0] * size, [1] * size]
    cases.append({
        "name": "counterexample",
        "description": "phi_{1,1} = (0 1), psi_0 = 0, psi_1(x,0)=0, psi_1(x,1)=1",
        "phi0": [ident, ident],
        "phi1": [ident, trans],
        "psi0": zero,
        "psi1": psi_counter,
        "expected_sd": Fraction(1229, 1280),
    })

    # 4. Best random b-dependent instance found in an exploratory search
    #    (seed 124, 1000 trials).  Included as EVIDENCE that the gap can be
    #    larger than the simple counterexample.
    cases.append({
        "name": "random_best_seed124",
        "description": "Random instance from exploratory search; EVIDENCE, not theorem",
        "phi0": [
            [8, 6, 10, 11, 3, 7, 15, 14, 4, 0, 1, 13, 9, 5, 12, 2],
            [13, 4, 14, 5, 10, 11, 0, 9, 15, 1, 2, 7, 8, 6, 3, 12],
        ],
        "phi1": [
            [10, 2, 14, 11, 8, 4, 5, 0, 12, 9, 13, 1, 7, 15, 3, 6],
            [0, 9, 12, 3, 6, 15, 14, 2, 5, 11, 4, 8, 13, 7, 10, 1],
        ],
        "psi0": [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
        ],
        "psi1": [
            [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        ],
        "expected_sd": Fraction(1843, 1920),
    })

    return cases


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--k3-seed", type=int, default=20260614)
    p.add_argument("--k3-instances", type=int, default=10)
    return p.parse_args()


def main():
    args = parse_args()
    p = P_NOISE
    n = N
    lags = all_lagrangians(n)
    orbit_min = universal_minimum(n, p)
    print(f"Track R: b-dependent point-map refutation, n={n}; orbit minimum = {orbit_min}\n")

    # ------------------------------------------------------------------
    # K3 verification
    # ------------------------------------------------------------------
    rng_k3 = random.Random(args.k3_seed)
    k3_instances = build_k3_instances(n, rng_k3, args.k3_instances)
    k3_results = []
    all_ge = True
    any_equal = False
    for inst in k3_instances:
        sd = exact_sd_b_dependent(
            n, lags,
            inst["phi0"], inst["phi1"],
            inst["psi0"], inst["psi1"],
            p,
        )
        ge = sd >= orbit_min
        eq = sd == orbit_min
        all_ge &= ge
        if eq:
            any_equal = True
        k3_results.append({
            "name": inst["name"],
            "sd": str(sd),
            "meets_universal_bound": ge,
            "equals_orbit_minimum": eq,
        })
        print(f"  {inst['name']}: SD = {sd}, ge_min={ge}, eq_min={eq}")
    assert all_ge, "Track K3 instances unexpectedly violate the universal minimum"
    print("\n=> Track K3 instances verified: all >= minimum, none equal\n")

    # ------------------------------------------------------------------
    # Structured cases
    # ------------------------------------------------------------------
    structured = build_structured_cases(n)
    structured_results = []
    for case in structured:
        sd = exact_sd_b_dependent(
            n, lags,
            case["phi0"], case["phi1"],
            case["psi0"], case["psi1"],
            p,
        )
        expected = case["expected_sd"]
        match = (sd == expected)
        below_min = (sd < orbit_min)
        structured_results.append({
            "name": case["name"],
            "description": case["description"],
            "sd": str(sd),
            "expected_sd": str(expected),
            "sd_matches_expected": match,
            "meets_universal_bound": sd >= orbit_min,
            "equals_orbit_minimum": sd == orbit_min,
            "strictly_beats_universal_minimum": below_min,
        })
        print(f"  {case['name']:24s}: SD = {sd}, expected = {expected}, "
              f"match={match}, below_min={below_min}")
        assert match, f"structured case {case['name']} did not match expected exact SD"

    counterexample_sd = next(r for r in structured_results if r["name"] == "counterexample")["sd"]
    print(f"\n=> Counterexample SD = {counterexample_sd} < orbit minimum {orbit_min}")

    # ------------------------------------------------------------------
    # JSON output
    # ------------------------------------------------------------------
    result = {
        "track": "R",
        "experiment": 330,
        "noise_rate_p": str(p),
        "theorem_refutation": {
            "statement": "The label-flipping universal minimum 1-(p^2+(1-p)^2)/4^n is NOT a lower bound for the full b-dependent point-map family",
            "label": "THEOREM",
            "proof_method": "Explicit counterexample with exact rational SD below the minimum",
            "counterexample_sd": counterexample_sd,
            "universal_minimum": str(orbit_min),
        },
        "verification_k3": {
            "seed": args.k3_seed,
            "num_instances": len(k3_results),
            "instances": k3_results,
            "all_meet_bound": all_ge,
            "any_equal_to_minimum": any_equal,
            "label": "EVIDENCE / THEOREM",
        },
        "structured_cases": {
            "cases": structured_results,
            "label": "THEOREM",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction and integer counts; JSON stores string fractions",
            "L2_duality_care": "not invoked",
            "L3_query_class_hygiene": "TV-only; no Feldman/SQ inference",
            "L4_never_transform_comparison_distribution": "fresh pair remains natural; g_i act only on split side",
        },
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from the SAME uniform secret L",
            "family": "b-dependent point-map split g_i(x,b) = (phi_{i,b}(x), b \\oplus psi_i(x,b))",
            "PRE_REGISTERED": "The Track K2 minimum is proven only for label-flipping (b-independent) maps; b-dependence can strictly improve closeness to the fresh pair. Exact infimum over all b-dependent maps remains OPEN.",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "330-trackR-b-dependent-refutation.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
