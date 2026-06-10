"""
93 — M1 entropy-support bound verification.

For random isotropic A and random B, measures:
  1. SD(BA, Uniform) — actual uniformity gap
  2. k = number of rows with |b_i| ≤ w (w = floor(0.19n))
  3. M1 bound: k_bound = ((3/2)n^2 + n/2 + delta*m*n + 1) / (0.094*n)

Verifies that k ≤ k_bound empirically for n=5..8, various m.

No 7th; no break; no security claim. OPEN = LSN.
"""
import json
import math
import random
from collections import Counter

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

def mat_vec(b, A):
    D = len(A)
    n = len(A[0])
    return [sum(b[i] * A[i][j] for i in range(D)) % 2 for j in range(n)]

def hamming_weight(v):
    return sum(v)

def sd_to_uniform(samples, n):
    """Empirical SD to uniform: max |freq(c) - 1/2^n|."""
    total = 2 ** n
    counts = Counter(tuple(s) for s in samples)
    max_dev = 0.0
    for c, cnt in counts.items():
        dev = abs(cnt / len(samples) - 1.0 / total)
        if dev > max_dev:
            max_dev = dev
    # Also account for unseen strings
    unseen = total - len(counts)
    if unseen > 0:
        max_dev = max(max_dev, 1.0 / total)
    return max_dev

def main():
    results = []
    for n in [5, 6, 7, 8]:
        D = 2 * n
        w = int(0.19 * n)
        print(f"\nn={n}, D={D}, w={w}")
        for m in [10 * n, 16 * n, 20 * n]:
            print(f"  m={m}:")
            for trial in range(10):
                A = sample_isotropic_basis(D, n)
                # Random B
                B = [[random.randint(0, 1) for _ in range(D)] for _ in range(m)]
                BA = [mat_vec(b, A) for b in B]

                k = sum(1 for b in B if hamming_weight(b) <= w)
                delta = sd_to_uniform(BA, n)

                # M1 bound
                bound = ((1.5 * n * n + n / 2 + delta * m * n + 1) / (0.094 * n))

                print(f"    trial={trial}: k={k:4d}, delta={delta:.4f}, bound={bound:.1f}, ok={k <= bound}")
                results.append({
                    "n": n, "m": m, "trial": trial,
                    "k": k, "delta": delta, "bound": bound, "ok": k <= bound
                })
                assert k <= bound, f"M1 bound violated: {k} > {bound}"

    with open("experiments/93-m1-verification.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiments/93-m1-verification.json")

if __name__ == "__main__":
    main()
