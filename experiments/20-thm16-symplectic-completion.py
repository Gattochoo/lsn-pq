r"""
Lane C4 — verify the symplectic-completion ENGINE of Thm 1.6 Stage 1 (LPN → sympLPN).

Lane C2 illustrated the degeneracy mechanism but explicitly did NOT reimplement the reduction.
This closes part of that gap: the *algebraic engine* of Stage 1 (LPN → sympLPN), which is
stated verbatim in 2509.20697 §1.2.3 (Eqs 1.3–1.4) and is fully implementable.

Construction (Eq 1.3): stack the given matrix and a padding block A' as
      B = [ N1 ; M ; N2 ; A' ]  ∈ F₂^{2n×ℓ},   N1,N2 ∈ F₂^{a×ℓ},  M,A' ∈ F₂^{b×ℓ},  a+b=n.
The top n rows (N1,M) are the symplectic "x" half, the bottom n rows (N2,A') the "z" half.
(Eq 1.4): the symplectic inner product of columns i,j of B equals  S_ij + S_ji,  where
      S := N1ᵀ N2 + Mᵀ A'.
So ALL columns are symplectically orthogonal  ⟺  S is symmetric. The reduction therefore:
   sample a uniform SYMMETRIC S';  set T := S' − N1ᵀ N2;  solve Mᵀ A' = T for A'.
The given LPN data lives verbatim in the top 2n−b rows [N1;M;N2]; only A' (b rows) is added.

What this script verifies (faithfully, from the verbatim equations):
  - the completed B has EVERY pair of columns symplectically orthogonal (B isotropic);
  - B has full column rank ℓ;
  - S = N1ᵀN2 + MᵀA' equals the intended symmetric S' (so Eq 1.4 holds as stated);
  - the original matrix [N1;M;N2] is embedded VERBATIM as the top 2n−b rows of B.
What it does NOT claim: the precise LPN-secret-preservation map (2509.20697 §§5–6, not
reimplemented) — so this verifies the completion engine, not the whole reduction. (Honest.)

Run: python3 20-thm16-symplectic-completion.py
"""
import numpy as np

SEED = 20260606
rng = np.random.default_rng(SEED)


def symplectic_gram(B, n):
    """Gram matrix G_ij = Ω(col_i, col_j) over F₂, with the (top n | bottom n) split."""
    top = B[:n, :]            # x-half  (n × ℓ)
    bot = B[n:, :]            # z-half  (n × ℓ)
    # Ω(col_i,col_j) = top_i·bot_j + bot_i·top_j  = (topᵀbot + botᵀtop)_{ij}
    G = (top.T @ bot + bot.T @ top) % 2
    return G


def gf2_rank(M):
    M = (M % 2).astype(np.int8).copy()
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        piv = np.where(M[r:, c])[0]
        if len(piv) == 0:
            continue
        p = r + piv[0]
        M[[r, p]] = M[[p, r]]
        mask = M[:, c].copy()
        mask[r] = 0
        M[mask == 1] ^= M[r]
        r += 1
        if r == rows:
            break
    return r


def gf2_solve(A, b):
    """one solution x of A x = b over F₂ (A: m×k, b: m), or None if inconsistent."""
    A = (A % 2).astype(np.int8).copy()
    b = (b % 2).astype(np.int8).copy()
    m, k = A.shape
    aug = np.concatenate([A, b.reshape(-1, 1)], axis=1)
    pivots = []
    r = 0
    for c in range(k):
        piv = np.where(aug[r:, c])[0]
        if len(piv) == 0:
            continue
        p = r + piv[0]
        aug[[r, p]] = aug[[p, r]]
        mask = aug[:, c].copy()
        mask[r] = 0
        aug[mask == 1] ^= aug[r]
        pivots.append(c)
        r += 1
        if r == m:
            break
    # consistency: any row with all-zero A-part but nonzero b is inconsistent
    for i in range(r, m):
        if aug[i, :k].sum() == 0 and aug[i, k] == 1:
            return None
    x = np.zeros(k, dtype=np.int8)
    for i, c in enumerate(pivots):
        x[c] = aug[i, k]
    return x


def random_symmetric(ell, rng):
    U = rng.integers(0, 2, size=(ell, ell)).astype(np.int8)
    S = np.triu(U)
    S = (S + S.T) % 2
    np.fill_diagonal(S, U.diagonal())     # keep diagonal free
    return S


def complete_one(n, ell, b, rng):
    """one symplectic-completion trial. Returns (ok_iso, full_rank, S_matches, embed_ok)."""
    a = n - b
    N1 = rng.integers(0, 2, size=(a, ell)).astype(np.int8) if a > 0 else np.zeros((0, ell), np.int8)
    N2 = rng.integers(0, 2, size=(a, ell)).astype(np.int8) if a > 0 else np.zeros((0, ell), np.int8)
    # M must have full column rank ℓ so Mᵀ A' = T is solvable for every T
    while True:
        M = rng.integers(0, 2, size=(b, ell)).astype(np.int8)
        if gf2_rank(M) == ell:
            break
    Sprime = random_symmetric(ell, rng)               # target symmetric S
    T = (Sprime - (N1.T @ N2)) % 2                     # solve Mᵀ A' = T, column by column
    Mt = M.T                                           # ℓ × b
    Acols = []
    for j in range(ell):
        x = gf2_solve(Mt, T[:, j])
        if x is None:
            return None
        Acols.append(x)
    Aprime = np.array(Acols, dtype=np.int8).T          # b × ℓ
    B = np.concatenate([N1, M, N2, Aprime], axis=0) % 2   # 2n × ℓ

    G = symplectic_gram(B, n)
    ok_iso = bool((G == 0).all())                      # all columns symplectically orthogonal
    full_rank = (gf2_rank(B) == ell)
    S = (N1.T @ N2 + M.T @ Aprime) % 2
    S_matches = bool((S == Sprime).all())              # Eq 1.4 holds with the intended S
    top = np.concatenate([N1, M, N2], axis=0) % 2      # the given (LPN) data
    embed_ok = bool((B[: 2 * n - b, :] == top).all())  # embedded verbatim in top 2n-b rows
    return ok_iso, full_rank, S_matches, embed_ok


def main():
    print("=" * 76)
    print("Lane C4 — symplectic-completion engine of Thm 1.6 Stage 1 (LPN → sympLPN)")
    print(f"seed={SEED}  (verbatim Eq 1.3–1.4, 2509.20697 §1.2.3)")
    print("=" * 76)
    print(f"\n  {'n':>2} {'ℓ':>2} {'b=(1+ε)ℓ':>9} {'a=n-b':>6} {'trials':>7} "
          f"{'isotropic':>10} {'full-rank':>10} {'S=Sym':>7} {'embed':>7}")
    TR = 200
    for (n, ell, b) in [(3, 2, 3), (5, 2, 3), (6, 4, 5), (8, 4, 6), (10, 6, 7)]:
        if n - b < 0:
            continue
        iso = fr = sm = emb = 0
        done = 0
        for _ in range(TR):
            res = complete_one(n, ell, b, rng)
            if res is None:
                continue
            done += 1
            iso += res[0]
            fr += res[1]
            sm += res[2]
            emb += res[3]
        frac = lambda x: f"{x}/{done}"
        print(f"  {n:>2} {ell:>2} {b:>9} {n-b:>6} {done:>7} "
              f"{frac(iso):>10} {frac(fr):>10} {frac(sm):>7} {frac(emb):>7}")
        assert iso == done and fr == done and sm == done and emb == done, "completion failed"

    print("\n  All trials: B is isotropic (every column pair symplectically orthogonal),")
    print("  full column rank, S = N1ᵀN2 + MᵀA' is exactly the intended symmetric S' (Eq 1.4),")
    print("  and the given matrix [N1;M;N2] is embedded VERBATIM in the top 2n−b rows of B.")
    print("  => the symplectic-completion ENGINE of the LPN→sympLPN reduction (Stage 1) is")
    print("     verified: an arbitrary matrix is turned into a symplectically-orthogonal")
    print("     (isotropic) sympLPN matrix while its rows are preserved intact -- the")
    print("     structural basis of LPN ↪ LSN. (NOT a reimplementation of the §§5–6 secret-")
    print("     preservation map; that stays deferred. Evidence for LSN⊇LPN, not a 7th proof.)")


if __name__ == "__main__":
    main()
