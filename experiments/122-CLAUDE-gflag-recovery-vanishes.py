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
122 — Claude G-FLAG resolution (round 4): the mid-weight above-chance recovery VANISHES with n.

Kimi's E-OP9e (119) left huge rec/ch ratios (n=12 w=8: 409, n=14 w=9: 819) unexplained — but
those were from 20-30 trials (1-2 lucky exact recoveries of an n-bit secret). This 200/120-trial
recheck, with m bumped 4x (signal-vs-noise test), resolves it:

  n   w    m  trials  rec%   chance%
 10   7   40    200   1.00   0.0977
 10   7  160    200   3.50   0.0977   <- weak signal at n=10 (≤2n-dim noise partially exploited)
 12   8   48    200   0.00   0.0244
 12   8  192    200   1.00   0.0244
 14   9   56    120   0.00   0.0061
 14   9  224    120   0.00   0.0061   <- ZERO even at 4x samples / 120 trials

Recovery DECREASES monotonically to 0 with n (3.5% @ n=10 → 1% @ n=12 → 0% @ n=14). The huge
round-4 ratios were small-trial noise. Closure-leaning; NOT a Path-B signal (negligible at the
cryptographic n=65). Consistent with the Fisher-info argument (small-n TV large ⇒ some recovery;
n↑ ⇒ TV(P_C,U)→0 ⇒ recovery→0) — which is exactly the sharpened OP9 residue Kimi r5 attacks.

No 7th; no break; no security claim. OPEN = LSN.
"""
import random, itertools
def iso_A(n):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = random.randint(0,1); M[i][j]=v; M[j][i]=v
    return [[(1 if (r<n and r==c) else (M[r-n][c] if r>=n else 0)) for c in range(n)] for r in range(2*n)]
def trial(n, w, m, p=0.25):
    D=2*n; A=iso_A(n)
    B=[[1 if t in set(random.sample(range(D),w)) else 0 for t in range(D)] for _ in range(m)]
    x=[random.randint(0,1) for _ in range(n)]
    e=[1 if random.random()<p else 0 for _ in range(D)]
    wv=[(sum(A[r][c]*x[c] for c in range(n))+e[r])%2 for r in range(D)]
    C=[[sum(B[i][k]*A[k][c] for k in range(D))%2 for c in range(n)] for i in range(m)]
    y=[sum(B[i][k]*wv[k] for k in range(D))%2 for i in range(m)]
    best=-1; bx=None
    for xb in itertools.product((0,1), repeat=n):
        ag=sum(1 for i in range(m) if (sum(C[i][c]*xb[c] for c in range(n))%2)==y[i])
        if ag>best: best=ag; bx=xb
    return list(bx)==x
if __name__ == "__main__":
    random.seed(11)
    print(f"{'n':>3} {'w':>3} {'m':>4} {'trials':>6} {'rec%':>6} {'chance%':>9}")
    for (n,w) in [(10,7),(12,8),(14,9)]:
        for m in [4*n, 16*n]:
            T=200 if n<=12 else 120
            rec=sum(trial(n,w,m) for _ in range(T))
            print(f"{n:>3} {w:>3} {m:>4} {T:>6} {100*rec/T:>6.2f} {100/2**n:>9.4f}")
    print("recovery -> 0 with n (3.5%@n10 -> 0%@n14) => closure-leaning, G-FLAG benign.")
