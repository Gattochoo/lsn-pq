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
OP1 Track A — Moment closed-form attempt (m_1, m_2, m_3).

From the bundle correlation expansion:
  E[prod_{i in S}(1 + sigma^2 s_i)] = sum_{j=0}^k C(k,j) sigma^{2j} m_j
where m_j = Pr[j random distinct rows all in (x,x')-quadrant].

m_1 is already closed: m_1 = 2^{2n-2} / (2^{2n}-1) (exp/165).
This script measures m_2 and m_3 exactly for n=2,3 by enumeration,
using the efficient t-count method:
  t = number of rows in Q = popcount(A1 & A2)
  m_j = E_A[ C(t,j) / C(2n,j) ]

The goal is to guess a closed form for m_2 (and m_3) that would
prove fixed-k convergence and the suppression sign for all n.

No closure; no break; no security claim. OPEN = LSN.
"""

import itertools
import json
import time
from fractions import Fraction


def symplectic_form(v, w, n):
    mask = (1 << n) - 1
    v_low = v & mask
    v_high = v >> n
    w_low = w & mask
    w_high = w >> n
    return (bin(v_low & w_high).count('1') + bin(v_high & w_low).count('1')) & 1


def rank_over_f2(rows, n_cols):
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
    result = [row for row in mat if row != 0]
    result.sort()
    return result


def enumerate_isotropic_subspaces(n):
    dim = 2 * n
    vectors = list(range(1, 1 << dim))
    seen = set()
    subspaces = []
    for combo in itertools.combinations(vectors, n):
        if rank_over_f2(list(combo), dim) != n:
            continue
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
        rref = tuple(rref_over_f2(list(combo), dim))
        if rref not in seen:
            seen.add(rref)
            subspaces.append(list(rref))
    return subspaces


def generate_gl(n):
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


def compute_moments(n, subspaces, gl_matrices):
    """Compute m_1, m_2, m_3 exactly for given n."""
    dim = 2 * n
    num_matrices = 0
    # Accumulate sum of C(t,j) for j=1,2,3
    sum_c_t_1 = Fraction(0)
    sum_c_t_2 = Fraction(0)
    sum_c_t_3 = Fraction(0)

    # Precompute denominators
    denom_1 = Fraction(dim)
    denom_2 = Fraction(dim * (dim - 1), 2)
    denom_3 = Fraction(dim * (dim - 1) * (dim - 2), 6)

    for rref in subspaces:
        for G in gl_matrices:
            num_matrices += 1
            y1 = G[0]  # G^T * e1
            y2 = G[1]  # G^T * e2

            A1 = 0
            for i in range(n):
                if (y1 >> i) & 1:
                    A1 ^= rref[i]
            A2 = 0
            for i in range(n):
                if (y2 >> i) & 1:
                    A2 ^= rref[i]

            off_bits = A1 & A2
            t = bin(off_bits).count('1')  # number of rows in Q

            sum_c_t_1 += Fraction(t)
            sum_c_t_2 += Fraction(t * (t - 1), 2)
            if t >= 3:
                sum_c_t_3 += Fraction(t * (t - 1) * (t - 2), 6)

    m1 = (sum_c_t_1 / num_matrices) / denom_1
    m2 = (sum_c_t_2 / num_matrices) / denom_2
    m3 = (sum_c_t_3 / num_matrices) / denom_3

    return {
        "n": n,
        "num_matrices": num_matrices,
        "m1": {"fraction": str(m1), "float": float(m1)},
        "m2": {"fraction": str(m2), "float": float(m2)},
        "m3": {"fraction": str(m3), "float": float(m3)},
        "closed_form_m1": str(Fraction(2**(2*n - 2), 2**(2*n) - 1)),
        "m1_match": m1 == Fraction(2**(2*n - 2), 2**(2*n) - 1),
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
        res = compute_moments(n, subspaces, gl)
        all_results.append(res)
        print(f"  m1 = {res['m1']['fraction']} = {res['m1']['float']:.6f} (closed: {res['closed_form_m1']}, match: {res['m1_match']})")
        print(f"  m2 = {res['m2']['fraction']} = {res['m2']['float']:.6f}")
        print(f"  m3 = {res['m3']['fraction']} = {res['m3']['float']:.6f}")
        print(f"  Done in {time.time() - t0:.2f}s")

    output = {
        "metadata": {
            "experiment": "op1-moments-closed-form",
            "description": "Exact moments m_1, m_2, m_3 for n=2,3 via enumeration",
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "notes": [
                "m_j = E_A[C(t,j) / C(2n,j)] where t = number of rows in (x,x')-quadrant",
                "m_1 closed form: 2^{2n-2} / (2^{2n}-1)",
                "Goal: guess closed form for m_2, m_3 from n=2,3 data",
            ],
        },
        "results": all_results,
    }

    json_path = "experiments/167-KIMI-op1-moments-closed-form.json"
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal time: {time.time() - start:.2f}s")
    print(f"Output written to {json_path}")


if __name__ == "__main__":
    main()
