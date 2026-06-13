#!/usr/bin/env python3
"""
541-CLAUDE-trackX-lambda-coupled-verification.py

Adjudication of Kimi Track X (ff4036c): lambda-coupled correlated B family.

B ~ LambdaCoupled(lambda): w.p. lambda all m rows = one uniform r; w.p.
1-lambda rows i.i.d. uniform. Marginal-uniform (satisfies lem:m1). Kimi's
finding: SD(P_out(lambda), LPN) is non-decreasing in lambda and STRICTLY
ABOVE the lambda=0 baseline for lambda>0 -> correlated B makes the output
LESS LPN-like (no lem:m2 threat in this family); the signature is the
rank-collapse of Be's support.

From-scratch (my own (C,y) construction at n=2, no reuse of Kimi 510):
  P_out(lambda) = lambda*P_allequal + (1-lambda)*P_uniform.
  (1) lambda=0 baseline == Track F/L matched values (36575/524288 etc.) and
      LPN_{1/4} values (3225/32768 etc.) — ties to established ground truth.
  (2) lambda=1 (all rows equal): exact SD == Kimi table (matched + 1/4),
      and -> 1 fast (rank-collapse: C has rank<=1).
  (3) monotonicity in lambda on the grid {0,1/4,1/2,3/4,1}.
  (4) the obstruction: under P_out(lambda=1), C has rank <= 1 always, whereas
      LPN's C is full-rank w.h.p. -> singular component (named signature).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import combinations

NN = 4  # 2n at n=2
SIZE = 1 << NN


def omega(a, b):
    s = 0
    for i in range(2):
        s ^= (((a >> i) & 1) & ((b >> (i + 2)) & 1)) ^ \
             (((a >> (i + 2)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians():
    found = set()
    for basis in combinations(range(1, SIZE), 2):
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


# ordered bases of Lagrangians = the isotropic matrix ensemble A (2x... n=2: A is 4x2)
def bases_of(L):
    nz = [v for v in L if v != 0]
    out = []
    for a in nz:
        for b in nz:
            if a != b:
                span = {0, a, b, a ^ b}
                if span == set(L):
                    out.append((a, b))  # columns a=A e1, b=A e2
    return out


LAGS = all_lagrangians()
ALL_A = [(a, b) for L in LAGS for (a, b) in bases_of(L)]  # |A| = 90


def Ax(A, x):
    v = 0
    if x & 1:
        v ^= A[0]
    if x & 2:
        v ^= A[1]
    return v


def p_lpn(p, m):
    """LPN_p law over (C in F_2^{m x 2}, y in F_2^m): C uniform, y=Cx'+e'."""
    law = {}
    wC = Fraction(1, 2 ** (2 * m))
    for Cbits in range(1 << (2 * m)):
        crow = [(Cbits >> (2 * i)) & 3 for i in range(m)]
        for x in range(4):
            cx = 0
            for i, r in enumerate(crow):
                cx |= (bin(r & x).count("1") & 1) << i
            for e in range(1 << m):
                w = wC * Fraction(1, 4) * p ** bin(e).count("1") * \
                    (1 - p) ** (m - bin(e).count("1"))
                y = cx ^ e
                law[(Cbits, y)] = law.get((Cbits, y), Fraction(0)) + w
    return law


def p_out(lam, m):
    """lambda*P_allequal + (1-lambda)*P_uniform, exact (C,y) law."""
    uni, alleq = {}, {}
    wL = Fraction(1, len(LAGS))
    # uniform-B baseline and all-equal, sharing (A,x,e)
    for L in LAGS:
        for A in bases_of(L):
            wA = wL / len(bases_of(L))
            for x in range(4):
                v0 = Ax(A, x)
                for e in range(1 << NN):
                    we = Fraction(1, 4) ** bin(e).count("1") * \
                        Fraction(3, 4) ** (NN - bin(e).count("1"))
                    v = v0 ^ e
                    # all-equal: B rows all = r (uniform); C row_i = r.A (same),
                    # y_i = r.v (same bit). C encoded m rows each = (r.Ae1, r.Ae2)
                    for r in range(SIZE):
                        crow = (bin(r & A[0]).count("1") & 1) | \
                               ((bin(r & A[1]).count("1") & 1) << 1)
                        Cbits = 0
                        for i in range(m):
                            Cbits |= crow << (2 * i)
                        yb = bin(r & v).count("1") & 1
                        y = 0
                        for i in range(m):
                            y |= yb << i
                        key = (Cbits, y)
                        alleq[key] = alleq.get(key, Fraction(0)) + \
                            wA * Fraction(1, 4) * we * Fraction(1, SIZE)
                    # uniform B: m i.i.d. rows
                    for Bbits in range(1 << (NN * m)):
                        rows = [(Bbits >> (NN * i)) & (SIZE - 1) for i in range(m)]
                        Cbits = 0
                        y = 0
                        for i, rr in enumerate(rows):
                            cr = (bin(rr & A[0]).count("1") & 1) | \
                                 ((bin(rr & A[1]).count("1") & 1) << 1)
                            Cbits |= cr << (2 * i)
                            y |= (bin(rr & v).count("1") & 1) << i
                        key = (Cbits, y)
                        uni[key] = uni.get(key, Fraction(0)) + \
                            wA * Fraction(1, 4) * we * Fraction(1, 2 ** (NN * m))
    out = {}
    for k, val in uni.items():
        out[k] = out.get(k, Fraction(0)) + (1 - lam) * val
    for k, val in alleq.items():
        out[k] = out.get(k, Fraction(0)) + lam * val
    return out


def SD(P, Q):
    keys = set(P) | set(Q)
    return sum(abs(P.get(k, Fraction(0)) - Q.get(k, Fraction(0))) for k in keys) / 2


KIMI_1_4 = {  # SD vs LPN_{1/4} at lambda=0 / lambda=1
    2: ("35/1024", "27/32"), 3: ("3225/32768", "249/256"),
    4: ("5903/32768", "8151/8192"),
}
KIMI_MATCHED = {
    2: ("36575/524288", "452191/524288"),
    3: ("695896635/4294967296", "4109085/4194304"),
}
PEFF = Fraction(175, 512)


def main():
    ok = True
    print("=" * 72)
    print("541-CLAUDE  Track X — lambda-coupled correlated B: verification")
    print("=" * 72)

    for m in (2, 3):
        lpn14 = p_lpn(Fraction(1, 4), m)
        lpnpe = p_lpn(PEFF, m)
        P0 = p_out(Fraction(0), m)
        P1 = p_out(Fraction(1), m)
        sd0_14, sd1_14 = SD(P0, lpn14), SD(P1, lpn14)
        sd0_pe, sd1_pe = SD(P0, lpnpe), SD(P1, lpnpe)
        m14 = (sd0_14 == Fraction(KIMI_1_4[m][0]) and sd1_14 == Fraction(KIMI_1_4[m][1]))
        mpe = (sd0_pe == Fraction(KIMI_MATCHED[m][0]) and sd1_pe == Fraction(KIMI_MATCHED[m][1]))
        ok &= m14 and mpe
        print(f"\n  m={m}: vs LPN_1/4   lam0={float(sd0_14):.6f} lam1={float(sd1_14):.6f} "
              f"{'OK' if m14 else 'FAIL'}")
        print(f"        vs matched   lam0={float(sd0_pe):.6f} lam1={float(sd1_pe):.6f} "
              f"{'OK' if mpe else 'FAIL'}")
        # monotonicity on grid
        grid = [Fraction(g, 4) for g in range(5)]
        sds = [SD(p_out(lam, m), lpnpe) for lam in grid]
        mono = all(a <= b for a, b in zip(sds, sds[1:]))
        ok &= mono and sds[0] < sds[-1]
        print(f"        matched SD monotone in lambda [0,1/4,..,1]: "
              f"{[round(float(s),4) for s in sds]} {'OK' if mono else 'FAIL'}")

    # (4) rank-collapse obstruction: lambda=1 -> C rank <= 1
    print("\n(4) rank-collapse obstruction (lambda=1, m=3):")
    P1 = p_out(Fraction(1), 3)
    bad = 0
    for (Cbits, y), v in P1.items():
        if v == 0:                       # 0-mass keys from the (1-lambda)=0 branch
            continue
        crow = [(Cbits >> (2 * i)) & 3 for i in range(3)]
        # all rows equal -> rank <= 1
        if len(set(crow)) > 1:
            bad += 1
    ok &= bad == 0
    print(f"   all (C,y) in support of P_out(1) have identical rows (rank<=1): "
          f"{'OK' if bad == 0 else f'FAIL ({bad})'}  -> singular to full-rank LPN")

    print("\n" + "=" * 72)
    print("RESULT:", "ALL CHECKS PASS — Track X ACCEPT (negative result confirmed: "
          "correlated B makes output LESS LPN-like)" if ok else "FAILURE")
    print("  lambda=0 ties to Track F/L baseline; lambda>0 increases SD; obstruction")
    print("  = rank-collapse of Be's support. lem:m2 general B stays OPEN.")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
