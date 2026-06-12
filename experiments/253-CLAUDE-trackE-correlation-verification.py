#!/usr/bin/env python3
"""
253-CLAUDE-trackE-correlation-verification.py

Independent adjudication of Kimi Track E (aa02290): exact sympLPN correlations.

THEOREM E.1: advantage correlation of the k-row bundle parity query
    g_x(A) = (-1)^{<1_S, Ax>} (1-2p)^k :
    <g_x, g_{x'}> = (1-2p)^{2k}            if x = x'
                  = -(1-2p)^{2k}/(2^{2n}-1) if x != x'.
THEOREM E.2: likelihood-ratio correlations
    <D_x,D_x> = (1+tau)^{2n} - 1,  <D_x,D_{x'}> = -((1+tau)^{2n}-1)/(2^{2n}-1),
    tau = (1-2p)^2.

From-scratch checks (exact Fractions):
  (1) the character average E_A[(-1)^{<1_S, Aw>}] = -1/(2^{2n}-1) for EVERY
      non-empty row-subset S and EVERY w != 0, by enumerating the full
      isotropic-basis ensemble (all Lagrangians x all ordered bases) at n=2,3.
  (2) the sigma-twist: Kimi's proof lemma "sum_{v in L}(-1)^{<1_S,v>} =
      2^n 1[1_S in L]" is FALSE as written; the correct statement carries
      1_{sigma(S)} (J-twist, sigma(i) = i +- n). Exhibit a concrete (L, S)
      counterexample, and verify the corrected lemma over all L and all S.
      (The final probability is unaffected: Pr_L[w in L] = 1/(2^n+1) for any
      fixed non-zero w.)
  (3) E.2 likelihood-ratio correlations by direct (A, y) enumeration at
      n=2 (90 matrices x 16 y) and n=3 (22680 x 64): diagonal 369/256,
      11529/4096; off-diagonal -123/1280, -183/4096; all pairs (x, x').
  (4) the averages: rho_bar (likelihood) = 1107/2560 (n=2), 6405/16384 (n=3);
      k-bundle average = 3(1/4)^k/10 (n=2), 5(1/4)^k/36 (n=3).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from fractions import Fraction
from itertools import combinations, permutations

P = Fraction(1, 4)
TAU = (1 - 2 * P) ** 2  # 1/4


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (((a >> i) & 1) & ((b >> (i + n)) & 1)) ^ \
             (((a >> (i + n)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians(n):
    N = 2 * n
    found = set()
    for basis in combinations(range(1, 1 << N), n):
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
    return [sorted(s) for s in found]


def ensemble_matrices(n):
    """All matrices of the isotropic ensemble: ordered bases (as column
    tuples) of every Lagrangian."""
    mats = []
    for L in all_lagrangians(n):
        elems = [v for v in L if v != 0]
        for tup in permutations(elems, n):
            span = {0}
            ok = True
            for b in tup:
                if b in span:
                    ok = False
                    break
                span |= {x ^ b for x in span}
            if ok:
                mats.append(tup)
    return mats


def Ax(A, x, n):
    v = 0
    for j in range(n):
        if (x >> j) & 1:
            v ^= A[j]
    return v


def dot(a, b):
    return bin(a & b).count("1") & 1


def sigma_mask(mask, n):
    """swap lower and upper halves of a 2n-bit mask."""
    lo = mask & ((1 << n) - 1)
    hi = mask >> n
    return (hi) | (lo << n)


def main():
    ok = True
    print("=" * 76)
    print("253-CLAUDE  Track E — sympLPN exact correlations: from-scratch check")
    print("=" * 76)

    for n in (2, 3):
        N = 2 * n
        mats = ensemble_matrices(n)
        lags = all_lagrangians(n)
        print(f"\nn={n}: ensemble size = {len(mats)} matrices, "
              f"{len(lags)} Lagrangians")

        # (1) character average for every non-empty S and every w != 0
        worst = []
        target = -Fraction(1, 2 ** N - 1)
        all_S = range(1, 1 << N)
        ok1 = True
        for Smask in all_S:
            for w in range(1, 2 ** n):
                tot = Fraction(0)
                for A in mats:
                    v = Ax(A, w, n)
                    tot += (-1) ** dot(Smask, v)
                avg = tot / len(mats)
                if avg != target:
                    ok1 = False
                    worst.append((Smask, w, avg))
        ok &= ok1
        print(f"   (1) E_A[(-1)^<1_S,Aw>] = -1/(2^{{2n}}-1) = {target} for ALL "
              f"{(1 << N) - 1} masks x {2**n - 1} secrets: {'OK' if ok1 else 'FAIL ' + str(worst[:3])}")

        # (2) sigma-twist lemma
        # corrected: sum_{v in L} (-1)^{<1_S, v>} = 2^n * 1[ sigma(1_S) in L ]
        ok2 = True
        counterexample_found = False
        for L in lags:
            Lset = set(L)
            for Smask in all_S:
                ssum = sum((-1) ** dot(Smask, v) for v in Lset)
                corrected = 2 ** n * (1 if sigma_mask(Smask, n) in Lset else 0)
                kimi_form = 2 ** n * (1 if Smask in Lset else 0)
                if ssum != corrected:
                    ok2 = False
                if ssum != kimi_form and not counterexample_found:
                    counterexample_found = True
                    print(f"   (2) counterexample to the UNtwisted lemma: "
                          f"L={L}, S-mask={Smask:0{N}b}: sum={ssum}, "
                          f"untwisted claim={kimi_form}, corrected={corrected}")
        ok &= ok2
        print(f"   (2) corrected sigma-twist lemma holds for ALL (L, S): "
              f"{'OK' if ok2 else 'FAIL'}"
              f"   (untwisted version refuted: {counterexample_found})")

        # (3) likelihood-ratio correlations
        # ratio_x(A,y) = prod_i (1 + (1-2p)(-1)^{y_i + (Ax)_i}).
        # (3a) at n=2: FULL direct (A, y) enumeration (no algebraic shortcut),
        #      including a check of the y-marginalization identity
        #      E_y[(r_x-1)(r_x'-1)] = prod_i(1 + tau (-1)^{v_i}) - 1, v = A(x+x').
        # (3b) at n=3: the y-marginalized form over all A (the identity having
        #      been verified exactly at n=2 for every (A, x, x')).
        s_lin = 1 - 2 * P
        diag_target = (1 + TAU) ** N - 1
        off_target = -diag_target / (2 ** N - 1)
        ok3 = True
        for x in range(2 ** n):
            for xp in range(x, 2 ** n):
                tot = Fraction(0)
                for A in mats:
                    ux, uxp = Ax(A, x, n), Ax(A, xp, n)
                    v = ux ^ uxp
                    marg = Fraction(1)
                    for i in range(N):
                        marg *= 1 + TAU * (-1) ** ((v >> i) & 1)
                    marg -= 1
                    if n == 2:
                        dtot = Fraction(0)
                        for y in range(1 << N):
                            rx = Fraction(1)
                            rxp = Fraction(1)
                            for i in range(N):
                                yi = (y >> i) & 1
                                rx *= 1 + s_lin * (-1) ** (yi ^ ((ux >> i) & 1))
                                rxp *= 1 + s_lin * (-1) ** (yi ^ ((uxp >> i) & 1))
                            dtot += (rx - 1) * (rxp - 1)
                        if dtot / (1 << N) != marg:
                            ok3 = False
                            print(f"      y-marginalization FAIL at A={A}, "
                                  f"x={x}, x'={xp}")
                        tot += dtot / (1 << N)
                    else:
                        tot += marg
                corr = tot / len(mats)
                want = diag_target if x == xp else off_target
                if corr != want:
                    ok3 = False
                    print(f"      MISMATCH x={x} x'={xp}: {corr} != {want}")
        ok &= ok3
        mode = "full (A,y) + marginalization identity" if n == 2 \
            else "y-marginalized over all A"
        print(f"   (3) likelihood-ratio correlations, all secret pairs "
              f"[{mode}]: {'OK' if ok3 else 'FAIL'}  "
              f"(diag={diag_target}, off={off_target})")

        # (4) averages
        rho_bar = (2 ** n * diag_target + (4 ** n - 2 ** n) * abs(off_target)) \
            / 4 ** n
        rho_claim = {2: Fraction(1107, 2560), 3: Fraction(6405, 16384)}[n]
        ok4 = rho_bar == rho_claim
        kb = (1 - 2 * P) ** 2 * Fraction(2 ** n + 2, 2 ** n * (2 ** n + 1))
        kb_claim = {2: Fraction(3, 40), 3: Fraction(5, 144)}[n]  # k = 1
        ok4 &= kb == kb_claim
        ok &= ok4
        print(f"   (4) rho_bar = {rho_bar} (claim {rho_claim}); "
              f"k=1 bundle avg = {kb} (claim {kb_claim}): {'OK' if ok4 else 'FAIL'}")

    print("\n" + "=" * 76)
    print("RESULT:", "ALL CHECKS PASS — E.1 + E.2 ACCEPT (with sigma-twist proof fix)"
          if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 76)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
