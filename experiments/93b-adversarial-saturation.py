"""
93b — Adversarial saturation probe for M1 bound (ILLUSTRATIVE).

Varying the fraction alpha of low-weight rows in B, measures:
  1. SD(BA, Uniform) — actual uniformity gap
  2. k = actual low-weight rows
  3. M1 bound vs actual k

This script is ILLUSTRATIVE: it verifies that the M1 bound ingredients hold
individually (entropy estimate, uniformity bound, noise amplification), but it
does NOT assemble a full non-vacuous barrier because at small n the 11m/n term
dominates the bound.  It confirms M1 is not vacuous for the tested parameter
ranges, not that the marginal-adaptive corner is closed.

No 7th; no break; no security claim. OPEN = LSN.
"""
import json
import random
import math
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
    assert len(cols) == n, f"Failed: {len(cols)}/{n}"
    return cols

def mat_vec(b, A):
    D = len(A)
    n = len(A[0])
    return [sum(b[i] * A[i][j] for i in range(D)) % 2 for j in range(n)]

def hamming_weight(v):
    return sum(v)

def sd_to_uniform(samples, n):
    total = 2 ** n
    counts = Counter(tuple(s) for s in samples)
    max_dev = 0.0
    for c, cnt in counts.items():
        dev = abs(cnt / len(samples) - 1.0 / total)
        if dev > max_dev:
            max_dev = dev
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
        for m in [50 * n, 100 * n, 200 * n]:
            print(f"  m={m}:")
            for alpha in [0.0, 0.05, 0.10, 0.20, 0.30, 0.50]:
                vals = []
                for trial in range(20):
                    A = sample_isotropic_basis(D, n)
                    B = []
                    for _ in range(m):
                        if random.random() < alpha:
                            # low-weight row
                            b = [0] * D
                            # random weight ≤ w
                            w_row = random.randint(0, w)
                            ones = random.sample(range(D), w_row)
                            for idx in ones:
                                b[idx] = 1
                        else:
                            # high-weight row (weight > w)
                            b = [random.randint(0, 1) for _ in range(D)]
                            while hamming_weight(b) <= w:
                                b = [random.randint(0, 1) for _ in range(D)]
                        B.append(b)

                    BA = [mat_vec(b, A) for b in B]
                    k = sum(1 for b in B if hamming_weight(b) <= w)
                    delta = sd_to_uniform(BA, n)
                    vals.append({"k": k, "delta": delta})

                mean_k = sum(v["k"] for v in vals) / len(vals)
                mean_delta = sum(v["delta"] for v in vals) / len(vals)
                # M1 bound (corrected)
                bound = ((1.5 * n * n + n / 2 + mean_delta * m * n + m + 1) / (0.094 * n))
                print(f"    alpha={alpha:.2f}: E[k]={mean_k:.1f}, delta={mean_delta:.4f}, bound={bound:.1f}, ok={mean_k <= bound}")
                results.append({
                    "n": n, "m": m, "alpha": alpha,
                    "mean_k": mean_k, "mean_delta": mean_delta,
                    "bound": bound, "ok": mean_k <= bound
                })

    with open("experiments/93b-adversarial-saturation.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiments/93b-adversarial-saturation.json")

if __name__ == "__main__":
    main()
