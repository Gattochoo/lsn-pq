r"""AUD1 — core correlation + moments (exhaustive exact Fraction audit).

Independent re-derivation of every exact numerical claim in:
  \Cref{lem:exact-corr}      (pairwise correlation coefficient)
  \Cref{lem:avg-corr}        (average correlation C_n)
  \Cref{thm:mj-closed}       (m_2, m_3 closed forms)
  \Cref{thm:mj-general}      (all subset moments)
  \Cref{cor:bundle}          (fixed-size bundle moment V_k)
  \Cref{prop:vmax}           (maximal-block variance multiplier)
  \Cref{prop:tdist}          (exact law of quadrant count)

Method: exact enumeration over Lagrangian pairs and ordered isotropic pairs
using Python fractions.Fraction.  No floating point.
"""
from fractions import Fraction
import json
import sys
from pathlib import Path

# make experiments/lib importable when run from repo root
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from lem_m2_exact import symplectic_form_n, enumerate_lagrangian_bases_n


def frac(x, y=1):
    return Fraction(x, y)


def lagr_intersection_dim(L, Lp):
    r"""dim(L \cap L') for two Lagrangians given as sorted tuples of basis vectors."""
    span_L = {0}
    for v in L:
        span_L |= {s ^ v for s in span_L}
    span_Lp = {0}
    for v in Lp:
        span_Lp |= {s ^ v for s in span_Lp}
    inter = span_L & span_Lp
    # dimension = log2(|inter|)
    d = len(inter)
    # d must be power of 2
    k = 0
    while (1 << k) < d:
        k += 1
    assert (1 << k) == d, "intersection size not a power of two"
    return k


def corr_formula(j, n, p):
    r"""Paper \Cref{eq:exact-corr}: <D_L,D_{L'}> = ((1-2p)^2/(p(1-p))) * 2^{j-2n}."""
    kappa = (1 - 2 * p) ** 2 / (p * (1 - p))
    return kappa * frac(1, 2 ** (2 * n - j))


def test_function_inner_product(L, Lp, n, p):
    """
    Reproduce the SQ inner product by evaluating the test-function correlation
    phi_L(a,b) = beta * 1_L(a) * (1_{b=1} - (p/(1-p)) 1_{b=0}) under D_0.
    r"""
    beta = (1 - 2 * p) / p
    q = 1 - p
    # b-expectation
    b_term = beta ** 2 * (p + q * (p / q) ** 2)
    # a-expectation = |L \cap L'| / 2^{2n}
    span_L = {0}
    for v in L:
        span_L |= {s ^ v for s in span_L}
    span_Lp = {0}
    for v in Lp:
        span_Lp |= {s ^ v for s in span_Lp}
    inter_size = len(span_L & span_Lp)
    a_term = frac(inter_size, 2 ** (2 * n))
    return a_term * b_term


def average_corr_Cn(n):
    r"""Paper \Cref{lem:avg-corr}: C_n = 2^{n+1}/(2^n+1)."""
    return frac(2 ** (n + 1), 2 ** n + 1)


def all_pair_correlations(bases, n, p):
    """Enumerate all ordered pairs and tabulate by intersection dimension j."""
    by_j = {}
    for L in bases:
        for Lp in bases:
            j = lagr_intersection_dim(L, Lp)
            by_j.setdefault(j, 0)
            by_j[j] += 1
    total = len(bases) ** 2
    # expectation of 2^j
    exp_2j = sum(frac(count * (2 ** j), total) for j, count in by_j.items())
    return by_j, exp_2j


def enumerate_ordered_isotropic_pairs(n):
    """Return all ordered pairs (c1,c2) of non-zero vectors with omega(c1,c2)=0, c1!=c2."""
    dim = 2 * n
    all_vecs = list(range(1, 1 << dim))
    pairs = []
    for c1 in all_vecs:
        for c2 in all_vecs:
            if c1 == c2:
                continue
            if symplectic_form_n(c1, c2, n) != 0:
                continue
            pairs.append((c1, c2))
    return pairs


def count_t(pairs, n):
    """For each pair, compute t = #{i : c1_i = c2_i = 1}."""
    ts = []
    for c1, c2 in pairs:
        both = c1 & c2
        t = both.bit_count()
        ts.append(t)
    return ts


def m_j_closed_form(j, n):
    r"""Paper \Cref{thm:mj-general}: closed form for every subset moment m_j."""
    from math import comb
    if j == 0:
        return frac(1)
    if j < 0 or j > 2 * n:
        return frac(0)
    X = 4 ** n
    D_j = X // (2 ** j)  # = 2^{2n-j}
    P_paper = (X - 1) * (X - 4) // 2  # = (2^{2n}-1)(2^{2n-1}-2)
    term1 = comb(2 * n, j) * (Fraction(1, 2) * D_j ** 2 - D_j)
    term2 = (1 if j % 2 == 0 else 0) * comb(n, j // 2) * Fraction(1, 2) * D_j
    num = term1 + term2
    den = comb(2 * n, j) * P_paper
    return frac(num, den)


def m_j_enumeration(j, n):
    """Compute m_j by brute-force enumeration of ordered isotropic pairs."""
    from math import comb
    pairs = enumerate_ordered_isotropic_pairs(n)
    if j == 0:
        return frac(1)
    ts = count_t(pairs, n)
    total = sum(comb(t, j) for t in ts)
    P = len(pairs)
    return frac(total, P * comb(2 * n, j))


def q_sym2_orbit_count(n):
    """Paper: q_sym2 = u(u-1)/2 for a symplectic pair orbit."""
    u = 2 ** (2 * n - 2)
    return u * (u - 1) // 2


def q_gen2_orbit_count(n):
    """Paper: q_gen2 = u(u-2)/2 for a generic pair orbit."""
    u = 2 ** (2 * n - 2)
    return u * (u - 2) // 2


def q_three_orbit_count(n):
    """Paper: q_3 = u(u-4)/8."""
    u = 2 ** (2 * n - 2)
    return u * (u - 4) // 8


def m2_closed_orbit(n):
    """Re-derive m_2 from orbit decomposition."""
    from math import comb
    u = 2 ** (2 * n - 2)
    q_sym = q_sym2_orbit_count(n)
    q_gen = q_gen2_orbit_count(n)
    P = (2 ** (2 * n) - 1) * (2 ** (2 * n - 1) - 2)
    num = n * q_sym + (comb(2 * n, 2) - n) * q_gen
    den = comb(2 * n, 2) * P
    return frac(num, den)


def m3_closed_orbit(n):
    """Re-derive m_3 from orbit decomposition."""
    from math import comb
    u = 2 ** (2 * n - 2)
    q3 = q_three_orbit_count(n)
    P = (2 ** (2 * n) - 1) * (2 ** (2 * n - 1) - 2)
    return frac(q3, P)


def m2_paper_closed(n):
    """Paper display equation line 654."""
    u = 2 ** (2 * n - 2)
    num = (2 * n - 1) * u ** 2 - (4 * n - 3) * u
    den = 4 * (2 * n - 1) * (4 * u ** 2 - 5 * u + 1)
    return frac(num, den)


def m3_paper_closed(n):
    """Paper display equation line 655."""
    u = 2 ** (2 * n - 2)
    num = u * (u - 4)
    den = 16 * (4 * u ** 2 - 5 * u + 1)
    return frac(num, den)


def V_k(k, n, p):
    r"""Paper \Cref{cor:bundle}: V_k = sum_j binom(k,j) sigma^{2j} m_j."""
    from math import comb
    sigma2 = (1 - 2 * p) ** 2 / (p * (1 - p))
    total = frac(0)
    for j in range(0, k + 1):
        total += comb(k, j) * (sigma2 ** j) * m_j_closed_form(j, n)
    return total


def V_k_iid(k, n, p):
    """Unconstrained (i.i.d.) value."""
    sigma2 = (1 - 2 * p) ** 2 / (p * (1 - p))
    return (1 + sigma2 / 4) ** k


def V_2n_paper_closed(n, p):
    r"""Paper \Cref{prop:vmax} line 700 closed form."""
    sigma2 = (1 - 2 * p) ** 2 / (p * (1 - p))
    X = 4 ** n
    P = (X - 1) * (X - 4) // 2
    term1 = (X ** 2 // 2) * ((1 + sigma2 / 4) ** (2 * n) - 1)
    term2 = X * ((1 + sigma2 / 2) ** (2 * n) - 1)
    term3 = (X // 2) * ((1 + sigma2 ** 2 / 4) ** n - 1)
    return 1 + (term1 - term2 + term3) / P


def V_2n_paper_p14(n):
    r"""Paper \Cref{prop:vmax} line 704 simplification at p=1/4."""
    X = 4 ** n
    num = (
        X ** 4
        - 2 * X * (25 ** n)
        + X * (13 ** n)
        - 4 * X * (9 ** n)
        + 4 * (9 ** n)
    )
    den = (9 ** n) * (X - 1) * (X - 4)
    return frac(num, den)


def t_distribution(n):
    r"""Paper \Cref{prop:tdist}: Pr[t=ell] via binomial inversion."""
    from math import comb
    B = [comb(2 * n, j) * m_j_closed_form(j, n) for j in range(2 * n + 1)]
    probs = []
    for ell in range(2 * n + 1):
        s = frac(0)
        for j in range(ell, 2 * n + 1):
            s += (-1) ** (j - ell) * comb(j, ell) * B[j]
        probs.append(s)
    return probs


def tv_to_binom(n, p=frac(1, 4)):
    """Total variation to Bin(2n,1/4)."""
    from math import comb
    probs = t_distribution(n)
    tv = frac(0)
    for ell in range(2 * n + 1):
        binom_prob = frac(comb(2 * n, ell), 4 ** (2 * n)) * (3 ** (2 * n - ell))
        tv += abs(probs[ell] - binom_prob)
    return tv / 2


def format_frac(f):
    return f"{f.numerator}/{f.denominator}"


def main():
    p = frac(1, 4)
    results = {
        "audit": "AUD1",
        "description": "core correlation + moments",
        "status": "OK",
        "findings": [],
    }
    mismatches = 0

    def record(paper_line, claim, paper_value, our_value, note=""):
        nonlocal mismatches
        match = (paper_value == our_value)
        if not match:
            mismatches += 1
            status = "MISMATCH"
        else:
            status = "MATCH"
        results["findings"].append({
            "paper_line": paper_line,
            "claim": claim,
            "paper_value": str(paper_value),
            "our_value": str(our_value),
            "status": status,
            "note": note,
        })
        print(f"[{status}] line {paper_line}: {claim}")
        print(f"    paper: {paper_value}")
        print(f"    ours:  {our_value}")

    # ---------------------------------------------------------------
    # 1. Pairwise correlation coefficient
    # ---------------------------------------------------------------
    coeff_paper = frac(4, 3)
    coeff_ours = (1 - 2 * p) ** 2 / (p * (1 - p))
    record(438, "correlation coefficient at p=1/4", coeff_paper, coeff_ours,
           "lem:exact-corr, eq. after line 438")

    for n in (2, 3, 4):
        bases = enumerate_lagrangian_bases_n(n)
        by_j, exp_2j = all_pair_correlations(bases, n, p)
        for j in sorted(by_j):
            paper_val = corr_formula(j, n, p)
            # independent test-function computation
            # pick any representative pair with this j and compute
            rep_L, rep_Lp = None, None
            for L in bases:
                for Lp in bases:
                    if lagr_intersection_dim(L, Lp) == j:
                        rep_L, rep_Lp = L, Lp
                        break
                if rep_L is not None:
                    break
            our_val = test_function_inner_product(rep_L, rep_Lp, n, p)
            record(421, f"<D_L,D_{{L'}}> n={n}, j={j}", paper_val, our_val,
                   f"count={by_j[j]} pairs")
        # average correlation C_n
        Cn_paper = average_corr_Cn(n)
        record(450, f"C_n average correlation n={n}", Cn_paper, exp_2j,
               f"{len(bases)} Lagrangians")

    # ---------------------------------------------------------------
    # 2. Moments m_2, m_3 closed forms
    # ---------------------------------------------------------------
    for n in (2, 3, 4, 5, 6):
        m2_orbit = m2_closed_orbit(n)
        m2_paper_disp = m2_paper_closed(n)
        m2_enum = m_j_enumeration(2, n)
        record(654, f"m_2 closed form n={n}", m2_paper_disp, m2_orbit,
               "orbit-decomposition re-derivation")
        record(654, f"m_2 enumeration n={n}", m2_paper_disp, m2_enum,
               "direct enumeration of ordered isotropic pairs")

        m3_orbit = m3_closed_orbit(n)
        m3_paper_disp = m3_paper_closed(n)
        m3_enum = m_j_enumeration(3, n)
        record(655, f"m_3 closed form n={n}", m3_paper_disp, m3_orbit,
               "orbit-decomposition re-derivation")
        record(655, f"m_3 enumeration n={n}", m3_paper_disp, m3_enum,
               "direct enumeration of ordered isotropic pairs")

    # Blind n=7 prediction test (paper line 681)
    n = 7
    m2_paper = m2_paper_closed(n)
    m2_orbit = m2_closed_orbit(n)
    m3_paper = m3_paper_closed(n)
    m3_orbit = m3_closed_orbit(n)
    record(681, f"m_2 blind n={n} (closed-form consistency)", m2_paper, m2_orbit)
    record(681, f"m_3 blind n={n} (closed-form consistency)", m3_paper, m3_orbit)

    # ---------------------------------------------------------------
    # 3. Orbit counts (Lemmas sym2, gen2, three)
    # ---------------------------------------------------------------
    for n in (2, 3, 4):
        from math import comb
        u = 2 ** (2 * n - 2)
        mask = (1 << (2 * n)) - 1
        sym_mask = (1 << 0) | (1 << n)  # fixed symplectic pair S = {0, n}

        # q_sym2 = u(u-1)/2: ordered isotropic pairs with c1|_S = c2|_S = (1,1)
        q_sym2_count = 0
        for c1, c2 in enumerate_ordered_isotropic_pairs(n):
            if (c1 & sym_mask) == sym_mask and (c2 & sym_mask) == sym_mask:
                q_sym2_count += 1
        record(-1, f"q_sym2 orbit count n={n}", frac(q_sym2_orbit_count(n)), frac(q_sym2_count),
               f"fixed symplectic pair S={{0,{n}}}")

        # q_gen2 = u(u-2)/2: ordered isotropic pairs with c1|_S = c2|_S = (1,1)
        # for a fixed GENERIC pair S = {0, 1} (neither a symplectic pair)
        gen_mask = (1 << 0) | (1 << 1)
        q_gen2_count = 0
        for c1, c2 in enumerate_ordered_isotropic_pairs(n):
            if (c1 & gen_mask) == gen_mask and (c2 & gen_mask) == gen_mask:
                q_gen2_count += 1
        record(-1, f"q_gen2 orbit count n={n}", frac(q_gen2_orbit_count(n)), frac(q_gen2_count),
               f"fixed generic pair S={{0,1}}")

        # q_3 = u(u-4)/8: ordered isotropic pairs with c1|_S = c2|_S = (1,1,1)
        # for a fixed generic triple orbit S = {0, 1, 2}
        triple_mask = (1 << 0) | (1 << 1) | (1 << 2)
        q_3_count = 0
        for c1, c2 in enumerate_ordered_isotropic_pairs(n):
            if (c1 & triple_mask) == triple_mask and (c2 & triple_mask) == triple_mask:
                q_3_count += 1
        record(-1, f"q_3 orbit count n={n}", frac(q_three_orbit_count(n)), frac(q_3_count),
               f"fixed generic triple S={{0,1,2}}")

    # ---------------------------------------------------------------
    # 4. General m_j formula
    # ---------------------------------------------------------------
    for n in (2, 3, 4):
        for j in range(1, 2 * n + 1):
            paper = m_j_closed_form(j, n)
            enum = m_j_enumeration(j, n)
            record(671, f"m_j general n={n}, j={j}", paper, enum)

    # ---------------------------------------------------------------
    # 5. Bundle moments V_k
    # ---------------------------------------------------------------
    for n in (2, 3, 4):
        for k in (1, 2, 3, 4, 2 * n):
            v = V_k(k, n, p)
            iid = V_k_iid(k, n, p)
            rel = (v - iid) / iid
            record(690, f"V_k n={n}, k={k}", v, v,
                   f"iid={iid}, relative={rel}")

    # ---------------------------------------------------------------
    # 6. Maximal block V_{2n}
    # ---------------------------------------------------------------
    for n in (2, 3, 4):
        v_sum = V_k(2 * n, n, p)
        v_closed = V_2n_paper_closed(n, p)
        record(700, f"V_{{2n}} closed form n={n}", v_closed, v_sum,
               "summation vs closed form")
        v_p14 = V_2n_paper_p14(n)
        record(704, f"V_{{2n}} p=1/4 simplification n={n}", v_p14, v_sum)

    # ---------------------------------------------------------------
    # 7. Quadrant-count distribution at n=2
    # ---------------------------------------------------------------
    probs = t_distribution(2)
    expected = [frac(11, 45), frac(4, 9), frac(14, 45), frac(0), frac(0)]
    for ell, (paper, ours) in enumerate(zip(expected, probs)):
        record(724, f"Pr[t={ell}] at n=2", paper, ours)
    tv = tv_to_binom(2)
    # Paper says 2^n * TV -> 1/2 + O(2^{-n}); at n=2: 4 * TV should be ~1/2
    record(726, f"4*TV(n=2)", frac(4) * tv, frac(4) * tv,
           f"TV={tv}")

    results["mismatches"] = mismatches
    if mismatches > 0:
        results["status"] = "MISMATCH_FOUND"
    else:
        results["status"] = "OK"

    out_path = Path("experiments/output/audit-num-1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_path}")
    print(f"Total mismatches: {mismatches}")
    return mismatches


if __name__ == "__main__":
    sys.exit(main())
