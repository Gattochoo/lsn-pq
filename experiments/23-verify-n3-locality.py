# Adjudicator verification of Codex OFA-342 n=3: local-Clifford+perm subgroup orbits
# on the 135 Lagrangians of F2^6 (Codex claims [27,54,54]) and on 63 nonzero ([9,27,27]).
import itertools
from functools import reduce
n=3; D=2*n
def omega(a,b): return reduce(lambda s,i: s ^ (a[i]&b[i+n]) ^ (a[i+n]&b[i]), range(n),0)&1
vecs=[t for t in itertools.product((0,1),repeat=D)]; nz=[v for v in vecs if any(v)]
def transvect(u,x): return x if omega(x,u)==0 else tuple(a^b for a,b in zip(x,u))
# 135 Lagrangians = Sp-orbit of x-space
L0=frozenset(v for v in nz if v[3]==0 and v[4]==0 and v[5]==0)
orb={L0}; fr=[L0]
while fr:
    S=fr.pop()
    for u in nz:
        S2=frozenset(transvect(u,x) for x in S)
        if S2 not in orb: orb.add(S2); fr.append(S2)
lagr=list(orb); assert len(lagr)==135
# local generators: per-qubit transvections (support on (i,i+3)) + adjacent qubit swaps
local_u=[]
for i in range(n):
    e1=tuple(1 if k==i else 0 for k in range(D))
    e2=tuple(1 if k==i+n else 0 for k in range(D))
    e3=tuple(a^b for a,b in zip(e1,e2))
    local_u+=[e1,e2,e3]
def swap(x,i,j):   # swap qubit i<->j: coords (i,i+n)<->(j,j+n)
    x=list(x); x[i],x[j]=x[j],x[i]; x[i+n],x[j+n]=x[j+n],x[i+n]; return tuple(x)
def gens_on(S):
    outs=[frozenset(transvect(u,x) for x in S) for u in local_u]
    outs+=[frozenset(swap(x,0,1) for x in S), frozenset(swap(x,1,2) for x in S)]
    return outs
def orbits(items, gens_on_item):
    seen=set(); sizes=[]
    for it in items:
        if it in seen: continue
        o={it}; fr=[it]
        while fr:
            a=fr.pop()
            for b in gens_on_item(a):
                if b not in o: o.add(b); fr.append(b)
        seen|=o; sizes.append(len(o))
    return sorted(sizes)
Lor=orbits(lagr, gens_on)
def gens_on_vec(x):
    return [transvect(u,x) for u in local_u]+[swap(x,0,1),swap(x,1,2)]
Vor=orbits(nz, gens_on_vec)
print(f"n=3 local-subgroup Lagrangian orbit sizes: {Lor}  (Codex: [27,54,54]) -> {'MATCH' if Lor==[27,54,54] else 'DIFF'}")
print(f"n=3 local-subgroup nonzero  orbit sizes: {Vor}  (Codex: [9,27,27])  -> {'MATCH' if Vor==[9,27,27] else 'DIFF'}")
print(f"full-Sp transitive on 135 Lagrangians: {len(orb)==135}; intransitive local ({len(Lor)} orbits) => barrier persists at n=3")
