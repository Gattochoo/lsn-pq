#!/usr/bin/env python3
r"""
226-KIMI-trackM-triple-composition-generating-function.py

Track M — M1/M2 deliverable: closed-form 8-variable generating function for the
joint composition of an ordered isotropic TRIPLE.

Ensemble: ordered triples (c1, c2, c3) in F_2^{2n} that are
  (i) pairwise isotropic: Omega(c_i, c_j) = 0 for all i < j,
  (ii) linearly independent over F_2.
For n = 2 the maximal isotropic subspace has dimension 2, so no such triple
exists and the GF is identically 0.  The ensemble is non-trivial for n >= 3.

Category variables.  For each coordinate the triple of bits
  tau = (tau_1, tau_2, tau_3) in F_2^3
falls into one of eight categories.  We write x_tau = x_{tau_1 tau_2 tau_3}.
The joint GF is
    G_n^{(3)}(x) = E[ prod_{tau in F_2^3} x_tau^{t_tau} ],
where t_tau counts coordinates with category tau.

THEOREM (this script):
  Let L range over the subspaces of the 3-dimensional category space F_2^3.
  For a subspace L define
      T_L(x) = sum_{tau in L} x_tau,
      S_{lambda,L}(x) = sum_{u,v in L}
          (-1)^{lambda_{12}(u_1 v_2 + u_2 v_1)
                 + lambda_{13}(u_1 v_3 + u_3 v_1)
                 + lambda_{23}(u_2 v_3 + u_3 v_2)}
          x_u x_v,
  and
      G_L(x) = (1/8) [ T_L(x)^{2n} + sum_{lambda != 0} S_{lambda,L}(x)^n ].
  Then the numerator of the triple GF is the inclusion-exclusion/Moebius sum
      N_n(x) = G_{F_2^3}
               - sum_{H hyperplane} G_H
               + 2 sum_{\ell line} G_\ell
               - 8 G_{\{0\}}.
  Equivalently the coefficient of L is the F_2-subspace Moebius function
  mu(0, L) = (-1)^{dim L} 2^{(dim L choose 2)}.  Finally
      G_n^{(3)}(x) = N_n(x) / P_3(n),
  with
      P_3(n) = (2^{2n} - 1)(2^{2n-1} - 2)(2^{2n-2} - 4).

Proof sketch:
  The pairwise-isotropy indicator is the 3-variable character sum over
  lambda in F_2^3.  Because Omega factorizes over the n symplectic coordinate
  pairs, the lambda = 0 term contributes T_{F_2^3}^{2n} and each non-zero
  lambda contributes S_{lambda}^{n}.  The seven non-zero lambdas split into
  three single-edge, three two-edge, and one triangle orbit under S_3.
  Excluding zero vectors, equalities, and the relation c1+c2+c3 = 0 covers
  exactly all non-independent triples; these are the seven non-zero linear
  forms on F_2^3, giving the inclusion-exclusion above.  The Moebius
  coefficients (+1, -1, +2, -8) are computed by summing over subsets.

Verification:
  - Direct enumeration of ordered isotropic independent triples.
  - n = 3: 22,680 triples; n = 4: 1,927,800 triples (see Count correction
    below).
  - Coefficient-by-coefficient match between closed-form expansion and
    enumeration.

Count correction (L1 / Sound Verifier):
  The Track M reminder parenthetically wrote n=4 as 255*126*56 = 1,799,280.
  The third factor for independent c3 is 2^{2n-2} - 4 = 64 - 4 = 60, giving
  255*126*60 = 1,927,800, which is exactly what our enumeration returns.
  We report and use the corrected value.

Guards:
  (L1) Exact arithmetic via fractions.Fraction; JSON stores rationals as strings.
  (L2) J-twist care: the character sum uses the standard symplectic form
       Omega on V x V; per-symplectic-pair contraction avoids dual-space
       confusion.
  (L3) Query-class hygiene: this is a structural three-secret composition
       result; no unrestricted SQ hardness / Feldman inference is claimed.
  (L4) Not engaged: there is no comparison distribution to transform here.

PRE-REGISTER interpretation guard:
  - Scope: three-secret pairwise level only; the full multi-pair SQ level
    remains OPEN.
  - The closed form is a counting theorem over the triple ensemble.
  - Hardness implication: by itself this GF does not prove SQ lower bounds for
    learning tasks.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from fractions import Fraction
from itertools import product, combinations
from functools import lru_cache
from math import comb
from collections import defaultdict
from pathlib import Path
import json
import sys
import time


# ---------------------------------------------------------------------------
# Category indexing
# ---------------------------------------------------------------------------

CATS = list(product((0, 1), repeat=3))
CAT_INDEX = {c: i for i, c in enumerate(CATS)}
# Convenience: label order 000,001,010,011,100,101,110,111.


def unit_monomial(tau: tuple[int, int, int]) -> tuple[int, ...]:
    e = [0] * 8
    e[CAT_INDEX[tau]] = 1
    return tuple(e)


# ---------------------------------------------------------------------------
# Symplectic geometry
# ---------------------------------------------------------------------------

def symplectic_form_n(a: int, b: int, n: int) -> int:
    """Standard alternating symplectic form on F_2^{2n}."""
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) * ((b >> (i + n)) & 1)) ^ (
            ((a >> (i + n)) & 1) * ((b >> i) & 1)
        )
    return s


# ---------------------------------------------------------------------------
# Exact polynomial helpers (8 variables)
# ---------------------------------------------------------------------------

def poly_add(p: dict, q: dict, sign: int = 1) -> dict:
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, Fraction(0)) + sign * v
    return {k: v for k, v in r.items() if v != 0}


@lru_cache(maxsize=None)
def compositions_fixed_sum(k: int, total: int):
    """All k-tuples of non-negative integers summing to total."""
    if k == 1:
        return [(total,)]
    res = []
    for a in range(total + 1):
        for rest in compositions_fixed_sum(k - 1, total - a):
            res.append((a,) + rest)
    return res


def expand_power(poly: dict, power: int) -> dict:
    """Expand a homogeneous polynomial to a fixed power, exact Fractions."""
    if power == 0:
        return {tuple([0] * 8): Fraction(1)}
    monos = list(poly.items())
    k = len(monos)
    out = {}
    for comp in compositions_fixed_sum(k, power):
        # multinomial coefficient
        mult = comb(power, comp[0])
        rem = power - comp[0]
        for i in range(1, k):
            mult = mult * comb(rem, comp[i])
            rem -= comp[i]
        exp = [0] * 8
        coef = Fraction(1)
        for cnt, (e, c) in zip(comp, monos):
            if cnt == 0:
                continue
            for i in range(8):
                exp[i] += cnt * e[i]
            coef *= c ** cnt
        coef *= mult
        exp_t = tuple(exp)
        out[exp_t] = out.get(exp_t, Fraction(0)) + coef
    return {k: v for k, v in out.items() if v != 0}


# ---------------------------------------------------------------------------
# Character-sum building blocks
# ---------------------------------------------------------------------------

def chi_pair(lam: tuple[int, int, int], u: tuple[int, int, int], v: tuple[int, int, int]) -> int:
    """Sign attached to a symplectic coordinate pair for lambda != 0."""
    exp = (
        lam[0] * (u[0] * v[1] + u[1] * v[0])
        + lam[1] * (u[0] * v[2] + u[2] * v[0])
        + lam[2] * (u[1] * v[2] + u[2] * v[1])
    )
    return -1 if (exp & 1) else 1


@lru_cache(maxsize=None)
def S_lambda_poly(lam: tuple[int, int, int], L_frozen: frozenset) -> dict:
    """Quadratic per-symplectic-pair polynomial S_{lambda,L}."""
    L = tuple(sorted(L_frozen))
    p = defaultdict(Fraction)
    for u in L:
        for v in L:
            coef = chi_pair(lam, u, v)
            e = tuple(unit_monomial(u)[i] + unit_monomial(v)[i] for i in range(8))
            p[e] += Fraction(coef)
    return dict(p)


@lru_cache(maxsize=None)
def raw_GF_count(L_frozen: frozenset, n: int) -> dict:
    """
    Unnormalised GF for triples satisfying the linear constraints encoded by L.
    Returns a polynomial whose coefficients are integer counts divided by 8.
    """
    L = frozenset(L_frozen)
    N = 2 * n
    T = {unit_monomial(t): Fraction(1) for t in L}
    total = expand_power(T, N)
    for lam in product((0, 1), repeat=3):
        if lam == (0, 0, 0):
            continue
        S = S_lambda_poly(lam, L)
        total = poly_add(total, expand_power(S, n))
    return {k: v / 8 for k, v in total.items()}


# ---------------------------------------------------------------------------
# Inclusion-exclusion over all non-zero linear forms on F_2^3
# ---------------------------------------------------------------------------

HYPERPLANES = [
    frozenset({tau for tau in CATS if (a * tau[0] + b * tau[1] + c * tau[2]) % 2 == 0})
    for a, b, c in product((0, 1), repeat=3)
    if (a, b, c) != (0, 0, 0)
]

_LINES = []
_seen = set()
for v in CATS:
    if v == (0, 0, 0):
        continue
    L = frozenset({(0, 0, 0), v})
    if L not in _seen:
        _seen.add(L)
        _LINES.append(L)
LINES = _LINES
POINT = frozenset({(0, 0, 0)})
FULL = frozenset(CATS)


def triple_GF_count(n: int) -> dict:
    """Unnormalised numerator N_n(x) for the independent triple ensemble."""
    poly = raw_GF_count(FULL, n)
    for H in HYPERPLANES:
        poly = poly_add(poly, raw_GF_count(H, n), -1)
    for L in LINES:
        poly = poly_add(poly, raw_GF_count(L, n), 2)
    poly = poly_add(poly, raw_GF_count(POINT, n), -8)
    return poly


def P3(n: int) -> int:
    N = 2 * n
    return (2 ** N - 1) * (2 ** (N - 1) - 2) * (2 ** (N - 2) - 4)


# ---------------------------------------------------------------------------
# Direct enumeration (verification only)
# ---------------------------------------------------------------------------

def enumerate_triples(n: int) -> tuple[int, dict]:
    """Direct enumeration of ordered isotropic independent triples."""
    N = 2 * n
    full = 1 << N
    hist: dict[tuple[int, ...], int] = {}
    cnt = 0
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
                e = [0] * 8
                for i in range(N):
                    idx = (
                        (((c1 >> i) & 1) << 2)
                        | (((c2 >> i) & 1) << 1)
                        | ((c3 >> i) & 1)
                    )
                    e[idx] += 1
                e_t = tuple(e)
                hist[e_t] = hist.get(e_t, 0) + 1
                cnt += 1
    return cnt, hist


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def mono_key(e: tuple[int, ...]) -> str:
    return "(" + ",".join(str(v) for v in e) + ")"


def frac_dict(poly: dict[tuple[int, ...], Fraction]) -> dict[str, str]:
    return {mono_key(k): str(v) for k, v in sorted(poly.items())}


def int_dict(poly: dict[tuple[int, ...], Fraction]) -> dict[str, int]:
    return {mono_key(k): int(v) for k, v in sorted(poly.items())}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "226-KIMI-trackM-triple-gf.json"

    results = {
        "track": "M",
        "experiment": 226,
        "prefix": "track-M:",
        "purpose": "closed-form 8-variable generating function for ordered isotropic independent triples",
        "theorem": (
            "G_n^(3)(x) = ( G_{F_2^3} - sum_H G_H + 2 sum_ell G_ell - 8 G_{{0}} ) / P_3(n), "
            "with G_L = (T_L^{2n} + sum_{lambda!=0} S_{lambda,L}^n)/8 and P_3(n)=(2^{2n}-1)(2^{2n-1}-2)(2^{2n-2}-4)."
        ),
        "claims": {
            "triple_gf_closed_form": "THEOREM",
            "P3_count_law": "THEOREM",
            "enumeration_verification_n3": "EVIDENCE (exact coefficient-wise match, 22,680 triples)",
            "enumeration_verification_n4": "EVIDENCE (exact coefficient-wise match, 1,927,800 triples)",
            "n4_count_correction": "NOTE (directive parenthetical 1,799,280 corrected to 1,927,800)",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON rationals stored as strings; counts stored as integers",
            "L2_J_twist": "character sum uses (-1)^{Omega(c_i,c_j)} with standard symplectic form; per-symplectic-pair contraction avoids dual-space confusion",
            "L3_query_class_hygiene": "three-secret structural composition result only; no unrestricted SQ / Feldman inference claim",
            "L4_comparison_distribution": "not engaged (no comparison distribution is transformed in this counting theorem)",
        },
        "pre_register_interpretation": {
            "scope": "three-secret pairwise level only; full multi-pair SQ level remains OPEN",
            "benchmark": "coordinate categories are the unconstrained i.i.d. 8-way multinomial if isotropy constraints are ignored",
            "hardness_implication": "structural generating-function result; does not by itself imply SQ hardness for full learning tasks",
        },
        "per_n": {},
        "verification": {},
    }

    all_ok = True
    for n in (2, 3, 4):
        t0 = time.time()
        count_poly = triple_GF_count(n)
        closed_time = time.time() - t0
        P = P3(n)

        if n == 2:
            # Degenerate: no independent triples in F_2^4.
            per_n = {
                "N": 4,
                "P3": 0,
                "num_distinct_compositions": 0,
                "closed_form_is_zero": len(count_poly) == 0,
                "closed_form_time_sec": closed_time,
            }
            results["per_n"][str(n)] = per_n
            print(
                f"n={n}: degenerate (no independent triples), closed-form time={closed_time:.3f}s"
            )
            continue

        prob_poly = {k: Fraction(v, P) for k, v in count_poly.items()}

        t0 = time.time()
        enum_cnt, enum_hist = enumerate_triples(n)
        enum_time = time.time() - t0
        enum_poly = {k: Fraction(v, enum_cnt) for k, v in enum_hist.items()}

        count_match = (enum_cnt == P) and (sum(count_poly.values()) == P)
        poly_match = prob_poly == enum_poly
        non_negative = all(c >= 0 for c in prob_poly.values())
        sums_to_one = sum(prob_poly.values()) == 1

        if not (count_match and poly_match and non_negative and sums_to_one):
            all_ok = False

        per_n = {
            "N": 2 * n,
            "P3": P,
            "enumeration_count": enum_cnt,
            "count_match": count_match,
            "num_distinct_compositions": len(prob_poly),
            "polynomial_matches_enumeration": poly_match,
            "coefficients_non_negative": non_negative,
            "coefficients_sum_to_one": sums_to_one,
            "closed_form_time_sec": closed_time,
            "enumeration_time_sec": enum_time,
            "count_polynomial": int_dict(count_poly),
            "probability_polynomial": frac_dict(prob_poly),
        }
        results["per_n"][str(n)] = per_n

        print(
            f"n={n}: P3={P}, enum={enum_cnt}, monomials={len(prob_poly)}, "
            f"poly_match={poly_match}, non-negative={non_negative}, sums-to-one={sums_to_one}, "
            f"closed={closed_time:.3f}s, enum={enum_time:.3f}s"
        )

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
