#!/usr/bin/env python3
"""192: OP7 n=2 exact SD for symplectic-orbit sample freshness.

OP7 asks whether a public symplectic transformation can produce fresh
independent samples for a rerandomized secret.  For n=2 we compute the exact
total-variation distance between:

  (i) the transformed distribution: one sample (x,b) from D_L is mapped by two
      public symplectic matrices S_1, S_2 to two samples (S_1 x, b), (S_2 x, b)
      for the rerandomized secrets S_1 L and S_2 L;

 (ii) the fresh distribution: two independent samples from D_{S_1 L} and
      D_{S_2 L}.

The SD depends only on T = S_1^{-1} S_2.  We enumerate all T in Sp(4, F_2) and
report the exact minimum, maximum, and mean.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path


def symplectic_form(u: int, v: int) -> int:
    return (
        ((u >> 0) & 1) * ((v >> 2) & 1)
        ^ ((u >> 1) & 1) * ((v >> 3) & 1)
        ^ ((u >> 2) & 1) * ((v >> 0) & 1)
        ^ ((u >> 3) & 1) * ((v >> 1) & 1)
    ) & 1


def matrix_from_cols(cols: tuple[int, ...]) -> tuple[int, ...]:
    rows = [0] * 4
    for j in range(4):
        col = cols[j]
        for i in range(4):
            if (col >> i) & 1:
                rows[i] |= 1 << j
    return tuple(rows)


def det(cols: tuple[int, ...]) -> int:
    rows = matrix_from_cols(cols)
    pivots = {}
    for r in rows:
        x = r
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return 1 if len(pivots) == 4 else 0


def is_symplectic(cols: tuple[int, ...]) -> bool:
    for i in range(4):
        for j in range(4):
            if symplectic_form(cols[i], cols[j]) != symplectic_form(1 << i, 1 << j):
                return False
    return True


def enumerate_sp4() -> list[tuple[int, ...]]:
    sp = []
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


def matvec(M_cols: tuple[int, ...], x: int) -> int:
    y = 0
    for i in range(4):
        if (x >> i) & 1:
            y ^= M_cols[i]
    return y


def enumerate_lagrangian_subspaces() -> list[frozenset[int]]:
    subspaces = []
    seen = set()
    for v1 in range(1, 1 << 4):
        for v2 in range(v1 + 1, 1 << 4):
            if symplectic_form(v1, v2) != 0:
                continue
            span = {0, v1, v2, v1 ^ v2}
            key = tuple(sorted(span))
            if key in seen:
                continue
            seen.add(key)
            subspaces.append(frozenset(span))
    return subspaces


def exact_sd_for_T(
    L_list: list[frozenset[int]], T_cols: tuple[int, ...], p: Fraction
) -> Fraction:
    """Exact SD between transformed and fresh distributions for a fixed T."""
    pnum, pden = p.numerator, p.denominator
    N_L = len(L_list)
    N_x = 1 << 4
    D_fresh = N_L * N_x * N_x * pden * pden
    D_trans = N_L * N_x * pden
    scale = D_fresh // D_trans

    fresh_match = [[0] * 2 for _ in range(N_x)]
    trans_scaled = [[0] * 2 for _ in range(N_x)]

    for L in L_list:
        mask = 0
        for x in L:
            mask |= 1 << x
        for u in range(N_x):
            in_u = (mask >> u) & 1
            v = matvec(T_cols, u)
            in_v = (mask >> v) & 1
            for b in range(2):
                w_u = (pden - pnum) if (in_u == b) else pnum
                w_v = (pden - pnum) if (in_v == b) else pnum
                trans_scaled[u][b] += w_u
                fresh_match[u][b] += w_u * w_v

    fresh_mass = sum(fresh_match[u][b] for u in range(N_x) for b in range(2))
    total = D_fresh - fresh_mass
    for u in range(N_x):
        for b in range(2):
            total += abs(scale * trans_scaled[u][b] - fresh_match[u][b])

    return Fraction(total, 2 * D_fresh)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    p = Fraction(1, 4)

    sp4 = enumerate_sp4()
    L_list = enumerate_lagrangian_subspaces()

    sds = [exact_sd_for_T(L_list, T, p) for T in sp4]
    sds.sort()

    result = {
        "n": 2,
        "p": str(p),
        "num_symplectic": len(sp4),
        "num_lagrangian": len(L_list),
        "min_sd": str(sds[0]),
        "min_sd_float": float(sds[0]),
        "max_sd": str(sds[-1]),
        "max_sd_float": float(sds[-1]),
        "mean_sd": str(sum(sds, Fraction(0)) / len(sds)),
        "mean_sd_float": float(sum(sds, Fraction(0)) / len(sds)),
        "median_sd": str(sds[len(sds) // 2]),
        "median_sd_float": float(sds[len(sds) // 2]),
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "192-op7-n2-exact-SD.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
