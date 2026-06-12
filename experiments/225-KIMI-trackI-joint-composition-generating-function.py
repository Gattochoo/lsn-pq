#!/usr/bin/env python3
"""
225-KIMI-trackI-joint-composition-generating-function.py

Track I deliverable: closed-form joint generating function for the four-category
row composition of an ordered isotropic pair.

For an ordered isotropic pair (c1, c2) in F_2^{2n} (nonzero, distinct,
Omega(c1,c2)=0), each coordinate i falls into one of four categories:
  tau = 11  if c1_i = c2_i = 1
  tau = 10  if c1_i = 1, c2_i = 0
  tau = 01  if c1_i = 0, c2_i = 1
  tau = 00  if c1_i = c2_i = 0.

The joint generating function is
    G_n(x11, x10, x01, x00) = E[ prod_tau x_tau^{t_tau} ],
where t_tau counts coordinates of category tau over the ordered isotropic-pair
ensemble.

THEOREM (this script):
    Let
        T = x11 + x10 + x01 + x00,
        S = T^2 - 4*(x10*x01 + x10*x11 + x01*x11),
        A = x00 + x01,
        B = x00 + x10,
        C = x00 + x11,
        P = (2^{2n} - 1)(2^{2n-1} - 2).
    Then
        G_n = [ (T^{2n} + S^n)/2 - A^{2n} - B^{2n} - C^{2n} + 2*x00^{2n} ] / P.

Proof sketch (radical / non-degenerate character-sum split, with J-twist):
  1_{Omega(c1,c2)=0} = (1/2) * sum_{lambda in F_2} (-1)^{lambda * Omega(c1,c2)}.
  The lambda=0 term is the "radical" contribution and factorizes as T^{2n}.
  The lambda=1 term is the non-degenerate character; it factorizes over the n
  symplectic coordinate pairs, each pair contributing S.  This is the required
  J-twist: the exponent is the standard symplectic form Omega(c1,c2), whose
  Gram matrix is J.  Finally we subtract the excluded cases c1=0, c2=0, and
  c1=c2, which contribute A^{2n}, B^{2n}, and C^{2n} respectively, and add
  back their triple intersection 2*x00^{2n}.

The formula is verified by direct enumeration for n = 2, 3, 4.

Corollaries extracted from G_n:
  (a) Re-derive thm:mj-general:  E[C(t11, j)] = coeff of x^j in G_n(1+x,1,1,1).
  (b) Re-derive prop:tdist:      Pr[t11 = ell] = coeff of x^ell in G_n(x,1,1,1).
  (c) Disagreement count d = t10 + t01:
          Pr[d = 0] = 0,
          Pr[d = k] = C(2n, k) / (2^{2n} - 1)   for k = 1, ..., 2n.
      Proven by specializing G_n to (1, y, y, 1).

Guards:
  (L1) Exact arithmetic via fractions.Fraction; JSON stores rationals as strings.
  (L2) J-twist care: the character sum uses (-1)^{Omega(c1,c2)}, i.e. the
       standard symplectic form whose Gram matrix is J.  We sum directly over
       V x V, so no dual-space confusion arises.
  (L3) Query-class hygiene: this is a pairwise-level structural result; no
       unrestricted SQ claim is made.

PRE-REGISTER interpretation guard:
  - Scope: two-secret pairwise level only; the multi-pair joint composition
    remains open.
  - The benchmark Bin(2n, 1/4) for t11 is the unconstrained i.i.d. row law.
  - Hardness implication: the closed-form generating function is a structural
    counting result.  It does not, by itself, imply SQ hardness for full
    learning tasks (those require the SQ machinery of Track E).

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from fractions import Fraction
from math import comb
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Symplectic geometry helpers
# ---------------------------------------------------------------------------

def symplectic_form_n(a: int, b: int, n: int) -> int:
    """Standard alternating symplectic form on F_2^{2n}."""
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) * ((b >> (i + n)) & 1)) ^ (
            ((a >> (i + n)) & 1) * ((b >> i) & 1)
        )
    return s


def ordered_isotropic_pairs(n: int) -> list[tuple[int, int]]:
    """All ordered isotropic pairs (c1, c2): nonzero, distinct, Omega(c1,c2)=0."""
    N = 2 * n
    full = 1 << N
    pairs = []
    for c1 in range(1, full):
        for c2 in range(1, full):
            if c1 == c2:
                continue
            if symplectic_form_n(c1, c2, n) == 0:
                pairs.append((c1, c2))
    return pairs


def pair_composition(c1: int, c2: int, N: int) -> tuple[int, int, int, int]:
    """Return (t11, t10, t01, t00) for a pair over N = 2n coordinates."""
    t11 = t10 = t01 = t00 = 0
    for i in range(N):
        a = (c1 >> i) & 1
        b = (c2 >> i) & 1
        if a == 1 and b == 1:
            t11 += 1
        elif a == 1 and b == 0:
            t10 += 1
        elif a == 0 and b == 1:
            t01 += 1
        else:
            t00 += 1
    return t11, t10, t01, t00


# ---------------------------------------------------------------------------
# Closed-form joint generating function
# ---------------------------------------------------------------------------

def P_isotropic(n: int) -> int:
    """Number of ordered isotropic pairs."""
    N = 2 * n
    return (2 ** N - 1) * (2 ** (N - 1) - 2)


def G_n_eval(
    n: int,
    x11: Fraction,
    x10: Fraction,
    x01: Fraction,
    x00: Fraction,
) -> Fraction:
    """Evaluate the closed-form joint generating function at a point."""
    T = x11 + x10 + x01 + x00
    S = T * T - 4 * (x10 * x01 + x10 * x11 + x01 * x11)
    A = x00 + x01
    B = x00 + x10
    C = x00 + x11
    num = (T ** (2 * n) + S ** n) / 2 - A ** (2 * n) - B ** (2 * n) - C ** (2 * n) + 2 * x00 ** (2 * n)
    return Fraction(num, P_isotropic(n))


def G_n_polynomial(n: int) -> dict[tuple[int, int, int, int], Fraction]:
    """
    Expand G_n as a sparse polynomial.

    Returns a dict mapping (t11, t10, t01, t00) -> coefficient (Fraction),
    summing over the 4-category compositions of 2n coordinates.
    """
    P = P_isotropic(n)
    poly: dict[tuple[int, int, int, int], Fraction] = {}

    def add(mono: tuple[int, int, int, int], coef: Fraction) -> None:
        if coef == 0:
            return
        poly[mono] = poly.get(mono, Fraction(0)) + coef

    # T^{2n}: multinomial expansion.
    for a in range(2 * n + 1):
        for b in range(2 * n + 1 - a):
            for c in range(2 * n + 1 - a - b):
                d = 2 * n - a - b - c
                coef = Fraction(
                    comb(2 * n, a) * comb(2 * n - a, b) * comb(2 * n - a - b, c)
                )
                add((a, b, c, d), Fraction(coef, 2))

    # S^n where S = x11^2 + x10^2 + x01^2 + x00^2
    #               + 2*x11*x00 + 2*x10*x00 + 2*x01*x00
    #               - 2*x10*x01 - 2*x11*x01 - 2*x11*x10.
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
    Sn: dict[tuple[int, int, int, int], Fraction] = {(0, 0, 0, 0): Fraction(1)}
    for _ in range(n):
        new: dict[tuple[int, int, int, int], Fraction] = {}
        for m1, c1 in Sn.items():
            for m2, c2 in base.items():
                m = (m1[0] + m2[0], m1[1] + m2[1], m1[2] + m2[2], m1[3] + m2[3])
                new[m] = new.get(m, Fraction(0)) + c1 * c2
        Sn = new
    for m, c in Sn.items():
        add(m, Fraction(c, 2))

    # Subtract A^{2n} = (x00 + x01)^{2n}.
    for c in range(2 * n + 1):
        d = 2 * n - c
        add((0, 0, c, d), -Fraction(comb(2 * n, c)))

    # Subtract B^{2n} = (x00 + x10)^{2n}.
    for b in range(2 * n + 1):
        d = 2 * n - b
        add((0, b, 0, d), -Fraction(comb(2 * n, b)))

    # Subtract C^{2n} = (x00 + x11)^{2n}.
    for a in range(2 * n + 1):
        d = 2 * n - a
        add((a, 0, 0, d), -Fraction(comb(2 * n, a)))

    # Add back 2*x00^{2n}.
    add((0, 0, 0, 2 * n), Fraction(2))

    # Divide by P and drop zero coefficients.
    return {m: Fraction(c, P) for m, c in poly.items() if c != 0}


# ---------------------------------------------------------------------------
# Corollary helpers
# ---------------------------------------------------------------------------

def m_j_closed(n: int, j: int) -> Fraction:
    """Closed form from thm:mj-general."""
    N = 2 * n
    P = P_isotropic(n)
    Dj = 2 ** (N - j)
    num = comb(N, j) * (Fraction(Dj * Dj, 2) - Dj)
    if j % 2 == 0:
        num += comb(n, j // 2) * Fraction(Dj, 2)
    return Fraction(num, comb(N, j) * P)


def binomial_transform_moments(n: int) -> list[Fraction]:
    """B_j = E[C(t11, j)] from prop:tdist / thm:mj-general."""
    N = 2 * n
    return [Fraction(1)] + [comb(N, j) * m_j_closed(n, j) for j in range(1, N + 1)]


def t_distribution_transform(n: int) -> list[Fraction]:
    """Pr[t11 = ell] by binomial inversion of B_j."""
    N = 2 * n
    B = binomial_transform_moments(n)
    probs = []
    for ell in range(N + 1):
        total = Fraction(0)
        for j in range(ell, N + 1):
            sign = -1 if (j - ell) & 1 else 1
            total += sign * comb(j, ell) * B[j]
        probs.append(total)
    return probs


def disagreement_closed(n: int, k: int) -> Fraction:
    """Exact Pr[d = k] from the corollary: C(2n,k)/(2^{2n}-1) for k>=1, 0 for k=0."""
    if k == 0:
        return Fraction(0)
    return Fraction(comb(2 * n, k), 2 ** (2 * n) - 1)


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------

def frac_dict(poly: dict[tuple[int, ...], Fraction]) -> dict[str, str]:
    return {
        "(" + ",".join(str(v) for v in mono) + ")": str(coef)
        for mono, coef in sorted(poly.items())
    }


def frac_list(xs: list[Fraction]) -> list[str]:
    return [str(x) for x in xs]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    out_dir = Path(__file__).with_suffix("").parent.parent / "experiments" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "225-KIMI-trackI-joint-composition.json"

    results = {
        "track": "I",
        "experiment": 225,
        "prefix": "track-I:",
        "purpose": "closed-form joint generating function G_n for the four-category pairwise composition of ordered isotropic pairs",
        "claims": {
            "G_n_closed_form": "THEOREM (proved by J-twisted character sum; verified by enumeration n=2,3,4)",
            "enumeration_check": "EVIDENCE (exact enumeration, n=2,3,4; polynomial coefficients match)",
            "mj_general_rederivation": "THEOREM (specialization of G_n agrees with thm:mj-general)",
            "tdist_rederivation": "THEOREM (specialization of G_n agrees with prop:tdist)",
            "disagreement_count_law": "THEOREM (closed form Pr[d=k] = C(2n,k)/(2^{2n}-1) for k>=1)",
            "multi_pair_composition": "OPEN",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON rationals stored as strings",
            "L2_J_twist": "character sum uses (-1)^{Omega(c1,c2)} with standard symplectic form (Gram matrix J); direct sum over V x V avoids dual-space confusion",
            "L3_query_class_hygiene": "pairwise-level structural result only; no unrestricted SQ hardness claim",
        },
        "pre_register_interpretation": {
            "scope": "two-secret pairwise level only; multi-pair joint composition remains open",
            "benchmark": "Bin(2n,1/4) for t11 is the unconstrained i.i.d. row law",
            "hardness_implication": "structural generating-function result; does not by itself imply SQ hardness for full learning tasks",
        },
        "per_n": {},
        "corollaries": {},
        "verification": {},
    }

    # ------------------------------------------------------------------
    # I1 + I2: closed-form G_n and enumeration verification
    # ------------------------------------------------------------------
    all_ok = True
    for n in (2, 3, 4):
        N = 2 * n
        pairs = ordered_isotropic_pairs(n)
        P = P_isotropic(n)
        assert len(pairs) == P, (n, len(pairs), P)

        # Enumerated polynomial.
        hist: dict[tuple[int, int, int, int], int] = {}
        for c1, c2 in pairs:
            t = pair_composition(c1, c2, N)
            hist[t] = hist.get(t, 0) + 1
        enum_poly = {t: Fraction(c, P) for t, c in hist.items()}

        # Closed-form polynomial.
        form_poly = G_n_polynomial(n)

        # Point-wise sanity checks.
        point_checks = []
        for pt in ((2, 1, 1, 1), (3, 2, 1, 1), (1, 2, 3, 4)):
            x11, x10, x01, x00 = map(Fraction, pt)
            enum_val = sum(
                c
                * (x11 ** t[0])
                * (x10 ** t[1])
                * (x01 ** t[2])
                * (x00 ** t[3])
                for t, c in enum_poly.items()
            )
            form_val = G_n_eval(n, x11, x10, x01, x00)
            point_checks.append(
                {
                    "point": pt,
                    "enumerated": str(enum_val),
                    "closed_form": str(form_val),
                    "match": enum_val == form_val,
                }
            )

        # Polynomial coefficient-by-coefficient match.
        poly_match = True
        for t in set(enum_poly) | set(form_poly):
            a = enum_poly.get(t, Fraction(0))
            b = form_poly.get(t, Fraction(0))
            if a != b:
                poly_match = False
                all_ok = False
                print(f"n={n} coefficient mismatch at {t}: enum={a}, form={b}", file=sys.stderr)

        non_negative = all(c >= 0 for c in form_poly.values())
        sums_to_one = sum(form_poly.values()) == 1
        if not (poly_match and non_negative and sums_to_one):
            all_ok = False

        results["per_n"][str(n)] = {
            "N": N,
            "P_isotropic_pairs": P,
            "num_distinct_compositions": len(form_poly),
            "closed_form_polynomial": frac_dict(form_poly),
            "point_checks": point_checks,
            "polynomial_matches_enumeration": poly_match,
            "coefficients_non_negative": non_negative,
            "coefficients_sum_to_one": sums_to_one,
        }
        print(
            f"n={n}: G_n has {len(form_poly)} monomials, "
            f"enumeration match={poly_match}, non-negative={non_negative}, sums-to-one={sums_to_one}"
        )

    # ------------------------------------------------------------------
    # I3(a): re-derive thm:mj-general
    # ------------------------------------------------------------------
    mj_ok = True
    mj_checks: dict[str, list[dict[str, str]]] = {}
    for n in (2, 3, 4):
        poly = G_n_polynomial(n)
        # Marginal distribution of t11 from G_n(x,1,1,1).
        marginal_a: dict[int, Fraction] = {}
        for (a, _b, _c, _d), cf in poly.items():
            marginal_a[a] = marginal_a.get(a, Fraction(0)) + cf
        N = 2 * n
        rows = []
        for j in range(1, N + 1):
            # E[C(t11, j)] = sum_a Pr[t11=a] * C(a, j)
            exp = sum(
                marginal_a.get(a, Fraction(0)) * comb(a, j) for a in range(j, N + 1)
            )
            closed = comb(N, j) * m_j_closed(n, j)
            match = exp == closed
            if not match:
                mj_ok = False
                all_ok = False
            rows.append(
                {
                    "j": j,
                    "E_C_t11_j_from_Gn": str(exp),
                    "E_C_t11_j_from_thm_mj_general": str(closed),
                    "match": match,
                }
            )
        mj_checks[str(n)] = rows
    results["corollaries"]["thm_mj_general_rederivation"] = {
        "statement": "E[C(t11, j)] equals the closed form of thm:mj-general for all j",
        "label": "THEOREM",
        "checks": mj_checks,
        "all_match": mj_ok,
    }
    print(f"thm:mj-general re-derivation: all match = {mj_ok}")

    # ------------------------------------------------------------------
    # I3(b): re-derive prop:tdist
    # ------------------------------------------------------------------
    td_ok = True
    td_checks: dict[str, dict[str, object]] = {}
    for n in (2, 3, 4):
        poly = G_n_polynomial(n)
        marginal_a = {}
        for (a, _b, _c, _d), cf in poly.items():
            marginal_a[a] = marginal_a.get(a, Fraction(0)) + cf
        N = 2 * n
        from_gn = [marginal_a.get(ell, Fraction(0)) for ell in range(N + 1)]
        from_transform = t_distribution_transform(n)
        match = from_gn == from_transform
        if not match:
            td_ok = False
            all_ok = False
        td_checks[str(n)] = {
            "N": N,
            "from_G_n_specialization": frac_list(from_gn),
            "from_binomial_transform_of_B_j": frac_list(from_transform),
            "match": match,
            "vanishes_for_ell_ge_2n_minus_1": all(
                from_gn[ell] == 0 for ell in range(N - 1, N + 1)
            ),
        }
    results["corollaries"]["prop_tdist_rederivation"] = {
        "statement": "Pr[t11 = ell] from G_n(x,1,1,1) equals prop:tdist binomial inversion",
        "label": "THEOREM",
        "checks": td_checks,
        "all_match": td_ok,
    }
    print(f"prop:tdist re-derivation: all match = {td_ok}")

    # ------------------------------------------------------------------
    # I3(c): disagreement count d = t10 + t01
    # ------------------------------------------------------------------
    disc_ok = True
    disc_checks: dict[str, dict[str, object]] = {}
    for n in (2, 3, 4, 5, 6):
        poly = G_n_polynomial(n)
        # G_n(1, y, y, 1): marginal of d = t10 + t01.
        marginal_d: dict[int, Fraction] = {}
        for (_a, b, c, _d), cf in poly.items():
            k = b + c
            marginal_d[k] = marginal_d.get(k, Fraction(0)) + cf
        N = 2 * n
        from_gn = [marginal_d.get(k, Fraction(0)) for k in range(N + 1)]
        from_closed = [disagreement_closed(n, k) for k in range(N + 1)]
        match = from_gn == from_closed
        if not match:
            disc_ok = False
            all_ok = False
        disc_checks[str(n)] = {
            "N": N,
            "from_G_n_specialization": frac_list(from_gn),
            "from_closed_form_C_2n_k_over_2_2n_minus_1": frac_list(from_closed),
            "match": match,
            "sum_to_one": sum(from_closed) == 1,
        }
    results["corollaries"]["disagreement_count"] = {
        "statistic": "d = t10 + t01 (number of coordinates where the two rows differ)",
        "theorem": "Pr[d=0]=0 and Pr[d=k] = C(2n, k) / (2^{2n} - 1) for k = 1, ..., 2n",
        "label": "THEOREM",
        "proof": "Specialize G_n to (1, y, y, 1); S collapses to 4 and the numerator factors as (2^{2n-1} - 2)*((1+y)^{2n} - 1)",
        "checks": disc_checks,
        "all_match": disc_ok,
    }
    print(f"disagreement-count closed form: all match = {disc_ok}")

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
