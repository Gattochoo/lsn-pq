#!/usr/bin/env python3
# Copyright 2026 Kwanghoo Choo
# SPDX-License-Identifier: Apache-2.0
"""190: CLAUDE independent verification of Kimi's uniform-B lem:m2 SD (187-189).

From-scratch (independent of experiments/lib) computation of the exact output SD for
uniform B per A. Confirms Kimi's values AND adds the load-bearing extra analyses:
  - reduces (C,y) row distribution as Unif(rowspace([A|Ax+e])), m iid rows;
  - reproduces Kimi 187 exactly: n=2 m=3 -> 3225/32768, m=4 -> 5903/32768
    (after fixing an initial key-layout bug in my own LPN target);
  - p_eff = output per-coordinate noise rate = (1-(1-p)^{2n})/2 -> 1/2 as n grows
    (so the output is LPN at noise -> 1/2, NOT LPN_{1/4}: 0.342 n=2, 0.411 n=3, ...);
  - SD vs MATCHED-rate LPN_{p_eff} (isolates the correlation, the real lem:m2 question):
    grows with m (0.070, 0.162, 0.253, 0.324 for n=2 m=2..5) -> correlation is
    detectable and increasingly so -> SUPPORTS lem:m2 along the relevant m-axis.
Verdict context: Kimi's NUMBERS are correct; the 189 "threatens lem:m2" reading is a
regime/target conflation (fixed small m + LPN_{1/4} target + lem:m1's noise->1/2 regime).
"""

from fractions import Fraction
from itertools import product as iproduct

def popcount(x): return bin(x).count("1")
def om(u,v,n):
    lo=(1<<n)-1
    return (popcount((u&lo)&(v>>n))^popcount((u>>n)&(v&lo)))&1

def lagr_bases(n):
    """one basis (n columns in F_2^{2n}) per Lagrangian subspace."""
    N=2*n; seen={}
    # BFS isotropic subspaces dim n
    levels=[{frozenset([0])}]
    for _ in range(n):
        nxt=set()
        for S in levels[-1]:
            for v in range(1,1<<N):
                if v in S: continue
                if all(om(v,s,n)==0 for s in S):
                    nxt.add(frozenset(list(S)+[s^v for s in S]))
        levels.append(nxt)
    bases=[]
    for L in levels[n]:
        elems=sorted(e for e in L if e)
        # greedy independent basis
        basis=[]; 
        def rank(cols):
            piv=[];r=0
            for v in cols:
                x=v
                for p in piv: x=min(x,x^p)
                if x: piv.append(x);r+=1
            return r
        for e in elems:
            if rank(basis+[e])==len(basis)+1:
                basis.append(e)
                if len(basis)==n: break
        bases.append(tuple(basis))
    return bases

def colspace(cols):
    sp={0}
    for c in cols:
        sp|={s^c for s in sp}
    return sp

def out_dist(n,m,p=Fraction(1,4)):
    """exact output distribution of (C,y) for uniform B per A, as counts/denom over key=(C<<m)|y... 
       represented compactly. Returns dict key->Fraction prob."""
    N=2*n; bases=lagr_bases(n)
    pe={e: (p**popcount(e))*((1-p)**(N-popcount(e))) for e in range(1<<N)}
    dist={}
    wA=Fraction(1,len(bases)); wx=Fraction(1,1<<n)
    for A in bases:
        csA=colspace(list(A))
        for x in range(1<<n):
            Ax=0
            for j in range(n):
                if (x>>j)&1: Ax^=A[j]
            for e in range(1<<N):
                pee=pe[e]
                if pee==0: continue
                col=Ax^e
                # augmented columns = A[0..n-1], col  (each 2n-bit); row b-> (b.A_0,...,b.col) in F_2^{n+1}
                augcols=list(A)+[col]
                # rowspace R = {(b.augcols[0],...): b in F_2^{2n}} ; dim = rank of augcols as vectors
                def rank(cols):
                    piv=[];r=0
                    for v in cols:
                        xx=v
                        for pv in piv: xx=min(xx,xx^pv)
                        if xx: piv.append(xx);r+=1
                    return r
                rk=rank(augcols)               # = n + (1 if e not in csA else 0)
                Rsize=1<<rk
                # enumerate R = image of b->(n+1)-vector. dim rk, so 2^rk elements.
                # build R by enumerating a basis of the image.
                # image vectors: for each b, v=(<b,augcols[j]>)_j. Basis: pick 2n unit b's -> rows = augcols^T columns? 
                # Simpler: R = column space of the (n+1) x 2n matrix whose row j is augcols[j] (as 2n-bit). 
                # i.e. R = { (a_0,...,a_n) : exists b, a_j=<b,augcols[j]> } = row space of matrix M with rows=augcols.
                # = set of F_2^{n+1} vectors orthogonal-complement style; compute as span of columns of M^T.
                # M is (n+1)x2n with row j = augcols[j]. R = col space of M (m=n+1 rows)... 
                # R = { M b : b in F_2^{2n} } where (Mb)_j = <augcols[j], b>. So R = column space of M viewed n+1 dim.
                # Build R by Gaussian: R spanned by the 2n columns of M. column k = (bit k of augcols[0],...,bit k of augcols[n]).
                cols_of_M=[]
                for k in range(N):
                    cv=0
                    for j in range(n+1):
                        if (augcols[j]>>k)&1: cv|=(1<<j)
                    cols_of_M.append(cv)
                R={0}
                for cv in cols_of_M:
                    R|={r^cv for r in R}
                assert len(R)==Rsize,(len(R),Rsize)
                Rlist=sorted(R)
                wcell=wA*wx*pee
                prow=Fraction(1,Rsize)
                # m iid rows over R; each row is (n+1)-bit value v: C-part = v>>1? define c=v's high n bits, ybit=v&1
                # accumulate product distribution. For SD we need full joint over m rows.
                # key: concatenappend rows. row value occupies (n+1) bits.
                from itertools import product as ipr
                for rows in ipr(Rlist, repeat=m):
                    key=0
                    for rv in rows:
                        key=(key<<(n+1))|rv
                    dist[key]=dist.get(key,Fraction(0))+wcell*(prow**m)
    return dist

def lpn_dist(n,m,pp):
    """LPN_{pp}: C uniform F_2^{m x n}, x uniform F_2^n, e'~Bern(pp)^m, y=Cx+e'. key same layout (rows of (c_i,y_i))."""
    dist={}
    # iterate C as m rows each n bits, x in F_2^n, e' in F_2^m
    wC=Fraction(1,1<<(n*m)); wx=Fraction(1,1<<n)
    pe={ep:(pp**popcount(ep))*((1-pp)**(m-popcount(ep))) for ep in range(1<<m)}
    for Cbits in range(1<<(n*m)):
        rows_c=[(Cbits>>((n)*i))&((1<<n)-1) for i in range(m)]
        for x in range(1<<n):
            for ep in range(1<<m):
                key=0; pep=pe[ep]
                if pep==0: continue
                for i in range(m):
                    ci=rows_c[i]
                    yi=(popcount(ci&x)&1)^((ep>>i)&1)
                    rv=ci|(yi<<n)
                    key=(key<<(n+1))|rv
                dist[key]=dist.get(key,Fraction(0))+wC*wx*pep
    return dist

def SD(d1,d2):
    keys=set(d1)|set(d2)
    return sum(abs(d1.get(k,Fraction(0))-d2.get(k,Fraction(0))) for k in keys)/2

def peff(n,p=Fraction(1,4)):
    N=2*n
    return (1-(1-p)**N)/2

import sys
for (n,m) in [(2,2),(2,3),(2,4),(2,5)]:
    pe_=peff(n)
    od=out_dist(n,m)
    sd_quarter=SD(od, lpn_dist(n,m,Fraction(1,4)))
    sd_matched=SD(od, lpn_dist(n,m,pe_))
    print(f"n={n} m={m}: p_eff={float(pe_):.4f} | SD vs LPN_1/4={sd_quarter}={float(sd_quarter):.4f} | SD vs LPN_matched({pe_})={sd_matched}={float(sd_matched):.4f}")
    sys.stdout.flush()
