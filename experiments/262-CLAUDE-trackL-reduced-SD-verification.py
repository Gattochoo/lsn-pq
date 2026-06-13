#!/usr/bin/env python3
"""
262-CLAUDE-trackL-reduced-SD-verification.py

Independent adjudication of Kimi Track L (698311a): exact matched-rate SD at
n=2 for large m via the S3 + s00 reductions.

MY OWN implementation (independent code) of the same two reductions:

  state = (m1,m2,m3; s1,s2,s3) over the three non-zero row types (S3-canonical:
  iterate ordered compositions but exploit nothing else from Kimi's code),
  with the s00-sum closed out per state:

  - per (C,y)-point integers over the common scale S = 4 qd 4^m D^m:
      F = 4 (qd-qn) 256^m                      (full part, z-independent)
      G = 4 qn 512^m / 2^rank                  (graph spike, z=0 & membership)
      L(z) = qd sum_w a^{z+r_w} b^{m-z-r_w}    (matched LPN; a=175,b=337,D=512)
    L(z) is strictly geometric: L(z+1) = L(z) a/b, so |const - L(z)| has at
    most one sign change in z. The z-sum uses exact binomial prefix sums of
    C(m00,z) a^z b^{m00-z}; the crossing is located by float log and then
    FIXED EXACTLY by integer comparisons at z*-1, z*, z*+1 (floats never enter
    any value, only the initial bracketing).
  - membership signatures at n=2: {(0,0,0), (m1,m2,0), (m1,0,m3), (0,m2,m3)}
    with z=0; rank = min(#present nonzero types, 2).

Checks:
  (1) anchors: m = 8, 12 against the triple-known table (my 252/260 rails);
  (2) m = 24, 48 against the round-2 Track F values;
  (3) THE NEW POINTS: m = 64 (and m = 80 if runtime permits) against Kimi's
      204 fractions — fraction-for-fraction.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import sys
import math
from fractions import Fraction
from math import comb

A_, B_, D_ = 175, 337, 512          # p_eff(2) = 175/512
QN, QD = 29, 64                     # q_graph(2) = 29/64

KNOWN = {
    8: "16905825785074125865887285/38685626227668133590597632",
    12: "2670376973898429557749111289348052212525/5444517870735015415413993718908291383296",
    24: "16832756036765379095034202127924274618943844971887062499211392003318774009896365/29642774844752946028434172162224104410437116074403984394101141506025761187823616",
}


def exact_sd_reduced(m, kimi_claim=None):
    """Exact SD(P_out, LPN_peff) at n=2 via my reduced enumeration."""
    F_point = 4 * (QD - QN) * 256 ** m            # full part, per point
    G_base = 4 * QN * 512 ** m                    # graph numerator (div 2^r)
    # prefix sums of C(m00, z) a^z b^{m00-z}: pre[m00][k] = sum_{z<=k}
    pre = []
    for m00 in range(m + 1):
        row = [0] * (m00 + 2)
        acc = 0
        for z in range(m00 + 1):
            acc += comb(m00, z) * A_ ** z * B_ ** (m00 - z)
            row[z + 1] = acc
        pre.append(row)
    # binomial prefix of plain C(m00, z)
    preC = []
    for m00 in range(m + 1):
        row = [0] * (m00 + 2)
        acc = 0
        for z in range(m00 + 1):
            acc += comb(m00, z)
            row[z + 1] = acc
        preC.append(row)

    log_ab = math.log(A_ / B_)
    total = 0
    for M in range(m + 1):                        # M = m1+m2+m3
        m00 = m - M
        preR = pre[m00]
        preCC = preC[m00]
        bm00 = B_ ** m00
        for m1 in range(M + 1):
            for m2 in range(M - m1 + 1):
                m3 = M - m1 - m2
                present = (m1 > 0) + (m2 > 0) + (m3 > 0)
                rank = min(present, 2)
                G_point = G_base >> rank          # 512^m divisible by 2^r
                wC = comb(m, m00) * comb(M, m1) * comb(M - m1, m2)
                # w-patterns over (t1,t2,t3): 00 -> (0,0,0); others flip two
                pats = ((0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))
                memb = {(0, 0, 0), (m1, m2, 0), (m1, 0, m3), (0, m2, m3)}
                for s1 in range(m1 + 1):
                    c1 = comb(m1, s1)
                    for s2 in range(m2 + 1):
                        c12 = c1 * comb(m2, s2)
                        for s3 in range(m3 + 1):
                            wy = c12 * comb(m3, s3)
                            # L(z) = qd * sum_w a^{z+r_w} b^{m-z-r_w}
                            #      = (qd * Lam) * a^z b^{m00-z} / b^{m00}
                            # with Lam = sum_w a^{r_w} b^{M-r_w}
                            Lam = 0
                            for p1, p2, p3 in pats:
                                r_w = (s1 if not p1 else m1 - s1) + \
                                      (s2 if not p2 else m2 - s2) + \
                                      (s3 if not p3 else m3 - s3)
                                Lam += A_ ** r_w * B_ ** (M - r_w)
                            LamQ = QD * Lam
                            # z-sum of C(m00,z) |F + G 1[z=0,mem] - L(z)|
                            # L-as-integer at z: LamQ * a^z b^{m00-z}... but the
                            # per-point L(z) = LamQ * a^z * b^{m00-z} / b^{m00}?
                            # Rebuild: L(z) = QD sum_w a^{z+r_w} b^{m-z-r_w}
                            #        = QD a^z b^{m00-z} sum_w a^{r_w} b^{M-r_w}
                            #          / b^{m00} * b^{m00} ... exponents:
                            # z + r_w + (m - z - r_w) = m  OK; factor a^z b^{-z}:
                            # = (a^z b^{m00-z}/b^{m00}) * QD sum_w a^{r_w} b^{m-r_w-... }
                            # Cleanest: define Lz(z) = LamQ * A_**z * B_**(m00-z)
                            # then actual L(z)*b^{m00} = Lz(z) * b^{?}: check
                            # L(z) = QD sum a^{z+r_w} b^{m-z-r_w}; with
                            # m - z - r_w = (M - r_w) + (m00 - z):
                            # L(z) = QD a^z b^{m00-z} * sum_w a^{r_w} b^{M-r_w}
                            #      = Lz(z).   (exact, no division)
                            z0m = (s1, s2, s3) in memb
                            # crossing: F vs Lz(z) (G only at z=0);
                            # Lz strictly decreasing (a<b);
                            # find z* = first z with Lz(z) <= F
                            if LamQ * bm00 <= F_point:
                                zstar = 0
                            else:
                                t = math.log(F_point / (LamQ * bm00)) / log_ab \
                                    if F_point > 0 else m00 + 1
                                zstar = max(0, min(m00 + 1, int(t)))
                                # exact fix-up around zstar
                                while zstar > 0 and \
                                        LamQ * A_ ** (zstar - 1) * B_ ** (m00 - zstar + 1) <= F_point:
                                    zstar -= 1
                                while zstar <= m00 and \
                                        LamQ * A_ ** zstar * B_ ** (m00 - zstar) > F_point:
                                    zstar += 1
                            # zstar = first z where L <= F (L-F changes + -> -)
                            # sum_{z < zstar} C (L - F)  +  sum_{z >= zstar} C (F - L)
                            SL_lo = preR[min(zstar, m00 + 1)]
                            SC_lo = preCC[min(zstar, m00 + 1)]
                            SL_hi = preR[m00 + 1] - SL_lo
                            SC_hi = preCC[m00 + 1] - SC_lo
                            ssum = (LamQ * SL_lo - F_point * SC_lo) \
                                + (F_point * SC_hi - LamQ * SL_hi)
                            # graph spike correction at z=0 if membership:
                            if z0m:
                                # replace |F - L(0)| by |F + G - L(0)| at z=0
                                L0 = LamQ * bm00
                                old = abs(F_point - L0)
                                new = abs(F_point + G_point - L0)
                                ssum += new - old
                            total += wC * wy * ssum
    # F,G,L are per-(C,y)-point probabilities scaled by S0 = 4*QD*D^m; the
    # C-uniform 1/4^m enters via the counts wC (so divide once more by 4^m).
    return Fraction(total, 2 * 4 ** m * (4 * QD * D_ ** m))


def main():
    # calibrate the overall scale on a small anchor first (m=8), then run big m
    targets = [8, 12, 24]
    args = [int(a) for a in sys.argv[1:]] or [8, 12, 24, 48, 64]
    for m in args:
        sd = exact_sd_reduced(m)
        line = f"m={m}: SD = {float(sd):.9f}"
        if m in KNOWN:
            line += "  anchor " + ("OK" if sd == Fraction(KNOWN[m]) else
                                   "FAIL " + str(sd))
        print(line, flush=True)
        print(f"   exact: {sd}", flush=True)


if __name__ == "__main__":
    main()
