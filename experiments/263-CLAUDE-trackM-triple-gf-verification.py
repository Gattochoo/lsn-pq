#!/usr/bin/env python3
"""
263-CLAUDE-trackM-triple-gf-verification.py

Adjudication of Kimi Track M (5732176): 8-variable triple-composition GF.

From-scratch rails (my own code; the closed form re-implemented from the
formula text in the meta note, not from Kimi's script):

  (1) direct enumeration of ordered pairwise-isotropic, linearly independent
      triples (c1,c2,c3) at n=3 (expect 22,680) and n=4 (expect 1,927,800 —
      the THIRD FACTOR IS 60, not the directive's erroneous 56; verify
      P3 = (4^n-1)(4^n/2-2)(4^n/4-4) matches the count) -> exact 8-category
      composition law.
  (2) my own implementation of the Mobius/character closed form
      (coefficients +1, -1 per hyperplane, +2 per line, -8 at {0} — re-derived
      as mu_c = (-1)^c 2^{c(c-1)/2}); coefficient-dict equality with (1).
  (3) pair-marginals == thm:joint-gf (my 258 G_closed, independent rail).
  (4) corollary spot checks: t111 law and agreement count a = t000 + t111
      from the GF == direct enumeration (n=3).
  (5) n=2 degeneracy: P3(2) = 0 (no isotropic 3-space in F_2^4).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import product

# ------------------------------------------------------------ basics

def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def P3(n):
    X = 4 ** n
    return (X - 1) * (X // 2 - 2) * (X // 4 - 4)


def enum_triples(n):
    """Direct enumeration -> dict{8-tuple composition: count}."""
    N = 2 * n
    full = 1 << N
    # pre-filter pairs c1,c2 (isotropic, independent)
    hist = {}
    cnt = 0
    for c1 in range(1, full):
        # c2 in c1-perp, not in {0, c1}
        for c2 in range(1, full):
            if c2 == c1 or omega(c1, c2, n):
                continue
            span = {0, c1, c2, c1 ^ c2}
            for c3 in range(1, full):
                if c3 in span or omega(c1, c3, n) or omega(c2, c3, n):
                    continue
                key = [0] * 8
                for i in range(N):
                    tau = (((c1 >> i) & 1) << 2) | (((c2 >> i) & 1) << 1) | \
                        ((c3 >> i) & 1)
                    key[tau] += 1
                hist[tuple(key)] = hist.get(tuple(key), 0) + 1
                cnt += 1
    return hist, cnt


# ------------------------------------- my closed-form implementation
# variables indexed by tau in F_2^3 encoded as integer 0..7 (bit2=c1,bit1=c2,bit0=c3)
# polynomial dicts: key = 8-tuple exponent vector, value = int coefficient

def pmul(p1, p2):
    out = {}
    for k1, v1 in p1.items():
        for k2, v2 in p2.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            out[k] = out.get(k, 0) + v1 * v2
    return out


def ppow(p, e):
    out = {tuple([0] * 8): 1}
    while e:
        if e & 1:
            out = pmul(out, p)
        p = pmul(p, p)
        e >>= 1
    return out


def padd(acc, p, c):
    for k, v in p.items():
        acc[k] = acc.get(k, 0) + c * v
    return acc


def subspaces_f23():
    """All subspaces of F_2^3 grouped by dim."""
    vecs = list(range(1, 8))
    subs = {0: [frozenset([0])], 1: [], 2: [], 3: [frozenset(range(8))]}
    seen1, seen2 = set(), set()
    for v in vecs:
        s = frozenset([0, v])
        if s not in seen1:
            seen1.add(s)
            subs[1].append(s)
    for a in vecs:
        for b in vecs:
            if b <= a:
                continue
            s = frozenset([0, a, b, a ^ b])
            if s not in seen2:
                seen2.add(s)
                subs[2].append(s)
    return subs


def var(tau):
    k = [0] * 8
    k[tau] = 1
    return {tuple(k): 1}


def G_L(L, n):
    """(1/8)(T_L^{2n} + sum_{lambda != 0} S_{lambda,L}^n) — integer-8x version
    (return 8*G_L to stay integral)."""
    N = 2 * n
    TL = {}
    for tau in L:
        padd(TL, var(tau), 1)
    acc = ppow(TL, N)
    for lam in range(1, 8):
        l12, l13, l23 = (lam >> 2) & 1, (lam >> 1) & 1, lam & 1
        S = {}
        for u in L:
            u1, u2, u3 = (u >> 2) & 1, (u >> 1) & 1, u & 1
            for v in L:
                v1, v2, v3 = (v >> 2) & 1, (v >> 1) & 1, v & 1
                sgn = (-1) ** (l12 * (u1 * v2 + u2 * v1)
                               + l13 * (u1 * v3 + u3 * v1)
                               + l23 * (u2 * v3 + u3 * v2))
                padd(S, pmul(var(u), var(v)), sgn)
        acc_S = ppow(S, n)
        padd(acc, acc_S, 1)
    return acc  # = 8 * G_L (counts, before 1/8)


def closed_form(n):
    """My implementation of the Mobius-summed closed form -> count dict."""
    subs = subspaces_f23()
    total = {}
    padd(total, G_L(frozenset(range(8)), n), 1)      # +1 full
    for H in subs[2]:
        padd(total, G_L(H, n), -1)                   # -1 hyperplanes
    for l in subs[1]:
        padd(total, G_L(l, n), 2)                    # +2 lines
    padd(total, G_L(subs[0][0], n), -8)              # -8 zero
    # divide by 8 (the character normalization)
    out = {}
    for k, v in total.items():
        assert v % 8 == 0, (k, v)
        if v:
            out[k] = v // 8
    return out


def main():
    ok = True
    print("=" * 76)
    print("263-CLAUDE  Track M — triple GF: from-scratch verification")
    print("=" * 76)

    # Mobius coefficients re-derivation
    mu = [(-1) ** c * 2 ** (c * (c - 1) // 2) for c in range(4)]
    ok &= mu == [1, -1, 2, -8]
    print(f"\n  Mobius mu by corank: {mu} (expect [1,-1,2,-8]) "
          f"{'OK' if mu == [1, -1, 2, -8] else 'FAIL'}")
    print(f"  P3(2) = {P3(2)} (degenerate, expect 0) "
          f"{'OK' if P3(2) == 0 else 'FAIL'}")
    ok &= P3(2) == 0

    for n in (3, 4):
        hist, cnt = enum_triples(n)
        p3 = P3(n)
        c_ok = cnt == p3
        ok &= c_ok
        print(f"\n  n={n}: enumerated {cnt} triples; P3 = {p3} "
              f"{'OK' if c_ok else 'FAIL'} "
              f"({'corrected 60-factor' if n == 4 else ''})")
        cf = closed_form(n)
        m_ok = cf == hist
        ok &= m_ok
        print(f"        closed form == enumeration ({len(hist)} monomials): "
              f"{'OK' if m_ok else 'FAIL'}")

        if n == 3:
            # (3) pair marginal (c1,c2) vs thm:joint-gf coefficients (258 rail)
            pair = {}
            for k, v in hist.items():
                t = [0, 0, 0, 0]  # (t11,t10,t01,t00) for (c1,c2)
                for tau in range(8):
                    a, b = (tau >> 2) & 1, (tau >> 1) & 1
                    idx = {(1, 1): 0, (1, 0): 1, (0, 1): 2, (0, 0): 3}[(a, b)]
                    t[idx] += k[tau]
                key = tuple(t)
                pair[key] = pair.get(key, 0) + v
            # direct pair law times the c3-count per pair: each isotropic pair
            # extends to exactly (4^n/4 - 4) triples
            ext = 4 ** n // 4 - 4
            P2 = (4 ** n - 1) * (4 ** n // 2 - 2)
            # compare normalized pair law with my 258 G_enum
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "g258", "experiments/258-CLAUDE-trackI-joint-gf-verification.py")
            g258 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(g258)
            ge = g258.G_enum(n)
            mine = {k: Fraction(v, P2 * ext) for k, v in pair.items()}
            pm_ok = mine == ge
            ok &= pm_ok
            print(f"        (c1,c2) pair-marginal == thm:joint-gf law: "
                  f"{'OK' if pm_ok else 'FAIL'}")
            # (4) t111 and agreement count laws from hist
            t111 = {}
            agree = {}
            for k, v in hist.items():
                t111[k[7]] = t111.get(k[7], 0) + v  # tau=111 -> index 7
                a = k[0] + k[7]                     # t000 + t111
                agree[a] = agree.get(a, 0) + v
            print(f"        t111 law: {dict(sorted(t111.items()))}")
            print(f"        agreement law (t000+t111): "
                  f"{dict(sorted(agree.items()))}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — Track M THEOREM ACCEPT" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
