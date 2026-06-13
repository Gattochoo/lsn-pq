#!/usr/bin/env python3
"""
259-CLAUDE-trackJ-pencil-ratio-verification.py

Adjudication of Kimi Track J (f904dec): pencil-ratio theorem
  ratio(n,k) = (2^n+1)/(2^{n-k}+1),  via  C_n = 2^{n+1}/(2^n+1).

Proof re-derived by hand (quotient bijection; q-binomial theorem). Checks:

  (1) C_n = 2^{n+1}/(2^n+1) against the thm:distance sum (Gaussian binomials),
      n = 1..10; matches Track D's measured 8/5 (n=2), 16/9 (n=3).
  (2) q-binomial identity sum_l [n,l]_2 2^{l(l-1)/2} = prod_{i=0}^{n-1}(1+2^i),
      n = 1..10.
  (3) ratio formula vs DIRECT pencil computation:
      - n = 2, 3: pencils inside my full Lagrangian enumeration (254 rail);
      - n = 4: my own quotient-lift construction of the pencil of
        W = <e_1..e_k> (no full Lagr(8) enumeration), pairwise intersections
        within the lifted pencil -> exact diagonal-inclusive average;
        also verifies |S_W| = |Lagr(2(n-k))| and the lift is isotropic/maximal.
  (4) scale check: |S_W| vs |Lagr|/2^{2n} for k >= 3, n = 3..8 (k=3 pencils
      below scale for n >= 3, per J3).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import combinations


def omega_pairs(a, b, pairs):
    """symplectic form given list of (i, i') coordinate pairs."""
    s = 0
    for i, ip in pairs:
        s ^= (((a >> i) & 1) & ((b >> ip) & 1)) ^ (((a >> ip) & 1) & ((b >> i) & 1))
    return s


def omega(a, b, n):
    return omega_pairs(a, b, [(i, i + n) for i in range(n)])


def gauss_binom(n, k):
    num, den = 1, 1
    for i in range(k):
        num *= 2 ** n - 2 ** i
        den *= 2 ** k - 2 ** i
    return num // den


def lagr_size(n):
    out = 1
    for i in range(1, n + 1):
        out *= 2 ** i + 1
    return out


def C_from_distance(n):
    tot = sum(gauss_binom(n, j) * 2 ** ((n - j) * (n - j + 1) // 2) * 2 ** j
              for j in range(n + 1))
    return Fraction(tot, lagr_size(n))


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


def pencil_avg_direct(n, k):
    """avg of 2^{dim cap} over the pencil of W = <e_1..e_k> via full enum."""
    lags = all_lagrangians(n)
    W = {0}
    for i in range(k):
        W |= {x ^ (1 << i) for x in W}
    pen = [L for L in lags if W <= L]
    s = sum(Fraction(len(a & b)) for a in pen for b in pen)
    return s / len(pen) ** 2, len(pen)


def pencil_avg_quotient(n, k):
    """n=4-capable: build the pencil of W = <e_1..e_k> by lifting
    Lagr(W^perp/W). Coordinates: W = span(e_0..e_{k-1}) (bits 0..k-1);
    W^perp = {v : omega(v, e_i) = 0 for i<k} = bits {0..2n-1} minus
    {n..n+k-1} (since omega(v, e_i) = v_{i+n}). Quotient symplectic basis:
    (e_i, e_{i+n}) for i = k..n-1, plus W-bits 0..k-1 as the kernel."""
    N = 2 * n
    m = n - k
    # quotient = F_2^{2m} with pairs (i, i+m) mapping to ambient bits
    # amb(i) = k + i (for i < m), amb(i+m) = n + k + i
    sub = all_lagrangians(m) if m > 0 else [set([0])]
    pen = []
    for Lq in sub:
        # lift: span of W-bits + embedded quotient vectors
        emb = set()
        for v in Lq:
            w = 0
            for i in range(m):
                if (v >> i) & 1:
                    w |= 1 << (k + i)
                if (v >> (m + i)) & 1:
                    w |= 1 << (n + k + i)
            emb.add(w)
        # full lift = W + emb (all cosets)
        Wfull = {0}
        for i in range(k):
            Wfull |= {x ^ (1 << i) for x in Wfull}
        L = {w ^ x for w in emb for x in Wfull}
        assert len(L) == 2 ** n
        assert all(omega(u, v, n) == 0 for u in L for v in L)
        pen.append(L)
    s = sum(Fraction(len(a & b)) for a in pen for b in pen)
    return s / len(pen) ** 2, len(pen)


def main():
    ok = True
    print("=" * 76)
    print("259-CLAUDE  Track J — pencil-ratio theorem verification")
    print("=" * 76)

    print("\n(1) C_n = 2^{n+1}/(2^n+1) vs thm:distance sum:")
    for n in range(1, 11):
        a, b = C_from_distance(n), Fraction(2 ** (n + 1), 2 ** n + 1)
        m = a == b
        ok &= m
        if n in (1, 2, 3, 6, 10):
            print(f"   n={n:>2}: C_n = {a}  {'OK' if m else 'FAIL'}")

    print("\n(2) q-binomial identity (n=1..10):")
    for n in range(1, 11):
        lhs = sum(gauss_binom(n, l) * 2 ** (l * (l - 1) // 2)
                  for l in range(n + 1))
        rhs = 1
        for i in range(n):
            rhs *= 1 + 2 ** i
        m = lhs == rhs
        ok &= m
    print(f"   all n=1..10: {'OK' if ok else 'FAIL'}")

    print("\n(3) ratio formula vs direct pencils:")
    for n, k in ((2, 1), (2, 2), (3, 1), (3, 2), (3, 3)):
        avg, sz = pencil_avg_direct(n, k)
        ratio = avg / Fraction(2 ** (n + 1), 2 ** n + 1)
        pred = Fraction(2 ** n + 1, 2 ** (n - k) + 1)
        m = ratio == pred and sz == lagr_size(n - k)
        ok &= m
        print(f"   n={n} k={k} (full enum): |S_W|={sz}, ratio={ratio} "
              f"(pred {pred}) {'OK' if m else 'FAIL'}")
    for k in (1, 2, 3, 4):
        avg, sz = pencil_avg_quotient(4, k)
        ratio = avg / Fraction(2 ** 5, 2 ** 4 + 1)
        pred = Fraction(17, 2 ** (4 - k) + 1)
        m = ratio == pred and sz == lagr_size(4 - k)
        ok &= m
        print(f"   n=4 k={k} (quotient lift): |S_W|={sz}, avg={avg}, "
              f"ratio={ratio} (pred {pred}) {'OK' if m else 'FAIL'}")

    print("\n(4) scale check (k=3 below conjectured scale for n>=3):")
    for n in range(3, 9):
        sw = lagr_size(n - 3)
        thr = Fraction(lagr_size(n), 4 ** n)
        below = sw < thr
        ok &= below
        print(f"   n={n}: |S_W(k=3)| = {sw} vs scale {float(thr):.3f}: "
              f"{'below OK' if below else 'NOT below'}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — Track J THEOREM ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
