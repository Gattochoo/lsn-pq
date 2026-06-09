"""
Kimi workstream-B-residual anchor: the orthogonal O(2m,F2) baseline + the
Jordan-Wigner collapse Kimi's candidate MUST evade.

Residual (the one door left to a 2nd band inhabitant): an O(2m,F2)-orthogonal
discrete hard-decoding that resists JW reduction to the symplectic LSN. Known
fermionic stabilizer codes do NOT resist -- JW maps them to qubit Pauli stabilizer
codes (= LSN). We (A) verify a small orthogonal-F2 baseline, and (B) SHOW the JW
collapse concretely so the bar is unambiguous.
"""
import itertools

# ---------- gf2 helpers ----------
def gf2_rank(rows):
    rows = [r[:] for r in rows]; n = len(rows[0]); r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                rows[i] = [a ^ b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r

# ======================================================================
# A. orthogonal group O+(4,2) baseline (hyperbolic Q(v)=v0v1 + v2v3)
# ======================================================================
def Q(v): return (v[0] & v[1]) ^ (v[2] & v[3])
vecs = list(itertools.product((0, 1), repeat=4))
singular = [v for v in vecs if Q(v) == 0]
print("== A. orthogonal baseline O+(4,2), Q(v)=v0v1+v2v3 ==")
print(f"singular vectors (Q=0)      = {len(singular)} / 16")

# count O(Q): invertible 4x4 over F2 preserving Q  (brute over 2^16)
order_O = 0
for bits in range(1 << 16):
    M = [[(bits >> (4 * i + j)) & 1 for j in range(4)] for i in range(4)]
    if gf2_rank(M) != 4:
        continue
    ok = True
    for v in vecs:
        Mv = tuple(sum(M[i][j] & v[j] for j in range(4)) & 1 for i in range(4))
        if Q(Mv) != Q(v):
            ok = False; break
    order_O += ok
print(f"|O+(4,2)|                   = {order_O}   (known: 72)")

# maximal totally singular subspaces (dim 2, Q=0 on all of W)
two_dim = set()
nz = [v for v in vecs if any(v)]
for u, w in itertools.combinations(nz, 2):
    c = tuple(a ^ b for a, b in zip(u, w))
    two_dim.add(frozenset({u, w, c}))
tot_sing = [W for W in two_dim if all(Q(x) == 0 for x in W)]
print(f"maximal totally-singular 2-spaces = {len(tot_sing)}   (the 'Lagrangian' analog)")
print()

# ======================================================================
# B. the Jordan-Wigner collapse the candidate MUST evade
# Majorana gamma_i (i=1..2m) -> Pauli on m qubits, symplectic rep (x|z) in F2^{2m}.
# gamma_{2j-1} = Z_1..Z_{j-1} X_j ;  gamma_{2j} = Z_1..Z_{j-1} Y_j
# ======================================================================
m = 3
def e(k, m):
    v = [0] * m; v[k] = 1; return v
def jw(i):           # i in 1..2m  -> (x,z) each length m
    j = (i + 1) // 2          # qubit index 1..m
    pre = [1 if k < j - 1 else 0 for k in range(m)]   # Z on 1..j-1
    x = e(j - 1, m)
    if i % 2 == 1:            # odd: X_j
        z = pre[:]
    else:                     # even: Y_j  (x and z on qubit j)
        z = [pre[k] ^ (1 if k == j - 1 else 0) for k in range(m)]
    return x, z
def symp(a, b):      # symplectic inner product of (x|z),(x'|z') -> commute=0/anti=1
    (xa, za), (xb, zb) = a, b
    return (sum(xa[k] & zb[k] for k in range(m)) ^ sum(za[k] & xb[k] for k in range(m))) & 1
def pauli_str(a):
    x, z = a; s = ""
    for k in range(m):
        s += {(0,0):"I",(1,0):"X",(0,1):"Z",(1,1):"Y"}[(x[k], z[k])]
    return s

G = {i: jw(i) for i in range(1, 2*m+1)}
print("== B. Jordan-Wigner: gamma_i -> Pauli (m=3 qubits) ==")
for i in range(1, 2*m+1):
    print(f"  gamma_{i} -> {pauli_str(G[i])}")
anti = all(symp(G[i], G[j]) == 1 for i in range(1, 2*m+1) for j in range(i+1, 2*m+1))
print(f"all distinct Majoranas anticommute (symplectic prod=1): {anti}")

def monomial(*idx):  # even product of Majoranas -> Pauli (XOR of symplectic vecs)
    x = [0]*m; z = [0]*m
    for i in idx:
        xi, zi = G[i]
        x = [a ^ b for a, b in zip(x, xi)]; z = [a ^ b for a, b in zip(z, zi)]
    return x, z
print("  even monomials map to Paulis (the orthogonal->symplectic collapse):")
for mon in [(1,2),(3,4),(1,2,3,4),(2,5)]:
    print(f"    gamma_{'gamma_'.join('')}{mon} -> {pauli_str(monomial(*mon))}")
S = [monomial(1,2), monomial(3,4), monomial(5,6)]   # a commuting fermionic stabilizer set
commute = all(symp(S[a], S[b]) == 0 for a in range(len(S)) for b in range(a+1, len(S)))
print(f"  a commuting Majorana-stabilizer set -> commuting Paulis (a qubit code): {commute}")
print()
print("PUNCHLINE for Kimi: JW is an EFFICIENT (poly) isomorphism carrying the")
print("orthogonal Majorana structure onto the symplectic Pauli structure. So any")
print("fermionic STABILIZER decoding factors through it == qubit stabilizer decoding")
print("== LSN. A genuine 2nd inhabitant must be an O(2m,F2) decoding that does NOT")
print("factor through this map. Known fermionic codes all do. THAT is the bar.")
