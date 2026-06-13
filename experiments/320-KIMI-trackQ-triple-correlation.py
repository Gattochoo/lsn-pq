#!/usr/bin/env python3
"""
320-KIMI-trackQ-triple-correlation.py

Track Q deliverable: exact 3-wise correlation of bundle/parity queries for the
sympLPN formulation, computed under the isotropic ensemble.

Setup (sympLPN, restricted 3-local parity query class):
  - Secret x in F_2^n.
  - One sample is (A, y) with A ~ A_n (uniform full-rank isotropic matrix,
    equivalently a uniform ordered basis of a uniform Lagrangian L) and
    y = A x + e, e ~ Bernoulli(p)^{2n}.
  - Reference distribution D_0: same A and y ~ Unif(F_2^{2n}) independent.
  - For a fixed non-empty S subseteq [2n] with |S| = k, the k-local parity
    query is h^{(S)}(A, y) = (-1)^{sum_{i in S} y_i}.
  - Its conditional expectation (advantage function) under secret x is
        g_x(A) = E_{D_x | A}[h^{(S)}]
               = (-1)^{<1_S, A x>} (1 - 2 p)^k.

THEOREM (this script):
  For every fixed non-empty S subseteq [2n] and all secrets x, x', x'' in F_2^n,
  the 3-wise correlation under D_0 (i.e. averaging only over A, since the noise
  expectations have already been taken inside g_x) is

      E_{A ~ A_n}[ g_x(A) g_{x'}(A) g_{x''}(A) ]
        = (1 - 2 p)^{3k}                         if x + x' + x'' = 0,
        = -(1 - 2 p)^{3k} / (2^{2n} - 1)         otherwise.

  Equivalently, writing w = x + x' + x'',
      E_A[(-1)^{<1_S, A w>}] =  1                if w = 0,
                              = -1/(2^{2n} - 1) if w != 0,
  for every non-empty S.

Connection to thm:triple-gf:
  For linearly independent x, x', x'' the three vectors
  (c_1, c_2, c_3) = (A x, A x', A x'') form a uniform ordered independent
  isotropic triple in L.  The sign expectation
  E[(-1)^{<1_S, c_1 + c_2 + c_3>}] is the specialization of the triple
  composition GF with variables x_tau = (-1)^{<1_S, tau>}.  We verify this
  specialization against the closed form above at n = 3, 4 by loading the
  Track M triple-GF output and evaluating the same parity specialization.

Guards:
  L1: fractions.Fraction everywhere; JSON stores rationals as strings.
  L2: symplectic-form conventions inherited from experiments/lib; the sign
      uses the standard dot product on F_2^{2n} and the J-twist is handled
      by the Lagrangian character sum already present in Track M.
  L3: results are stated only for the RESTRICTED 3-local-parity query class.
      They do NOT plug into cor:symplpn-sq, whose Feldman application requires
      arbitrary bounded queries.  The restricted-SQ implication is labelled OPEN.
  L4: no comparison distribution is transformed.

PRE-REGISTER interpretation guard:
  - Scope: exact correlation for 3-local parity queries on one sympLPN block.
  - Benchmark: in the unconstrained LPN ensemble, A w is uniform over F_2^{2n}
    and the off-diagonal 3-wise correlation is exactly 0; under isotropic A_n
    it is -.../(2^{2n}-1), an exponentially small negative deviation.
  - Hardness implication: small 3-wise correlations are EVIDENCE that the
    isotropic conditioning does not help a 3-local-parity distinguisher; any
    SQ lower bound for this restricted query class requires a separate
    restricted-SQ theorem (OPEN).

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import comb
from pathlib import Path

# Shared library: Lagrangian enumeration (read-only use).
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n


P = Fraction(1, 4)          # standard verification noise rate
K_LOCAL = 3                 # restricted 3-local parity query class


def dot_parity(mask: int, v: int) -> int:
    """Parity of <mask, v> over F_2."""
    return (mask & v).bit_count() & 1


def span_set(basis: tuple[int, ...]) -> set[int]:
    """Full (including 0) span of an ordered basis over F_2."""
    span = {0}
    for b in basis:
        span |= {s ^ b for s in span}
    return span


def triple_correlation_formula(n: int, k: int, w_zero: bool) -> Fraction:
    """Closed-form 3-wise correlation for a k-local parity query."""
    d = Fraction((1 - 2 * P) ** (3 * k))
    if w_zero:
        return d
    return -d / Fraction(2 ** (2 * n) - 1)


def sign_expectation_formula(n: int, w_zero: bool) -> Fraction:
    """E_A[(-1)^{<1_S, A w>}] for non-empty S."""
    if w_zero:
        return Fraction(1)
    return -Fraction(1, 2 ** (2 * n) - 1)


def enumerate_independent_triples(bases: list[tuple[int, ...]]):
    """
    Yield, for every Lagrangian L in `bases`, every ordered independent triple
    (c1, c2, c3) of non-zero vectors in L.  Each triple is yielded once.
    """
    for basis in bases:
        L = list(span_set(basis) - {0})
        # c1 != 0
        for c1 in L:
            # c2 != 0, c2 != c1
            for c2 in L:
                if c2 == c1:
                    continue
                c1_xor_c2 = c1 ^ c2
                # c3 != 0, not c1, not c2, not c1^c2
                for c3 in L:
                    if c3 == c1 or c3 == c2 or c3 == c1_xor_c2:
                        continue
                    yield c1, c2, c3


def enumerate_sumzero_pairs(bases: list[tuple[int, ...]]):
    """
    Yield, for every Lagrangian L in `bases`, every ordered independent pair
    (c1, c2) of non-zero vectors in L.  The corresponding sum-zero triple is
    (c1, c2, c1 ^ c2).
    """
    for basis in bases:
        L = list(span_set(basis) - {0})
        for c1 in L:
            for c2 in L:
                if c2 == c1:
                    continue
                yield c1, c2


def enum_sign_average_independent(bases: list[tuple[int, ...]], s_mask: int) -> Fraction:
    """Average of (-1)^{<s_mask, c1+c2+c3>} over all ordered independent triples."""
    total_sign = 0
    count = 0
    for c1, c2, c3 in enumerate_independent_triples(bases):
        total_sign += 1 if dot_parity(s_mask, c1 ^ c2 ^ c3) == 0 else -1
        count += 1
    return Fraction(total_sign, count)


def enum_sign_average_sumzero(bases: list[tuple[int, ...]], s_mask: int) -> Fraction:
    """Average sign for sum-zero dependent triples; should be exactly 1."""
    total_sign = 0
    count = 0
    for c1, c2 in enumerate_sumzero_pairs(bases):
        c3 = c1 ^ c2
        total_sign += 1 if dot_parity(s_mask, c1 ^ c2 ^ c3) == 0 else -1
        count += 1
    return Fraction(total_sign, count)


def load_triple_gf_poly(n: int) -> dict[tuple[int, ...], Fraction]:
    """Load the Track M triple-GF probability polynomial for the given n."""
    src = Path(__file__).parent / "output" / "226-KIMI-trackM-triple-gf.json"
    with open(src) as f:
        data = json.load(f)
    poly_raw = data["per_n"][str(n)]["probability_polynomial"]
    poly: dict[tuple[int, ...], Fraction] = {}
    for k, v in poly_raw.items():
        inner = k.strip("()")
        e = tuple(int(x) for x in inner.split(","))
        poly[e] = Fraction(v)
    return poly


def triple_gf_sign_expectation(n: int) -> Fraction:
    """
    Evaluate the triple GF at x_tau = (-1)^{tau_1 + tau_2 + tau_3}.
    This is E[(-1)^{<1, c1+c2+c3>}] over ordered independent triples.
    """
    poly = load_triple_gf_poly(n)
    cats = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    total = Fraction(0)
    for e, prob in poly.items():
        # e lists counts for cats in the order 000,001,010,011,100,101,110,111.
        exponent = 0
        for cnt, tau in zip(e, cats):
            parity = (tau[0] ^ tau[1] ^ tau[2]) & 1
            exponent += cnt * parity
        total += prob * (Fraction(-1) ** exponent)
    return total


def average_abs_triple_correlation(n: int, k: int) -> Fraction:
    """
    Average |3-wise correlation| over all secret triples (x,x',x'') in (F_2^n)^3.
    Count of triples with x+x'+x''=0 is 4^n; remaining 8^n - 4^n have magnitude
    d/(2^{2n}-1).
    """
    d = Fraction((1 - 2 * P) ** (3 * k))
    N2 = 2 ** n
    N4 = 4 ** n
    N8 = 8 ** n
    diag = N4 * d
    off = (N8 - N4) * d / Fraction(2 ** (2 * n) - 1)
    return Fraction(diag + off, N8)


def main() -> int:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "320-KIMI-trackQ-triple-correlation.json"

    results = {
        "track": "Q",
        "experiment": 320,
        "prefix": "track-Q:",
        "purpose": "exact 3-wise correlation of restricted 3-local parity queries in sympLPN",
        "p": str(P),
        "k_local": K_LOCAL,
        "theorem": {
            "statement": "For a fixed non-empty S with |S|=k and secrets x,x',x'', E_A[g_x g_{x'} g_{x''}] = (1-2p)^{3k} if x+x'+x''=0, else -(1-2p)^{3k}/(2^{2n}-1).",
            "label": "THEOREM",
        },
        "claims": {
            "exact_triple_correlation": "THEOREM",
            "enumeration_verification_n3": "EVIDENCE",
            "enumeration_verification_n4": "EVIDENCE",
            "triple_gf_consistency": "EVIDENCE",
            "restricted_sq_implication": "OPEN (needs a cited restricted-SQ theorem for k-local parities)",
            "no_unrestricted_feldman": "GUARD (L3)",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON rationals stored as strings",
            "L2_J_twist": "sign uses standard dot product; Lagrangian character sum / symplectic form handled by Track M triple-GF",
            "L3_query_class_hygiene": "results stated only for the restricted 3-local-parity query class; they do NOT plug into cor:symplpn-sq's unrestricted Feldman bound",
            "L4_comparison_distribution": "not engaged (no comparison distribution transformed)",
        },
        "pre_register_interpretation": {
            "scope": "exact correlation for 3-local parity queries on one sympLPN block",
            "benchmark": "unconstrained LPN gives 0 off-diagonal 3-wise correlation; isotropic ensemble gives -d/(2^{2n}-1)",
            "hardness_implication": "EVIDENCE that isotropic conditioning does not help a 3-local-parity distinguisher; any SQ lower bound for this restricted class is OPEN",
        },
        "per_n": {},
        "verification": {},
    }

    all_ok = True

    # Masks for verification: 3-local and full-block parity.
    for n in (3, 4):
        N = 2 * n
        s_local = (1 << K_LOCAL) - 1          # first 3 rows
        s_all = (1 << N) - 1                  # all rows

        per_n: dict[str, object] = {
            "N": N,
            "s_local_mask": s_local,
            "s_all_mask": s_all,
        }

        # Closed-form values.
        d_local = Fraction((1 - 2 * P) ** (3 * K_LOCAL))
        corr_sumzero = triple_correlation_formula(n, K_LOCAL, w_zero=True)
        corr_nonsum = triple_correlation_formula(n, K_LOCAL, w_zero=False)
        sign_sumzero = sign_expectation_formula(n, w_zero=True)
        sign_nonsum = sign_expectation_formula(n, w_zero=False)

        per_n["closed_form"] = {
            "d_local": str(d_local),
            "correlation_sumzero": str(corr_sumzero),
            "correlation_nonsum": str(corr_nonsum),
            "sign_expectation_sumzero": str(sign_sumzero),
            "sign_expectation_nonsum": str(sign_nonsum),
        }

        # Enumerate one ordered basis per Lagrangian once, then reuse.
        t0 = time.time()
        bases = enumerate_lagrangian_bases_n(n)
        enum_bases_time = time.time() - t0

        # Direct enumeration over Lagrangians / vector triples.
        t0 = time.time()
        avg_sign_local_ind = enum_sign_average_independent(bases, s_local)
        avg_sign_all_ind = enum_sign_average_independent(bases, s_all)
        enum_ind_time = time.time() - t0

        t0 = time.time()
        avg_sign_local_sz = enum_sign_average_sumzero(bases, s_local)
        avg_sign_all_sz = enum_sign_average_sumzero(bases, s_all)
        enum_sz_time = time.time() - t0

        corr_local_ind = d_local * avg_sign_local_ind
        corr_all_ind = d_local * avg_sign_all_ind
        corr_local_sz = d_local * avg_sign_local_sz
        corr_all_sz = d_local * avg_sign_all_sz

        checks = {
            "independent_sum_local": {
                "description": "secrets e1, e2, e3 (sum != 0), 3-local parity",
                "enum_avg_sign": str(avg_sign_local_ind),
                "formula_avg_sign": str(sign_nonsum),
                "enum_correlation": str(corr_local_ind),
                "formula_correlation": str(corr_nonsum),
                "match": avg_sign_local_ind == sign_nonsum and corr_local_ind == corr_nonsum,
            },
            "independent_sum_all": {
                "description": "secrets e1, e2, e3 (sum != 0), full-block parity",
                "enum_avg_sign": str(avg_sign_all_ind),
                "formula_avg_sign": str(sign_nonsum),
                "enum_correlation": str(corr_all_ind),
                "formula_correlation": str(corr_nonsum),
                "match": avg_sign_all_ind == sign_nonsum and corr_all_ind == corr_nonsum,
            },
            "sum_zero_local": {
                "description": "secrets e1, e2, e1+e2 (sum = 0), 3-local parity",
                "enum_avg_sign": str(avg_sign_local_sz),
                "formula_avg_sign": str(sign_sumzero),
                "enum_correlation": str(corr_local_sz),
                "formula_correlation": str(corr_sumzero),
                "match": avg_sign_local_sz == sign_sumzero and corr_local_sz == corr_sumzero,
            },
            "sum_zero_all": {
                "description": "secrets e1, e2, e1+e2 (sum = 0), full-block parity",
                "enum_avg_sign": str(avg_sign_all_sz),
                "formula_avg_sign": str(sign_sumzero),
                "enum_correlation": str(corr_all_sz),
                "formula_correlation": str(corr_sumzero),
                "match": avg_sign_all_sz == sign_sumzero and corr_all_sz == corr_sumzero,
            },
        }
        for ch in checks.values():
            if not ch["match"]:
                all_ok = False

        per_n["enumeration"] = {
            "bases_time_sec": enum_bases_time,
            "independent_time_sec": enum_ind_time,
            "sumzero_time_sec": enum_sz_time,
            "checks": checks,
        }

        # Triple-GF consistency check (independent case only, S = all rows).
        t0 = time.time()
        gf_sign = triple_gf_sign_expectation(n)
        gf_time = time.time() - t0
        gf_match = gf_sign == sign_nonsum
        if not gf_match:
            all_ok = False

        per_n["triple_gf"] = {
            "specialization": "x_tau = (-1)^{tau_1+tau_2+tau_3}",
            "gf_sign_expectation": str(gf_sign),
            "formula_sign_expectation": str(sign_nonsum),
            "match": gf_match,
            "time_sec": gf_time,
        }

        # Average absolute triple correlation over all secret triples.
        avg_abs = average_abs_triple_correlation(n, K_LOCAL)
        per_n["average_abs_triple_correlation"] = {
            "value": str(avg_abs),
            "note": "average over all (x,x',x'') in (F_2^n)^3 of |E_A[g_x g_{x'} g_{x''}]|",
        }

        results["per_n"][str(n)] = per_n

        print(
            f"n={n}: independent avg sign (local/all) = {avg_sign_local_ind} / {avg_sign_all_ind}; "
            f"sum-zero avg sign = {avg_sign_local_sz}; "
            f"GF sign = {gf_sign}; avg_abs = {avg_abs}"
        )

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
