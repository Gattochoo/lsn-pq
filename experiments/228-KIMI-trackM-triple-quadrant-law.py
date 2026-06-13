#!/usr/bin/env python3
r"""
228-KIMI-trackM-triple-quadrant-law.py

Track M — M3(b) corollary: triple-quadrant count law.

Specialise the 8-variable triple GF to
    x_{111} = z,    x_tau = 1 for tau != 111.
The coefficient of z^k is Pr[ t_{111} = k ], where t_{111} counts the
coordinates at which all three rows are 1.

We tabulate the exact distribution for n = 3 and n = 4 and cross-check the
table against direct enumeration of ordered isotropic independent triples.

Guards: L1 (Fractions, JSON string fractions), L2 (inherited J-twist care),
L3 (structural tabulation, no Feldman inference).
"""

from fractions import Fraction
from pathlib import Path
import json
import sys


SRC = Path(__file__).parent / "output" / "226-KIMI-trackM-triple-gf.json"


def parse_frac_dict(d: dict[str, str]) -> dict[tuple[int, ...], Fraction]:
    out = {}
    for k, v in d.items():
        inner = k.strip("()")
        e = tuple(int(x) for x in inner.split(","))
        out[e] = Fraction(v)
    return out


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


def enumerate_t111(n: int) -> tuple[int, list[int]]:
    """Direct enumeration of t_{111} counts.  Returns (total, counts)."""
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
                t = bin(c1 & c2 & c3).count("1")
                counts[t] += 1
                total += 1
    return total, counts


def main() -> int:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "228-KIMI-trackM-triple-quadrant-law.json"

    with open(SRC) as f:
        triple_data = json.load(f)

    results = {
        "track": "M",
        "experiment": 228,
        "prefix": "track-M:",
        "purpose": "triple-quadrant count law for t_{111}",
        "claims": {
            "triple_quadrant_count_law": "THEOREM (specialisation of the verified triple GF)",
            "enumeration_cross_check": "EVIDENCE (exact table match by direct enumeration)",
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

        # Distribution from the closed-form count polynomial.
        pmf_from_gf = [Fraction(0) for _ in range(N + 1)]
        for e, c in count_poly.items():
            k = e[7]  # index of category 111
            pmf_from_gf[k] += Fraction(c, P)

        # Direct enumeration check.
        enum_total, enum_counts = enumerate_t111(n)
        pmf_enum = [Fraction(c, enum_total) for c in enum_counts]
        match = (enum_total == P) and (pmf_from_gf == pmf_enum)
        if not match:
            all_ok = False

        results["per_n"][str(n)] = {
            "N": N,
            "P3": P,
            "enumeration_total": enum_total,
            "enumeration_counts": enum_counts,
            "pmf_from_gf": [str(x) for x in pmf_from_gf],
            "pmf_from_enumeration": [str(x) for x in pmf_enum],
            "distributions_match": match,
        }
        print(f"n={n}: t111 table match={match}, P3={P}, enum={enum_total}")

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
