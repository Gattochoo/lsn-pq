#!/usr/bin/env python3
"""
540-CLAUDE-trackZ-nonlinear-converse.py

Adjudication of Kimi Track Z (028525b): n=2 non-linear converse — every
permutation of F_2^4 mapping each Lagrangian to a Lagrangian is linear (in
Sp(4,2)).

Independent verification by my OWN backtracking enumeration (not Kimi's 530):
assign f on the 15 non-zero points one at a time (f(0)=0 forced since 0 is the
unique common point of all Lagrangians), pruning whenever a fully-assigned
Lagrangian's image is not a Lagrangian. Count the solutions and check EVERY one
is F_2-linear and symplectic.

Key structural fact (the engine): a Lagrangian L = {0,a,b,a+b} is a 2-dim
subspace, so its image {0,f(a),f(b),f(a+b)} is a Lagrangian only if it is
closed under addition, forcing f(a+b) = f(a)+f(b) on every isotropic pair
(omega(a,b)=0). Non-linearity could only hide on symplectic pairs
(omega(a,b)=1); the enumeration shows it cannot.

Checks:
  (1) backtracking count of Lagrangian-preserving permutations == 720.
  (2) every solution is linear: f(x+y)=f(x)+f(y) for all x,y.
  (3) every solution is symplectic: omega(f(x),f(y))=omega(x,y) on a basis.
  (4) the 720 == Sp(4,2) (matvec set equals exp/441's symplectic set).

Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
"""

from itertools import combinations

N = 4
SIZE = 1 << N
NZ = list(range(1, SIZE))


def omega(a, b):
    s = 0
    for i in range(2):
        s ^= (((a >> i) & 1) & ((b >> (i + 2)) & 1)) ^ \
             (((a >> (i + 2)) & 1) & ((b >> i) & 1))
    return s


def all_lagrangians():
    found = set()
    for basis in combinations(range(1, SIZE), 2):
        span = {0}
        ok = True
        for b in basis:
            if b in span:
                ok = False
                break
            span |= {x ^ b for x in span}
        if not ok or len(span) != 4:
            continue
        if any(omega(u, v) for u in span for v in span):
            continue
        found.add(frozenset(span))
    return [set(s) for s in found]


LAGS = all_lagrangians()
LAGSET = set(frozenset(L) for L in LAGS)


def backtrack():
    """Enumerate permutations f (f(0)=0) preserving the Lagrangian family."""
    f = {0: 0}
    used = {0}
    sols = []

    # order non-zero points; for pruning, after assigning a point check every
    # Lagrangian fully assigned among the non-zero points.
    order = NZ
    # precompute, for each non-zero point, the Lagrangians it completes
    # (i.e. whose 3 non-zero points are all <= this point in `order` index)
    idx = {v: i for i, v in enumerate(order)}
    completes = {v: [] for v in order}
    for L in LAGS:
        nz = sorted((p for p in L if p != 0), key=lambda p: idx[p])
        completes[nz[-1]].append([p for p in L if p != 0])

    def rec(i):
        if i == len(order):
            sols.append(dict(f))
            return
        v = order[i]
        for w in NZ:
            if w in used:
                continue
            f[v] = w
            ok = True
            for tri in completes[v]:
                img = frozenset({0} | {f[p] for p in tri})
                if len(img) != 4 or img not in LAGSET:
                    ok = False
                    break
            if ok:
                used.add(w)
                rec(i + 1)
                used.discard(w)
            del f[v]

    rec(0)
    return sols


def is_linear(f):
    for x in range(SIZE):
        for y in range(SIZE):
            if f[x ^ y] != f[x] ^ f[y]:
                return False
    return True


def is_symplectic_map(f):
    for i in range(N):
        for j in range(N):
            if omega(f[1 << i], f[1 << j]) != omega(1 << i, 1 << j):
                return False
    return True


def main():
    ok = True
    print("=" * 72)
    print("540-CLAUDE  Track Z — non-linear converse: independent backtracking")
    print("=" * 72)
    print(f"\n  |Lagr(4,2)| = {len(LAGS)} (expect 15)")
    ok &= len(LAGS) == 15

    sols = backtrack()
    print(f"\n(1) Lagrangian-preserving permutations (f(0)=0): {len(sols)} "
          f"(expect 720) {'OK' if len(sols) == 720 else 'FAIL'}")
    ok &= len(sols) == 720

    nonlinear = [f for f in sols if not is_linear(f)]
    print(f"(2) every solution linear: {'OK' if not nonlinear else f'FAIL ({len(nonlinear)} non-linear)'}")
    ok &= not nonlinear

    nonsymp = [f for f in sols if is_linear(f) and not is_symplectic_map(f)]
    print(f"(3) every solution symplectic: {'OK' if not nonsymp else 'FAIL'}")
    ok &= not nonsymp

    # (4) the 720 maps == Sp(4,2) as a set of linear maps (by columns)
    sol_mats = set(tuple(f[1 << j] for j in range(N)) for f in sols)
    # symplectic linear maps by columns
    def all_gl_symplectic():
        from itertools import product
        S = set()
        for cols in product(range(SIZE), repeat=N):
            # invertible?
            img = set()
            for x in range(SIZE):
                y = 0
                for j in range(N):
                    if (x >> j) & 1:
                        y ^= cols[j]
                img.add(y)
            if len(img) != SIZE:
                continue
            if all(omega(cols[i] if False else _mv(cols, 1 << i),
                         _mv(cols, 1 << j)) == omega(1 << i, 1 << j)
                   for i in range(N) for j in range(N)):
                S.add(cols)
        return S

    def _mv(cols, x):
        y = 0
        for j in range(N):
            if (x >> j) & 1:
                y ^= cols[j]
        return y

    sp = all_gl_symplectic()
    same = sol_mats == sp
    ok &= same and len(sp) == 720
    print(f"(4) the 720 solutions == Sp(4,2) ({len(sp)} matrices): "
          f"{'OK' if same else 'FAIL'}")

    print("\n" + "=" * 72)
    print("RESULT:", "ALL CHECKS PASS — Track Z n=2 non-linear converse ACCEPT"
          if ok else "FAILURE")
    print("  (general-n via cited polar-space automorphism theorem; not reproven.)")
    print("Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
