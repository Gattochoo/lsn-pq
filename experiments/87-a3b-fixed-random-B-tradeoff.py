"""
87 — A3b: fixed↔random B trade-off probe (n=5).

Model: A ∈ F2^{D×n} (D=2n) isotropic columns, public.
B is drawn from an interpolating family between two endpoints:
  (i)  FIXED low-rank B_fixed (rank r < D), giving Gram-detector viability;
  (ii) RANDOM B over the affine space {B : BA uniform}, giving piling-up bias decay.

Interpolation:  B = B_fixed + Z,  where rows of Z lie in nullspace(A^T).
Randomness parameter q ∈ [0, 1/2]:
    w_{ij} ~ Bernoulli(q) iid,  z_i = sum_j w_{ij} v_j,  {v_j}=nullspace(A^T) basis.
    q=0   → B = B_fixed (fixed, low-rank, Gram detector works).
    q=1/2 → B = B_fixed + Z_uniform (random, full-rank, bias small).

Metrics vs q:
    1. Gram-detectability:  min_Q rank(Ω + B^T Q B)  (exact formula 2c − rank(Ω|_K)).
       For fixed low-rank B this is large (≥ n when c ≥ n/2), enabling Gram detection.
       For random full-rank B this is small (< n), blocking detection.
    2. Label bias:  avg_i |(1−2p)^{|b_i|}|.
       For fixed B with small row weight, bias ≈ (1−2p)^{O(1)} = Θ(1).
       For random B with row weight ~ D/2, bias ≈ (1−2p)^{D/2} = 2^{−Θ(n)}.

Trade-off hypothesis: as q increases, Gram rank drops from ≥n to <n (detector dies)
while bias decays from Θ(1) to 2^{−Θ(n)} (LPN solver dies).  The two endpoint theorems
are connected by a continuous trade-off curve.

Output: JSON + summary table.  No 7th; no break; no security claim.
"""
import json
import random
from collections import Counter

random.seed(42)

p = 0.25
n = 5
D = 2 * n  # 10
m = 12

def rank(M):
    if not M or not M[0]: return 0
    A = [r[:] for r in M]
    rows, cols = len(A), len(A[0])
    piv = 0
    for c_ in range(cols):
        r_ = next((r for r in range(piv, rows) if A[r][c_]), None)
        if r_ is None: continue
        A[piv], A[r_] = A[r_], A[piv]
        for rr in range(rows):
            if rr != piv and A[rr][c_]:
                A[rr] = [x ^ y for x, y in zip(A[rr], A[piv])]
        piv += 1
    return piv

def matmul(X, Y):
    q, r = len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][j] for k in range(q)) % 2 for j in range(r)]
            for i in range(len(X))]

def transpose(X):
    return [list(r) for r in zip(*X)]

def vec_add(u, v):
    return [a ^ b for a, b in zip(u, v)]

def sample_isotropic_basis(D, n):
    """A ∈ F2^{D×n} with isotropic columns."""
    Om = [[0] * D for _ in range(D)]
    for i in range(n):
        Om[i][i + n] = 1
        Om[i + n][i] = 1
    cols = []
    attempts = 0
    while len(cols) < n and attempts < 10000:
        v = [random.randint(0, 1) for _ in range(D)]
        attempts += 1
        ok = True
        for u in cols:
            pair = sum(u[i] * Om[i][j] * v[j] for i in range(D) for j in range(D)) % 2
            if pair != 0:
                ok = False
                break
        if ok:
            cols.append(v)
    if len(cols) < n:
        while len(cols) < n:
            cols.append(cols[-1][:])
    return transpose(cols)

def nullspace_basis(M):
    """Basis for {x : M x = 0}.  Returns list of column vectors."""
    rows, cols = len(M), len(M[0])
    A = [r[:] for r in M]
    piv = 0
    pivcol = {}
    for c_ in range(cols):
        r_ = next((r for r in range(piv, rows) if A[r][c_]), None)
        if r_ is None: continue
        A[piv], A[r_] = A[r_], A[piv]
        for rr in range(rows):
            if rr != piv and A[rr][c_]:
                A[rr] = [x ^ y for x, y in zip(A[rr], A[piv])]
        pivcol[c_] = piv
        piv += 1
    free_cols = [c_ for c_ in range(cols) if c_ not in pivcol]
    basis = []
    for f in free_cols:
        vec = [0] * cols
        vec[f] = 1
        for c_, p_ in pivcol.items():
            vec[c_] = A[p_][f]
        basis.append(vec)
    return basis

def sample_B_fixed_lowrank(m, D, target_rank):
    """Sample B_fixed ∈ F2^{m×D} with rank ≈ target_rank (rows in a random r-dim subspace)."""
    r = target_rank
    # Random r-dimensional subspace of F2^D
    basis = []
    attempts = 0
    while len(basis) < r and attempts < 1000:
        v = [random.randint(0, 1) for _ in range(D)]
        attempts += 1
        if rank(basis + [v]) > len(basis):
            basis.append(v)
    B = []
    for _ in range(m):
        coeffs = [random.randint(0, 1) for _ in range(r)]
        row = [0] * D
        for j in range(r):
            if coeffs[j]:
                row = vec_add(row, basis[j])
        B.append(row)
    return B

def sample_B_given_A(A, B_fixed, q):
    """B = B_fixed + Z, rows of Z in nullspace(A^T), randomness q."""
    null_basis = nullspace_basis(transpose(A))  # vectors in F2^D
    k = len(null_basis)
    B = [b[:] for b in B_fixed]
    for i in range(m):
        w = [random.randint(0, 1) if random.random() < 2 * q else 0 for _ in range(k)]
        for j in range(k):
            if w[j]:
                B[i] = vec_add(B[i], null_basis[j])
    return B

def min_rank_transportable(B, n):
    """Exact formula: min_Q rank(Ω + B^T Q B) = 2c − rank(Ω|_K)."""
    D_local = 2 * n
    rho = rank(B)
    c = D_local - rho
    if c <= 0:
        return 0
    Om = [[0] * D_local for _ in range(D_local)]
    for i in range(n):
        Om[i][i + n] = 1
        Om[i + n][i] = 1
    M = [row[:] for row in B]
    rows, cols = len(M), len(M[0])
    piv = 0
    pivcol = {}
    for c_ in range(cols):
        r_ = next((r for r in range(piv, rows) if M[r][c_]), None)
        if r_ is None: continue
        M[piv], M[r_] = M[r_], M[piv]
        for rr in range(rows):
            if rr != piv and M[rr][c_]:
                M[rr] = [x ^ y for x, y in zip(M[rr], M[piv])]
        pivcol[c_] = piv
        piv += 1
    K_vecs = []
    for f in [c_ for c_ in range(cols) if c_ not in pivcol]:
        v = [0] * cols
        v[f] = 1
        for c_, p_ in pivcol.items():
            v[c_] = M[p_][f]
        K_vecs.append(v)
    if len(K_vecs) != c:
        return c
    S = [k[:] for k in K_vecs]
    for e in range(cols):
        cand = [0] * cols
        cand[e] = 1
        if rank(S + [cand]) > len(S):
            S.append(cand)
        if len(S) == cols:
            break
    Sm = transpose(S)
    Omp = matmul(matmul(transpose(Sm), Om), Sm)
    OKK = [r[:c] for r in Omp[:c]]
    rKK = rank(OKK)
    return 2 * c - rKK

def bias_per_row(B, p):
    val = abs(1 - 2 * p)
    return sum(val ** sum(b) for b in B) / len(B)

def run_trial(A, B_fixed, q, n):
    B = sample_B_given_A(A, B_fixed, q)
    gram_r = min_rank_transportable(B, n)
    bias = bias_per_row(B, p)
    rank_B = rank(B)
    c = 2 * n - rank_B
    return {
        "rank_B": rank_B,
        "c": c,
        "min_rank_E": gram_r,
        "bias": bias,
    }

def main():
    q_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    trials_per_q = 30
    num_A = 6
    target_ranks = [3, 4, 5]  # low-rank fixed B endpoints

    all_data = []
    for idx_A in range(num_A):
        A = sample_isotropic_basis(D, n)
        # Verify isotropy
        Om = [[0] * D for _ in range(D)]
        for i in range(n):
            Om[i][i + n] = 1
            Om[i + n][i] = 1
        iso = matmul(matmul(transpose(A), Om), A)
        assert rank(iso) == 0, "A not isotropic"

        for tr in target_ranks:
            B_fixed = sample_B_fixed_lowrank(m, D, tr)
            for q in q_values:
                trials = [run_trial(A, B_fixed, q, n) for _ in range(trials_per_q)]
                all_data.append({
                    "A_idx": idx_A,
                    "target_rank": tr,
                    "q": q,
                    "trials": trials,
                })

    summary = {}
    for tr in target_ranks:
        summary[tr] = {}
        for q in q_values:
            entries = []
            for block in all_data:
                if block["target_rank"] == tr and abs(block["q"] - q) < 1e-9:
                    for t in block["trials"]:
                        entries.append(t)
            summary[tr][q] = {
                "n_trials": len(entries),
                "avg_rank_B": sum(e["rank_B"] for e in entries) / len(entries),
                "avg_c": sum(e["c"] for e in entries) / len(entries),
                "avg_min_rank_E": sum(e["min_rank_E"] for e in entries) / len(entries),
                "avg_bias": sum(e["bias"] for e in entries) / len(entries),
                "min_rank_E_dist": dict(Counter(e["min_rank_E"] for e in entries)),
            }

    out = {
        "params": {"n": n, "m": m, "p": p, "D": D, "trials_per_q": trials_per_q, "num_A": num_A},
        "summary": {str(tr): {str(q): v for q, v in d.items()} for tr, d in summary.items()},
        "raw": all_data,
    }

    with open("experiments/87-a3b-results.json", "w") as f:
        json.dump(out, f, indent=2)

    print("A3b trade-off probe (n=5):")
    for tr in target_ranks:
        print(f"\n--- target_rank(B_fixed) = {tr} ---")
        print(f"{'q':>5} {'avg rank(B)':>12} {'avg c':>7} {'avg min rank(E)':>17} {'avg bias':>12}")
        for q in q_values:
            s = summary[tr][q]
            print(f"{q:>5.2f} {s['avg_rank_B']:>12.2f} {s['avg_c']:>7.2f} "
                  f"{s['avg_min_rank_E']:>17.2f} {s['avg_bias']:>12.6f}")
    print("\nSaved to experiments/87-a3b-results.json")

if __name__ == "__main__":
    main()
