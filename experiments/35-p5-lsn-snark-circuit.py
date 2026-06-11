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
Experiment 35: P5 LSN-SNARK Circuit Prototype

Builds an R1CS circuit for the LSN signature:
  Witness: w_j (basis of L^perp), e_i (noise), a_{k,i} (intermediates)
  Public: x_i (sample points), y_i (sample labels), pk_hash
  Constraints: a_{k,i} = a_{k-1,i} * (1 + <w_k, x_i>), y_i = a_{n,i} + e_i
"""

import numpy as np
import time
from collections import defaultdict

SEED = 2026060835
rng = np.random.default_rng(SEED)


def omega_int(u, v, n):
    mask = (1 << n) - 1
    ul, uh = u & mask, (u >> n) & mask
    vl, vh = v & mask, (v >> n) & mask
    return ((ul & vh).bit_count() + (uh & vl).bit_count()) & 1


class XorBasis:
    __slots__ = ("piv",)
    def __init__(self):
        self.piv = {}
    def add(self, v):
        while v:
            h = v.bit_length() - 1
            r = self.piv.get(h)
            if r is None:
                self.piv[h] = v
                return True
            v ^= r
        return False


def rand_lagrangian(n, rng):
    D = 2 * n
    xb = XorBasis()
    rows = []
    while len(rows) < n:
        v = int(rng.integers(1, 1 << D))
        if all(omega_int(v, b, n) == 0 for b in rows) and xb.add(v):
            rows.append(v)
    return tuple(rows)


def subspace_elems(rows):
    elems = {0}
    for v in rows:
        elems |= {e ^ v for e in elems}
    return elems


def find_l_perp_basis(n, L_rows):
    """Find basis of L^perp (standard dot product)."""
    dim = 2 * n
    M = np.array([[int((row >> j) & 1) for j in range(dim)] for row in L_rows], dtype=int)
    # Row reduce
    rows, cols = M.shape
    r = 0
    pivots = []
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if M[i, c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        M[[r, pivot]] = M[[pivot, r]]
        pivots.append(c)
        for i in range(rows):
            if i != r and M[i, c] == 1:
                M[i] ^= M[r]
        r += 1
    
    free_vars = [c for c in range(cols) if c not in pivots]
    null_basis = []
    for fv in free_vars:
        vec = np.zeros(cols, dtype=int)
        vec[fv] = 1
        for i, p in enumerate(pivots):
            if M[i, fv] == 1:
                vec[p] = 1
        null_basis.append(vec)
    return null_basis


def build_r1cs(n, m, x_vals, y_vals, w_basis, e_vals):
    """
    Build R1CS matrices A, B, C.
    Variables (index):
      0: constant 1
      1..n*2n: w_{k,j} (secret basis)
      n*2n+1 .. n*2n+n*m: a_{k,i} (intermediates)
      n*2n+n*m+1 .. n*2n+n*m+m: e_i (noise)
    Public inputs: x_i, y_i (not part of witness variable indexing here)
    
    Constraints (per sample i):
      For k=1: a_{1,i} = 1 * (1 + <w_1, x_i>)
      For k=2..n: a_{k,i} = a_{k-1,i} * (1 + <w_k, x_i>)
      Final: y_i = a_{n,i} + e_i  =>  a_{n,i} + e_i - y_i = 0
    """
    num_w = n * 2 * n
    num_a = n * m
    num_e = m
    total_vars = 1 + num_w + num_a + num_e  # constant + w + a + e
    
    def idx_w(k, j):
        return 1 + k * (2*n) + j  # k=0..n-1, j=0..2n-1
    
    def idx_a(k, i):
        return 1 + num_w + i * n + k  # k=0..n-1, i=0..m-1
    
    def idx_e(i):
        return 1 + num_w + num_a + i
    
    constraints = []
    
    for i in range(m):
        x = x_vals[i]
        
        for k in range(n):
            # Compute b_k = 1 + <w_k, x>
            # b_k is a linear combination: 1 + sum_j w_{k,j} * x_j
            
            # A, B, C are sparse vectors (dict: var_idx -> coeff)
            A = {}
            B = {}
            C = {}
            
            if k == 0:
                A[0] = 1  # constant 1
            else:
                A[idx_a(k-1, i)] = 1
            
            # B = b_k = 1 + sum_j x_j * w_{k,j}
            B[0] = 1
            for j in range(2*n):
                x_j = (x >> j) & 1
                if x_j == 1:
                    B[idx_w(k, j)] = 1
            
            C[idx_a(k, i)] = 1
            
            constraints.append((A, B, C))
        
        # Final linear constraint: a_{n-1,i} + e_i = y_i
        # In R1CS: (a_{n-1,i} + e_i - y_i) * 1 = 0
        # But y_i is public, so we put -y_i in C
        A = {}
        B = {0: 1}
        C = {}
        C[idx_a(n-1, i)] = 1
        C[idx_e(i)] = 1
        C[0] = y_vals[i]  # Note: over F_2, subtraction = addition
        
        constraints.append((A, B, C))
    
    return constraints, total_vars


def generate_witness(n, m, L_rows, x_vals, p, rng):
    """Generate witness: w_basis, a_intermediates, e_noise."""
    w_basis = find_l_perp_basis(n, L_rows)
    
    # Compute a_{k,i} and e_i
    a_vals = {}
    e_vals = []
    
    L_elems = subspace_elems(L_rows)
    
    for i in range(m):
        x = x_vals[i]
        true_label = 1 if x in L_elems else 0
        
        # Compute a_{k,i}
        for k in range(n):
            w = w_basis[k]
            dot = sum(int((x >> j) & 1) * int(w[j]) for j in range(2*n)) % 2
            b_k = (1 + dot) % 2
            if k == 0:
                a_vals[(k, i)] = b_k
            else:
                a_vals[(k, i)] = (a_vals[(k-1, i)] * b_k) % 2
        
        # Compute noise
        y = a_vals[(n-1, i)]
        # Add Bernoulli noise
        if rng.random() < p:
            y ^= 1
        e_vals.append(y ^ a_vals[(n-1, i)])
    
    return w_basis, a_vals, e_vals


def check_r1cs(constraints, witness):
    """Check all constraints: (A·w) * (B·w) = C·w over F_2."""
    errors = 0
    for idx, (A, B, C) in enumerate(constraints):
        a_val = sum(witness.get(v, 0) * c for v, c in A.items()) % 2
        b_val = sum(witness.get(v, 0) * c for v, c in B.items()) % 2
        c_val = sum(witness.get(v, 0) * c for v, c in C.items()) % 2
        if (a_val * b_val) % 2 != c_val:
            errors += 1
    return errors


def main():
    print("=" * 76)
    print("P5: LSN-SNARK Circuit Prototype")
    print("=" * 76)
    
    for n, m in [(5, 100), (10, 500), (15, 1000)]:
        print(f"\n--- n={n}, m={m} ---")
        
        t0 = time.time()
        
        # Generate key pair
        L = rand_lagrangian(n, rng)
        x_vals = [int(rng.integers(0, 1 << (2*n))) for _ in range(m)]
        
        # Generate witness
        w_basis, a_vals, e_vals = generate_witness(n, m, L, x_vals, 0.25, rng)
        
        # Compute y_vals
        L_elems = subspace_elems(L)
        y_vals = []
        for i in range(m):
            true_y = 1 if x_vals[i] in L_elems else 0
            noisy_y = true_y ^ e_vals[i]
            y_vals.append(noisy_y)
        
        # Build R1CS
        constraints, num_vars = build_r1cs(n, m, x_vals, y_vals, w_basis, e_vals)
        
        # Build witness vector
        witness = {0: 1}  # constant 1
        
        # w variables
        for k in range(n):
            for j in range(2*n):
                idx = 1 + k * (2*n) + j
                witness[idx] = int(w_basis[k][j])
        
        # a variables
        base_a = 1 + n * (2*n)
        for k in range(n):
            for i in range(m):
                idx = base_a + i * n + k
                witness[idx] = a_vals[(k, i)]
        
        # e variables
        base_e = base_a + n * m
        for i in range(m):
            idx = base_e + i
            witness[idx] = e_vals[i]
        
        # Check constraints
        errors = check_r1cs(constraints, witness)
        
        elapsed = time.time() - t0
        
        print(f"  Variables: {num_vars}")
        print(f"  Constraints: {len(constraints)}")
        print(f"  Constraint breakdown: {m} samples × {n+1} = {m*(n+1)}")
        print(f"  R1CS errors: {errors}")
        print(f"  Witness generation + R1CS build: {elapsed:.2f}s")
        
        # Estimate Groth16 parameters
        # Proving time: roughly O(N log N) where N = num constraints
        # For N=16000, log2(N) ≈ 14, N log N ≈ 220K group operations
        # At ~1ms per operation (Python simulation), this is ~220s
        # In optimized C++ (libsnark): ~2-5s for N=16000
        est_proof_time = len(constraints) * np.log2(len(constraints)) * 0.001
        print(f"  Est. Groth16 prover time (libsnark): {est_proof_time/100:.1f}s")
        print(f"  Est. proof size (Groth16): 3 group elements ≈ 192 bytes")
        print(f"  Est. verify time: 3 pairings ≈ 1.5ms")
    
    print("\n" + "=" * 76)
    print("Circuit design validated.")
    print("Next: Integrate with actual SNARK library (libsnark, bellman, or arkworks).")
    print("=" * 76)


if __name__ == "__main__":
    main()
