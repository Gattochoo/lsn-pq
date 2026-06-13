#!/usr/bin/env python3
r"""
229-KIMI-trackM-agreement-statistic.py

Track M — M3(c) corollary: one SQ-relevant statistic tabulated.

Statistic chosen: the triple agreement count
    a = t_{000} + t_{111},
i.e. the number of coordinates at which the three rows all agree
(all 0 or all 1).  This is the natural three-secret analogue of the pairwise
quadrant count and is directly relevant to correlation-style SQ queries on the
triple ensemble.

The exact distribution of a is obtained from the verified 8-variable count
polynomial (experiment 226) by grouping monomials with the same value of
e_{000} + e_{111}.  For n = 3 we also cross-check against direct enumeration.

Guards: L1, L2, L3 as in the other Track M scripts.
"""

from fractions import Fraction
from pathlib import Path
import json
import sys


SRC = Path(__file__).parent / "output" / "226-KIMI-trackM-triple-gf.json"


def parse_int_dict(d: dict[str, str]) -> dict[tuple[int, ...], int]:
    out = {}
    for k, v in d.items():
        inner = k.strip("()")
        e = tuple(int(x) for x in inner.split(","))
        out[e] = int(v)
    return out


def symplectic_form_n(a: int, b: int, n: int) -> int:
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) * ((b >> (i + n)) & 1)) ^ (
            ((a >> (i + n)) & 1) * ((b >> i) & 1)
        )
    return s


def enumerate_agreement(n: int) -> tuple[int, list[int]]:
    """Direct enumeration of a = t000 + t111 counts."""
    N = 2 * n
    full = 1 << N
    counts = [0] * (N + 1)
    total = 0
    for c1 in range(1, full):
        for c2 in range(1, full):
            if c1 == c2 or symplectic_form_n(c1, c2, n):
                continue
            for c3 in range(1, full):
                if c3 in (c1, c2):
                    continue
                if symplectic_form_n(c1, c3, n) or symplectic_form_n(c2, c3, n):
                    continue
                if c3 == c1 ^ c2:
                    continue
                agree0 = (~(c1 | c2 | c3)) & ((1 << N) - 1)
                agree1 = c1 & c2 & c3
                a = bin(agree0).count("1") + bin(agree1).count("1")
                counts[a] += 1
                total += 1
    return total, counts


def main() -> int:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "229-KIMI-trackM-agreement-statistic.json"

    with open(SRC) as f:
        triple_data = json.load(f)

    results = {
        "track": "M",
        "experiment": 229,
        "prefix": "track-M:",
        "purpose": "tabulate the triple agreement count a = t000 + t111",
        "statistic": {
            "name": "triple agreement count",
            "definition": "a = t_{000} + t_{111} = #{i : (c1_i, c2_i, c3_i) in {(0,0,0),(1,1,1)}}",
        },
        "claims": {
            "agreement_count_distribution": "THEOREM (specialisation/grouping of the verified triple GF)",
            "n3_enumeration_check": "EVIDENCE (direct enumeration match at n=3)",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction; JSON rationals as strings; counts as integers",
            "L2_J_twist": "inherited from the triple GF character sum",
            "L3_query_class_hygiene": "structural tabulation only; no SQ hardness inference",
            "L4_comparison_distribution": "not engaged",
        },
        "per_n": {},
        "verification": {},
    }

    all_ok = True
    for n in (3, 4):
        N = 2 * n
        count_poly = parse_int_dict(triple_data["per_n"][str(n)]["count_polynomial"])
        P = triple_data["per_n"][str(n)]["P3"]

        pmf = [Fraction(0) for _ in range(N + 1)]
        for e, c in count_poly.items():
            a = e[0] + e[7]
            pmf[a] += Fraction(c, P)

        # Direct enumeration only for n=3 (n=4 uses the verified GF).
        enum_total = None
        enum_pmf = None
        match = None
        if n == 3:
            enum_total, enum_counts = enumerate_agreement(n)
            enum_pmf = [Fraction(c, enum_total) for c in enum_counts]
            match = (enum_total == P) and (pmf == enum_pmf)
            if not match:
                all_ok = False

        results["per_n"][str(n)] = {
            "N": N,
            "P3": P,
            "pmf": [str(x) for x in pmf],
            "enumeration_total": enum_total,
            "enumeration_pmf": [str(x) for x in enum_pmf] if enum_pmf is not None else None,
            "enumeration_match": match,
        }
        print(f"n={n}: agreement table computed; n=3 enum match={match}")

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
