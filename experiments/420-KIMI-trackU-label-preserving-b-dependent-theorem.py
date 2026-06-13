#!/usr/bin/env python3
"""420 (Track U): exact same-secret SD for label-preserving b-dependent bijections.

A label-preserving b-dependent point map is a public bijection

    g_i(x,b) = (phi_{i,b}(x), b),

where for each label bit b the map phi_{i,b}: F_2^{2n} -> F_2^{2n} is a bijection.
The split sends one LSN sample (x,b) to the pair (g_0(x,b), g_1(x,b)).

U1. THEOREM.  Under the natural same-secret comparison to two independent fresh
    samples from D_L, the exact statistical distance is

        SD = 1 - (p^2 + (1-p)^2) / 4^n
             + (1-2p)^2 / (2 * 4^n) * (2 - A_0 - A_1),

    where for beta in {0,1}

        A_beta = Pr_{L,x}[ 1_L(phi_{0,beta} x) = 1_L(phi_{1,beta} x) ].

    Consequently A_beta <= 1 with equality iff phi_{0,beta} = phi_{1,beta},
    so the label-preserving universal minimum

        SD_min = 1 - (p^2 + (1-p)^2) / 4^n

    is a lower bound for this family, attained exactly when g_0 = g_1
    (the literal duplicate).

Verification:
  * Direct exact enumeration vs. the closed form for representative cases.
  * Reproduction / verification of exp/341 (Claude bijectivity audit) and
    exp/330 (Track R) label-preserving data points.
  * Every tested map is explicitly asserted to be a bijection (the R lesson).

Guards:
  L1 exact arithmetic: Fractions/integer counts; JSON stores string fractions.
  L2 duality care: not invoked (no character sums over Lagrangians).
  L3 query-class hygiene: exact TV statements only; no SQ/Feldman inference.
  L4 comparison distribution: the fresh pair (u1,b1,u2,b2) is never transformed.

Discipline: Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.
"""
import argparse
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases_n, symplectic_form_n

P_NOISE = Fraction(1, 4)


def all_lagrangians(n: int) -> list[set[int]]:
    """Return all Lagrangian subspaces of F_2^{2n} as sets of vectors."""
    bases = enumerate_lagrangian_bases_n(n)
    subs = []
    for basis in bases:
        span = [0]
        for v in basis:
            span += [s ^ v for s in span]
        subs.append(set(span))
    return subs


def is_bijection(perm: list[int]) -> bool:
    """A list is a bijection of {0,...,len-1} iff it is a permutation."""
    return sorted(perm) == list(range(len(perm)))


def assert_bijections(phi0: list[list[int]], phi1: list[list[int]]) -> None:
    """Assert every branch map is a bijection; raise loudly if not."""
    for b in (0, 1):
        assert is_bijection(phi0[b]), f"phi_0[{b}] is not a bijection"
        assert is_bijection(phi1[b]), f"phi_1[{b}] is not a bijection"


def apply_matrix_cols(cols: tuple[int, ...], x: int) -> int:
    """Apply a matrix given as columns to a vector x over F_2."""
    y = 0
    for i, col in enumerate(cols):
        if (x >> i) & 1:
            y ^= col
    return y


def det_f2(cols: tuple[int, ...]) -> int:
    """Determinant (0 or 1) of an N x N matrix over F_2 given as columns."""
    N = len(cols)
    rows = [0] * N
    for j, col in enumerate(cols):
        for i in range(N):
            if (col >> i) & 1:
                rows[i] |= 1 << j
    pivots = {}
    for r in rows:
        x = r
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return 1 if len(pivots) == N else 0


def is_symplectic_matrix(cols: tuple[int, ...], n: int) -> bool:
    """Check that columns form a symplectic matrix w.r.t. the standard form."""
    N = 2 * n
    basis = [1 << i for i in range(N)]
    for i in range(N):
        for j in range(N):
            if symplectic_form_n(cols[i], cols[j], n) != symplectic_form_n(basis[i], basis[j], n):
                return False
    return True


def enumerate_sp4() -> list[tuple[int, ...]]:
    """Brute-force enumerate Sp(4,F_2) (720 elements)."""
    n = 2
    N = 4
    out = []
    for bits in range(1 << (N * N)):
        cols = []
        for j in range(N):
            col = 0
            for i in range(N):
                if (bits >> (j * N + i)) & 1:
                    col |= 1 << i
            cols.append(col)
        if det_f2(cols) and is_symplectic_matrix(tuple(cols), n):
            out.append(tuple(cols))
    return out


def enumerate_gl(n: int) -> list[tuple[int, ...]]:
    """Enumerate all invertible n x n matrices over F_2 as column tuples."""
    N = n
    out = []
    for bits in range(1 << (N * N)):
        cols = []
        for j in range(N):
            col = 0
            for i in range(N):
                if (bits >> (j * N + i)) & 1:
                    col |= 1 << i
            cols.append(col)
        if det_f2(cols):
            out.append(tuple(cols))
    return out


def random_bijection(size: int, rng: random.Random) -> list[int]:
    """Return a random permutation of {0,...,size-1}."""
    perm = list(range(size))
    rng.shuffle(perm)
    return perm


def random_symplectic_perm(n: int, rng: random.Random) -> list[int]:
    """Generate a random element of Sp(2n,F_2) as a permutation of F_2^{2n}."""
    size = 1 << (2 * n)
    perm = list(range(size))
    for _ in range(rng.randint(6, 14)):
        v = rng.randrange(1, size)
        perm = [perm[x] ^ (v if symplectic_form_n(perm[x], v, n) else 0) for x in range(size)]
    return perm


def agreement_A(n: int, lags: list[set[int]], f1: list[int], f2: list[int]) -> Fraction:
    """A = Pr_{L,x}[ 1_L(f1 x) = 1_L(f2 x) ], x uniform over F_2^{2n}."""
    size = 1 << (2 * n)
    total = 0
    for x in range(size):
        u, v = f1[x], f2[x]
        total += sum(1 for L in lags if (u in L) == (v in L))
    return Fraction(total, len(lags) * size)


def universal_minimum(n: int, p: Fraction = P_NOISE) -> Fraction:
    """Orbit/universal minimum 1 - (p^2+(1-p)^2)/4^n."""
    return Fraction(1) - (p * p + (1 - p) * (1 - p)) / (4 ** n)


def sd_label_preserving_b_dependent_theorem(
    n: int, A0: Fraction, A1: Fraction, p: Fraction = P_NOISE
) -> Fraction:
    """Closed-form exact SD for the label-preserving b-dependent family (U1)."""
    base = universal_minimum(n, p)
    correction = ((1 - 2 * p) ** 2) * (2 - A0 - A1) / (2 * (4 ** n))
    return base + correction


def exact_sd_label_preserving_b_dependent(
    n: int,
    lags: list[set[int]],
    phi0: list[list[int]],
    phi1: list[list[int]],
    p: Fraction = P_NOISE,
) -> Fraction:
    """Exact SD for label-preserving b-dependent split vs. untransformed fresh pair.

    g_i(x,b) = (phi_{i,b}(x), b).  The fresh comparison pair is left in the
    natural domain (L4 guard).
    """
    assert_bijections(phi0, phi1)

    N = 2 * n
    size = 1 << N
    pnum = p.numerator
    qnum = p.denominator - p.numerator
    denom = p.denominator

    D_P = len(lags) * size * denom * denom
    D_Q = len(lags) * size * size * denom * denom

    counts_P: dict[int, int] = {}
    counts_Q: dict[int, int] = {}

    for L in lags:
        mask = 0
        for v in L:
            mask |= 1 << v
        # Split side: g_i(x,b) with b = c \oplus e, label preserved.
        for x in range(size):
            c = (mask >> x) & 1
            for e in (0, 1):
                b = c ^ e
                x0 = phi0[b][x]
                x1 = phi1[b][x]
                key = (x0 << (N + 2)) | (b << (N + 1)) | (x1 << 1) | b
                w = (qnum if e == 0 else pnum) * denom
                counts_P[key] = counts_P.get(key, 0) + w
        # Fresh comparison side: unchanged.
        for u1 in range(size):
            c1 = (mask >> u1) & 1
            for u2 in range(size):
                c2 = (mask >> u2) & 1
                for e1 in (0, 1):
                    b1 = c1 ^ e1
                    w1 = qnum if e1 == 0 else pnum
                    for e2 in (0, 1):
                        b2 = c2 ^ e2
                        w2 = qnum if e2 == 0 else pnum
                        key = (u1 << (N + 2)) | (b1 << (N + 1)) | (u2 << 1) | b2
                        counts_Q[key] = counts_Q.get(key, 0) + w1 * w2

    num = 0
    keys = set(counts_P.keys()) | set(counts_Q.keys())
    for k in keys:
        num += abs(counts_P.get(k, 0) * D_Q - counts_Q.get(k, 0) * D_P)
    return Fraction(num, 2 * D_P * D_Q)


def build_duplicate(n: int) -> tuple[list[list[int]], list[list[int]]]:
    """Literal duplicate: g_0 = g_1 = identity for both labels."""
    size = 1 << (2 * n)
    ident = [list(range(size)), list(range(size))]
    return ident, ident


def build_transposition_only(n: int) -> tuple[list[list[int]], list[list[int]]]:
    """exp/341 transposition-only case: phi_{1,1} = (0 1), all others identity."""
    size = 1 << (2 * n)
    assert size >= 2
    swap01 = list(range(size))
    swap01[0], swap01[1] = swap01[1], swap01[0]
    phi0 = [list(range(size)), list(range(size))]
    phi1 = [list(range(size)), swap01]
    return phi0, phi1


def build_named_cases(n: int, rng: random.Random) -> list[dict]:
    """Build representative label-preserving b-dependent cases."""
    size = 1 << (2 * n)
    ident = list(range(size))
    sp4 = enumerate_sp4()
    gl4 = enumerate_gl(4)

    cases: list[dict] = []

    # 1. literal duplicate
    phi0, phi1 = build_duplicate(n)
    cases.append({"name": "duplicate", "phi0": phi0, "phi1": phi1})

    # 2. transposition-only (exp/341 / exp 330)
    phi0, phi1 = build_transposition_only(n)
    cases.append({"name": "transposition_only", "phi0": phi0, "phi1": phi1})

    # 3. symplectic pair on both labels
    T = sp4[7]
    f_sp = [apply_matrix_cols(T, x) for x in range(size)]
    phi0 = [ident, ident]
    phi1 = [f_sp, f_sp]
    cases.append({"name": "symplectic_same_b", "phi0": phi0, "phi1": phi1})

    # 4. symplectic pair differing between b=0 and b=1
    T2 = sp4[11]
    f_sp2 = [apply_matrix_cols(T2, x) for x in range(size)]
    phi0 = [ident, ident]
    phi1 = [f_sp, f_sp2]
    cases.append({"name": "symplectic_b_dependent", "phi0": phi0, "phi1": phi1})

    # 5. affine pair on b=0, identity on b=1
    A = gl4[5]
    t = rng.randrange(1, size)
    f_aff = [(apply_matrix_cols(A, x) ^ t) for x in range(size)]
    phi0 = [ident, ident]
    phi1 = [f_aff, ident]
    cases.append({"name": "affine_b_dependent", "phi0": phi0, "phi1": phi1})

    # 6. random b-dependent pair (seeded)
    phi0 = [ident, ident]
    phi1 = [random_bijection(size, rng), random_bijection(size, rng)]
    cases.append({"name": "random_b_dependent", "phi0": phi0, "phi1": phi1})

    # 7. fully independent random bijections in all four branches
    phi0 = [random_bijection(size, rng), random_bijection(size, rng)]
    phi1 = [random_bijection(size, rng), random_bijection(size, rng)]
    cases.append({"name": "random_all_branches", "phi0": phi0, "phi1": phi1})

    return cases


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--seed", type=int, default=20260616)
    p.add_argument("--search", type=int, default=3000,
                   help="number of random bijective maps to sample for exp/341 verification")
    return p.parse_args()


def main():
    args = parse_args()
    p = P_NOISE
    rng = random.Random(args.seed)
    n = 2
    lags = all_lagrangians(n)
    orbit_min = universal_minimum(n, p)
    print(f"Track U: label-preserving b-dependent bijections, n={n}; orbit minimum = {orbit_min}\n")

    # ------------------------------------------------------------------
    # U1: theorem verification on named cases
    # ------------------------------------------------------------------
    cases = build_named_cases(n, rng)
    case_results = []
    all_ok = True
    for case in cases:
        name = case["name"]
        phi0, phi1 = case["phi0"], case["phi1"]
        assert_bijections(phi0, phi1)

        A0 = agreement_A(n, lags, phi0[0], phi1[0])
        A1 = agreement_A(n, lags, phi0[1], phi1[1])
        sd_theorem = sd_label_preserving_b_dependent_theorem(n, A0, A1, p)
        sd_direct = exact_sd_label_preserving_b_dependent(n, lags, phi0, phi1, p)
        match = (sd_theorem == sd_direct)
        ge = (sd_direct >= orbit_min)
        duplicate = (phi0 == phi1)
        eq_min = (sd_direct == orbit_min)
        ok = match and ge and (eq_min == duplicate)
        all_ok &= ok

        case_results.append({
            "name": name,
            "sd": str(sd_direct),
            "sd_theorem": str(sd_theorem),
            "A0": str(A0),
            "A1": str(A1),
            "formula_matches_direct": match,
            "meets_universal_bound": ge,
            "equals_orbit_minimum": eq_min,
            "is_literal_duplicate": duplicate,
        })
        print(f"  {name:24s}: SD = {sd_direct}, A0={A0}, A1={A1}, "
              f"match={match}, ge={ge}, dup={duplicate}")
    assert all_ok, "theorem verification failed on a named case"
    print("  => U1 closed form matches direct enumeration for all named cases")

    # ------------------------------------------------------------------
    # U2: large random bijective search matching exp/341 regime
    # ------------------------------------------------------------------
    size = 1 << (2 * n)
    ident = [list(range(size)), list(range(size))]
    search_results = []
    below = 0
    min_sd: Fraction | None = None
    min_instance: dict | None = None
    for idx in range(args.search):
        # label-preserving b-dependent: phi_{0,b} and phi_{1,b} are random bijections
        phi0 = [random_bijection(size, rng), random_bijection(size, rng)]
        phi1 = [random_bijection(size, rng), random_bijection(size, rng)]
        assert_bijections(phi0, phi1)

        A0 = agreement_A(n, lags, phi0[0], phi1[0])
        A1 = agreement_A(n, lags, phi0[1], phi1[1])
        sd = sd_label_preserving_b_dependent_theorem(n, A0, A1, p)
        sd_direct = exact_sd_label_preserving_b_dependent(n, lags, phi0, phi1, p)
        assert sd == sd_direct, f"search instance {idx}: theorem/direct mismatch"

        if min_sd is None or sd < min_sd:
            min_sd = sd
            min_instance = {
                "index": idx,
                "A0": str(A0),
                "A1": str(A1),
                "sd": str(sd),
            }
        if sd < orbit_min:
            below += 1
            print(f"  *** SEARCH COUNTEREXAMPLE at idx {idx}: SD = {sd} < {orbit_min} ***")
        if idx < 10:
            search_results.append({
                "index": idx,
                "sd": str(sd),
                "A0": str(A0),
                "A1": str(A1),
                "meets_bound": sd >= orbit_min,
            })

    print(f"\n  Random search: {args.search} bijective label-preserving b-dependent instances")
    print(f"    instances below universal minimum: {below}")
    print(f"    minimum SD found: {min_sd} = {float(min_sd):.6f}")
    assert below == 0, "universal minimum was violated in random search"
    assert min_sd is not None and min_sd >= orbit_min

    # ------------------------------------------------------------------
    # U3: n=3 spot check
    # ------------------------------------------------------------------
    n3 = 3
    lags3 = all_lagrangians(n3)
    size3 = 1 << (2 * n3)
    f1_n3 = [list(range(size3)), list(range(size3))]
    f2_n3 = [random_symplectic_perm(n3, rng), random_symplectic_perm(n3, rng)]
    assert_bijections(f1_n3, f2_n3)
    A0_3 = agreement_A(n3, lags3, f1_n3[0], f2_n3[0])
    A1_3 = agreement_A(n3, lags3, f1_n3[1], f2_n3[1])
    sd_theorem_3 = sd_label_preserving_b_dependent_theorem(n3, A0_3, A1_3, p)
    sd_direct_3 = exact_sd_label_preserving_b_dependent(n3, lags3, f1_n3, f2_n3, p)
    orbit3 = universal_minimum(n3, p)
    assert sd_theorem_3 == sd_direct_3
    assert sd_direct_3 >= orbit3
    print(f"\n  n=3 spot: SD = {sd_direct_3} (theorem OK); A0={A0_3}, A1={A1_3}; "
          f"orbit min = {orbit3}; strict = {sd_direct_3 > orbit3}")

    # ------------------------------------------------------------------
    # Assemble output
    # ------------------------------------------------------------------
    result = {
        "track": "U",
        "experiment": 420,
        "noise_rate_p": str(p),
        "theorem_U1": {
            "statement": "For label-preserving b-dependent bijections g_i(x,b) = (phi_{i,b}(x), b), the exact same-secret SD is 1 - (p^2+(1-p)^2)/4^n + (1-2p)^2/(2*4^n)*(2 - A_0 - A_1), where A_beta = Pr_{L,x}[1_L(phi_{0,beta} x) = 1_L(phi_{1,beta} x)]",
            "universal_minimum": str(orbit_min),
            "lower_bound_statement": "SD >= 1 - (p^2+(1-p)^2)/4^n, with equality iff phi_{0,beta} = phi_{1,beta} for both beta (i.e. g_0 = g_1, the literal duplicate)",
            "equality_condition": "A_beta = 1 iff phi_{0,beta} = phi_{1,beta}",
            "closed_form_p_1_4": "123/128 + (2 - A_0 - A_1)/128  at n=2",
            "label": "THEOREM",
        },
        "verification_n2": {
            "named_cases": case_results,
            "search": {
                "num_sampled": args.search,
                "instances_below_minimum": below,
                "minimum_sd": str(min_sd) if min_sd is not None else None,
                "minimum_sd_instance": min_instance,
                "first_ten_instances": search_results,
            },
            "label": "THEOREM",
        },
        "verification_n3_spot": {
            "sd": str(sd_direct_3),
            "sd_theorem": str(sd_theorem_3),
            "A0": str(A0_3),
            "A1": str(A1_3),
            "orbit_minimum": str(orbit3),
            "strictly_above_minimum": sd_direct_3 > orbit3,
            "label": "THEOREM",
        },
        "exp341_consistency": {
            "note": "The transposition_only case reproduces exp/341 value 1231/1280 exactly; the closed form gives A_0=1, A_1=9/10, hence SD = 123/128 + (1/10)/128 = 1231/1280",
            "label": "THEOREM",
        },
        "guards": {
            "L1_exact_arithmetic": "fractions.Fraction end-to-end; JSON stores string fractions",
            "L2_duality_care": "not invoked (no character sums over Lagrangians)",
            "L3_query_class_hygiene": "exact TV statements only; no Feldman/SQ/query-class inference",
            "L4_never_transform_comparison_distribution": "fresh pair (u1,b1,u2,b2) remains in natural domain; public maps act only on split side",
        },
        "interpretation_guard": {
            "comparison_distribution": "two independent fresh samples from the SAME uniform secret L",
            "family": "label-preserving b-dependent point maps g_i(x,b) = (phi_{i,b}(x), b) with each phi_{i,b} a bijection",
            "bijectivity_assertion": "every tested phi_{i,b} is explicitly asserted to be a permutation of F_2^{2n}",
            "PRE_REGISTERED": "structural distributional theorem for this restricted bijective family; does not extend to non-bijective or label-modifying maps; not a lem:m2 rate or attack claim",
        },
    }

    out_path = Path(args.output) if args.output else Path("experiments/output") / "420-trackU-label-preserving-b-dependent-theorem.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
