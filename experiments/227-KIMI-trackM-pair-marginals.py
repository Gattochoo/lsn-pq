#!/usr/bin/env python3
r"""
227-KIMI-trackM-pair-marginals.py

Track M — M3(a) corollary: every pair-marginal of the triple composition GF
reproduces thm:joint-gf (the closed 4-variable pairwise GF of Track I).

The triple GF uses 8 categories indexed by the bit triple
  (tau_1, tau_2, tau_3) in F_2^3,
corresponding to the coordinate-wise values of (c1, c2, c3).  Collapsing the
category variable of the omitted secret gives a 4-variable marginal.  By S_3
symmetry the three pair-marginals are formally identical; we verify all three
explicitly.

Guards: L1 (fractions.Fraction, JSON string fractions), L2 (J-twist is built
into the parent triple GF), L3 (pairwise-level structural check only).
"""

from fractions import Fraction
from math import comb
from pathlib import Path
import json
import sys


def load_triple_gf():
    src = Path(__file__).parent / "output" / "226-KIMI-trackM-triple-gf.json"
    with open(src) as f:
        data = json.load(f)
    return data


def parse_frac_dict(d: dict[str, str]) -> dict[tuple[int, ...], Fraction]:
    out = {}
    for k, v in d.items():
        # key format "(a,b,c,d,e,f,g,h)"
        inner = k.strip("()")
        e = tuple(int(x) for x in inner.split(","))
        out[e] = Fraction(v)
    return out


def pair_G_n_polynomial(n: int) -> dict[tuple[int, int, int, int], Fraction]:
    """Closed-form 4-variable GF from thm:joint-gf (Track I / 225)."""
    P = (2 ** (2 * n) - 1) * (2 ** (2 * n - 1) - 2)
    poly = {}

    def add(mono, coef):
        if coef == 0:
            return
        poly[mono] = poly.get(mono, Fraction(0)) + coef

    # (T^{2n} + S^n)/2
    for a in range(2 * n + 1):
        for b in range(2 * n + 1 - a):
            for c in range(2 * n + 1 - a - b):
                d = 2 * n - a - b - c
                coef = comb(2 * n, a) * comb(2 * n - a, b) * comb(2 * n - a - b, c)
                add((a, b, c, d), Fraction(coef, 2))

    base = {
        (2, 0, 0, 0): Fraction(1),
        (0, 2, 0, 0): Fraction(1),
        (0, 0, 2, 0): Fraction(1),
        (0, 0, 0, 2): Fraction(1),
        (1, 0, 0, 1): Fraction(2),
        (0, 1, 0, 1): Fraction(2),
        (0, 0, 1, 1): Fraction(2),
        (0, 1, 1, 0): Fraction(-2),
        (1, 0, 1, 0): Fraction(-2),
        (1, 1, 0, 0): Fraction(-2),
    }
    Sn = {(0, 0, 0, 0): Fraction(1)}
    for _ in range(n):
        new = {}
        for m1, c1 in Sn.items():
            for m2, c2 in base.items():
                m = (m1[0] + m2[0], m1[1] + m2[1], m1[2] + m2[2], m1[3] + m2[3])
                new[m] = new.get(m, Fraction(0)) + c1 * c2
        Sn = new
    for m, c in Sn.items():
        add(m, Fraction(c, 2))

    # -A^{2n} - B^{2n} - C^{2n} + 2 x00^{2n}
    for c in range(2 * n + 1):
        add((0, 0, c, 2 * n - c), -Fraction(comb(2 * n, c)))
    for b in range(2 * n + 1):
        add((0, b, 0, 2 * n - b), -Fraction(comb(2 * n, b)))
    for a in range(2 * n + 1):
        add((a, 0, 0, 2 * n - a), -Fraction(comb(2 * n, a)))
    add((0, 0, 0, 2 * n), Fraction(2))

    return {m: Fraction(c, P) for m, c in poly.items() if c != 0}


# Marginal collapse maps.  Pair variable order is (t11, t10, t01, t00).

def marginal_12(e: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Collapse c3: (t11, t10, t01, t00) from (c1, c2)."""
    return (e[6] + e[7], e[4] + e[5], e[2] + e[3], e[0] + e[1])


def marginal_13(e: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Collapse c2: (t11, t10, t01, t00) from (c1, c3)."""
    return (e[5] + e[7], e[4] + e[6], e[1] + e[3], e[0] + e[2])


def marginal_23(e: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Collapse c1: (t11, t10, t01, t00) from (c2, c3)."""
    return (e[3] + e[7], e[2] + e[6], e[1] + e[5], e[0] + e[4])


def main() -> int:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "227-KIMI-trackM-pair-marginals.json"

    triple_data = load_triple_gf()
    results = {
        "track": "M",
        "experiment": 227,
        "prefix": "track-M:",
        "purpose": "verify that each pair-marginal of the triple GF reproduces thm:joint-gf",
        "claims": {
            "pair_marginals_reproduce_joint_gf": "THEOREM (specialization/marginalization of the triple GF)",
            "enumeration_independence_check": "EVIDENCE (marginalization of the verified n=3,4 triple polynomials)",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON rationals as strings",
            "L2_J_twist": "inherited from the triple GF character sum; marginalization does not alter the symplectic form",
            "L3_query_class_hygiene": "pairwise-level structural consistency check only",
            "L4_comparison_distribution": "not engaged",
        },
        "per_n": {},
        "verification": {},
    }

    all_ok = True
    for n in (3, 4):
        prob_poly = parse_frac_dict(triple_data["per_n"][str(n)]["probability_polynomial"])
        pair_poly = pair_G_n_polynomial(n)

        checks = {}
        for name, marg in (
            ("pair_12", marginal_12),
            ("pair_13", marginal_13),
            ("pair_23", marginal_23),
        ):
            marg_poly: dict[tuple[int, int, int, int], Fraction] = {}
            for e, c in prob_poly.items():
                me = marg(e)
                marg_poly[me] = marg_poly.get(me, Fraction(0)) + c
            match = marg_poly == pair_poly
            if not match:
                all_ok = False
            checks[name] = {
                "match": match,
                "num_monomials": len(marg_poly),
                "sums_to_one": sum(marg_poly.values()) == 1,
            }

        results["per_n"][str(n)] = {
            "N": 2 * n,
            "P3": triple_data["per_n"][str(n)]["P3"],
            "pair_G_n_monomials": len(pair_poly),
            "marginal_checks": checks,
            "all_pair_marginals_match": all(ch["match"] for ch in checks.values()),
        }
        print(
            f"n={n}: pair-marginal checks: "
            f"12={checks['pair_12']['match']} 13={checks['pair_13']['match']} 23={checks['pair_23']['match']}"
        )

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
