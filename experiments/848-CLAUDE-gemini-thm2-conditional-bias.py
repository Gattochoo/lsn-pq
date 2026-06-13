#!/usr/bin/env python3
"""
848-CLAUDE-gemini-thm2-conditional-bias.py

Tests Gemini's (agy) round-9 "Theorem 2 (Weight-1 Quotient Collapse)", which
claims I(x;y|C) >= ~0.38n is a HARD FLOOR (refuting lem:m2). Its mechanism:
since row(C_L B) (+) row(HB) = F_2^{2n} for full-rank B, every weight-1 e_i
decomposes e_i = w_u + w_s (w_u in row(C_L B), w_s in row(HB)). Then the message
form <w_u, e> = e_i + <w_s, e>, and <w_s,e> is fixed by the syndrome s = HBe.
Gemini CLAIMS: conditioned on s, <w_u,e> = e_i + const "carries bias 1-2p", so the
n message forms stay biased -> u biased -> Omega(n) leak.

THE GAP (Claude): e_i is itself entangled in s = HBe. The claimed bias 1-2p is the
UNCONDITIONAL bias of e_i; the operative quantity is the bias of e_i GIVEN s. If
conditioning on the n-dim syndrome smooths e_i (bias -> 0), the floor collapses and
I = o(n) survives. This script computes the ACTUAL conditional bias / conditional
entropy H(<w_u,e> | s) exactly (16 noise vectors, Bernoulli(1/4) weighted) and
averages over sampled (A, uniform-B) at n=2, m=4,5,6,7.

Decision rule:
  - Gemini's Theorem 2 (stays biased): avg H(form | s) ~ H_2(1/4) = 0.811 bits, and
    avg |bias| ~ stays away from 0 as m grows.
  - lem:m2 (smoothing): avg H(form | s) -> 1 bit (uniform), avg |bias| -> 0 as m grows.

Cross-anchor: also report I(x;y|C)'s trend (GG: converges ~0.33 at n=2, i.e. 0.16n,
NOT Gemini's 0.38n=0.76) as independent corroboration.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from itertools import combinations
from math import log2

NN = 4   # 2n at n=2
n = 2
P = 0.25


def omega(a, b):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def lagrangians():
    out = set()
    for bb in combinations(range(1, 1 << NN), 2):
        span = {0}
        for x in bb:
            span |= {y ^ x for y in span}
        if len(span) != 4:
            continue
        if any(omega(u, v) for u in span for v in span):
            continue
        out.add(frozenset(span))
    return [sorted(s) for s in out]


def dot(a, b):
    return bin(a & b).count("1") & 1


def rowspace(vecs):
    """basis (list of ints over F_2^NN) of the span of given vectors."""
    basis = []
    for v in vecs:
        x = v
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return basis


def in_span(v, basis):
    x = v
    for b in basis:
        x = min(x, x ^ b)
    return x == 0


def reduce_vec(v, basis):
    x = v
    for b in basis:
        x = min(x, x ^ b)
    return x


def main():
    rng = random.Random(11)
    LAGS = lagrangians()
    print("=" * 74)
    print("848-CLAUDE  Gemini Theorem-2 test: conditional bias of message forms")
    print("=" * 74)
    print(f"  n={n}, p={P}. Unconditional |bias| of e_i = 1-2p = {1-2*P}.")
    print(f"  H_2(1/4) = {-(P*log2(P)+(1-P)*log2(1-P)):.4f} bits (biased); 1.0 = uniform.")
    print(f"  {'m':>2} {'avg H(form|s)':>14} {'avg |bias|form':>15} {'#samples':>9}   trend")
    Hp = -(P*log2(P)+(1-P)*log2(1-P))
    prev = None
    for m in (4, 5, 6, 7):
        Hsum = 0.0
        biassum = 0.0
        cnt = 0
        for _ in range(4000):
            L = rng.choice(LAGS)
            nz = [v for v in L if v]
            a0, a1 = rng.sample(nz, 2)
            rows = [rng.randrange(1 << NN) for _ in range(m)]
            # B columns over F_2^m (col j = bit j of each row)
            # We need: HB rows (in F_2^{2n}=F_2^4) and a message form w_u.
            # H = left-null-space of C: vectors h in F_2^m with sum_i h_i * Crow_i = 0,
            # where Crow_i = (<row_i,a0>, <row_i,a1>) in F_2^2.
            Crow = [(dot(r, a0) | (dot(r, a1) << 1)) for r in rows]  # 2-bit per row
            # H basis: h in F_2^m with sum_i h_i * Crow_i (as F_2^2 vectors) = 0
            # i.e. the two columns (bit0 of Crow, bit1 of Crow) dotted with h = 0.
            col0 = 0
            col1 = 0
            for i, cr in enumerate(Crow):
                if cr & 1:
                    col0 |= 1 << i
                if cr & 2:
                    col1 |= 1 << i
            # H = {h : dot(h,col0)=0 and dot(h,col1)=0}
            Hbasis = []
            for h in range(1 << m):
                if dot(h, col0) == 0 and dot(h, col1) == 0:
                    x = h
                    for b in Hbasis:
                        x = min(x, x ^ b)
                    if x:
                        Hbasis.append(x)
                        Hbasis.sort(reverse=True)
            # HB rows in F_2^{2n}: for each h in Hbasis, the F_2^4 vector
            #   (HBe = sum_i h_i (row_i . e))  => the vector w with w_k = sum_i h_i (row_i)_k
            HBrows = []
            for h in Hbasis:
                w = 0
                for k in range(NN):
                    bit = 0
                    for i, r in enumerate(rows):
                        if (h >> i) & 1:
                            bit ^= (r >> k) & 1
                    if bit:
                        w |= 1 << k
                HBrows.append(w)
            HBspan = rowspace(HBrows)
            if len(HBspan) != n:   # need rank(HB)=n (full-rank-B typical)
                continue
            # message space row(C_L B): complement of HBspan in F_2^4 within row(B).
            # row(B) = span of B's rows-as-F_2^4 vectors = span(rows). For full-rank B
            # over F_2^4 that's all of F_2^4. message space = any complement of HBspan.
            Bspan = rowspace(rows)
            if len(Bspan) != NN:
                continue
            # find a weight-1 e_i not in HBspan; w_u = e_i reduced mod HBspan is the
            # message-form representative (w_u ≡ e_i mod row(HB)); the form is <w_u,e>
            # but to get "e_i + <w_s,e>" we use the form phi(e) = <e_i, e> = e_i-th bit,
            # whose value given s is what Gemini predicts stays biased.
            ei = None
            for k in range(NN):
                if not in_span(1 << k, HBspan):
                    ei = 1 << k
                    break
            if ei is None:
                continue
            # joint (form, s) over e in F_2^4 with Bernoulli(1/4) weights;
            # form = <ei,e> (= the message bit Gemini claims stays biased),
            # s = (HBe) coordinates = (<HBrow, e> for HBrow in HBspan basis)
            from collections import defaultdict
            joint = defaultdict(float)
            for e in range(1 << NN):
                w = P ** bin(e).count("1") * (1 - P) ** (NN - bin(e).count("1"))
                f = dot(ei, e)
                s = 0
                for j, hr in enumerate(HBspan):
                    if dot(hr, e):
                        s |= 1 << j
                joint[(f, s)] += w
            # H(form | s) and conditional bias
            Ps = defaultdict(float)
            for (f, s), w in joint.items():
                Ps[s] += w
            Hcond = 0.0
            biasc = 0.0
            for s, ps in Ps.items():
                p0 = joint.get((0, s), 0.0) / ps
                p1 = joint.get((1, s), 0.0) / ps
                h = 0.0
                for pp in (p0, p1):
                    if pp > 0:
                        h -= pp * log2(pp)
                Hcond += ps * h
                biasc += ps * abs(p0 - p1)
            Hsum += Hcond
            biassum += biasc
            cnt += 1
        if cnt:
            aH = Hsum / cnt
            ab = biassum / cnt
            trend = ""
            if prev is not None:
                trend = "H↑→uniform (smoothing)" if aH > prev + 1e-4 else "H~flat"
            print(f"  {m:>2} {aH:>14.4f} {ab:>15.4f} {cnt:>9}   {trend}")
            prev = aH
    print()
    print("  INTERPRETATION:")
    print(f"  - Gemini Thm2 (stays biased): H(form|s) ~ {Hp:.3f}, |bias| stays > 0.")
    print("  - lem:m2 (smoothing): H(form|s) -> 1.0, |bias| -> 0 as m grows.")
    print("  Plus: GG/646 shows I(x;y|C) at n=2 converges to ~0.33 bits (0.16n),")
    print("  NOT Gemini's 0.38n = 0.76 -- independent contradiction of the 'floor'.")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
