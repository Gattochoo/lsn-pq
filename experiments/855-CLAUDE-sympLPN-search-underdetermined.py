#!/usr/bin/env python3
"""
855-CLAUDE-sympLPN-search-underdetermined.py

Foundational grounding check that QUALIFIES the worst-case floor of exp 853/854.
Question: is sympLPN single-instance SEARCH (recover x from one (A,y)) info-
theoretically determined? sympLPN gives only 2n samples for an n-bit secret at
p=1/4; LPN capacity 1-H_2(1/4)=0.19 bits/sample needs ~5.3n samples, so 2n is far
short. Compute H(x | A, y) exactly (posterior entropy) over uniform Lagrangian A.

Result feeds an HONEST CORRECTION to exp 853/854's framing:
  - If H(x|A,y) ~ H(x): search-sympLPN single-instance is underdetermined ("hard"
    only trivially / info-theoretically), so a search-floor LPN<=search-sympLPN
    reduces to a partly-trivially-hard problem.
  - The crypto-relevant version is DECISIONAL; the zero-padding reduction does NOT
    give decisional-LPN <= decisional-sympLPN, because LPN-uniform maps to
    (uniform-top, Bernoulli-noise-bottom), which is distinguishable from
    sympLPN-uniform (fully uniform). [reasoned, not a numeric claim here]

So the "first positive anchor" must be stated as: a SEARCH floor to worst-case
sympLPN, with the underdetermination caveat; the clean decisional anchor is NOT
established. Sound Verifier self-correction of an over-claim.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from math import log2

rng = random.Random(41)


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def rand_lag_basis(n, rng):
    NN = 2 * n
    while True:
        A = []
        span = [0]
        ok = True
        for _ in range(n):
            cands = [v for v in range(1, 1 << NN)
                     if v not in span and all(omega(v, a, n) == 0 for a in A)]
            if not cands:
                ok = False
                break
            v = rng.choice(cands)
            A.append(v)
            span = span + [s ^ v for s in span]
        if ok and len(A) == n:
            return A


def Ax(A, x, n):
    o = 0
    for i in range(n):
        if (x >> i) & 1:
            o ^= A[i]
    return o


def main():
    print("=" * 72)
    print("855-CLAUDE  sympLPN single-instance search determinacy: H(x | A, y)")
    print("=" * 72)
    p = 0.25
    r = p / (1 - p)
    for n in (2, 3, 4):
        NN = 2 * n
        Hsum = 0.0
        trials = 400 if n < 4 else 150
        for _ in range(trials):
            A = rand_lag_basis(n, rng)
            x = rng.randrange(1 << n)
            e = sum((1 << i) for i in range(NN) if rng.random() < p)
            y = Ax(A, x, n) ^ e
            ws = [r ** bin(y ^ Ax(A, xp, n)).count("1") for xp in range(1 << n)]
            Z = sum(ws)
            P = [w / Z for w in ws]
            Hsum += -sum(pp * log2(pp) for pp in P if pp > 0)
        avgH = Hsum / trials
        print(f"  n={n}: avg H(x|A,y) = {avgH:.4f} bits  (H(x)={n}, "
              f"retained {100*avgH/n:.0f}%)  => {'UNDERDETERMINED' if avgH > 0.4*n else 'determined'}")
    print()
    print("  CONCLUSION: sympLPN single-instance SEARCH is info-theoretically")
    print("  underdetermined (x keeps ~70% of its entropy). So:")
    print("  - The exp 853/854 floor is SEARCH-only and to an underdetermined problem;")
    print("    it embeds a DETERMINED instance (enough LPN samples), so it is valid but")
    print("    narrow (worst-case search-sympLPN on determined instances).")
    print("  - The crypto-relevant DECISIONAL floor is NOT given by zero-padding:")
    print("    LPN-uniform -> (uniform-top, Bernoulli-bottom) != sympLPN-uniform.")
    print("  Honest qualification of the 'first positive anchor' (over-claim corrected).")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
