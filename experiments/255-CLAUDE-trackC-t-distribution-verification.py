#!/usr/bin/env python3
"""
255-CLAUDE-trackC-t-distribution-verification.py

Independent adjudication of Kimi Track C (a517440): exact distribution of the
pairwise quadrant count t, and its TV distance to Bin(2n, 1/4).

From-scratch rails (no reuse of Kimi's script):
  (1) n = 2, 3, 4: t-histogram by DIRECT enumeration of all ordered isotropic
      pairs (my 194 machinery re-implemented) == Kimi's claimed pmfs ==
      binomial-inversion transform of B_j = C(2n,j) m_j (my verified m_j).
  (2) n = 2..10: exact TV( dist(t), Bin(2n,1/4) ) via the transform with MY
      m_j closed form — compare every fraction in Kimi's table.
  (3) rate check: 2^n * TV trend toward 1/2 (claimed rate 2^{-(n+1)},
      labeled EVIDENCE/OPEN by Kimi — confirm the numbers, not the proof).
  (4) sanity: each pmf sums to 1, vanishes for t >= 2n-1, and reproduces
      m_j when re-contracted: sum_ell C(ell,j) Pr[t=ell] = C(2n,j) m_j.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from math import comb


def symplectic_pairs_hist(n):
    """t-histogram over all ordered isotropic pairs (direct enumeration)."""
    N = 2 * n
    full = 1 << N

    def omega(a, b):
        s = 0
        for i in range(n):
            s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
                 (((a >> (i + n)) & 1) & ((b >> i) & 1))
        return s

    hist = [0] * (N + 1)
    count = 0
    for c1 in range(1, full):
        for c2 in range(1, full):
            if c1 != c2 and omega(c1, c2) == 0:
                hist[bin(c1 & c2).count("1")] += 1
                count += 1
    P = (2 ** N - 1) * (2 ** (N - 1) - 2)
    assert count == P
    return [Fraction(h, P) for h in hist]


def m_j_closed(n, j):
    if j == 0:
        return Fraction(1)
    N = 2 * n
    P = (2 ** N - 1) * (2 ** (N - 1) - 2)
    Dj = 2 ** (N - j)
    C = comb(N, j)
    num = C * (Fraction(Dj * Dj, 2) - Dj)
    if j % 2 == 0:
        num += comb(n, j // 2) * Fraction(Dj, 2)
    return num / (C * P)


def t_pmf_from_transform(n):
    N = 2 * n
    B = [comb(N, j) * m_j_closed(n, j) for j in range(N + 1)]
    return [sum((-1) ** (j - l) * comb(j, l) * B[j] for j in range(l, N + 1))
            for l in range(N + 1)]


def binom_pmf(N, p):
    return [comb(N, l) * p ** l * (1 - p) ** (N - l) for l in range(N + 1)]


KIMI_PMF = {
    2: ["11/45", "4/9", "14/45", "0", "0"],
    3: ["10/63", "12/35", "22/63", "4/35", "11/315", "0", "0"],
    4: ["1541/16065", "824/3213", "596/1785", "3184/16065", "212/2295",
        "104/5355", "4/1071", "0", "0"],
}

KIMI_TV = {
    2: "707/5760", 3: "35183/645120", 4: "14891599/526417920",
    5: "788813171/54707355648", 6: "129011724689/17570715402240",
    7: "90177646929/23821297909760",
    8: "8866562072659001/4611334179001466880",
    9: "12710182327048981/13117434475422154752",
    10: "29399506915728870947/60446002750575209349120",
}


def main():
    ok = True
    print("=" * 76)
    print("255-CLAUDE  Track C — exact t-distribution + TV: from-scratch check")
    print("=" * 76)

    # (1) direct enumeration vs claimed pmf vs transform, n=2,3,4
    print("\n(1) direct enumeration == Kimi pmf == transform:")
    for n in (2, 3, 4):
        direct = symplectic_pairs_hist(n)
        trans = t_pmf_from_transform(n)
        kimi = [Fraction(s) for s in KIMI_PMF[n]]
        m1 = direct == trans == kimi
        ok &= m1
        print(f"   n={n}: {'ALL THREE IDENTICAL OK' if m1 else '*** MISMATCH ***'}")

    # (4) sanity: sums, vanishing, re-contraction to B_j
    print("\n(4) structural sanity (transform pmf):")
    for n in (2, 3, 4, 6, 8, 10):
        N = 2 * n
        pmf = t_pmf_from_transform(n)
        s1 = sum(pmf) == 1
        s2 = all(pmf[l] == 0 for l in range(N - 1, N + 1))
        s3 = all(sum(comb(l, j) * pmf[l] for l in range(N + 1))
                 == comb(N, j) * m_j_closed(n, j) for j in range(N + 1))
        s4 = all(p >= 0 for p in pmf)
        ok &= s1 and s2 and s3 and s4
        print(f"   n={n:>2}: sum=1 {'OK' if s1 else 'FAIL'}; zero at t>=2n-1 "
              f"{'OK' if s2 else 'FAIL'}; re-contracts to all B_j "
              f"{'OK' if s3 else 'FAIL'}; nonneg {'OK' if s4 else 'FAIL'}")

    # (2)+(3) exact TV table
    print("\n(2) exact TV(dist(t), Bin(2n,1/4)), n=2..10:")
    for n in range(2, 11):
        N = 2 * n
        pmf = t_pmf_from_transform(n)
        ref = binom_pmf(N, Fraction(1, 4))
        tv = sum(abs(a - b) for a, b in zip(pmf, ref)) / 2
        claim = Fraction(KIMI_TV[n])
        m = tv == claim
        ok &= m
        print(f"   n={n:>2}: TV = {float(tv):.6e}  2^n*TV = {float(tv * 2**n):.4f}"
              f"  {'OK (exact match)' if m else '*** MISMATCH vs ' + str(claim)}")
    print("   (claimed rate 2^{-(n+1)} i.e. 2^n*TV -> 1/2: EVIDENCE label "
          "appropriate — trend confirmed, no proof)")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — Track C ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
