#!/usr/bin/env python3
"""
220-KIMI-trackC-exact-t-distribution.py

Track C deliverable: exact distribution of the quadrant count t for one secret
pair under the isotropic (symplectic-LPN) public-matrix ensemble.

Given the proven subset moments (thm:mj-general, lsn-core.tex, sec:moments)
    m_j = E[ C(t,j) / C(2n,j) ],
the binomial moments are B_j := E[C(t,j)] = C(2n,j) * m_j.
The distribution of t on {0,...,2n} is recovered by the standard inclusion-
exclusion (binomial) transform
    Pr[t = ell] = sum_{j=ell}^{2n} (-1)^{j-ell} * C(j,ell) * B_j.

This script:
  1. Derives Pr[t=ell] from B_j using exact rational arithmetic.
  2. Verifies the derived distribution by independent direct enumeration of
     ordered isotropic pairs for n = 2,3,4.
  3. Computes the exact total-variation distance to Bin(2n, 1/4), the law of t
     under the unconstrained i.i.d. row ensemble, for n = 2,...,10.

All arithmetic uses fractions.Fraction.  JSON stores rationals as strings.

Interpretation guard (PRE-REGISTER):
  - Comparison distribution: Bin(2n, 1/4) is the exact law of t when rows are
    i.i.d. uniform (unconstrained ensemble).  It is the natural matched
    benchmark for the same quadrant-count statistic.
  - Scaling: t is a single-pair statistic over 2n coordinates; no m parameter
    appears.  The study is at fixed pair count (pairwise-level), not a joint
    test across many secret pairs.
  - Hardness implication: this is a structural moment/distribution result.  It
    does not, by itself, bound SQ hardness for multi-pair or full learning
    tasks (those require the SQ machinery of Track E).

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from fractions import Fraction
from math import comb
import json
import sys
from pathlib import Path


def symplectic_form_n(a: int, b: int, n: int) -> int:
    """Standard alternating symplectic form on F_2^{2n}."""
    s = 0
    for i in range(n):
        ai = (a >> i) & 1
        ain = (a >> (i + n)) & 1
        bi = (b >> i) & 1
        bin_ = (b >> (i + n)) & 1
        s ^= (ai & bin_) ^ (ain & bi)
    return s


def ordered_isotropic_pairs(n: int) -> list[tuple[int, int]]:
    """All ordered isotropic pairs (c1,c2) of distinct non-zero vectors."""
    N = 2 * n
    full = 1 << N
    nonzero = list(range(1, full))
    pairs = []
    for c1 in nonzero:
        for c2 in nonzero:
            if c1 == c2:
                continue
            if symplectic_form_n(c1, c2, n) == 0:
                pairs.append((c1, c2))
    return pairs


def t_distribution_enumeration(n: int):
    """Exact distribution of t = |supp(c1) & supp(c2)| by raw enumeration."""
    N = 2 * n
    pairs = ordered_isotropic_pairs(n)
    denom = len(pairs)
    hist = [0] * (N + 1)
    for c1, c2 in pairs:
        t = (c1 & c2).bit_count()
        hist[t] += 1
    return [Fraction(h, denom) for h in hist]


def P_isotropic(n: int) -> int:
    """Number of ordered isotropic pairs: (2^{2n}-1)(2^{2n-1}-2)."""
    N = 2 * n
    return (2 ** N - 1) * (2 ** (N - 1) - 2)


def m_j_closed(n: int, j: int) -> Fraction:
    """Closed form from thm:mj-general; valid for all 1 <= j <= 2n."""
    N = 2 * n
    P = P_isotropic(n)
    Dj = 2 ** (N - j)
    # First term: C(N,j) * (D_j^2/2 - D_j)
    num = comb(N, j) * (Fraction(Dj * Dj, 2) - Dj)
    if j % 2 == 0:
        num += comb(n, j // 2) * Fraction(Dj, 2)
    return Fraction(num, comb(N, j) * P)


def binomial_moments(n: int) -> list[Fraction]:
    """B_j = E[C(t,j)] for j = 0,...,2n; B_0 = 1."""
    N = 2 * n
    B = [Fraction(1, 1)]  # j = 0
    for j in range(1, N + 1):
        B.append(comb(N, j) * m_j_closed(n, j))
    return B


def t_distribution_transform(n: int) -> list[Fraction]:
    """Pr[t=ell] from the binomial transform of B_j."""
    N = 2 * n
    B = binomial_moments(n)
    probs = []
    for ell in range(N + 1):
        total = Fraction(0)
        for j in range(ell, N + 1):
            sign = -1 if (j - ell) & 1 else 1
            total += sign * comb(j, ell) * B[j]
        probs.append(total)
    return probs


def binomial_probabilities(n: int, p: Fraction) -> list[Fraction]:
    """Probability mass of Bin(2n, p)."""
    N = 2 * n
    q = Fraction(1) - p
    return [comb(N, k) * (p ** k) * (q ** (N - k)) for k in range(N + 1)]


def total_variation(p: list[Fraction], q: list[Fraction]) -> Fraction:
    """Exact TV distance between two distributions on the same support."""
    return sum(abs(p[i] - q[i]) for i in range(len(p))) / 2


def frac_list(xs: list[Fraction]) -> list[str]:
    return [str(x) for x in xs]


def float_list(xs: list[Fraction], digits: int = 12) -> list[float]:
    fmt = "{:." + str(digits) + "g}"
    return [float(fmt.format(float(x))) for x in xs]


def main():
    out_dir = Path(__file__).with_suffix("").parent.parent / "experiments" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "220-KIMI-trackC-exact-t-distribution.json"

    results = {
        "track": "C",
        "experiment": 220,
        "purpose": "exact distribution of quadrant count t and TV to Bin(2n,1/4)",
        "claims": {
            "distribution_formula": "THEOREM (derived from thm:mj-general via binomial transform)",
            "enumeration_check": "EVIDENCE (exact enumeration, n=2,3,4)",
            "tv_values": "EVIDENCE (exact rational computation, n=2..10)",
        },
        "interpretation_guard": {
            "comparison_distribution": "Bin(2n,1/4): exact law of t under unconstrained i.i.d. uniform rows; natural matched benchmark for the same statistic",
            "scaling": "single secret pair (pairwise-level); no m parameter; not a joint multi-pair analysis",
            "hardness_implication": "structural distribution result only; does not by itself imply SQ hardness for full learning tasks",
        },
        "per_n": {},
        "verification": {},
        "tv_summary": {},
    }

    # Verification: transform vs enumeration for n = 2,3,4
    verification_ok = True
    for n in (2, 3, 4):
        N = 2 * n
        trans = t_distribution_transform(n)
        enum = t_distribution_enumeration(n)
        match = all(a == b for a, b in zip(trans, enum))
        B = binomial_moments(n)
        results["per_n"][str(n)] = {
            "N": N,
            "P_isotropic_pairs": P_isotropic(n),
            "binomial_moments_B_j": frac_list(B),
            "transform_distribution": frac_list(trans),
            "enumeration_distribution": frac_list(enum),
            "transform_equals_enumeration": match,
        }
        if not match:
            verification_ok = False
            print(f"MISMATCH at n={n}", file=sys.stderr)
        print(f"n={n}: transform == enumeration ? {match}")

    # TV to Bin(2n, 1/4) for n = 2,...,10
    tv_results = {}
    for n in range(2, 11):
        N = 2 * n
        trans = t_distribution_transform(n)
        binom = binomial_probabilities(n, Fraction(1, 4))
        tv = total_variation(trans, binom)
        tv_results[str(n)] = {
            "N": N,
            "tv_exact": str(tv),
            "tv_float": float(tv),
        }
        print(f"n={n}: TV(dist(t), Bin({N},1/4)) = {tv}  ~= {float(tv):.6e}")

    results["tv_summary"] = tv_results
    results["verification"]["transform_matches_enumeration"] = verification_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    if not verification_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
