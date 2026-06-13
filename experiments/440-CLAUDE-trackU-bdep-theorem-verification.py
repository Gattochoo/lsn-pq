#!/usr/bin/env python3
"""
440-CLAUDE-trackU-bdep-theorem-verification.py

Adjudication of Kimi Track U (636188c): exact same-secret SD for
label-preserving b-dependent BIJECTIONS g_i(x,b) = (phi_{i,b}(x), b).

THEOREM (Kimi U1): SD = 1 - (p^2+(1-p)^2)/4^n
                      + (1-2p)^2/(2*4^n) * (2 - A_0 - A_1),
  A_beta = Pr_{L,x}[ 1_L(phi_{0,beta} x) = 1_L(phi_{1,beta} x) ].
=> SD >= 1-(p^2+(1-p)^2)/4^n, equality iff phi_{0,beta}=phi_{1,beta} for both beta.

From-scratch (my own sd via direct construction from 341 + my own A_beta and
formula): verify formula == enumeration on named + random bijective cases,
equality-iff, and the >= minimum claim. Bijectivity asserted for every map.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from fractions import Fraction
from itertools import combinations

P = Fraction(1, 4)


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians(n):
    NN = 2 * n
    found = set()
    for basis in combinations(range(1, 1 << NN), n):
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


def sd_direct(n, lags, phi0, phi1, p=P):
    """phi_i = (phi_i[0], phi_i[1]) per-label bijections; g_i(x,b)=(phi_i[b][x], b)."""
    size = 1 << (2 * n)
    NL = len(lags)
    Pd, Qd = {}, {}
    wL = Fraction(1, NL)
    for L in lags:
        for x in range(size):
            c = 1 if x in L else 0
            for e in (0, 1):
                b = c ^ e
                w = wL * Fraction(1, size) * (p if e else 1 - p)
                key = ((phi0[b][x], b), (phi1[b][x], b))
                Pd[key] = Pd.get(key, Fraction(0)) + w
        for u1 in range(size):
            c1 = 1 if u1 in L else 0
            for u2 in range(size):
                c2 = 1 if u2 in L else 0
                for e1 in (0, 1):
                    for e2 in (0, 1):
                        w = wL * Fraction(1, size * size) * \
                            (p if e1 else 1 - p) * (p if e2 else 1 - p)
                        key = ((u1, c1 ^ e1), (u2, c2 ^ e2))
                        Qd[key] = Qd.get(key, Fraction(0)) + w
    keys = set(Pd) | set(Qd)
    return sum(abs(Pd.get(k, Fraction(0)) - Qd.get(k, Fraction(0)))
               for k in keys) / 2


def A_beta(n, lags, p0b, p1b):
    """Pr_{L,x}[ 1_L(p0b x) = 1_L(p1b x) ]."""
    size = 1 << (2 * n)
    NL = len(lags)
    tot = Fraction(0)
    for x in range(size):
        u, v = p0b[x], p1b[x]
        agree = sum(1 for L in lags if (u in L) == (v in L))
        tot += Fraction(agree, NL)
    return tot / size


def formula(n, A0, A1, p=P):
    base = 1 - (p ** 2 + (1 - p) ** 2) / 4 ** n
    return base + (1 - 2 * p) ** 2 / (2 * 4 ** n) * (2 - A0 - A1)


def is_perm(f, size):
    return sorted(f) == list(range(size))


def main():
    ok = True
    rng = random.Random(20260617)
    n = 2
    size = 1 << (2 * n)
    lags = all_lagrangians(n)
    ident = list(range(size))
    orbit = Fraction(123, 128)

    print("=" * 74)
    print("440-CLAUDE  Track U — label-preserving b-dependent SD theorem")
    print("=" * 74)

    def rb():
        p = list(range(size)); rng.shuffle(p); return p

    # named cases: phi_i = [phi_i^{b=0}, phi_i^{b=1}]
    swap01 = list(range(size)); swap01[0], swap01[1] = 1, 0
    cases = []
    cases.append(("literal dup", [ident, ident], [ident, ident], True))
    cases.append(("transp b-dep", [ident, ident], [ident, swap01], False))
    s0 = rb()
    cases.append(("sym same", [ident, ident], [s0, s0], False))
    cases.append(("sym b-dep", [ident, ident], [s0, rb()], False))
    cases.append(("rand b-dep", [rb(), rb()], [rb(), rb()], False))

    print("\n(1) formula == direct enumeration (named, n=2):")
    for name, phi0, phi1, expect_eq in cases:
        for f in phi0 + phi1:
            assert is_perm(f, size)
        sd_e = sd_direct(n, lags, phi0, phi1)
        A0 = A_beta(n, lags, phi0[0], phi1[0])
        A1 = A_beta(n, lags, phi0[1], phi1[1])
        sd_f = formula(n, A0, A1)
        m = sd_e == sd_f
        ge = sd_e >= orbit
        eq = sd_e == orbit
        ok &= m and ge and (eq == expect_eq)
        print(f"   {name:>14}: A0={str(A0):>6} A1={str(A1):>6} SD={str(sd_e):>10} "
              f"formula {'OK' if m else 'FAIL'} >=min {'OK' if ge else 'FAIL'} "
              f"{'EQ' if eq else '>'}{'ok' if eq == expect_eq else ' IFF-FAIL'}")

    # (2) random bijective search: none below min
    print("\n(2) random label-preserving b-dependent bijections (n=2):")
    below = 0
    mn = None
    for _ in range(1500):
        phi0 = [rb(), rb()]
        phi1 = [rb(), rb()]
        sd = sd_direct(n, lags, phi0, phi1)
        mn = sd if mn is None else min(mn, sd)
        if sd < orbit:
            below += 1
            # cross-check via formula
    ok &= below == 0
    print(f"   1500 bijections: below 123/128 = {below}; min SD = {float(mn):.6f} "
          f"(Kimi 4941/5120={float(Fraction(4941,5120)):.6f}); "
          f"{'OK (>= min)' if below == 0 else '*** BROKEN ***'}")

    # (3) n=3 spot
    print("\n(3) n=3 spot (formula vs enumeration):")
    lags3 = all_lagrangians(3)
    sz3 = 1 << 6
    def rb3():
        p = list(range(sz3)); rng.shuffle(p); return p
    phi0 = [list(range(sz3)), list(range(sz3))]
    phi1 = [rb3(), rb3()]
    A0 = A_beta(3, lags3, phi0[0], phi1[0])
    A1 = A_beta(3, lags3, phi0[1], phi1[1])
    sd_e = sd_direct(3, lags3, phi0, phi1)
    sd_f = formula(3, A0, A1)
    m = sd_e == sd_f
    ok &= m and sd_e >= Fraction(507, 512)
    print(f"   A0={A0} A1={A1} SD={sd_e}={float(sd_e):.6f} formula {'OK' if m else 'FAIL'}; "
          f">= 507/512: {sd_e >= Fraction(507,512)}")

    print("\n" + "=" * 74)
    print("RESULT:", "ALL CHECKS PASS — Track U THEOREM ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
