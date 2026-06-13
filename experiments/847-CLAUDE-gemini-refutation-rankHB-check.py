#!/usr/bin/env python3
"""
847-CLAUDE-gemini-refutation-rankHB-check.py

Refutes Gemini's (agy) round-9 "refutation" of the open-core proposition
H(u|s,C) >= n-o(n). Gemini claimed the syndrome s = HBe behaves as a uniform
(m-n)-dimensional vector (H(s|C) ~ m-n), so for m >= 2.622n the syndrome
over-determines e and I(x;y|C) -> n (reduction information-theoretically
lossless). That step VIOLATES the established confinement rank(HB) <= n.

THEOREM (rank(HB) <= n): H = parity-check of C (HC=0). Then HB*A = H(BA) = HC = 0,
so Col(A) subset ker(HB); rank(A)=n => dim ker(HB) >= n => rank(HB) <= 2n-n = n.
Hence H(s|C) <= n, NOT m-n: the syndrome captures at most n of e's ~1.62n entropy
bits and cannot over-determine e. (Cross-ref exp 740, exhaustive at n=2.)

This script confirms numerically that rank(HB) stays <= n as m grows (so Gemini's
H(s|C) ~ m-n is false: at m=6, n=2 it would predict 4, truth is 2).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from itertools import combinations

NN = 4  # 2n at n=2
n = 2


def rank2(cols):
    b = []
    for c in cols:
        x = c
        for v in b:
            x = min(x, x ^ v)
        if x:
            b.append(x)
            b.sort(reverse=True)
    return len(b)


def omega(a, b):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def lagrangians():
    out = set()
    for bb in combinations(range(1, 1 << NN), 2):
        span = {0}
        for x in bb:
            span |= {y ^ x for y in span}
        if len(span) != 4:
            continue
        if any(omega(u, v) for u in span for v in span):
            continue
        out.add(frozenset(span))
    return [sorted(s) for s in out]


def main():
    rng = random.Random(7)
    LAGS = lagrangians()
    print("=" * 70)
    print("847-CLAUDE  Gemini refutation check: rank(HB) <= n (NOT m-n)")
    print("=" * 70)
    print(f"n={n}: {len(LAGS)} Lagrangians")
    ok = True
    for m in (4, 5, 6, 7):
        mr = 0
        for _ in range(500):
            L = rng.choice(LAGS)
            nz = [v for v in L if v]
            a0, a1 = rng.sample(nz, 2)
            rows = [rng.randrange(1 << NN) for _ in range(m)]
            # C columns (m-bit): col_k[i] = <row_i, a_k>
            Ccols = []
            for ak in (a0, a1):
                c = 0
                for i, r in enumerate(rows):
                    if bin(r & ak).count("1") & 1:
                        c |= 1 << i
                Ccols.append(c)
            # B columns (m-bit): col_j[i] = (row_i)_j
            Bcols = []
            for j in range(NN):
                c = 0
                for i, r in enumerate(rows):
                    if (r >> j) & 1:
                        c |= 1 << i
                Bcols.append(c)
            # rank(HB) = rank(B) - rank(C)  [Col(C)=Col(BA) subset Col(B)]
            rHB = rank2(Bcols) - rank2(Ccols)
            mr = max(mr, rHB)
            if rHB > n:
                ok = False
        gem = m - n
        print(f"  m={m}: max rank(HB)={mr} (= n={n})   Gemini's ~m-n would be {gem}"
              f"{'   <-- DIVERGES' if gem != mr else ''}")
    print()
    print(f"VERDICT: rank(HB) <= n={n} for all m {'CONFIRMED' if ok else 'FAILED'}.")
    print("  => H(syndrome|C) <= n bits, NOT m-n. Gemini's step 3 (HB full-rank")
    print("  random) violates HB*A = HC = 0. The syndrome cannot over-determine e;")
    print("  the reduction is NOT information-theoretically lossless. I(x;y|C) <= 0.378n")
    print("  (full-rank B), an UPPER bound consistent with the no-go. open core OPEN.")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
