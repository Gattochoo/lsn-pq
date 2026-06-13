#!/usr/bin/env python3
"""510 (Track X): exact SD for a correlated randomized marginal-adaptive B family.

Defines a one-parameter family of marginal-uniform but row-correlated matrices:

    B ~ LambdaCoupled(lambda) :
      with probability lambda, all m rows equal a common uniform r ~ U(F_2^4);
      with probability 1 - lambda, the rows are i.i.d. uniform over F_2^4.

Every row is marginally uniform, so the lem:m1 marginal-uniform constraint is
respected, but the joint distribution is non-product for lambda != 0.  Pairwise
row correlation under any nonzero linear functional is exactly lambda.

For n = 2 and small m we compute the exact total-variation distance
SD(P_out(lambda), P_lpn) against two native LPN targets:

  * LPN_{1/4}      : the ambient Bernoulli(1/4) noise rate.
  * LPN_{p_eff}    : the matched per-coordinate output rate
                     p_eff(2) = (1 - (3/4)^4) / 2 = 175/512.

The uniform-B-per-A baseline corresponds to lambda = 0.

Standing guards
---------------
L1 exact arithmetic: all probabilities are Fractions; JSON stores string fractions.
L2 J-twist duality: the output distribution is inspected directly in the (C, y)
    pair space; no Fourier/J-twist dual rewriting is used.
L3 query-class hygiene: only exact total-variation (unrestricted distinguisher)
    is reported; no Feldman/SQ/query-class inference is made.
L4 never transform the comparison distribution: P_lpn is the standard LPN_p
    distribution over (C, y) for the chosen p; no reweighting or conditioning.

PRE-REGISTER interpretation guards
----------------------------------
* Comparison distributions: standard LPN_{1/4} and matched-rate LPN_{175/512}
  on F_2^{m x 2} x F_2^m.
* Family: lambda-coupled marginal-uniform B distribution defined above.
* n-axis: fixed n = 2 (the exact-computation regime).
* m-axis: small m = 1, ..., MAX_M; no asymptotic extrapolation is claimed.
* Negative result: if every sampled lambda >= 0 has SD >= the lambda = 0 baseline,
  this is reported as a NEGATIVE/partial result, not a general lem:m2 theorem.
"""
import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import (
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    randomized_uniform_B_counts,
    reduction_counts_for_B,
)


def p_eff_n2() -> Fraction:
    """Matched per-coordinate output noise rate for uniform B at n = 2."""
    return Fraction(1 - Fraction(3, 4) ** 4, 2)


def constant_rows_equal_B_counts(m: int, bases):
    """Integer counts for (C, y) when all m rows of B equal a uniform r in F_2^4.

    The matrix space has size 16 (one for each r).  We simply call the fixed-B
    exact enumerator for each constant matrix and accumulate.
    """
    mask = (1 << m) - 1
    B_const = lambda r: [mask if ((r >> j) & 1) else 0 for j in range(4)]
    total = None
    for r in range(1 << 4):
        counts = reduction_counts_for_B(B_const(r), bases, m)
        if total is None:
            total = counts
        else:
            for i, c in enumerate(counts):
                total[i] += c
    denom = 16 * 15360  # 16 matrices x (15 bases * 4 x * 256 e-mass)
    return total, denom


def lambda_coupled_counts(
    lam: Fraction,
    uniform_counts: list[int],
    uniform_denom: int,
    constant_counts: list[int],
    constant_denom: int,
) -> tuple[list[int], int]:
    """Exact integer counts for the lambda-coupled mixture.

    P_out = (1-lam) * P_uniform_B  +  lam * P_all-rows-equal.

    Both components are represented on the common denominator uniform_denom.
    """
    if not (0 <= lam <= 1):
        raise ValueError("lam must be in [0, 1]")
    scale = uniform_denom // constant_denom  # = 2^{4m-4}
    p = lam.numerator
    q = lam.denominator
    mixed = [
        (q - p) * u + p * (c * scale)
        for u, c in zip(uniform_counts, constant_counts)
    ]
    denom = q * uniform_denom
    return mixed, denom


def table_for_p(
    m: int,
    p: Fraction,
    lambda_values: list[Fraction],
    uniform_counts: list[int],
    uniform_denom: int,
    constant_counts: list[int],
    constant_denom: int,
) -> dict:
    """Compute the exact SD table for one LPN noise rate p."""
    lpn_counts, lpn_denom = lpn_target_counts(m, p)
    baseline_sd = None
    rows = []
    for lam in lambda_values:
        mixed_counts, mixed_denom = lambda_coupled_counts(
            lam,
            uniform_counts, uniform_denom,
            constant_counts, constant_denom,
        )
        sd = exact_sd_counts(mixed_counts, mixed_denom, lpn_counts, lpn_denom)
        if lam == 0:
            baseline_sd = sd
        rows.append({
            "lambda": str(lam),
            "sd": str(sd),
            "sd_float": float(sd),
            "one_minus_sd": str(Fraction(1) - sd),
            "one_minus_sd_float": float(Fraction(1) - sd),
        })

    for row in rows:
        delta = Fraction(row["sd"]) - baseline_sd
        row["delta_sd_vs_baseline"] = str(delta)
        row["delta_sd_vs_baseline_float"] = float(delta)

    min_row = min(rows, key=lambda r: Fraction(r["sd"]))
    sd_values = [Fraction(r["sd"]) for r in rows]
    monotone_non_decreasing = all(
        sd_values[i] <= sd_values[i + 1] for i in range(len(sd_values) - 1)
    )
    return {
        "m": m,
        "p": str(p),
        "baseline_sd": str(baseline_sd),
        "baseline_sd_float": float(baseline_sd),
        "lambda_rows": rows,
        "min_sd_lambda": min_row["lambda"],
        "min_sd": min_row["sd"],
        "min_sd_float": min_row["sd_float"],
        "sd_monotone_non_decreasing_in_lambda": monotone_non_decreasing,
    }


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--max-m", type=int, default=6, help="maximum m to compute")
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    max_m = args.max_m
    if not 1 <= max_m <= 6:
        raise ValueError("this experiment supports 1 <= max-m <= 6")

    bases = list(enumerate_lagrangian_bases())
    p_values = [Fraction(1, 4), p_eff_n2()]
    lambda_values = [Fraction(k, 8) for k in range(9)]  # 0, 1/8, ..., 1

    tables = {str(p): [] for p in p_values}
    precomputed = {}

    for m in range(1, max_m + 1):
        print(f"Precomputing counts for m = {m} ...", flush=True)
        uniform_counts, uniform_denom = randomized_uniform_B_counts(m, bases)
        constant_counts, constant_denom = constant_rows_equal_B_counts(m, bases)
        precomputed[m] = (uniform_counts, uniform_denom, constant_counts, constant_denom)

        for p in p_values:
            print(f"  SD for m={m}, p={p} ...", flush=True)
            table = table_for_p(
                m, p, lambda_values,
                uniform_counts, uniform_denom,
                constant_counts, constant_denom,
            )
            tables[str(p)].append(table)

    result = {
        "n": 2,
        "max_m": max_m,
        "p_eff_n2": str(p_eff_n2()),
        "num_lagrangian": len(bases),
        "lambda_values": [str(v) for v in lambda_values],
        "tables": tables,
        "interpretation": {
            "comparison_distributions": [
                "LPN_{1/4} (ambient noise)",
                "LPN_{175/512} (matched per-coordinate output rate for n=2)",
            ],
            "B_family": "lambda-coupled marginal-uniform rows: all rows equal uniform r with prob lambda, else i.i.d. uniform",
            "pairwise_row_correlation": "lambda for any nonzero linear functional",
            "negative_result_criterion": "all sampled lambda values have SD >= baseline lambda=0",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / f"510-trackX-lambda-coupled-row-correlation-maxM{max_m}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
