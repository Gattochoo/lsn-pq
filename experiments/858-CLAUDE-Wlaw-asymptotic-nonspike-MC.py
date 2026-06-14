#!/usr/bin/env python3
"""
858-CLAUDE-Wlaw-asymptotic-nonspike-MC.py

The new angle on lem:m2 single-block: separate the VANISHING q_graph spike (W=0
from e in Col(A)) from the NON-SPIKE W-component, and ask whether the non-spike
min-syndrome-weight W = min_{x'} wt(y + C x') distinguishes the marginal-uniform
reduction output from matched LPN ASYMPTOTICALLY in m (and n). Exact computation
(exp 857) only reached m<=6 -- too small to see the asymptotic separation. Here we
use Monte-Carlo at larger m (n=2: m up to 30; n=3: m up to 20) to read the trend.

For each setting we draw reduction samples conditioned on e NOT in Col(A) (so the
graph-route W=0 spike is removed; this is exactly the non-spike component) and
compare the W-distribution to genuine LPN_{p_eff(n)} with the SAME public-matrix
shape, p_eff(n) = (1-(3/4)^{2n})/2 (the marginal bit-rate of the reduction output).

DECISION (disciplined -- data, not hand-wave; post-Theta(n) and post-Gemini-W-var):
  - If mean_red and mean_LPN SEPARATE (gap grows ~m) and the histograms barely
    overlap (estimated SD -> 1) as m grows -> the non-spike W-law IS a non-vanishing
    distinguisher -> lem:m2 single-block is closeable. EVIDENCE.
  - If they CONVERGE (overlap -> large, SD -> small) as m,n grow -> the confined
    noise mimics LPN beyond the vanishing spike -> lem:m2 may be FALSE (a reduction
    exists). EVIDENCE the other way.
  Monte-Carlo gives estimates, not exact SD; we report mean, std, and histogram
  overlap (1 - total-variation estimate) with enough samples to read the trend.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def rand_lag_basis(n, rng):
    NN = 2 * n
    while True:
        A = []
        span = [0]
        ok = True
        for _ in range(n):
            cands = [v for v in range(1, 1 << NN)
                     if v not in span and all(omega(v, a, n) == 0 for a in A)]
            if not cands:
                ok = False
                break
            v = rng.choice(cands)
            A.append(v)
            span = span + [s ^ v for s in span]
        if ok and len(A) == n:
            return A, set(span)


def popcount(x):
    return bin(x).count("1")


def reduction_W(n, m, rng, A, spanA):
    NN = 2 * n
    # e ~ Bernoulli(1/4)^{2n}, conditioned e NOT in Col(A) (=spanA) -- non-spike
    while True:
        e = sum((1 << i) for i in range(NN) if rng.random() < 0.25)
        if e not in spanA:
            break
    # uniform B: m rows over F_2^{2n}
    rows = [rng.randrange(1 << NN) for _ in range(m)]
    x = rng.randrange(1 << n)
    v = 0  # A x  (in F_2^{2n})
    for i in range(n):
        if (x >> i) & 1:
            v ^= A[i]
    u = v ^ e  # A x + e
    # C columns (m-bit): col_k bit i = <row_i, a_k>;  y bit i = <row_i, u>
    Ccols = [0] * n
    y = 0
    for i, r in enumerate(rows):
        for k in range(n):
            if popcount(r & A[k]) & 1:
                Ccols[k] |= 1 << i
        if popcount(r & u) & 1:
            y |= 1 << i
    # W = min over codewords C x'
    best = m + 1
    for xp in range(1 << n):
        cw = 0
        for k in range(n):
            if (xp >> k) & 1:
                cw ^= Ccols[k]
        w = popcount(y ^ cw)
        if w < best:
            best = w
    return best


def lpn_W(n, m, peff, rng):
    # uniform C (m x n) as n columns (m-bit); x; e'~Bernoulli(peff)^m
    Ccols = [rng.randrange(1 << m) for _ in range(n)]
    x = rng.randrange(1 << n)
    e = sum((1 << i) for i in range(m) if rng.random() < peff)
    cw = 0
    for k in range(n):
        if (x >> k) & 1:
            cw ^= Ccols[k]
    y = cw ^ e
    best = m + 1
    for xp in range(1 << n):
        c2 = 0
        for k in range(n):
            if (xp >> k) & 1:
                c2 ^= Ccols[k]
        w = popcount(y ^ c2)
        if w < best:
            best = w
    return best


def summarize(samples):
    nM = len(samples)
    mean = sum(samples) / nM
    var = sum((s - mean) ** 2 for s in samples) / nM
    return mean, var ** 0.5


def hist(samples, m):
    h = {}
    for s in samples:
        h[s] = h.get(s, 0) + 1
    nM = len(samples)
    return {k: v / nM for k, v in h.items()}


def tv_estimate(h1, h2):
    ks = set(h1) | set(h2)
    return 0.5 * sum(abs(h1.get(k, 0) - h2.get(k, 0)) for k in ks)


def main():
    rng = random.Random(101)
    print("=" * 80)
    print("858-CLAUDE  non-spike W-law asymptotics (Monte-Carlo): reduction vs LPN")
    print("=" * 80)
    NSAMP = 8000
    configs = [(2, [8, 14, 22, 30]), (3, [9, 15, 24])]
    for n, ms in configs:
        peff = (1 - (0.75) ** (2 * n)) / 2
        print(f"\n  n={n}, p_eff={peff:.4f}:")
        print(f"  {'m':>3} {'mean_red':>9} {'std_red':>8} {'mean_LPN':>9} {'std_LPN':>8} "
              f"{'meangap':>8} {'TV(W)est':>9}")
        for m in ms:
            # reduction: redraw a fresh (A, B, x, e) per sample (fresh-B model)
            red = []
            for _ in range(NSAMP):
                A, spanA = rand_lag_basis(n, rng)
                red.append(reduction_W(n, m, rng, A, spanA))
            lpn = [lpn_W(n, m, peff, rng) for _ in range(NSAMP)]
            mr, sr = summarize(red)
            ml, sl = summarize(lpn)
            tv = tv_estimate(hist(red, m), hist(lpn, m))
            print(f"  {m:>3} {mr:>9.3f} {sr:>8.3f} {ml:>9.3f} {sl:>8.3f} "
                  f"{mr - ml:>8.3f} {tv:>9.3f}")
    print()
    print("  READ: TV(W)est -> 1 with growing m (and persisting/growing across n) =>")
    print("  non-spike W-law is a non-vanishing distinguisher (lem:m2 closeable).")
    print("  TV(W)est -> 0 => confined noise mimics LPN; lem:m2 may be FALSE.")
    print("  (Monte-Carlo estimate, NSAMP=%d; trend, not exact SD.)" % NSAMP)
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
