#!/usr/bin/env python3
"""
254-CLAUDE-trackD-pencil-verification.py

Independent adjudication of Kimi Track D (b4264f1 + 07174da):
conj:pencil evidence program.

Scale convention (matches the paper): <D_L, D_{L'}> = kappa 2^{j-2n} is LINEAR
in 2^j = |L cap L'|, so every ratio to rho_avg is computable on the raw
|L cap L'| scale (PRE-REGISTER #1 of Kimi's note is sound; verified here by
re-deriving the convention from lem:exact-corr + thm:distance, which is
diagonal-INCLUSIVE: Pr[j=n] = 1/|Lagr| > 0).

Checks (all exact integer/Fraction arithmetic, Lagrangians from scratch):
  (1) n=2: distance distribution vs thm:distance; rho_avg_raw = 8/5;
      EXHAUSTIVE max over all 2^15 subsets of the diagonal-inclusive average
      (expect max = 4, singletons only; ratio 2.5 < 5);
      exact size-3 maximum (expect 8/3, k=1 pencils).
  (2) n=3: distance distribution (64,56,14,1)/135; rho_avg_raw = 16/9;
      pencil census (63 / 315 / 135, pencil sizes 15 / 3 / 1);
      pencil ratios: k=1 -> 9/5, k=2 -> 3, k=3 (singleton) -> 9/2;
      EXACT maximum over ALL size-3 subsets (C(135,3) = 398,505) and ALL
      size-4 subsets (C(135,4) = 13,150,665) — strictly stronger than
      Kimi's search-based claims at these sizes.
  (3) Escalation check at the conjectured scale (|D'| >= 3 at n=3):
      does anything beat 5 rho_avg?

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import combinations

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
    return sorted(found, key=sorted)


def isotropic_subspaces(n, dim):
    """All totally isotropic subspaces of given dim (as frozensets)."""
    N = 2 * n
    found = set()
    for basis in combinations(range(1, 1 << N), dim):
        span = {0}
        ok = True
        for b in basis:
            if b in span:
                ok = False
                break
            span |= {x ^ b for x in span}
        if not ok or len(span) != 2 ** dim:
            continue
        if any(omega(u, v, n) for u in span for v in span):
            continue
        found.add(frozenset(span))
    return sorted(found, key=sorted)


def main():
    ok = True
    print("=" * 76)
    print("254-CLAUDE  Track D — conj:pencil: from-scratch adjudication")
    print("=" * 76)

    # ---------------- n = 2 ----------------
    n = 2
    lags2 = all_lagrangians(2)
    assert len(lags2) == 15
    M2 = [[len(a & b) for b in lags2] for a in lags2]

    # distance distribution & rho_avg
    from collections import Counter
    cnt = Counter()
    for i in range(15):
        for j in range(15):
            cnt[(len(lags2[i] & lags2[j]) - 1).bit_length()] += 1
    dist_ok = (cnt[2] == 15 and cnt[1] == 15 * 6 and cnt[0] == 15 * 8)
    rho2 = Fraction(sum(M2[i][j] for i in range(15) for j in range(15)), 15 * 15)
    ok &= dist_ok and rho2 == Fraction(8, 5)
    print(f"\n(1) n=2: distance dist (1,6,8)/15 per L: {'OK' if dist_ok else 'FAIL'};"
          f"  rho_avg_raw = {rho2} (expect 8/5)")

    # exhaustive over all 2^15 subsets
    best = Fraction(0)
    best_sets = []
    best3 = Fraction(0)
    best3_sets = []
    for mask in range(1, 1 << 15):
        idx = [i for i in range(15) if (mask >> i) & 1]
        s = len(idx)
        tot = sum(M2[i][j] for i in idx for j in idx)
        avg = Fraction(tot, s * s)
        if avg > best:
            best, best_sets = avg, [tuple(idx)]
        elif avg == best:
            best_sets.append(tuple(idx))
        if s == 3:
            if avg > best3:
                best3, best3_sets = avg, [tuple(idx)]
            elif avg == best3:
                best3_sets.append(tuple(idx))
    singletons_only = all(len(t) == 1 for t in best_sets)
    ok &= best == 4 and singletons_only
    print(f"   exhaustive 2^15: max avg = {best} (expect 4), attained by "
          f"{len(best_sets)} subsets, all singletons: {singletons_only}")
    print(f"   max ratio at scale (all non-empty) = {best/rho2} "
          f"(= 2.5? {'OK' if best/rho2 == Fraction(5,2) else 'FAIL'}) < 5  "
          f"-> conj:pencil HOLDS at n=2 (factor-2 margin)")
    ok &= best / rho2 == Fraction(5, 2)
    # size-3 maximisers: are they exactly the k=1 pencils?
    pencils2 = isotropic_subspaces(2, 1)
    pencil_sets = set()
    for W in pencils2:
        members = tuple(sorted(i for i, L in enumerate(lags2) if W <= L))
        if len(members) == 3:
            pencil_sets.add(members)
    b3 = set(tuple(sorted(t)) for t in best3_sets)
    ok &= best3 == Fraction(8, 3)
    print(f"   size-3 max = {best3} (expect 8/3), maximisers = {len(b3)}, "
          f"k=1 pencils = {len(pencil_sets)}, equal sets: {b3 == pencil_sets}")

    # ---------------- n = 3 ----------------
    n = 3
    lags3 = all_lagrangians(3)
    assert len(lags3) == 135
    M3 = [[len(a & b) for b in lags3] for a in lags3]
    cnt3 = Counter()
    L0 = lags3[0]
    for j in range(135):
        cnt3[(len(L0 & lags3[j]) - 1).bit_length()] += 1
    dist3_ok = (cnt3[3], cnt3[2], cnt3[1], cnt3[0]) == (1, 14, 56, 64)
    rho3 = Fraction(sum(M3[i][j] for i in range(135) for j in range(135)),
                    135 * 135)
    ok &= dist3_ok and rho3 == Fraction(16, 9)
    print(f"\n(2) n=3: distance dist (1,14,56,64)/135: {'OK' if dist3_ok else 'FAIL'};"
          f"  rho_avg_raw = {rho3} (expect 16/9);  5*rho_avg = {5*rho3}")

    # pencil census
    iso1 = isotropic_subspaces(3, 1)
    iso2 = isotropic_subspaces(3, 2)
    sizes1 = {sum(1 for L in lags3 if W <= L) for W in iso1}
    sizes2 = {sum(1 for L in lags3 if W <= L) for W in iso2}
    census_ok = (len(iso1), len(iso2), sizes1, sizes2) == (63, 315, {15}, {3})
    ok &= census_ok
    print(f"   pencil census: |k=1| = {len(iso1)} (63), |k=2| = {len(iso2)} "
          f"(315), sizes {sizes1}/{sizes2} (15/3): {'OK' if census_ok else 'FAIL'}")

    # pencil ratios
    W1 = iso1[0]
    P1 = [i for i, L in enumerate(lags3) if W1 <= L]
    avg1 = Fraction(sum(M3[i][j] for i in P1 for j in P1), len(P1) ** 2)
    W2 = iso2[0]
    P2 = [i for i, L in enumerate(lags3) if W2 <= L]
    avg2 = Fraction(sum(M3[i][j] for i in P2 for j in P2), len(P2) ** 2)
    r1, r2 = avg1 / rho3, avg2 / rho3
    ok &= r1 == Fraction(9, 5) and r2 == 3
    print(f"   k=1 pencil ratio = {r1} (expect 9/5); k=2 pencil ratio = {r2} "
          f"(expect 3); singleton ratio = {Fraction(8,1)/rho3} (expect 9/2)")

    # EXACT size-3 maximum over all C(135,3) triples
    print("\n   exact size-3 maximum over all C(135,3) = 398,505 triples ...")
    best_T3 = 0
    arg3 = None
    diag = [M3[i][i] for i in range(135)]
    for a in range(135):
        Ma = M3[a]
        for b in range(a + 1, 135):
            Mb = M3[b]
            ab = Ma[b]
            for c in range(b + 1, 135):
                T = 24 + 2 * (ab + Ma[c] + Mb[c])
                if T > best_T3:
                    best_T3, arg3 = T, (a, b, c)
    max3 = Fraction(best_T3, 9)
    ok &= max3 == Fraction(16, 3)
    # is the maximiser a k=2 pencil?
    inter3 = lags3[arg3[0]] & lags3[arg3[1]] & lags3[arg3[2]]
    print(f"   size-3 EXACT max avg = {max3} (= 16/3? "
          f"{'OK' if max3 == Fraction(16,3) else 'FAIL'}), ratio = {max3/rho3};"
          f" maximiser common intersection dim = {(len(inter3)-1).bit_length()}"
          f" (k=2 pencil => 2)")

    # EXACT size-4 maximum over all C(135,4)
    print("   exact size-4 maximum over all C(135,4) = 13,150,665 quadruples ...")
    best_T4 = 0
    arg4 = None
    for a in range(135):
        Ma = M3[a]
        for b in range(a + 1, 135):
            Mb = M3[b]
            sab = Ma[b]
            for c in range(b + 1, 135):
                Mc = M3[c]
                sabc = sab + Ma[c] + Mb[c]
                base = 32 + 2 * sabc
                for d in range(c + 1, 135):
                    T = base + 2 * (Ma[d] + Mb[d] + Mc[d])
                    if T > best_T4:
                        best_T4, arg4 = T, (a, b, c, d)
    max4 = Fraction(best_T4, 16)
    print(f"   size-4 EXACT max avg = {max4}, ratio = {max4/rho3} "
          f"(Kimi search claimed < 3.5 at size >= 4)")
    ok &= max4 / rho3 < 5

    # (3) escalation check
    esc = (max3 / rho3 < 5) and (max4 / rho3 < 5) and (best / rho2 < 5)
    ok &= esc
    print(f"\n(3) escalation: nothing at scale beats 5*rho_avg "
          f"(n=2 exhaustive; n=3 exact at sizes 3,4): "
          f"{'NO ESCALATION' if esc else '*** ESCALATE ***'}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
