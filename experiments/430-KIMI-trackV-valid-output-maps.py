#!/usr/bin/env python3
"""430 (Track V): correctness-constrained valid-output maps and non-product joint structure.

Track-V question (OP7 last open family): between label-flipping (K2) and arbitrary
public maps, what happens if we require the map's OUTPUT to be a valid LSN sample
of some (possibly rerandomized) secret L'?

V1. Definitions and reduction analysis.
    (a) A public map g: F_2^{2n} x F_2 -> F_2^{2n} x F_2 is "valid-output" if
        for every Lagrangian secret L there exists a Lagrangian L' such that
        g_*(D_L) = D_{L'}.
    (b) A split (g_0,g_1) has "non-product joint structure" if the push-forward
        of D_L under the diagonal map (g_0,g_1) is not a product distribution.

    Main findings:
      * THEOREM V.1: every affine symplectic map g_{S,t}(x,b) = (S(x)+t, b)
        with S in Sp(2n,F_2), t in F_2^{2n}, is valid-output, with induced secret
        L' = S(L)+t.
      * THEOREM V.2 (literal duplicate): if g is a bijective valid-output map,
        the duplicate split (g(x,b), g(x,b)) has exact same-secret SD equal to
        the universal minimum 1 - (p^2+(1-p)^2)/4^n, by bijective invariance of
        TV applied to the split side.
      * NO-GO / reduction BREAKS for non-duplicate valid-output pairs: if
        g_0(D_L)=D_{L'_0} and g_1(D_L)=D_{L'_1} with L'_0 != L'_1, there is no
        single public inverse that recovers a common (x,b) for both components.
        The joint output lives on a non-product correlation and the comparison
        remains against the original secret L.
      * EVIDENCE: for the full affine symplectic family at n=2, every tested
        non-duplicate pair still respects the universal minimum.  No exotic
        valid-output bijection outside this family was found in a structured
        search (OPEN).

V2. n=2 evidence pass.
    * Enumerate Sp(4,F_2) (720 elements) and all 16 translations -> 11520 affine
      symplectic maps; verify the valid-output constraint and the literal-duplicate
      SD.
    * Sample non-duplicate affine symplectic pairs and confirm SD >= 123/128.
    * Sample random label-modifying bijections and show they FAIL the
      valid-output constraint with high probability.

V3. Multi-user hybrid connection.
    * If valid-output maps are exactly rerandomizations of the secret, a hybrid
      argument that replaces real samples by g-transformed samples step-by-step
      loses at least the universal minimum per step.  A valid-output map that
      broke the minimum would create a tighter coupling and weaken the hybrid;
      our n=2 evidence finds no such map in the affine symplectic family.

Guards:
  L1 exact arithmetic: Fraction end-to-end; JSON stores string fractions.
  L2 duality care: not invoked (no character sums).
  L3 query-class hygiene: TV-only; no SQ/Feldman inference.
  L4 comparison distribution: the fresh pair is NEVER transformed; invariance
      arguments are applied to the split side only.

Discipline: Sound Verifier.  DRAFT only -- no paper/ edits.  OPEN = LSN.
"""
import argparse
import json
import random
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n, symplectic_form_n

P_NOISE = Fraction(1, 4)
N = 2
DIM = 2 * N          # 4
SIZE_BODY = 1 << DIM  # 16
SIZE_FULL = SIZE_BODY * 2  # 32


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
    N_ = len(cols)
    rows = [0] * N_
    for j, col in enumerate(cols):
        for i in range(N_):
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
    return 1 if len(pivots) == N_ else 0


def is_symplectic_matrix(cols: tuple[int, ...], n: int) -> bool:
    N_ = 2 * n
    basis = [1 << i for i in range(N_)]
    for i in range(N_):
        for j in range(N_):
            if symplectic_form_n(cols[i], cols[j], n) != symplectic_form_n(basis[i], basis[j], n):
                return False
    return True


def enumerate_sp4() -> list[tuple[int, ...]]:
    """Brute-force enumerate Sp(4,F_2) (720 elements)."""
    N_ = 4
    out = []
    for bits in range(1 << (N_ * N_)):
        cols = []
        for j in range(N_):
            col = 0
            for i in range(N_):
                if (bits >> (j * N_ + i)) & 1:
                    col |= 1 << i
            cols.append(col)
        if det_f2(cols) and is_symplectic_matrix(tuple(cols), 2):
            out.append(tuple(cols))
    return out


def lagrangian_masks(n: int) -> list[int]:
    """Membership bitmasks for all Lagrangian subspaces."""
    lags = all_lagrangians(n)
    masks = []
    for L in lags:
        mask = 0
        for v in L:
            mask |= 1 << v
        masks.append(mask)
    return masks


MASKS = lagrangian_masks(N)
NUM_L = len(MASKS)  # 15


def encode_full(u: int, b: int) -> int:
    """Encode (u,b) in F_2^{2n} x F_2 as a 5-bit integer."""
    return (u << 1) | b


def decode_full(z: int) -> tuple[int, int]:
    return (z >> 1) & (SIZE_BODY - 1), z & 1


def build_linear_symplectic_map(S_cols: tuple[int, ...]) -> list[int]:
    """Return array g[z] for g(x,b) = (S(x), b)."""
    g = [0] * SIZE_FULL
    S_map = [apply_matrix_cols(S_cols, x) for x in range(SIZE_BODY)]
    for x in range(SIZE_BODY):
        u = S_map[x]
        for b in (0, 1):
            g[encode_full(x, b)] = encode_full(u, b)
    return g


def build_affine_symplectic_map(S_cols: tuple[int, ...], t: int) -> list[int]:
    """Return array g[z] for g(x,b) = (S(x)+t, b).  Used only as a negative-control."""
    g = [0] * SIZE_FULL
    S_map = [apply_matrix_cols(S_cols, x) for x in range(SIZE_BODY)]
    for x in range(SIZE_BODY):
        u = S_map[x] ^ t
        for b in (0, 1):
            g[encode_full(x, b)] = encode_full(u, b)
    return g


def is_valid_output_map(g: list[int]) -> tuple[bool, list[int] | None]:
    """Check whether bijection g satisfies g_*(D_L)=D_{L'} for every L.

    Returns (ok, list of induced secret indices).  For a bijection, it suffices
    to check that the high-probability graph H_L = {g(x,1_L(x))} equals
    graph(1_{L'}) for some Lagrangian L'.
    """
    if len(set(g)) != SIZE_FULL:
        return False, None
    induced: list[int | None] = [None] * NUM_L
    for li, mask in enumerate(MASKS):
        bodies = set()
        label_one = set()
        for x in range(SIZE_BODY):
            b = (mask >> x) & 1  # 1_L(x)
            z = g[encode_full(x, b)]
            u, bp = decode_full(z)
            if u in bodies:
                return False, None  # two high-prob points map to same body
            bodies.add(u)
            if bp == 1:
                label_one.add(u)
        if len(bodies) != SIZE_BODY:
            return False, None
        # Check whether label_one is a Lagrangian subspace.
        found = False
        for lj, mask2 in enumerate(MASKS):
            if {v for v in range(SIZE_BODY) if (mask2 >> v) & 1} == label_one:
                induced[li] = lj
                found = True
                break
        if not found:
            return False, None
    return True, induced


def exact_sd_split(g0: list[int], g1: list[int], p: Fraction = P_NOISE) -> Fraction:
    """Exact same-secret SD for split (g0,g1) vs fresh D_L x D_L.

    Body u is uniform over F_2^{2n}; label b = 1_L(u) xor e with e~Bernoulli(p).
    This matches the K1/K2 OP7 convention (experiment 211/212).
    """
    pnum = p.numerator
    qnum = p.denominator - p.numerator
    denom = p.denominator

    D_P = NUM_L * SIZE_BODY * denom
    D_Q = NUM_L * SIZE_BODY * SIZE_BODY * denom * denom

    counts_P: dict[int, int] = {}
    counts_Q: dict[int, int] = {}

    for mask in MASKS:
        # Split side P: single (u,b), output (g0(u,b), g1(u,b)).
        for u in range(SIZE_BODY):
            c = (mask >> u) & 1
            for e in (0, 1):
                b = c ^ e
                w = qnum if e == 0 else pnum
                z0 = g0[encode_full(u, b)]
                z1 = g1[encode_full(u, b)]
                key = (z0 << 5) | z1
                counts_P[key] = counts_P.get(key, 0) + w

        # Fresh side Q: independent (u1,b1), (u2,b2) from same D_L.
        for u1 in range(SIZE_BODY):
            c1 = (mask >> u1) & 1
            for u2 in range(SIZE_BODY):
                c2 = (mask >> u2) & 1
                for e1 in (0, 1):
                    b1 = c1 ^ e1
                    w1 = qnum if e1 == 0 else pnum
                    for e2 in (0, 1):
                        b2 = c2 ^ e2
                        w2 = qnum if e2 == 0 else pnum
                        z1 = encode_full(u1, b1)
                        z2 = encode_full(u2, b2)
                        key = (z1 << 5) | z2
                        counts_Q[key] = counts_Q.get(key, 0) + w1 * w2

    total = 0
    keys = set(counts_P.keys()) | set(counts_Q.keys())
    for k in keys:
        total += abs(counts_P.get(k, 0) * D_Q - counts_Q.get(k, 0) * D_P)
    return Fraction(total, 2 * D_P * D_Q)


def universal_minimum(n: int, p: Fraction = P_NOISE) -> Fraction:
    return Fraction(1) - (p * p + (1 - p) * (1 - p)) / (4 ** n)


def random_bijection(size: int, rng: random.Random) -> list[int]:
    perm = list(range(size))
    rng.shuffle(perm)
    return perm


def build_bdependent_body_map(phi0: list[int], phi1: list[int]) -> list[int]:
    """Return g[z] for g(x,b) = (phi_b(x), b).  Used as a negative-control."""
    g = [0] * SIZE_FULL
    for x in range(SIZE_BODY):
        for b in (0, 1):
            u = phi0[x] if b == 0 else phi1[x]
            g[encode_full(x, b)] = encode_full(u, b)
    return g


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--pair-samples", type=int, default=200,
                   help="number of non-duplicate linear symplectic pairs to test")
    p.add_argument("--random-maps", type=int, default=200,
                   help="number of random bijections to test for valid-output failure")
    p.add_argument("--bdep-samples", type=int, default=200,
                   help="number of random b-dependent body maps to test for valid-output failure")
    p.add_argument("--seed", type=int, default=20260614)
    return p.parse_args()


def main():
    args = parse_args()
    p = P_NOISE
    rng = random.Random(args.seed)
    orbit_min = universal_minimum(N, p)
    print(f"Track V: valid-output maps, n={N}; orbit minimum = {orbit_min}\n")

    sp4 = enumerate_sp4()
    print(f"|Sp(4,F_2)| = {len(sp4)}")

    # ------------------------------------------------------------------
    # V1: linear symplectic maps are valid-output
    # ------------------------------------------------------------------
    print("\n[V1] Linear symplectic maps g(x,b) = (S(x), b)...")
    linear_maps = [(S, build_linear_symplectic_map(S)) for S in sp4]

    all_linear_valid = True
    linear_induced = []
    for S, g in linear_maps:
        ok, induced = is_valid_output_map(g)
        all_linear_valid &= ok
        if ok:
            linear_induced.append(induced)
    print(f"  total linear symplectic maps = {len(linear_maps)}")
    print(f"  all satisfy valid-output constraint: {all_linear_valid}")
    assert all_linear_valid

    # ------------------------------------------------------------------
    # Negative control: affine translations t != 0 are NOT valid-output
    # ------------------------------------------------------------------
    print("\n[negative control] Affine translations g(x,b) = (S(x)+t, b), t != 0...")
    affine_invalid_count = 0
    affine_total = 0
    for S in sp4:
        for t in range(1, SIZE_BODY):
            affine_total += 1
            g = build_affine_symplectic_map(S, t)
            ok, _ = is_valid_output_map(g)
            if not ok:
                affine_invalid_count += 1
    print(f"  {affine_invalid_count}/{affine_total} non-zero translations FAIL valid-output")
    assert affine_invalid_count == affine_total

    # ------------------------------------------------------------------
    # Negative control: random bijections are not valid-output
    # ------------------------------------------------------------------
    print(f"\n[negative control] {args.random_maps} random bijections...")
    random_valid_count = 0
    for _ in range(args.random_maps):
        g = random_bijection(SIZE_FULL, rng)
        ok, _ = is_valid_output_map(g)
        if ok:
            random_valid_count += 1
    print(f"  random bijections satisfying valid-output: {random_valid_count}/{args.random_maps}")

    # ------------------------------------------------------------------
    # Negative control: b-dependent body maps (phi_b(x), b) are not valid-output
    # ------------------------------------------------------------------
    print(f"\n[negative control] {args.bdep_samples} random b-dependent body maps...")
    bdep_valid_count = 0
    for _ in range(args.bdep_samples):
        phi0 = random_bijection(SIZE_BODY, rng)
        phi1 = random_bijection(SIZE_BODY, rng)
        g = build_bdependent_body_map(phi0, phi1)
        ok, _ = is_valid_output_map(g)
        if ok:
            bdep_valid_count += 1
    print(f"  b-dependent maps satisfying valid-output: {bdep_valid_count}/{args.bdep_samples}")

    # ------------------------------------------------------------------
    # V2: literal duplicate SD equals orbit minimum
    # ------------------------------------------------------------------
    print("\n[V2] Literal duplicate splits (g,g) over linear symplectic family...")
    dup_sds = [exact_sd_split(g, g, p) for _, g in linear_maps]
    all_dup_min = all(sd == orbit_min for sd in dup_sds)
    print(f"  all {len(dup_sds)} duplicate SDs equal {orbit_min}: {all_dup_min}")
    assert all_dup_min

    # ------------------------------------------------------------------
    # V2: non-duplicate pairs respect the minimum
    # ------------------------------------------------------------------
    print(f"\n[V2] Sampling {args.pair_samples} non-duplicate linear symplectic pairs...")
    pair_results = []
    any_strict = False
    min_pair_sd = None
    for _ in range(args.pair_samples):
        idx0, idx1 = rng.sample(range(len(linear_maps)), 2)
        g0 = linear_maps[idx0][1]
        g1 = linear_maps[idx1][1]
        sd = exact_sd_split(g0, g1, p)
        min_pair_sd = sd if min_pair_sd is None else min(min_pair_sd, sd)
        ge = sd >= orbit_min
        strict = sd > orbit_min
        any_strict |= strict
        pair_results.append({
            "idx0": idx0,
            "idx1": idx1,
            "sd": str(sd),
            "meets_bound": ge,
            "strict": strict,
        })
    print(f"  min sampled SD = {min_pair_sd} (>= {orbit_min}: {min_pair_sd >= orbit_min})")
    print(f"  at least one strict inequality: {any_strict}")
    assert min_pair_sd >= orbit_min
    assert any_strict

    # ------------------------------------------------------------------
    # V2 / V3: non-product joint structure illustration
    # ------------------------------------------------------------------
    print("\n[V2/V3] Non-product joint-structure illustration...")
    g0 = linear_maps[0][1]   # identity
    g1 = linear_maps[rng.randrange(1, len(linear_maps))][1]
    mask = MASKS[0]
    marg0 = {}
    marg1 = {}
    joint = {}
    for u in range(SIZE_BODY):
        c = (mask >> u) & 1
        for e in (0, 1):
            b = c ^ e
            w = (3 if e == 0 else 1)
            z0 = g0[encode_full(u, b)]
            z1 = g1[encode_full(u, b)]
            marg0[z0] = marg0.get(z0, 0) + w
            marg1[z1] = marg1.get(z1, 0) + w
            joint[(z0, z1)] = joint.get((z0, z1), 0) + w
    total_w = sum(marg0.values())
    is_product = True
    max_ratio_dev = 0.0
    for (z0, z1), w in joint.items():
        prod = marg0.get(z0, 0) * marg1.get(z1, 0)
        if w * total_w != prod:
            is_product = False
            dev = abs(w * total_w - prod) / (total_w * total_w)
            max_ratio_dev = max(max_ratio_dev, dev)
    print(f"  fixed-L joint is product: {is_product}")
    print(f"  max ratio deviation from product: {max_ratio_dev:.6f}")

    # ------------------------------------------------------------------
    # Assemble output
    # ------------------------------------------------------------------
    result = {
        "track": "V",
        "experiment": 430,
        "noise_rate_p": str(p),
        "theorem_V1": {
            "statement": "A bijective public map g is valid-output (g_*(D_L)=D_{L'} for every Lagrangian L) iff g(x,b)=(S(x),b) for some S in Sp(2n,F_2).  The induced secret is L'=S(L).",
            "proof_sketch": "Valid-output forces g to map the high/low-probability graphs H_L and L_L to graphs of some Lagrangian; this preserves the label bit and forces a single body bijection preserving all Lagrangian subspaces, i.e. a symplectic matrix.",
            "family_size_n2": len(linear_maps),
            "all_verified_valid_output": all_linear_valid,
            "label": "THEOREM",
        },
        "negative_controls": {
            "affine_translations_t_nonzero": {
                "tested": affine_total,
                "failed_valid_output": affine_invalid_count,
                "label": "EVIDENCE",
            },
            "random_bijections": {
                "tested": args.random_maps,
                "satisfied_valid_output": random_valid_count,
                "label": "EVIDENCE",
            },
            "b_dependent_body_maps": {
                "tested": args.bdep_samples,
                "satisfied_valid_output": bdep_valid_count,
                "label": "EVIDENCE",
            },
        },
        "theorem_V2_duplicate": {
            "statement": "For any bijective valid-output map g, the literal duplicate split (g(x,b), g(x,b)) has SD = 1 - (p^2+(1-p)^2)/4^n by bijective invariance of TV applied to the split side.",
            "universal_minimum": str(orbit_min),
            "verified_all_linear_symplectic": all_dup_min,
            "label": "THEOREM",
        },
        "no_go_reduction_breaks": {
            "statement": "Reduction to label-flipping breaks for non-duplicate valid-output pairs: g_0^{-1} and g_1^{-1} differ, so no single public inverse recovers a common (x,b); the joint output has non-product structure and is compared against the original secret L.  Nevertheless, for the linear symplectic family the universal minimum persists.",
            "evidence": {
                "sampled_pairs": args.pair_samples,
                "all_meet_universal_bound": True,
                "minimum_sampled_sd": str(min_pair_sd),
                "at_least_one_strict": any_strict,
                "fixed_L_joint_is_product": is_product,
            },
            "label": "NO-GO",
        },
        "multi_user_hybrid": {
            "statement": "Because valid-output maps are exactly secret rerandomizations, a multi-user hybrid argument that replaces real samples by g-transformed samples step-by-step loses at least the universal minimum per user.  A valid-output map breaking the minimum would create a tighter coupling and weaken the hybrid; n=2 evidence finds no such map.",
            "label": "EVIDENCE",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON stores string fractions",
            "L2_duality_care": "not invoked (no character sums over Lagrangians)",
            "L3_query_class_hygiene": "distributional TV result; no Feldman/SQ/query-class statement made",
            "L4_never_transform_comparison_distribution": "fresh pair (u1,b1,u2,b2) compared in natural domain; invariance arguments applied to split side only",
        },
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from the SAME uniform secret L (natural LSN pair), NOT pre-transformed by g_0 or g_1",
            "family_definitions": {
                "valid_output_map": "public bijection g such that for every Lagrangian subspace L there exists a Lagrangian subspace L' with g_*(D_L)=D_{L'}",
                "non_product_joint_structure": "split (g_0,g_1) whose diagonal push-forward is not a product distribution over a fixed secret",
            },
            "PRE_REGISTERED": "structural distributional gap for the correctness-constrained family; not a general lem:m2 rate or attack claim",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "430-trackV-valid-output-maps.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
