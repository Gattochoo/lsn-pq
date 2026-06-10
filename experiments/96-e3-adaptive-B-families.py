#!/usr/bin/env python3
"""
P3 E3: Adversarial adaptive-B families for Open Problem 9.

Design ≥4 B families and measure how well each matches P1 statistics.
Families:
  (i) uniform    — random rows (baseline, already in P1)
  (ii) low_w3    — constant weight 3 (maximizes noise correlation / minimizes piling-up)
  (iii) high_w   — weight ~n (intermediate piling-up)
  (iv) all_ones  — every row = (1,...,1) (maximal piling-up, Be = parity of all e bits)

For each family, run the 4 statistics from P1 E1 and report distance to P1.
"""

import random
import json
import sys

# Helpers (same as 94, 95)
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

def sample_P0_with_B(n, m, p, B_family):
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
    elif B_family == "high_w":
        B = []
        target = n
        for _ in range(m):
            row = 0
            positions = random.sample(range(2 * n), min(target, 2 * n))
            for pos in positions:
                row |= (1 << pos)
            B.append(row)
    elif B_family == "all_ones":
        B = [(1 << (2 * n)) - 1 for _ in range(m)]
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

def run_for_family(n, m, p_prime, B_family, num_samples=2000):
    P0_stats = {"syndrome": [], "rank_diff": [], "corr": [], "max_agree": []}
    for _ in range(num_samples):
        C0, y0 = sample_P0_with_B(n, m, 0.25, B_family)
        r0 = gf2_rank(C0)
        aug0 = list(C0)
        n0 = max((x.bit_length() for x in C0), default=0)
        aug0.append(y0 | (1 << n0))
        r0y = gf2_rank(aug0)
        P0_stats["syndrome"].append(syndrome_weight(C0, y0))
        P0_stats["rank_diff"].append(r0y - r0)
        P0_stats["corr"].append(second_moment_proxy(y0, m))
        P0_stats["max_agree"].append(max_agreement(C0, y0))

    P1_stats = {"syndrome": [], "rank_diff": [], "corr": [], "max_agree": []}
    for _ in range(num_samples):
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

    def mean(v):
        return sum(v) / len(v)

    def sep(p0, p1):
        m0, m1 = mean(p0), mean(p1)
        v0 = sum((x - m0) ** 2 for x in p0) / len(p0)
        v1 = sum((x - m1) ** 2 for x in p1) / len(p1)
        ps = ((v0 + v1) / 2) ** 0.5
        return round(abs(m0 - m1) / ps, 4) if ps > 0 else float('inf')

    return {
        "B_family": B_family,
        "P0_means": {
            "syndrome": round(mean(P0_stats["syndrome"]), 4),
            "rank_diff": round(mean(P0_stats["rank_diff"]), 4),
            "corr": round(mean(P0_stats["corr"]), 4),
            "max_agree": round(mean(P0_stats["max_agree"]), 4),
        },
        "P1_means": {
            "syndrome": round(mean(P1_stats["syndrome"]), 4),
            "rank_diff": round(mean(P1_stats["rank_diff"]), 4),
            "corr": round(mean(P1_stats["corr"]), 4),
            "max_agree": round(mean(P1_stats["max_agree"]), 4),
        },
        "separation": {
            "syndrome": sep(P0_stats["syndrome"], P1_stats["syndrome"]),
            "rank_diff": sep(P0_stats["rank_diff"], P1_stats["rank_diff"]),
            "corr": sep(P0_stats["corr"], P1_stats["corr"]),
            "max_agree": sep(P0_stats["max_agree"], P1_stats["max_agree"]),
        },
    }

def main():
    random.seed(0xE3A1)
    families = ["uniform", "low_w3", "high_w", "all_ones"]
    configs = [
        (4, 8, 0.2),
        (5, 10, 0.2),
        (6, 12, 0.2),
        (6, 24, 0.2),
    ]

    all_results = []
    for n, m, p_prime in configs:
        print(f"Running n={n}, m={m}, p'={p_prime} ...", file=sys.stderr)
        family_results = []
        for fam in families:
            print(f"  family={fam} ...", file=sys.stderr)
            res = run_for_family(n, m, p_prime, fam, num_samples=2000)
            family_results.append(res)
        all_results.append({
            "n": n, "m": m, "p_prime": p_prime,
            "families": family_results,
        })

    output = {
        "experiment": "96-e3-adaptive-B-families",
        "description": "4 B families vs P1 on 4 statistics",
        "results": all_results,
    }
    with open("experiments/96-e3-results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Saved experiments/96-e3-results.json", file=sys.stderr)
    print("\n=== SEPARATION RATIOS (P0 vs P1) ===", file=sys.stderr)
    print("n | m  | family    | syndrome | rank_diff | corr   | max_agree", file=sys.stderr)
    for entry in all_results:
        for fam in entry["families"]:
            s = fam["separation"]
            print(f"{entry['n']} | {entry['m']:2} | {fam['B_family']:9} | "
                  f"{s['syndrome']:8.3f} | {s['rank_diff']:9.3f} | "
                  f"{s['corr']:6.3f} | {s['max_agree']:9.3f}", file=sys.stderr)

if __name__ == "__main__":
    main()
