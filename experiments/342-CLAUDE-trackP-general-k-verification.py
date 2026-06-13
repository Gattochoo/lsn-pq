#!/usr/bin/env python3
"""
342-CLAUDE-trackP-general-k-verification.py

Adjudication of Kimi Track P (2715452): general-k composition GF + P_k(n) law.

From-scratch (my own general-k character-sum implementation, extending my 263
k=3 code — NOT Kimi's 310):

  (1) P_k(n) = prod_{i=0}^{k-1}(2^{2n-i} - 2^i): direct enumeration of ordered
      pairwise-isotropic independent k-tuples vs the formula (k=2,3 at
      n=2,3,4; k=4 at n=4 by the formula only, 46,267,200).
  (2) Mobius coefficients mu_c = (-1)^c 2^{C(c,2)} over the F_2^k subspace
      lattice: 1,-1 (k=2); 1,-1,2,-8 (k=3); 1,-1,2,-8,128 (k=4).
  (3) my general-k GF closed form (G_L = 2^{-C(k,2)}(T_L^{2n} + sum_{lam!=0}
      S_{lam,L}^n), Mobius-summed) == direct enumeration at k=2,3 (n=2,3,4) —
      reproduces thm:joint-gf and thm:triple-gf.
  (4) k=4 WITHOUT full enumeration: my G_n^{(4)} closed form (n=4); its
      pair-marginal == thm:joint-gf (my 258) and triple-marginal ==
      thm:triple-gf (my 263). This is the marginal-consistency test.
  (5) t_{1^k} law + exact TV to Bin(2n, 2^{-k}) (the CORRECT benchmark; the
      directive's 4^{-k} was wrong, as Kimi flagged) for several (n,k);
      cross-check Kimi's TV table.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import combinations
from math import comb


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def Pk(n, k):
    p = 1
    for i in range(k):
        p *= (2 ** (2 * n - i) - 2 ** i)
    return p


def enum_count(n, k):
    """Count ordered pairwise-isotropic independent k-tuples directly."""
    N = 2 * n
    full = 1 << N
    def rec(chosen, span):
        if len(chosen) == k:
            return 1
        tot = 0
        for c in range(1, full):
            if c in span:
                continue
            if any(omega(c, p, n) for p in chosen):
                continue
            nspan = set(span)
            for s in list(span):
                nspan.add(s ^ c)
            tot += rec(chosen + [c], nspan)
        return tot
    return rec([], {0})


# ---- polynomial dicts over variables x_tau, tau in F_2^k (index 0..2^k-1) ----

def pmul(p1, p2):
    out = {}
    for k1, v1 in p1.items():
        for k2, v2 in p2.items():
            key = tuple(a + b for a, b in zip(k1, k2))
            out[key] = out.get(key, 0) + v1 * v2
    return out


def ppow(p, e, K):
    out = {tuple([0] * K): 1}
    while e:
        if e & 1:
            out = pmul(out, p)
        p = pmul(p, p)
        e >>= 1
    return out


def padd(acc, p, c):
    for key, v in p.items():
        acc[key] = acc.get(key, 0) + c * v
    return acc


def subspaces(k):
    """All subspaces of F_2^k as frozensets of ints, grouped by dim."""
    vecs = list(range(1 << k))
    by_dim = {d: [] for d in range(k + 1)}
    seen = set()
    # generate by all subsets of a basis — brute over spanning sets is fine k<=4
    from itertools import combinations as comb_
    by_dim[0].append(frozenset([0]))
    for d in range(1, k + 1):
        for basis in comb_(range(1, 1 << k), d):
            span = {0}
            ok = True
            for b in basis:
                if b in span:
                    ok = False
                    break
                span |= {x ^ b for x in span}
            if not ok or len(span) != (1 << d):
                continue
            fs = frozenset(span)
            if fs not in seen:
                seen.add(fs)
                by_dim[d].append(fs)
    return by_dim


def var(tau, K):
    key = [0] * (1 << K)
    key[tau] = 1
    return {tuple(key): 1}


def G_L(L, n, k):
    """8x... return 2^{C(k,2)} * G_L (integral)."""
    N = 2 * n
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    TL = {}
    for tau in L:
        padd(TL, var(tau, k), 1)
    acc = ppow(TL, N, k)
    nlam = 1 << len(pairs)
    for lam in range(1, nlam):
        S = {}
        for u in L:
            ub = [(u >> (k - 1 - t)) & 1 for t in range(k)]  # u_1..u_k
            for v in L:
                vb = [(v >> (k - 1 - t)) & 1 for t in range(k)]
                e = 0
                for idx, (i, j) in enumerate(pairs):
                    if (lam >> idx) & 1:
                        e ^= (ub[i] * vb[j] + ub[j] * vb[i]) & 1
                padd(S, pmul(var(u, k), var(v, k)), (-1) ** e)
        padd(acc, ppow(S, n, k), 1)
    return acc  # = 2^{C(k,2)} G_L


def G_general(n, k):
    pw = 1 << comb(k, 2)
    by_dim = subspaces(k)
    total = {}
    for d in range(k + 1):
        c = k - d
        mu = (-1) ** c * 2 ** comb(c, 2)
        for L in by_dim[d]:
            padd(total, G_L(L, n, k), mu)
    out = {}
    for key, v in total.items():
        assert v % pw == 0
        if v:
            out[key] = Fraction(v // pw, Pk(n, k))
    return out


def enum_law(n, k):
    """direct enumeration -> dict{composition tuple: Fraction}."""
    N = 2 * n
    full = 1 << N
    hist = {}
    P = Pk(n, k)
    def rec(chosen, span):
        if len(chosen) == k:
            comp = [0] * (1 << k)
            for i in range(N):
                tau = 0
                for t in range(k):
                    tau = (tau << 1) | ((chosen[t] >> i) & 1)
                comp[tau] += 1
            key = tuple(comp)
            hist[key] = hist.get(key, 0) + 1
            return
        for c in range(1, full):
            if c in span:
                continue
            if any(omega(c, p, n) for p in chosen):
                continue
            nspan = set(span)
            for s in list(span):
                nspan.add(s ^ c)
            rec(chosen + [c], nspan)
    rec([], {0})
    return {key: Fraction(v, P) for key, v in hist.items()}


def main():
    ok = True
    print("=" * 76)
    print("342-CLAUDE  Track P — general-k composition GF: from-scratch check")
    print("=" * 76)

    # (1) P_k count
    print("\n(1) P_k(n) = prod(2^{2n-i}-2^i) vs enumeration:")
    for n, k in ((2, 2), (2, 3), (3, 2), (3, 3), (4, 2)):
        f, e = Pk(n, k), enum_count(n, k)
        ok &= f == e
        print(f"   n={n} k={k}: formula {f} == enum {e} {'OK' if f == e else 'FAIL'}")
    print(f"   P_4(4) = {Pk(4,4)} (formula; first non-degenerate 4-tuple), "
          f"P_3(2)={Pk(2,3)} P_4(3)={Pk(3,4)} (degenerate 0: "
          f"{'OK' if Pk(2,3)==0 and Pk(3,4)==0 else 'FAIL'})")
    ok &= Pk(2, 3) == 0 and Pk(3, 4) == 0

    # (2) Mobius
    print("\n(2) Mobius mu_c = (-1)^c 2^{C(c,2)}:")
    for k in (2, 3, 4):
        mus = [(-1) ** c * 2 ** comb(c, 2) for c in range(k + 1)]
        print(f"   k={k}: {mus}")
    ok &= [(-1) ** c * 2 ** comb(c, 2) for c in range(4)] == [1, -1, 2, -8]

    # (3) general-k GF == enumeration for k=2,3
    print("\n(3) my general-k GF == direct enumeration (reproduces joint/triple):")
    for n, k in ((2, 2), (3, 2), (4, 2), (3, 3), (4, 3)):
        gf = G_general(n, k)
        en = enum_law(n, k)
        m = gf == en
        ok &= m
        print(f"   n={n} k={k}: {len(en)} monomials, GF==enum {'OK' if m else 'FAIL'}")

    # (4) k=4 marginal consistency at n=4 (no full enumeration)
    print("\n(4) k=4 at n=4 — marginal consistency (no 256^4 enumeration):")
    G4 = G_general(4, 4)
    # pair-marginal onto coords (c1,c2): sum over c3,c4 categories
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "g258", "experiments/258-CLAUDE-trackI-joint-gf-verification.py")
    g258 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g258)
    spec3 = importlib.util.spec_from_file_location(
        "g263", "experiments/263-CLAUDE-trackM-triple-gf-verification.py")
    g263 = importlib.util.module_from_spec(spec3); spec3.loader.exec_module(g263)

    pair = {}
    trip = {}
    for comp, v in G4.items():
        t2 = [0, 0, 0, 0]   # (c1,c2): t11,t10,t01,t00
        t3 = [0] * 8        # (c1,c2,c3)
        for tau in range(16):
            b1, b2, b3 = (tau >> 3) & 1, (tau >> 2) & 1, (tau >> 1) & 1
            idx2 = {(1, 1): 0, (1, 0): 1, (0, 1): 2, (0, 0): 3}[(b1, b2)]
            t2[idx2] += comp[tau]
            t3[(b1 << 2) | (b2 << 1) | b3] += comp[tau]
        pair[tuple(t2)] = pair.get(tuple(t2), Fraction(0)) + v
        trip[tuple(t3)] = trip.get(tuple(t3), Fraction(0)) + v
    pm_ok = pair == g258.G_enum(4)
    tm_ok = trip == g263.closed_form(4)
    ok &= pm_ok and tm_ok
    print(f"   pair-marginal of G^(4) == thm:joint-gf (n=4): {'OK' if pm_ok else 'FAIL'}")
    print(f"   triple-marginal of G^(4) == thm:triple-gf (n=4): {'OK' if tm_ok else 'FAIL'}")

    # (5) t_{1^k} law + TV to Bin(2n, 2^{-k})  (correct benchmark)
    print("\n(5) t_{1^k} TV to Bin(2n, 2^{-k}) (correct; directive's 4^{-k} wrong):")
    kimi_tv = {(2, 2): "707/5760", (3, 2): "35183/645120", (3, 3): "1096511/27525120",
               (4, 2): "14891599/526417920", (4, 3): "216403141/12478054400"}
    for n, k in ((2, 2), (3, 2), (3, 3), (4, 2), (4, 3)):
        gf = G_general(n, k)
        N = 2 * n
        allone = (1 << k) - 1   # tau = 1^k index
        law = [Fraction(0)] * (N + 1)
        for comp, v in gf.items():
            law[comp[allone]] += v
        pq = Fraction(1, 2 ** k)
        ref = [comb(N, l) * pq ** l * (1 - pq) ** (N - l) for l in range(N + 1)]
        tv = sum(abs(a - b) for a, b in zip(law, ref)) / 2
        m = (n, k) not in kimi_tv or tv == Fraction(kimi_tv[(n, k)])
        ok &= m
        print(f"   n={n} k={k}: TV = {tv} = {float(tv):.6f}  "
              f"{'OK (matches Kimi)' if (n,k) in kimi_tv and m else ''}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — Track P THEOREM ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
