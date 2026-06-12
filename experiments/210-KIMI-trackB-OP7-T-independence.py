#!/usr/bin/env python3
"""210 (Track B): OP7 T-independence theorem and exact f(n) for n=3,4.

Track-B question: is the statistical distance between the symplectic-orbit
"transformed pair" and a truly fresh independent pair independent of the public
symplectic map T?  If yes, compute the exact value f(n) at n=3,4.

We prove T-independence by a sample-space bijection (see the meta note), then
verify it computationally:
  * n=2: enumerate all 720 elements of Sp(4,F_2).
  * n=3: test several random elements of Sp(6,F_2).
  * n=4: report the closed-form value (direct enumeration is unnecessary because
    the closed form is proven).

The exact closed form for the standard LSN noise rate p=1/4 is
    f(n) = 1 - (p^2 + (1-p)^2) / 4^n = 1 - 5/(8 * 4^n).

Membership convention (Claude/192 bug fix): the fresh second sample is labelled
by the rerandomized secret T*L, i.e. 1_{T*L}(T u) = 1_L(u).

Interpretation guard (PRE-REGISTER):
  * Comparison distribution: two independent fresh samples from D_{S_1 L} and
    D_{S_2 L}, same noise rate p=1/4 (matched).
  * Scaling: structural result in the 2n-dimensional secret space; no fixed-m
    artifact.
  * Output SD: f(n) -> 1 as n grows, bounded far from 1/2.  This means the
    public symplectic orbit transformation does NOT create fresh samples.
"""
import argparse
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

# Allow the script to be run directly from experiments/ while importing the
# shared library package at the project root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n, symplectic_form_n


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
    """Generate a random element of Sp(2n,F_2) as a word of transvections.

    Each transvection rho_u(v) = v + omega(v,u) u is symplectic, and transvections
    generate the symplectic group, so a random word starting from the identity
    yields a symplectic matrix (not necessarily uniformly distributed, but
    sufficient to test T-independence).
    """
    N = 2 * n
    cols = [1 << i for i in range(N)]
    for _ in range(steps):
        u = rng.randint(1, (1 << N) - 1)
        for i in range(N):
            if symplectic_form_n(cols[i], u, n):
                cols[i] ^= u
    assert is_symplectic_matrix(tuple(cols), n)
    return tuple(cols)


def lagrangian_masks(n: int):
    """Return list of Lagrangian subspaces as integer membership bitmasks."""
    bases = enumerate_lagrangian_bases_n(n)
    masks = []
    for basis in bases:
        span = [0]
        for v in basis:
            span += [s ^ v for s in span]
        mask = 0
        for s in span:
            mask |= 1 << s
        masks.append(mask)
    return masks


def exact_sd_transformed_vs_fresh(
    n: int, T_cols: tuple[int, ...], p: Fraction = Fraction(1, 4)
) -> Fraction:
    """Exact SD between transformed pair and fresh pair for a fixed T.

    Transformed pair:   (u, 1_L(u)+e,  T u, 1_L(u)+e)   (same noise bit)
    Fresh pair:         (u, 1_L(u)+e1, v, 1_{T*L}(v)+e2) (independent noises)
    """
    N = 2 * n
    M = 1 << N
    pden = p.denominator
    pnum = p.numerator
    qnum = pden - pnum
    pe_num = {0: qnum, 1: pnum}

    masks = lagrangian_masks(n)
    N_L = len(masks)
    D_P = N_L * M * pden
    D_Q = N_L * M * M * pden * pden

    T_map = [apply_matrix_cols(T_cols, x) for x in range(M)]

    P_counts: dict[tuple[int, int, int, int], int] = {}
    Q_counts: dict[tuple[int, int, int, int], int] = {}

    for mask in masks:
        # membership bitmask of the rerandomized secret T*L
        TL_mask = 0
        m = mask
        while m:
            lsb = m & -m
            v = (lsb.bit_length() - 1)
            TL_mask |= 1 << T_map[v]
            m ^= lsb

        # Transformed distribution (deterministic second point, identical noise)
        for u in range(M):
            c1 = (mask >> u) & 1
            v = T_map[u]
            for b in (0, 1):
                e = b ^ c1
                key = (u, b, v, b)
                P_counts[key] = P_counts.get(key, 0) + pe_num[e]

        # Fresh distribution (independent points, independent noises, second secret T*L)
        for u in range(M):
            c1 = (mask >> u) & 1
            for v in range(M):
                c2 = (TL_mask >> v) & 1
                base_u0 = pe_num[0] if c1 == 0 else pe_num[1]
                base_u1 = pe_num[1] if c1 == 0 else pe_num[0]
                base_v0 = pe_num[0] if c2 == 0 else pe_num[1]
                base_v1 = pe_num[1] if c2 == 0 else pe_num[0]
                # four (b1,b2) combinations
                Q_counts[(u, 0, v, 0)] = Q_counts.get((u, 0, v, 0), 0) + base_u0 * base_v0
                Q_counts[(u, 0, v, 1)] = Q_counts.get((u, 0, v, 1), 0) + base_u0 * base_v1
                Q_counts[(u, 1, v, 0)] = Q_counts.get((u, 1, v, 0), 0) + base_u1 * base_v0
                Q_counts[(u, 1, v, 1)] = Q_counts.get((u, 1, v, 1), 0) + base_u1 * base_v1

    total_num = 0
    keys = set(P_counts.keys()) | set(Q_counts.keys())
    for k in keys:
        total_num += abs(P_counts.get(k, 0) * D_Q - Q_counts.get(k, 0) * D_P)
    return Fraction(total_num, 2 * D_P * D_Q)


def f_formula(n: int, p: Fraction = Fraction(1, 4)) -> Fraction:
    """Closed-form SD for T=I (hence for every T by T-independence)."""
    q = Fraction(1) - p
    M = 1 << (2 * n)  # 4^n
    return Fraction(1) - (p * p + q * q) / M


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--n3-random-count", type=int, default=5)
    p.add_argument("--seed", type=int, default=20260614)
    return p.parse_args()


def main():
    args = parse_args()
    p = Fraction(1, 4)

    # Closed-form values for the requested n.
    formula_values = {}
    for n in (2, 3, 4, 5, 6):
        formula_values[str(n)] = str(f_formula(n, p))

    # n=2: enumerate the full symplectic group.
    print("Enumerating Sp(4,F_2)...")
    sp4 = enumerate_sp4()
    print(f"  |Sp(4,F_2)| = {len(sp4)}")
    f2 = f_formula(2, p)
    n2_sds = [exact_sd_transformed_vs_fresh(2, T, p) for T in sp4]
    assert all(sd == f2 for sd in n2_sds)
    n2_evidence = {
        "num_symplectic": len(sp4),
        "formula_f2": str(f2),
        "all_equal_formula": True,
        "sample_sd": str(n2_sds[0]),
    }
    print(f"  n=2: all SD = {f2}")

    # n=3: test identity and random symplectic matrices.
    rng = random.Random(args.seed)
    f3 = f_formula(3, p)
    n3_tests = []
    test_Ts = [tuple(1 << i for i in range(6))]  # identity
    for idx in range(args.n3_random_count):
        test_Ts.append(random_symplectic_matrix(3, rng))
    for idx, T in enumerate(test_Ts):
        sd = exact_sd_transformed_vs_fresh(3, T, p)
        n3_tests.append({
            "index": idx,
            "is_identity": (T == tuple(1 << i for i in range(6))),
            "sd": str(sd),
            "equal_formula": (sd == f3),
        })
        print(f"  n=3 test {idx}: SD = {sd}, equals formula = {sd == f3}")
    assert all(t["equal_formula"] for t in n3_tests)

    # n=4: closed form only (direct enumeration is unnecessary because the
    # closed form is proven; it is also large).
    f4 = f_formula(4, p)

    result = {
        "track": "B",
        "experiment": 210,
        "noise_rate_p": str(p),
        "theorem": "T-independence of OP7 SD over Sp(2n,F_2)",
        "closed_form_f(n)": "1 - (p^2 + (1-p)^2) / 4^n",
        "closed_form_p_1_4": "1 - 5/(8 * 4^n)",
        "formula_values": formula_values,
        "requested": {
            "f(3)": str(f3),
            "f(4)": str(f4),
        },
        "n2_full_enumeration": n2_evidence,
        "n3_random_tests": n3_tests,
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from D_{S_1 L} and D_{S_2 L}, matched noise rate p=1/4",
            "scaling": "structural result in 2n-dimensional secret space; no fixed-m artifact",
            "output_sd": "f(n) -> 1, bounded away from 1/2; orbit transformation does not create fresh samples",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "210-trackB-OP7-T-independence.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
