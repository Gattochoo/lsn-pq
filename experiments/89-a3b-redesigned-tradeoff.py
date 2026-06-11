# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
89 — A3b redesigned: fixed↔random B trade-off probe (n=5), row-wise mixture family.

Fixes the degeneracy in experiments/87: ZA=0 froze BA, making the family trivially non-uniform.
New family: each row b_i is independently
    structured  w.p. 1−q  (from a fixed low-rank B_fixed)
    uniform     w.p. q   (random in F2^D)
This makes BA a genuine mixture: q=0 → low-rank BA; q=1 → uniform BA.

Metrics (output-side, per adjudication):
    1. BA uniformity: statistical distance of BA from uniform F2^{m×n}.
    2. Gram detectability: min_Q rank(Ω + B^T Q B).
    3. Label bias: avg_i |(1−2p)^{|b_i|}|.

Output: JSON + summary.  No 7th; no break; no security claim. OPEN = LSN.
"""
import json
import random
import math
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
    """A ∈ F2^{D×n} with isotropic columns forming a basis (rank n)."""
    Om = [[0] * D for _ in range(D)]
    for i in range(n):
        Om[i][i + n] = 1
        Om[i + n][i] = 1
    cols = []
    attempts = 0
    while len(cols) < n and attempts < 20000:
        v = [random.randint(0, 1) for _ in range(D)]
        attempts += 1
        # Isotropy check
        ok = True
        for u in cols:
            pair = sum(u[i] * Om[i][j] * v[j] for i in range(D) for j in range(D)) % 2
            if pair != 0:
                ok = False
                break
        if not ok:
            continue
        # Linear independence check
        if rank([list(c) for c in cols] + [v]) <= len(cols):
            continue
        cols.append(v)
    assert len(cols) == n, f"Failed to find isotropic basis: got {len(cols)}/{n}"
    return transpose(cols)

def sample_B_fixed_lowrank(m, D, target_rank):
    """Sample B_fixed ∈ F2^{m×D} with rank ≈ target_rank."""
    r = target_rank
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

def sample_B_mixture(B_fixed, q):
    """Each row: structured (B_fixed) w.p. 1-q, uniform w.p. q."""
    B = []
    for i in range(len(B_fixed)):
        if random.random() < q:
            B.append([random.randint(0, 1) for _ in range(len(B_fixed[0]))])
        else:
            B.append(B_fixed[i][:])
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

def ba_uniformity(BA, n, trials=200):
    """Estimate total-variation-like distance of BA from uniform F2^{m×n}.
    We use a simple proxy: entropy of row-space + rank test vs uniform."""
    m_local = len(BA)
    # Rank of BA
    r = rank(BA)
    # Expected rank of uniform random m×n is min(m,n) w.h.p.
    max_r = min(m_local, n)
    # Simple proxy: fraction of max rank achieved (1 = uniform-like, <1 = structured)
    rank_proxy = r / max_r if max_r > 0 else 0.0
    # Row-distribution test: count distinct rows vs expected
    distinct = len(set(tuple(r) for r in BA))
    expected_distinct = min(2 ** n, m_local) * (1 - (1 - 1 / (2 ** n)) ** m_local)
    # Very rough: compare distinct rows to expected under uniform
    distinct_proxy = distinct / expected_distinct if expected_distinct > 0 else 0.0
    return rank_proxy, distinct_proxy, r

def run_trial(A, B_fixed, q, n):
    B = sample_B_mixture(B_fixed, q)
    BA = matmul(B, A)
    gram_r = min_rank_transportable(B, n)
    bias = bias_per_row(B, p)
    rank_B = rank(B)
    c = 2 * n - rank_B
    rank_proxy, distinct_proxy, rank_BA = ba_uniformity(BA, n)
    return {
        "rank_B": rank_B,
        "c": c,
        "min_rank_E": gram_r,
        "bias": bias,
        "rank_BA": rank_BA,
        "rank_proxy": rank_proxy,
        "distinct_proxy": distinct_proxy,
    }

def main():
    q_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    trials_per_q = 40
    num_A = 6
    target_ranks = [3, 4, 5]

    all_data = []
    for idx_A in range(num_A):
        A = sample_isotropic_basis(D, n)
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
                "avg_rank_BA": sum(e["rank_BA"] for e in entries) / len(entries),
                "avg_rank_proxy": sum(e["rank_proxy"] for e in entries) / len(entries),
                "avg_distinct_proxy": sum(e["distinct_proxy"] for e in entries) / len(entries),
            }

    out = {
        "params": {"n": n, "m": m, "p": p, "D": D, "trials_per_q": trials_per_q, "num_A": num_A},
        "summary": {str(tr): {str(q): v for q, v in d.items()} for tr, d in summary.items()},
        "raw": all_data,
    }

    with open("experiments/89-a3b-results.json", "w") as f:
        json.dump(out, f, indent=2)

    print("A3b redesigned trade-off probe (n=5, row-wise mixture):")
    for tr in target_ranks:
        print(f"\n--- target_rank(B_fixed) = {tr} ---")
        print(f"{'q':>5} {'rank(B)':>8} {'c':>5} {'minR(E)':>8} {'bias':>10} {'rank(BA)':>9} {'rank_proxy':>11} {'dist_proxy':>11}")
        for q in q_values:
            s = summary[tr][q]
            print(f"{q:>5.1f} {s['avg_rank_B']:>8.2f} {s['avg_c']:>5.2f} "
                  f"{s['avg_min_rank_E']:>8.2f} {s['avg_bias']:>10.6f} "
                  f"{s['avg_rank_BA']:>9.2f} {s['avg_rank_proxy']:>11.4f} {s['avg_distinct_proxy']:>11.4f}")
    print("\nSaved to experiments/89-a3b-results.json")

if __name__ == "__main__":
    main()
