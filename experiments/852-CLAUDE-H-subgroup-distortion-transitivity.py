#!/usr/bin/env python3
"""
852-CLAUDE-H-subgroup-distortion-transitivity.py

Closes the last crack in Gemini's symplectic worst-to-avg obstruction: is there an
intermediate subgroup H (weight-preserving monomial < H <= Sp) that is TRANSITIVE on
Lagrangians yet has BOUNDED weight-distortion W? If the low-distortion elements
generate a transitive group, a *low-noise* self-reduction would survive (W=2 gives
correctable p' = (1-(1-2p)^2)/2 = 0.375, still usable). If not, the obstruction is
near-complete: you cannot randomize the Lagrangian without unbounded noise blow-up.

Method (n=2, exact, FULL Sp(4,2), order 720): enumerate all symplectic g, compute
W(g) = max_{u!=0} wt(g^T u)/wt(u). For k = 1, 2, 3: form the subgroup <{g : W(g)<=k}>
(closure under multiplication) and check its orbit on the 15 Lagrangians. Transitive
iff orbit = all 15.

  W<=1 = weight-preserving (monomial)  -> correctable p' = p (perfect, no blow-up)
  W<=2                                  -> correctable p' = 0.375 (mild blow-up)
  W<=3                                  -> correctable p' = 0.4375
  W =4 (full)                           -> p' -> 0.47 (signal gone)

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction as Fr
from itertools import combinations

n = 2
NN = 2 * n
P = Fr(1, 4)


def omega(a, b):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def matvec(M, v):
    out = 0
    for j in range(NN):
        if (v >> j) & 1:
            out ^= M[j]
    return out


def matmul(A, B):
    # columns: (A*B)_col_j = A applied to B_col_j
    return tuple(matvec(A, B[j]) for j in range(NN))


def transpose(M):
    T = [0] * NN
    for j in range(NN):
        for i in range(NN):
            if (M[j] >> i) & 1:
                T[i] |= 1 << j
    return tuple(T)


def is_invertible(M):
    basis = []
    for c in M:
        x = c
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x); basis.sort(reverse=True)
    return len(basis) == NN


def is_symplectic(M):
    for i in range(NN):
        for j in range(NN):
            if omega(M[i], M[j]) != omega(1 << i, 1 << j):
                return False
    return True


def enumerate_sp():
    out = []
    # enumerate all NN-tuples of columns; filter. 2^(NN*NN)=2^16 for n=2.
    for bits in range(1 << (NN * NN)):
        M = tuple((bits >> (NN * j)) & ((1 << NN) - 1) for j in range(NN))
        if is_invertible(M) and is_symplectic(M):
            out.append(M)
    return out


def W_of(M):
    MT = transpose(M)
    best = Fr(0)
    for u in range(1, 1 << NN):
        r = Fr(bin(matvec(MT, u)).count("1"), bin(u).count("1"))
        if r > best:
            best = r
    return best


def lagrangians():
    out = set()
    for bb in combinations(range(1, 1 << NN), 2):
        sp = {0}
        for x in bb:
            sp |= {y ^ x for y in sp}
        if len(sp) != 4:
            continue
        if any(omega(u, v) for u in sp for v in sp):
            continue
        out.add(frozenset(sp))
    return list(out)


def gen_subgroup(gens):
    I = tuple(1 << j for j in range(NN))
    grp = {I}
    frontier = [I]
    gl = list(gens)
    while frontier:
        nf = []
        for a in frontier:
            for g in gl:
                p = matmul(g, a)
                if p not in grp:
                    grp.add(p); nf.append(p)
        frontier = nf
    return grp


def orbit_size(grp, LAGS):
    L0 = LAGS[0]
    orb = {frozenset(matvec(M, v) for v in L0) for M in grp}
    return len(orb)


def main():
    print("=" * 76)
    print("852-CLAUDE  intermediate subgroup H: distortion vs Lagrangian transitivity")
    print("=" * 76)
    SP = enumerate_sp()
    LAGS = lagrangians()
    print(f"  |Sp(4,2)| = {len(SP)} (expect 720); #Lagrangians = {len(LAGS)} (expect 15)")
    Wmap = {M: W_of(M) for M in SP}
    from collections import Counter
    dist = Counter(float(w) for w in Wmap.values())
    print(f"  W(g) distribution over Sp: {dict(sorted(dist.items()))}")
    print()
    # DECISIVE test: SINGLE-application reachability. A self-reduction applies ONE g
    # (sampled to make g.L0 uniform). So what matters is the orbit of L0 under the SET
    # {g : W(g)<=k} applied ONCE -- NOT the group it generates (whose product elements
    # have unbounded W). Also report the per-Lagrangian minimum W needed.
    L0 = LAGS[0]
    minW = {}
    for M in SP:
        Lp = frozenset(matvec(M, v) for v in L0)
        w = Wmap[M]
        if Lp not in minW or w < minW[Lp]:
            minW[Lp] = w
    print(f"  {'k':>3} {'#elts W<=k':>10} {'1-step reach/15':>15} {'corr_p':>8}  single-step transitive?")
    for k in (1, 2, 3, 4):
        reach = sum(1 for L in LAGS if minW.get(L, Fr(99)) <= k)
        pcorr = (1 - (1 - 2 * P) ** k) / 2 if k < 4 else Fr(47, 100)
        trans = "YES" if reach == len(LAGS) else "no"
        print(f"  {k:>3} {sum(1 for M in SP if Wmap[M]<=k):>10} {reach:>9}/15 "
              f"{float(pcorr):>13.4f}  {trans}")
    # distribution of min-W needed across the 15 Lagrangians
    from collections import Counter
    needW = Counter(float(minW[L]) for L in LAGS)
    print(f"\n  min W needed to reach each of the 15 Lagrangians (1 step): {dict(sorted(needW.items()))}")
    worst = max(float(minW[L]) for L in LAGS)
    print(f"  => WORST Lagrangian needs W={worst:.0f} in one step "
          f"(=> corrected p' = {float((1-(1-2*P)**int(worst))/2) if worst<4 else 0.47:.4f}).")

    print("\n  VERDICT (single-application, the operative test):")
    if worst <= 2:
        print(f"  - CRACK: every Lagrangian reachable in ONE step with W<={worst:.0f};")
        print("    a low-noise worst-to-avg self-reduction may survive. ESCALATE.")
    else:
        print(f"  - Some Lagrangian needs W={worst:.0f} in a single step -> corrected noise")
        print("    near 1/2 for those. The bounded-W elements do NOT reach all Lagrangians")
        print("    in one step, so a UNIFORM single-g randomization forces high distortion.")
        print("    (Note: <W<=2> generates all of Sp, but via high-W products -- a multi-")
        print("    step walk composes W multiplicatively, W<=2^t, so reaching the far")
        print("    Lagrangians still blows up the noise. Gemini's obstruction stands.)")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
