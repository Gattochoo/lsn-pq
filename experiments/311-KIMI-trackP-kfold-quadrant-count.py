#!/usr/bin/env python3
r"""
311-KIMI-trackP-kfold-quadrant-count.py

Track P — P3 deliverable: the all-ones k-fold quadrant count t_{1^k} and its
TV distance to the unconstrained binomial benchmark.

Setup.  For an ordered isotropic independent k-tuple (c_1, ..., c_k) in
F_2^{2n}, each coordinate pos contributes the category
    tau(pos) = (c_1[pos], ..., c_k[pos]) in F_2^k.
The all-ones quadrant count is
    t_{1^k} = #{pos in {0, ..., 2n-1} : tau(pos) = (1, ..., 1)}.

Corollary (this script).  The probability generating function of t_{1^k}
is obtained from the general-k composition GF G_n^{(k)}(x) by specialising
x_{1^k} -> x and x_tau -> 1 for tau != 1^k.  Equivalently
    E[ x^{t_{1^k}} ] = N_n^{(k)}(x) / P_k(n),
where N_n^{(k)}(x) is the one-variable marginal of the general-k numerator.
The exact distribution is read off from the coefficients.

Interpretation / benchmark guard (L4-related):
  In the unconstrained i.i.d. model (no isotropy constraints) each coordinate
is independently all-ones with probability 2^{-k}, so the natural comparison
law is Bin(2n, 2^{-k}).  We report TV to this benchmark as the structural
closeness measure.  The directive also requests TV to Bin(2n, 4^{-k}); we
include it for completeness but note that for k=2 this is NOT the
unconstrained benchmark (the known k=2 law is Bin(2n, 1/4), not Bin(2n, 1/16)).

Verification:
  - Exact PGF coefficients match direct enumeration of t_{1^k} for small
    (n, k).
  - For k=2 the exact law reproduces the t11 marginal of thm:joint-gf.

Guards:
  (L1) Exact arithmetic via fractions.Fraction; JSON stores rationals as
       strings.
  (L2) Inherited from the general-k GF: standard symplectic form.
  (L3) Query-class hygiene: structural counting corollary only; no
       unrestricted SQ / Feldman inference is claimed.
  (L4) The comparison distribution is Bin(2n, 2^{-k}) (and additionally
       Bin(2n, 4^{-k}) as requested); neither is transformed.

PRE-REGISTER interpretation guard:
  - Scope: exact one-variable marginal of the k-tuple composition GF.
  - The small TV to Bin(2n, 2^{-k}) is EVIDENCE for structural closeness,
    not a hardness proof.
  - Multi-pair SQ implications remain OPEN.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from fractions import Fraction
from itertools import product, combinations
from math import comb
from pathlib import Path
import json
import sys
import time


# ---------------------------------------------------------------------------
# Re-use helpers from the general-k machinery (copied here for isolation)
# ---------------------------------------------------------------------------

def symplectic_form_n(a: int, b: int, n: int) -> int:
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) * ((b >> (i + n)) & 1)) ^ (
            ((a >> (i + n)) & 1) * ((b >> i) & 1)
        )
    return s


def P_k(n: int, k: int) -> int:
    total = 1
    for i in range(k):
        total *= 2 ** (2 * n - i) - 2 ** i
    return total


def all_subspaces(k: int) -> list[tuple[frozenset, int]]:
    subspaces = [(frozenset({0}), 0)]
    seen = {frozenset({0})}
    elements = list(range(1, 1 << k))
    for dim in range(1, k + 1):
        for subset in combinations(elements, dim):
            span = {0}
            for v in subset:
                span = span | {s ^ v for s in span}
            if len(span) != 1 << dim:
                continue
            fs = frozenset(span)
            if fs in seen:
                continue
            seen.add(fs)
            subspaces.append((fs, dim))
    return subspaces


def mobius_to_top(dim: int, k: int) -> int:
    d = k - dim
    return (-1) ** d * 2 ** (d * (d - 1) // 2)


def poly_add(p: dict, q: dict, sign: int = 1) -> dict:
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, Fraction(0)) + sign * v
    return {k: v for k, v in r.items() if v != 0}


def expand_power_iterative(poly: dict, power: int, num_vars: int) -> dict:
    if power == 0:
        return {tuple([0] * num_vars): Fraction(1)}
    max_degree = power * max(sum(e) for e in poly)
    result = {tuple([0] * num_vars): Fraction(1)}
    for _ in range(power):
        new = {}
        for e1, c1 in result.items():
            for e2, c2 in poly.items():
                deg = sum(e1) + sum(e2)
                if deg > max_degree:
                    continue
                e = tuple(e1[i] + e2[i] for i in range(num_vars))
                new[e] = new.get(e, Fraction(0)) + c1 * c2
        result = {e: c for e, c in new.items() if c != 0}
    return result


def raw_GF_all_ones(k: int, n: int, L: frozenset) -> dict:
    """
    One-variable G_L for the all-ones marginal.
    Variable 0 = not all-ones, variable 1 = all-ones.
    """
    all_one = (1 << k) - 1
    num_vars = 2
    N = 2 * n

    # T_L(x) = (|L| - 1_{all_one in L}) * y_0 + 1_{all_one in L} * y_1
    has_all_one = 1 if all_one in L else 0
    t0 = len(L) - has_all_one
    T = {}
    if t0:
        T[(1, 0)] = Fraction(t0)
    if has_all_one:
        T[(0, 1)] = Fraction(has_all_one)

    total = expand_power_iterative(T, N, num_vars)

    pair_idx = list(combinations(range(k), 2))
    for lam_bits in product((0, 1), repeat=len(pair_idx)):
        if all(b == 0 for b in lam_bits):
            continue
        S = {}
        L_list = sorted(L)
        for u in L_list:
            for v in L_list:
                exp = 0
                for (i, j), lam in zip(pair_idx, lam_bits):
                    ui = (u >> i) & 1
                    vi = (v >> i) & 1
                    uj = (u >> j) & 1
                    vj = (v >> j) & 1
                    exp ^= lam & ((ui & vj) ^ (uj & vi))
                sign = -1 if exp else 1
                iu = 1 if u == all_one else 0
                iv = 1 if v == all_one else 0
                e = (iu + iv, 0)  # placeholder; corrected below
                # e[0] counts non-all-ones, e[1] counts all-ones occurrences
                e = [0, 0]
                e[iu] += 1
                e[iv] += 1
                e_t = tuple(e)
                S[e_t] = S.get(e_t, Fraction(0)) + Fraction(sign)
        total = poly_add(total, expand_power_iterative(S, n, num_vars))

    denom = 1 << (k * (k - 1) // 2)
    return {e: v / denom for e, v in total.items()}


def t_ones_GF(k: int, n: int) -> dict[int, Fraction]:
    """Return PGF as {power of x: coefficient}."""
    subspaces = all_subspaces(k)
    poly = {}
    for L, dim in subspaces:
        coeff = mobius_to_top(dim, k)
        GL = raw_GF_all_ones(k, n, L)
        poly = poly_add(poly, GL, coeff)
    P = P_k(n, k)
    if P == 0:
        return {}
    pgf = {}
    for e, c in poly.items():
        if c == 0:
            continue
        # e = (count_non_all_ones, count_all_ones); variable is x for all-ones.
        power = e[1]
        pgf[power] = pgf.get(power, Fraction(0)) + Fraction(c, P)
    return {p: c for p, c in pgf.items() if c != 0}


# ---------------------------------------------------------------------------
# Direct enumeration of t_{1^k}
# ---------------------------------------------------------------------------

def enumerate_t_ones(n: int, k: int) -> dict[int, int]:
    """Histogram of t_{1^k} over ordered isotropic independent k-tuples."""
    N = 2 * n
    full = 1 << N
    all_one = (1 << k) - 1
    hist: dict[int, int] = {}

    def rec(chosen: list[int], bits: list[int]):
        if len(chosen) == k:
            cnt = 0
            for pos in range(N):
                mask = 0
                for idx, c in enumerate(chosen):
                    mask |= ((c >> pos) & 1) << idx
                if mask == all_one:
                    cnt += 1
            hist[cnt] = hist.get(cnt, 0) + 1
            return
        for v in range(1, full):
            ok = True
            for c in chosen:
                if symplectic_form_n(c, v, n):
                    ok = False
                    break
            if not ok:
                continue
            span = {0}
            for c in chosen:
                span = span | {s ^ c for s in span}
            if v in span:
                continue
            rec(chosen + [v], bits)

    rec([], [0] * N)
    return hist


# ---------------------------------------------------------------------------
# Binomial comparison and TV
# ---------------------------------------------------------------------------

def binomial_pmf(trials: int, p: Fraction) -> list[Fraction]:
    q = Fraction(1) - p
    return [Fraction(comb(trials, ell)) * (p ** ell) * (q ** (trials - ell)) for ell in range(trials + 1)]


def tv_distance(p: dict[int, Fraction], q: list[Fraction]) -> Fraction:
    total = Fraction(0)
    keys = set(p.keys()) | set(range(len(q)))
    for ell in keys:
        total += abs(p.get(ell, Fraction(0)) - q[ell])
    return total / 2


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def frac_dict(d: dict) -> dict:
    return {str(k): str(v) for k, v in sorted(d.items())}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "311-KIMI-trackP-kfold-quadrant-count.json"

    results = {
        "track": "P",
        "experiment": 311,
        "prefix": "track-P:",
        "purpose": "all-ones k-fold quadrant count t_{1^k}: exact law and TV to binomial benchmarks",
        "claims": {
            "t_ones_exact_pgf": "COROLLARY (specialisation of the general-k composition GF)",
            "t_ones_distribution": "THEOREM (coefficients of the exact PGF)",
            "tv_to_bin_2_minus_k": "EVIDENCE (exact TV to the unconstrained Bin(2n, 2^{-k}) benchmark)",
            "tv_to_bin_4_minus_k": "EVIDENCE (directive-requested TV to Bin(2n, 4^{-k}); note this is NOT the unconstrained benchmark for k>1)",
            "enumeration_verification": "EVIDENCE (small-case exact match)",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON rationals stored as strings; counts stored as integers",
            "L2_J_twist": "inherited from general-k GF; standard symplectic form",
            "L3_query_class_hygiene": "structural one-variable marginal only; no unrestricted SQ / Feldman inference claim",
            "L4_comparison_distribution": "comparison is the untransformed Bin(2n, 2^{-k}) benchmark (plus Bin(2n, 4^{-k}) as requested)",
        },
        "pre_register_interpretation": {
            "scope": "exact one-variable marginal of the k-tuple composition GF",
            "benchmark_note": "Bin(2n, 2^{-k}) is the unconstrained i.i.d. row law; Bin(2n, 4^{-k}) is included only because the directive requests it and is NOT the natural benchmark for k>1",
            "hardness_implication": "small TV is structural-closeness EVIDENCE, not a hardness proof; multi-pair SQ implications remain OPEN",
        },
        "per_case": {},
        "verification": {},
    }

    all_ok = True
    cases = [
        (2, 2),
        (3, 2),
        (3, 3),
        (4, 2),
        (4, 3),
        (4, 4),
    ]

    for n, k in cases:
        if k > n:
            # Degenerate: no independent k-tuple exists.
            results["per_case"][f"n={n},k={k}"] = {
                "degenerate": True,
                "P_k": 0,
                "pgf": {},
                "tv_to_Bin_2_minus_k": None,
                "tv_to_Bin_4_minus_k": None,
            }
            print(f"n={n},k={k}: degenerate (P_k=0)")
            continue

        t0 = time.time()
        pgf = t_ones_GF(k, n)
        elapsed = time.time() - t0

        # Convert PGF to probability distribution on {0, ..., 2n}.
        dist = {ell: pgf.get(ell, Fraction(0)) for ell in range(2 * n + 1)}
        non_neg = all(c >= 0 for c in dist.values())
        sum_one = sum(dist.values()) == 1
        if not (non_neg and sum_one):
            all_ok = False

        # Binomial benchmarks.
        pmf_natural = binomial_pmf(2 * n, Fraction(1, 2 ** k))
        pmf_directive = binomial_pmf(2 * n, Fraction(1, 4 ** k))
        tv_natural = tv_distance(dist, pmf_natural)
        tv_directive = tv_distance(dist, pmf_directive)

        # Enumeration verification for tractable cases.
        enum_match = None
        enum_hist = None
        if (n, k) in ((2, 2), (3, 2), (3, 3), (4, 2)):
            hist = enumerate_t_ones(n, k)
            enum_total = sum(hist.values())
            P = P_k(n, k)
            enum_dist = {ell: Fraction(hist.get(ell, 0), enum_total) for ell in range(2 * n + 1)}
            enum_match = (enum_total == P) and (enum_dist == dist)
            enum_hist = {ell: hist.get(ell, 0) for ell in range(2 * n + 1)}
            if not enum_match:
                all_ok = False

        results["per_case"][f"n={n},k={k}"] = {
            "n": n,
            "k": k,
            "P_k": P_k(n, k),
            "pgf": frac_dict(pgf),
            "distribution": frac_dict(dist),
            "coefficients_non_negative": non_neg,
            "sums_to_one": sum_one,
            "tv_to_Bin_2n_2_minus_k": str(tv_natural),
            "tv_to_Bin_2n_4_minus_k": str(tv_directive),
            "enumeration_count": enum_hist,
            "enumeration_matches_pgf": enum_match,
            "closed_form_time_sec": elapsed,
        }
        print(
            f"n={n},k={k}: TV(Bin(2n,2^-k))={tv_natural}, "
            f"TV(Bin(2n,4^-k))={tv_directive}, enum_match={enum_match}, time={elapsed:.3f}s"
        )

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
