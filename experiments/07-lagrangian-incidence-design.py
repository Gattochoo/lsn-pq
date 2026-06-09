"""
Workstream A, step 3 — the Lagrangian incidence design: how blind are low-degree
public breakers, hence how non-linear must Codex's OFA-307 breaker be to "close"?

Pure combinatorics on the VERIFIED 135 Lagrangians of Sp(6,2) (no sample-model
assumptions -> no drift risk). We ask: can a public selector single out the secret
Lagrangian L from low-degree tests on its points?
  - degree-1 (single Pauli x): how many Lagrangians contain x?  constant => blind.
  - degree-2 (pair x,y):       how many contain both?           constant-per-class
                                                                => blind to that degree.
If incidences are constant within each public (Omega-)class, a breaker of that
degree carries ZERO secret signal -- it must go higher-degree or use the noise.
"""
import itertools
from functools import reduce
from collections import Counter

n = 3; dim = 2 * n
def omega(u, v):
    return reduce(lambda a, i: a ^ (u[i]&v[i+n]) ^ (u[i+n]&v[i]), range(n), 0) & 1

# rebuild the 135 Lagrangians as the Sp orbit of the x-space (verified baseline)
vecs = [t for t in itertools.product((0,1), repeat=dim)]
nonzero = [v for v in vecs if any(v)]
L0 = frozenset(v for v in nonzero if v[3]==0 and v[4]==0 and v[5]==0)   # span(e0,e1,e2)
def transvect(v, x): return x if omega(x, v)==0 else tuple(a^b for a,b in zip(x,v))
orbit, frontier = {L0}, [L0]
while frontier:
    S = frontier.pop()
    for v in nonzero:
        S2 = frozenset(transvect(v, x) for x in S)
        if S2 not in orbit: orbit.add(S2); frontier.append(S2)
lagr = list(orbit)
print(f"#Lagrangians = {len(lagr)} (expect 135)\n")

# ---- degree-1: single-vector incidence ----
inc1 = Counter()
for x in nonzero:
    inc1[x] = sum(1 for L in lagr if x in L)
vals1 = set(inc1.values())
print("== degree-1 (single Pauli x) ==")
print(f"  #Lagrangians containing a fixed nonzero x : values = {sorted(vals1)}")
print(f"  -> CONSTANT over all 63 nonzero x: {len(vals1)==1}  (= {next(iter(vals1))})")
print(f"  => a degree-1 public selector is PERFECTLY BLIND to the secret L.\n")

# ---- degree-2: pair incidence, split by public Omega-class ----
iso_counts, noniso_counts = Counter(), Counter()
for x, y in itertools.combinations(nonzero, 2):
    if x == tuple(a^b for a,b in zip(x,y)):  # skip dependent (x=y impossible here)
        continue
    both = sum(1 for L in lagr if x in L and y in L)
    if omega(x, y) == 0:
        iso_counts[both] += 1
    else:
        noniso_counts[both] += 1
print("== degree-2 (pair x,y), split by PUBLIC Omega(x,y) ==")
print(f"  Omega=1 (non-isotropic) pairs: #Lagrangians-containing-both distribution = {dict(noniso_counts)}")
print(f"     -> always 0 (a Lagrangian is isotropic) -- but Omega is PUBLIC, no secret leak.")
print(f"  Omega=0 (isotropic) pairs:     distribution = {dict(iso_counts)}")
iso_vals = set(iso_counts.keys()) - {0}
print(f"     -> among isotropic INDEPENDENT pairs, nonzero incidence values = {sorted(iso_vals)}")
print()
print("INTERPRETATION for OFA-307:")
print(" - degree-1 selector: blind (every Pauli in exactly 15 of 135 Lagrangians).")
print(" - degree-2 selector: only reads the PUBLIC Omega-class (iso vs non-iso); within")
print("   the isotropic class the incidence is highly regular -> almost no secret signal.")
print(" => a public breaker that 'closes' with LOW-degree linear tests is reading public")
print("    structure, not the secret. A real REDUCES must be genuinely non-linear OR")
print("    exploit the NOISE coupling (C2). A low-degree 'close' at n=3 = artifact (A1).")
