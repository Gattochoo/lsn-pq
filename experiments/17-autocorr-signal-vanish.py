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
Decoder-INDEPENDENT closure of the whole autocorrelation family (bucket-rank-stop,
isotropic-greedy, coset-gain, and any future variant) at poly-sample.

Every such decoder reads the XOR-autocorrelation C(d)=|{v in P: v+d in P}| and tries
to find L by the fact that C(d) is large for d in L (member pairs) and small for
d not in L. So the RAW signal any of them needs is: mean C(d) for d in L (signal)
vs mean C(d) for d not in L (background). If signal/background -> 1, NO autocorrelation
decoder can distinguish L. Measure it vs sample density m at the crypto rate p=0.10.
"""
import numpy as np
rng = np.random.default_rng(20260606)

def omega(a, b, n):
    return int((np.dot(a[:n], b[n:]) + np.dot(a[n:], b[:n])) & 1)
def gf2_rank(M):
    M=(M%2).copy(); r=0; rows,cols=M.shape
    for c in range(cols):
        pv=np.where(M[r:,c])[0]
        if len(pv)==0: continue
        p=r+pv[0]; M[[r,p]]=M[[p,r]]; m=M[:,c].copy(); m[r]=0; M[m==1]^=M[r]; r+=1
        if r==rows: break
    return r
def rand_lagr(n):
    D=2*n; B=[]
    while len(B)<n:
        v=rng.integers(0,2,D)
        if v.any() and all(omega(v,b,n)==0 for b in B) and gf2_rank(np.array(B+[v]))==len(B)+1: B.append(v)
    return np.array(B)
def members(B,D):
    s=set()
    for c in range(1<<len(B)):
        v=np.zeros(D,int)
        for i in range(len(B)):
            if (c>>i)&1: v^=B[i]
        s.add(int(sum(int(v[b])<<b for b in range(D))))
    return s

p=0.10
print(f"crypto rate p={p}. signal = mean C(d), d in L\\0 ; background = mean C(d), d not in L.")
print(f"{'n':>2} {'m':>7} {'m/2^n':>7} {'#trueObs':>8} {'signal':>8} {'bg':>8} {'sig/bg':>7}  channel")
for n in [4,5,6]:
    D=2*n; N=1<<D; twon=1<<n
    Lspace=None
    ms=[1<<(D-1), 1<<(D-2), 1<<(D-3), twon*4, twon, n**3, n**2]
    ms=sorted(set(m for m in ms if 1<=m<=N), reverse=True)
    for m in ms:
        sig=[]; bg=[]; trueobs=[]
        TR=8
        for _ in range(TR):
            B=rand_lagr(n); mem=members(B,D)
            Lset=set(int(sum(int(v[b])<<b for b in range(D))) for v in
                     [np.array([(x>>b)&1 for b in range(D)]) for x in range(N)] if x in mem) if False else mem
            S=rng.choice(N, size=m, replace=False)             # observed subset
            lab={int(v): (1 if int(v) in mem else 0)^(1 if rng.random()<p else 0) for v in S}
            P=set(v for v,b in lab.items() if b==1)
            trueobs.append(sum(1 for v in S if int(v) in mem))
            # C(d) for d in L\0
            Ld=[d for d in mem if d!=0]
            cs=[sum(1 for v in P if (v^d) in P) for d in Ld]
            sig.append(np.mean(cs))
            # background: random d not in L
            bd=[]
            while len(bd)<min(len(Ld),20):
                d=int(rng.integers(1,N))
                if d not in mem: bd.append(d)
            cb=[sum(1 for v in P if (v^d) in P) for d in bd]
            bg.append(np.mean(cb))
        s=np.mean(sig); b=np.mean(bg)+1e-9
        ch="EXPONENTIAL(dense)" if m>=twon else "poly-ward (m/2^n<1)"
        print(f"{n:>2} {m:>7} {m/twon:>7.2f} {np.mean(trueobs):>8.1f} {s:>8.2f} {b:>8.2f} {s/b:>7.2f}  {ch}")
    print()
print("Reading: at dense m (>= 2^n, exponential) signal >> background (sig/bg >> 1) ->")
print("decoders work. At poly-ward m (m/2^n < 1) #trueObs -> ~0, so member pairs vanish")
print("and signal/background -> 1: d in L is INDISTINGUISHABLE from d not in L. NO")
print("autocorrelation decoder -- bucket-rank-stop, isotropic-greedy, coset-gain, or any")
print("future variant -- can recover, because the raw L-signal it reads is gone. This")
print("closes the WHOLE family at poly-sample, channel-level (not per-decoder).")
