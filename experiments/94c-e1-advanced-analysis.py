#!/usr/bin/env python3
"""
P1 E1 advanced analysis: ROC curves and AUC for the 4 statistics.
Goes beyond separation ratio to measure actual distinguishing advantage.
"""

import random
import json
import sys

# Reuse helpers from 94-e1-distinguishing-game.py
def dot_parity(a, b):
    return (a & b).bit_count() & 1

def gf2_rank(matrix_rows):
    m = list(matrix_rows)
    rank = 0
    row = 0
    if not m:
        return 0
    col = max((x.bit_length() for x in m), default=0)
    for c in range(col - 1, -1, -1):
        pivot = None
        for r in range(row, len(m)):
            if (m[r] >> c) & 1:
                pivot = r
                break
        if pivot is None:
            continue
        m[row], m[pivot] = m[pivot], m[row]
        for r in range(len(m)):
            if r != row and ((m[r] >> c) & 1):
                m[r] ^= m[row]
        row += 1
        rank += 1
        if row >= len(m):
            break
    return rank

def syndrome_weight(C, y):
    m = len(C)
    if m == 0:
        return 0
    n = max((x.bit_length() for x in C), default=0)
    aug = list(C)
    for i in range(m):
        if (y >> i) & 1:
            aug[i] |= (1 << n)
    rank = 0
    row = 0
    for c in range(n - 1, -1, -1):
        pivot = None
        for r in range(row, m):
            if (aug[r] >> c) & 1:
                pivot = r
                break
        if pivot is None:
            continue
        aug[row], aug[pivot] = aug[pivot], aug[row]
        for r in range(m):
            if r != row and ((aug[r] >> c) & 1):
                aug[r] ^= aug[row]
        row += 1
        rank += 1
        if row >= m:
            break
    weight = 0
    for i in range(rank, m):
        if (aug[i] >> n) & 1:
            weight += 1
    return weight

def second_moment_proxy(y, m):
    w = y.bit_count()
    if m <= 1:
        return 0.0
    total_pairs = m * (m - 1) // 2
    if total_pairs == 0:
        return 0.0
    one_pairs = w * (w - 1) // 2
    zero_pairs = (m - w) * (m - w - 1) // 2
    agree = (one_pairs + zero_pairs) / total_pairs
    return 2.0 * agree - 1.0

def max_agreement(C, y):
    m = len(C)
    if m == 0:
        return 0
    n = max((x.bit_length() for x in C), default=0)
    best = 0
    for x in range(1 << n):
        cnt = sum(1 for i in range(m) if dot_parity(C[i], x) == ((y >> i) & 1))
        if cnt > best:
            best = cnt
    return best

def random_symmetric_matrix_rows(n):
    rows = []
    for i in range(n):
        row = random.getrandbits(n)
        for j in range(i):
            if (rows[j] >> i) & 1:
                row |= (1 << j)
            else:
                row &= ~(1 << j)
        rows.append(row)
    return rows

def isotropic_basis_from_symmetric(M_rows, n):
    A = []
    for j in range(n):
        A.append(1 << j)
        b_row = 0
        for i in range(n):
            if (M_rows[j] >> i) & 1:
                b_row |= (1 << i)
        A.append(b_row)
    return A

def sample_P0(n, m, p, B_family="uniform"):
    M_rows = random_symmetric_matrix_rows(n)
    A = isotropic_basis_from_symmetric(M_rows, n)
    x = random.getrandbits(n)
    e = 0
    for k in range(2 * n):
        if random.random() < p:
            e |= (1 << k)
    w = 0
    for k in range(2 * n):
        if (dot_parity(A[k], x) ^ ((e >> k) & 1)):
            w |= (1 << k)

    if B_family == "uniform":
        B = [random.getrandbits(2 * n) for _ in range(m)]
    elif B_family == "low_w3":
        B = []
        for _ in range(m):
            row = 0
            positions = random.sample(range(2 * n), min(3, 2 * n))
            for pos in positions:
                row |= (1 << pos)
            B.append(row)
    else:
        raise ValueError(B_family)

    C = []
    for i in range(m):
        c_row = 0
        for k in range(2 * n):
            if (B[i] >> k) & 1:
                c_row ^= A[k]
        C.append(c_row)

    y = 0
    for i in range(m):
        if dot_parity(B[i], w):
            y |= (1 << i)

    return C, y

def sample_P1(m, n, p_prime):
    C_prime = [random.getrandbits(n) for _ in range(m)]
    x_prime = random.getrandbits(n)
    y_prime = 0
    for i in range(m):
        val = dot_parity(C_prime[i], x_prime)
        if random.random() < p_prime:
            val ^= 1
        if val:
            y_prime |= (1 << i)
    return C_prime, y_prime

def compute_roc(P0_vals, P1_vals):
    """Compute ROC curve and AUC for a statistic where higher = more P0-like."""
    all_vals = sorted(set(P0_vals + P1_vals))
    tpr_list = []
    fpr_list = []
    n0 = len(P0_vals)
    n1 = len(P1_vals)

    for thresh in all_vals + [all_vals[-1] + 1]:
        tp = sum(1 for v in P0_vals if v >= thresh)
        fp = sum(1 for v in P1_vals if v >= thresh)
        tpr = tp / n0
        fpr = fp / n1
        tpr_list.append(tpr)
        fpr_list.append(fpr)

    # AUC via trapezoid rule
    auc = 0.0
    for i in range(len(fpr_list) - 1):
        dx = fpr_list[i+1] - fpr_list[i]
        avg_y = (tpr_list[i+1] + tpr_list[i]) / 2.0
        auc += dx * avg_y

    return {"tpr": tpr_list, "fpr": fpr_list, "auc": round(auc, 6)}

def run_analysis(n, m, p_prime, B_family, num_samples=2000):
    P0_stats = {"syndrome": [], "rank_diff": [], "corr": [], "max_agree": []}
    P1_stats = {"syndrome": [], "rank_diff": [], "corr": [], "max_agree": []}

    for _ in range(num_samples):
        C0, y0 = sample_P0(n, m, 0.25, B_family)
        r0 = gf2_rank(C0)
        aug0 = list(C0)
        n0 = max((x.bit_length() for x in C0), default=0)
        aug0.append(y0 | (1 << n0))
        r0y = gf2_rank(aug0)
        P0_stats["syndrome"].append(syndrome_weight(C0, y0))
        P0_stats["rank_diff"].append(r0y - r0)
        P0_stats["corr"].append(second_moment_proxy(y0, m))
        P0_stats["max_agree"].append(max_agreement(C0, y0))

        C1, y1 = sample_P1(m, n, p_prime)
        r1 = gf2_rank(C1)
        aug1 = list(C1)
        n1 = max((x.bit_length() for x in C1), default=0)
        aug1.append(y1 | (1 << n1))
        r1y = gf2_rank(aug1)
        P1_stats["syndrome"].append(syndrome_weight(C1, y1))
        P1_stats["rank_diff"].append(r1y - r1)
        P1_stats["corr"].append(second_moment_proxy(y1, m))
        P1_stats["max_agree"].append(max_agreement(C1, y1))

    result = {
        "n": n, "m": m, "p_prime": p_prime, "B_family": B_family,
        "num_samples": num_samples,
    }

    for stat_name in ["syndrome", "rank_diff", "corr", "max_agree"]:
        roc = compute_roc(P0_stats[stat_name], P1_stats[stat_name])
        # Also compute histograms
        hist_P0 = {}
        hist_P1 = {}
        for v in P0_stats[stat_name]:
            hist_P0[v] = hist_P0.get(v, 0) + 1
        for v in P1_stats[stat_name]:
            hist_P1[v] = hist_P1.get(v, 0) + 1
        result[stat_name] = {
            "auc": roc["auc"],
            "P0_hist": {str(k): v for k, v in hist_P0.items()},
            "P1_hist": {str(k): v for k, v in hist_P1.items()},
        }

    return result

def main():
    random.seed(0x94C0)
    configs = [
        (4, 8, 0.2, "uniform"),
        (5, 10, 0.2, "uniform"),
        (6, 12, 0.2, "uniform"),
        (6, 24, 0.2, "uniform"),
    ]

    all_results = []
    for n, m, p_prime, B_family in configs:
        print(f"Running n={n}, m={m} ...", file=sys.stderr)
        res = run_analysis(n, m, p_prime, B_family, num_samples=2000)
        all_results.append(res)

    output = {
        "experiment": "94c-e1-advanced-analysis",
        "description": "ROC/AUC and histograms for 4 statistics",
        "results": all_results,
    }
    with open("experiments/94c-e1-advanced.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n=== AUC SUMMARY ===", file=sys.stderr)
    print("n | m  | syndrome | rank_diff | corr   | max_agree", file=sys.stderr)
    for r in all_results:
        print(f"{r['n']} | {r['m']:2} | {r['syndrome']['auc']:8.4f} | {r['rank_diff']['auc']:9.4f} | "
              f"{r['corr']['auc']:6.4f} | {r['max_agree']['auc']:9.4f}", file=sys.stderr)

if __name__ == "__main__":
    main()
