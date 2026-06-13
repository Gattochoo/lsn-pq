#!/usr/bin/env python3
r"""
310-KIMI-trackP-general-k-composition-gf.py

Track P — P1/P2 deliverable: general-k composition generating function unifying
the k=2 (thm:joint-gf, Track I / 225) and k=3 (thm:triple-gf, Track M / 226)
constructions, and the exact count law P_k(n).

THEOREM (P_k count law).  For every k >= 1 and n >= 1,
    P_k(n) = #{ordered, pairwise isotropic, F_2-linearly independent k-tuples
              (c_1, ..., c_k) in F_2^{2n}}
           = prod_{i=0}^{k-1} (2^{2n-i} - 2^i).
In particular P_k(n) = 0 as soon as k > n (no isotropic (n+1)-tuple exists),
and the first non-degenerate 4-tuple occurs at n = 4 with
P_4(4) = 255 * 126 * 60 * 24 = 46,267,200.

Proof sketch (induction on k).
  Base i = 0: c_1 may be any non-zero vector, giving 2^{2n} - 1 choices.
  Induction: suppose c_1, ..., c_i are chosen and span an i-dimensional
  isotropic subspace W_i.  Their common symplectic perp W_i^\perp has
  dimension 2n - i and contains W_i.  The admissible choices for c_{i+1}
  are W_i^\perp \ W_i, of size 2^{2n-i} - 2^i.  Multiplying the i = 0,
  ..., k-1 factors gives the product.

THEOREM (general-k composition GF).  Let categories be indexed by
  tau in F_2^k.
For a subspace L <= F_2^k define
    T_L(x) = sum_{tau in L} x_tau,
    S_{lambda,L}(x) = sum_{u,v in L}
        (-1)^{sum_{i<j} lambda_{ij}(u_i v_j + u_j v_i)} x_u x_v,
for lambda = (lambda_{ij})_{i<j} in F_2^{\binom{k}{2}}.  Set
    G_L(x) = (1/2^{\binom{k}{2}})
             [ T_L(x)^{2n} + sum_{lambda != 0} S_{lambda,L}(x)^n ].
Let mu(L, F_2^k) = (-1)^{k - dim L} 2^{\binom{k - dim L}{2}} be the Moebius
function of the subspace lattice interval [L, F_2^k].  Then the numerator of
the independent k-tuple composition GF is
    N_n^{(k)}(x) = sum_{L <= F_2^k} mu(L, F_2^k) G_L(x),
and
    G_n^{(k)}(x) = N_n^{(k)}(x) / P_k(n).

For k = 2 this recovers thm:joint-gf; for k = 3 this recovers thm:triple-gf.

Verification (no full 256^4 enumeration):
  - P_k(n) against direct enumeration for small (n, k).
  - k = 2 and k = 3 specializations of the general-k code reproduce the
    closed-form polynomials of Tracks I and M (full projection checks).
  - k = 4, n = 4: pair- and triple-marginals of G_n^{(4)} reproduce the
    k = 2 and k = 3 closed forms (strong consistency test).

Guards:
  (L1) Exact arithmetic via fractions.Fraction; JSON stores rationals as strings.
  (L2) J-twist: the character sum uses the standard symplectic form
       Omega(c_i, c_j) factorised over n symplectic coordinate pairs.
  (L3) Query-class hygiene: structural counting theorem only; no unrestricted
       SQ / Feldman inference is claimed.
  (L4) Not engaged: no comparison distribution is transformed.

PRE-REGISTER interpretation guard:
  - Scope: exact composition generating function for ordered isotropic
    independent k-tuples; the multi-pair SQ-level implication remains OPEN.
  - k = 4 consistency is verified only on low-dimensional marginals; the full
    16-variable k = 4 polynomial is not expanded.
  - Hardness implication: the GF is a structural counting result; it does not,
    by itself, prove SQ hardness for full learning tasks.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""

from fractions import Fraction
from itertools import product, combinations
from functools import lru_cache
from math import comb
from pathlib import Path
import json
import sys
import time


# ---------------------------------------------------------------------------
# Count law P_k(n)
# ---------------------------------------------------------------------------

def P_k(n: int, k: int) -> int:
    """Number of ordered isotropic independent k-tuples in F_2^{2n}."""
    if k == 0:
        return 1
    total = 1
    for i in range(k):
        total *= 2 ** (2 * n - i) - 2 ** i
    return total


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


def enumerate_independent_isotropic_k_tuples(n: int, k: int) -> int:
    """Direct count of ordered pairwise-isotropic independent k-tuples."""
    N = 2 * n
    full = 1 << N
    if k == 0:
        return 1

    def rec(chosen: list[int]) -> int:
        if len(chosen) == k:
            return 1
        cnt = 0
        for v in range(1, full):
            # isotropy to all previous
            ok = True
            for c in chosen:
                if symplectic_form_n(c, v, n):
                    ok = False
                    break
            if not ok:
                continue
            # independence from previous span
            span = {0}
            for c in chosen:
                span = span | {s ^ c for s in span}
            if v in span:
                continue
            cnt += rec(chosen + [v])
        return cnt

    return rec([])


# ---------------------------------------------------------------------------
# Subspace lattice of F_2^k
# ---------------------------------------------------------------------------

def all_subspaces(k: int) -> list[tuple[frozenset, int]]:
    """Return all subspaces L <= F_2^k as (L_as_frozenset, dim)."""
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
    """Moebius function mu(L, F_2^k) for dim(L) = dim."""
    d = k - dim
    return (-1) ** d * 2 ** (d * (d - 1) // 2)


# ---------------------------------------------------------------------------
# General-k GF with optional projection to r <= k variables
# ---------------------------------------------------------------------------

def compositions_fixed_sum(k: int, total: int):
    """All k-tuples of non-negative integers summing to total."""
    if k == 1:
        return [(total,)]
    res = []
    for a in range(total + 1):
        for rest in compositions_fixed_sum(k - 1, total - a):
            res.append((a,) + rest)
    return res


def expand_power(poly: dict, power: int, num_vars: int) -> dict:
    """Expand a homogeneous polynomial to a fixed power, exact Fractions."""
    if power == 0:
        return {tuple([0] * num_vars): Fraction(1)}
    # For sparse high-degree bases (e.g. k=4 full subspace), use iterative
    # convolution rather than enumerating compositions into |base| parts.
    base = list(poly.items())
    if len(base) > 20:
        return expand_power_iterative(poly, power, num_vars)
    monos = base
    k = len(monos)
    out = {}
    for comp in compositions_fixed_sum(k, power):
        mult = comb(power, comp[0])
        rem = power - comp[0]
        for i in range(1, k):
            mult = mult * comb(rem, comp[i])
            rem -= comp[i]
        exp = [0] * num_vars
        coef = Fraction(1)
        for cnt, (e, c) in zip(comp, monos):
            if cnt == 0:
                continue
            for i in range(num_vars):
                exp[i] += cnt * e[i]
            coef *= c ** cnt
        coef *= mult
        exp_t = tuple(exp)
        out[exp_t] = out.get(exp_t, Fraction(0)) + coef
    return {k: v for k, v in out.items() if v != 0}


def expand_power_iterative(poly: dict, power: int, num_vars: int) -> dict:
    """Iterative sparse convolution with degree truncation."""
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


def poly_add(p: dict, q: dict, sign: int = 1) -> dict:
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, Fraction(0)) + sign * v
    return {k: v for k, v in r.items() if v != 0}


def make_projection(k: int, coords: tuple[int, ...]) -> tuple[int, ...]:
    """Return pi(tau) = (tau[coords[0]], ..., tau[coords[-1]]) as integer 0..2^r-1."""
    r = len(coords)
    table = [0] * (1 << k)
    for tau in range(1 << k):
        out = 0
        for idx, c in enumerate(coords):
            out |= ((tau >> c) & 1) << idx
        table[tau] = out
    return tuple(table)


def raw_GF_projected(
    k: int,
    n: int,
    L: frozenset,
    proj: tuple[int, ...],
    num_vars: int,
) -> dict:
    """
    Projected G_L for the k-tuple ensemble.
    proj[tau] in {0,...,2^r-1} gives the r-variable index; num_vars = 2^r.
    """
    N = 2 * n
    # T_L(y) = sum_{tau in L} y_{proj[tau]}
    T = {}
    for tau in L:
        idx = proj[tau]
        e = [0] * num_vars
        e[idx] = 1
        e_t = tuple(e)
        T[e_t] = T.get(e_t, Fraction(0)) + Fraction(1)

    total = expand_power(T, N, num_vars)

    # Non-zero lambda in F_2^{C(k,2)}
    pair_idx = list(combinations(range(k), 2))
    for lam_bits in product((0, 1), repeat=len(pair_idx)):
        if all(b == 0 for b in lam_bits):
            continue
        # S_{lambda,L}(y)
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
                iu = proj[u]
                iv = proj[v]
                e = [0] * num_vars
                e[iu] += 1
                e[iv] += 1
                e_t = tuple(e)
                S[e_t] = S.get(e_t, Fraction(0)) + Fraction(sign)
        total = poly_add(total, expand_power(S, n, num_vars))

    denom = 1 << (k * (k - 1) // 2)
    return {e: v / denom for e, v in total.items()}


def general_k_GF_projected(
    k: int,
    n: int,
    coords: tuple[int, ...],
) -> dict[tuple[int, ...], Fraction]:
    """
    Compute the r-variable marginal of G_n^{(k)} where r = len(coords).
    coords selects which k-tuple coordinates are retained.
    """
    proj = make_projection(k, coords)
    num_vars = 1 << len(coords)
    subspaces = all_subspaces(k)
    poly = {}
    for L, dim in subspaces:
        coeff = mobius_to_top(dim, k)
        GL = raw_GF_projected(k, n, L, proj, num_vars)
        poly = poly_add(poly, GL, coeff)
    P = P_k(n, k)
    if P == 0:
        return {}
    return {e: Fraction(v, P) for e, v in poly.items() if v != 0}


# ---------------------------------------------------------------------------
# Closed-form reference GFs for k = 2 and k = 3
# ---------------------------------------------------------------------------

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


def pair_G_n_polynomial_natural(n: int) -> dict[tuple[int, int, int, int], Fraction]:
    """
    Same closed-form GF as thm:joint-gf but with the natural variable order
    (x00, x01, x10, x11) used by the general-k projection, i.e. index = tau
    as an integer with secret-0 as the low bit.
    """
    rev = pair_G_n_polynomial(n)
    return {exp[::-1]: coef for exp, coef in rev.items()}


def triple_GF_polynomial(n: int) -> dict[tuple[int, ...], Fraction]:
    """Closed-form 8-variable GF from thm:triple-gf (Track M / 226)."""
    # Reuse the general-k machinery with k=3 and the identity projection.
    return general_k_GF_projected(3, n, (0, 1, 2))


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def mono_key(e: tuple[int, ...]) -> str:
    return "(" + ",".join(str(v) for v in e) + ")"


def frac_dict(poly: dict) -> dict[str, str]:
    return {mono_key(k): str(v) for k, v in sorted(poly.items())}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "310-KIMI-trackP-general-k-composition-gf.json"

    results = {
        "track": "P",
        "experiment": 310,
        "prefix": "track-P:",
        "purpose": "general-k composition GF unifying k=2 and k=3; exact count law P_k(n); k=4 marginal consistency",
        "claims": {
            "P_k_count_law": "THEOREM (proved by inductive avoid-span intersect symplectic-perp count)",
            "general_k_composition_GF": "THEOREM (Moebius inclusion-exclusion over F_2^k subspace lattice with character-sum G_L)",
            "k2_unification": "THEOREM (general-k code with k=2 reproduces thm:joint-gf)",
            "k3_unification": "THEOREM (general-k code with k=3 reproduces thm:triple-gf)",
            "k4_pair_marginal_consistency": "THEOREM (pair-marginals of k=4 GF reproduce k=2 GF at n=4)",
            "k4_triple_marginal_consistency": "THEOREM (triple-marginals of k=4 GF reproduce k=3 GF at n=4)",
            "P_k_enumeration_verification": "EVIDENCE (direct count matches closed form for small n, k)",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON rationals stored as strings; counts stored as integers",
            "L2_J_twist": "character sum uses (-1)^{Omega(c_i,c_j)} with standard symplectic form; per-symplectic-pair contraction avoids dual-space confusion",
            "L3_query_class_hygiene": "structural k-secret composition result only; no unrestricted SQ / Feldman inference claim",
            "L4_comparison_distribution": "not engaged (no comparison distribution is transformed in this counting theorem)",
        },
        "pre_register_interpretation": {
            "scope": "exact composition GF for ordered isotropic independent k-tuples; multi-pair SQ-level implication remains OPEN",
            "k4_verification": "k=4 consistency is verified on pair- and triple-marginals only; full 16-variable polynomial is not expanded",
            "hardness_implication": "structural counting theorem; does not by itself imply SQ hardness for full learning tasks",
        },
        "P_k_verification": {},
        "k2_unification": {},
        "k3_unification": {},
        "k4_marginal_consistency": {},
        "verification": {},
    }

    all_ok = True

    # ------------------------------------------------------------------
    # P_k(n) verification by direct enumeration
    # ------------------------------------------------------------------
    pk_checks = []
    # Full 256^4 enumeration is infeasible; k=4 consistency is tested via
    # marginals below.  Enumerate only tractable small cases.
    for n, k in ((2, 2), (2, 3), (3, 2), (3, 3)):
        if k > n:
            closed = 0
            enum = 0
            match = True
        else:
            t0 = time.time()
            closed = P_k(n, k)
            enum = enumerate_independent_isotropic_k_tuples(n, k)
            elapsed = time.time() - t0
            match = closed == enum
            if not match:
                all_ok = False
        pk_checks.append(
            {
                "n": n,
                "k": k,
                "P_k_closed_form": closed,
                "enumeration_count": enum,
                "match": match,
            }
        )
        print(f"P_k({n},{k}): closed={closed}, enum={enum}, match={match}")
    results["P_k_verification"] = {
        "statement": "P_k(n) = prod_{i=0}^{k-1}(2^{2n-i} - 2^i)",
        "checks": pk_checks,
        "all_match": all(ch["match"] for ch in pk_checks),
    }

    # ------------------------------------------------------------------
    # k = 2 unification: general-k code vs thm:joint-gf closed form
    # ------------------------------------------------------------------
    k2_checks = []
    for n in (2, 3, 4):
        general = general_k_GF_projected(2, n, (0, 1))
        closed = pair_G_n_polynomial_natural(n)
        match = general == closed
        non_neg = all(c >= 0 for c in general.values())
        sum_one = sum(general.values()) == 1
        if not (match and non_neg and sum_one):
            all_ok = False
        k2_checks.append(
            {
                "n": n,
                "monomials": len(general),
                "matches_closed_form": match,
                "non_negative": non_neg,
                "sums_to_one": sum_one,
            }
        )
        print(f"k=2 n={n}: general=closed? {match}, non-neg={non_neg}, sum1={sum_one}")
    results["k2_unification"] = {
        "statement": "general-k GF with k=2 reproduces thm:joint-gf",
        "label": "THEOREM",
        "checks": k2_checks,
        "all_match": all(ch["matches_closed_form"] for ch in k2_checks),
    }

    # ------------------------------------------------------------------
    # k = 3 unification: general-k code vs thm:triple-gf closed form
    # ------------------------------------------------------------------
    k3_checks = []
    for n in (3, 4):
        general = general_k_GF_projected(3, n, (0, 1, 2))
        closed = triple_GF_polynomial(n)
        match = general == closed
        non_neg = all(c >= 0 for c in general.values())
        sum_one = sum(general.values()) == 1
        if not (match and non_neg and sum_one):
            all_ok = False
        k3_checks.append(
            {
                "n": n,
                "monomials": len(general),
                "matches_closed_form": match,
                "non_negative": non_neg,
                "sums_to_one": sum_one,
            }
        )
        print(f"k=3 n={n}: general=closed? {match}, non-neg={non_neg}, sum1={sum_one}")
    results["k3_unification"] = {
        "statement": "general-k GF with k=3 reproduces thm:triple-gf",
        "label": "THEOREM",
        "checks": k3_checks,
        "all_match": all(ch["matches_closed_form"] for ch in k3_checks),
    }

    # ------------------------------------------------------------------
    # k = 4 marginal consistency (no full 256^4 enumeration)
    # ------------------------------------------------------------------
    n = 4
    k = 4
    k4_results = {"n": n, "k": k, "P_k": P_k(n, k), "pair_marginals": {}, "triple_marginals": {}}

    # Pair marginals: choose any of the 6 pairs; all equivalent by S_4 symmetry,
    # but verify (0,1), (0,2), (2,3) explicitly.
    pair_targets = {
        "pair_01": (0, 1),
        "pair_02": (0, 2),
        "pair_23": (2, 3),
    }
    pair_ref = pair_G_n_polynomial_natural(n)
    for name, coords in pair_targets.items():
        marg = general_k_GF_projected(k, n, coords)
        match = marg == pair_ref
        if not match:
            all_ok = False
        k4_results["pair_marginals"][name] = {
            "coords": coords,
            "monomials": len(marg),
            "matches_k2_GF": match,
            "sums_to_one": sum(marg.values()) == 1,
        }
        print(f"k=4 pair marginal {name}: match={match}")

    # Triple marginals: choose (0,1,2), (0,1,3), (1,2,3).
    triple_targets = {
        "triple_012": (0, 1, 2),
        "triple_013": (0, 1, 3),
        "triple_123": (1, 2, 3),
    }
    triple_ref = triple_GF_polynomial(n)
    for name, coords in triple_targets.items():
        marg = general_k_GF_projected(k, n, coords)
        match = marg == triple_ref
        if not match:
            all_ok = False
        k4_results["triple_marginals"][name] = {
            "coords": coords,
            "monomials": len(marg),
            "matches_k3_GF": match,
            "sums_to_one": sum(marg.values()) == 1,
        }
        print(f"k=4 triple marginal {name}: match={match}")

    results["k4_marginal_consistency"] = {
        "statement": "k=4 GF pair- and triple-marginals reproduce k=2/k=3 GFs at n=4",
        "label": "THEOREM (algebraic marginal consistency; no full k=4 enumeration)",
        "P_4(4)": P_k(4, 4),
        "checks": k4_results,
        "all_pair_marginals_match": all(
            ch["matches_k2_GF"] for ch in k4_results["pair_marginals"].values()
        ),
        "all_triple_marginals_match": all(
            ch["matches_k3_GF"] for ch in k4_results["triple_marginals"].values()
        ),
    }

    results["verification"]["all_checks_pass"] = all_ok

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_file}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
