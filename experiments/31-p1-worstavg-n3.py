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
P1 Verification for n=3 using Stab(L) semidirect product structure.
Stab(L) ≅ GL(3,F_2) ⋉ Sym^2(F_2^3), |Stab| = 168 * 64 = 10,752.
"""

import numpy as np
from itertools import product

def mat_mul(A, B, mod=2):
    return (A @ B) % mod

def mat_vec_mul(A, v, mod=2):
    return (A @ v) % mod

# ---------------------------------------------------------------------------
# GL(3, F_2): all 3x3 invertible matrices over F_2
# ---------------------------------------------------------------------------

def generate_gl3():
    gl = []
    for bits in range(2**9):
        M = np.zeros((3,3), dtype=int)
        temp = bits
        for i in range(3):
            for j in range(3):
                M[i,j] = temp & 1
                temp >>= 1
        if np.linalg.det(M) % 2 == 1:
            gl.append(M)
    return gl

# ---------------------------------------------------------------------------
# Sym^2(F_2^3): 3x3 symmetric matrices
# ---------------------------------------------------------------------------

def generate_sym3():
    sym = []
    # Symmetric 3x3 over F_2: 6 free variables (diagonal: 3, upper: 3)
    for bits in range(2**6):
        S = np.zeros((3,3), dtype=int)
        temp = bits
        for i in range(3):
            S[i,i] = temp & 1
            temp >>= 1
        for i in range(3):
            for j in range(i+1, 3):
                S[i,j] = S[j,i] = temp & 1
                temp >>= 1
        sym.append(S)
    return sym

# ---------------------------------------------------------------------------
# Stab(L) = {(A, S) : A ∈ GL(3), S ∈ Sym^2(3)}
# Action: (A, S) acts as block matrix [A, S*(A^T)^{-1}; 0, (A^T)^{-1}]
# On standard basis: L = span{e1,e2,e3}, V/L = span{e4,e5,e6}
# ---------------------------------------------------------------------------

def make_stab_element(A, S):
    """Create 6x6 symplectic matrix from (A, S)."""
    AT_inv = np.linalg.inv(A.T) % 2
    # Ensure integer entries
    AT_inv = AT_inv.astype(int) % 2
    B = mat_mul(S, AT_inv)
    M = np.zeros((6,6), dtype=int)
    M[:3, :3] = A
    M[:3, 3:] = B
    M[3:, 3:] = AT_inv
    return M % 2

def generate_stab():
    gl = generate_gl3()
    sym = generate_sym3()
    stab = []
    for A in gl:
        for S in sym:
            stab.append(make_stab_element(A, S))
    return stab

# ---------------------------------------------------------------------------
# Verify Stab acts transitively on L\{0}
# ---------------------------------------------------------------------------

def verify_n3():
    print("=" * 70)
    print("P1 Verification: n=3")
    print("=" * 70)
    
    gl = generate_gl3()
    sym = generate_sym3()
    print(f"\n[1] |GL(3,F_2)| = {len(gl)} (expected: 168)")
    print(f"    |Sym^2(F_2^3)| = {len(sym)} (expected: 64)")
    print(f"    |Stab(L)| = {len(gl)*len(sym)} (expected: 10,752)")
    
    print("\n[2] Generating Stab(L)...")
    stab = generate_stab()
    print(f"    Generated: {len(stab)}")
    
    # Standard Lagrangian: L = span{e1, e2, e3}
    e1 = np.array([1,0,0,0,0,0], dtype=int)
    e2 = np.array([0,1,0,0,0,0], dtype=int)
    e3 = np.array([0,0,1,0,0,0], dtype=int)
    L = [e1, e2, e3]
    
    # Check all elements of Stab fix L
    print("\n[3] Verifying Stab fixes L...")
    all_fix = True
    for M in stab:
        for v in L:
            w = mat_vec_mul(M, v)
            # w should be in span(L)
            if w[3] != 0 or w[4] != 0 or w[5] != 0:
                all_fix = False
                break
        if not all_fix:
            break
    print(f"    All elements fix L: {all_fix}")
    
    # Orbits on nonzero vectors in L
    print("\n[4] Computing orbits of Stab on L\\{{0}}...")
    nonzero_L = []
    for bits in range(1, 8):
        v = np.zeros(6, dtype=int)
        for i in range(3):
            if bits & (1 << i):
                v += L[i]
        v %= 2
        nonzero_L.append(v)
    
    orbits = []
    seen = set()
    for v in nonzero_L:
        key = tuple(v)
        if key in seen:
            continue
        orbit = set()
        for M in stab:
            w = mat_vec_mul(M, v)
            orbit.add(tuple(w))
        for w in orbit:
            seen.add(w)
        orbits.append(orbit)
    
    print(f"    Number of orbits: {len(orbits)}")
    print(f"    Orbit sizes: {[len(o) for o in orbits]}")
    print(f"    Transitive on L\\{{0}}: {len(orbits) == 1}")
    
    # Noise inhomogeneity
    print("\n[5] Verifying fresh noise inhomogeneity...")
    # L0 = vectors in L
    L0_set = set()
    for bits in range(8):
        v = np.zeros(6, dtype=int)
        for i in range(3):
            if bits & (1 << i):
                v += L[i]
        v %= 2
        L0_set.add(tuple(v))
    
    V = [np.array(v, dtype=int) for v in product([0,1], repeat=6)]
    # Worst-case noise: eta(x) = 0 for x in L, eta(x) = 1 for x not in L
    eta = {tuple(v): (0 if tuple(v) in L0_set else 1) for v in V}
    
    # Add fresh Bernoulli(0.25) noise
    np.random.seed(42)
    xi = {tuple(v): np.random.binomial(1, 0.25) for v in V}
    eta_prime = {k: (eta[k] ^ xi[k]) for k in eta}
    
    eta_L = [eta_prime[tuple(v)] for v in V if tuple(v) in L0_set and any(v)]
    eta_out = [eta_prime[tuple(v)] for v in V if tuple(v) not in L0_set]
    
    print(f"    Noise rate on L\\{{0}}: {sum(eta_L)/len(eta_L):.3f}")
    print(f"    Noise rate outside L: {sum(eta_out)/len(eta_out):.3f}")
    print(f"    INHOMOGENEOUS: {sum(eta_L)/len(eta_L) != sum(eta_out)/len(eta_out)}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    verify_n3()
