#!/usr/bin/env python3
"""
740-CLAUDE-stacked-rank-tightening.py  (v2 — premise corrected)

Tightening of the stacked-syndrome-rank verdict (642). A second Claude session
caught that Gemini's rank(HY) <= 2n is loose; their proposed sharp bound was
rank(HB) = rank(B) - n. v1 of this script tested EXACTLY that and it FAILED
numerically: over low-rank B, rank(HY) exceeded rank(B) - n. The failure is a
finding, not noise -- the premise "rank(C) = n" is false when B is rank-
deficient. The CORRECT identity is

  C = BA,  Col(C) = Col(BA) subset Col(B)  (always),
  H = left parity-check of C, so ker H = Col(C),
  rank(HB) = dim Col(B) - dim(Col(B) cap Col(C))
           = rank(B) - rank(C)            [since Col(C) subset Col(B)]
           = rank(B) - rank(BA).

Now rank(BA) = n - dim(Col(A) cap ker B), so

  rank(HB) = rank(B) - n + dim(Col(A) cap ker B)
           = n - corank(B) + dim(Col(A) cap ker B).

Two consequences, both sharper/cleaner than either Gemini or the v1 premise:

  (A) UNIVERSAL BOUND  rank(HY) <= rank(HB) <= n   for every B (Gemini's 2n is
      loose by a factor of 2). Proof: dim(Col(A) cap ker B) <= corank(B), so
      rank(HB) <= n - corank(B) + corank(B) = n.

  (B) FULL-RANK B  (corank 0): rank(HB) = n EXACTLY, never 0. So in the honest
      regime (uniform B is full-rank w.h.p.) the distinguisher's threshold is n,
      not 2n: LPN rank -> min(m-n, k) exceeds n already for k >= n+1.

  The second session's "rank(B) - n" is the full-rank-B specialization (correct
  there, = n). The degenerate HB = 0 they feared needs rank(B) <= n, which forces
  Col(C) = Col(B) => y in Col(C) ALWAYS => W = 0 always => caught by the W-spike
  with prob 1. No escape in the shared-C model either way.

CRUCIAL SCOPE (Track EE, commit 78b81fc): rank(HY) is a MULTI-BLOCK statistic
(Y = [Be^(1)..Be^(k)], k>1 columns sharing one C). lem:m2 itself is a SINGLE
block (one e, Y has one column, rank in {0,1} -- trivial). So this bound closes
the MULTI-block shared-C variant, NOT lem:m2 proper. Recorded here so the paper
edit does not over-claim.

Checks (n=2, exact):
  (1) identity rank(HB) = rank(B) - rank(BA), over random (B, A) of all ranks.
  (2) universal bound rank(HY) <= rank(HB) <= n (Gemini's 2n loose).
  (3) full-rank B => rank(HB) = n exactly (never degenerate).
  (4) rank(B) <= n extreme => HB may be 0, but then y in Col(C) always (W=0).
  (5) typical rank(B) for uniform B (is full-rank dominant?).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random


def f2_rank(cols):
    """column rank over F_2 of a list of integers (bit-packed columns)."""
    basis = []
    for c in cols:
        x = c
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return len(basis)


def main():
    rng = random.Random(3)
    n = 2
    NN = 2 * n
    m = 7
    print("=" * 74)
    print("740-CLAUDE v2  sharp stacked-rank identity: rank(HB) = rank(B) - rank(BA)")
    print("=" * 74)

    def rand_full_rank_cols(count, nbits, want):
        while True:
            cols = [rng.randrange(1 << nbits) for _ in range(count)]
            if f2_rank(cols) == want:
                return cols

    def make_B(target_rank):
        """m x 2n matrix as NN columns (m-bit), column rank exactly target_rank."""
        if target_rank == 0:
            return [0] * NN
        indep = rand_full_rank_cols(target_rank, m, target_rank)
        cols = []
        # guarantee the rank is hit: first target_rank columns are the indep set
        for i in range(NN):
            if i < target_rank:
                cols.append(indep[i])
            else:
                coeffs = rng.randrange(1 << target_rank)
                c = 0
                for j in range(target_rank):
                    if (coeffs >> j) & 1:
                        c ^= indep[j]
                cols.append(c)
        rng.shuffle(cols)
        return cols  # B as NN columns over F_2^m

    def C_from_BA(Bcols, Acols):
        """C = B A. A given as n columns over F_2^{2n}; C column k (m-bit)."""
        Ccols = []
        for ak in Acols:
            c = 0
            for j in range(NN):
                if (ak >> j) & 1:
                    c ^= Bcols[j]
            Ccols.append(c)
        return Ccols  # n columns over F_2^m

    def left_parity_basis(Ccols):
        """basis of {h in F_2^m : h . C_col = 0 for all cols} (ker H = Col(C))."""
        H = []
        for h in range(1 << m):
            if all(bin(c & h).count("1") % 2 == 0 for c in Ccols):
                H.append(h)
        Hb = []
        for h in H:
            x = h
            for b in Hb:
                x = min(x, x ^ b)
            if x:
                Hb.append(x)
                Hb.sort(reverse=True)
        return Hb

    def HB_image_cols(Hb, Bcols):
        """columns of H B: for each B-column, the |Hb|-bit vector (h_r . Bcol)."""
        out = []
        for bcol in Bcols:
            v = 0
            for r, h in enumerate(Hb):
                if bin(h & bcol).count("1") & 1:
                    v |= 1 << r
            out.append(v)
        return out

    print("\n(1)+(2)+(3) identity rank(HB)=rank(B)-rank(BA), bound <= n, full-rank => n")
    ok = True
    seen_fullrank_eq_n = 0
    max_rHB = -1
    bound_violations = 0
    for target in (0, 1, 2, 3, 4):
        idviol = 0
        for _ in range(60):
            Bcols = make_B(target)
            rB = f2_rank(Bcols)
            Acols = rand_full_rank_cols(n, NN, n)
            Ccols = C_from_BA(Bcols, Acols)
            rC = f2_rank(Ccols)                 # = rank(BA)
            Hb = left_parity_basis(Ccols)
            HBcols = HB_image_cols(Hb, Bcols)
            rHB = f2_rank(HBcols)
            # identity
            if rHB != rB - rC:
                idviol += 1
                ok = False
            # universal bound <= n
            if rHB > n:
                bound_violations += 1
                ok = False
            max_rHB = max(max_rHB, rHB)
            if rB == NN:                        # full-rank B
                if rHB != n:
                    ok = False
                else:
                    seen_fullrank_eq_n += 1
        tag = "OK" if idviol == 0 else f"IDENT-FAIL({idviol})"
        print(f"   rank(B) target {target}: rank(HB)=rank(B)-rank(BA) {tag}; "
              f"all rank(HB) <= n={n} so far (max={max_rHB})")
    print(f"   -> universal bound rank(HB) <= n: "
          f"{'HOLDS' if bound_violations == 0 else f'VIOLATED x{bound_violations}'} "
          f"(Gemini's 2n is loose by 2x)")
    print(f"   -> full-rank B always gave rank(HB)=n: {seen_fullrank_eq_n} cases, "
          f"none degenerate")

    print("\n(4) rank(B) <= n extreme: HB can be 0; then y in Col(C) ALWAYS (W=0 spike)")
    # demonstrate: rank(B)=n, Col(C)=Col(B) possible -> HB=0; and any y has e-part in Col(B)
    deg = 0
    for _ in range(200):
        Bcols = make_B(n)                  # rank n
        rB = f2_rank(Bcols)
        Acols = rand_full_rank_cols(n, NN, n)
        Ccols = C_from_BA(Bcols, Acols)
        rC = f2_rank(Ccols)
        Hb = left_parity_basis(Ccols)
        HBcols = HB_image_cols(Hb, Bcols)
        rHB = f2_rank(HBcols)
        if rHB == 0:
            deg += 1
            # when HB=0: Col(B) subset Col(C) (=> equal, both rank n). every Be in Col(C).
            colB = f2_rank(Bcols)
            colBC = f2_rank(Bcols + Ccols)
            assert colBC == rC, "HB=0 must mean Col(B) subset Col(C)"
    print(f"   among rank-n B: {deg}/200 gave HB=0; each verified Col(B) subset Col(C)")
    print(f"   => in those cases y = Cx + Be has Be in Col(C), so y in Col(C) ALWAYS")
    print(f"      = W=0 spike (caught with prob 1). Escaping rank-test forces W-spike.")

    print("\n(5) typical rank(B) for uniform B (m x 2n, m=7, n=2):")
    ranks = {}
    for _ in range(3000):
        Bcols = [rng.randrange(1 << m) for _ in range(NN)]
        r = f2_rank(Bcols)
        ranks[r] = ranks.get(r, 0) + 1
    print(f"   rank distribution: {dict(sorted(ranks.items()))}")
    full = ranks.get(NN, 0)
    print(f"   => full-rank 2n={NN}: {full}/3000 = {full/3000:.3f}; "
          f"so rank(HB)=n is the typical case")

    print("\n(6) SINGLE-BLOCK scope guard (Track EE): for k=1, Y has ONE column,")
    print("    rank(HY) in {0,1} -- trivial. The bound above closes the MULTI-block")
    print("    shared-C variant, NOT lem:m2 (single block). lem:m2's single-block")
    print("    signal is the low-dim support SD, asymptotic rate OPEN.")

    print("\n" + "=" * 74)
    print("VERDICT (v2): sharp identity rank(HB) = rank(B) - rank(BA); universal")
    print("  bound rank(HY) <= rank(HB) <= n (Gemini's 2n loose 2x); full-rank B")
    print("  => rank(HB) = n exactly (never degenerate). Second session's rank(B)-n")
    print("  is the full-rank specialization. Degenerate HB=0 forces W=0-always.")
    print("  SCOPE: closes MULTI-block shared-C only; lem:m2 (single-block) stays OPEN.")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
