#!/usr/bin/env python3
"""211 (Track G, corrected by Track K): label-preserving obstruction and exact SD.

Track-G question: does the OP7 obstruction extend beyond the symplectic-orbit
family to arbitrary public bijections that preserve the label bit?

G1. THEOREM (closed-form marginal obstruction).  Still valid.
    For the LSN noise rate p and a uniform Lagrangian secret L, let
    (u_1,b_1) and (u_2,b_2) be two independent fresh samples from D_L.  Then

        mu_n := Pr[1_L(u)=1] = 1/2^n,
        q_n  := Pr[b=1]     = p + (1-2p)/2^n,
        Pr_fresh[b_1 != b_2] = 2 q_n (1-q_n).

    For any public bijections f_1,f_2 of F_2^{2n}, the label-preserving split
    (x,b) |--> ((f_1(x),b),(f_2(x),b)) emits a pair whose (b_1,b_2)-marginal is
    supported on {00,11}, whereas the fresh pair puts mass Pr_fresh[b_1!=b_2] on
    {01,10}.  By data processing,

        SD( split_{f1,f2}(D_L) , D_L x D_L )  >=  Pr_fresh[b_1 != b_2].

G3. CLAIM WITHDRAWN / CORRECTED (Track K, L4 repair).
    The original G.3 asserted that the exact same-secret SD is the same for
    every pair of public bijections.  That proof violated guard (L4): it applied
    the verification bijections f_i^{-1} to the FRESH comparison pair too, which
    is only sound if the fresh distribution is invariant under those bijections
    -- it is not.  The corrected same-secret law is

        SD = 1 - 4^{-n} [ 2 p(1-p) + (1-2p)^2 A ],
        A  = Pr_{L,x}[ 1_L(f_1 x) = 1_L(f_2 x) ],

    and the orbit value 1 - (p^2+(1-p)^2)/4^n is the universal MINIMUM, with
    equality iff f_1 = f_2 (i.e. A = 1).  See Track K experiments 212+ for the
    label-flipping extension.

Guards:
  L1 exact arithmetic: Fractions end-to-end; JSON stores string fractions.
  L2 duality care: not invoked (no character sums over Lagrangians).
  L3 query-class hygiene: total-variation/distinguishability only; no SQ claim.
  L4 comparison distribution: the fresh pair (u_1,b_1,u_2,b_2) is NOT
      transformed by f_1,f_2.  Any bijection is applied to the split side only.

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
    """Apply a matrix given as columns to a vector x over F_2."""
    y = 0
    for i, col in enumerate(cols):
        if (x >> i) & 1:
            y ^= col
    return y


def det_f2(cols: tuple[int, ...]) -> int:
    """Determinant (0 or 1) of an N x N matrix over F_2 given as columns."""
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
    """Check that columns form a symplectic matrix w.r.t. the standard form."""
    N = 2 * n
    basis = [1 << i for i in range(N)]
    for i in range(N):
        for j in range(N):
            if symplectic_form_n(cols[i], cols[j], n) != symplectic_form_n(basis[i], basis[j], n):
                return False
    return True


def enumerate_sp4() -> list[tuple[int, ...]]:
    """Brute-force enumerate Sp(4,F_2) (720 elements)."""
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
    """Enumerate all invertible n x n matrices over F_2 as column tuples."""
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
    """Return a random permutation of {0,...,size-1}."""
    perm = list(range(size))
    rng.shuffle(perm)
    return perm


def random_symplectic_perm(n: int, rng: random.Random, steps: int = 80) -> list[int]:
    """Generate a random element of Sp(2n,F_2) as a permutation of F_2^{2n}."""
    size = 1 << (2 * n)
    perm = list(range(size))
    for _ in range(rng.randint(6, 14)):
        v = rng.randrange(1, size)
        perm = [perm[x] ^ (v if symplectic_form_n(perm[x], v, n) else 0)
                for x in range(size)]
    return perm


def pr_b_neq_formula(n: int, p: Fraction = P_NOISE) -> Fraction:
    """Closed form Pr_fresh[b_1 != b_2] (THEOREM G.1)."""
    q = p + Fraction(1 - 2 * p, 2 ** n)
    return 2 * q * (1 - q)


def agreement_A(n: int, lags: list[set[int]], f1: list[int], f2: list[int]) -> Fraction:
    """A = Pr_{L,x}[ 1_L(f1 x) = 1_L(f2 x) ]."""
    size = 1 << (2 * n)
    total = 0
    for x in range(size):
        u, v = f1[x], f2[x]
        total += sum(1 for L in lags if (u in L) == (v in L))
    return Fraction(total, len(lags) * size)


def corrected_sd_formula(n: int, A: Fraction, p: Fraction = P_NOISE) -> Fraction:
    """Corrected same-secret SD for a label-preserving split (Track K)."""
    return Fraction(1) - Fraction(1, 4 ** n) * (
        2 * p * (1 - p) + (1 - 2 * p) ** 2 * A
    )


def universal_minimum(n: int, p: Fraction = P_NOISE) -> Fraction:
    """Orbit/minimum value 1 - (p^2+(1-p)^2)/4^n, attained iff f1=f2."""
    return Fraction(1) - (p * p + (1 - p) * (1 - p)) / (4 ** n)


def exact_sd_label_preserving(
    n: int,
    lags: list[set[int]],
    f1: list[int],
    f2: list[int],
    p: Fraction = P_NOISE,
) -> Fraction:
    """Exact SD between transformed split pair and the UNTRANSFORMED fresh pair.

    L4 guard: f1,f2 are applied only to the split-side sample (x,b);
    the fresh comparison sample (u1,b1,u2,b2) is left in the natural domain.
    """
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
        # Split side: (f1(x), b, f2(x), b)
        for x in range(size):
            c = (mask >> x) & 1
            for e in (0, 1):
                b = c ^ e
                key = (f1[x] << (N + 2)) | (b << (N + 1)) | (f2[x] << 1) | b
                w = (qnum if e == 0 else pnum) * denom
                counts_P[key] = counts_P.get(key, 0) + w
        # Fresh comparison side: (u1, b1, u2, b2), NOT transformed.
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


def sample_bijection_pairs(n: int, rng: random.Random) -> dict[str, tuple[list[int], list[int]]]:
    """Generate the 12 named bijection pairs for n=2 testing."""
    N = 2 * n
    size = 1 << N
    pairs: dict[str, tuple[list[int], list[int]]] = {}

    # identity / identity
    pairs["id_id"] = (list(range(size)), list(range(size)))

    # five symplectic orbit pairs
    sp4 = enumerate_sp4()
    for idx, T in enumerate(sp4[:5]):
        f2 = [apply_matrix_cols(T, x) for x in range(size)]
        pairs[f"symplectic_{idx}"] = (list(range(size)), f2)

    # three affine pairs: f(x) = A x + t
    gl4 = enumerate_gl(4)
    for idx, A in enumerate(gl4[:3]):
        t = rng.randrange(1, size)
        f = [(apply_matrix_cols(A, x) ^ t) for x in range(size)]
        pairs[f"affine_{idx}"] = (list(range(size)), f)

    # three random bijections
    for idx in range(3):
        f2 = random_bijection(size, rng)
        pairs[f"random_{idx}"] = (list(range(size)), f2)

    return pairs


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--seed", type=int, default=20260614)
    return p.parse_args()


def main():
    args = parse_args()
    p = P_NOISE
    rng = random.Random(args.seed)

    # ------------------------------------------------------------------
    # G1: closed form and verification by enumeration
    # ------------------------------------------------------------------
    formula_values = {}
    enum_values = {}
    for n in (2, 3):
        formula = pr_b_neq_formula(n, p)
        # enumerate over all Lagrangians and (u1,u2,e1,e2)
        lags = all_lagrangians(n)
        size = 1 << (2 * n)
        total = Fraction(0)
        for L in lags:
            mask = 0
            for v in L:
                mask |= 1 << v
            for u1 in range(size):
                c1 = (mask >> u1) & 1
                for u2 in range(size):
                    c2 = (mask >> u2) & 1
                    for e1 in (0, 1):
                        w1 = p if e1 else (1 - p)
                        b1 = c1 ^ e1
                        for e2 in (0, 1):
                            w2 = p if e2 else (1 - p)
                            b2 = c2 ^ e2
                            if b1 != b2:
                                total += w1 * w2
        enum = total / (len(lags) * size * size)
        assert formula == enum, f"n={n}: formula {formula} != enum {enum}"
        formula_values[str(n)] = str(formula)
        enum_values[str(n)] = str(enum)
    print("G1: Pr_fresh[b1!=b2] formula == enumeration for n=2,3")
    print(f"  n=2: {formula_values['2']}")
    print(f"  n=3: {formula_values['3']}")

    # ------------------------------------------------------------------
    # K1: corrected same-secret SD law at n=2 (12 pairs)
    # ------------------------------------------------------------------
    n = 2
    lags2 = all_lagrangians(n)
    orbit_min = universal_minimum(n, p)
    print(f"\nK1: corrected same-secret SD, n={n}; orbit minimum = {orbit_min}")

    pairs = sample_bijection_pairs(n, rng)
    sd_results = []
    all_ok = True
    any_strict = False
    for name, (f1, f2) in pairs.items():
        A = agreement_A(n, lags2, f1, f2)
        sd_formula = corrected_sd_formula(n, A, p)
        sd_direct = exact_sd_label_preserving(n, lags2, f1, f2, p)
        match = (sd_formula == sd_direct)
        ge = (sd_direct >= orbit_min)
        ident = (f1 == f2)
        eq = (sd_direct == orbit_min)
        all_ok &= match and ge and (eq == ident)
        if not eq:
            any_strict = True
        sd_results.append({
            "name": name,
            "sd": str(sd_direct),
            "A": str(A),
            "formula_matches_direct": match,
            "meets_universal_bound": ge,
            "equals_orbit_minimum": eq,
            "is_literal_duplicate": ident,
        })
        print(f"  {name}: SD = {sd_direct}, A = {A}, formula_match={match}, "
              f"ge_bound={ge}, eq_orbit={eq}")
    assert all_ok, "corrected law verification failed"
    assert any_strict, "expected at least one strictly-larger SD"
    print("  => corrected law verified; orbit value is the universal MINIMUM")

    # ------------------------------------------------------------------
    # K1: n=3 spot check
    # ------------------------------------------------------------------
    n3 = 3
    lags3 = all_lagrangians(n3)
    f1_n3 = list(range(1 << (2 * n3)))
    f2_n3 = random_symplectic_perm(n3, rng)
    A3 = agreement_A(n3, lags3, f1_n3, f2_n3)
    sd_formula_n3 = corrected_sd_formula(n3, A3, p)
    sd_direct_n3 = exact_sd_label_preserving(n3, lags3, f1_n3, f2_n3, p)
    assert sd_formula_n3 == sd_direct_n3
    orbit3 = universal_minimum(n3, p)
    print(f"\nn=3 spot: SD = {sd_direct_n3} (formula OK; A = {A3}); "
          f"orbit minimum = {orbit3}; strict = {sd_direct_n3 > orbit3}")

    # ------------------------------------------------------------------
    # Assemble output
    # ------------------------------------------------------------------
    result = {
        "track": "G-corrected-by-K",
        "experiment": 211,
        "noise_rate_p": str(p),
        "theorem_G1": {
            "statement": "Pr_fresh[b1 != b2] = 2 (p + (1-2p)/2^n) (1-p - (1-2p)/2^n)",
            "mu_n": "1/2^n",
            "q_n": "p + (1-2p)/2^n",
            "values": formula_values,
            "verified_by_enumeration": enum_values,
            "label": "THEOREM",
        },
        "theorem_G1_lower_bound": {
            "statement": "For every pair of public bijections f1,f2 of F_2^{2n}, the label-preserving split has SD >= Pr_fresh[b1 != b_2]",
            "reason": "(b1,b2)-marginal of transformed pair is supported on {00,11}; fresh pair puts the stated mass on {01,10}; data processing for total variation",
            "family": "label-preserving public bijections f1,f2",
            "label": "THEOREM",
        },
        "old_G3_withdrawn": {
            "original_claim": "Exact same-secret SD is independent of f1,f2 and equals 1 - (p^2+(1-p)^2)/4^n for all bijection pairs",
            "flaw": "Applied the verification bijections f_i^{-1} to the FRESH comparison pair too, violating guard (L4); the fresh distribution is not invariant under arbitrary bijections",
            "status": "WITHDRAWN / CORRECTED",
            "label": "WITHDRAWN",
        },
        "corrected_same_secret_law": {
            "statement": "SD(split_{f1,f2}(D_L), D_L x D_L) = 1 - 4^{-n}[2p(1-p) + (1-2p)^2 A], where A = Pr_{L,x}[1_L(f1 x) = 1_L(f2 x)]",
            "closed_form_p_1_4": "1 - (3 + 2 A)/128",
            "universal_minimum": str(orbit_min),
            "equality_condition": "A = 1 iff f1 = f2 (literal duplicate); otherwise SD strictly larger",
            "n2_target_minimum": str(orbit_min),
            "n3_target_minimum": str(orbit3),
            "n3_spot_sd": str(sd_direct_n3),
            "n3_spot_A": str(A3),
            "tested_pairs_n2": sd_results,
            "label": "THEOREM",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON stores string fractions",
            "L2_duality_care": "not invoked (no character sums over Lagrangians)",
            "L3_query_class_hygiene": "distributional TV result; no Feldman/SQ/query-class statement made",
            "L4_never_transform_comparison_distribution": "fresh pair (u1,b1,u2,b2) is compared in the natural domain; f1,f2 act only on the split side",
        },
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from the SAME uniform secret L (natural LSN pair), NOT pre-transformed by f1 or f2",
            "family_names": "label-preserving = split (x,b)|->((f1(x),b),(f2(x),b)); label-flipping extension in Track K experiment 212",
            "PRE_REGISTERED": "hardness interpretation guarded: structural distributional gap, not a lem:m2 rate or attack claim",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "211-trackG-label-preserving-universal-bound.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
