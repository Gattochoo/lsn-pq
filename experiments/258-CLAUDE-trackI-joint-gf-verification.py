#!/usr/bin/env python3
"""
258-CLAUDE-trackI-joint-gf-verification.py

Adjudication of Kimi Track I (6e3d55f): closed-form joint generating function

  G_n = [ (T^{2n} + S^n)/2 - A^{2n} - B^{2n} - C^{2n} + 2 x00^{2n} ] / P,
  T = x11+x10+x01+x00,  S = T^2 - 4(x10 x01 + x10 x11 + x01 x11),
  A = x00+x01, B = x00+x10, C = x00+x11,  P = (2^{2n}-1)(2^{2n-1}-2).

Proof re-derived by hand (character sum: per-symplectic-pair sign matrix gives
exactly S; inclusion-exclusion boundary +2 x00^{2n}). This script verifies
independently of Kimi's 225 script:

  (1) full composition law: direct enumeration of ordered isotropic pairs at
      n = 2, 3, 4 -> joint composition histogram == coefficients of G_n
      (compare as exact polynomial dictionaries, not point evaluations).
  (2) corollary (a): specialization x11 -> 1+x reproduces my verified m_j
      closed form for all j (n = 2..6) — beyond Kimi's n<=4.
  (3) corollary (b): specialization x11 -> x reproduces the exact t-pmf
      (my 255 transform) for n = 2..6.
  (4) corollary (c): disagreement law Pr[d=k] = C(2n,k)/(2^{2n}-1) — verified
      BOTH from G_n and by the one-line direct argument (c1+c2 is uniform over
      nonzero vectors: #{c1: omega(c1,v)=0, c1 not in {0,v}} = 2^{2n-1}-2,
      v-independent), n = 2..6.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import product
from math import comb


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


# ---- polynomial dict helpers: keys = (t11, t10, t01, t00), values Fraction --

def poly_mul(p1, p2):
    out = {}
    for k1, v1 in p1.items():
        for k2, v2 in p2.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            out[k] = out.get(k, Fraction(0)) + v1 * v2
    return out


def poly_pow(p, e):
    out = {(0, 0, 0, 0): Fraction(1)}
    base = dict(p)
    while e:
        if e & 1:
            out = poly_mul(out, base)
        base = poly_mul(base, base)
        e >>= 1
    return out


def poly_add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Fraction(0)) + v
    return {k: v for k, v in out.items() if v != 0}


def poly_scale(p, c):
    return {k: v * c for k, v in p.items()}


X11, X10, X01, X00 = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)


def G_closed(n):
    """Kimi's closed form as an exact polynomial dict."""
    N = 2 * n
    T = {X11: Fraction(1), X10: Fraction(1), X01: Fraction(1), X00: Fraction(1)}
    S = poly_add(poly_pow(T, 2),
                 poly_scale(poly_mul({X10: Fraction(1)}, {X01: Fraction(1)}), -4),
                 poly_scale(poly_mul({X10: Fraction(1)}, {X11: Fraction(1)}), -4),
                 poly_scale(poly_mul({X01: Fraction(1)}, {X11: Fraction(1)}), -4))
    A = {X00: Fraction(1), X01: Fraction(1)}
    B = {X00: Fraction(1), X10: Fraction(1)}
    Cp = {X00: Fraction(1), X11: Fraction(1)}
    P = (2 ** N - 1) * (2 ** (N - 1) - 2)
    G = poly_add(poly_scale(poly_pow(T, N), Fraction(1, 2)),
                 poly_scale(poly_pow(S, n), Fraction(1, 2)),
                 poly_scale(poly_pow(A, N), -1),
                 poly_scale(poly_pow(B, N), -1),
                 poly_scale(poly_pow(Cp, N), -1),
                 {(0, 0, 0, 2 * n * 0 + N): Fraction(2)})
    return {k: v / P for k, v in G.items()}


def G_enum(n):
    """Direct enumeration: joint composition law of ordered isotropic pairs."""
    N = 2 * n
    full = 1 << N
    hist = {}
    cnt = 0
    for c1 in range(1, full):
        for c2 in range(1, full):
            if c1 == c2 or omega(c1, c2, n):
                continue
            t11 = bin(c1 & c2).count("1")
            t10 = bin(c1 & ~c2 & (full - 1)).count("1")
            t01 = bin(~c1 & c2 & (full - 1)).count("1")
            t00 = N - t11 - t10 - t01
            k = (t11, t10, t01, t00)
            hist[k] = hist.get(k, 0) + 1
            cnt += 1
    P = (2 ** N - 1) * (2 ** (N - 1) - 2)
    assert cnt == P
    return {k: Fraction(v, P) for k, v in hist.items()}


def main():
    ok = True
    print("=" * 76)
    print("258-CLAUDE  Track I — joint GF: polynomial-identity verification")
    print("=" * 76)

    print("\n(1) G_n closed form == direct enumeration (full coefficient dicts):")
    for n in (2, 3, 4):
        ge = G_enum(n)
        gc = G_closed(n)
        m = ge == gc
        ok &= m
        s1 = sum(ge.values()) == 1
        ok &= s1
        print(f"   n={n}: {len(ge)} compositions; dicts identical: "
              f"{'OK' if m else 'FAIL'}; sums to 1: {'OK' if s1 else 'FAIL'}")

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

    print("\n(2)(3) specializations reproduce m_j and the t-pmf (n=2..6):")
    for n in range(2, 7):
        N = 2 * n
        gc = G_closed(n)
        # t-pmf: marginal over t11
        pmf = [Fraction(0)] * (N + 1)
        for (a, b, c, d), v in gc.items():
            pmf[a] += v
        # m_j from pmf
        ok_j = all(sum(comb(l, j) * pmf[l] for l in range(N + 1))
                   == comb(N, j) * m_j_closed(n, j) for j in range(N + 1))
        # t-pmf vs transform (my 255 method)
        B = [comb(N, j) * m_j_closed(n, j) for j in range(N + 1)]
        pmf255 = [sum((-1) ** (j - l) * comb(j, l) * B[j]
                      for j in range(l, N + 1)) for l in range(N + 1)]
        ok_p = pmf == pmf255
        ok &= ok_j and ok_p
        print(f"   n={n}: all m_j OK: {ok_j}; t-pmf == transform: {ok_p}")

    print("\n(4) disagreement law Pr[d=k] = C(2n,k)/(2^{2n}-1):")
    for n in range(2, 7):
        N = 2 * n
        gc = G_closed(n)
        dlaw = [Fraction(0)] * (N + 1)
        for (a, b, c, d), v in gc.items():
            dlaw[b + c] += v
        target = [Fraction(0)] + [Fraction(comb(N, k), 2 ** N - 1)
                                  for k in range(1, N + 1)]
        m = dlaw == target
        ok &= m
        # one-line direct argument: per-v count is v-independent = 2^{2n-1}-2
        if n <= 4:
            full = 1 << N
            counts = set()
            for v in range(1, full):
                c = sum(1 for c1 in range(full)
                        if c1 not in (0, v) and omega(c1, v, n) == 0)
                counts.add(c)
            direct = counts == {2 ** (N - 1) - 2}
            ok &= direct
            print(f"   n={n}: G_n-marginal OK: {m}; per-v count "
                  f"v-independent (=2^{{2n-1}}-2): {direct}")
        else:
            print(f"   n={n}: G_n-marginal OK: {m}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — Track I THEOREM ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
