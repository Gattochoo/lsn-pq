r"""
Lane G (#1) — SQ / statistical-dimension POSITIVE-evidence ingredient for sympLPN.

The program's evidence is mostly no-go (specific decoders fail). This adds the standard
*positive* hardness ingredient against the broad STATISTICAL-QUERY (SQ) class. For a noisy-
linear problem "learn x from (a, ⟨a,x⟩⊕e)" with a-distribution μ, the SQ-hardness is governed
by the pairwise correlation of the secret-conditional distributions:
        Cor(x, x') = (1−2p)² · μ̂(x⊕x'),   μ̂(Δ) = E_{a~μ}[(−1)^{⟨a,Δ⟩}]   (the Fourier bias of μ).
SQ algorithms need ≳ 1/max_{Δ≠0}|Cor| queries (statistical-dimension lower bound). For UNIFORM
a (plain LPN), μ̂(Δ)=0 for Δ≠0 — maximal SQ-hardness. The question for sympLPN: does the
symplectic structure on a (rows of a matrix A with symplectically-orthogonal COLUMNS) bias μ —
creating a Δ with large μ̂(Δ) (an SQ attack) — or stay balanced (SQ-hard like LPN)?

This computes max_{Δ≠0}|μ̂(Δ)| for the sympLPN a-distribution and compares to uniform LPN.
Honest scope: this is the per-sample MARGINAL SQ ingredient (the full SQ analysis would also
account for within-matrix row correlations); a balanced marginal is the primary positive
indicator, an imbalanced one would be a concrete SQ attack.

Run: python3 25-sq-statistical-dimension.py
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


def rand_isotropic_frame(n, k, rng):
    """k symplectically-orthogonal, independent columns in F₂^{2n} (k≤n)."""
    D = 2 * n
    xb = XorBasis()
    cols = []
    while len(cols) < k:
        v = int(rng.integers(1, 1 << D))
        if all(omega_int(v, c, n) == 0 for c in cols) and xb.add(v):
            cols.append(v)
    return cols                                  # k ints (columns), each a 2n-bit vector


def rows_of(cols, n, k):
    """rows of the 2n×k matrix A whose columns are `cols`; row i ∈ F₂^k."""
    rows = []
    for i in range(2 * n):
        r = 0
        for j in range(k):
            r |= ((cols[j] >> i) & 1) << j
        rows.append(r)
    return rows


def fourier_bias(row_ints, k):
    """max_{Δ≠0} |E[(-1)^{<row,Δ>}]| over pooled rows."""
    R = np.array(row_ints, dtype=np.int64)
    best = 0.0
    argbest = 0
    for Delta in range(1, 1 << k):
        ip = np.array([(int(r) & Delta).bit_count() & 1 for r in R])
        b = abs(np.mean(1 - 2 * ip))            # E[(-1)^{<r,Δ>}]
        if b > best:
            best = b
            argbest = Delta
    return best, argbest


def main():
    print("=" * 76)
    print("Lane G (#1) — SQ statistical-dimension ingredient: Fourier bias of the sympLPN")
    print("a-distribution vs uniform LPN  (small bias => SQ-hard like LPN)")
    print(f"seed={SEED}")
    print("=" * 76)
    print(f"\n  {'n':>2} {'k':>2} {'#A mats':>8} {'#rows':>7} "
          f"{'sympLPN max|μ̂(Δ)|':>18} {'uniform-LPN max|μ̂|':>19} {'sampling ~1/√#rows':>19}")
    for (n, k) in [(4, 2), (4, 3), (4, 4), (5, 3), (6, 3), (6, 4)]:
        NA = 4000
        symp_rows = []
        for _ in range(NA):
            cols = rand_isotropic_frame(n, k, rng)
            symp_rows.extend(rows_of(cols, n, k))
        unif_rows = [int(rng.integers(0, 1 << k)) for _ in range(len(symp_rows))]
        sb, sd = fourier_bias(symp_rows, k)
        ub, _ = fourier_bias(unif_rows, k)
        samp = 1.0 / np.sqrt(len(symp_rows))
        print(f"  {n:>2} {k:>2} {NA:>8} {len(symp_rows):>7} "
              f"{sb:>18.4f} {ub:>19.4f} {samp:>19.4f}")

    print("\n  Reading: if the sympLPN max|μ̂(Δ)| is on the order of the uniform-LPN value and of")
    print("  the sampling floor 1/√#rows (i.e. NO Δ stands out), then the symplectic structure")
    print("  does NOT bias the a-distribution -> the secret-pairwise correlation (1−2p)²μ̂(Δ)")
    print("  stays exponentially small like LPN -> sympLPN inherits LPN's SQ lower bound")
    print("  (statistical-query algorithms need ≳ exp many queries). That is POSITIVE hardness")
    print("  evidence against the broad SQ class -- complementary to the decoder no-go results.")
    print("  If instead some Δ had bias ≫ sampling floor, that Δ would be a concrete SQ attack")
    print("  (≈0; would be escalated). Honest scope: per-sample marginal ingredient, not a full")
    print("  SQ proof (within-matrix row correlations not modeled). No 7th; no security claim.")


if __name__ == "__main__":
    main()
