"""
91 — Reachability-set R_w counting probe (§1b any-B counting theorem).

For A ∈ F2^{D×n} isotropic basis (D=2n), define
    R_w(A) = {c ∈ F2^n : ∃b ∈ F2^D, |b| ≤ w, b^T A = c}.
Upper bound (A-independent): |R_w| ≤ Σ_{j=0}^w C(D, j).

Probe: for random isotropic A, compute exact |R_w(A)| by enumeration and compare
to the binomial bound.  Also measure: if BA is δ-close to uniform, what fraction
of rows are forced to have weight > w?

The critical threshold w* solves Σ_{j=0}^{w*} C(D,j) / 2^n = 2^{-Θ(n)}.
At w = 0.19n, the mass is ≈ 2^{-0.19n} (verified: n=64 → 1.4e-3, n=128 → 1.1e-5).

Output: JSON with exact counts + threshold table.  No 7th; no break; no security claim.
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
    """b^T A where b is D-vector, A is D×n."""
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
    return cols  # list of n column vectors, each length D

def compute_Rw(A, w):
    """Exact enumeration of R_w(A) = {b^T A : |b| ≤ w}."""
    D = len(A)
    n = len(A[0])
    R = set()
    # Enumerate all b with weight ≤ w
    # For small D (≤ 16), full enumeration is feasible
    for mask in range(1 << D):
        if bin(mask).count('1') > w:
            continue
        b = [(mask >> i) & 1 for i in range(D)]
        c = tuple(matmul_vec(b, A))
        R.add(c)
    return R

def binomial_bound(D, w):
    return sum(comb(D, j) for j in range(w + 1))

def main():
    results = []
    for n in [4, 5, 6, 7, 8]:
        D = 2 * n
        print(f"\nn={n}, D={D}")
        # Test a few random isotropic A
        for trial in range(3):
            A = sample_isotropic_basis(D, n)
            for w in range(1, D + 1):
                R = compute_Rw(A, w)
                bound = binomial_bound(D, w)
                ratio = len(R) / (2 ** n)
                bound_ratio = bound / (2 ** n)
                if w == int(0.19 * n) or w == int(0.19 * n) + 1:
                    print(f"  trial={trial}, w={w}: |R|={len(R)}, bound={bound}, "
                          f"ratio={ratio:.6f}, bound_ratio={bound_ratio:.6f}")
                results.append({
                    "n": n,
                    "trial": trial,
                    "w": w,
                    "|R|": len(R),
                    "bound": bound,
                    "ratio": ratio,
                    "bound_ratio": bound_ratio,
                })

    # Threshold table: find w where bound_ratio first drops below various targets
    print("\n--- Threshold table (bound_ratio = Σ_{j≤w} C(2n,j) / 2^n) ---")
    print(f"{'n':>3} {'w':>3} {'bound_ratio':>12} {'target=2^{-0.19n}':>16} {'target=2^{-0.1n}':>16}")
    for n in [4, 5, 6, 7, 8, 16, 32, 64, 128]:
        D = 2 * n
        target1 = 2 ** (-0.19 * n)
        target2 = 2 ** (-0.1 * n)
        for w in range(D + 1):
            br = sum(comb(D, j) for j in range(w + 1)) / (2 ** n)
            if br <= target1:
                print(f"{n:>3} {w:>3} {br:>12.6e} {target1:>16.6e} {target2:>16.6e}")
                break

    with open("experiments/91-reachability-set-results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiments/91-reachability-set-results.json")

if __name__ == "__main__":
    main()
