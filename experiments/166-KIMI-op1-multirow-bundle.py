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

r"""
OP1 Track A Step 4 — Multi-row bundle correlation measurement.

For n=2,3, enumerate all full-rank isotropic matrices A (bases of Lagrangians).
For each k = 1..2n, measure the k-row bundle off-diagonal and diagonal correlation:

  C_n^{(k)} = E_{A}[ E_{S \subseteq [2n], |S|=k}[ prod_{i in S} (1 + sigma^2 s_i) ] ] - 1

where s_i = (<a_i, x> <a_i, x'>) for off-diag, s_i = <a_i, x> for diag.

This interpolates between k=1 (single-row, settled as LPN in exp/165) and
k=2n (batch, vacuous per exp/163). The research question: at which k does
the S_A=0 inter-row dependence either keep correlation controlled (SD preserved)
or blow up (re-hits the batch wall)?

No closure; no break; no security claim. OPEN = LSN.
"""

import itertools
import json
import math
import time
from collections import defaultdict
from fractions import Fraction

# --- parameters ---
P = 0.25
SIGMA2 = Fraction(4, 3)  # (1-2p)^2 / (p*(1-p)) = (0.5)^2 / (0.25*0.75) = 0.25 / 0.1875 = 4/3


def symplectic_form(v, w, n):
    """Omega(v, w) for v, w in F_2^{2n}, represented as ints."""
    mask = (1 << n) - 1
    v_low = v & mask
    v_high = v >> n
    w_low = w & mask
    w_high = w >> n
    return (bin(v_low & w_high).count('1') + bin(v_high & w_low).count('1')) & 1


def rank_over_f2(rows, n_cols):
    """Rank of matrix over F_2. rows: list of ints, each n_cols bits."""
    mat = rows[:]
    r = 0
    for c in range(n_cols):
        pivot = None
        for i in range(r, len(mat)):
            if (mat[i] >> c) & 1:
                pivot = i
                break
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        for i in range(len(mat)):
            if i != r and ((mat[i] >> c) & 1):
                mat[i] ^= mat[r]
        r += 1
        if r >= len(mat):
            break
    return r


def rref_over_f2(rows, n_cols):
    """Reduced row echelon form over F_2. Returns list of ints."""
    mat = rows[:]
    r = 0
    for c in range(n_cols):
        pivot = None
        for i in range(r, len(mat)):
            if (mat[i] >> c) & 1:
                pivot = i
                break
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        for i in range(len(mat)):
            if i != r and ((mat[i] >> c) & 1):
                mat[i] ^= mat[r]
        r += 1
        if r >= len(mat):
            break
    # Remove zero rows and sort for canonicalization
    result = [row for row in mat if row != 0]
    result.sort()
    return result


def generate_gl(n):
    """Generate all invertible n×n matrices over F_2. Each as list of n ints (row bitmasks)."""
    gl = []
    total = 1 << (n * n)
    for bits in range(total):
        mat = []
        for i in range(n):
            row = (bits >> (i * n)) & ((1 << n) - 1)
            mat.append(row)
        if rank_over_f2(mat, n) == n:
            gl.append(mat)
    return gl


def enumerate_isotropic_subspaces(n):
    """Enumerate all n-dimensional isotropic subspaces of F_2^{2n}.
    Returns list of RREF matrices (each as list of n ints, 2n bits)."""
    dim = 2 * n
    vectors = list(range(1, 1 << dim))  # all nonzero vectors
    seen = set()
    subspaces = []
    for combo in itertools.combinations(vectors, n):
        # Check linear independence
        if rank_over_f2(list(combo), dim) != n:
            continue
        # Check isotropy: Omega(v_i, v_j) = 0 for all i,j
        is_iso = True
        for i in range(n):
            for j in range(i, n):
                if symplectic_form(combo[i], combo[j], n) != 0:
                    is_iso = False
                    break
            if not is_iso:
                break
        if not is_iso:
            continue
        # Canonicalize via RREF
        rref = tuple(rref_over_f2(list(combo), dim))
        if rref not in seen:
            seen.add(rref)
            subspaces.append(list(rref))
    return subspaces


def compute_bundle_correlations(n, subspaces, gl_matrices):
    """Compute correlations for all k=1..2n for given n.
    Returns dict with results."""
    dim = 2 * n
    num_matrices = 0
    # Accumulators: for each k, accumulate sum of products (before -1)
    k_values = list(range(1, dim + 1))
    diag_sum = {k: Fraction(0) for k in k_values}
    off_sum = {k: Fraction(0) for k in k_values}

    # Precompute all subsets of rows for each k
    row_indices = list(range(dim))
    subsets_by_k = {}
    for k in k_values:
        subsets_by_k[k] = list(itertools.combinations(row_indices, k))

    for rref in subspaces:
        # rref is n rows, each dim bits
        for G in gl_matrices:
            num_matrices += 1
            # Compute A_x for x = e_1 and x = e_2
            # y = G^T * x
            # For x = e_1: y = first row of G (since G^T_{i,1} = G_{1,i})
            # For x = e_2: y = second row of G
            y1 = G[0]  # G^T * e_1
            y2 = G[1]  # G^T * e_2

            # A1 = sum of rref rows selected by y1
            A1 = 0
            for i in range(n):
                if (y1 >> i) & 1:
                    A1 ^= rref[i]

            # A2 = sum of rref rows selected by y2
            A2 = 0
            for i in range(n):
                if (y2 >> i) & 1:
                    A2 ^= rref[i]

            # Extract bitmasks for s_i values
            diag_bits = A1  # bit j = <a_j, x1>
            off_bits = A1 & A2  # bit j = <a_j, x1> * <a_j, x2>

            for k in k_values:
                subsets = subsets_by_k[k]
                num_subsets = len(subsets)
                diag_prod_sum = Fraction(0)
                off_prod_sum = Fraction(0)
                for subset in subsets:
                    diag_p = Fraction(1)
                    off_p = Fraction(1)
                    for j in subset:
                        s_diag = (diag_bits >> j) & 1
                        s_off = (off_bits >> j) & 1
                        if s_diag:
                            diag_p *= (1 + SIGMA2)
                        if s_off:
                            off_p *= (1 + SIGMA2)
                    diag_prod_sum += diag_p
                    off_prod_sum += off_p
                diag_avg = diag_prod_sum / num_subsets
                off_avg = off_prod_sum / num_subsets
                diag_sum[k] += diag_avg
                off_sum[k] += off_avg

    # Normalize by number of matrices
    results = []
    for k in k_values:
        diag_product = diag_sum[k] / num_matrices
        off_product = off_sum[k] / num_matrices
        diag_corr = float(diag_product - 1)
        off_corr = float(off_product - 1)
        results.append({
            "k": k,
            "num_subsets": len(subsets_by_k[k]),
            "diag_product_avg": float(diag_product),
            "diag_correlation": diag_corr,
            "offdiag_product_avg": float(off_product),
            "offdiag_correlation": off_corr,
        })

    return {
        "n": n,
        "num_matrices": num_matrices,
        "num_subspaces": len(subspaces),
        "gl_size": len(gl_matrices),
        "k_results": results,
    }


def main():
    start = time.time()
    all_results = []

    for n in [2, 3]:
        print(f"Processing n={n}...")
        t0 = time.time()
        subspaces = enumerate_isotropic_subspaces(n)
        gl = generate_gl(n)
        print(f"  Found {len(subspaces)} isotropic subspaces, {len(gl)} GL matrices")
        res = compute_bundle_correlations(n, subspaces, gl)
        all_results.append(res)
        print(f"  Done in {time.time() - t0:.2f}s")

    output = {
        "metadata": {
            "experiment": "op1-multi-row-bundle",
            "description": "Multi-row bundle correlation for sympLPN SQ under S_A=0",
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "parameters": {
                "p": P,
                "sigma2": str(SIGMA2),
            },
            "notes": [
                "k=1 corresponds to single-row model (settled as LPN in exp/165)",
                "k=2n corresponds to batch model (vacuous per exp/163)",
                "Bundle interpolates between these two extremes",
                "Off-diag uses x=e_1, x'=e_2; diag uses x=e_1",
                "All computations use exact Fractions; output is float",
            ],
        },
        "results": all_results,
    }

    json_path = "experiments/166-KIMI-op1-multirow-bundle.json"
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal time: {time.time() - start:.2f}s")
    print(f"Output written to {json_path}")

    # Print summary table
    print("\nSummary:")
    print(f"{'n':>3} {'k':>3} {'diag_corr':>12} {'offdiag_corr':>14} {'num_subsets':>12}")
    for res in all_results:
        n = res["n"]
        for kr in res["k_results"]:
            print(f"{n:>3} {kr['k']:>3} {kr['diag_correlation']:>12.6f} {kr['offdiag_correlation']:>14.6f} {kr['num_subsets']:>12}")


if __name__ == "__main__":
    main()
