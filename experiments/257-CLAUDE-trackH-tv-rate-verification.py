#!/usr/bin/env python3
"""
257-CLAUDE-trackH-tv-rate-verification.py

Adjudication of Kimi Track H (0c064c2): THEOREM 2^n TV -> 1/2.

Proof re-derived by hand (sound); this script verifies every quantitative
ingredient exactly (Fractions), independently of Kimi's 221 script:

  (1) the closed-form decomposition
        Delta_ell = (X^2 C - 1) beta_ell - 2XC q_ell + (-1)^ell XC r_ell
                    - 1[ell=0] * 4/(X-4)
      equals the binomial-inversion Delta computed from my own m_j closed form
      (194/255 rail), for all ell, n = 2..10. Includes the spurious-j=0
      bookkeeping check: X^2 C - XC - 1 = 4/(X-4).
  (2) r_ell = [z^ell] ((5+2z+z^2)/4)^n  and  sum_ell r_ell = 2^n  (n=1..12).
  (3) error mass: sum_ell |E_ell| <= |X^2C-1| + 2XC + 4/(X-4) = O(4^{-n});
      print 4^n * (bound) to exhibit boundedness.
  (4) the theorem's conclusion: |2^n TV - 1/2| * 2^n bounded (n=2..12),
      i.e. remainder O(2^{-n}) as claimed.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from math import comb


def m_j_closed(n, j):
    if j == 0:
        return Fraction(1)
    N = 2 * n
    P = (2 ** N - 1) * (2 ** (N - 1) - 2)
    Dj = 2 ** (N - j)
    Cb = comb(N, j)
    num = Cb * (Fraction(Dj * Dj, 2) - Dj)
    if j % 2 == 0:
        num += comb(n, j // 2) * Fraction(Dj, 2)
    return num / (Cb * P)


def delta_transform(n):
    """Delta_ell from binomial inversion of my m_j (independent rail)."""
    N = 2 * n
    B = [comb(N, j) * m_j_closed(n, j) for j in range(N + 1)]
    pmf = [sum((-1) ** (j - l) * comb(j, l) * B[j] for j in range(l, N + 1))
           for l in range(N + 1)]
    ref = [comb(N, l) * Fraction(1, 4) ** l * Fraction(3, 4) ** (N - l)
           for l in range(N + 1)]
    return [a - b for a, b in zip(pmf, ref)]


def r_coeffs(n):
    """coefficients of ((5+2z+z^2)/4)^n."""
    poly = [Fraction(1)]
    base = [Fraction(5, 4), Fraction(2, 4), Fraction(1, 4)]
    for _ in range(n):
        new = [Fraction(0)] * (len(poly) + 2)
        for i, a in enumerate(poly):
            for k, b in enumerate(base):
                new[i + k] += a * b
        poly = new
    return poly


def main():
    ok = True
    print("=" * 76)
    print("257-CLAUDE  Track H — TV-rate theorem: ingredient verification")
    print("=" * 76)

    print("\n(1) closed-form decomposition == transform Delta (exact), n=2..10:")
    for n in range(2, 11):
        N = 2 * n
        X = Fraction(4 ** n)
        Cc = 1 / ((X - 1) * (X - 4))
        # spurious j=0 bookkeeping
        ok &= (X * X * Cc - X * Cc - 1) == Fraction(4, 1) / (X - 4)
        r = r_coeffs(n)
        beta = [comb(N, l) * Fraction(1, 4) ** l * Fraction(3, 4) ** (N - l)
                for l in range(N + 1)]
        q = [Fraction(comb(N, l), 2 ** N) for l in range(N + 1)]
        closed = [(X * X * Cc - 1) * beta[l] - 2 * X * Cc * q[l]
                  + (-1) ** l * X * Cc * r[l]
                  - (Fraction(4, 1) / (X - 4) if l == 0 else 0)
                  for l in range(N + 1)]
        trans = delta_transform(n)
        m = closed == trans
        ok &= m
        print(f"   n={n:>2}: identical for all ell: {'OK' if m else 'FAIL'}")

    print("\n(2) sum r_ell = 2^n (n=1..12):")
    for n in range(1, 13):
        s = sum(r_coeffs(n))
        m = s == 2 ** n
        ok &= m
        pos = all(c > 0 for c in r_coeffs(n))
        ok &= pos
        if n in (1, 4, 8, 12):
            print(f"   n={n:>2}: sum = {s} {'OK' if m else 'FAIL'}; "
                  f"all r_ell > 0: {'OK' if pos else 'FAIL'}")

    print("\n(3) error mass 4^n * bound (should stay bounded):")
    for n in (2, 4, 6, 8, 10, 12):
        X = Fraction(4 ** n)
        Cc = 1 / ((X - 1) * (X - 4))
        bound = abs(X * X * Cc - 1) + 2 * X * Cc + Fraction(4, 1) / (X - 4)
        print(f"   n={n:>2}: 4^n * error-bound = {float(bound * 4 ** n):.4f}")

    print("\n(4) |2^n TV - 1/2| * 2^n (remainder O(2^{-n}) => bounded):")
    for n in range(2, 13):
        tv = sum(abs(d) for d in delta_transform(n)) / 2
        dev = abs(2 ** n * tv - Fraction(1, 2))
        print(f"   n={n:>2}: 2^n*TV = {float(2**n*tv):.6f}; "
              f"2^n * |dev| = {float(dev * 2 ** n):.4f}")
        ok &= dev * 2 ** n < 3  # bounded constant

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — Track H THEOREM ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
