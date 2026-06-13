#!/usr/bin/env python3
"""830 (Track LL): exact I(x;y|C) for uniform-B-per-A at n=3 (m up to feasible)
and n=4 (small m), using the row-factored / ordered-basis measure.

Context
-------
The open core (lem:m2) asks whether I(x;y|C) = o(n) for typical marginal-uniform
C.  Track GG/II pinned the n=2 values; Track LL pushes to n=3 and n=4 to test
the trend.  The paper/Claude-646 canonical model is the **ordered-basis measure**:
A is a uniform ordered isotropic basis of a uniform Lagrangian, B is uniform
over F_2^{m x 2n} per A, e ~ Bernoulli(1/4)^{2n}.

Method (row-factored, never 2^{4m})
-----------------------------------
The naive ordered-basis enumeration would iterate over all ordered bases
(|GL(n)| per Lagrangian).  We avoid this by averaging analytically over the
ordered-basis choice.

For fixed Lagrangian L, representative basis A, and U in GL(n), the ordered
basis is A_U = A U.  Condition on the public matrix C = B A_U.  Because B is
uniform and independent of A, C is uniform over F_2^{m x n}.  Given C, B is
uniform on the affine space { B : B A_U = C }.  For a row r of B this is the
coset r_0 + ker(A_U^T); since L is Lagrangian, ker(A_U^T) = L.

For error vector e:
  * if e not in L, then l · e is uniform over F_2 as l ranges over L, so the
    corresponding output noise bit r·e is uniform over F_2 independent of C;
  * if e in L, say e = A_U z, then r·e = (r A_U) · z = C · z deterministically.

Averaging over the uniform ordered basis of L makes A_U^{-1} e uniform over
F_2^n \ {0} for each non-zero e in L.  Defining

    alpha(n) = E_L[ P_{e ~ Bern(1/4)^{2n}}( e in L ) ]
             = (1 / (|Lags_n| * 4^{2n})) sum_{L} sum_{v in L} 3^{2n - wt(v)},

    beta(n)  = P(e = 0) = (3/4)^{2n},

the conditional output law for a matrix C of rank r is:

    P(y | C, x) =
        beta                         if y = C x,
        (alpha - beta)/(2^n - 1)     if y in col(C) \ {Cx},
        0                            otherwise,

plus a uniform "outside'' mass (1 - alpha)/2^m spread over all y in F_2^m.
Explicitly:

    p1(r) = (1-alpha)/2^m + beta + (alpha-beta)(2^{n-r} - 1)/(2^n - 1),
    p2(r) = (1-alpha)/2^m + (alpha-beta) 2^{n-r}/(2^n - 1),
    p3    = (1-alpha)/2^m,

    P_in(r)  = (1-alpha)/2^m + alpha/2^r    (marginal for y in col(C)),
    P_out    = (1-alpha)/2^m                (marginal for y not in col(C)).

The conditional mutual information for rank r is

    I_r = p1(r) log2(p1(r)/P_in(r)) + (2^r - 1) p2(r) log2(p2(r)/P_in(r)),

and, using the exact rank distribution of a uniform m x n matrix over F_2,

    I(x;y|C) = sum_{r=0}^{min(m,n)} P(rank=r) * I_r.

The entire computation uses exact rational arithmetic for alpha, beta, the rank
counts and the probabilities; only the final log2 evaluations are floats.

Claims and labels
----------------
* The reduction from ordered-basis averaging to the alpha/beta/rank formula is
  a THEOREM (derivation above, checked against the direct n=2 enumeration of
  Track II / 646).
* The exact values for n=3, m up to 10 and n=4, m up to 8 are EVIDENCE.
* The trend of I(x;y|C)/n at comparable m/n is EVIDENCE/OPEN: the ratio
  decreases as n grows at fixed m/n, consistent with sublinear I, but small-n
  finite data cannot prove asymptotics.  No over-extrapolation.

Guards
------
L1 exact arithmetic: alpha and beta are Fractions; rank counts and probabilities
    are exact rationals; JSON stores string fractions.
L2 J-twist duality: derivation stays in the (C,y) output space.
L3 query-class hygiene: I(x;y|C) is the unrestricted information-theoretic ceiling.
L4 never transform the comparison distribution: no LPN comparison is used.
PRE-REGISTER: quantity = I(x;y|C) in bits; model = uniform-B-per-A single-block
reduction output under the ordered-basis measure; closure-grade = fixed-n.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n


# ---------------------------------------------------------------------------
# Exact rational helpers
# ---------------------------------------------------------------------------

def alpha_exact(n: int) -> Fraction:
    """Exact alpha(n) = E_L[P(e in L)] for uniform Lagrangian L in F_2^{2n}."""
    dim = 2 * n
    bases = enumerate_lagrangian_bases_n(n)
    num_subspaces = len(bases)
    total = Fraction(0)
    denom = Fraction(4 ** dim)
    for basis in bases:
        # Enumerate all vectors in the subspace spanned by basis.
        subspace = [0]
        for s in range(1, 1 << n):
            v = 0
            for j in range(n):
                if (s >> j) & 1:
                    v ^= basis[j]
            subspace.append(v)
        sub_sum = sum(3 ** (dim - v.bit_count()) for v in subspace)
        total += Fraction(sub_sum, denom)
    return total / num_subspaces


def beta_exact(n: int) -> Fraction:
    """P(e = 0) = (3/4)^{2n}."""
    return Fraction(3, 4) ** (2 * n)


def rank_count_exact(m: int, n: int, r: int) -> int:
    """Number of m x n matrices over F_2 with rank r (exact integer)."""
    num = 1
    den = 1
    for i in range(r):
        num *= (2 ** m - 2 ** i) * (2 ** n - 2 ** i)
        den *= (2 ** r - 2 ** i)
    return num // den


def conditional_mi_bits(n: int, m: int, alpha: Fraction, beta: Fraction) -> dict:
    """Compute I(x;y|C) in bits using the rank-based formula.

    Returns a dict with the float I, exact rank distribution, and per-rank
    probabilities as string fractions.
    """
    nx = 1 << n
    two_to_m = 1 << m
    max_r = min(m, n)
    total_matrices = 1 << (n * m)

    rank_probs = []
    per_rank = []
    I_total = 0.0

    for r in range(max_r + 1):
        count = rank_count_exact(m, n, r)
        prob = Fraction(count, total_matrices)

        two_to_r = 1 << r
        two_to_n_minus_r = 1 << (n - r)

        # p1: y = Cx
        p1 = Fraction(1 - alpha, two_to_m) + beta + (alpha - beta) * Fraction(two_to_n_minus_r - 1, nx - 1)
        # p2: y in col(C) \ {Cx}
        p2 = Fraction(1 - alpha, two_to_m) + (alpha - beta) * Fraction(two_to_n_minus_r, nx - 1)
        # marginal probability of y in col(C)
        p_in = Fraction(1 - alpha, two_to_m) + Fraction(alpha, two_to_r)

        # I_r
        I_r = 0.0
        if p1 > 0 and p_in > 0:
            I_r += float(p1) * math.log2(float(p1) / float(p_in))
        if p2 > 0 and p_in > 0 and r > 0:
            I_r += (two_to_r - 1) * float(p2) * math.log2(float(p2) / float(p_in))

        I_total += float(prob) * I_r

        per_rank.append({
            "rank": r,
            "count": count,
            "probability": str(prob),
            "p1": str(p1),
            "p2": str(p2),
            "P_in": str(p_in),
            "I_r_bits": I_r,
        })
        rank_probs.append(str(prob))

    return {
        "I_bits": I_total,
        "rank_distribution": per_rank,
    }


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_experiment(
    n3_ms: list[int] | None = None,
    n4_ms: list[int] | None = None,
    output_dir: Path | None = None,
):
    if n3_ms is None:
        n3_ms = list(range(1, 11))  # m = 1..10
    if n4_ms is None:
        n4_ms = list(range(1, 9))   # m = 1..8

    results = {
        "track": "LL",
        "experiment": 830,
        "quantity": "I(x;y|C) bits (ordered-basis measure)",
        "standing_guards": ["L1 exact arithmetic", "L2 J-twist duality", "L3 query-class hygiene", "L4 never transform LPN"],
        "modeling_choices": {
            "A_ensemble": "uniform ordered isotropic basis of a uniform Lagrangian (paper/lsn-core.tex line 602)",
            "B_per_row": "uniform over F_2^{2n}, independent per row and per A",
            "ambient_noise": "Bernoulli(1/4)^{2n}",
            "method": "row-factored ordered-basis average -> alpha/beta/rank formula (never 2^{4m} enumeration)",
        },
        "alphas": {},
        "betas": {},
        "rows_n3": [],
        "rows_n4": [],
        "claim_labels": {
            "ordered_basis_formula": "THEOREM (averaging over GL(n) ordered bases; checked against n=2 direct enumeration)",
            "exact_values_n3_n4": "EVIDENCE (finite n,m)",
            "sublinearity_trend": "EVIDENCE/OPEN (small-n trend only; no asymptotic proof)",
        },
    }

    for n in [2, 3, 4]:
        t0 = time.time()
        alpha = alpha_exact(n)
        beta = beta_exact(n)
        results["alphas"][str(n)] = str(alpha)
        results["betas"][str(n)] = str(beta)
        print(f"n={n}: alpha={float(alpha):.8f}, beta={float(beta):.8f} (computed in {time.time()-t0:.2f}s)", file=sys.stderr)

    alpha3 = Fraction(results["alphas"]["3"])
    beta3 = Fraction(results["betas"]["3"])
    alpha4 = Fraction(results["alphas"]["4"])
    beta4 = Fraction(results["betas"]["4"])

    for m in n3_ms:
        t0 = time.time()
        res = conditional_mi_bits(3, m, alpha3, beta3)
        row = {
            "m": m,
            "m_over_n": str(Fraction(m, 3)),
            "I_bits": res["I_bits"],
            "I_over_n": res["I_bits"] / 3,
            "elapsed_seconds": time.time() - t0,
        }
        results["rows_n3"].append(row)
        print(f"n=3, m={m}: I={res['I_bits']:.6f}, I/n={res['I_bits']/3:.6f}", file=sys.stderr)

    for m in n4_ms:
        t0 = time.time()
        res = conditional_mi_bits(4, m, alpha4, beta4)
        row = {
            "m": m,
            "m_over_n": str(Fraction(m, 4)),
            "I_bits": res["I_bits"],
            "I_over_n": res["I_bits"] / 4,
            "elapsed_seconds": time.time() - t0,
        }
        results["rows_n4"].append(row)
        print(f"n=4, m={m}: I={res['I_bits']:.6f}, I/n={res['I_bits']/4:.6f}", file=sys.stderr)

    # Cross-n comparison at comparable m/n ratios using the n=2 canonical/ordered
    # values from Track II (646).
    n2_values = {
        1: 0.040183461837335274,   # Track II / 646 ordered-basis, m=1
        2: 0.09430904407345661,    # Track II ordered-basis, m=2
        3: 0.153064287919533,      # Track II ordered-basis, m=3
        4: 0.2040292087173045,     # Track II ordered-basis, m=4
        5: 0.2404095928360578,     # Track II ordered-basis, m=5
        6: 0.2628844401026241,     # Track II ordered-basis, m=6
        7: 0.2755223350964832,     # Track II ordered-basis, m=7
        8: 0.2827774749291242,     # Track II ordered-basis, m=8
    }

    comparable = []
    for ratio in [Fraction(1, 1), Fraction(3, 2), Fraction(2, 1), Fraction(5, 2), Fraction(3, 1)]:
        entry = {"ratio": str(ratio)}
        for n in [2, 3, 4]:
            m = int(ratio * n)
            if ratio * n != m:
                continue
            if n == 2:
                I = n2_values.get(m)
            elif n == 3:
                I = next((r["I_bits"] for r in results["rows_n3"] if r["m"] == m), None)
            else:
                I = next((r["I_bits"] for r in results["rows_n4"] if r["m"] == m), None)
            if I is not None:
                entry[f"n{n}_m{m}"] = {"I_bits": I, "I_over_n": I / n}
        comparable.append(entry)
    results["comparable_m_over_n"] = comparable

    # Simple linear fit of I/n vs n at comparable ratios (least-squares).
    fits = []
    for entry in comparable:
        xs = []
        ys = []
        for key, val in entry.items():
            if key.startswith("n") and "_m" in key:
                n = int(key.split("_")[0][1:])
                ys.append(val["I_over_n"])
                xs.append(n)
        if len(xs) >= 2:
            mx = sum(xs) / len(xs)
            my = sum(ys) / len(ys)
            ss_xx = sum((x - mx) ** 2 for x in xs)
            ss_xy = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs)))
            slope = ss_xy / ss_xx if ss_xx != 0 else 0.0
            intercept = my - slope * mx
            fits.append({
                "ratio": entry["ratio"],
                "slope_I_over_n_per_n": slope,
                "intercept": intercept,
                "points": [{"n": x, "I_over_n": y} for x, y in zip(xs, ys)],
            })
    results["I_over_n_vs_n_fit"] = fits

    if output_dir is None:
        output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "830-trackLL-Ixy-growth-n3-n4.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track LL: exact I(x;y|C) growth at n=3,4")
    parser.add_argument("--n3-ms", type=int, nargs="+", default=None, help="m values for n=3")
    parser.add_argument("--n4-ms", type=int, nargs="+", default=None, help="m values for n=4")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    results = run_experiment(n3_ms=args.n3_ms, n4_ms=args.n4_ms, output_dir=args.output_dir)
    print(json.dumps(results, indent=2))
