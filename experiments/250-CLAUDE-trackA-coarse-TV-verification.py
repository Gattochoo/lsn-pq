#!/usr/bin/env python3
"""
250-CLAUDE-trackA-coarse-TV-verification.py

Independent adjudication of Kimi's Track-A deliverable
(meta/2026-06-14-KIMI-lem-m2-matched-rate-sampling.md, experiments/196-KIMI-*).

Kimi's pipeline rests on an ANALYTIC closed form for the TV over the coarse
(rank(C), 1{y in col(C)}) partition (the MC only validates the sampler).
By the data-processing inequality this analytic value is a RIGOROUS lower
bound on the true matched-rate SD. This script re-derives everything from
scratch:

  (1) q(n), p_eff(n) closed forms vs the exact 191 JSON values (n=2,3).
  (2) BRUTE FORCE at (n=2, m=2): enumerate ALL 15 Lagrangians x all v in L
      x all e x all B (2^8) exactly -> joint (rank, member) law of the
      reduction; enumerate all C', x' with exact Bernoulli(p_eff) weights ->
      joint law of matched LPN. Compare BOTH to the claimed conditional
      formulas P_out(s=1|r) = q + (1-q) 2^{r-m} and
      P_lpn(s=1|r) = ((2^m - 2^r)(1-p)^m + (2^r - 1)) / (2^m - 1).
  (3) Exact coarse TV along m=2n for n=2..8 (Fractions; Gaussian-binomial
      rank law). Check Kimi's 0.1395 (n=4), 0.0816 (n=5); compare to the
      exact full SD at (2,4), (3,6) from 191 (the "within ~2%" claim).
  (4) Decay: TV(n+1)/TV(n) -> 9/16 (the graph-mixing rate q(n) ~ (3/4)^{2n});
      saturation: TV_coarse(n, m -> infty) -> q(n) (the functional caps at q).
  (5) PRE-REGISTER (iii) quantification: along m=2n the output rate
      p_eff -> 1/2 and m_useful(n) = 4n/(1-2 p_eff)^2 = 4n (16/9)^{2n} >> 2n
      (vacuous-output diagonal), printed explicitly.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import json
from fractions import Fraction
from math import comb
from itertools import combinations

# ---------------------------------------------------------------- basics

def p_eff(n):
    return (1 - Fraction(3, 4) ** (2 * n)) / 2


def q_graph(n):
    t = Fraction(3, 4) ** (2 * n)
    return t + (1 - t) / (2 ** n + 1)


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians(n):
    """All n-dim totally isotropic subspaces of F_2^{2n} (as frozensets)."""
    N = 2 * n
    vecs = list(range(1, 1 << N))
    subs = set()
    for basis in combinations(vecs, n):
        # span + independence
        span = {0}
        for b in basis:
            span |= {x ^ b for x in span}
        if len(span) != 2 ** n:
            continue
        if any(omega(u, v, n) for u in span for v in span):
            continue
        subs.add(frozenset(span))
    return [sorted(s) for s in subs]


# ------------------------------------------------- (rank, member) helpers

def rank_and_image(rows, m):
    """rank of the F_2 row-set and its span (set of ints)."""
    span = {0}
    rank = 0
    basis = []
    for r in rows:
        x = r
        for b in basis:
            x = min(x, x ^ b)  # not proper reduction; do textbook instead
    # textbook Gaussian elimination
    basis = []
    for r in rows:
        x = r
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    rank = len(basis)
    span = {0}
    for b in basis:
        span |= {v ^ b for v in span}
    return rank, span


def main():
    ok = True
    print("=" * 76)
    print("250-CLAUDE  Track A — coarse (rank,member) TV: from-scratch adjudication")
    print("=" * 76)

    # (1) q, p_eff vs exact 191 JSONs
    print("\n(1) closed forms vs exact 191 data:")
    for n, m in ((2, 4), (3, 6)):
        d = json.load(open(
            f"experiments/output/191-lem-m2-uniform-B-matched-rate-m2n-n{n}-m{m}.json"))
        pe_ok = Fraction(d["p_eff"]) == p_eff(n)
        q_ok = Fraction(d["q_graph"]) == q_graph(n)
        ok &= pe_ok and q_ok
        print(f"   n={n}: p_eff {'OK' if pe_ok else 'FAIL'} ({d['p_eff']}), "
              f"q_graph {'OK' if q_ok else 'FAIL'} ({d['q_graph']})")

    # (2) brute force at (n=2, m=2)
    print("\n(2) brute force (n=2, m=2): all 15 Lagrangians x v x e x B:")
    n, m = 2, 2
    N = 2 * n
    lags = all_lagrangians(n)
    assert len(lags) == 15, len(lags)
    # reduction side: exact joint over (r,s); weights: L uniform, v=Ax uniform
    # over L, e Bernoulli(1/4)^{2n} (weight (1/3... use Fraction (1/4,3/4)), B uniform.
    out = {}
    wB = Fraction(1, 2 ** (m * N))
    for L in lags:
        Lset = set(L)
        wL = Fraction(1, 15)
        for v0 in L:  # = Ax, uniform over L
            wv = Fraction(1, 2 ** n)
            for e in range(1 << N):
                we = (Fraction(1, 4) ** bin(e).count("1")
                      * Fraction(3, 4) ** (N - bin(e).count("1")))
                v = v0 ^ e
                in_L = v in Lset
                for Bbits in range(1 << (m * N)):
                    rows = [(Bbits >> (i * N)) & ((1 << N) - 1) for i in range(m)]
                    # C rows = action of B-rows on a basis of L: rank(C) =
                    # rank of B restricted to L = rank of {row . l}_l in L...
                    # basis-free: image of L under y(w)=bits (row_i . w)_i
                    imgL = set()
                    for w in Lset:
                        y = 0
                        for i, r in enumerate(rows):
                            y |= (bin(r & w).count("1") & 1) << i
                        imgL.add(y)
                    rank = (len(imgL) - 1).bit_length()  # |img|=2^rank
                    yv = 0
                    for i, r in enumerate(rows):
                        yv |= (bin(r & v).count("1") & 1) << i
                    s = 1 if yv in imgL else 0
                    out[(rank, s)] = out.get((rank, s), 0) + wL * wv * we * wB
    # LPN side: C' uniform m x n, x' uniform, e' Bernoulli(p_eff)
    pe = p_eff(n)
    lpn = {}
    wC = Fraction(1, 2 ** (m * n))
    wx = Fraction(1, 2 ** n)
    for Cbits in range(1 << (m * n)):
        crows = [(Cbits >> (i * n)) & ((1 << n) - 1) for i in range(m)]
        rank, span = rank_and_image(crows, m)
        # y' = C'x' + e' ; s = 1{y' in col(C')} = 1{e' in col-span (as row map)}
        # column space of C' = image of x -> C'x = span of columns; rows here are
        # rows of C', so compute image over x:
        img = set()
        for x in range(1 << n):
            y = 0
            for i, r in enumerate(crows):
                y |= (bin(r & x).count("1") & 1) << i
            img.add(y)
        rank = (len(img) - 1).bit_length()
        for e in range(1 << m):
            we = pe ** bin(e).count("1") * (1 - pe) ** (m - bin(e).count("1"))
            s = 1 if e in img else 0  # y' in img <=> e' in img (img is a subspace)
            lpn[(rank, s)] = lpn.get((rank, s), 0) + wC * we
    # compare to claimed conditionals
    q = q_graph(n)
    rank_marg_out = {}
    rank_marg_lpn = {}
    for (r, s), w in out.items():
        rank_marg_out[r] = rank_marg_out.get(r, 0) + w
    for (r, s), w in lpn.items():
        rank_marg_lpn[r] = rank_marg_lpn.get(r, 0) + w
    all_match = True
    for r in sorted(rank_marg_out):
        po = out.get((r, 1), Fraction(0)) / rank_marg_out[r]
        po_claim = q + (1 - q) * Fraction(2 ** r, 2 ** m)
        pl = lpn.get((r, 1), Fraction(0)) / rank_marg_lpn[r]
        pl_claim = Fraction((2 ** m - 2 ** r) * 1, 1)  # build below
        pl_claim = ((2 ** m - 2 ** r) * (1 - pe) ** m + (2 ** r - 1)) / (2 ** m - 1)
        mo, ml = po == po_claim, pl == pl_claim
        rm = rank_marg_out[r] == rank_marg_lpn[r]
        all_match &= mo and ml and rm
        print(f"   r={r}: P_out(s=1|r) {'OK' if mo else 'FAIL'}  "
              f"P_lpn(s=1|r) {'OK' if ml else 'FAIL'}  rank-marginals equal "
              f"{'OK' if rm else 'FAIL'}")
    ok &= all_match
    print(f"   => both conditional formulas EXACT at (2,2): "
          f"{'CONFIRMED' if all_match else 'REFUTED'}")

    # (3) exact coarse TV along m=2n
    print("\n(3) exact coarse TV along m=2n (Fractions):")

    def rank_dist(m_, n_):
        tot = Fraction(2) ** (m_ * n_)
        dist = {}
        for r in range(0, min(m_, n_) + 1):
            cnt = 1
            for i in range(r):
                cnt *= (2 ** n_ - 2 ** i)
            gb = 1  # number of rank-r m x n matrices:
            # count = gauss_binom(m,r) * prod_{i<r}(2^n - 2^i)
            num, den = 1, 1
            for i in range(r):
                num *= (2 ** m_ - 2 ** i)
                den *= (2 ** r - 2 ** i)
            dist[r] = Fraction(num // den * cnt, 1) / tot
        assert sum(dist.values()) == 1
        return dist

    def coarse_tv(n_, m_):
        q_ = q_graph(n_)
        pe_ = p_eff(n_)
        rd = rank_dist(m_, n_)
        tv = Fraction(0)
        for r, w in rd.items():
            po = q_ + (1 - q_) * Fraction(2 ** r, 2 ** m_)
            pl = ((2 ** m_ - 2 ** r) * (1 - pe_) ** m_ + (2 ** r - 1)) / (2 ** m_ - 1)
            tv += w * abs(po - pl)
        return tv

    full_sd = {(2, 4): Fraction("277825754675/1099511627776"),
               (3, 6): Fraction("274605773661408696847360184835/"
                                 "1267650600228229401496703205376")}
    kimi = {(4, 8): 0.1395, (5, 10): 0.0816}
    prev = None
    for n_ in range(2, 9):
        m_ = 2 * n_
        tv = coarse_tv(n_, m_)
        line = f"   n={n_:>2} m={m_:>2}: coarse TV = {float(tv):.6f}"
        if (n_, m_) in full_sd:
            ratio = tv / full_sd[(n_, m_)]
            line += f"   /full SD = {float(ratio):.4f}"
        if (n_, m_) in kimi:
            agree = abs(float(tv) - kimi[(n_, m_)]) < 5e-5
            ok &= agree
            line += f"   vs Kimi {kimi[(n_, m_)]}: {'OK' if agree else 'FAIL'}"
        if prev is not None:
            line += f"   decay {float(tv / prev):.4f}"
        prev = tv
        print(line)
    print(f"   (9/16 = {9/16:.4f} — the predicted asymptotic decay, "
          f"q(n) ~ (3/4)^{{2n}})")

    # (4) saturation: coarse TV caps at q(n) as m grows
    print("\n(4) saturation of the rank-member functional (m -> large):")
    for n_ in (4, 5):
        tv64 = coarse_tv(n_, 64)
        print(f"   n={n_}: coarse TV at m=64 = {float(tv64):.6f}  vs  "
              f"q(n) = {float(q_graph(n_)):.6f}  (cap)")

    # (5) PRE-REGISTER (iii): the m=2n diagonal is vacuous-output
    print("\n(5) PRE-REGISTER (iii) — usable-vs-vacuous along m=2n:")
    for n_ in (2, 3, 4, 5, 8):
        gap = float(1 - 2 * p_eff(n_))
        m_useful = 4 * n_ / gap ** 2
        print(f"   n={n_}: 1-2p_eff = (3/4)^{{2n}} = {gap:.5f}; "
              f"m_useful ~ 4n/(1-2p)^2 = {m_useful:,.0f}  vs  m=2n = {2*n_}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
