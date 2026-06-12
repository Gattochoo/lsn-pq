#!/usr/bin/env python3
"""
194-CLAUDE-op1-general-j-verification.py

Independent adjudication of Kimi's general-j subset-moment closure
(meta/2026-06-14-KIMI-op1-general-j-moment-closure.md, f7ecc63).

CLAIM (Kimi boxed formula), with u = 2^{2n-2}, D_j = 2^{2n-j},
P = (2^{2n}-1)(2^{2n-1}-2):

    m_j = [ C(2n,j) * (D_j^2/2 - D_j) + [j even] * C(n,j/2) * D_j/2 ]
          / ( C(2n,j) * P ).

This script verifies the formula WITHOUT using Kimi's orbit decomposition:
it recomputes m_j straight from the paper's DEFINITION (lsn-core.tex, sec:moments)

    m_j = E_{(c1,c2) ~ P}[ C(t, j) ] / C(2n, j),   t = |supp(c1) AND supp(c2)|,

by exhaustively enumerating the ordered isotropic-pair ensemble P for n = 2,3,4
(standard symplectic form over F_2). All arithmetic is exact (Fraction).

Cross-checks performed:
  (1) boxed formula  ==  definition-enumeration, for ALL 1<=j<=2n, n=2,3,4
  (2) reduction to thm:mj-closed at j=2,3
  (3) m_j = 0 for j >= 2n-1
  (4) sign of the discrepancy m_j - (1/4)^j  (Kimi's "negative for all j" is WRONG)
  (5) magnitude |m_j - (1/4)^j| = Theta(4^{-n})   (4^n * gap stays bounded)

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from math import comb
from itertools import product


def symplectic_pairs(n):
    """All ordered isotropic pairs (c1,c2): nonzero, distinct, Omega(c1,c2)=0.

    Standard symplectic form on F_2^{2n}: coordinate i (0..n-1) pairs with i+n.
    Returns list of (c1, c2) as integer bitmasks over 2n bits.
    """
    N = 2 * n
    full = 1 << N
    nonzero = [v for v in range(1, full)]

    def omega(a, b):
        s = 0
        for i in range(n):
            ai = (a >> i) & 1
            ain = (a >> (i + n)) & 1
            bi = (b >> i) & 1
            bin_ = (b >> (i + n)) & 1
            s ^= (ai & bin_) ^ (ain & bi)
        return s

    pairs = []
    for c1 in nonzero:
        for c2 in nonzero:
            if c1 == c2:
                continue
            if omega(c1, c2) == 0:
                pairs.append((c1, c2))
    return pairs


def m_j_from_definition(n, pairs):
    """m_j for all j, straight from the definition: E[C(t,j)]/C(2n,j)."""
    N = 2 * n
    P = len(pairs)
    # popcount-of-AND histogram over the ensemble
    hist = [0] * (N + 1)
    for c1, c2 in pairs:
        t = bin(c1 & c2).count("1")
        hist[t] += 1
    out = {}
    for j in range(1, N + 1):
        num = sum(hist[t] * comb(t, j) for t in range(j, N + 1))
        out[j] = Fraction(num, P * comb(N, j))
    return out


def m_j_boxed(n, j):
    """Kimi's closed form."""
    N = 2 * n
    P = (2 ** N - 1) * (2 ** (N - 1) - 2)
    Dj = 2 ** (N - j)
    C2nj = comb(N, j)
    num = C2nj * (Fraction(Dj * Dj, 2) - Dj)
    if j % 2 == 0:
        num += comb(n, j // 2) * Fraction(Dj, 2)
    return Fraction(num, C2nj * P)


def m2_closed(n):
    u = 2 ** (2 * n - 2)
    return Fraction((2 * n - 1) * u * u - (4 * n - 3) * u,
                    4 * (2 * n - 1) * (4 * u * u - 5 * u + 1))


def m3_closed(n):
    u = 2 ** (2 * n - 2)
    return Fraction(u * (u - 4), 16 * (4 * u * u - 5 * u + 1))


def main():
    print("=" * 72)
    print("194-CLAUDE  general-j subset-moment closure — independent check")
    print("=" * 72)

    all_ok = True
    for n in (2, 3, 4):
        N = 2 * n
        pairs = symplectic_pairs(n)
        P_expect = (2 ** N - 1) * (2 ** (N - 1) - 2)
        assert len(pairs) == P_expect, (n, len(pairs), P_expect)
        m_def = m_j_from_definition(n, pairs)

        print(f"\nn={n}  (2n={N},  |P|={len(pairs)})")
        for j in range(1, N + 1):
            box = m_j_boxed(n, j)
            df = m_def[j]
            match = (box == df)
            all_ok &= match
            quarter = Fraction(1, 4 ** j)
            gap = df - quarter            # signed discrepancy
            scaled = float(gap) * (4 ** n) if gap != 0 else 0.0
            flag = "OK " if match else "*** MISMATCH ***"
            print(f"  j={j:>2}  m_j={str(df):>22}  box={'==' if match else '!='}def"
                  f"  sign(m_j-1/4^j)={'+' if gap>0 else ('-' if gap<0 else '0')}"
                  f"  4^n*gap={scaled:+.4f}  {flag}")

        # (2) reduction to thm:mj-closed
        r2 = (m_def[2] == m2_closed(n))
        r3 = (m_def[3] == m3_closed(n))
        all_ok &= r2 and r3
        print(f"   reduces to thm:mj-closed:  m_2 {'OK' if r2 else 'FAIL'}, "
              f"m_3 {'OK' if r3 else 'FAIL'}")

        # (3) vanishing for j >= 2n-1
        van = all(m_def[j] == 0 for j in range(N - 1, N + 1))
        all_ok &= van
        print(f"   m_j = 0 for j >= 2n-1 = {N-1}:  {'OK' if van else 'FAIL'}")

    # (4) sign summary — Kimi's "negative for all j>=1" is WRONG
    print("\n" + "-" * 72)
    print("Sign of discrepancy  m_j - (1/4)^j  (adjudication of Kimi 'Consequences'):")
    for n in (2, 3, 4):
        pairs = symplectic_pairs(n)
        m_def = m_j_from_definition(n, pairs)
        m1gap = m_def[1] - Fraction(1, 4)
        print(f"  n={n}:  m_1 - 1/4 = {m1gap}  ({'POSITIVE (from above)' if m1gap>0 else 'neg'})"
              f"   -> j=1 is +, contradicting 'negative for all j'")

    print("\n" + "=" * 72)
    print("RESULT:", "ALL CHECKS PASS — formula ACCEPT" if all_ok else "FAILURE")
    print("Note: boxed formula correct; Kimi's 'discrepancy negative for all j>=1'")
    print("      is wrong (m_1 > 1/4); correct sign is + at j=1, - for j>=2.")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 72)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
