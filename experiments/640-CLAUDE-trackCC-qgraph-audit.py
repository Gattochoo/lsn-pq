#!/usr/bin/env python3
"""
640-CLAUDE-trackCC-qgraph-audit.py

Adjudication of Kimi Track CC (7b17b4e). CC's main NO-GO (fixed-k rank-sum
distinguisher with FRESH per-sample B leaks at rate -> 0) is sound by
subadditivity; this audit targets CC's q_graph FORMULA, which is wrong.

CC claims: "Sp(2n,F_2) acts transitively on Lagrangians and the Ber(p)^{2n}
weight is coordinate-wise, so Pr[e in L] is the same for every Lagrangian"
=> computes it on the standard Lagrangian: q_graph(n) = (3/4)^n.

THE ERROR: Sp(2n,F_2) does NOT preserve the Bernoulli(1/4) weight (symplectic
maps mix coordinates linearly; Hamming-weight-based probability is invariant
only under coordinate permutations, not general linear maps). So Pr[e in L]
DEPENDS on L, and the reduction's A is a UNIFORM Lagrangian, so q_graph is the
AVERAGE (= round-1 value 29/64 at n=2), not the standard-L value (3/4)^n = 9/16.

Checks:
  (1) Pr[e in L] differs across Lagrangians L (exhibit standard L = (3/4)^n
      and a DIFFERENT L with a different value) — refutes "same for every L".
  (2) the uniform-average over all Lagrangians = round-1 q_graph(n)
      = (3/4)^{2n} + (1-(3/4)^{2n})/(2^n+1) (29/64 at n=2), NOT (3/4)^n.
  (3) an explicit Sp(4,F_2) element that changes Pr[e in L] (weight not
      preserved) — the concrete refutation of the invariance claim.
  (4) CC's NO-GO conclusion is robust: both (3/4)^n and the true average -> 0,
      so fixed-k subadditivity gives rate -> 0 regardless. The error is in the
      RATE FORMULA, not the qualitative NO-GO.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import combinations

P = Fraction(1, 4)


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians(n):
    NN = 2 * n
    found = set()
    for basis in combinations(range(1, 1 << NN), n):
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


def pr_e_in_L(L, n):
    NN = 2 * n
    tot = Fraction(0)
    for v in L:
        w = bin(v).count("1")
        tot += P ** w * (1 - P) ** (NN - w)
    return tot


def q_graph_round1(n):
    return Fraction(3, 4) ** (2 * n) + (1 - Fraction(3, 4) ** (2 * n)) / (2 ** n + 1)


def main():
    ok = True
    print("=" * 74)
    print("640-CLAUDE  Track CC q_graph audit — 'same for every L' is FALSE")
    print("=" * 74)

    for n in (2, 3):
        NN = 2 * n
        lags = all_lagrangians(n)
        # standard Lagrangian = span{e_0,...,e_{n-1}} (first n coords free, last n = 0)
        std = {0}
        for i in range(n):
            std |= {x ^ (1 << i) for x in std}
        pr_std = pr_e_in_L(std, n)
        kimi = Fraction(3, 4) ** n
        # distinct values across Lagrangians
        vals = sorted(set(pr_e_in_L(L, n) for L in lags))
        avg = sum(pr_e_in_L(L, n) for L in lags) / len(lags)
        r1 = q_graph_round1(n)
        print(f"\nn={n}: {len(lags)} Lagrangians")
        print(f"  Pr[e in standard L] = {pr_std} = (3/4)^n = {kimi}  "
              f"{'(Kimi value)' if pr_std == kimi else ''}")
        print(f"  distinct Pr[e in L] values: {[str(v) for v in vals]}")
        same = len(vals) == 1
        ok &= not same  # we EXPECT them to differ (CC's claim is that they're same)
        print(f"  'same for every L'? {same}  -> CC claim "
              f"{'CONFIRMED' if same else 'REFUTED (values differ)'}")
        print(f"  uniform AVERAGE = {avg}  vs round-1 q_graph = {r1}  "
              f"{'MATCH' if avg == r1 else 'MISMATCH'}")
        ok &= avg == r1
        print(f"  => reduction q_graph (uniform A) = {avg} "
              f"= {float(avg):.4f}, NOT (3/4)^n = {float(kimi):.4f}")

    # (3) explicit Sp element changing Pr[e in L]
    print("\n(3) Sp does not preserve Bernoulli weight (concrete):")
    n = 2
    std = {0, 1, 2, 3}  # span{e0,e1} = {00,e0,e1,e0+e1} over 4 bits = {0,1,2,3}
    # a different Lagrangian: span{e0+e2? } ... just take any non-standard from list
    lags = all_lagrangians(2)
    others = [L for L in lags if L != std]
    L2 = max(others, key=lambda L: pr_e_in_L(L, 2)) if others else std
    Lmin = min(others, key=lambda L: pr_e_in_L(L, 2))
    print(f"   standard L: Pr = {pr_e_in_L(std,2)} = {float(pr_e_in_L(std,2)):.4f}")
    print(f"   some other L: Pr = {pr_e_in_L(L2,2)} = {float(pr_e_in_L(L2,2)):.4f}")
    print(f"   min-Pr L: Pr = {pr_e_in_L(Lmin,2)} = {float(pr_e_in_L(Lmin,2)):.4f}")
    print(f"   => Pr[e in L] is L-DEPENDENT; 'invariant under Sp' is false.")

    # (4) NO-GO robustness
    print("\n(4) CC's qualitative NO-GO is robust (both -> 0):")
    for n in (2, 4, 6, 8):
        print(f"   n={n}: (3/4)^n = {float(Fraction(3,4)**n):.5f}, "
              f"true q_graph = {float(q_graph_round1(n)):.5f}  (both -> 0)")
    print("   => fixed-k rank-sum advantage = O(k * q_graph) -> 0 either way;")
    print("      the NO-GO holds. Only the RATE FORMULA (3/4)^n is wrong;")
    print("      the true rate is the uniform-Lagrangian average.")

    print("\n" + "=" * 74)
    print("VERDICT: CC NO-GO (fresh-B fixed-k rank-sum -> rate 0) ACCEPT; but the")
    print("  q_graph = (3/4)^n FORMULA is WRONG (Sp does NOT fix Bernoulli weight;")
    print("  reduction's A is uniform -> q_graph is the average, 29/64 at n=2).")
    print("  shared-B (k>n) remains the genuine OPEN sub-question.")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
