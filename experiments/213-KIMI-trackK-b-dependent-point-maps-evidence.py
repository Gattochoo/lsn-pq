#!/usr/bin/env python3
"""213 (Track K, stretch): b-dependent point maps — empirical evidence.

K3. Scope definition (EVIDENCE/OPEN).
    A b-dependent point map is a public bijection

        g_i : F_2^{2n} x F_2 -> F_2^{2n} x F_2,
        g_i(x,b) = (phi_{i,b}(x), b ⊕ psi_i(x,b)),

    where for each label bit b, phi_{i,b} is a public bijection of F_2^{2n}
    and psi_i: F_2^{2n} x F_2 -> F_2 is a public label-flip function.  The
    split map sends one sample (x,b) to the pair (g_0(x,b), g_1(x,b)).

    This family strictly generalises the label-flipping family of experiment
    212 (which is the special case phi_{i,b}=f_i independent of b and
    psi_i(x,b)=h_i(x)).  Because the x-coordinate now depends on the secret
    label bit b, the outputs are not independent LSN samples conditioned on a
    single public Lagrangian, so the exact SD formula of K2 does not apply
    without further structural analysis.

    This script enumerates random instances at n = 2 exactly and checks that
    the universal minimum

        SD_min = 1 - (p^2 + (1-p)^2) / 4^n

    is still a lower bound for every tested instance.  Persistence of the
    bound for all b-dependent bijections remains a conjecture (EVIDENCE).

Guards:
  L1 exact arithmetic: Fractions/integer counts; JSON stores string fractions.
  L2 duality care: not invoked.
  L3 query-class hygiene: no SQ/Feldman inference.
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


def all_lagrangians(n: int) -> list[set[int]]:
    bases = enumerate_lagrangian_bases_n(n)
    subs = []
    for basis in bases:
        span = [0]
        for v in basis:
            span += [s ^ v for s in span]
        subs.append(set(span))
    return subs


def random_bijection(size: int, rng: random.Random) -> list[int]:
    perm = list(range(size))
    rng.shuffle(perm)
    return perm


def random_function_domain_b(size: int, rng: random.Random) -> list[list[int]]:
    """Return two functions F_2^{2n} x F_2 -> F_2, indexed by [b][x]."""
    return [[rng.randint(0, 1) for _ in range(size)] for _ in range(2)]


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
    N = 2 * n
    size = 1 << N
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
                key = (x0 << (N + 2)) | (b0 << (N + 1)) | (x1 << 1) | b1
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
                        key = (u1 << (N + 2)) | (b1 << (N + 1)) | (u2 << 1) | b2
                        counts_Q[key] = counts_Q.get(key, 0) + w1 * w2

    num = 0
    keys = set(counts_P.keys()) | set(counts_Q.keys())
    for k in keys:
        num += abs(counts_P.get(k, 0) * D_Q - counts_Q.get(k, 0) * D_P)
    return Fraction(num, 2 * D_P * D_Q)


def build_instances(n: int, rng: random.Random, count: int = 10) -> list[dict]:
    size = 1 << (2 * n)
    instances = []
    for idx in range(count):
        phi0 = [random_bijection(size, rng), random_bijection(size, rng)]
        phi1 = [random_bijection(size, rng), random_bijection(size, rng)]
        psi0 = random_function_domain_b(size, rng)
        psi1 = random_function_domain_b(size, rng)
        instances.append({
            "name": f"bdep_{idx}",
            "phi0": phi0,
            "phi1": phi1,
            "psi0": psi0,
            "psi1": psi1,
        })
    return instances


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--seed", type=int, default=20260614)
    p.add_argument("--instances", type=int, default=10)
    return p.parse_args()


def main():
    args = parse_args()
    p = P_NOISE
    rng = random.Random(args.seed)
    n = 2
    lags = all_lagrangians(n)
    orbit_min = universal_minimum(n, p)
    print(f"Track K3 (stretch): b-dependent point maps, n={n}; orbit minimum = {orbit_min}\n")

    instances = build_instances(n, rng, args.instances)
    results = []
    all_ge = True
    any_equal = False
    for inst in instances:
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
        results.append({
            "name": inst["name"],
            "sd": str(sd),
            "meets_universal_bound": ge,
            "equals_orbit_minimum": eq,
        })
        print(f"  {inst['name']}: SD = {sd}, ge_min={ge}, eq_min={eq}")
    assert all_ge, "universal minimum was violated by a random b-dependent instance"
    print("\n=> Evidence: universal minimum holds for all tested b-dependent instances")
    if not any_equal:
        print("   No tested instance attains the minimum (consistent with non-duplicate maps)")

    result = {
        "track": "K",
        "experiment": 213,
        "noise_rate_p": str(p),
        "claim": {
            "statement": "For b-dependent public bijections g_i(x,b) = (phi_{i,b}(x), b⊕psi_i(x,b)), the universal minimum 1-(p^2+(1-p)^2)/4^n appears to remain a lower bound at n=2",
            "status": "EVIDENCE / OPEN",
            "label": "EVIDENCE",
        },
        "verification_n2": {
            "num_instances": len(results),
            "instances": results,
            "all_meet_bound": all_ge,
            "any_equal_to_minimum": any_equal,
            "label": "EVIDENCE",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction and integer counts; JSON stores string fractions",
            "L2_duality_care": "not invoked",
            "L3_query_class_hygiene": "TV-only; no Feldman/SQ inference",
            "L4_never_transform_comparison_distribution": "fresh pair remains natural; g_i act only on split side",
        },
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from the SAME uniform secret L",
            "family": "b-dependent point-map split g_i(x,b) = (phi_{i,b}(x), b⊕psi_i(x,b))",
            "PRE_REGISTERED": "conjectural persistence of the universal minimum; not a theorem and not a rate/attack claim",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "213-trackK-b-dependent-point-maps-evidence.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
