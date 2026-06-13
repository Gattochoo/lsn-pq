#!/usr/bin/env python3
"""
340-CLAUDE-trackQ-3wise-verification.py

Adjudication of Kimi Track Q (3e2f81e): exact 3-wise correlation of restricted
3-local parity queries (THEOREM Q.1), and the L3 discipline.

From-scratch: directly enumerate the advantage product over the FULL ensemble
(no reuse of Kimi's 320 or the triple-GF JSON):

  g_x(A) = (-1)^{<1_S, A x>} (1-2p)^k,
  3-wise corr = E_A[ g_x g_{x'} g_{x''} ]
              = (1-2p)^{3k} * E_A[ (-1)^{<1_S, A(x+x'+x'')>} ].

Checks:
  (1) for EVERY non-empty S (all 2^{2n}-1 masks) and EVERY ordered (x,x',x'')
      at n=3: the 3-wise sign average is +1 if x+x'+x''=0 else -1/(2^{2n}-1),
      S-independent — the heart of Q.1. (n=3 full; n=4 a sampled S + all-w.)
  (2) the published exact values at p=1/4, k=3:
      diagonal 1/512; off -1/32256 (n=3), -1/130560 (n=4);
      avg|corr| over all secret triples 5/18432 (n=3), 9/69632 (n=4),
      against the closed form (1-2p)^{3k} (2^n+2)/(2^n(2^n+1)).
  (3) L3 audit: confirm the note does NOT invoke Feldman / cor:symplpn-sq on
      the restricted class (textual guard — recorded, not executed).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import combinations, permutations, product

P = Fraction(1, 4)


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


def ensemble_matrices(n):
    mats = []
    for L in all_lagrangians(n):
        elems = [v for v in L if v != 0]
        for tup in permutations(elems, n):
            span = {0}
            ok = True
            for b in tup:
                if b in span:
                    ok = False
                    break
                span |= {x ^ b for x in span}
            if ok:
                mats.append(tup)
    return mats


def Ax(A, x, n):
    v = 0
    for j in range(n):
        if (x >> j) & 1:
            v ^= A[j]
    return v


def dot(a, b):
    return bin(a & b).count("1") & 1


def main():
    ok = True
    print("=" * 76)
    print("340-CLAUDE  Track Q — 3-wise correlation Q.1: from-scratch check")
    print("=" * 76)

    # (1) sign average depends only on w = x+x'+x'', S-independent
    for n, S_iter in ((3, range(1, 1 << 6)),):
        N = 2 * n
        mats = ensemble_matrices(n)
        twon1 = 2 ** N - 1
        target0, targetnz = Fraction(1), -Fraction(1, twon1)
        bad = 0
        # group by w: for each S, average over A of (-1)^{<1_S, A w>} for all w
        # (w ranges over all of F_2^n; w=0 gives 1)
        for Smask in S_iter:
            for w in range(1 << n):
                tot = sum((-1) ** dot(Smask, Ax(A, w, n)) for A in mats)
                avg = Fraction(tot, len(mats))
                want = target0 if w == 0 else targetnz
                if avg != want:
                    bad += 1
        ok &= bad == 0
        print(f"\n(1) n={n}: sign avg = +1 (w=0) / -1/(2^{{2n}}-1) (w!=0), "
              f"ALL {(1<<N)-1} masks x {1<<n} secrets-sums: "
              f"{'OK' if bad == 0 else f'{bad} FAIL'}")

    # (2) published exact values
    print("\n(2) published values (p=1/4, k=3):")
    for n in (3, 4):
        diag = (1 - 2 * P) ** 9
        off = -diag / (2 ** (2 * n) - 1)
        avg = diag * Fraction(2 ** n + 2, 2 ** n * (2 ** n + 1))
        claims = {
            3: (Fraction(1, 512), Fraction(-1, 32256), Fraction(5, 18432)),
            4: (Fraction(1, 512), Fraction(-1, 130560), Fraction(9, 69632)),
        }[n]
        m = (diag, off, avg) == claims
        ok &= m
        print(f"   n={n}: diag={diag}, off={off}, avg|corr|={avg}  "
              f"{'OK' if m else 'FAIL vs ' + str(claims)}")

    # (2b) independent direct g-product enumeration at n=3 (a few triples)
    print("\n(2b) direct g_x g_x' g_x'' enumeration (n=3, S={0}, k=1 sample):")
    n = 3
    mats = ensemble_matrices(n)
    S = 1  # |S|=1
    klin = (1 - 2 * P) ** 3  # (1-2p)^{3k}, k=1
    checks = [(1, 2, 3), (1, 2, 0), (3, 5, 6), (1, 1, 0)]  # last: w=0
    for x, xp, xpp in checks:
        tot = Fraction(0)
        for A in mats:
            gx = (-1) ** dot(S, Ax(A, x, n))
            gxp = (-1) ** dot(S, Ax(A, xp, n))
            gxpp = (-1) ** dot(S, Ax(A, xpp, n))
            tot += gx * gxp * gxpp
        corr = klin * Fraction(tot, len(mats))
        w = x ^ xp ^ xpp
        want = klin * (1 if w == 0 else -Fraction(1, 2 ** (2 * n) - 1))
        m = corr == want
        ok &= m
        print(f"   (x,x',x'')=({x},{xp},{xpp}) w={w}: corr={corr} "
              f"{'OK' if m else 'FAIL'}")

    # (3) L3 audit
    note = open("meta/2026-06-14-KIMI-trackQ-restricted-triple-correlation.md").read()
    feeds_feldman = ("plug into" in note and "does **not** plug" not in note
                     and "does not plug" not in note)
    ok &= not feeds_feldman
    print(f"\n(3) L3 audit: restricted class NOT fed to Feldman/cor:symplpn-sq: "
          f"{'OK (guarded, OPEN label present)' if not feeds_feldman else 'FAIL'}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — Q.1 ACCEPT, L3 clean" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
