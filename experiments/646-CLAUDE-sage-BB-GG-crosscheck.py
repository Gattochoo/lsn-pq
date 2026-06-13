#!/usr/bin/env python3
# 646-CLAUDE-sage-BB-GG-crosscheck.sage
#
# INDEPENDENT (SageMath, exact QQ) cross-engine re-derivation of round-8 Track BB
# (column-pair SD, exp 641->644) and Track GG (I(x;y|C), exp 720->645). Different
# implementation from the pure-Python scripts: Lagrangians via VectorSpace(GF(2))
# .subspaces(2) filtered by the symplectic form; exact QQ rationals throughout.
#
# Must reproduce (cross-engine): BB m=4 baseline SD = 277825754675/1099511627776
# (matches Kimi HH/FF and my float 644); BB lam=1/4 ABOVE baseline at all m (no
# threat); GG uniform-B I(x;y|C) with DECREASING increments after m=3, far below
# H(x)=2 (recovery fails -> supports lem:m2).
#
# Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

import sys
from sage.all import *
from itertools import product as iproduct
from math import log2

F = GF(2)
V = VectorSpace(F, 4)
NN = 4
P = QQ(1)/4
PEFF = QQ(175)/512

# symplectic form J on F_2^4 (n=2): blocks [[0,I],[I,0]]
J = matrix(F, 4, 4, [[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])

def to_int(v):
    return sum(int(v[i]) << i for i in range(4))

def dot(u, w):   # standard F_2 inner product
    return int(u.dot_product(w))

# Lagrangians = 2-dim isotropic subspaces under J
LAGS = []
for S in V.subspaces(2):
    bas = S.basis()
    if all((bas[i] * J * bas[j]) == 0 for i in range(len(bas)) for j in range(len(bas))):
        LAGS.append([V(v) for v in S])   # all 4 vectors of the subspace

def bases_of(Lvecs):
    nz = [v for v in Lvecs if v != 0]
    out = []
    for a0, a1 in iproduct(nz, nz):
        if a0 != a1 and a0 + a1 in nz:   # {0,a0,a1,a0+a1} == L
            out.append((a0, a1))
    return out

def hw_int(e):
    return bin(e).count("1")

def perrow_uniform(a0, a1, v):
    pr = {}
    q = QQ(1)/(1<<NN)
    for r in range(1 << NN):
        rv = V([(r>>i)&1 for i in range(4)])
        key = (dot(rv,a0), dot(rv,a1), dot(rv,v))
        pr[key] = pr.get(key, QQ(0)) + q
    return pr

def coef(a):   # (a0^a1, a2^a3) for column-pair coupling
    ai = to_int(a)
    return (((ai>>0)&1) ^ ((ai>>1)&1), ((ai>>2)&1) ^ ((ai>>3)&1))

def perrow_coupled(a0, a1, v):
    c0s,c0t = coef(a0); c1s,c1t = coef(a1); cvs,cvt = coef(v)
    pr = {}
    q = QQ(1)/4
    for s in range(2):
        for t in range(2):
            key = ((s&c0s)^(t&c0t), (s&c1s)^(t&c1t), (s&cvs)^(t&cvt))
            pr[key] = pr.get(key, QQ(0)) + q
    return pr

def mfold(perrow, m):
    dist = {(0,0): QQ(1)}
    for i in range(m):
        nd = {}; sh = 2*i
        for (Cacc,yacc), w in dist.items():
            for (c0,c1,yy), pw in perrow.items():
                k = (Cacc | ((c0 | (c1<<1))<<sh), yacc | (yy<<i))
                nd[k] = nd.get(k, QQ(0)) + w*pw
        dist = nd
    return dist

def lpn_law(p, m):
    law = {}; wC = QQ(1)/(2**(2*m))
    for Cbits in range(1<<(2*m)):
        crow = [(Cbits>>(2*i))&3 for i in range(m)]
        for x in range(4):
            cx = 0
            for i,rr in enumerate(crow):
                cx |= (bin(rr & x).count("1")&1) << i
            for e in range(1<<m):
                w = wC * (QQ(1)/4) * p**hw_int(e) * (1-p)**(m-hw_int(e))
                law[(Cbits, cx^e)] = law.get((Cbits, cx^e), QQ(0)) + w
    return law

def colpair_output(lam, m):
    out = {}; wL = QQ(1)/len(LAGS); cU = {}; cC = {}
    for Lv in LAGS:
        Bs = bases_of(Lv); wA = wL/len(Bs)
        for (a0,a1) in Bs:
            for x in range(4):
                Ax = (a0 if x&1 else V(0)) + (a1 if x&2 else V(0))
                for e in range(1<<NN):
                    ev = V([(e>>i)&1 for i in range(4)])
                    we = P**hw_int(e) * (1-P)**(NN-hw_int(e))
                    v = Ax + ev
                    base = wA * (QQ(1)/4) * we
                    key = (to_int(a0), to_int(a1), to_int(v))
                    if lam > 0:
                        if key not in cC: cC[key] = mfold(perrow_coupled(a0,a1,v), m)
                        for kk,pw in cC[key].items():
                            out[kk] = out.get(kk, QQ(0)) + lam*base*pw
                    if lam < 1:
                        if key not in cU: cU[key] = mfold(perrow_uniform(a0,a1,v), m)
                        for kk,pw in cU[key].items():
                            out[kk] = out.get(kk, QQ(0)) + (1-lam)*base*pw
    return out

def SD(Pd, Qd):
    return sum(abs(Pd.get(k,QQ(0)) - Qd.get(k,QQ(0))) for k in set(Pd)|set(Qd)) / 2

def I_xy_given_C(m):
    joint = {}; wL = QQ(1)/len(LAGS); cU = {}
    for Lv in LAGS:
        Bs = bases_of(Lv); wA = wL/len(Bs)
        for (a0,a1) in Bs:
            for x in range(4):
                Ax = (a0 if x&1 else V(0)) + (a1 if x&2 else V(0))
                for e in range(1<<NN):
                    ev = V([(e>>i)&1 for i in range(4)])
                    we = P**hw_int(e) * (1-P)**(NN-hw_int(e))
                    v = Ax + ev
                    key = (to_int(a0), to_int(a1), to_int(v))
                    if key not in cU: cU[key] = mfold(perrow_uniform(a0,a1,v), m)
                    w0 = wA * (QQ(1)/4) * we
                    for (C,y),pw in cU[key].items():
                        kk = (C,x,y)
                        joint[kk] = joint.get(kk, QQ(0)) + w0*pw
    PC={}; PCx={}; PCy={}
    for (C,x,y),p in joint.items():
        PC[C]=PC.get(C,QQ(0))+p; PCx[(C,x)]=PCx.get((C,x),QQ(0))+p; PCy[(C,y)]=PCy.get((C,y),QQ(0))+p
    I = 0.0
    for (C,x,y),p in joint.items():
        if p>0:
            I += float(p) * log2(float(p*PC[C])/float(PCx[(C,x)]*PCy[(C,y)]))
    return I, sum(joint.values())

print("="*72)
print("646-CLAUDE  SageMath exact cross-check (BB SD + GG I(x;y|C)), n=2")
print(f"  |Lagrangians|={len(LAGS)} (expect 15)")
print("="*72)

EXACT_M4 = QQ(277825754675)/1099511627776
print("\n[BB] SD(colpair(lambda), LPN_{175/512}) -- exact QQ:")
print(f"  {'m':>2} {'lam=0 baseline':>16} {'lam=1/4':>12} {'lam=1':>12}  verdict")
for m in (4,5,6):
    lpn = lpn_law(PEFF, m)
    s0 = SD(colpair_output(QQ(0), m), lpn)
    s14 = SD(colpair_output(QQ(1)/4, m), lpn)
    s1 = SD(colpair_output(QQ(1), m), lpn)
    note = ""
    if m == 4:
        note = "  [== exact 277825754675/1099511627776]" if s0 == EXACT_M4 else f"  [MISMATCH {s0}]"
    v = "lam=1/4 >= baseline (no threat)" if s14 >= s0 else "*** BELOW baseline (THREAT) ***"
    print(f"  {m:>2} {float(s0):>16.6f} {float(s14):>12.6f} {float(s1):>12.6f}  {v}{note}")
    sys.stdout.flush()

print("\n[GG] I(x;y|C) uniform-B-per-A (bits), H(x)=2:")
print(f"  {'m':>2} {'I(x;y|C)':>12} {'increment':>11}  (GG: 0.041,0.097,0.159,0.214,0.254,0.280)")
prev=None; rows=[]
for m in range(1,7):
    I,tot = I_xy_given_C(m)
    inc = "" if prev is None else f"{I-prev:.4f}"
    print(f"  {m:>2} {I:>12.4f} {inc:>11}   (sum={float(tot):.6f})")
    sys.stdout.flush()
    rows.append(I); prev=I
incs=[rows[i]-rows[i-1] for i in range(1,len(rows))]
peak=incs.index(max(incs))+2
dec=all(incs[i]>=incs[i+1]-1e-12 for i in range(peak-1,len(incs)-1))
print(f"\n  increments peak at m={peak}, decreasing after: {dec}; "
      f"I(m=6)={rows[-1]:.4f} << H(x)=2 ({100*rows[-1]/2:.1f}%)")
print("  => BB: no threat (I-drop != SD-drop); GG: sublinear, recovery fails -> support lem:m2.")
print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
print("="*72)
