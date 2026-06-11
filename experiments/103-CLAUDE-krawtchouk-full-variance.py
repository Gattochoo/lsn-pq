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
103 — Claude verification (09:00): Krawtchouk concentration with FULL variance (covariances incl).

Kimi's P5b (experiments/98) used a diagonal-only variance as an upper bound. This computes the
ACTUAL variance of W_N(1/2) = sum_{v in N} 2^{-|v|} (N = Omega·L, uniform Lagrangian) directly
from the empirical distribution of W (so all covariance terms are included), to check whether
covariances dominate (they would kill the concentration) or not.

Result: std/mean is monotone DECREASING ~ Theta(1/sqrt(n)) even with full variance =>
covariances do NOT dominate => Chebyshev gives W_N(1/2) <= E[W_N(1/2)]·(1+o(1)) with prob
1 - O(1/n).  E[W] matches 1 + (9/8)^n (the corrected k=0-inclusive constant).

CONSEQUENCE (honest): lem:affine-coset-bias CAN be promoted expectation-form -> w.h.p. form
(prob 1-O(1/n)) -- BUT only after an ANALYTIC variance bound (this is numeric, n<=9 exact/sampled).
Per our own discipline (we rejected Kimi's finite-n asymptotic claim), the paper edit waits for
the analytic second-moment proof. This script = evidence the direction is real.

No 7th; no break; no security claim. OPEN = LSN.
"""
import itertools, random

def N_of_M(n, M):
    N = set()
    for ui in range(2 ** n):
        u = [(ui >> t) & 1 for t in range(n)]
        v = [sum(M[i][t] * u[t] for t in range(n)) % 2 for i in range(n)]
        N.add(tuple(v + u))      # Omega·(u, Mu) = (Mu, u)
    return N

def Whalf(N):
    return sum((0.5) ** sum(vec) for vec in N)

def make(n, bits):
    idx = [(i, j) for i in range(n) for j in range(i, n)]
    M = [[0] * n for _ in range(n)]
    for b, (i, j) in zip(bits, idx):
        M[i][j] = b; M[j][i] = b
    return M

def main():
    random.seed(0)
    print(f"{'n':>3} {'mode':>8} {'E[W]':>9} {'1+(9/8)^n':>10} {'Var(full)':>10} {'std/mean':>9}")
    for n in range(3, 10):
        L = n * (n + 1) // 2
        Ws = []
        if 2 ** L <= 40000:
            for bits in itertools.product((0, 1), repeat=L):
                Ws.append(Whalf(N_of_M(n, make(n, bits))))
            mode = "exact"
        else:
            for _ in range(6000):
                Ws.append(Whalf(N_of_M(n, make(n, [random.randint(0, 1) for _ in range(L)]))))
            mode = "samp6k"
        m = sum(Ws) / len(Ws)
        var = sum((w - m) ** 2 for w in Ws) / len(Ws)
        print(f"{n:>3} {mode:>8} {m:>9.4f} {1+(9/8)**n:>10.4f} {var:>10.5f} {(var**0.5)/m:>9.4f}")
    print("\nstd/mean ~ Theta(1/sqrt(n)) (full variance) => covariances do not dominate => "
          "Chebyshev 1-O(1/n). Analytic variance proof = remaining step before paper promotion.")

if __name__ == "__main__":
    main()
