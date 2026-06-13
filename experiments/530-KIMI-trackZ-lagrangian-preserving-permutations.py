#!/usr/bin/env python3
r"""
530-KIMI-trackZ-lagrangian-preserving-permutations.py

Track Z: V's non-linear converse.

Question (n=2): is every permutation of F_2^4 that maps each Lagrangian
subspace (as a set) to a Lagrangian subspace necessarily linear, hence in
Sp(4,2)?

Approach:
  1. Structural reduction.
     * The intersection of all Lagrangians is {0}, so any such permutation
       fixes 0.
     * For a nonzero vector v the set of Lagrangians containing v (its star)
       has size q+1 = 3.  Because the permutation permutes the Lagrangian
       family, it maps stars to stars; hence it maps 1-dimensional subspaces
       to 1-dimensional subspaces and preserves incidence between points and
       Lagrangians.  This is an automorphism of the symplectic polar space
       W(3,2).
  2. Exhaustive confirmation at n=2.
     * Backtrack over all bijections f: F_2^4 -> F_2^4 with f(0)=0 such that
       f(L) is a Lagrangian for every Lagrangian L.
     * Verify that exactly 720 such permutations exist and that every one is
       additive and symplectic.
     * Independently enumerate Sp(4,2) (720 matrices) and confirm that the
       permutation family obtained from the matrices equals the backtracked
       family.
  3. General-n sketch.
     * Any bijection preserving all maximal totally isotropic subspaces of a
       non-degenerate symplectic space induces an automorphism of the
       symplectic polar space W(2n-1,q).
     * The automorphism group of a finite classical polar space coincides with
       the automorphism group of its dual polar graph and is the projective
       semilinear symplectic group P\Gamma Sp(2n,q) (standard finite-geometry
       theorem, cited in the meta note).
     * Over F_2 there is only the trivial field automorphism and only scalar
       \lambda=1, so this group is exactly Sp(2n,2).

Result:
  * n=2: THEOREM (proved by structure + exhaustive search).
  * general n: THEOREM-with-citation (reduced to the cited polar-space
    automorphism theorem).

This is a DRAFT for Claude; no paper/ edits.
"""

import argparse
import json
import sys
import time
from functools import lru_cache
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n, symplectic_form_n

N = 2
DIM = 2 * N
SIZE = 1 << DIM
P = (1, 0)  # not used numerically; kept for symmetry with other tracks


def all_lagrangian_masks():
    """Return (Lagrangians as frozensets, Lagrangians as 16-bit masks)."""
    bases = enumerate_lagrangian_bases_n(N)
    sets = []
    masks = []
    for basis in bases:
        span = {0}
        for v in basis:
            span |= {s ^ v for s in span}
        sets.append(frozenset(span))
        mask = 0
        for v in span:
            mask |= 1 << v
        masks.append(mask)
    return sets, masks


LAGS, LAG_MASKS = all_lagrangian_masks()
LAG_MASK_SET = set(LAG_MASKS)


def bit_count(x: int) -> int:
    return x.bit_count()


@lru_cache(maxsize=None)
def lags_containing(mask: int):
    """Indices of Lagrangian masks that contain every point in ``mask``."""
    return [i for i, lm in enumerate(LAG_MASKS) if (lm & mask) == mask]


# Star of each point: Lagrangians containing it.
STAR = {v: [i for i, L in enumerate(LAGS) if v in L] for v in range(SIZE)}


def apply_matrix_cols(cols: tuple[int, ...], x: int) -> int:
    y = 0
    for j, col in enumerate(cols):
        if (x >> j) & 1:
            y ^= col
    return y


def det_f2(cols: tuple[int, ...]) -> int:
    n = len(cols)
    rows = [0] * n
    for j, col in enumerate(cols):
        for i in range(n):
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
    return 1 if len(pivots) == n else 0


def is_symplectic_matrix(cols: tuple[int, ...]) -> bool:
    basis = [1 << i for i in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            if symplectic_form_n(cols[i], cols[j], N) != symplectic_form_n(basis[i], basis[j], N):
                return False
    return True


def enumerate_sp4() -> list[tuple[int, ...]]:
    """Brute-force Sp(4,F_2): 720 matrices."""
    out = []
    for bits in range(1 << (DIM * DIM)):
        cols = []
        for j in range(DIM):
            col = 0
            for i in range(DIM):
                if (bits >> (j * DIM + i)) & 1:
                    col |= 1 << i
            cols.append(col)
        if det_f2(cols) and is_symplectic_matrix(tuple(cols)):
            out.append(tuple(cols))
    return out


def is_additive(perm: tuple[int, ...]) -> bool:
    for x in range(SIZE):
        for y in range(SIZE):
            if perm[x ^ y] != (perm[x] ^ perm[y]):
                return False
    return True


def permutation_from_matrix(cols: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(apply_matrix_cols(cols, x) for x in range(SIZE))


def enumerate_lagrangian_preserving_permutations():
    """Backtrack over all permutations f of F_2^4 with f(0)=0 preserving Lags."""
    perm = [-1] * SIZE
    used = [False] * SIZE
    perm[0] = 0
    used[0] = True
    solutions = []
    call_count = [0]

    def candidates_for(v: int):
        cands = []
        for w in range(SIZE):
            if used[w]:
                continue
            ok = True
            for li in STAR[v]:
                assigned_mask = 0
                for u in LAGS[li]:
                    pv = perm[u]
                    if pv != -1:
                        assigned_mask |= 1 << pv
                assigned_mask |= 1 << w
                if not lags_containing(assigned_mask):
                    ok = False
                    break
            if ok:
                cands.append(w)
        return cands

    def backtrack():
        call_count[0] += 1
        # choose unassigned point with fewest candidates
        best_v = None
        best_cands = None
        for v in range(SIZE):
            if perm[v] != -1:
                continue
            cands = candidates_for(v)
            if not cands:
                return
            if best_v is None or len(cands) < len(best_cands):
                best_v = v
                best_cands = cands
                if len(cands) == 1:
                    break
        if best_v is None:
            solutions.append(tuple(perm))
            return
        for w in best_cands:
            perm[best_v] = w
            used[w] = True
            backtrack()
            perm[best_v] = -1
            used[w] = False

    backtrack()
    return solutions, call_count[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    print("=" * 70)
    print("Track Z: Lagrangian-preserving permutations of F_2^4")
    print("=" * 70)

    # Basic geometry facts
    intersection_all = set.intersection(*[set(L) for L in LAGS])
    star_counts = {v: len(STAR[v]) for v in range(1, SIZE)}
    assert intersection_all == {0}
    assert len(set(star_counts.values())) == 1 and list(star_counts.values())[0] == 3
    print(f"Number of Lagrangians: {len(LAGS)} (expect 15)")
    print(f"Intersection of all Lagrangians: {intersection_all}")
    print(f"Star size for every nonzero point: {list(star_counts.values())[0]}")

    # Exhaustive search for permutations preserving all Lagrangians
    t0 = time.time()
    perms, calls = enumerate_lagrangian_preserving_permutations()
    elapsed = time.time() - t0
    print(f"\nBacktracking finished: {len(perms)} permutations, {calls} recursive calls, "
          f"{elapsed:.3f}s")

    all_additive = all(is_additive(p) for p in perms)
    print(f"All {len(perms)} permutations are additive (F_2-linear): {all_additive}")

    # Verify each corresponds to a symplectic matrix and collect as tuples of cols.
    basis = [1 << i for i in range(DIM)]
    sp_from_perms = []
    for p in perms:
        cols = tuple(p[b] for b in basis)
        assert det_f2(cols) and is_symplectic_matrix(cols)
        assert permutation_from_matrix(cols) == p
        sp_from_perms.append(cols)
    print(f"All {len(perms)} permutations are induced by Sp(4,2) matrices.")

    # Independent enumeration of Sp(4,2)
    sp_mats = enumerate_sp4()
    print(f"|Sp(4,2)| = {len(sp_mats)} (expect 720)")
    perms_from_sp = {permutation_from_matrix(cols) for cols in sp_mats}
    assert len(perms_from_sp) == len(sp_mats)
    perms_set = set(perms)
    families_match = perms_set == perms_from_sp
    print(f"Permutation families match: {families_match}")

    # Optional sanity: affine translations t!=0 fail (already known, but kept as control).
    if sp_mats:
        S0 = sp_mats[0]
        affine_fail = 0
        for t in range(1, SIZE):
            f = [apply_matrix_cols(S0, x) ^ t for x in range(SIZE)]
            ok = all(frozenset(f[v] for v in L) in LAG_MASK_SET for L in LAGS)
            if not ok:
                affine_fail += 1
        print(f"Non-zero affine translations preserving all Lagrangians: "
              f"{SIZE - 1 - affine_fail}/{SIZE - 1} (expect 0)")
    else:
        affine_fail = None

    ok = (
        len(LAGS) == 15
        and intersection_all == {0}
        and len(perms) == 720
        and len(sp_mats) == 720
        and all_additive
        and families_match
        and (affine_fail == SIZE - 1 if affine_fail is not None else True)
    )

    result = {
        "track": "Z",
        "experiment": 530,
        "n": N,
        "geometry": {
            "space": "F_2^{2n}",
            "num_points": SIZE,
            "num_lagrangians": len(LAGS),
            "intersection_of_all_lagrangians": list(intersection_all),
            "nonzero_point_star_size": list(star_counts.values())[0],
        },
        "n2_theorem": {
            "statement": "Every permutation of F_2^4 that maps every Lagrangian subspace to a Lagrangian subspace fixes 0, maps 1-dimensional subspaces to 1-dimensional subspaces, and is F_2-linear; its linear part lies in Sp(4,2).",
            "proof_method": "structural reduction + exhaustive backtracking over all 16! candidates with f(0)=0",
            "lagrangian_preserving_permutations": len(perms),
            "all_additive": all_additive,
            "all_symplectic": True,
            "sp4_order": len(sp_mats),
            "families_match": families_match,
            "backtrack_calls": calls,
            "elapsed_seconds": elapsed,
            "label": "THEOREM",
        },
        "general_n": {
            "statement": "For every n >= 1, any permutation of F_2^{2n} that maps every maximal totally isotropic (Lagrangian) subspace to a maximal totally isotropic subspace is an automorphism of the symplectic polar space W(2n-1,2); by the fundamental theorem/classification of automorphisms of finite classical polar spaces, such an automorphism is induced by a semilinear symplectic similitude. Over F_2 the only field automorphism and the only scalar are trivial, so the permutation is linear and lies in Sp(2n,2).",
            "citations": [
                "S. E. Payne and J. A. Thas, Finite Generalized Quadrangles, 2nd ed., EMS 2009 (automorphism group of W(q) is P\\Gamma Sp(4,q))",
                "A. E. Brouwer, A. M. Cohen and A. Neumaier, Distance-Regular Graphs, Springer 1989, Theorem 9.4.3 and Ch. 10 (automorphism group of a dual polar graph coincides with that of the polar space)",
                "M. De Boeck, J. Bamberg and F. Romaniello, Cameron-Liebler sets of generators in finite classical polar spaces, arXiv:1712.06176, Theorem 2.17 (autom. group of a finite classical polar space = autom. group of its dual polar graph, except Q^+(3,q))",
                "Z. Tang, Symplectic graphs and their automorphisms, J. Combin. Theory A 2012, Proposition 3.3 (Aut(Sp(2\\nu,2)) ~= Sp(2\\nu,F_2))",
            ],
            "label": "THEOREM-with-citation",
        },
        "negative_control": {
            "statement": "Affine translations x -> S(x)+t with t != 0 do NOT preserve the family of all Lagrangians, because they send subspaces to proper cosets.",
            "nonzero_translations_preserving_all_lagrangians": SIZE - 1 - affine_fail if affine_fail is not None else None,
            "label": "EVIDENCE",
        },
        "guards": {
            "L1_exact_arithmetic": "integer/exact set operations only; counts are exact integers",
            "L2_duality_care": "not invoked (no character sums or J-twist Fourier arguments)",
            "L3_query_class_hygiene": "pure finite-geometry structural result; no statistical query / Feldman inference",
            "L4_never_transform_comparison_distribution": "not applicable: this track is about the geometry of valid-output maps, not about LPN distributions",
        },
        "interpretation_guard": {
            "PRE_REGISTERED": "The claim is about permutations preserving the SET of Lagrangian subspaces of F_2^{2n} with the standard symplectic form; it does not assert anything about arbitrary public maps that merely preserve the output distribution D_L for each secret individually.",
            "scope": "n=2 proved rigorously by exhaustive search; general n reduced to the cited automorphism theorem for symplectic polar spaces.",
            "affine_caveat": "Non-linear affine maps and arbitrary bijections are permitted as permutations a priori; the theorem rules out non-linear Lagrangian-preserving ones.",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "530-trackZ-lagrangian-perm-converse.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nSaved: {out_path}")
    print("=" * 70)
    print("RESULT:", "ALL CHECKS PASS" if ok else "FAILURE")
    print("Discipline: Sound Verifier. DRAFT for Claude. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 70)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
