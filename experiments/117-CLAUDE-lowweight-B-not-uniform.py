"""
117 — Claude check: Kimi's E-OP9a (b2a2671) claims bottom_w1 B is a marginal-uniform counterexample
to the eff-noise lemma (entropy_ratio~0.99, p_eff=1/4). But that entropy is PER-ROW, not JOINT.
This shows the output C=BA is DETERMINISTICALLY SYMMETRIC (C=M=M^T), hence NOT marginally uniform
(uniform m x n matrix has symmetric core w.p. 2^{-n(n-1)/2}). So bottom_w1 VIOLATES joint
marginal-uniformity => it is NOT a counterexample; the low-weight <-> uniformity CONFLICT holds
(Claude recon) => supports closure, not refutation.
No 7th; no break; no security claim. OPEN = LSN.
"""
import random
random.seed(2)
def iso_A(n):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = random.randint(0,1); M[i][j] = v; M[j][i] = v
    A = [[(1 if (r<n and r==c) else (M[r-n][c] if r>=n else 0)) for c in range(n)] for r in range(2*n)]
    return A, M
for n in [6, 8, 10]:
    sym = 0; T = 200
    for _ in range(T):
        A, M = iso_A(n)
        C = [A[n + (i % n)][:] for i in range(4*n)]      # bottom_w1: c_i = A[n+j] = M[j]
        core = C[:n]
        sym += all(core[i][j] == core[j][i] for i in range(n) for j in range(n))
    print(f"n={n}: bottom_w1 output C symmetric (C=M^T) in {sym}/{T} trials "
          f"(uniform would be ~2^-{n*(n-1)//2})")
print("C always symmetric => detectably NON-uniform => bottom_w1 not a valid marginal-uniform B.")
