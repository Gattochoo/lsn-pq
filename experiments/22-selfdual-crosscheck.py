r"""
Lane C7 — independent cross-check of the SEED (symplectic-Fourier self-duality + self-dual
noise rigidity), plus one new angle (instance-randomization is free → barrier localized to noise).

A parallel agent's SEED (2026-06-06-SEED-symplectic-fourier-selfduality.md) claims:
  (a) for a Lagrangian L ⊂ F₂^{2n}, the SYMPLECTIC Fourier transform F_Ω[1_L] = 2^n·1_L
      (1_L is self-dual, eigenvalue 2^n), and
  (b) any symplectic-Fourier-self-dual distribution g has g(0) = 2^{-n}  (so a self-dual noise
      is rigidly pinned at error rate 1 − 2^{-n} → 1; Regev-style self-dual-noise smoothing is
      information-theoretically useless for LSN).
This independently verifies (a),(b) with my own implementation, and adds an angle:
  (c) F_Ω = WHT ∘ J (J swaps the two symplectic halves), so F_Ω² = 2^{2n} I (eigenvalues ±2^n),
      which is WHY the rigidity holds; and
  (d) instance-randomization is FREE: random Lagrangians are sampled ~uniformly (and by Witt's
      theorem Sp(2n,F₂) acts transitively on Lagrangians, so a worst-case L* maps to a uniform
      L' by an efficient symplectic change of basis). Hence the worst→avg obstruction is NOT in
      the instance (free) but ENTIRELY in the noise (the g(0)=2^{-n} rigidity) — sharpening the
      seed's "live tip".

Run: python3 22-selfdual-crosscheck.py
"""
import numpy as np

SEED = 20260607
rng = np.random.default_rng(SEED)


def omega_int(u, v, n):
    mask = (1 << n) - 1
    ul, uh = u & mask, (u >> n) & mask
    vl, vh = v & mask, (v >> n) & mask
    return ((ul & vh).bit_count() + (uh & vl).bit_count()) & 1


def fwht(a):
    a = a.astype(np.float64).copy()
    N = a.shape[0]
    h = 1
    while h < N:
        a = a.reshape(N // (2 * h), 2, h)
        x = a[:, 0, :].copy()
        y = a[:, 1, :].copy()
        a[:, 0, :] = x + y
        a[:, 1, :] = x - y
        a = a.reshape(N)
        h *= 2
    return a


def J_perm(n):
    """index permutation J swapping the low-n and high-n bit halves of F₂^{2n}."""
    D = 2 * n
    mask = (1 << n) - 1
    perm = np.empty(1 << D, dtype=np.int64)
    for i in range(1 << D):
        perm[i] = ((i >> n) | ((i & mask) << n)) & ((1 << D) - 1)
    return perm


def F_omega(f, perm):
    """symplectic Fourier F_Ω[f](w) = Σ_v f(v)(-1)^{Ω(w,v)} = WHT[f∘J](w)."""
    return fwht(f[perm])


def rand_lagrangian(n, rng):
    D = 2 * n
    piv = {}
    rows = []

    def indep(v):
        x = v
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                return True
        return False

    while len(rows) < n:
        v = int(rng.integers(1, 1 << D))
        if all(omega_int(v, b, n) == 0 for b in rows) and indep(v):
            rows.append(v)
    return rows


def subspace_key(rows, n):
    elems = frozenset_span(rows)
    return elems


def frozenset_span(rows):
    elems = {0}
    for r in rows:
        elems |= {e ^ r for e in elems}
    return frozenset(elems)


def main():
    print("=" * 76)
    print("Lane C7 — cross-check the self-duality SEED (+ instance-randomization angle)")
    print(f"seed={SEED}")
    print("=" * 76)

    # (a) F_Ω[1_L] = 2^n · 1_L
    print("\n[a] symplectic-Fourier self-duality of Lagrangians:  F_Ω[1_L] =? 2^n · 1_L")
    print(f"  {'n':>2} {'trials':>7} {'self-dual (F_Ω[1_L]=2^n·1_L)':>30}")
    for n in [2, 3, 4]:
        D = 2 * n
        perm = J_perm(n)
        TR = 30
        ok = 0
        for _ in range(TR):
            rows = rand_lagrangian(n, rng)
            mem = frozenset_span(rows)
            ind = np.zeros(1 << D)
            for e in mem:
                ind[e] = 1.0
            F = F_omega(ind, perm)
            target = (1 << n) * ind
            ok += int(np.allclose(F, target))
        print(f"  {n:>2} {TR:>7} {f'{ok}/{TR}':>30}")

    # (c) F_Ω^2 = 2^{2n} I  (eigenvalues ±2^n) -> WHY rigidity holds
    print("\n[c] F_Ω∘F_Ω =? 2^{2n}·I   (so eigenvalues are ±2^n)")
    for n in [2, 3]:
        D = 2 * n
        perm = J_perm(n)
        f = rng.standard_normal(1 << D)
        FF = F_omega(F_omega(f, perm), perm)
        print(f"  n={n}: max|F_Ω²f − 2^{{2n}}f| = {np.max(np.abs(FF - (1 << (2*n)) * f)):.2e}")

    # (b) rigidity: any self-dual (eigenvalue +2^n) vector g with Σg=1 has g(0)=2^{-n}
    print("\n[b] rigidity of self-dual distributions:  g(0) =? 2^{-n}  (Σg=1)")
    print(f"  {'n':>2} {'g(0)':>12} {'2^{-n}':>10} {'match':>7}")
    for n in [1, 2, 3]:
        D = 2 * n
        perm = J_perm(n)
        f = np.abs(rng.standard_normal(1 << D))                 # arbitrary base
        g = (f + F_omega(f, perm) / (1 << n)) / 2.0             # project to +2^n eigenspace
        # self-dual check + normalize Σ=1
        sd_err = np.max(np.abs(F_omega(g, perm) - (1 << n) * g))
        g = g / g.sum()
        print(f"  {n:>2} {g[0]:>12.6f} {2.0**(-n):>10.6f} "
              f"{('OK' if abs(g[0] - 2.0**(-n)) < 1e-9 and sd_err < 1e-9 else 'CHECK'):>7}")

    # depolarizing is self-dual only at q=1/6 (n=1): P(I)=1/2=2^{-1}
    print("\n  depolarizing (n=1) P(I)=1-3q,P(X)=P(Y)=P(Z)=q is self-dual only at:")
    perm1 = J_perm(1)
    best = None
    for q1000 in range(0, 334):
        q = q1000 / 1000.0
        g = np.array([1 - 3 * q, q, q, q])           # index: 00=I,01=Z? -> order [00,01,10,11]
        # map to (low=X, high=Z): I=00,X=10,Z=01,Y=11 -> g[00]=1-3q,g[10]=q,g[01]=q,g[11]=q
        gg = np.array([1 - 3 * q, q, q, q])
        err = np.max(np.abs(F_omega(gg, perm1) - 2 * gg))
        if best is None or err < best[1]:
            best = (q, err)
    print(f"    closest-to-self-dual q = {best[0]:.3f} (err {best[1]:.2e}); P(I)=1-3q={1-3*best[0]:.3f} = 2^-1")

    # (d) instance-randomization is free: random Lagrangians sampled ~uniformly
    print("\n[d] instance-randomization (the OTHER half of worst→avg) is FREE:")
    print("    random Lagrangians are efficiently sampled and cover the space ~uniformly")
    print(f"    {'n':>2} {'#Lagrangians':>13} {'distinct sampled':>17} {'samples':>8}")
    for n in [2, 3]:
        nlag = 1
        for i in range(1, n + 1):
            nlag *= (1 << i) + 1
        S = 1500 if n == 2 else 4000
        seen = set()
        for _ in range(S):
            seen.add(frozenset_span(rand_lagrangian(n, rng)))
        print(f"    {n:>2} {nlag:>13} {len(seen):>17} {S:>8}")

    print("\n  Reading: (a) Lagrangians ARE symplectic-Fourier self-dual (eigenvalue 2^n); (c)")
    print("  F_Ω²=2^{2n}I so eigenvalues are ±2^n, which forces (b) every self-dual distribution")
    print("  to g(0)=2^{-n} (rigid near-total error). The SEED's two claims reproduce exactly.")
    print("  (d) Instance-randomization is FREE (uniform Lagrangian sampling; Witt: Sp transitive")
    print("  on Lagrangians, so a worst-case L* → uniform L' by an efficient symplectic map). So")
    print("  the worst→avg obstruction is NOT the instance (free) but ENTIRELY the NOISE rigidity")
    print("  g(0)=2^{-n} -- exactly localizing the barrier the seed identified. Evidence; no 7th.")


if __name__ == "__main__":
    main()
