"""
80 — SDA bug verification: pencil counterexample + spread construction.
(Fable-5 independent re-verification; companion to
 meta/2026-06-09-CLAUDE-fable5-SDA-judgment-and-fix-plan.md)

Three parts:
 [1] n=3 BRUTE-FORCE ground truth: the dim-2 isotropic pencil is a subset of size
     >= |Lagr|/2^{2n} whose average E[2^{dim(L∩L')}] exceeds gamma-bar = 2*E_global
     -> SDA(2*rho_avg) < 2^{2n}; the paper's Theorem 5.4 proof route is falsified.
 [2] EXACT structural identities for all n (q-binomial; no enumeration):
     E_pencil(k) = 2^k * E_{Lagr(n-k)}[2^j],  |pencil| = |Lagr(n-k)|,
     |Lagr(n)|/|Lagr(n-2)| = (2^{n-1}+1)(2^n+1) <= 2^{2n}.
     Shows every fixed C <= 4 is killed (k=2 pencil ratio -> 4 from below) while
     k=3 pencils are below the SDA size threshold for n >= 4 (so C = 5 survives pencils).
 [3] Desarguesian symplectic spread at n=3 (concrete): 2^n+1 pairwise-transversal
     Lagrangians L_lambda = {(x, lambda*x)} over F_8 — the family behind the
     UNCONDITIONAL Omega(2^n) @ VSTAT(O(2^n)) theorem (worst-case promise).

No 7th; no break; no security claim. OPEN = LSN.
"""
import itertools

# ---------------------------------------------------------------- [1] n=3 brute
n = 3
D = 2 * n

def omega(a, b):
    s = 0
    for i in range(n):
        s ^= (a[i] & b[i + n]) ^ (a[i + n] & b[i])
    return s & 1

def span(basis):
    S = {tuple([0] * D)}
    for v in basis:
        S |= {tuple(x ^ y for x, y in zip(s, v)) for s in S}
    return frozenset(S)

def part1():
    vecs = list(itertools.product((0, 1), repeat=D))
    nz = [v for v in vecs if any(v)]
    seen, Ls = set(), []
    for c in itertools.combinations(nz, n):
        sp = span(c)
        if len(sp) != 2 ** n or sp in seen:
            continue
        if all(omega(a, b) == 0 for a in c for b in c):
            seen.add(sp)
            Ls.append(sp)
    assert len(Ls) == 135, len(Ls)

    def dimint(L1, L2):
        return (len(L1 & L2)).bit_length() - 1

    tot = cnt = 0
    for i in range(len(Ls)):
        for j in range(len(Ls)):
            if i != j:
                tot += 2 ** dimint(Ls[i], Ls[j]); cnt += 1
    Eglob = tot / cnt

    e1 = tuple(1 if i == 0 else 0 for i in range(D))
    e2 = tuple(1 if i == 1 else 0 for i in range(D))
    W = span([e1, e2])                      # dim-2 isotropic (omega(e1,e2)=0)
    pen = [L for L in Ls if W <= L]
    tp = cp = 0
    for i in range(len(pen)):
        for j in range(len(pen)):
            if i != j:
                tp += 2 ** dimint(pen[i], pen[j]); cp += 1
    Epen = tp / cp
    thr = len(Ls) / 2 ** (2 * n)
    print(f"[1] n=3 brute: |Lagr|=135  E_glob={Eglob:.4f}  gamma-bar=2E={2*Eglob:.4f}")
    print(f"    pencil(dim-2): size={len(pen)} >= threshold {thr:.2f}; E_pencil={Epen:.4f}")
    viol = len(pen) >= thr and Epen > 2 * Eglob
    print(f"    VIOLATION (size>=|Lagr|/2^(2n) and E>gamma-bar): {viol}")
    assert viol and abs(Epen - 4.0) < 1e-9      # = 4*E_quot(n=1)=4 exactly

# ------------------------------------------------------- [2] exact structural
def qbin(m, k):
    num = den = 1
    for i in range(k):
        num *= (2 ** (m - i) - 1); den *= (2 ** (i + 1) - 1)
    return num // den

def E2(m):
    """E[2^{dim(L∩L')}] over DISTINCT Lagrangian pairs in Lagr(2m), exact."""
    if m <= 1:
        return 1.0                            # Lagr(2): 3 lines, pairwise j=0
    cs = [qbin(m, j) * 2 ** (((m - j) * (m - j + 1)) // 2) for j in range(m + 1)]
    S = sum(cs); num = sum(cs[j] * 2 ** j for j in range(m + 1))
    return (num - 2 ** m) / (S - 1)

def part2():
    print("\n[2] structural (exact): E_pencil(k=2)=4*E(n-2) vs gamma-bar=2*E(n); pencil size factor")
    print(f"    {'n':>3} {'E(n)':>7} {'2E':>7} {'4E(n-2)':>8} {'viol?':>6} "
          f"{'2^(2n)/((2^(n-1)+1)(2^n+1))':>28}")
    for m in [4, 5, 8, 12, 41, 65]:
        ratio = 2 ** (2 * m) / ((2 ** (m - 1) + 1) * (2 ** m + 1))
        viol = 4 * E2(m - 2) > 2 * E2(m)
        print(f"    {m:>3} {E2(m):>7.4f} {2*E2(m):>7.4f} {4*E2(m-2):>8.4f} "
              f"{str(viol):>6} {ratio:>28.4f}")
        assert viol and ratio >= 1.0
    print("    k=2 ratio -> 4 from below: kills every C<=4. k=3 pencil: ratio->8 but size")
    print("    |Lagr|/2^(3n-3) < |Lagr|/2^(2n) for n>=4 -> irrelevant at the 2^(2n) scale.")
    print("    => conditional threshold gamma-bar = 5*rho_avg survives all pencils.")

# ----------------------------------------------- [3] spread (F_8 Desarguesian)
def part3():
    POLY = 0b1011                              # t^3 + t + 1

    def mul(a, b):
        r = 0
        for i in range(3):
            if (b >> i) & 1:
                r ^= a << i
        for d in (5, 4, 3):
            if (r >> d) & 1:
                r ^= POLY << (d - 3)
        return r & 7

    def sq(a):
        return mul(a, a)

    def trace(z):                              # Tr(z) = z + z^2 + z^4 in F_2
        s = z ^ sq(z) ^ sq(sq(z))
        assert s in (0, 1), s
        return s

    Lams = [frozenset((x, mul(l, x)) for x in range(8)) for l in range(8)]
    Lams.append(frozenset((0, y) for y in range(8)))   # L_inf

    def w2(u, v):                               # omega((a,b),(c,d)) = Tr(ad)+Tr(bc)
        return trace(mul(u[0], v[1])) ^ trace(mul(u[1], v[0]))

    iso = all(all(w2(a, b) == 0 for a in L for b in L) for L in Lams)
    trans = all(len(Lams[i] & Lams[j]) == 1 for i in range(9) for j in range(9) if i != j)
    dims = all(len(L) == 8 for L in Lams)
    print("\n[3] Desarguesian symplectic spread, n=3 (F_8 = F_2[t]/(t^3+t+1)):")
    print(f"    9 = 2^n+1 subspaces; dim n each: {dims}; all isotropic: {iso}; "
          f"pairwise transversal: {trans}")
    assert dims and iso and trans
    print("    => exists for all n (char-2 graphs are automatically isotropic).")
    print("    pairwise corr = kappa*2^(-2n) (minimum), beta = kappa*2^(-n)")
    print("    -> unconditional Omega(2^n) queries @ VSTAT(O(2^n))  [worst-case promise;")
    print("       NOT average-case over uniform L — that is the conditional theorem's job].")

if __name__ == "__main__":
    part1()
    part2()
    part3()
    print("\nAll checks passed. SDA(2*rho_avg) >= 2^{2n} is FALSE (pencil); fix = Option A+D.")
