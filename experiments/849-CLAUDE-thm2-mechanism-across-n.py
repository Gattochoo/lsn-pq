#!/usr/bin/env python3
"""
849-CLAUDE-thm2-mechanism-across-n.py

Pushes the Theta(n) finding (Gemini Theorem 2, confirmed at n=2 by exp 848) across
n = 2,3,4 at the MECHANISM level -- faster than the full I(x;y|C) computation
(which needs large m to converge). If the message-form mechanism is n-independent,
it predicts I(x;y|C) = Theta(n), not o(n).

Two quantities, averaged over sampled (random Lagrangian A, uniform B), m = 2n,3n:
  (1) avg conditional |bias| of a weight-1 message form <e_i,e> given the syndrome
      s = HBe (e_i a weight-1 vector NOT in row(HB)). If this stays ~ 1-2p = 0.5
      across n and m, the message directions do NOT smooth -> biased -> leak.
  (2) #{independent weight-1 directions e_i mod row(HB)} = the count of biased
      message directions. rank(HB) <= n caps the syndrome, so ~ n message
      directions stay biased -> sum of Omega(1) biases over ~n directions = Theta(n).

Decision: if |bias| ~ 0.5 (flat in n,m) AND #biased-dirs scales like n, then
I(x;y|C) = Theta(n) (Gemini's scaling), confirming the paper's 'prove I=o(n)' is the
wrong target. If |bias| -> 0 as n grows, the mechanism is a finite-n artifact and
I = o(n) survives.

Lagrangians sampled (not enumerated): random isotropic n-frame in F_2^{2n}.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from math import log2
from collections import defaultdict

P = 0.25


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def dot(a, b):
    return bin(a & b).count("1") & 1


def add_to_basis(basis, v):
    x = v
    for b in basis:
        x = min(x, x ^ b)
    if x:
        basis.append(x)
        basis.sort(reverse=True)
        return True
    return False


def in_span(v, basis):
    x = v
    for b in basis:
        x = min(x, x ^ b)
    return x == 0


def random_lagrangian_basis(n, rng):
    """random ordered isotropic basis A=(a_0..a_{n-1}) of a Lagrangian in F_2^{2n}."""
    NN = 2 * n
    while True:
        A = []
        span = []
        ok = True
        for _ in range(n):
            cands = [v for v in range(1, 1 << NN)
                     if not in_span(v, span) and all(omega(v, a, n) == 0 for a in A)]
            if not cands:
                ok = False
                break
            v = rng.choice(cands)
            A.append(v)
            add_to_basis(span, v)
        if ok and len(A) == n:
            return A


def main():
    rng = random.Random(17)
    print("=" * 78)
    print("849-CLAUDE  Theorem-2 mechanism across n: does the message form stay biased?")
    print("=" * 78)
    print(f"  p={P}, unconditional |bias| = 1-2p = {1-2*P}. Smoothing => |bias|->0.")
    print(f"  {'n':>2} {'m':>3} {'avg|bias|form':>14} {'avgH(form|s)':>13} "
          f"{'#biased-dirs':>13} {'ratio/n':>8}")
    for n in (2, 3, 4):
        NN = 2 * n
        for m in (2 * n, 3 * n):
            biassum = 0.0
            Hsum = 0.0
            dircount = 0.0
            cnt = 0
            nsamp = 1500 if n < 4 else 600
            for _ in range(nsamp):
                A = random_lagrangian_basis(n, rng)
                rows = [rng.randrange(1 << NN) for _ in range(m)]
                # C row i = (<row_i, a_k>)_k in F_2^n
                # columns of C (over rows) for parity check: col_k = bits <row_i,a_k>
                Ccols = []
                for ak in A:
                    c = 0
                    for i, r in enumerate(rows):
                        if dot(r, ak):
                            c |= 1 << i
                    Ccols.append(c)
                # H = {h in F_2^m : dot(h, Ccol_k)=0 for all k}; basis of left-null(C)
                Hbasis = []
                # solve: h with Ccols (n constraints). Enumerate null space via reduction
                # (m can be up to 12; 2^12=4096 ok for n=4 m=12)
                for h in range(1 << m):
                    if all(dot(h, c) == 0 for c in Ccols):
                        add_to_basis(Hbasis, h)
                # HB rows in F_2^{2n}: for h in Hbasis, vector w with w_k = sum_i h_i (row_i)_k
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
                HBspan = []
                for w in HBrows:
                    add_to_basis(HBspan, w)
                if len(HBspan) != n:
                    continue  # need full-rank-B typical (rank(HB)=n)
                # count independent weight-1 dirs mod row(HB)
                quo = list(HBspan)
                cdir = 0
                for k in range(NN):
                    if add_to_basis(quo, 1 << k):
                        cdir += 1
                dircount += cdir
                # pick one weight-1 e_i not in HBspan; conditional bias of <e_i,e> given s
                ei = None
                for k in range(NN):
                    if not in_span(1 << k, HBspan):
                        ei = 1 << k
                        break
                if ei is None:
                    continue
                joint = defaultdict(float)
                for e in range(1 << NN):
                    w = P ** bin(e).count("1") * (1 - P) ** (NN - bin(e).count("1"))
                    f = dot(ei, e)
                    s = 0
                    for j, hr in enumerate(HBspan):
                        if dot(hr, e):
                            s |= 1 << j
                    joint[(f, s)] += w
                Ps = defaultdict(float)
                for (f, s), w in joint.items():
                    Ps[s] += w
                Hc = 0.0
                bc = 0.0
                for s, ps in Ps.items():
                    p0 = joint.get((0, s), 0.0) / ps
                    p1 = joint.get((1, s), 0.0) / ps
                    h = 0.0
                    for pp in (p0, p1):
                        if pp > 0:
                            h -= pp * log2(pp)
                    Hc += ps * h
                    bc += ps * abs(p0 - p1)
                biassum += bc
                Hsum += Hc
                cnt += 1
            if cnt:
                print(f"  {n:>2} {m:>3} {biassum/cnt:>14.4f} {Hsum/cnt:>13.4f} "
                      f"{dircount/cnt:>13.2f} {dircount/cnt/n:>8.2f}")
    print()
    print("  READ: |bias|form flat ~0.5 across n => message dirs stay biased (no smoothing).")
    print("  #biased-dirs ~ n (ratio/n ~ 1) => Theta(n) biased directions => I(x;y|C)=Theta(n).")
    print("  Both => Gemini Theorem 2 scaling holds; paper's 'prove I=o(n)' is the wrong")
    print("  target. (No-go itself rests on SD-from-LPN, unaffected.)")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
