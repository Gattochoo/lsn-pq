#!/usr/bin/env python3
"""
E-OP9b: 저무게 행의 c_i 비균등성 정량화 (trade-off 곡선).

G-TARGET: 이 실험이 재는 것은 "저무게 행이 marginal-uniformity를 얼마나 해치는가?"이며,
이것은 "x 복원가능성"과 직결된다.

설계: 고정된 B에 대해, A가 랜덤할 때 c_i = (BA)_i의 분포가 uniform에서 얼마나 떨어지는지 측정.
- Support 종류: bottom-only (하단 블록만), top-only (상단 블록만), mixed (혼합).
- 무게 w: 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64.
- Metric: entropy ratio H(c_i)/n (1=완벽히 균등, 0=완전히 결정적).
- 추가: x 복원 성공률 vs w (recovery correlation).

Output: JSON with trade-off curves.
"""

import random
import json
import sys
from collections import Counter
from math import log2

sys.path.insert(0, 'experiments')
with open('experiments/94-e1-distinguishing-game.py') as f:
    code = f.read().replace("if __name__ == '__main__':", "if False:")
exec(code)

# Reuse helpers from 113
exec(open('experiments/113-e-op9a-lowweight-B-recovery.py').read().replace('if __name__ == "__main__":', 'if False:'))

def fixed_B(family, n, m, w):
    """Generate a fixed B matrix for trade-off measurement.
    
    All rows have the same structure (same support pattern) to isolate the effect of w.
    """
    if family == "bottom_w":
        # All rows select the first w bottom basis vectors: indices 1, 3, 5, ..., 2w-1
        # This gives c_i = M_0 + M_1 + ... + M_{w-1} for all rows.
        row = sum(1 << (2 * j + 1) for j in range(w))
        return [row] * m
    elif family == "top_w":
        # All rows select the first w top basis vectors: indices 0, 2, 4, ..., 2w-2
        # This gives c_i = e_0 + e_1 + ... + e_{w-1} for all rows.
        row = sum(1 << (2 * j) for j in range(w))
        return [row] * m
    elif family == "mixed_w":
        # Half top, half bottom (or as close as possible)
        w_top = w // 2
        w_bottom = w - w_top
        row = sum(1 << (2 * j) for j in range(w_top))
        row |= sum(1 << (2 * j + 1) for j in range(w_bottom))
        return [row] * m
    elif family == "random_w":
        # Random support of weight w in 2n bits, fixed per row
        row = 0
        positions = random.sample(range(2 * n), w)
        for p in positions:
            row |= (1 << p)
        return [row] * m
    else:
        raise ValueError(family)

def measure_nonuniformity(family, n, m, w, num_A_samples=2000):
    """Measure entropy ratio of c_i for fixed B and random A."""
    B = fixed_B(family, n, m, w)
    counter = Counter()
    for _ in range(num_A_samples):
        M_rows = random_symmetric_matrix_rows(n)
        A = isotropic_basis_from_symmetric(M_rows, n)
        C = compute_C(B, A)
        # Use first row of C
        counter[C[0]] += 1
    
    total = sum(counter.values())
    ent = 0.0
    for count in counter.values():
        p = count / total
        ent -= p * log2(p)
    
    max_possible = n
    entropy_ratio = ent / max_possible if max_possible > 0 else 1.0
    
    # Also compute chi-square distance from uniform (over observed bins)
    expected = total / (2 ** n)
    chi2 = 0.0
    for count in counter.values():
        chi2 += (count - expected) ** 2 / expected
    
    return {
        "entropy_ratio": round(entropy_ratio, 4),
        "chi2": round(chi2, 2),
        "unique_values": len(counter),
        "total_samples": total,
    }

def recovery_with_fixed_B(family, n, m, w, num_trials=200):
    """x recovery success rate with fixed B."""
    B = fixed_B(family, n, m, w)
    successes = 0
    for _ in range(num_trials):
        C, y, true_x = sample_P0_with_B(n, m, B)
        recovered_x, _ = max_agreement_for_recovery(C, y)
        if recovered_x == true_x:
            successes += 1
    return successes / num_trials

if __name__ == "__main__":
    random.seed(0x5E1F)
    configs = [
        # (n, m, family, w_list)
        (6, 24, "bottom_w", [1, 2, 3, 4, 5, 6]),
        (6, 24, "top_w", [1, 2, 3, 4, 5, 6]),
        (6, 24, "mixed_w", [2, 4, 6]),
        (8, 32, "bottom_w", [1, 2, 3, 4, 6, 8]),
        (8, 32, "top_w", [1, 2, 3, 4, 6, 8]),
        (10, 40, "bottom_w", [1, 2, 3, 5, 8, 10]),
        (10, 40, "top_w", [1, 2, 3, 5, 8, 10]),
    ]
    
    results = []
    for n, m, family, w_list in configs:
        for w in w_list:
            print(f"Running n={n}, m={m}, family={family}, w={w} ...", file=sys.stderr)
            nu = measure_nonuniformity(family, n, m, w, num_A_samples=2000)
            rec = recovery_with_fixed_B(family, n, m, w, num_trials=200)
            entry = {
                "n": n,
                "m": m,
                "family": family,
                "w": w,
                "nonuniformity": nu,
                "recovery_rate": rec,
            }
            results.append(entry)
            print(f"  entropy_ratio={nu['entropy_ratio']}, recovery_rate={rec:.2f}", file=sys.stderr)
    
    output = {
        "experiment": "114-e-op9b-tradeoff-curve",
        "description": "Low-weight B trade-off: non-uniformity vs recovery",
        "date": "2026-06-12",
        "results": results,
    }
    with open("experiments/114-e-op9b-results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("Saved experiments/114-e-op9b-results.json", file=sys.stderr)
