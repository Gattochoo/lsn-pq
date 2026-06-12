#!/usr/bin/env python3
"""183: OP7 sample freshness -- symplectic-orbit transformation for n=2.

Tests whether applying public symplectic matrices S_1, S_2 to one sample
(x, b) can produce two samples close to independent fresh samples from
D_{S_i * L}.

Run: python3 experiments/183-KIMI-OP7-symplectic-orbit-freshness.py
"""
from collections import Counter
from itertools import product
import json
import math
from pathlib import Path


def popcount(x):
    return bin(x).count("1")


def symplectic_form(u, v):
    """Standard symplectic form on F_2^4: omega(u,v)."""
    # basis: e1,e2,f1,f2 with omega(ei,ej)=omega(fi,fj)=0, omega(ei,fj)=delta_ij
    # represent u = (u0,u1,u2,u3) as u0*e1 + u1*e2 + u2*f1 + u3*f2
    return (
        ((u >> 0) & 1) * ((v >> 2) & 1)
        ^ ((u >> 1) & 1) * ((v >> 3) & 1)
        ^ ((u >> 2) & 1) * ((v >> 0) & 1)
        ^ ((u >> 3) & 1) * ((v >> 1) & 1)
    ) & 1


def matvec(M_cols, x):
    """M * x where M is given by list of 4 column vectors."""
    y = 0
    for i in range(4):
        if (x >> i) & 1:
            y ^= M_cols[i]
    return y


def matrix_from_cols(M_cols):
    """Convert column representation to row-bit representation."""
    rows = [0] * 4
    for j in range(4):
        col = M_cols[j]
        for i in range(4):
            if (col >> i) & 1:
                rows[i] |= 1 << j
    return tuple(rows)


def det(M_cols):
    """Determinant of 4x4 matrix over F_2 (column representation)."""
    rows = matrix_from_cols(M_cols)
    # Gaussian elimination
    pivots = {}
    for r in rows:
        x = r
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return 1 if len(pivots) == 4 else 0


def is_symplectic(M_cols):
    """Check M preserves symplectic form: omega(Mu, Mv) = omega(u,v)."""
    # It suffices to check on basis pairs.
    for i in range(4):
        for j in range(4):
            if symplectic_form(M_cols[i], M_cols[j]) != symplectic_form(1 << i, 1 << j):
                return False
    return True


def enumerate_sp4():
    """Enumerate Sp(4, F_2)."""
    sp = []
    # Generate all 4x4 matrices by choosing columns.
    # First column: any non-zero vector (15 choices)
    # But faster: brute force over all 2^16 matrices and filter.
    for bits in range(1 << 16):
        cols = []
        for j in range(4):
            col = 0
            for i in range(4):
                if (bits >> (j * 4 + i)) & 1:
                    col |= 1 << i
            cols.append(col)
        if det(cols) and is_symplectic(cols):
            sp.append(tuple(cols))
    return sp


def enumerate_lagrangian_subspaces():
    """Enumerate all Lagrangian subspaces of F_2^4 as sets of vectors."""
    # A Lagrangian is a 2-dim isotropic subspace.
    subspaces = []
    seen = set()
    # Enumerate ordered bases (v1, v2) with omega(v1,v2)=0 and v1,v2 independent.
    for v1 in range(1, 1 << 4):
        for v2 in range(v1 + 1, 1 << 4):
            if symplectic_form(v1, v2) != 0:
                continue
            # check independence
            if v2 == v1:
                continue
            # span
            span = {0, v1, v2, v1 ^ v2}
            key = tuple(sorted(span))
            if key in seen:
                continue
            seen.add(key)
            subspaces.append(frozenset(span))
    return subspaces


def indicator(L_set):
    """Return dict x -> 1_L(x)."""
    return {x: 1 if x in L_set else 0 for x in range(1 << 4)}


def apply_S_to_L(L_set, S_cols):
    """S * L = {S v : v in L}."""
    return frozenset(matvec(S_cols, v) for v in L_set)


def compute_SD_for_S_pair(L_list, ind_list, S1_cols, S2_cols, p=0.25):
    """
    L_list: list of Lagrangian subspaces (frozensets).
    ind_list: list of indicator dicts for L_list.
    S1_cols, S2_cols: symplectic matrices (column representation).
    Returns SD between transformed output and independent fresh samples.
    """
    # Precompute transformed Lagrangians and indicators
    L1_list = [apply_S_to_L(L, S1_cols) for L in L_list]
    L2_list = [apply_S_to_L(L, S2_cols) for L in L_list]
    ind1_list = [indicator(L) for L in L1_list]
    ind2_list = [indicator(L) for L in L2_list]

    P_trans = Counter()  # transformed distribution
    P_fresh = Counter()  # fresh independent distribution

    num_L = len(L_list)
    p_L = 1.0 / num_L

    for idx, L in enumerate(L_list):
        ind = ind_list[idx]
        ind1 = ind1_list[idx]
        ind2 = ind2_list[idx]

        for x in range(1 << 4):
            for e in range(2):
                p_x = 1.0 / 16
                p_e = p if e == 1 else (1 - p)
                b = ind[x] ^ e

                x1 = matvec(S1_cols, x)
                x2 = matvec(S2_cols, x)

                trans_key = (x1, b, x2, b)
                P_trans[trans_key] += p_L * p_x * p_e

                # Fresh samples: independent x1, x2 and independent noise
                for x1_f in range(1 << 4):
                    for e1_f in range(2):
                        p_x1 = 1.0 / 16
                        p_e1 = p if e1_f == 1 else (1 - p)
                        b1_f = ind1[x1_f] ^ e1_f
                        for x2_f in range(1 << 4):
                            for e2_f in range(2):
                                p_x2 = 1.0 / 16
                                p_e2 = p if e2_f == 1 else (1 - p)
                                b2_f = ind2[x2_f] ^ e2_f
                                fresh_key = (x1_f, b1_f, x2_f, b2_f)
                                P_fresh[fresh_key] += (
                                    p_L * p_x * p_e * p_x1 * p_e1 * p_x2 * p_e2
                                )

    keys = set(P_trans.keys()) | set(P_fresh.keys())
    sd = 0.0
    for key in keys:
        sd += abs(P_trans.get(key, 0.0) - P_fresh.get(key, 0.0))
    return 0.5 * sd


def main():
    print("Enumerating Sp(4, F_2)...")
    sp4 = enumerate_sp4()
    print(f"  |Sp(4,F2)| = {len(sp4)}")

    print("Enumerating Lagrangian subspaces...")
    L_list = enumerate_lagrangian_subspaces()
    print(f"  |Lagr(4,F2)| = {len(L_list)}")
    ind_list = [indicator(L) for L in L_list]

    # For efficiency, sample random S pairs rather than all pairs.
    import random
    rng = random.Random(42)
    num_pairs = 200
    results = []
    best_sd = 2.0
    best_pair = None

    print(f"Testing {num_pairs} random symplectic pairs...")
    for trial in range(num_pairs):
        S1 = rng.choice(sp4)
        S2 = rng.choice(sp4)
        sd = compute_SD_for_S_pair(L_list, ind_list, S1, S2)
        results.append(sd)
        if sd < best_sd:
            best_sd = sd
            best_pair = (S1, S2)
        if trial % 50 == 0:
            print(f"  ...trial {trial}, best SD={best_sd:.6f}")

    print(f"\nBest SD over {num_pairs} pairs: {best_sd:.6f}")
    print(f"Mean SD: {sum(results)/len(results):.6f}")
    print(f"Min SD: {min(results):.6f}")
    print(f"Max SD: {max(results):.6f}")

    out_dir = Path("experiments/output")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "183-op7-symplectic-orbit-freshness.json"
    with open(out_file, "w") as f:
        json.dump(
            {
                "n": 2,
                "num_S": len(sp4),
                "num_L": len(L_list),
                "num_pairs": num_pairs,
                "best_SD": best_sd,
                "mean_SD": sum(results) / len(results),
                "min_SD": min(results),
                "max_SD": max(results),
            },
            f,
            indent=2,
        )
    print(f"\nResults saved to {out_file}")


if __name__ == "__main__":
    main()
