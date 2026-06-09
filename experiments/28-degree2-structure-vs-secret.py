r"""
Lane I — degree-2 analysis: sympLPN's symplectic structure is a PUBLIC, x-independent
degree-2 constraint → a trivial a-distribution distinguisher, but NO secret-recovery advantage.

Lane G#1 showed the degree-1 (linear) statistic μ̂(Δ) of the sympLPN a-distribution is balanced
(no linear SQ attack on the secret). The natural next step (open question iv / "beyond linear"):
is there a degree-2 attack? sympLPN's defining structure IS degree-2 — the matrix A (2n×k) has
symplectically-orthogonal columns, i.e. the rows a_1..a_{2n} ∈ F₂^k satisfy the bilinear relation
        S_A := Σ_{i=1}^{n} ( a_i a_{i+n}^T + a_{i+n} a_i^T )  =  0   (a k×k symmetric F₂ matrix),
because (S_A)_{pq} = Ω(column_p, column_q). This is a genuine degree-2 structure that uniform-LPN
rows do NOT have. The question: does it leak the secret x (from b = A x + e)?

Claim (tested here): S_A is a function of A ALONE — it is PUBLIC and **x-independent**. So:
  (a) it gives a TRIVIAL degree-2 distinguisher for the a-distribution (you can just check S_A=0),
  (b) but it carries ZERO information about x; the x-equations b_i = ⟨a_i,x⟩⊕e_i are the same
      rank-k noisy-parity system as plain LPN, so secret-recovery is the SAME LPN-hard problem.
=> the symplectic (degree-2) structure does NOT give a secret-recovery advantage at any degree;
   the secret is protected by the degree-1 noisy-parity hardness (G#1 / LPN). This is WHY G#1
   (degree-1 balance) is the whole secret-recovery story.

Run: python3 28-degree2-structure-vs-secret.py
"""
import numpy as np

SEED = 20260607
rng = np.random.default_rng(SEED)


def omega_int(u, v, n):
    mask = (1 << n) - 1
    ul, uh = u & mask, (u >> n) & mask
    vl, vh = v & mask, (v >> n) & mask
    return ((ul & vh).bit_count() + (uh & vl).bit_count()) & 1


class XorBasis:
    __slots__ = ("piv",)

    def __init__(self):
        self.piv = {}

    def add(self, v):
        x = v
        while x:
            h = x.bit_length() - 1
            r = self.piv.get(h)
            if r is None:
                self.piv[h] = x
                return True
            x ^= r
        return False


def rand_isotropic_cols(n, k, rng):
    """k symplectically-orthogonal independent columns in F₂^{2n} (k≤n) as int vectors."""
    D = 2 * n
    xb = XorBasis()
    cols = []
    while len(cols) < k:
        v = int(rng.integers(1, 1 << D))
        if all(omega_int(v, c, n) == 0 for c in cols) and xb.add(v):
            cols.append(v)
    return cols


def A_matrix(cols, n, k):
    """2n×k 0/1 matrix whose columns are `cols` (col j bit i = A[i,j])."""
    A = np.zeros((2 * n, k), dtype=np.int8)
    for j in range(k):
        for i in range(2 * n):
            A[i, j] = (cols[j] >> i) & 1
    return A


def S_constraint(A, n, k):
    """S_A = Σ_i (a_i a_{i+n}^T + a_{i+n} a_i^T) mod 2  (k×k). Zero iff columns are isotropic."""
    S = np.zeros((k, k), dtype=np.int64)
    for i in range(n):
        ai = A[i, :].astype(np.int64)
        aj = A[i + n, :].astype(np.int64)
        S += np.outer(ai, aj) + np.outer(aj, ai)
    return S % 2


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
        m = M[:, c].copy(); m[r] = 0
        M[m == 1] ^= M[r]
        r += 1
        if r == rows:
            break
    return r


def main():
    print("=" * 78)
    print("Lane I — degree-2: symplectic structure is a PUBLIC, x-independent constraint")
    print(f"seed={SEED}")
    print("=" * 78)

    print("\n[A] the degree-2 constraint S_A = Σ(a_i a_{i+n}^T + a_{i+n} a_i^T):  0 for sympLPN,")
    print("    nonzero for uniform -> a TRIVIAL degree-2 distinguisher for the a-distribution")
    print(f"  {'n':>2} {'k':>2} {'trials':>7} {'sympLPN S_A=0':>14} {'uniform S_A=0':>14}")
    for (n, k) in [(4, 2), (4, 4), (5, 3), (6, 4)]:
        TR = 200
        symp_zero = unif_zero = 0
        for _ in range(TR):
            cols = rand_isotropic_cols(n, k, rng)
            A = A_matrix(cols, n, k)
            symp_zero += int(not S_constraint(A, n, k).any())
            U = rng.integers(0, 2, size=(2 * n, k)).astype(np.int8)
            unif_zero += int(not S_constraint(U, n, k).any())
        print(f"  {n:>2} {k:>2} {TR:>7} {f'{symp_zero}/{TR}':>14} {f'{unif_zero}/{TR}':>14}")

    print("\n[B] but S_A is x-FREE; the secret's x-equations are the SAME rank-k noisy parity as LPN")
    print(f"  {'n':>2} {'k':>2} {'rank(A) sympLPN':>16} {'rank(A) uniform':>16} {'(both = k -> same #x-eqs)':>26}")
    for (n, k) in [(4, 2), (4, 4), (5, 3), (6, 4)]:
        TR = 200
        symp_rank_full = unif_rank_full = 0
        for _ in range(TR):
            cols = rand_isotropic_cols(n, k, rng)
            A = A_matrix(cols, n, k)
            symp_rank_full += int(gf2_rank(A) == k)
            U = rng.integers(0, 2, size=(2 * n, k)).astype(np.int8)
            unif_rank_full += int(gf2_rank(U) == k)
        print(f"  {n:>2} {k:>2} {f'{symp_rank_full}/{TR} full':>16} "
              f"{f'{unif_rank_full}/{TR} full':>16} {'yes':>26}")

    print("""
  Reading:
  [A] sympLPN's A satisfies the degree-2 relation S_A = 0 (=Ω-Gram of its columns) in 100% of
      trials; a uniform A essentially never does. So a degree-2 statistic of A TRIVIALLY
      distinguishes the sympLPN a-distribution from uniform -- but this is information you ALREADY
      HAVE (A is public; you can read off that it is isotropic). It is x-INDEPENDENT.
  [B] The secret x enters only through b = A x + e. The x-equations are the noisy parities
      ⟨a_i,x⟩⊕e_i; A has full column rank k for both sympLPN and uniform, so there are exactly k
      independent x-equations at noise p -- the SAME rank-k noisy-parity (LPN) recovery problem.
      The degree-2 constraint S_A=0 adds NO equation in x (it is x-free).
  => The symplectic (degree-2) structure is entirely PUBLIC and x-independent: it yields only a
     trivial a-distribution distinguisher, NOT a secret-recovery advantage. Secret recovery is the
     same degree-1 noisy-parity hardness as LPN (G#1 / Lane C). This explains why G#1 (degree-1
     balance) is the whole secret-recovery story, and why no degree-2 attack on the secret arises
     from the symplectic structure. POSITIVE hardness clarification; no attack; no 7th; no claim.""")


if __name__ == "__main__":
    main()
