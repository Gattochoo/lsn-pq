#!/usr/bin/env python3
"""
261-CLAUDE-trackK-label-flipping-verification.py

Adjudication of Kimi Track K (0b7b5df).

  K1: 211 repaired per L4 (fresh side untransformed — diff inspected) and the
      corrected law matches the 256-CLAUDE theorem. Here: internal-consistency
      re-check of Kimi's published (A, SD) tables at p=1/4
      (SD = 1 - (3+2A)/128 at n=2; n=3 spot 1 - (1/64)(3/8 + A/4)).
  K2: label-flipping law verified FROM SCRATCH by direct enumeration at n=2:
      SD( ((f1 x, b+h1(x)), (f2 x, b+h2(x))) , same-secret fresh )
        = 1 - 4^{-n}[ 2p(1-p) + (1-2p)^2 A' ],
      A' = Pr[ 1_L(f1 x) xor 1_L(f2 x) = h1(x) xor h2(x) ],
      on my own test set including:
        - literal duplicate (equality must hold),
        - constant one-side flip (A'=0, SD = 125/128 — sharp),
        - random h (A' = zero-fraction of h1 xor h2),
        - symplectic + flips, fully random (f, h),
        - a ZERO-VECTOR case: f1 maps some x0 to 0 while f2 x0 != 0 — exercises
          the gap in Kimi's separation phrasing (no Lagrangian excludes 0; the
          membership XOR is still non-constant via 1 xor 1_L(f2 x0)).
  Equality-iff: A' = 1 exactly for the literal duplicate in all tests.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from fractions import Fraction
from itertools import combinations

P_NOISE = Fraction(1, 4)


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians(n):
    N = 2 * n
    found = set()
    for basis in combinations(range(1, 1 << N), n):
        span = {0}
        ok = True
        for b in basis:
            if b in span:
                ok = False
                break
            span |= {x ^ b for x in span}
        if not ok or len(span) != 2 ** n:
            continue
        if any(omega(u, v, n) for u in span for v in span):
            continue
        found.add(frozenset(span))
    return [set(s) for s in found]


def sd_direct_flip(n, lags, f1, f2, h1, h2, p=P_NOISE):
    """Exact SD by direct construction (no formula)."""
    size = 1 << (2 * n)
    NL = len(lags)
    P, Q = {}, {}
    wL = Fraction(1, NL)
    for L in lags:
        for x in range(size):
            c = 1 if x in L else 0
            for e in (0, 1):
                b = c ^ e
                w = wL * Fraction(1, size) * (p if e else 1 - p)
                key = (f1[x], b ^ h1[x], f2[x], b ^ h2[x])
                P[key] = P.get(key, Fraction(0)) + w
        for u1 in range(size):
            c1 = 1 if u1 in L else 0
            for u2 in range(size):
                c2 = 1 if u2 in L else 0
                for e1 in (0, 1):
                    for e2 in (0, 1):
                        w = wL * Fraction(1, size * size) * \
                            (p if e1 else 1 - p) * (p if e2 else 1 - p)
                        key = (u1, c1 ^ e1, u2, c2 ^ e2)
                        Q[key] = Q.get(key, Fraction(0)) + w
    keys = set(P) | set(Q)
    return sum(abs(P.get(k, Fraction(0)) - Q.get(k, Fraction(0)))
               for k in keys) / 2


def sd_formula_flip(n, lags, f1, f2, h1, h2, p=P_NOISE):
    size = 1 << (2 * n)
    NL = len(lags)
    Ap = Fraction(0)
    for x in range(size):
        u, v = f1[x], f2[x]
        target = h1[x] ^ h2[x]
        good = sum(1 for L in lags
                   if ((1 if u in L else 0) ^ (1 if v in L else 0)) == target)
        Ap += Fraction(good, NL)
    Ap /= size
    return 1 - Fraction(1, 4 ** n) * (2 * p * (1 - p)
                                      + (1 - 2 * p) ** 2 * Ap), Ap


def random_symplectic_perm(n, rng):
    size = 1 << (2 * n)
    perm = list(range(size))
    for _ in range(rng.randint(6, 14)):
        v = rng.randrange(1, size)
        perm = [perm[x] ^ (v if omega(perm[x], v, n) else 0)
                for x in range(size)]
    return perm


def main():
    ok = True
    rng = random.Random(20260615)
    n = 2
    size = 1 << (2 * n)
    lags = all_lagrangians(n)
    ident = list(range(size))
    zero_h = [0] * size
    orbit = Fraction(123, 128)

    print("=" * 76)
    print("261-CLAUDE  Track K — label-flipping law: from-scratch verification")
    print("=" * 76)

    # test set
    h_const1 = [1] * size
    h_rand = [rng.randint(0, 1) for _ in range(size)]
    g_rand = list(range(size))
    rng.shuffle(g_rand)
    T = random_symplectic_perm(n, rng)
    # zero-vector case: f1 swaps 0 <-> 5 (so f1(5)=0), f2 = identity
    f_zero = list(range(size))
    f_zero[0], f_zero[5] = f_zero[5], f_zero[0]
    h_rand2 = [rng.randint(0, 1) for _ in range(size)]

    cases = [
        ("duplicate (id,id,0,0)", ident, ident, zero_h, zero_h, True),
        ("dup-rand (g,g,h,h)", g_rand, g_rand, h_rand, h_rand, True),
        ("const flip (id,id,0,1)", ident, ident, zero_h, h_const1, False),
        ("rand flip (id,id,0,h)", ident, ident, zero_h, h_rand, False),
        ("symplectic+flip (id,T,0,h)", ident, T, zero_h, h_rand, False),
        ("full random (g,T,h,h2)", g_rand, T, h_rand, h_rand2, False),
        ("ZERO-CASE (fzero,id,0,0)", f_zero, ident, zero_h, zero_h, False),
    ]

    for name, f1, f2, h1, h2, expect_eq in cases:
        sd_e = sd_direct_flip(n, lags, f1, f2, h1, h2)
        sd_f, Ap = sd_formula_flip(n, lags, f1, f2, h1, h2)
        m = sd_e == sd_f
        ge = sd_e >= orbit
        eq = sd_e == orbit
        ok &= m and ge and (eq == expect_eq)
        print(f"   {name:>28}: SD = {str(sd_e):>10}  A' = {str(Ap):>7}  "
              f"formula {'OK' if m else 'FAIL'}  >=min {'OK' if ge else 'FAIL'}  "
              f"{'EQUALITY' if eq else 'strict'}"
              f"{' OK' if eq == expect_eq else ' *** iff-FAIL ***'}")

    # sharp value checks
    sd_c, Ac = sd_formula_flip(n, lags, ident, ident, zero_h, h_const1)
    ok &= (Ac == 0 and sd_c == Fraction(125, 128))
    zeros = sum(1 for x in range(size) if h_rand[x] == 0)
    sd_r, Ar = sd_formula_flip(n, lags, ident, ident, zero_h, h_rand)
    ok &= Ar == Fraction(zeros, size)
    print(f"\n   sharp: const-flip A'=0, SD=125/128: "
          f"{'OK' if Ac == 0 and sd_c == Fraction(125,128) else 'FAIL'}; "
          f"rand-flip A' = zero-fraction {zeros}/{size}: "
          f"{'OK' if Ar == Fraction(zeros, size) else 'FAIL'}")

    # K1 table internal consistency (Kimi's published pairs at n=2)
    table = [("1", "123/128"), ("4/5", "617/640"), ("11/15", "1853/1920"),
             ("7/10", "309/320"), ("3/5", "619/640"), ("79/120", "7421/7680"),
             ("5/8", "495/512")]
    cons = all(1 - (3 + 2 * Fraction(a)) / 128 == Fraction(s) for a, s in table)
    n3 = (1 - Fraction(1, 64) * (Fraction(3, 8) + Fraction(29, 36) / 4)
          == Fraction(9133, 9216))
    ok &= cons and n3
    print(f"   K1 tables internally consistent (n=2 all, n=3 spot): "
          f"{'OK' if cons and n3 else 'FAIL'}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — K1/K2 ACCEPT (zero-case phrasing flagged)"
          if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
