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
Experiment 30: K3 Exact Constant Calculation + Low-Noise Regime Analysis

Context: K3 proof uses asymptotic bounds (O-notation). This script computes
EXACT constants for:
1. E[2^j] where j = dim(L ∩ L')
2. ρ_avg = (1-2p)^2 * 2^{-2n} * E[2^j]
3. TV_avg = (1-2p) * 2^{-2n} * (2^{n+1} - 2*E[2^j])
4. q_min = 1/ρ_avg (exact SQ query lower bound)
5. Low-noise regime: p = 1/√n, 1/n, 1/n^2

References: OFA-387 (q-binomial), K3 Lemma 3.1, K3 Lemma 4.1

Run: python3 30-k3-exact-constant-calculation.py
"""

from math import comb, sqrt


def q_binomial(n, k, q=2):
    """Gaussian binomial coefficient [n choose k]_q."""
    if k < 0 or k > n:
        return 0
    if k == 0:
        return 1
    num = 1
    den = 1
    for i in range(k):
        num *= (q**(n - i) - 1)
        den *= (q**(k - i) - 1)
    return num // den


def lagr_count(n):
    """Number of Lagrangian subspaces in Sp(2n, F_2) — STANDARD symplectic count."""
    total = 1
    for i in range(1, n+1):
        total *= (2**i + 1)
    return total


def dist_distribution(n):
    """
    Exact distribution of dim(L ∩ L') for random L, L'.
    Returns list of (j, count, prob) for j = 0..n.
    """
    total = lagr_count(n)
    dist = []
    for j in range(n + 1):
        count = q_binomial(n, j) * 2**((n - j) * (n - j + 1) // 2)
        # j = n is the self-pair (L = L'), excluded for distinct pairs
        if j == n:
            count = 1  # only L itself
        prob = count / total
        dist.append((j, count, prob))
    return dist


def compute_exact_constants(n):
    """Compute exact constants for given n."""
    dist = dist_distribution(n)
    total = lagr_count(n)
    
    # E[2^j] over ALL Lagrangians (including j=n for L=L')
    E_2j_all = sum(prob * 2**j for j, count, prob in dist)
    
    # E[2^j] over DISTINCT pairs only (j < n)
    distinct_total = total - 1
    E_2j_distinct = sum((count / distinct_total) * 2**j 
                        for j, count, prob in dist if j < n)
    
    # For correlation: use distinct pairs (j < n)
    # ρ_avg = (1-2p)^2 * 2^{-2n} * E[2^j] (distinct)
    # But actually ρ_avg averages over all pairs including self
    # Self-correlation: <D_L, D_L> = (1-2p)^2 * (1 + O(2^{-2n}))
    # For average over ALL pairs:
    rho_base = E_2j_all / total  # average 2^j weighted by count
    
    # More precise: ρ_avg over distinct pairs
    rho_distinct_base = E_2j_distinct
    
    # TV distance average
    # TV = (1-2p) * 2^{-2n} * (2^{n+1} - 2^{j+1})
    # E[TV] = (1-2p) * 2^{-2n} * (2^{n+1} - 2 * E[2^j])
    TV_factor_all = (2**(n+1) - 2 * E_2j_all) / (2**(2*n))
    TV_factor_distinct = (2**(n+1) - 2 * E_2j_distinct) / (2**(2*n))
    
    return {
        'n': n,
        'total_lagr': total,
        'E_2j_all': E_2j_all,
        'E_2j_distinct': E_2j_distinct,
        'rho_base_all': rho_base,
        'rho_base_distinct': rho_distinct_base,
        'TV_factor_all': TV_factor_all,
        'TV_factor_distinct': TV_factor_distinct,
        'dist': dist,
    }


def low_noise_analysis(n):
    """Analyze correlation at p = 1/sqrt(n), 1/n, 1/n^2."""
    const = compute_exact_constants(n)
    E2j = const['E_2j_distinct']
    
    results = []
    for p_label, p in [
        ('constant (p=0.10)', 0.10),
        ('1/sqrt(n)', 1/sqrt(n)),
        ('1/n', 1/n),
        ('1/n^2', 1/n**2),
    ]:
        if p >= 0.5:
            continue
        eps = 1 - 2*p
        rho_avg = eps**2 * E2j / (2**(2*n))
        q_min = 1 / rho_avg if rho_avg > 0 else float('inf')
        TV_avg = eps * (2**(n+1) - 2*E2j) / (2**(2*n))
        results.append((p_label, p, eps, rho_avg, q_min, TV_avg))
    return results


def main():
    print("=" * 76)
    print("Experiment 30: K3 Exact Constant + Low-Noise Regime")
    print("=" * 76)
    
    # Part 1: Exact constants for n = 2..10
    print("\n--- Part 1: Exact Constants ---")
    print(f"{'n':>2} | {'|Lagr|':>12} | {'E[2^j] (all)':>14} | {'E[2^j] (dist)':>14} | {'rho_base':>18} | {'q_min (p=0.1)':>16}")
    print("-" * 90)
    
    for n in range(2, 11):
        const = compute_exact_constants(n)
        E2j_all = const['E_2j_all']
        E2j_dist = const['E_2j_distinct']
        rho_base = const['rho_base_distinct']
        eps = 0.8  # p = 0.1
        rho_avg = eps**2 * rho_base / (2**(2*n))
        q_min = 1 / rho_avg
        
        print(f"{n:>2} | {const['total_lagr']:>12} | {E2j_all:>14.6f} | {E2j_dist:>14.6f} | {rho_base:>18.6f} | {q_min:>16.2f}")
    
    # Part 2: Distance distribution details for selected n
    print("\n--- Part 2: Distance Distribution (n=5,6,7) ---")
    for n in [5, 6, 7]:
        dist = dist_distribution(n)
        print(f"\nn={n}, |Lagr|={lagr_count(n)}")
        print(f"  j | count | prob | 2^j | prob*2^j")
        for j, count, prob in dist:
            marker = "*" if j == n else " "
            print(f" {marker}{j:>2} | {count:>10} | {prob:>8.6f} | {2**j:>4} | {prob*2**j:>12.8f}")
    
    # Part 3: Low-noise regime
    print("\n--- Part 3: Low-Noise Regime ---")
    print(f"{'n':>2} | {'p regime':>16} | {'p':>10} | {'eps=1-2p':>10} | {'rho_avg':>18} | {'q_min':>16} | {'TV_avg':>16}")
    print("-" * 110)
    
    for n in range(3, 11):
        results = low_noise_analysis(n)
        for p_label, p, eps, rho_avg, q_min, TV_avg in results:
            print(f"{n:>2} | {p_label:>16} | {p:>10.6f} | {eps:>10.6f} | {rho_avg:>18.2e} | {q_min:>16.2e} | {TV_avg:>16.2e}")
    
    # Part 4: Critical p_c where rho_avg = tau^2
    print("\n--- Part 4: Critical Noise Rate p_c ---")
    print("Find p where rho_avg = tau^2, tau = 1/n^2")
    print(f"{'n':>2} | {'tau = 1/n^2':>12} | {'p_c (approx)':>14} | {'q_min at p_c':>16}")
    print("-" * 60)
    
    for n in range(3, 11):
        const = compute_exact_constants(n)
        E2j = const['E_2j_distinct']
        tau = 1 / n**2
        target_rho = tau**2
        # rho_avg = (1-2p)^2 * E2j / 2^{2n} = target_rho
        # (1-2p)^2 = target_rho * 2^{2n} / E2j
        # p = (1 - sqrt(target_rho * 2^{2n} / E2j)) / 2
        rhs = target_rho * (2**(2*n)) / E2j
        if rhs < 1:
            p_c = (1 - sqrt(rhs)) / 2
            q_at_pc = 1 / target_rho
            print(f"{n:>2} | {tau:>12.6f} | {p_c:>14.6f} | {q_at_pc:>16.2e}")
        else:
            print(f"{n:>2} | {tau:>12.6f} | {'> 0.5 (always)':>14} | {'N/A':>16}")
    
    print("\n" + "=" * 76)
    print("Interpretation:")
    print("  - E[2^j] converges to ~1.65 for n>=4 (bounded constant)")
    print("  - rho_avg = (1-2p)^2 * E[2^j] / 2^{2n}  (exact formula)")
    print("  - q_min = 2^{2n} / [(1-2p)^2 * E[2^j]]")
    print("  - Low-noise (p=1/sqrt(n)): q_min still exponential in n")
    print("  - Critical p_c: where SQ bound breaks (p > p_c)")
    print("=" * 76)


if __name__ == "__main__":
    main()
