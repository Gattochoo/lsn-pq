"""
Independent verification of Codex's Sp(4,2)-on-Lagrangians baseline (n=2).
Codex fixes: 15 Lagrangians, group order 720, transitive action. Cross-check all
three from scratch (enumeration + transvection orbit), plus the stabilizer order.
"""
import itertools
from functools import reduce

# F2^4 with standard symplectic form Omega: coords (x1,x2,p1,p2)=(0,1,2,3)
def omega(u, v):
    return (u[0]&v[2]) ^ (u[2]&v[0]) ^ (u[1]&v[3]) ^ (u[3]&v[1])

vecs = [t for t in itertools.product((0,1), repeat=4)]
nonzero = [v for v in vecs if any(v)]

def span_key(u, w):
    # canonical key of the 2-dim subspace <u,w>: the frozenset of its 3 nonzero elts
    c = tuple(a ^ b for a, b in zip(u, w))
    return frozenset({u, w, c})

# 1) enumerate all 2-dim subspaces, filter Lagrangian (isotropic 2-dim)
two_dim = set()
for u, w in itertools.combinations(nonzero, 2):
    if u == w:
        continue
    two_dim.add(span_key(u, w))
lagr = {S for S in two_dim if all(omega(a, b) == 0 for a in S for b in S)}
print(f"#2-dim subspaces      = {len(two_dim)}   (expect 35 = Gauss-binom[4,2]_2)")
print(f"#Lagrangians          = {len(lagr)}   (Codex: 15)  -> {'OK' if len(lagr)==15 else 'MISMATCH'}")

# self-isotropy of every vector over F2 (omega(v,v)=0): sanity
print(f"every v self-isotropic= {all(omega(v,v)==0 for v in vecs)}")

# 2) transvections t_v(x)=x + omega(x,v) v generate Sp(4,2); orbit of one Lagrangian
def transvection(v):
    def t(x):
        return x if omega(x, v) == 0 else tuple(a ^ b for a, b in zip(x, v))
    return t
gens = [transvection(v) for v in nonzero]   # 15 generators

def apply_to_subspace(t, S):
    return frozenset(t(x) for x in S)

L0 = next(iter(lagr))
orbit, frontier = {L0}, [L0]
while frontier:
    S = frontier.pop()
    for t in gens:
        S2 = apply_to_subspace(t, S)
        if S2 not in orbit:
            orbit.add(S2); frontier.append(S2)
print(f"orbit of one Lagrangian = {len(orbit)}   -> transitive? {'YES' if orbit==lagr else 'NO'}")

# 3) group order + stabilizer (theory cross-check)
def sp_order(n, q=2):
    return q**(n*n) * reduce(lambda a,i:a*(q**(2*i)-1), range(1,n+1), 1)
order = sp_order(2)
print(f"|Sp(4,2)|             = {order}   (Codex: 720)  -> {'OK' if order==720 else 'MISMATCH'}")
print(f"stabilizer of a Lagr  = {order}//{len(lagr)} = {order//len(lagr)}  (Siegel parabolic; Sp(4,2)~=S6)")
print()
print("NOTE the action is TRANSITIVE => noiseless 'find the Lagrangian' is homogeneous")
print("(no distinguished orbit, no hidden invariant). All hardness/secret lives in the")
print("NOISE layer. The public-selector breaker must run on noisy/LPN-slice instances.")
