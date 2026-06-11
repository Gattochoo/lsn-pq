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
102 — Claude adjudication check (09:00): the corner question is RECOVERABILITY, not distinguishing.

Kimi's overnight arc framed OP9 as "distinguish P0=(C,Bw) from P1=LPN_{p'}" and concluded
"single-sample detection asymptotically impossible". This script shows that framing is the
WRONG target: the corner asks whether a USABLE marginal-adaptive reduction exists, i.e. whether
x is RECOVERABLE from (C,y). For marginal-uniform (=uniform) B:
  - effective noise of P0 w.r.t. true x  -> 1/2  (rows have weight Theta(n), bias (1/2)^Theta(n))
  - x is NOT recovered by max-agreement  (0-3 / 60 trials, = chance)
  - max-agree/m ~ 0.75 flat = the 2^n-candidate inflation of a 1/2-noise distribution, NOT recovery
A genuine usable LPN_{0.1} would recover x (max-agree ~0.90). Hence P0 is UNUSABLE-as-LPN =>
no usable reduction via uniform B => corner leans CLOSED via the paper's existing M1 +
cor:recovery-barrier; Kimi's "indistinguishable from LPN_0.1" is false in the way that matters.

NOTE (honest, for the record): this rules out the UNIFORM-B case only. The actual OPEN residue
of OP9 (= the M2 residue) is a CLEVER marginal-adaptive B with O(n) LOW-weight rows that still
keep BA marginally uniform. Neither Kimi's experiments nor this check settle that. Corner = OPEN.

No 7th; no break; no security claim. OPEN = LSN.
"""
import random, itertools

def iso_basis(n):
    D = 2 * n
    S = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = random.randint(0, 1); S[i][j] = v; S[j][i] = v
    cols = []
    for k in range(n):
        u = [1 if t == k else 0 for t in range(n)]
        v = [sum(S[i][t] * u[t] for t in range(n)) % 2 for i in range(n)]
        cols.append(u + v)
    return [[cols[c][r] for c in range(n)] for r in range(2 * n)]   # 2n x n

def main():
    random.seed(1)
    p = 0.25
    print(f"{'n':>3} {'m':>4} {'eff_noise_p0':>12} {'x_recovered':>12} {'maxagree/m':>11}")
    for n in [6, 8, 10, 12]:
        D = 2 * n; m = 4 * n; T = 60
        rec = 0; effs = []; mas = []
        for _ in range(T):
            A = iso_basis(n)
            B = [[random.randint(0, 1) for _ in range(D)] for _ in range(m)]   # marginal-uniform
            x = [random.randint(0, 1) for _ in range(n)]
            e = [1 if random.random() < p else 0 for _ in range(D)]
            w = [(sum(A[r][c] * x[c] for c in range(n)) + e[r]) % 2 for r in range(D)]
            C = [[sum(B[i][k] * A[k][c] for k in range(D)) % 2 for c in range(n)] for i in range(m)]
            y = [sum(B[i][k] * w[k] for k in range(D)) % 2 for i in range(m)]
            mis = sum(1 for i in range(m) if (sum(C[i][c] * x[c] for c in range(n)) % 2) != y[i])
            effs.append(mis / m)
            best = -1; bestx = None
            for xb in itertools.product((0, 1), repeat=n):
                ag = sum(1 for i in range(m) if (sum(C[i][c] * xb[c] for c in range(n)) % 2) == y[i])
                if ag > best: best = ag; bestx = xb
            mas.append(best / m)
            if list(bestx) == x: rec += 1
        print(f"{n:>3} {m:>4} {sum(effs)/T:>12.3f} {f'{rec}/{T}':>12} {sum(mas)/T:>11.3f}")
    print("\neff_noise -> 0.5, x not recovered => P0 unusable as LPN => uniform-B reduction is dead")
    print("(consistent with paper M1 + cor:recovery-barrier). Clever low-weight-but-uniform B = OPEN.")

if __name__ == "__main__":
    main()
