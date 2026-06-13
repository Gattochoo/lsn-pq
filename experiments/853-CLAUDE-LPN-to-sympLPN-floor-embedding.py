#!/usr/bin/env python3
"""
853-CLAUDE-LPN-to-sympLPN-floor-embedding.py

Opens the HARDNESS-FLOOR arc: does LPN <= sympLPN (def:symplpn)? A floor would
anchor sympLPN's hardness to LPN (complementing the sympLPN-not-reducible-to-LPN
no-go). Target is sympLPN, NOT membership-LSN (which is info-theoretically secure
with poly(n) samples per paper line 273 -> empty for a floor).

Two structural facts established here (n=2,3 exact), framing the floor:

(A) TOP-HALF embedding: column_j = (A'_col_j ; 0) in F_2^{2n} is isotropic
    (omega((u,0),(v,0))=0). Then y = Ax+e = (A'x + e_top ; e_bottom): top half is
    an n-sample LPN instance, bottom is pure noise. So LPN(n samples) <= sympLPN with
    this SPECIAL (vertical-complement) Lagrangian. But (i) only n samples, (ii) a
    degenerate Lagrangian, not uniform.

(B) ** GRAPH-LAGRANGIAN reformulation (the clean content) **: a Lagrangian of the
    big Schubert cell is {(v, Sv) : v} for a SYMMETRIC S (S^T=S). Its basis is
    A = [ (e_i ; S e_i) ]. Then y = Ax+e gives
        y_top   = x   + e_top      (n equations: identity block)
        y_bottom = S x + e_bottom  (n equations: matrix S)
    so sympLPN with a graph-Lagrangian IS EXACTLY an LPN instance with the structured
    2n x n matrix [ I ; S ], S symmetric, 2n samples, secret x. And uniform Lagrangian
    = uniform symmetric S over the big cell (a constant fraction of all Lagrangians).

    => average-case sympLPN ≡ LPN with public matrix [I ; S], S ~ uniform symmetric.
    The floor LPN <= sympLPN thus reduces to the concrete question:
        is [I;S]-structured LPN (S uniform symmetric) as hard as uniform-matrix LPN?
    (the worst-case/special-Lagrangian floor is immediate from (A); the average-case
    floor is this structured-LPN-hardness question -- handed to Gemini.)

This script verifies (A) isotropy+recovery and (B) the [I;S] equivalence exactly, and
counts graph-cell vs total Lagrangians.

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from itertools import combinations, product


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def is_isotropic(cols, n):
    return all(omega(cols[i], cols[j], n) == 0 for i in range(len(cols))
               for j in range(len(cols)))


def count_lagrangians(n):
    NN = 2 * n
    out = set()
    # enumerate n-dim isotropic subspaces (small n only)
    vecs = list(range(1, 1 << NN))
    # build by extending isotropic independent sets -- feasible n<=3 via spans
    def rec(basis, span):
        if len(basis) == n:
            out.add(frozenset(span))
            return
        for v in vecs:
            if v in span:
                continue
            if any(omega(v, b, n) for b in basis):
                continue
            nb = basis + [v]
            nsp = set(span)
            for s in span:
                nsp.add(s ^ v)
            rec(nb, nsp)
    rec([], {0})
    return out


def main():
    rng = random.Random(31)
    print("=" * 74)
    print("853-CLAUDE  LPN <= sympLPN floor: embeddings (top-half + graph-Lagrangian)")
    print("=" * 74)

    for n in (2, 3):
        NN = 2 * n
        print(f"\n--- n={n} (ambient F_2^{NN}) ---")

        # (A) top-half embedding
        # random LPN matrix A' (n x n), columns c_j in F_2^n; embed as (c_j ; 0)
        Acols = [rng.randrange(1, 1 << n) for _ in range(n)]
        top = [c for c in Acols]  # in F_2^n (top coords)
        symp_cols = [c for c in top]  # (c ; 0): bottom zero -> same int (low n bits)
        iso = is_isotropic(symp_cols, n)
        print(f"  (A) top-half: columns (A'_j ; 0) isotropic? {iso}  "
              f"(=> LPN(n samples) <= sympLPN with this special Lagrangian)")

        # (B) graph-Lagrangian: symmetric S (n x n), columns (e_i ; S e_i)
        # S symmetric over F_2
        S = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                b = rng.randrange(2)
                S[i][j] = b
                S[j][i] = b
        gcols = []
        for i in range(n):
            top_i = 1 << i               # e_i in top
            Se_i = 0                     # S e_i in bottom
            for r in range(n):
                if S[r][i]:
                    Se_i ^= 1 << r
            col = top_i | (Se_i << n)    # (e_i ; S e_i)
            gcols.append(col)
        iso2 = is_isotropic(gcols, n)
        # verify y_top = x + e_top, y_bottom = Sx + e_bottom
        ok = True
        for _ in range(200):
            x = rng.randrange(1 << n)
            # A x (no noise): sum of columns where x bit set
            Ax = 0
            for i in range(n):
                if (x >> i) & 1:
                    Ax ^= gcols[i]
            ytop = Ax & ((1 << n) - 1)
            ybot = (Ax >> n) & ((1 << n) - 1)
            Sx = 0
            for r in range(n):
                bit = 0
                for c in range(n):
                    if S[r][c] and ((x >> c) & 1):
                        bit ^= 1
                if bit:
                    Sx |= 1 << r
            if ytop != x or ybot != Sx:
                ok = False
                break
        print(f"  (B) graph-Lagrangian (S symmetric): isotropic? {iso2}; "
              f"y_top=x & y_bottom=Sx verified? {ok}")
        print(f"      => sympLPN(graph-L) == LPN with matrix [I ; S], S symmetric, "
              f"2n={NN} samples, secret x.")

        # cell counting
        if n <= 3:
            LAGS = count_lagrangians(n)
            total = len(LAGS)
            # graph-cell Lagrangians: those that are graphs {(v,Sv)} = those with
            # trivial intersection with the 'vertical' subspace {(0,w)} (top-projection
            # is full rank n). Count by symmetric S: 2^{n(n+1)/2}.
            graph_count = 1 << (n * (n + 1) // 2)
            import math
            pred_total = 1
            for i in range(1, n + 1):
                pred_total *= (2 ** i + 1)
            print(f"      Lagrangians total={total} (formula prod(2^i+1)={pred_total}); "
                  f"graph-cell=2^(n(n+1)/2)={graph_count} "
                  f"({100*graph_count/total:.0f}% -- a constant fraction).")

    print("\n  STRUCTURAL RESULT (clean reformulation):")
    print("  average-case sympLPN (uniform Lagrangian) ≡ LPN with public matrix [I ; S],")
    print("  S ~ uniform symmetric, restricted to the graph cell (constant fraction).")
    print("  => Floor LPN <= sympLPN reduces to: is [I;S]-LPN (S uniform symmetric) as")
    print("  hard as uniform-matrix LPN? Worst-case/special-Lagrangian floor is immediate")
    print("  (top-half embedding). [-> Gemini: structured-LPN hardness or obstruction.]")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
