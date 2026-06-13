#!/usr/bin/env python3
"""
542-CLAUDE-trackW-limit-rate-verification.py

Adjudication of Kimi Track W (fbcb43b): rigorous m->inf limit theorem with
explicit rates for uniform-B-per-A.

W-a: SD(P_full, P_lpn) >= 1 - rho(n)^m,
     rho(n) = 1 - (1/2^n)(1 - sqrt((1-p_eff)/2) - sqrt(p_eff/2)) (Hellinger).
W-b: Pr_lpn[y in col(C)] <= 2^n (1-p_eff)^m.
W-c: 1 - SD(P_out,P_lpn) <= (2-q)rho^m + (1-q)2^{n-m} + 2^n(1-p_eff)^m -> 0.

From-scratch checks (exact where possible):
  (1) rho(n) recomputed two ways: Kimi's closed form AND a direct per-row
      Hellinger affinity BC = sum sqrt(P_full(c,y) P_lpn(c,y)) over the exact
      per-row laws (I re-derive the per-row P_lpn: c!=0 -> uniform, c=0 ->
      Bernoulli(p_eff)). Match the table (0.99677 at n=2, etc.).
  (2) W-c bound is a valid UPPER bound on the TRUE 1-SD: compare against the
      exact full-SD table (Tracks F/L, n=2, m=8..80) -- bound >= 1-SD at every m.
  (3) per-row SD delta(n) = (1/2^n)(1/2 - p_eff) > 0 (ties to exp/442).
  (4) Hellinger tensorization sanity: SD(full^m, lpn^m) computed exactly at
      small m (my own product law) >= 1 - rho^m (the W-a bound holds).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import math
from fractions import Fraction


def p_eff(n):
    return (1 - Fraction(3, 4) ** (2 * n)) / 2


def q_graph(n):
    t = Fraction(3, 4) ** (2 * n)
    return t + (1 - t) / (2 ** n + 1)


def rho_closed(n):
    pe = float(p_eff(n))
    return 1 - (1 / 2 ** n) * (1 - math.sqrt((1 - pe) / 2) - math.sqrt(pe / 2))


def rho_direct(n):
    """per-row Hellinger affinity BC = sum sqrt(P_full P_lpn), my own per-row law."""
    pe = float(p_eff(n))
    N = 2 ** n  # number of c values; row space = (c in F_2^n, y in {0,1})
    bc = 0.0
    for c in range(N):
        for y in (0, 1):
            pf = 1.0 / (2 * N)               # P_full uniform
            if c != 0:
                pl = 1.0 / (2 * N)           # P_lpn: c!=0 -> y uniform
            else:
                pl = (1.0 / N) * ((1 - pe) if y == 0 else pe)  # c=0 -> Bernoulli
            bc += math.sqrt(pf * pl)
    return bc


# exact full-SD (Track F/L), n=2
FULL_SD_N2 = {
    8: "16905825785074125865887285/38685626227668133590597632",
    16: "776580527746517716721610547003155688886535620657255/1496577676626844588240573268701473812127674924007424",
    24: "16832756036765379095034202127924274618943844971887062499211392003318774009896365/29642774844752946028434172162224104410437116074403984394101141506025761187823616",
    48: "607477461132137352864009669432561278876547085540963876824000902259324180705585729760268074621527447131000809903636388269236874471512931193096020288141170484925/878694100496718043517683302282418331810487718418343092402491322775749527474899974671687634004666183037093927858109549828751614463963730408009475621262727315456",
    80: "6516657278891803832616236589954945406172739657093806040686943620569987057254109683197704791668274095220191620119308395368727282099557476622237619203792218538492257452368734407090320092262117702049733273480579682532654279485633996703894025267592898163193163092524325/8061134813471454564702450331367746071149403778627342561766978592325956765086744071570087522699847227396765060321916636335485039665263146015175460486800225477728068298324662539195732386420081192825687147647265448061340763744378078290380812053940375922997109693874176",
}


def w_c_bound(n, m):
    pe, q = float(p_eff(n)), float(q_graph(n))
    rho = rho_closed(n)
    return (2 - q) * rho ** m + (1 - q) * 2 ** (n - m) + 2 ** n * (1 - pe) ** m


def main():
    ok = True
    print("=" * 74)
    print("542-CLAUDE  Track W — limit theorem rates: verification")
    print("=" * 74)

    print("\n(1) rho(n): Kimi closed form vs direct per-row Hellinger:")
    for n, expect in ((2, 0.9967680961), (3, 0.9995000745), (4, 0.9999214519)):
        rc, rd = rho_closed(n), rho_direct(n)
        m1 = abs(rc - rd) < 1e-12
        m2 = abs(rc - expect) < 1e-9
        ok &= m1 and m2 and rc < 1
        print(f"   n={n}: closed={rc:.10f} direct={rd:.10f} (match {m1}); "
              f"vs table {expect}: {'OK' if m2 else 'FAIL'}; rho<1: {rc < 1}")

    print("\n(2) per-row SD delta(n) = (1/2^n)(1/2 - p_eff) > 0:")
    for n in (2, 3, 4):
        d = Fraction(1, 2 ** n) * (Fraction(1, 2) - p_eff(n))
        ok &= d > 0
        print(f"   n={n}: delta = {d} = {float(d):.6e} (>0: {d > 0})")

    print("\n(3) W-c bound is a valid UPPER bound on true 1-SD (n=2, Track F/L):")
    for m in (8, 16, 24, 48, 80):
        true_1sd = 1 - float(Fraction(FULL_SD_N2[m]))
        bnd = w_c_bound(2, m)
        valid = bnd >= true_1sd - 1e-9
        ok &= valid
        print(f"   m={m:>2}: true 1-SD = {true_1sd:.6f}  bound = {bnd:.6f}  "
              f"{'OK (>=)' if valid else '*** bound < true ***'}")
    print("   (bound is loose because rho(2)=0.9968 ~ 1; valid upper bound,")
    print("    -> 0 only for large m. This is the honest rate.)")

    # (4) Hellinger tensorization sanity at small m: exact SD(full^m, lpn^m)
    print("\n(4) Hellinger W-a bound at small m (n=2, exact full-vs-lpn SD):")
    n = 2
    pe = p_eff(n)
    from math import comb

    def sd_full_lpn(m):
        # only c=0 rows distinguish; #c=0 ~ Bin(m, 1/2^n)
        tot = Fraction(0)
        for k in range(m + 1):
            wk = Fraction(comb(m, k), 2 ** (n * m)) * (2 ** n - 1) ** (m - k)
            s = Fraction(0)
            for j in range(k + 1):
                pj = pe ** j * (1 - pe) ** (k - j)
                s += abs(pj - Fraction(1, 2 ** k)) * comb(k, j)
            tot += wk * s / 2
        return tot

    rho = rho_closed(2)
    for m in (1, 2, 4, 8):
        sd = sd_full_lpn(m)
        wa = 1 - rho ** m
        valid = float(sd) >= wa - 1e-9
        ok &= valid
        print(f"   m={m}: exact SD(full,lpn)={float(sd):.6f} >= 1-rho^m={wa:.6f} "
              f"{'OK' if valid else 'FAIL'}")

    print("\n" + "=" * 74)
    print("RESULT:", "ALL CHECKS PASS — Track W THEOREM ACCEPT (explicit rates valid)"
          if ok else "FAILURE")
    print("  lim SD=1 for uniform-B-per-A, rate O(rho(n)^m), rho(n)<1 fixed n.")
    print("  General randomized B stays OPEN (lem:m2 core).")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
