r"""
Lane C — verify the Appendix-D entropy-deficiency that underlies `LSN ⊀ LPN` (linear).

The `sympLPN ⊀ LPN` linear barrier (2603.19110 §2.4 / Appendix D) rests on Thm D.1:
the sympLPN matrix A ∈ F₂^{2n×n} is *isotropic* (its n columns are pairwise symplectically
orthogonal and jointly full rank), so it carries only ≈ (3/2)n² bits of entropy versus the
2n² bits a uniform 2n×n matrix carries. The n²/2 symplectic-orthogonality conditions make
A deficient by a CONSTANT factor d → 1/4, i.e. H(A) ≈ (1−d)·(uniform) with d→1/4 — so no
fixed linear B can smooth A to uniform (an LPN matrix) without the error blow-up of Thm
D.2. This script verifies that entropy count exactly.

Two independent confirmations:
  (1) brute-force count of full-rank isotropic frames for n=1,2,3 (enumerate all 2n×n
      F₂ matrices, keep those with pairwise-Ω-orthogonal, independent columns);
  (2) the closed form  N(n) = ∏_{k=1}^n (2^{2n-k+1} − 2^{k-1})
      (column a_k: orthogonal to the k−1 previous (a 2n−k+1-dim space) but outside their
       span (2^{k-1} vectors, which is itself isotropic ⊆ its own ⊥)).
Then log2 N(n) vs 2n² (uniform) and the deficiency d(n) = 1 − log2 N(n) / (2n²) → 1/4.

Run: python3 17-appendixD-entropy-deficiency.py
"""
import math
from itertools import product


def omega_int(u, v, n):
    """symplectic form Ω(u,v) on F₂^{2n}, vectors as bit-packed ints (low n | high n)."""
    mask = (1 << n) - 1
    ul, uh = u & mask, (u >> n) & mask
    vl, vh = v & mask, (v >> n) & mask
    return ((ul & vh).bit_count() + (uh & vl).bit_count()) & 1


def gf2_independent(cols):
    """are these bit-packed-int vectors F₂-linearly independent? (XOR basis)."""
    piv = {}
    for v in cols:
        x = v
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                break
        else:
            return False           # reduced to 0 -> dependent
    return True


def brute_count(n):
    """exact count of ordered full-rank isotropic n-frames in F₂^{2n} (n<=3 only)."""
    D = 2 * n
    vecs = range(1, 1 << D)            # nonzero column vectors
    count = 0
    for cols in product(vecs, repeat=n):
        # pairwise symplectic-orthogonality
        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                if omega_int(cols[i], cols[j], n) != 0:
                    ok = False
                    break
            if not ok:
                break
        if ok and gf2_independent(cols):
            count += 1
    return count


def formula_count(n):
    """N(n) = ∏_{k=1}^n (2^{2n-k+1} - 2^{k-1})."""
    N = 1
    for k in range(1, n + 1):
        N *= (1 << (2 * n - k + 1)) - (1 << (k - 1))
    return N


def main():
    print("=" * 74)
    print("Lane C — Appendix-D entropy deficiency of the sympLPN isotropic matrix A")
    print("=" * 74)

    print("\n[1] brute-force vs closed form  N(n) = ∏ (2^{2n-k+1} - 2^{k-1})")
    print(f"  {'n':>2} {'brute count':>14} {'formula N(n)':>14} {'match':>6}")
    for n in [1, 2, 3]:
        b = brute_count(n)
        f = formula_count(n)
        print(f"  {n:>2} {b:>14} {f:>14} {'OK' if b == f else 'MISMATCH':>6}")
        assert b == f, f"formula disagrees with brute force at n={n}"

    print("\n[2] entropy deficiency: log2 N(n) vs uniform 2n^2 bits;  d(n)=1-log2N/(2n^2)")
    print(f"  {'n':>3} {'log2 N(n)':>11} {'uniform 2n^2':>13} "
          f"{'~(3/2)n^2+n/2':>14} {'deficiency d':>13}")
    for n in [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]:
        N = formula_count(n)
        lg = math.log2(N)
        uniform = 2 * n * n
        approx = 1.5 * n * n + 0.5 * n
        d = 1 - lg / uniform
        print(f"  {n:>3} {lg:>11.2f} {uniform:>13} {approx:>14.1f} {d:>12.4f}")

    print("\n  => log2 N(n) tracks (3/2)n^2 + n/2 (leading (3/2)n^2), NOT the uniform 2n^2.")
    print("     deficiency d(n) -> 1/4 = 0.25 (a CONSTANT factor), exactly the Thm D.1")
    print("     '(1-d)mn with constant d'. The n^2/2 symplectic-orthogonality conditions")
    print("     are real and irremovable: a fixed linear B cannot smooth A to a uniform")
    print("     (LPN) matrix -- which, with the Thm D.2 error blow-up past the Shannon")
    print("     converse, is the information-theoretic core of `sympLPN ⊀ LPN` (linear).")

    # sanity: the count of isotropic n-frames should also factor through the number of
    # Lagrangian subspaces L(n) = ∏_{i=1}^n (2^i + 1), times ordered bases per subspace.
    print("\n[3] cross-check via Lagrangian-subspace count  L(n) = ∏_{i=1}^n (2^i + 1):")
    print(f"  {'n':>2} {'#Lagrangians':>14} {'#ordered bases/L':>17} "
          f"{'product':>16} {'= N(n)?':>8}")
    for n in [1, 2, 3, 4]:
        Ln = 1
        for i in range(1, n + 1):
            Ln *= (1 << i) + 1
        # ordered bases of an n-dim F₂ space: ∏_{j=0}^{n-1}(2^n - 2^j)
        bases = 1
        for j in range(n):
            bases *= (1 << n) - (1 << j)
        prod = Ln * bases
        N = formula_count(n)
        print(f"  {n:>2} {Ln:>14} {bases:>17} {prod:>16} {'OK' if prod == N else 'NO':>8}")
        assert prod == N, f"Lagrangian factorization disagrees at n={n}"

    print("\n  Both independent counts agree with N(n): the entropy deficiency is exact.")
    print("  VERDICT: Appendix-D Thm D.1 entropy deficiency CONFIRMED computationally")
    print("  (d -> 1/4). This is the verifiable mechanism behind the linear `LSN ⊀ LPN`")
    print("  separation -- evidence for, not proof of, the (open) any-reduction question.")


if __name__ == "__main__":
    main()
