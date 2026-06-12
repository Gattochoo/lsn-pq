#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
# 187: CLAUDE independent reproduction of Kimi 181 operational SD((C,z),LPN), n=2.
# Corroborates magnitude+trend (A-dep g: 0.042/0.139/0.290 vs Kimi SA 0.047/0.129/0.297)
# and flags the m-label (m=2 is m=n, not 2n; m=4 is 2n). Sign per Claude 109c6c1.
import itertools
from fractions import Fraction
from collections import defaultdict
def pc(x): return bin(x).count("1")
def om(v,w,n):
    lo=(1<<n)-1
    return (pc((v&lo)&(w>>n))^pc((v>>n)&(w&lo)))&1
def rank(rows):
    piv=[]
    for v in rows:
        x=v
        for p in piv: x=min(x,x^p)
        if x: piv.append(x)
    return len(piv)
n=2; N=2*n
def lagrangians(n):
    levels=[{frozenset([0])}]
    for _ in range(n):
        nxt=set()
        for S in levels[-1]:
            for v in range(1,1<<(2*n)):
                if v in S: continue
                if all(om(v,s,n)==0 for s in S): nxt.add(frozenset(list(S)+[s^v for s in S]))
        levels.append(nxt)
    return list(levels[n])
def bases(n):
    out=[]
    for L in lagrangians(n):
        el=[e for e in L if e]
        def rec(ch):
            if len(ch)==n: out.append(ch[:]);return
            for e in el:
                if rank(ch+[e])==len(ch)+1: rec(ch+[e])
        rec([])
    return out
As=bases(n); assert len(As)==90,len(As)

def Crows(B, cols):          # C=B*A, returns m n-bit rows
    m=len(B)
    return [sum((pc(B[i]&cols[j])&1)<<j for j in range(n)) for i in range(m)]
def Be(B,e):                 # m-bit
    o=0
    for i,b in enumerate(B):
        if pc(b&e)&1: o|=1<<i
    return o
def Cdotx(C,x):              # m-bit: <C_i,x>
    o=0
    for i,ci in enumerate(C):
        if pc(ci&x)&1: o|=1<<i
    return o
pe={e:Fraction(1,4)**pc(e)*Fraction(3,4)**(N-pc(e)) for e in range(1<<N)}
pA=Fraction(1,len(As))

def sd_for_g(m, gfunc):
    redj=defaultdict(Fraction); mC=defaultdict(Fraction)
    perC=defaultdict(lambda:[Fraction(0)]*m); perCw=defaultdict(Fraction)
    BC={}
    for idx,cols in enumerate(As):
        B=gfunc(cols,m); C=tuple(Crows(B,cols)); BC[idx]=(B,C)
        for e in range(1<<N):
            p=pA*pe[e]; ep=Be(B,e); mC[C]+=p; perCw[C]+=p
            for i in range(m):
                if (ep>>i)&1: perC[C][i]+=p
    for idx,cols in enumerate(As):
        B,C=BC[idx]
        for x in range(1<<n):
            cx=Cdotx(C,x)
            for e in range(1<<N):
                z=cx^Be(B,e)
                redj[(C,z)]+=pA*Fraction(1,1<<n)*pe[e]
    nullj=defaultdict(Fraction)
    for C in mC:
        r=[perC[C][i]/perCw[C] for i in range(m)]
        for x in range(1<<n):
            cx=Cdotx(C,x)
            for enz in range(1<<m):
                p=Fraction(1)
                for i in range(m): p*=(r[i] if (enz>>i)&1 else (1-r[i]))
                z=cx^enz
                nullj[(C,z)]+=mC[C]*Fraction(1,1<<n)*p
    keys=set(redj)|set(nullj)
    return float(sum(abs(redj[k]-nullj[k]) for k in keys)/2)

CANON=[0b0001,0b0010,0b0100,0b1000,0b1111,0b0111,0b1011]
def g_fixed(cols,m): return CANON[:m]
def g_Adep(cols,m):
    return [(cols[i%n]^CANON[i]) for i in range(m)]

for m in (2,3,4):
    print(f"m={m} (n={n}, 2n={2*n}): SD[g_fixed]={sd_for_g(m,g_fixed):.4f}  SD[g_Adep]={sd_for_g(m,g_Adep):.4f}")
print("LABEL CHECK: m=2 is m=n (min-determined); m=4 is m=2n. Kimi table calls m=2 '(=2n)'.")
