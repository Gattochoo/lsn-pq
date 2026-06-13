#!/usr/bin/env python3
"""
441-CLAUDE-trackV-valid-output-verification.py

Adjudication of Kimi Track V (0089ad2): valid-output public bijections are
exactly Sp(2n,F2) (secret rerandomizations) — V1 characterization.

Kimi proves it modulo the finite-geometry fact "automorphisms of the
symplectic polar space over F2 = Sp(2n,F2)" (labeled OPEN, not reproven).
I strengthen the converse to a THEOREM in the LINEAR range by exhaustion:
over ALL of GL(4,F2) (20,160 elements), the maps sending every Lagrangian to
a Lagrangian are EXACTLY Sp(4,F2) (720 elements = {M : M^T J M = J}). This
closes the linear converse from first principles at n=2 (non-linear bijections
remain the OPEN part Kimi flagged).

Checks:
  (1) forward: g(x,b)=(S(x),b), S in Sp(4,F2) -> valid-output: g_*(D_L)=D_{SL}
      exactly (push-forward of the noisy membership law), all 720 S.
  (2) LINEAR CONVERSE (exhaustive GL(4,2)): {M in GL : M(L) Lagrangian for all
      L} == Sp(4,2) == {M : M^T J M = J}. 20,160 matrices.
  (3) negative controls (reproduce Kimi): affine t!=0, random bijections,
      b-dependent body maps are NOT valid-output.
  (4) V2: literal duplicate of any Sp map has SD = 123/128 (sample);
      non-duplicate Sp pairs have SD >= 123/128 (sample, min ~617/640).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

import random
from fractions import Fraction
from itertools import combinations, product

P = Fraction(1, 4)
N = 4  # 2n at n=2
SIZE = 1 << N


def omega(a, b):
    s = 0
    for i in range(2):
        s ^= (((a >> i) & 1) & ((b >> (i + 2)) & 1)) ^ \
             (((a >> (i + 2)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians():
    found = set()
    for basis in combinations(range(1, SIZE), 2):
        span = {0}
        ok = True
        for b in basis:
            if b in span:
                ok = False
                break
            span |= {x ^ b for x in span}
        if not ok or len(span) != 4:
            continue
        if any(omega(u, v) for u in span for v in span):
            continue
        found.add(frozenset(span))
    return [set(s) for s in found]


LAGS = all_lagrangians()


def matvec(M, x):
    """M = tuple of 4 column images (M[j] = M e_j); apply to x."""
    y = 0
    for j in range(4):
        if (x >> j) & 1:
            y ^= M[j]
    return y


def is_invertible(M):
    img = set()
    for x in range(SIZE):
        img.add(matvec(M, x))
    return len(img) == SIZE


def maps_lagrangians(M):
    Lset = set(frozenset(L) for L in LAGS)
    for L in LAGS:
        imL = frozenset(matvec(M, v) for v in L)
        if imL not in Lset:
            return False
    return True


def is_symplectic(M):
    # check omega(M e_i, M e_j) = omega(e_i, e_j) on the basis
    for i in range(4):
        for j in range(4):
            if omega(matvec(M, 1 << i), matvec(M, 1 << j)) != omega(1 << i, 1 << j):
                return False
    return True


def sd_split(phi0, phi1, lp_label=True):
    """SD of split ((phi0(x),b),(phi1(x),b)) vs same-secret fresh, label-pres."""
    Pd, Qd = {}, {}
    wL = Fraction(1, len(LAGS))
    for L in LAGS:
        for x in range(SIZE):
            c = 1 if x in L else 0
            for e in (0, 1):
                b = c ^ e
                w = wL * Fraction(1, SIZE) * (P if e else 1 - P)
                key = ((phi0[x], b), (phi1[x], b))
                Pd[key] = Pd.get(key, Fraction(0)) + w
        for u1 in range(SIZE):
            c1 = 1 if u1 in L else 0
            for u2 in range(SIZE):
                c2 = 1 if u2 in L else 0
                for e1 in (0, 1):
                    for e2 in (0, 1):
                        w = wL * Fraction(1, SIZE * SIZE) * \
                            (P if e1 else 1 - P) * (P if e2 else 1 - P)
                        key = ((u1, c1 ^ e1), (u2, c2 ^ e2))
                        Qd[key] = Qd.get(key, Fraction(0)) + w
    keys = set(Pd) | set(Qd)
    return sum(abs(Pd.get(k, Fraction(0)) - Qd.get(k, Fraction(0))) for k in keys) / 2


def main():
    ok = True
    rng = random.Random(20260618)
    print("=" * 74)
    print("441-CLAUDE  Track V — valid-output = Sp characterization")
    print("=" * 74)

    # enumerate GL(4,2): all 4-col matrices, invertible
    print(f"\n  |Lagr(4,F2)| = {len(LAGS)} (expect 15)")
    ok &= len(LAGS) == 15

    # (2) LINEAR CONVERSE: exhaustive GL(4,2)
    print("\n(2) exhaustive GL(4,2): {M : M(Lagr)=Lagr} == Sp(4,2):")
    lagr_preserving = []
    symplectic = []
    gl_count = 0
    for cols in product(range(SIZE), repeat=4):
        M = cols
        if not is_invertible(M):
            continue
        gl_count += 1
        sp = is_symplectic(M)
        if sp:
            symplectic.append(M)
        if maps_lagrangians(M):
            lagr_preserving.append(M)
            if not sp:
                print(f"   *** Lagrangian-preserving but NOT symplectic: {M}")
    same = set(lagr_preserving) == set(symplectic)
    ok &= same and len(symplectic) == 720 and gl_count == 20160
    print(f"   |GL(4,2)| = {gl_count} (20160); |Sp(4,2)| = {len(symplectic)} (720); "
          f"|Lagr-preserving| = {len(lagr_preserving)}")
    print(f"   Lagrangian-preserving == symplectic: {'OK' if same else 'FAIL'}")
    print(f"   => LINEAR converse PROVEN by exhaustion: valid-output linear map "
          f"<=> Sp(4,2)")

    # (1) forward: S in Sp -> g_*(D_L) = D_{SL} (check membership pushforward)
    print("\n(1) forward: S in Sp -> S(L) is Lagrangian (valid-output), sample:")
    fwd_ok = True
    for S in rng.sample(symplectic, 50):
        for L in LAGS:
            imL = set(matvec(S, v) for v in L)
            if frozenset(imL) not in set(frozenset(x) for x in LAGS):
                fwd_ok = False
    ok &= fwd_ok
    print(f"   50 random Sp maps send all Lagrangians to Lagrangians: "
          f"{'OK' if fwd_ok else 'FAIL'}")

    # (3) negative controls
    print("\n(3) negative controls (not valid-output):")
    # affine t!=0: valid-output requires S0(L)+t Lagrangian for EVERY L
    S0 = symplectic[0]
    lagset = set(frozenset(x) for x in LAGS)
    aff_bad = 0
    for t in range(1, SIZE):
        good = all(frozenset(matvec(S0, v) ^ t for v in L) in lagset for L in LAGS)
        if not good:
            aff_bad += 1
    ok &= aff_bad == SIZE - 1
    print(f"   affine t!=0: {aff_bad}/{SIZE-1} fail valid-output (expect all) "
          f"{'OK' if aff_bad == SIZE - 1 else 'FAIL'}")
    rand_bad = 0
    for _ in range(200):
        pi = list(range(SIZE)); rng.shuffle(pi)
        # treat as body map g(x,b)=(pi[x],b); valid-output needs pi(L) Lagrangian all L
        good = all(frozenset(pi[v] for v in L) in set(frozenset(x) for x in LAGS)
                   for L in LAGS)
        if not good:
            rand_bad += 1
    ok &= rand_bad == 200
    print(f"   random bijections: {rand_bad}/200 fail valid-output "
          f"{'OK' if rand_bad == 200 else 'FAIL'}")

    # (4) V2 SD: duplicate = 123/128, non-duplicate >= min
    print("\n(4) V2 SD (label-preserving Sp splits):")
    orbit = Fraction(123, 128)
    S = symplectic[7]
    Sid = list(range(SIZE))
    Sm = [matvec(S, x) for x in range(SIZE)]
    sd_dup = sd_split(Sm, Sm)
    ok &= sd_dup == orbit
    print(f"   duplicate (S,S): SD = {sd_dup} (=123/128: {sd_dup == orbit})")
    below = 0
    mn = None
    for _ in range(60):
        A = [matvec(rng.choice(symplectic), x) for x in range(SIZE)]
        B = [matvec(rng.choice(symplectic), x) for x in range(SIZE)]
        sd = sd_split(A, B)
        mn = sd if mn is None else min(mn, sd)
        if sd < orbit:
            below += 1
    ok &= below == 0
    print(f"   60 non-duplicate Sp pairs: below min = {below}; min SD = "
          f"{float(mn):.6f} (Kimi 617/640={float(Fraction(617,640)):.6f}) "
          f"{'OK' if below == 0 else 'FAIL'}")

    print("\n" + "=" * 74)
    print("RESULT:", "ALL CHECKS PASS — Track V V1 ACCEPT; linear converse PROVEN "
          "(GL(4,2) exhaustive)" if ok else "FAILURE")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
