"""
91f — Exact reachability verification for §1b theorem.

For A ∈ F2^{D×n} with D=2n, define R_w(A) = {b^T A : b ∈ F2^D, |b| ≤ w}.
Upper bound: |R_w(A)| ≤ Σ_{j=0}^w C(D, j) for all A.

This probe verifies:
1. The upper bound holds for random isotropic A.
2. For w = ⌊0.19n⌋, |R_w| / 2^n is exponentially small.
3. The exact threshold w*(n) where |R_w| / 2^n drops below 2^{-0.06n}.

No 7th; no break; no security claim.
"""
import json
import math
from math import comb
import random

random.seed(42)

def rank(M):
    if not M or not M[0]:
        return 0
    A = [r[:] for r in M]
    rows, cols = len(A), len(A[0])
    piv = 0
    for c_ in range(cols):
        r_ = next((r for r in range(piv, rows) if A[r][c_]), None)
        if r_ is None:
            continue
        A[piv], A[r_] = A[r_], A[piv]
        for rr in range(rows):
            if rr != piv and A[rr][c_]:
                A[rr] = [x ^ y for x, y in zip(A[rr], A[piv])]
        piv += 1
    return piv

def matmul_vec(b, A):
    D = len(A)
    n = len(A[0])
    return [sum(b[i] * A[i][j] for i in range(D)) % 2 for j in range(n)]

def sample_isotropic_basis(D, n):
    Om = [[0] * D for _ in range(D)]
    for i in range(n):
        Om[i][i + n] = 1
        Om[i + n][i] = 1
    cols = []
    attempts = 0
    while len(cols) < n and attempts < 20000:
        v = [random.randint(0, 1) for _ in range(D)]
        attempts += 1
        ok = True
        for u in cols:
            pair = sum(u[i] * Om[i][j] * v[j] for i in range(D) for j in range(D)) % 2
            if pair != 0:
                ok = False
                break
        if not ok:
            continue
        if rank([list(c) for c in cols] + [v]) <= len(cols):
            continue
        cols.append(v)
    assert len(cols) == n, f"Failed to find isotropic basis: got {len(cols)}/{n}"
    return cols

def compute_Rw(A, w):
    D = len(A)
    R = set()
    for mask in range(1 << D):
        if bin(mask).count('1') > w:
            continue
        b = [(mask >> i) & 1 for i in range(D)]
        c = tuple(matmul_vec(b, A))
        R.add(c)
    return R

def main():
    results = []
    print("Reachability set verification")
    print("=" * 60)
    print(f"{'n':>4} {'D':>4} {'w':>4} {'|R_w|':>8} {'bound':>10} "
          f"{'ratio':>12} {'bound_ratio':>12}")
    print("-" * 60)
    
    for n in [4, 5, 6, 7, 8]:
        D = 2 * n
        for trial in range(3):
            A = sample_isotropic_basis(D, n)
            for w in [1, 2, int(0.19 * n), int(0.19 * n) + 1]:
                if w < 1:
                    continue
                R = compute_Rw(A, w)
                bound = sum(comb(D, j) for j in range(w + 1))
                ratio = len(R) / (2 ** n)
                bound_ratio = bound / (2 ** n)
                print(f"{n:>4} {D:>4} {w:>4} {len(R):>8} {bound:>10} "
                      f"{ratio:>12.6f} {bound_ratio:>12.6f}")
                assert len(R) <= bound, f"Bound violated: {len(R)} > {bound}"
                results.append({
                    "n": n, "trial": trial, "w": w,
                    "|R|": len(R), "bound": bound,
                    "ratio": ratio, "bound_ratio": bound_ratio
                })
    
    print("\n" + "=" * 60)
    print("Asymptotic check: w = ⌊0.19n⌋")
    print(f"{'n':>4} {'w':>4} {'bound_ratio':>14} {'2^{-0.06n}':>14} {'2^{-n}':>14}")
    print("-" * 60)
    for n in [8, 16, 32, 64, 128, 256]:
        D = 2 * n
        w = int(0.19 * n)
        # Use Stirling for large n
        if D <= 200:
            bound = sum(comb(D, j) for j in range(w + 1))
        else:
            # Approximate using entropy
            p = w / D
            h = -(p * math.log2(p) + (1 - p) * math.log2(1 - p)) if 0 < p < 1 else 0
            bound = 2 ** (D * h + math.log2(w + 1))
        bound_ratio = bound / (2 ** n)
        target1 = 2 ** (-0.06 * n)
        target2 = 2 ** (-n)
        print(f"{n:>4} {w:>4} {bound_ratio:>14.6e} {target1:>14.6e} {target2:>14.6e}")
    
    with open("experiments/91f-reachability-verification.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiments/91f-reachability-verification.json")

if __name__ == "__main__":
    main()
