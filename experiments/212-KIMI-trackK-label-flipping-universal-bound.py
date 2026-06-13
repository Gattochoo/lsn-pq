#!/usr/bin/env python3
"""212 (Track K): universal bound for label-flipping splits.

K2. THEOREM (label-flipping family).
    For public bijections f_1,f_2 of F_2^{2n} and public label-flip functions
    h_1,h_2: F_2^{2n} -> F_2, consider the split

        (x,b) |--> ((f_1(x), b ⊕ h_1(x)), (f_2(x), b ⊕ h_2(x))).

    Under the natural same-secret comparison to two independent fresh samples
    from D_L, the exact statistical distance is

        SD = 1 - 4^{-n} [ 2 p(1-p) + (1-2p)^2 A' ],
        A' = Pr_{L,x}[ 1_L(f_1 x) ⊕ 1_L(f_2 x) = h_1(x) ⊕ h_2(x) ].

    Moreover A' = 1 if and only if f_1 = f_2 and h_1 = h_2 (the literal
    duplicate).  Consequently the label-preserving universal minimum

        SD_min = 1 - (p^2 + (1-p)^2) / 4^n

    is a universal lower bound for the entire label-flipping family, with
    equality only for the literal duplicate.

K2 verification: exact enumeration at n = 2 for several (f_1,f_2,h_1,h_2)
    instances, including duplicates, equal-bijections with flipped labels,
    and independently-random choices.

Guards:
  L1 exact arithmetic: Fractions end-to-end; JSON stores string fractions.
  L2 duality care: not invoked.
  L3 query-class hygiene: TV-only; no SQ/Feldman inference.
  L4 comparison distribution: the fresh pair is never transformed.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n, symplectic_form_n

P_NOISE = Fraction(1, 4)


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


def apply_matrix_cols(cols: tuple[int, ...], x: int) -> int:
    y = 0
    for i, col in enumerate(cols):
        if (x >> i) & 1:
            y ^= col
    return y


def det_f2(cols: tuple[int, ...]) -> int:
    N = len(cols)
    rows = [0] * N
    for j, col in enumerate(cols):
        for i in range(N):
            if (col >> i) & 1:
                rows[i] |= 1 << j
    pivots = {}
    for r in rows:
        x = r
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return 1 if len(pivots) == N else 0


def is_symplectic_matrix(cols: tuple[int, ...], n: int) -> bool:
    N = 2 * n
    basis = [1 << i for i in range(N)]
    for i in range(N):
        for j in range(N):
            if symplectic_form_n(cols[i], cols[j], n) != symplectic_form_n(basis[i], basis[j], n):
                return False
    return True


def enumerate_sp4() -> list[tuple[int, ...]]:
    n = 2
    N = 4
    out = []
    for bits in range(1 << (N * N)):
        cols = []
        for j in range(N):
            col = 0
            for i in range(N):
                if (bits >> (j * N + i)) & 1:
                    col |= 1 << i
            cols.append(col)
        if det_f2(cols) and is_symplectic_matrix(tuple(cols), n):
            out.append(tuple(cols))
    return out


def enumerate_gl(n: int) -> list[tuple[int, ...]]:
    N = n
    out = []
    for bits in range(1 << (N * N)):
        cols = []
        for j in range(N):
            col = 0
            for i in range(N):
                if (bits >> (j * N + i)) & 1:
                    col |= 1 << i
            cols.append(col)
        if det_f2(cols):
            out.append(tuple(cols))
    return out


def random_bijection(size: int, rng: random.Random) -> list[int]:
    perm = list(range(size))
    rng.shuffle(perm)
    return perm


def random_function(size: int, rng: random.Random) -> list[int]:
    return [rng.randint(0, 1) for _ in range(size)]


def universal_minimum(n: int, p: Fraction = P_NOISE) -> Fraction:
    return Fraction(1) - (p * p + (1 - p) * (1 - p)) / (4 ** n)


def agreement_A_prime(
    n: int,
    lags: list[set[int]],
    f1: list[int],
    f2: list[int],
    h1: list[int],
    h2: list[int],
) -> Fraction:
    """A' = Pr_{L,x}[ 1_L(f1x) ⊕ 1_L(f2x) = h1(x) ⊕ h2(x) ]."""
    size = 1 << (2 * n)
    total = 0
    for x in range(size):
        u, v = f1[x], f2[x]
        target = h1[x] ^ h2[x]
        total += sum(1 for L in lags if ((u in L) ^ (v in L)) == target)
    return Fraction(total, len(lags) * size)


def corrected_sd_label_flipping(n: int, Aprime: Fraction, p: Fraction = P_NOISE) -> Fraction:
    return Fraction(1) - Fraction(1, 4 ** n) * (
        2 * p * (1 - p) + (1 - 2 * p) ** 2 * Aprime
    )


def exact_sd_label_flipping(
    n: int,
    lags: list[set[int]],
    f1: list[int],
    f2: list[int],
    h1: list[int],
    h2: list[int],
    p: Fraction = P_NOISE,
) -> Fraction:
    """Exact SD for the label-flipping split vs. the untransformed fresh pair."""
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
        # Split side: labels are flipped by h_i(x)
        for x in range(size):
            c = (mask >> x) & 1
            for e in (0, 1):
                b = c ^ e
                b1 = b ^ h1[x]
                b2 = b ^ h2[x]
                key = (f1[x] << (N + 2)) | (b1 << (N + 1)) | (f2[x] << 1) | b2
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


def build_cases(n: int, rng: random.Random) -> list[dict]:
    """Build 12 representative label-flipping cases for n=2."""
    N = 2 * n
    size = 1 << N
    ident = list(range(size))
    sp = enumerate_sp4()
    gl = enumerate_gl(4)

    zero = [0] * size
    one = [1] * size

    cases = []

    # 1. literal duplicate
    cases.append({"name": "dup_id_00", "f1": ident, "f2": ident, "h1": zero, "h2": zero})

    # 2. duplicate f, flipped constant labels
    cases.append({"name": "dup_id_01", "f1": ident, "f2": ident, "h1": zero, "h2": one})

    # 3. duplicate f, independent random labels
    cases.append({"name": "dup_id_rand", "f1": ident, "f2": ident, "h1": zero, "h2": random_function(size, rng)})

    # 4. duplicate random f, same labels
    r = random_bijection(size, rng)
    cases.append({"name": "dup_rand_00", "f1": r, "f2": r, "h1": zero, "h2": zero})

    # 5. duplicate random f, flipped labels
    cases.append({"name": "dup_rand_01", "f1": r, "f2": r, "h1": zero, "h2": random_function(size, rng)})

    # 6. symplectic pair, no label flip
    T = sp[7]
    f_sp = [apply_matrix_cols(T, x) for x in range(size)]
    cases.append({"name": "sp_00", "f1": ident, "f2": f_sp, "h1": zero, "h2": zero})

    # 7. symplectic pair, with label flip
    cases.append({"name": "sp_h", "f1": ident, "f2": f_sp, "h1": zero, "h2": random_function(size, rng)})

    # 8. affine pair, same labels
    A = gl[5]
    t = rng.randrange(1, size)
    f_aff = [(apply_matrix_cols(A, x) ^ t) for x in range(size)]
    cases.append({"name": "aff_00", "f1": ident, "f2": f_aff, "h1": zero, "h2": zero})

    # 9. affine pair, flipped labels
    cases.append({"name": "aff_h", "f1": ident, "f2": f_aff, "h1": zero, "h2": random_function(size, rng)})

    # 10. random f pair, no label flip
    r2 = random_bijection(size, rng)
    cases.append({"name": "rand_00", "f1": ident, "f2": r2, "h1": zero, "h2": zero})

    # 11. random f pair, both label flips
    cases.append({"name": "rand_hh", "f1": ident, "f2": r2, "h1": random_function(size, rng), "h2": random_function(size, rng)})

    # 12. two independent random bijections + two independent label flips
    cases.append({"name": "rand2_hh", "f1": random_bijection(size, rng), "f2": random_bijection(size, rng),
                  "h1": random_function(size, rng), "h2": random_function(size, rng)})

    return cases


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--seed", type=int, default=20260614)
    return p.parse_args()


def main():
    args = parse_args()
    p = P_NOISE
    rng = random.Random(args.seed)
    n = 2
    lags = all_lagrangians(n)
    orbit_min = universal_minimum(n, p)
    print(f"Track K2: label-flipping family, n={n}; orbit minimum = {orbit_min}\n")

    cases = build_cases(n, rng)
    results = []
    all_ok = True
    for case in cases:
        name = case["name"]
        f1, f2 = case["f1"], case["f2"]
        h1, h2 = case["h1"], case["h2"]
        Aprime = agreement_A_prime(n, lags, f1, f2, h1, h2)
        sd_formula = corrected_sd_label_flipping(n, Aprime, p)
        sd_direct = exact_sd_label_flipping(n, lags, f1, f2, h1, h2, p)
        match = (sd_formula == sd_direct)
        ge = (sd_direct >= orbit_min)
        duplicate = (f1 == f2 and h1 == h2)
        eq_min = (sd_direct == orbit_min)
        ok = match and ge and (eq_min == duplicate)
        all_ok &= ok
        results.append({
            "name": name,
            "sd": str(sd_direct),
            "Aprime": str(Aprime),
            "formula_matches_direct": match,
            "meets_universal_bound": ge,
            "equals_orbit_minimum": eq_min,
            "is_literal_duplicate": duplicate,
        })
        print(f"  {name:16s}: SD = {sd_direct}, A' = {Aprime}, "
              f"match={match}, ge={ge}, dup={duplicate}, eq_min={eq_min}")
    assert all_ok, "label-flipping verification failed"
    print("\n=> K2 theorem verified: universal minimum covers all label-flipping splits, "
          "equality only for literal duplicate")

    result = {
        "track": "K",
        "experiment": 212,
        "noise_rate_p": str(p),
        "theorem_K2": {
            "statement": "SD(split_{f1,f2,h1,h2}(D_L), D_L x D_L) = 1 - 4^{-n}[2p(1-p) + (1-2p)^2 A'], where A' = Pr_{L,x}[1_L(f1x) ⊕ 1_L(f2x) = h1(x) ⊕ h2(x)]",
            "universal_minimum": str(orbit_min),
            "equality_condition": "A' = 1 iff f1 = f2 and h1 = h2 (literal duplicate); otherwise SD > minimum",
            "label": "THEOREM",
        },
        "verification_n2": {
            "num_cases": len(results),
            "cases": results,
            "label": "THEOREM",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON stores string fractions",
            "L2_duality_care": "not invoked",
            "L3_query_class_hygiene": "TV-only; no Feldman/SQ inference",
            "L4_never_transform_comparison_distribution": "fresh pair remains in natural domain; f_i and h_i act only on the split side",
        },
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from the SAME uniform secret L",
            "family": "label-flipping split (x,b) |-> ((f1(x), b⊕h1(x)), (f2(x), b⊕h2(x)))",
            "PRE_REGISTERED": "structural distributional gap; not a rate or attack claim",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "212-trackK-label-flipping-universal-bound.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
