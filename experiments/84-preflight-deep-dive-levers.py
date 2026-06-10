"""
84 — Pre-flight verification of the deep-dive-plan-v2 levers (Claude, supervisor).
Run BEFORE handing the plan to Kimi: the plan's load-bearing identities must be true.

 [A3] Relation transport (full-rank linear reductions, all m):
      B in F2^{m x 2n} with rank 2n, B+ a left inverse, M := (B+)^T Omega B+.
      Then (BA)^T M (BA) = A^T Omega A = S_A = 0 identically for isotropic-column A.
      Verified 30/30 random (B, A) at n=3, m in {2n, 2n+2, 2n+5, 6n}.
      Detector false-positive on uniform C: ~2^{-C(n,2)} (n=3: ~1/8 observed 315/2000;
      n=65: 2^{-2080}) — the constraint count is exactly the isotropy count C(n,2).
 [A5] Dilution identity: Pr[a in L | b=1] = (1-p)2^{-n} / (p + (1-2p)2^{-n})
      (exact 3/10 at n=3, p=1/4; asymptotically ((1-p)/p) 2^{-n} = 3*2^{-n}).
      Each true positive (u,v) in graph(S) gives v = Su: n linear equations in the
      n(n+1)/2 Siegel-chart unknowns (identity; the basis of the diluted-LPN view).

No 7th; no break; no security claim. OPEN = LSN.
"""
import random
from fractions import Fraction

n = 3; D = 2 * n
Om = [[0] * D for _ in range(D)]
for i in range(n):
    Om[i][i + n] = 1; Om[i + n][i] = 1

def matmul(X, Y, p, q, r):
    return [[sum(X[i][k] * Y[k][j] for k in range(q)) % 2 for j in range(r)] for i in range(p)]
def transpose(X):
    return [list(r) for r in zip(*X)]
def rank(M_, rows, cols):
    A = [r[:] for r in M_]; piv = 0
    for c in range(cols):
        r_ = next((r for r in range(piv, rows) if A[r][c]), None)
        if r_ is None: continue
        A[piv], A[r_] = A[r_], A[piv]
        for rr in range(rows):
            if rr != piv and A[rr][c]:
                A[rr] = [x ^ y for x, y in zip(A[rr], A[piv])]
        piv += 1
    return piv
def left_inverse(B, m):
    BT = transpose(B)
    A = [BT[i][:] + [1 if j == i else 0 for j in range(D)] for i in range(D)]
    piv = 0; pivcols = []
    for c in range(m):
        r_ = next((r for r in range(piv, D) if A[r][c]), None)
        if r_ is None: continue
        A[piv], A[r_] = A[r_], A[piv]
        for rr in range(D):
            if rr != piv and A[rr][c]:
                A[rr] = [x ^ y for x, y in zip(A[rr], A[piv])]
        pivcols.append(c); piv += 1
        if piv == D: break
    assert piv == D
    Y = [[0] * D for _ in range(m)]
    for k, c in enumerate(pivcols):
        for j in range(D): Y[c][j] = A[k][m + j]
    return transpose(Y)

random.seed(3)
ok_all = True
for trial in range(30):
    m = random.choice([D, D + 2, D + 5, 3 * D])
    while True:
        B = [[random.randint(0, 1) for _ in range(D)] for _ in range(m)]
        if rank(B, m, D) == D: break
    Bp = left_inverse(B, m)
    I = matmul(Bp, B, D, m, D)
    assert all(I[i][j] == (1 if i == j else 0) for i in range(D) for j in range(D))
    M = matmul(matmul(transpose(Bp), Om, m, D, D), Bp, m, D, m)
    S = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = random.randint(0, 1); S[i][j] = v; S[j][i] = v
    cols = []
    for _ in range(n):
        u = [random.randint(0, 1) for _ in range(n)]
        v = [sum(S[i][j] * u[j] for j in range(n)) % 2 for i in range(n)]
        cols.append(u + v)
    A = transpose(cols)
    SA = matmul(matmul(transpose(A), Om, n, D, D), A, n, D, n)
    assert all(SA[i][j] == 0 for i in range(n) for j in range(n))
    BA = matmul(B, A, m, D, n)
    out = matmul(matmul(transpose(BA), M, n, m, m), BA, n, m, n)
    ok_all &= all(out[i][j] == 0 for i in range(n) for j in range(n))
print("[A3] full-rank transport (BA)^T M (BA) = 0, 30 random (B,A):", ok_all)
assert ok_all

m = 3 * D
while True:
    B = [[random.randint(0, 1) for _ in range(D)] for _ in range(m)]
    if rank(B, m, D) == D: break
Bp = left_inverse(B, m)
M = matmul(matmul(transpose(Bp), Om, m, D, D), Bp, m, D, m)
hits = 0; T = 2000
for _ in range(T):
    C = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    out = matmul(matmul(transpose(C), M, n, m, m), C, n, m, n)
    hits += all(out[i][j] == 0 for i in range(n) for j in range(n))
print(f"[A3] detector false-positive on uniform C: {hits}/{T} (expect ~2^-C(n,2) = 1/8 at n=3)")

p = Fraction(1, 4)
num = (1 - p) * Fraction(1, 2 ** n); den = p + (1 - 2 * p) * Fraction(1, 2 ** n)
print(f"[A5] dilution Pr[a in L | b=1] = {num/den} (exact at n=3) ~ ((1-p)/p)2^-n asymptotically")
assert num / den == Fraction(3, 10)
print("All pre-flight checks passed.")
