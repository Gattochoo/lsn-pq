#!/usr/bin/env python3
"""211 (Track G): universal label-preserving obstruction and exact SD invariance.

Track-G question: does the OP7 obstruction extend beyond the symplectic-orbit
family to arbitrary public bijections that preserve the label bit?

G1. THEOREM (closed-form marginal obstruction).
    For the LSN noise rate p and a uniformly random Lagrangian secret L, let
    (u_1,b_1) and (u_2,b_2) be two independent fresh samples from D_L.  Then

        mu_n := Pr[1_L(u)=1] = 2^n / 2^{2n} = 1/2^n,
        q_n  := Pr[b=1]     = mu_n(1-p) + (1-mu_n)p
                            = p + (1-2p)/2^n,
        Pr_fresh[b_1 != b_2] = 2 q_n (1-q_n)
                            = 2 (p + (1-2p)/2^n)(1-p - (1-2p)/2^n).

    For any public bijections f_1,f_2 of F_2^{2n}, the split map

        (x,b) |--> ((f_1(x),b), (f_2(x),b))

    emits a pair whose (b_1,b_2)-marginal is supported on {00,11}, whereas the
    fresh pair puts mass Pr_fresh[b_1!=b_2] on {01,10}.  By data processing,

        SD( split_{f_1,f_2}(D_L) , D_L x D_L )  >=  Pr_fresh[b_1 != b_2].

    This lower bound is universal for the label-preserving family.

G2. Scope definition of label-modifying maps (EVIDENCE/OPEN).

G3. THEOREM (exact SD is independent of the bijections).
    Under the natural same-secret comparison (both samples drawn from the same
    uniform secret L), the exact SD for the label-preserving split is the same
    for every pair of public bijections f_1,f_2:

        SD = 1 - (p^2 + (1-p)^2) / 4^n
           = 1 - 5/(8*4^n)            at p = 1/4.

    Proof sketch: applying the bijections f_i^{-1} to the i-th x-coordinate is
    a bijection on the joint sample space, so it preserves SD; it sends both
    the transformed and the fresh pair to the distributions obtained for
    f_1=f_2=id.  Hence the orbit-family value is universal for all label-
    preserving public bijections.  This is verified computationally below for
    identity, symplectic, affine, and random bijections at n=2.

Guards:
  L1 exact arithmetic: Fractions end-to-end; JSON stores string fractions.
  L2 duality care: not invoked (no character sums over Lagrangians).
  L3 query-class hygiene: this is a total-variation/distinguishability result;
       no Feldman/SQ theorem is used, so no query class is involved.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product
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


def random_symplectic_matrix(n: int, rng: random.Random, steps: int = 80) -> tuple[int, ...]:
    """Generate a random element of Sp(2n,F_2) as a word of transvections."""
    N = 2 * n
    cols = [1 << i for i in range(N)]
    for _ in range(steps):
        u = rng.randint(1, (1 << N) - 1)
        for i in range(N):
            if symplectic_form_n(cols[i], u, n):
                cols[i] ^= u
    assert is_symplectic_matrix(tuple(cols), n)
    return tuple(cols)


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


def pr_b_neq_formula(n: int, p: Fraction = P_NOISE) -> Fraction:
    """Closed form Pr_fresh[b_1 != b_2] (THEOREM G.1)."""
    q = p + Fraction(1 - 2 * p, 2 ** n)
    return 2 * q * (1 - q)


def orbit_sd_formula(n: int, p: Fraction = P_NOISE) -> Fraction:
    """Closed-form exact SD for any label-preserving split (THEOREM G.3)."""
    q = 1 - p
    return Fraction(1) - (p * p + q * q) / (4 ** n)


def pr_b_neq_by_enumeration(n: int, p: Fraction = P_NOISE) -> Fraction:
    """Enumerate Pr_fresh[b_1 != b_2] directly (verification of G.1)."""
    lags = all_lagrangians(n)
    N = 2 * n
    size = 1 << N
    total = Fraction(0)
    for L in lags:
        mask = 0
        for v in L:
            mask |= 1 << v
        for u1 in range(size):
            c1 = (mask >> u1) & 1
            for u2 in range(size):
                c2 = (mask >> u2) & 1
                # independent Bernoulli(p) noise bits e1,e2
                for e1 in (0, 1):
                    w1 = p if e1 else (1 - p)
                    b1 = c1 ^ e1
                    for e2 in (0, 1):
                        w2 = p if e2 else (1 - p)
                        b2 = c2 ^ e2
                        if b1 != b2:
                            total += w1 * w2
    total /= len(lags) * size * size
    return total


def exact_sd_label_preserving(
    n: int,
    f1: list[int] | None = None,
    f2: list[int] | None = None,
    p: Fraction = P_NOISE,
) -> Fraction:
    """Exact SD between transformed split pair and fresh same-secret pair.

    f1,f2 are permutations of F_2^{2n}; None means identity.  The output domain
    is encoded as a single integer (x1,b1,x2,b2) with 4n+2 bits.
    """
    lags = all_lagrangians(n)
    N = 2 * n
    size = 1 << N
    if f1 is None:
        f1 = list(range(size))
    if f2 is None:
        f2 = list(range(size))

    pnum = p.numerator
    qnum = p.denominator - p.numerator
    denom = p.denominator

    # We accumulate integer counts with common denominator denom^2 per (L,u,e) draw.
    # Transformed: for each (L,u,e) weight qnum or pnum.
    # Fresh: for each (L,u1,u2,e1,e2) weight qnum^{2-e1-e2} pnum^{e1+e2}.
    # To compare directly, expand transformed to denominator denom^2:
    #   transformed weight = qnum^{1-e} pnum^{e} * denom
    #   fresh weight       = qnum^{2-e1-e2} pnum^{e1+e2}
    # Common denominator per L draw for transformed: size * denom^2
    # Common denominator per L draw for fresh: size^2 * denom^2
    # Overall denominators:
    D_P = len(lags) * size * denom * denom  # transformed
    D_Q = len(lags) * size * size * denom * denom  # fresh

    counts_P: dict[int, int] = {}
    counts_Q: dict[int, int] = {}

    for L in lags:
        mask = 0
        for v in L:
            mask |= 1 << v
        # Transformed: (f1(u), b, f2(u), b)
        for u in range(size):
            c = (mask >> u) & 1
            for e in (0, 1):
                b = c ^ e
                key = (f1[u] << (N + 2)) | (b << (N + 1)) | (f2[u] << 1) | b
                w = (qnum if e == 0 else pnum) * denom
                counts_P[key] = counts_P.get(key, 0) + w
        # Fresh: (f1(u1), b1, f2(u2), b2)
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
                        key = (f1[u1] << (N + 2)) | (b1 << (N + 1)) | (f2[u2] << 1) | b2
                        counts_Q[key] = counts_Q.get(key, 0) + w1 * w2

    num = 0
    keys = set(counts_P.keys()) | set(counts_Q.keys())
    for k in keys:
        num += abs(counts_P.get(k, 0) * D_Q - counts_Q.get(k, 0) * D_P)
    return Fraction(num, 2 * D_P * D_Q)


def sample_bijection_pairs(n: int, rng: random.Random) -> dict[str, tuple[list[int], list[int]]]:
    """Generate a dictionary of named bijection pairs for n=2 testing."""
    N = 2 * n
    size = 1 << N
    pairs: dict[str, tuple[list[int], list[int]]] = {}

    # identity / identity
    pairs["id_id"] = (list(range(size)), list(range(size)))

    # symplectic orbit pairs
    sp4 = enumerate_sp4()
    for idx, T in enumerate(sp4[:3]):
        f2 = [apply_matrix_cols(T, x) for x in range(size)]
        pairs[f"symplectic_{idx}"] = (list(range(size)), f2)

    # affine pairs: f(x) = A x + t for various A in GL(4,F_2) and t
    gl4 = enumerate_gl(4)
    for idx, A in enumerate(gl4[:5]):
        t = idx % size
        f = [(apply_matrix_cols(A, x) ^ t) for x in range(size)]
        pairs[f"affine_{idx}"] = (list(range(size)), f)

    # random bijections
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
        enum = pr_b_neq_by_enumeration(n, p)
        assert formula == enum, f"n={n}: formula {formula} != enum {enum}"
        formula_values[str(n)] = str(formula)
        enum_values[str(n)] = str(enum)
    print("G1: Pr_fresh[b1!=b2] formula == enumeration for n=2,3")
    print(f"  n=2: {formula_values['2']}")
    print(f"  n=3: {formula_values['3']}")

    # ------------------------------------------------------------------
    # G3: exact SD invariance under bijections at n=2
    # ------------------------------------------------------------------
    n = 2
    target = orbit_sd_formula(n, p)
    print(f"\nG3: exact SD target for n={n} = {target}")

    pairs = sample_bijection_pairs(n, rng)
    sd_results = []
    all_match = True
    for name, (f1, f2) in pairs.items():
        sd = exact_sd_label_preserving(n, f1, f2, p)
        match = (sd == target)
        all_match &= match
        sd_results.append({
            "name": name,
            "sd": str(sd),
            "matches_target": match,
        })
        print(f"  {name}: SD = {sd}, matches = {match}")
    assert all_match, "SD invariance failed"

    # Also verify n=3 for identity (too many bijections to enumerate)
    n3_target = orbit_sd_formula(3, p)
    n3_id_sd = exact_sd_label_preserving(3, None, None, p)
    assert n3_id_sd == n3_target
    print(f"\nn=3 identity SD = {n3_id_sd} (target {n3_target})")

    # ------------------------------------------------------------------
    # Assemble output
    # ------------------------------------------------------------------
    result = {
        "track": "G",
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
            "statement": "For every pair of public bijections f1,f2 of F_2^{2n}, the label-preserving split has SD >= Pr_fresh[b1 != b2]",
            "reason": "(b1,b2)-marginal of transformed pair is supported on {00,11}; fresh pair puts the stated mass on {01,10}; data processing for total variation",
            "family": "label-preserving public bijections f1,f2",
            "label": "THEOREM",
        },
        "theorem_G3_invariance": {
            "statement": "Under same-secret comparison, SD(split_{f1,f2}(D_L), D_L x D_L) = 1 - (p^2+(1-p)^2)/4^n, independent of f1,f2",
            "closed_form_p_1_4": "1 - 5/(8*4^n)",
            "n2_target": str(target),
            "n3_target": str(n3_target),
            "n3_identity_sd": str(n3_id_sd),
            "tested_pairs_n2": sd_results,
            "label": "THEOREM",
        },
        "G2_label_modifying_family": {
            "definition": "public bijections g_i: F_2^{2n} x F_2 -> F_2^{2n} x F_2; split (x,b) |-> (g_1(x,b), g_2(x,b))",
            "correctness_constraint": "g_i maps D_L to D_{L'} for some Lagrangian L' (valid LSN sample -> valid LSN sample)",
            "findings": (
                "If g_i are valid, applying g_i^{-1} to the i-th output reduces to the "
                "label-preserving case, so the same universal lower bound applies. "
                "Fully general (invalid) label-modifying bijections produce outputs that are "
                "not LSN samples; the appropriate comparison distribution is OPEN."
            ),
            "label": "EVIDENCE/OPEN",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON stores string fractions",
            "L2_duality_care": "not invoked (no character sums over Lagrangians)",
            "L3_query_class_hygiene": "distributional TV result; no SQ/query-class statement made",
        },
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from the SAME uniform secret L (natural LSN pair)",
            "family_names": "label-preserving = split (x,b)|->((f1(x),b),(f2(x),b)); label-modifying = split with bijections g_i(x,b)",
            "output_sd": "universal exact SD -> 1 as n grows; universal lower bound from duplicated label bit -> 2p(1-p) = 3/8 at p=1/4",
            "PRE_REGISTERED": "hardness interpretation guarded: this is a structural distributional gap, not a lem:m2 rate or attack claim",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "211-trackG-label-preserving-universal-bound.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
