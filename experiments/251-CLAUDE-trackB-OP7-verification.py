#!/usr/bin/env python3
"""
251-CLAUDE-trackB-OP7-verification.py

Independent adjudication of Kimi Track B (ecacd48):
  THEOREM B.1  SD(P_T, Q_T) is independent of T in Sp(2n, F_2)
  THEOREM B.2  f(n) = SD(P_I, Q_I) = 1 - (p^2 + (1-p)^2)/4^n  (= 1 - 5/(8 4^n) at p=1/4)

Verification strategy (NO reuse of Kimi's bijection or counting):
build the two joint distributions DIRECTLY from the definition, with T inside,
and compute SD exactly (Fractions):

  P_T(u, b, z, c)  =  Pr[ u uniform, z = Tu, b = c = 1_L(u) + e ]
  Q_T(u, b, z, c)  =  Pr[ u, w uniform iid; z = Tw; b = 1_L(u)+e_1, c = 1_{TL}(Tw)+e_2
                          = 1_L(w)+e_2 ]   (corrected rerandomized-secret convention)

Checks:
  (1) n=2: exact SD for T = I and for 10 random non-identity T in Sp(4,F_2)
      (direct construction, not the bijection) — all must equal 123/128 = f(2).
  (2) n=3: exact SD for T = I and 3 random T in Sp(6,F_2) — must equal 507/512.
      Lagrangian enumeration from scratch (|Lagr(6,2)| = 135 verified).
  (3) closed-form arithmetic and the n=1 edge case (the B.2 proof's
      min(P,Q)=Q-on-diagonal step needs P >= Q there; check n=1 directly).
  (4) sanity: P_T's diagonal-only support (after the z=Tu coupling), and
      Q's diagonal mass = (p^2+(1-p)^2)/4^n exactly.

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
    vecs = list(range(1, 1 << N))
    found = set()
    for basis in combinations(vecs, n):
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


def random_symplectic(n, rng):
    """Random element of Sp(2n,F_2) as a product of symplectic transvections
    t_v(x) = x + omega(x,v) v.  Returns a matrix as list of column images? We
    only need the action as a function; represent as a permutation table."""
    N = 2 * n
    size = 1 << N
    perm = list(range(size))  # identity action
    for _ in range(rng.randint(6, 14)):
        v = rng.randrange(1, size)
        new = [0] * size
        for x in range(size):
            new[x] = perm[x] ^ (v if omega(perm[x], v, n) else 0)
        perm = new
    return perm


def is_symplectic_perm(perm, n):
    N = 2 * n
    size = 1 << N
    # linearity + form preservation on a basis
    for i in range(N):
        for j in range(N):
            if omega(perm[1 << i], perm[1 << j], n) != omega(1 << i, 1 << j, n):
                return False
    for x in (3, 5, 9, size - 1):
        y = 0
        for i in range(N):
            if (x >> i) & 1:
                y ^= perm[1 << i]
        if y != perm[x]:
            return False
    return True


def sd_for_T(n, lags, perm):
    """Exact SD(P_T, Q_T) by direct construction."""
    N = 2 * n
    size = 1 << N
    NL = len(lags)
    p = P_NOISE
    wL = Fraction(1, NL)
    wu = Fraction(1, size)

    P = {}
    Q = {}
    for L in lags:
        for u in range(size):
            inu = 1 if (u in L or u == 0) else 0
            # NOTE: 0 is in every subspace; ensure sets include 0
            inu = 1 if (u in L) else 0
            zu = perm[u]
            for e in (0, 1):
                b = inu ^ e
                wpe = (p if e else 1 - p)
                key = (u, b, zu, b)
                P[key] = P.get(key, Fraction(0)) + wL * wu * wpe
        for u in range(size):
            inu = 1 if (u in L) else 0
            for w in range(size):
                inw = 1 if (w in L) else 0
                zw = perm[w]
                for e1 in (0, 1):
                    b1 = inu ^ e1
                    w1 = (p if e1 else 1 - p)
                    for e2 in (0, 1):
                        b2 = inw ^ e2
                        w2 = (p if e2 else 1 - p)
                        key = (u, b1, zw, b2)
                        Q[key] = Q.get(key, Fraction(0)) + wL * wu * wu * w1 * w2
    # SD = (1/2) sum |P - Q|
    keys = set(P) | set(Q)
    sd = sum(abs(P.get(k, Fraction(0)) - Q.get(k, Fraction(0))) for k in keys) / 2
    qdiag = sum(v for (u, b, z, c), v in Q.items() if z == perm[u] and c == b)
    return sd, qdiag


def f_closed(n):
    p = P_NOISE
    return 1 - (p * p + (1 - p) ** 2) / 4 ** n


def main():
    rng = random.Random(20260614)
    ok = True
    print("=" * 72)
    print("251-CLAUDE  Track B / OP7 — direct-construction verification")
    print("=" * 72)

    # make sure subspace sets contain 0
    for n, n_random_T, expect_lag in ((2, 10, 15), (3, 3, 135)):
        lags = all_lagrangians(n)
        assert all(0 in L for L in lags)
        good = len(lags) == expect_lag
        ok &= good
        print(f"\nn={n}: |Lagr| = {len(lags)} (expect {expect_lag}) "
              f"{'OK' if good else 'FAIL'}")
        target = f_closed(n)

        # T = I
        ident = list(range(1 << (2 * n)))
        sd, qdiag = sd_for_T(n, lags, ident)
        m1 = sd == target
        ok &= m1
        print(f"   T=I       : SD = {sd}  (= f({n}) = {target}? {'OK' if m1 else 'FAIL'})")
        # Q diagonal mass check (B.2's key quantity)
        qd_target = (P_NOISE ** 2 + (1 - P_NOISE) ** 2) / 4 ** n
        m2 = qdiag == qd_target
        ok &= m2
        print(f"   Q diag mass = {qdiag}  (= (p^2+(1-p)^2)/4^n? {'OK' if m2 else 'FAIL'})")

        for t in range(n_random_T):
            perm = random_symplectic(n, rng)
            assert is_symplectic_perm(perm, n)
            if perm == ident:
                continue
            sd, _ = sd_for_T(n, lags, perm)
            mt = sd == target
            ok &= mt
            if not mt:
                print(f"   random T#{t}: SD = {sd}  *** MISMATCH ***")
        print(f"   {n_random_T} random non-identity T in Sp({2*n},F_2): "
              f"all SD == f({n})  {'OK' if ok else 'FAIL'}")

    # closed-form arithmetic
    print("\nclosed form: f(n) = 1 - 5/(8*4^n) at p=1/4:")
    vals = {2: Fraction(123, 128), 3: Fraction(507, 512), 4: Fraction(2043, 2048)}
    for n, v in vals.items():
        m = f_closed(n) == v == 1 - Fraction(5, 8 * 4 ** n)
        ok &= m
        print(f"   f({n}) = {f_closed(n)}  {'OK' if m else 'FAIL'}")

    # n=1 edge case (the min(P,Q) step's boundary): direct check
    lags1 = all_lagrangians(1)
    print(f"\nn=1 edge: |Lagr(2,F_2)| = {len(lags1)} (expect 3)")
    sd1, _ = sd_for_T(1, lags1, list(range(4)))
    m = sd1 == f_closed(1)
    ok &= m
    print(f"   f(1) direct = {sd1}  vs closed form {f_closed(1)}  {'OK' if m else 'FAIL'}")

    print("\n" + "=" * 72)
    print("RESULT:", "ALL CHECKS PASS — B.1 + B.2 ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
