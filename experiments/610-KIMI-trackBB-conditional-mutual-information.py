#!/usr/bin/env python3
"""610 (Track BB): exact conditional mutual information I(x;y|C) for lem:m2 reduction output.

Computes the decisive quantity from open:marginal-adaptive: the conditional mutual
information I(x;y|C) in bits, for the reduction output at n=2, small m, across
several marginal-uniform B families, and compares it to matched-rate LPN.

Families
--------
* uniform-B-per-A            : B ~ Unif(F_2^{m x 4}) drawn independently for each A.
* lambda-coupled rows        : with prob lambda all rows equal a uniform r;
                               with prob 1-lambda rows are i.i.d. uniform.
* lambda-column-pair-coupled : NEW family; with prob lambda columns satisfy
                               col0=col1=s, col2=col3=t (s,t uniform i.i.d.);
                               with prob 1-lambda rows are i.i.d. uniform.

All three families are marginal-uniform (each row of B is uniform over F_2^4),
so they respect the lem:m1 constraint.  lambda=0 in the latter two recovers the
uniform-B-per-A baseline.

Comparison distribution (L4)
----------------------------
Matched-rate LPN_{p_eff(n)} with p_eff(n) = (1 - (1-p)^{2n})/2, p=1/4.
For n=2 this is 175/512; for n=3 it is 3367/8192.  The LPN target is the
standard product distribution (C,x,y) with C uniform, x uniform, y=Cx+e',
e' ~ Ber(p_eff)^m.  It is never transformed.

Standing guards
---------------
L1 exact arithmetic: all probabilities are derived from integer counts and
    converted to floats only for the final logarithm; JSON stores string
    fractions for rational parameters and denominators.
L2 J-twist duality: output distribution inspected directly in the (C,y) pair
    space; no Fourier/J-twist dual rewriting is used.
L3 query-class hygiene: I(x;y|C) is the unrestricted information-theoretic
    ceiling; no Feldman/SQ/query-class inference is made.
L4 never transform the comparison distribution: P_lpn is the standard matched-rate
    LPN distribution over (C,y); no reweighting or conditioning is applied.

PRE-REGISTER interpretation guards
----------------------------------
* Quantity: conditional mutual information I(x;y|C) in bits.
* Comparison distribution: LPN_{p_eff(n)} matched rate, never transformed.
* Families: uniform-B-per-A, lambda-coupled rows, lambda-column-pair-coupled
  (new), all marginal-uniform.
* n-axis: n=2 fixed; one n=3 spot for the uniform-B-per-A baseline.
* m-axis: small m (1..8 for n=2, 2..4 for n=3 spot).
* CLOSURE-GRADE: fixed-n finite computations; any asymptotic extrapolation is
  explicitly labelled CONJECTURE/OPEN.
"""
import argparse
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import (
    apply_matrix,
    enumerate_lagrangian_bases,
    enumerate_lagrangian_bases_n,
)


# ---------------------------------------------------------------------------
# Helpers: exact probabilities and conditional mutual information
# ---------------------------------------------------------------------------

def p_eff(n: int, p: Fraction = Fraction(1, 4)) -> Fraction:
    """Matched per-coordinate output noise rate for ambient noise p."""
    return Fraction(1 - (Fraction(1) - p) ** (2 * n), 2)


def conditional_mi_bits(counts_by_x: list[list[int]], denom: int, m: int, n: int) -> float:
    """Compute I(x;y|C) in bits from integer counts P(x,C,y) = counts_by_x[x][key]/denom.

    key layout: (C_key << m) | y, where C_key encodes the m x n matrix C.
    """
    nx = 1 << n
    size = 1 << ((n + 1) * m)
    mask_y = (1 << m) - 1
    num_c = 1 << (n * m)

    # Convert integer counts to float probabilities once.
    inv_denom = 1.0 / float(denom)
    joint = [[0.0] * size for _ in range(nx)]
    p_c = [0.0] * num_c
    p_cx = [[0.0] * num_c for _ in range(nx)]
    p_cy = [[0.0] * (1 << m) for _ in range(num_c)]

    for x in range(nx):
        row = counts_by_x[x]
        jx = joint[x]
        pcx_x = p_cx[x]
        for key, cnt in enumerate(row):
            if cnt == 0:
                continue
            prob = cnt * inv_denom
            jx[key] = prob
            c_key = key >> m
            y = key & mask_y
            p_c[c_key] += prob
            pcx_x[c_key] += prob
            p_cy[c_key][y] += prob

    mi = 0.0
    for x in range(nx):
        jx = joint[x]
        pcx_x = p_cx[x]
        for key, prob in enumerate(jx):
            if prob == 0.0:
                continue
            c_key = key >> m
            y = key & mask_y
            denom_term = pcx_x[c_key] * p_cy[c_key][y]
            if denom_term == 0.0:
                continue
            mi += prob * math.log2(prob * p_c[c_key] / denom_term)
    return mi


# ---------------------------------------------------------------------------
# LPN matched-rate target: per-x counts
# ---------------------------------------------------------------------------

def lpn_counts_by_x(m: int, n: int, p: Fraction) -> tuple[list[list[int]], int]:
    """Integer counts for (x,C,y) under LPN_p.  Denominator = 2^{n(m+1)} * p.den^m."""
    nx = 1 << n
    size = 1 << ((n + 1) * m)
    counts = [[0] * size for _ in range(nx)]
    mask = (1 << m) - 1
    num_c = 1 << (n * m)
    D = p.denominator ** m

    # Precompute Cx for every C and x.
    cx = [[0] * num_c for _ in range(nx)]
    for C_key in range(num_c):
        tmp = C_key
        cols = [0] * n
        for j in range(n):
            cols[j] = tmp & mask
            tmp >>= m
        for x in range(nx):
            val = 0
            for j in range(n):
                if (x >> j) & 1:
                    val ^= cols[j]
            cx[x][C_key] = val

    for x in range(nx):
        row = counts[x]
        for C_key in range(num_c):
            cx_val = cx[x][C_key]
            for e in range(1 << m):
                w = e.bit_count()
                num = (p.numerator ** w) * ((p.denominator - p.numerator) ** (m - w))
                y = cx_val ^ e
                key = (C_key << m) | y
                row[key] += num

    denom = num_c * nx * D
    return counts, denom


# ---------------------------------------------------------------------------
# Reduction output: uniform-B-per-A, per-x counts (general n)
# ---------------------------------------------------------------------------

def uniform_B_per_A_counts_by_x(
    m: int, n: int, bases: list[tuple[int, ...]] | None = None
) -> tuple[list[list[int]], int]:
    """Exact integer counts P(x,C,y) when B ~ Unif(F_2^{m x 2n}) is drawn per A."""
    if bases is None:
        bases = enumerate_lagrangian_bases_n(n)
    nx = 1 << n
    dim = 2 * n
    size = 1 << ((n + 1) * m)
    counts = [[0] * size for _ in range(nx)]
    mask = (1 << m) - 1
    num_c = 1 << (n * m)

    # C columns per C_key.
    c_lists = [[0] * num_c for _ in range(n)]
    for C_key in range(num_c):
        tmp = C_key
        for j in range(n):
            c_lists[j][C_key] = tmp & mask
            tmp >>= m

    two_to_nm = 1 << (n * m)
    two_to_nminus1_m = 1 << ((n - 1) * m)
    total_error_weight = sum(
        3 ** (dim - e.bit_count()) for e in range(1 << dim)
    )

    for basis in bases:
        # span_map: vector in span(A) -> coefficient tuple over basis.
        span_map = {0: tuple([0] * n)}
        for s in range(1, nx):
            v = 0
            coeffs = [0] * n
            for j in range(n):
                if (s >> j) & 1:
                    v ^= basis[j]
                    coeffs[j] = 1
            span_map[v] = tuple(coeffs)

        for x in range(nx):
            a = 0
            for j in range(n):
                if (x >> j) & 1:
                    a ^= basis[j]
            case3_weight_sum = 0
            for e in range(1 << dim):
                w_e = 3 ** (dim - e.bit_count())
                v = a ^ e
                if v == 0:
                    add = w_e * two_to_nm
                    base_key = x
                    row = counts[base_key]
                    for C_key in range(num_c):
                        row[(C_key << m)] += add
                elif v in span_map:
                    coeffs = span_map[v]
                    add = w_e * two_to_nm
                    row = counts[x]
                    for C_key in range(num_c):
                        y = 0
                        for j in range(n):
                            if coeffs[j]:
                                y ^= c_lists[j][C_key]
                        row[(C_key << m) | y] += add
                else:
                    case3_weight_sum += w_e
            case3_add = case3_weight_sum * two_to_nminus1_m
            row = counts[x]
            for key in range(size):
                row[key] += case3_add

    denom = len(bases) * nx * total_error_weight * (1 << (2 * n * m))
    return counts, denom


# ---------------------------------------------------------------------------
# Lambda-coupled rows (n=2 only)
# ---------------------------------------------------------------------------

def constant_rows_B_counts_by_x(m: int, bases=None) -> tuple[list[list[int]], int]:
    """Counts P(x,C,y) when every row of B equals a common uniform r in F_2^4."""
    if bases is None:
        bases = enumerate_lagrangian_bases()
    nx = 1 << 2
    size = 1 << (3 * m)
    mask = (1 << m) - 1
    counts = [[0] * size for _ in range(nx)]

    for r in range(1 << 4):
        B_cols = [mask if ((r >> j) & 1) else 0 for j in range(4)]
        Bx = [apply_matrix(B_cols, v) & mask for v in range(1 << 4)]
        for a0, a1 in bases:
            c0 = Bx[a0]
            c1 = Bx[a1]
            C_key = (c0 << m) | c1
            for x in range(nx):
                a = 0
                if x & 1:
                    a ^= a0
                if x & 2:
                    a ^= a1
                for e in range(1 << 4):
                    v = a ^ e
                    y = Bx[v]
                    key = (C_key << m) | y
                    counts[x][key] += 3 ** (4 - e.bit_count())

    denom = (1 << 4) * len(bases) * nx * (1 << 4)
    return counts, denom


def lambda_coupled_counts_by_x(
    lam: Fraction,
    uniform_counts: list[list[int]],
    uniform_denom: int,
    constant_counts: list[list[int]],
    constant_denom: int,
) -> tuple[list[list[int]], int]:
    """Mixture (1-lam)*uniform + lam*constant-rows, exact integer counts per x."""
    if not (0 <= lam <= 1):
        raise ValueError("lam must be in [0,1]")
    nx = len(uniform_counts)
    scale = uniform_denom // constant_denom
    p = lam.numerator
    q = lam.denominator
    mixed = [
        [(q - p) * u + p * (c * scale) for u, c in zip(ux, cx)]
        for ux, cx in zip(uniform_counts, constant_counts)
    ]
    denom = q * uniform_denom
    return mixed, denom


# ---------------------------------------------------------------------------
# New family: lambda-column-pair-coupled (n=2 only)
# ---------------------------------------------------------------------------

def column_pair_coupled_B_counts_by_x(m: int, bases=None) -> tuple[list[list[int]], int]:
    """Counts P(x,C,y) when col0=col1=s, col2=col3=t with s,t uniform i.i.d."""
    if bases is None:
        bases = enumerate_lagrangian_bases()
    nx = 1 << 2
    size = 1 << (3 * m)
    mask = (1 << m) - 1
    counts = [[0] * size for _ in range(nx)]

    for s in range(1 << m):
        for t in range(1 << m):
            B_cols = [s, s, t, t]
            Bx = [apply_matrix(B_cols, v) & mask for v in range(1 << 4)]
            for a0, a1 in bases:
                c0 = Bx[a0]
                c1 = Bx[a1]
                C_key = (c0 << m) | c1
                for x in range(nx):
                    a = 0
                    if x & 1:
                        a ^= a0
                    if x & 2:
                        a ^= a1
                    for e in range(1 << 4):
                        v = a ^ e
                        y = Bx[v]
                        key = (C_key << m) | y
                        counts[x][key] += 3 ** (4 - e.bit_count())

    denom = (1 << (2 * m)) * len(bases) * nx * (1 << 4)
    return counts, denom


def column_pair_coupled_mix_counts_by_x(
    lam: Fraction,
    uniform_counts: list[list[int]],
    uniform_denom: int,
    coupled_counts: list[list[int]],
    coupled_denom: int,
) -> tuple[list[list[int]], int]:
    """Mixture (1-lam)*uniform + lam*column-pair-coupled, exact integer counts per x."""
    if not (0 <= lam <= 1):
        raise ValueError("lam must be in [0,1]")
    scale = uniform_denom // coupled_denom
    p = lam.numerator
    q = lam.denominator
    mixed = [
        [(q - p) * u + p * (c * scale) for u, c in zip(ux, cx)]
        for ux, cx in zip(uniform_counts, coupled_counts)
    ]
    denom = q * uniform_denom
    return mixed, denom


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_experiment(max_m_n2: int = 8, n3: bool = True, output_dir: Path | None = None):
    results = {
        "track": "BB",
        "experiment": 610,
        "quantity": "I(x;y|C) bits",
        "standing_guards": ["L1 exact arithmetic", "L2 J-twist duality", "L3 query-class hygiene", "L4 never transform LPN"],
        "n2": [],
    }
    if n3:
        results["n3_spot"] = []

    bases_n2 = enumerate_lagrangian_bases()
    lambda_values = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]

    # Precompute n=2 uniform-B-per-A counts for re-use in mixtures.
    print("Precomputing n=2 uniform-B-per-A per-x counts...", file=sys.stderr)
    uniform_n2_counts, uniform_n2_denom = uniform_B_per_A_counts_by_x(0, 2, bases_n2)
    # Note: m=0 placeholder; we will recompute per m.

    for m in range(1, max_m_n2 + 1):
        print(f"n=2, m={m}", file=sys.stderr)
        uniform_counts, uniform_denom = uniform_B_per_A_counts_by_x(m, 2, bases_n2)
        p2 = p_eff(2)
        lpn_counts, lpn_denom = lpn_counts_by_x(m, 2, p2)

        row = {
            "m": m,
            "p_eff_n2": str(p2),
            "uniform_B_per_A": {
                "I_bits": conditional_mi_bits(uniform_counts, uniform_denom, m, 2),
                "denom": str(uniform_denom),
            },
            "lpn_matched": {
                "I_bits": conditional_mi_bits(lpn_counts, lpn_denom, m, 2),
                "denom": str(lpn_denom),
            },
            "lambda_coupled_rows": [],
            "lambda_column_pair_coupled": [],
        }

        constant_counts, constant_denom = constant_rows_B_counts_by_x(m, bases_n2)
        for lam in lambda_values:
            mixed_counts, mixed_denom = lambda_coupled_counts_by_x(
                lam, uniform_counts, uniform_denom, constant_counts, constant_denom
            )
            row["lambda_coupled_rows"].append({
                "lambda": str(lam),
                "I_bits": conditional_mi_bits(mixed_counts, mixed_denom, m, 2),
            })

        coupled_counts, coupled_denom = column_pair_coupled_B_counts_by_x(m, bases_n2)
        for lam in lambda_values:
            mixed_counts, mixed_denom = column_pair_coupled_mix_counts_by_x(
                lam, uniform_counts, uniform_denom, coupled_counts, coupled_denom
            )
            row["lambda_column_pair_coupled"].append({
                "lambda": str(lam),
                "I_bits": conditional_mi_bits(mixed_counts, mixed_denom, m, 2),
            })

        results["n2"].append(row)

    if n3:
        bases_n3 = enumerate_lagrangian_bases_n(3)
        p3 = p_eff(3)
        for m in range(2, 5):
            print(f"n=3 spot, m={m}", file=sys.stderr)
            uniform_counts, uniform_denom = uniform_B_per_A_counts_by_x(m, 3, bases_n3)
            lpn_counts, lpn_denom = lpn_counts_by_x(m, 3, p3)
            results["n3_spot"].append({
                "m": m,
                "p_eff_n3": str(p3),
                "uniform_B_per_A": {
                    "I_bits": conditional_mi_bits(uniform_counts, uniform_denom, m, 3),
                    "denom": str(uniform_denom),
                },
                "lpn_matched": {
                    "I_bits": conditional_mi_bits(lpn_counts, lpn_denom, m, 3),
                    "denom": str(lpn_denom),
                },
            })

    if output_dir is None:
        output_dir = Path("experiments/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"610-trackBB-conditional-mutual-information-maxM{max_m_n2}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)
    return results


def main():
    parser = argparse.ArgumentParser(description="Track BB: exact I(x;y|C)")
    parser.add_argument("--max-m", type=int, default=8, help="max m for n=2")
    parser.add_argument("--no-n3", action="store_true", help="skip n=3 spot")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    results = run_experiment(max_m_n2=args.max_m, n3=not args.no_n3, output_dir=args.output_dir)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
