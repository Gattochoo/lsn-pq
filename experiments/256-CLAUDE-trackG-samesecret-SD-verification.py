#!/usr/bin/env python3
"""
256-CLAUDE-trackG-samesecret-SD-verification.py

Adjudication of Kimi Track G (0eb7126). Verdicts tested here:

  G.1 (universal b-marginal bound): Pr_fresh[b1 != b2] = 2 q_n (1-q_n),
      q_n = p + (1-2p)/2^n  — verify by enumeration (n=2,3). Key step: the
      per-L marginal rate is L-independent because |L| = 2^n for every L.

  G.3 (claimed: same-secret SD equals 1-(p^2+(1-p)^2)/4^n for EVERY bijection
      pair) — REFUTE. Kimi's experiment applied f1,f2 to the FRESH pair too
      (circular: SD(Phi#P, Phi#Q) = SD(P,Q) for any bijection Phi). The true
      same-secret comparison is f-DEPENDENT.

  CLAUDE replacement theorem (verified here exactly):
      SD(P_{f1,f2}, Q_same) = 1 - 4^{-n} [ 2p(1-p) + (1-2p)^2 * A(f1,f2) ],
      A = Pr_{L,x}[ 1_L(f1(x)) = 1_L(f2(x)) ],
  hence  SD >= 1 - (p^2+(1-p)^2)/4^n  for ALL label-preserving splits,
  with equality iff f1 = f2 (A=1). The orbit value is the universal MINIMUM,
  not the universal value.

Checks:
  (1) formula == direct enumeration at n=2 for: (id,id), 5 symplectic (id,T),
      3 affine, 3 random bijection pairs — exact Fractions.
  (2) at least one symplectic T gives SD STRICTLY > 123/128 (refuting G.3).
  (3) G.1 closed form vs enumeration; and bound subsumption:
      1-(p^2+(1-p)^2)/4^n >= Pr[b1!=b2] for n=2,3.
  (4) n=3 spot check of the formula vs enumeration for one non-identity pair.

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


def sd_direct(n, lags, f1, f2, p=P_NOISE):
    """Exact SD( (f1(x),b,f2(x),b) , same-secret fresh (u1,b1,u2,b2) )."""
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
                key = (f1[x], b, f2[x], b)
                P[key] = P.get(key, Fraction(0)) + w
        for u1 in range(size):
            c1 = 1 if u1 in L else 0
            for u2 in range(size):
                c2 = 1 if u2 in L else 0
                for e1 in (0, 1):
                    b1 = c1 ^ e1
                    w1 = (p if e1 else 1 - p)
                    for e2 in (0, 1):
                        b2 = c2 ^ e2
                        w2 = (p if e2 else 1 - p)
                        key = (u1, b1, u2, b2)
                        w = wL * Fraction(1, size * size) * w1 * w2
                        Q[key] = Q.get(key, Fraction(0)) + w
    keys = set(P) | set(Q)
    return sum(abs(P.get(k, Fraction(0)) - Q.get(k, Fraction(0)))
               for k in keys) / 2


def sd_formula(n, lags, f1, f2, p=P_NOISE):
    """CLAUDE formula: 1 - 4^{-n}[2p(1-p) + (1-2p)^2 A]."""
    size = 1 << (2 * n)
    NL = len(lags)
    A = Fraction(0)
    for x in range(size):
        u, v = f1[x], f2[x]
        agree = sum(1 for L in lags if (u in L) == (v in L))
        A += Fraction(agree, NL)
    A /= size
    return 1 - Fraction(1, 4 ** n) * (2 * p * (1 - p) + (1 - 2 * p) ** 2 * A), A


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
    rng = random.Random(20260614)
    print("=" * 76)
    print("256-CLAUDE  Track G — same-secret SD: formula vs enumeration; G.3 test")
    print("=" * 76)

    n = 2
    size = 1 << (2 * n)
    lags = all_lagrangians(n)
    orbit_value = 1 - (P_NOISE ** 2 + (1 - P_NOISE) ** 2) / 4 ** n  # 123/128

    # build test pairs
    ident = list(range(size))
    pairs = [("id,id", ident, ident)]
    for i in range(5):
        T = random_symplectic_perm(n, rng)
        pairs.append((f"id,Sp#{i}", ident, T))
    for i in range(3):  # affine: x -> x + t (translation = simplest affine)
        t = rng.randrange(1, size)
        pairs.append((f"id,shift+{t}", ident, [x ^ t for x in range(size)]))
    for i in range(3):
        g = list(range(size))
        rng.shuffle(g)
        pairs.append((f"id,rand#{i}", ident, g))

    print(f"\n(1)(2) n=2: orbit value = {orbit_value} = 123/128? "
          f"{orbit_value == Fraction(123,128)}")
    any_strict = False
    for name, f1, f2 in pairs:
        sd_e = sd_direct(n, lags, f1, f2)
        sd_f, A = sd_formula(n, lags, f1, f2)
        m = sd_e == sd_f
        ok &= m
        ge = sd_e >= orbit_value
        ok &= ge
        eq = sd_e == orbit_value
        ident_pair = f1 == f2
        # equality iff f1 == f2
        ok &= (eq == ident_pair)
        if not eq:
            any_strict = True
        print(f"   {name:>14}: SD = {str(sd_e):>10}  formula {'OK' if m else 'FAIL'}"
              f"  A = {str(A):>8}  >= orbit {'OK' if ge else 'FAIL'}"
              f"  {'EQUALITY' if eq else 'STRICT >'}"
              f"{'  (iff f1==f2 OK)' if (eq == ident_pair) else '  *** equality-iff FAIL ***'}")
    ok &= any_strict
    print(f"   => G.3 'same SD for every bijection pair' REFUTED: "
          f"{'yes (strict cases found)' if any_strict else 'NO'}")

    # (3) G.1 closed form + subsumption
    print("\n(3) G.1 b-marginal bound and subsumption:")
    for nn in (2, 3):
        q = P_NOISE + (1 - 2 * P_NOISE) / 2 ** nn
        closed = 2 * q * (1 - q)
        # enumeration: b1 != b2 over (L, u1, u2, e1, e2)
        lg = all_lagrangians(nn)
        sz = 1 << (2 * nn)
        tot = Fraction(0)
        for L in lg:
            inb = [1 if u in L else 0 for u in range(sz)]
            ones = sum(inb)
            # Pr[b=1 | L] = (ones*(1-p) + (sz-ones)*p)/sz
            pb = Fraction(ones * (1 - P_NOISE) + (sz - ones) * P_NOISE, sz)
            tot += 2 * pb * (1 - pb)
        enum = tot / len(lg)
        m = enum == closed
        ok &= m
        orbit_nn = 1 - (P_NOISE ** 2 + (1 - P_NOISE) ** 2) / 4 ** nn
        sub = orbit_nn >= closed
        ok &= sub
        print(f"   n={nn}: Pr[b1!=b2] = {closed} (enum {'OK' if m else 'FAIL'});"
              f"  orbit bound {orbit_nn} >= it: {'OK (subsumed)' if sub else 'FAIL'}")

    # (4) n=3 spot: one symplectic pair, formula vs enumeration
    print("\n(4) n=3 spot check (one symplectic pair):")
    lg3 = all_lagrangians(3)
    T3 = random_symplectic_perm(3, rng)
    id3 = list(range(1 << 6))
    sd_f3, A3 = sd_formula(3, lg3, id3, T3)
    sd_e3 = sd_direct(3, lg3, id3, T3)
    m = sd_e3 == sd_f3
    ok &= m
    orbit3 = 1 - (P_NOISE ** 2 + (1 - P_NOISE) ** 2) / 4 ** 3
    print(f"   SD = {sd_e3} (formula {'OK' if m else 'FAIL'}; A = {A3});"
          f" orbit = {orbit3}; strict-> {sd_e3 > orbit3}")
    ok &= sd_e3 > orbit3

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — G.1 ACCEPT; G.3 REFUTED; "
          "CLAUDE formula confirmed" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
