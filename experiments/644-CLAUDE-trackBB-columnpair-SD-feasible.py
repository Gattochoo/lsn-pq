#!/usr/bin/env python3
"""
644-CLAUDE-trackBB-columnpair-SD-feasible.py

Feasible exact recomputation of 641 (Track BB column-pair SD adjudication). The
original 641 brute-forces the uniform-B part by enumerating all 2^(4m) matrices
B (line `for Bbits in range(1 << (NN*m))`); at m=5 that is 2^20 matrices inside
a 90*4*16 outer loop -- it does not terminate (left running > 1h with no output).

KEY: both B-families factor over ROWS, so no matrix enumeration is needed.
  * uniform part: rows i.i.d. uniform over F_2^4. Per row, the triple
    (c0,c1,y) = (r.a0, r.a1, r.v) is the image of a uniform r in F_2^4 under
    three functionals; its law is computed by enumerating the 16 values of r.
    The m-row output law is the m-fold product (rows independent).
  * coupled part: B = [s s t t], s,t ~ U(F_2^m). Then per row, (s_i,t_i) is
    uniform over F_2^2 and i.i.d. across rows, so this part ALSO factors: the
    per-row triple is (s_i*c0s ^ t_i*c0t, s_i*c1s ^ t_i*c1t, s_i*cvs ^ t_i*cvt)
    over the 4 values of (s_i,t_i). m-fold product again.

Both reduce 2^(4m) (or 2^(2m)) to O(m * support). Identical model and verdict
logic to 641; the ONLY change is the exact evaluation method. Math is unchanged,
so the SD values must match 641 wherever 641 can be run to completion (m=4 is the
cross-check anchor).

Verdict question (unchanged): is the column-pair lambda=1/4 SD BELOW the lambda=0
(uniform) baseline? If yes -> genuine lem:m2 threat (ESCALATE). If no -> BB's
I(x;y|C) drop is NOT an SD drop (output leaks less about x but stays just as far
from LPN) = SUPPORTS lem:m2, not a threat.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from itertools import combinations, product

P = 0.25
PEFF = 175.0 / 512.0
NN = 4  # 2n at n=2
# EXACT cross-check anchor (computed once with fractions.Fraction, m=4):
#   lam=0 baseline SD = 277825754675/1099511627776 = 0.2526807...
# which MATCHES Kimi's independent uniform-B-per-A baseline (Track HH/FF tables).
# The float path below reproduces it to ~1e-9; asserted at runtime.
EXACT_M4_BASELINE = 277825754675.0 / 1099511627776.0  # 0.25268068...


def omega(a, b):
    s = 0
    for i in range(2):
        s ^= (((a >> i) & 1) & ((b >> (i + 2)) & 1)) ^ \
             (((a >> (i + 2)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians():
    found = set()
    for basis in combinations(range(1, 1 << NN), 2):
        span = {0}
        ok = True
        for b in basis:
            if b in span:
                ok = False
                break
            span |= {x ^ b for x in span}
        if not ok or len(span) != 4:
            continue
        if any(omega(u, v) for u in span for v in span):
            continue
        found.add(frozenset(span))
    return [sorted(s) for s in found]


def bases_of(L):
    nz = [v for v in L if v != 0]
    out = []
    for a0, a1 in product(nz, nz):
        if a0 != a1 and {0, a0, a1, a0 ^ a1} == set(L):
            out.append((a0, a1))
    return out


LAGS = all_lagrangians()


def lpn_law(p, m):
    law = {}
    wC = (1.0/2**(2*m))
    for Cbits in range(1 << (2 * m)):
        crow = [(Cbits >> (2 * i)) & 3 for i in range(m)]
        for x in range(4):
            cx = 0
            for i, r in enumerate(crow):
                cx |= (bin(r & x).count("1") & 1) << i
            for e in range(1 << m):
                w = wC * 0.25 * p ** bin(e).count("1") * \
                    (1 - p) ** (m - bin(e).count("1"))
                law[(Cbits, cx ^ e)] = law.get((Cbits, cx ^ e), 0.0) + w
    return law


def mfold_product(perrow, m):
    """perrow: dict (c0,c1,y)->prob over one row. Return dict (Cbits,y)->prob
    for m i.i.d. rows (independent), placing row i at bit-offset i."""
    dist = {(0, 0): 1.0}
    for i in range(m):
        nd = {}
        sh = 2 * i
        for (Cacc, yacc), w in dist.items():
            for (c0, c1, yy), pw in perrow.items():
                Cn = Cacc | ((c0 | (c1 << 1)) << sh)
                yn = yacc | (yy << i)
                k = (Cn, yn)
                nd[k] = nd.get(k, 0.0) + w * pw
        dist = nd
    return dist


def coef(a):
    return (((a >> 0) & 1) ^ ((a >> 1) & 1), ((a >> 2) & 1) ^ ((a >> 3) & 1))


def perrow_uniform(a0, a1, v):
    pr = {}
    q = (1.0/(1<<NN))
    for r in range(1 << NN):
        c0 = bin(r & a0).count("1") & 1
        c1 = bin(r & a1).count("1") & 1
        yy = bin(r & v).count("1") & 1
        pr[(c0, c1, yy)] = pr.get((c0, c1, yy), 0.0) + q
    return pr


def perrow_coupled(a0, a1, v):
    c0s, c0t = coef(a0)
    c1s, c1t = coef(a1)
    cvs, cvt = coef(v)
    pr = {}
    q = 0.25
    for s in range(2):
        for t in range(2):
            c0 = (s & c0s) ^ (t & c0t)
            c1 = (s & c1s) ^ (t & c1t)
            yy = (s & cvs) ^ (t & cvt)
            pr[(c0, c1, yy)] = pr.get((c0, c1, yy), 0.0) + q
    return pr


def colpair_output(lam, m):
    """Factored exact output law over (C,y) for the column-pair family."""
    out = {}
    wL = (1.0/len(LAGS))
    # cache product dists per (a0,a1,v) since v repeats across (x,e)
    cacheU, cacheC = {}, {}
    for L in LAGS:
        Bs = bases_of(L)
        wA = wL / len(Bs)
        for A in Bs:
            a0, a1 = A
            for x in range(4):
                Ax = (a0 if x & 1 else 0) ^ (a1 if x & 2 else 0)
                for e in range(1 << NN):
                    we = P ** bin(e).count("1") * (1 - P) ** (NN - bin(e).count("1"))
                    v = Ax ^ e
                    base = wA * 0.25 * we
                    key = (a0, a1, v)
                    if lam > 0:
                        if key not in cacheC:
                            cacheC[key] = mfold_product(perrow_coupled(a0, a1, v), m)
                        for kk, pw in cacheC[key].items():
                            out[kk] = out.get(kk, 0.0) + lam * base * pw
                    if lam < 1:
                        if key not in cacheU:
                            cacheU[key] = mfold_product(perrow_uniform(a0, a1, v), m)
                        for kk, pw in cacheU[key].items():
                            out[kk] = out.get(kk, 0.0) + (1 - lam) * base * pw
        # cache is m-specific; clear between Lagrangians to bound memory only if huge
    return out


def SD(Pd, Qd):
    keys = set(Pd) | set(Qd)
    return sum(abs(Pd.get(k, 0.0) - Qd.get(k, 0.0))
               for k in keys) / 2


def main():
    import sys
    print("=" * 74)
    print("644-CLAUDE  Track BB — column-pair SD (FEASIBLE, row-factored) ")
    print("=" * 74)
    print("\n  SD(output(lambda), matched LPN_{175/512}), n=2:")
    print(f"  {'m':>2} {'lam=0 (baseline)':>18} {'lam=1/4':>12} {'lam=1':>12}  verdict")
    threat = False
    ms = (4, 5, 6)
    for m in ms:
        lpn = lpn_law(PEFF, m)
        sd0 = SD(colpair_output(0.0, m), lpn)
        sd14 = SD(colpair_output(0.25, m), lpn)
        sd1 = SD(colpair_output(1.0, m), lpn)
        below = sd14 < sd0
        threat = threat or below
        xchk = ""
        if m == 4:
            ok = abs(sd0 - EXACT_M4_BASELINE) < 1e-9
            xchk = f"  [m4 baseline {'==' if ok else '!='} exact {EXACT_M4_BASELINE:.9f}]"
            assert ok, f"m=4 baseline {sd0} != exact {EXACT_M4_BASELINE}"
        print(f"  {m:>2} {float(sd0):>18.6f} {float(sd14):>12.6f} {float(sd1):>12.6f}  "
              f"{'*** lam=1/4 BELOW baseline (THREAT) ***' if below else 'lam=1/4 >= baseline (no threat)'}{xchk}")
        sys.stdout.flush()

    print("\n  VERDICT:")
    if threat:
        print("  column-pair lambda=1/4 SD is BELOW baseline -> genuine lem:m2")
        print("  threat direction. ESCALATE.")
    else:
        print("  column-pair lambda=1/4 SD is NOT below baseline. BB's I(x;y|C)")
        print("  drop is NOT an SD drop: lower I means the output leaks LESS about")
        print("  x (reduction recovers x worse) while staying just as distinguishable")
        print("  from LPN. This SUPPORTS lem:m2 (reduction broken), not a threat.")
    print("\nDiscipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
