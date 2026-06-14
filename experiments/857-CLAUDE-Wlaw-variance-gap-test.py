#!/usr/bin/env python3
"""
857-CLAUDE-Wlaw-variance-gap-test.py

Tests Gemini's proposed lem:m2 distinguisher: the FULL distribution of the
min-syndrome-weight W = min_x wt(y + Cx), specifically its VARIANCE. Gemini's
claim (OBSTRUCT, lem:m2 holds): for the marginal-uniform reduction output, W
concentrates at the random-code covering radius (variance O(1), a narrow spike),
whereas genuine LPN_{p'} has W = wt(e') ~ Binomial(m, p') (variance Theta(m), a
wide bell). The variance gap would be a non-vanishing distinguisher even though
the W=0 spike (q_graph) vanishes.

DISCIPLINE (post-Theta(n)-retraction): do NOT endorse Gemini's hand-wave
("marginal-uniform => Be uniform => random coset"); Be is confined to a <=2n-dim
subspace, NOT uniform in F_2^m. Compute the ACTUAL W-distribution exactly and
check the variance gap directly.

Computed (n=2, exact, uniform-B-per-A reduction output vs matched LPN_{p_eff},
p_eff = 175/512, m = 4..8):
  - W-distribution P(W=k) for both.
  - mean, variance of W for both.
  - P(W=0) (the vanishing spike) for both.
  - SD(W_red, W_LPN) and whether the variance ratio Var_LPN/Var_red grows in m.

If Var(W_red) stays ~flat while Var(W_LPN) grows ~m, Gemini's distinguisher is
real (EVIDENCE). If Var(W_red) also grows / SD stays small, it is not (and lem:m2
single-block may be undistinguishable -- the construct side).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction as Fr
from itertools import combinations, product

P = Fr(1, 4)
PEFF = Fr(175, 512)
NN = 4  # 2n, n=2
n = 2


def omega(a, b):
    s = 0
    for i in range(2):
        s ^= (((a >> i) & 1) & ((b >> (i + 2)) & 1)) ^ \
             (((a >> (i + 2)) & 1) & ((b >> i) & 1))
    return s


def lags():
    out = set()
    for bb in combinations(range(1, 1 << NN), 2):
        sp = {0}
        for x in bb:
            sp |= {y ^ x for y in sp}
        if len(sp) != 4:
            continue
        if any(omega(u, v) for u in sp for v in sp):
            continue
        out.add(frozenset(sp))
    return [sorted(s) for s in out]


LAGS = lags()


def bases_of(L):
    nz = [v for v in L if v]
    return [(a0, a1) for a0, a1 in product(nz, nz)
            if a0 != a1 and {0, a0, a1, a0 ^ a1} == set(L)]


def dot(a, b):
    return bin(a & b).count("1") & 1


def uniformB_output(m):
    """exact P(C,y) for uniform-B-per-A, row-factored (ordered-basis measure)."""
    out = {}
    wL = Fr(1, len(LAGS))
    for L in LAGS:
        Bs = bases_of(L)
        wA = wL / len(Bs)
        for (a0, a1) in Bs:
            for x in range(4):
                Ax = (a0 if x & 1 else 0) ^ (a1 if x & 2 else 0)
                for e in range(1 << NN):
                    we = P ** bin(e).count("1") * (1 - P) ** (NN - bin(e).count("1"))
                    v = Ax ^ e
                    pr = {}
                    for r in range(1 << NN):
                        k = (dot(r, a0), dot(r, a1), dot(r, v))
                        pr[k] = pr.get(k, Fr(0)) + Fr(1, 16)
                    dist = {(0, 0): Fr(1)}
                    for i in range(m):
                        nd = {}
                        for (Cc, yy), w in dist.items():
                            for (c0, c1, yb), pw in pr.items():
                                key = (Cc | ((c0 | (c1 << 1)) << (2 * i)), yy | (yb << i))
                                nd[key] = nd.get(key, Fr(0)) + w * pw
                        dist = nd
                    w0 = wA * Fr(1, 4) * we
                    for (C, y), pw in dist.items():
                        out[(C, y)] = out.get((C, y), Fr(0)) + w0 * pw
    return out


def lpn_law(p, m):
    law = {}
    wC = Fr(1, 2 ** (2 * m))
    for Cbits in range(1 << (2 * m)):
        crow = [(Cbits >> (2 * i)) & 3 for i in range(m)]
        for x in range(4):
            cx = 0
            for i, r in enumerate(crow):
                cx |= (bin(r & x).count("1") & 1) << i
            for e in range(1 << m):
                w = wC * Fr(1, 4) * p ** bin(e).count("1") * (1 - p) ** (m - bin(e).count("1"))
                law[(Cbits, cx ^ e)] = law.get((Cbits, cx ^ e), Fr(0)) + w
    return law


def Wval(Cbits, y, m):
    crow = [(Cbits >> (2 * i)) & 3 for i in range(m)]
    best = m + 1
    for x in range(4):
        cx = 0
        for i, r in enumerate(crow):
            cx |= (bin(r & x).count("1") & 1) << i
        w = bin(y ^ cx).count("1")
        if w < best:
            best = w
    return best


def Wdist(law, m):
    d = {}
    for (C, y), p in law.items():
        k = Wval(C, y, m)
        d[k] = d.get(k, Fr(0)) + p
    return d


def stats(d):
    mean = sum(k * p for k, p in d.items())
    var = sum((k * k) * p for k, p in d.items()) - mean * mean
    return float(mean), float(var)


def SDdist(d1, d2):
    ks = set(d1) | set(d2)
    return float(sum(abs(d1.get(k, Fr(0)) - d2.get(k, Fr(0))) for k in ks) / 2)


def main():
    print("=" * 78)
    print("857-CLAUDE  W-law variance-gap test (Gemini lem:m2 distinguisher), n=2")
    print("=" * 78)
    print(f"  {'m':>2} {'mean_red':>9} {'var_red':>8} {'mean_LPN':>9} {'var_LPN':>8} "
          f"{'P0_red':>7} {'P0_LPN':>7} {'SD(W)':>7} {'varLPN/varRed':>13}")
    prev_ratio = None
    for m in (4, 5, 6):
        red = uniformB_output(m)
        lpn = lpn_law(PEFF, m)
        wr = Wdist(red, m)
        wl = Wdist(lpn, m)
        mr, vr = stats(wr)
        ml, vl = stats(wl)
        p0r = float(wr.get(0, Fr(0)))
        p0l = float(wl.get(0, Fr(0)))
        sd = SDdist(wr, wl)
        ratio = vl / vr if vr > 1e-12 else float('inf')
        print(f"  {m:>2} {mr:>9.4f} {vr:>8.4f} {ml:>9.4f} {vl:>8.4f} "
              f"{p0r:>7.4f} {p0l:>7.4f} {sd:>7.4f} {ratio:>13.2f}")
    print()
    print("  READ (disciplined -- direct, not Gemini's hand-wave):")
    print("  - Gemini OBSTRUCT predicts: var_red ~ flat (O(1)), var_LPN ~ grows (Theta(m)),")
    print("    so varLPN/varRed GROWS and SD(W) stays bounded away from 0 -> lem:m2 holds.")
    print("  - If var_red ALSO grows / SD(W) shrinks -> Gemini's variance-gap is not a")
    print("    non-vanishing distinguisher at these sizes; the question stays OPEN/construct.")
    print("  NB: P0_red is the vanishing q_graph spike; the test is the REST of the W-law.")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
