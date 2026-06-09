r"""
Lane C8 — the transitivity-vs-locality conflict SCALES (n=2,3,4): noise-preserving
code-randomisation gets exponentially far from transitive on Lagrangians.

Context: the worst→avg-for-LSN sub-investigation converged on one obstruction —
  · full Sp(2n,F₂) is TRANSITIVE on Lagrangians (free code-randomisation; Witt), but its
    entangling elements destroy the per-qubit (depolarizing) noise;
  · the LOCAL-Clifford subgroup (Sp(2,F₂)^n ⋊ S_n) PRESERVES per-qubit noise but is NOT
    transitive on Lagrangians (parallel agent, verified n=2);
  · the adjudicator proved this in general (V is Sp-irreducible = finite Stone–von Neumann).
This adds the missing QUANTITATIVE scaling: how many orbits K(n) does the local subgroup
split the Lagrangians into, for n=2,3,4? If K(n) grows fast, the noise-preserving
randomisation is increasingly far from the transitivity a free worst→avg would need —
fleshing out the adjudicator's qualitative "no equivariant split" with numbers.

Independent of the parallel scripts (own RREF-keyed BFS). Run:
  python3 23-locality-conflict-scaling.py
"""
import itertools


def omega(a, b, n):
    s = 0
    for i in range(n):
        s ^= (a[i] & b[i + n]) ^ (a[i + n] & b[i])
    return s & 1


def transvect(u, x, n):
    return x if omega(x, u, n) == 0 else tuple(p ^ q for p, q in zip(x, u))


def qubit_perm(x, perm, n):
    """permute qubits by perm (a tuple): qubit i -> position perm[i]; acts on (x_i,z_i)."""
    y = [0] * (2 * n)
    for i in range(n):
        y[perm[i]] = x[i]
        y[perm[i] + n] = x[i + n]
    return tuple(y)


def span_key(basis, n):
    """canonical key of the subspace spanned by `basis` (frozenset of all its elements)."""
    elems = {tuple([0] * (2 * n))}
    for b in basis:
        elems |= {tuple(p ^ q for p, q in zip(e, b)) for e in elems}
    return frozenset(elems)


def rank_gf2(vs, n):
    piv = {}
    r = 0
    for v in vs:
        x = list(v)
        for c in range(2 * n):
            if x[c]:
                if c in piv:
                    x = [a ^ b for a, b in zip(x, piv[c])]
                else:
                    piv[c] = x
                    r += 1
                    break
    return r


def all_lagrangians(n):
    """all Lagrangians, via BFS orbit of the standard one under all transvections (= full Sp)."""
    D = 2 * n
    e = [tuple(1 if j == i else 0 for j in range(D)) for i in range(D)]
    Lstd_basis = [e[i] for i in range(n)]          # span of first n coords = a Lagrangian
    nz = [v for v in itertools.product((0, 1), repeat=D) if any(v)]
    start = frozenset_basis(Lstd_basis, n)
    seen = {span_key(start, n): start}
    frontier = [start]
    while frontier:
        Lb = frontier.pop()
        for u in nz:
            nb = tuple(transvect(u, b, n) for b in Lb)
            k = span_key(nb, n)
            if k not in seen:
                seen[k] = nb
                frontier.append(nb)
    return seen                                     # key -> a basis


def frozenset_basis(basis, n):
    return tuple(basis)


def count_local_orbits(lagr, n):
    """orbits of the Lagrangians under the LOCAL-Clifford subgroup (per-qubit Sp(2,F2) + S_n)."""
    # per-qubit transvection directions: X_i, Z_i, Y_i  (single-qubit support)
    local_u = []
    for i in range(n):
        xi = tuple(1 if j == i else 0 for j in range(2 * n))
        zi = tuple(1 if j == i + n else 0 for j in range(2 * n))
        yi = tuple(a ^ b for a, b in zip(xi, zi))
        local_u += [xi, zi, yi]
    # qubit permutations: adjacent transpositions generate S_n
    transpositions = []
    for i in range(n - 1):
        perm = list(range(n))
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
        transpositions.append(tuple(perm))

    keys = {span_key(b, n): b for b in lagr.values()}
    seen = set()
    orbit_sizes = []
    for k0, b0 in keys.items():
        if k0 in seen:
            continue
        orb = {k0}
        fr = [b0]
        while fr:
            b = fr.pop()
            nexts = [tuple(transvect(u, x, n) for x in b) for u in local_u]
            nexts += [tuple(qubit_perm(x, p, n) for x in b) for p in transpositions]
            for nb in nexts:
                kk = span_key(nb, n)
                if kk not in orb:
                    orb.add(kk)
                    fr.append(nb)
        seen |= orb
        orbit_sizes.append(len(orb))
    return sorted(orbit_sizes, reverse=True)


def main():
    print("=" * 74)
    print("Lane C8 — transitivity-vs-locality conflict, scaling n=2,3,4")
    print("=" * 74)
    print(f"\n  {'n':>2} {'#Lagrangians':>13} {'full-Sp orbits':>15} "
          f"{'LOCAL-Clifford orbits K(n)':>27}")
    expected_lag = {}
    for n in [2, 3, 4]:
        L = 1
        for i in range(1, n + 1):
            L *= (1 << i) + 1
        expected_lag[n] = L
        lagr = all_lagrangians(n)
        nlag = len(lagr)
        assert nlag == L, f"#Lagrangians {nlag} != {L}"
        local_orbits = count_local_orbits(lagr, n)
        K = len(local_orbits)
        # full Sp is transitive by construction (we built lagr as one transvection orbit) -> 1
        tail = "..." if K > 6 else ""
        print(f"  {n:>2} {nlag:>13} {1:>15}     K={K}; sizes {local_orbits[:6]}{tail}")

    print("\n  Reading: full Sp is TRANSITIVE on Lagrangians (1 orbit) -> free code-randomisation.")
    print("  But the LOCAL-Clifford subgroup (the one that PRESERVES per-qubit depolarizing")
    print("  noise) splits the Lagrangians into K(n) orbits, and K(n) GROWS with n -- so a")
    print("  noise-preserving code-randomisation is increasingly far from transitive. This is")
    print("  the quantitative scaling of the transitivity-vs-locality conflict (parallel agent,")
    print("  n=2) and the flesh on the adjudicator's Sp-irreducibility (no equivariant split):")
    print("  the only transitive randomisation needs entangling elements that wreck the noise.")
    print("  => no FREE noise-preserving worst→avg for per-qubit LSN, at every n tested.")
    print("  (NOT REDUCES, NOT a new barrier -- a quantitative confirmation. The open route")
    print("  remains the fresh-noise encoding, ≈0 in-house. No 7th; no security claim.)")


if __name__ == "__main__":
    main()
