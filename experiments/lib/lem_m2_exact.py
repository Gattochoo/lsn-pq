"""Exact small-n helpers for lem:m2 noise-side enumeration."""
from fractions import Fraction


def symplectic_form(u: int, v: int) -> int:
    """Standard symplectic form on F_2^4: omega(u,v)."""
    return (
        ((u >> 0) & 1) * ((v >> 2) & 1)
        ^ ((u >> 1) & 1) * ((v >> 3) & 1)
        ^ ((u >> 2) & 1) * ((v >> 0) & 1)
        ^ ((u >> 3) & 1) * ((v >> 1) & 1)
    ) & 1


def enumerate_lagrangian_bases() -> list[tuple[int, int]]:
    """Return list of Lagrangian subspaces of F_2^4 as (col0,col1) basis pairs."""
    subspaces = {}
    for v1 in range(1, 1 << 4):
        for v2 in range(v1 + 1, 1 << 4):
            if symplectic_form(v1, v2) != 0:
                continue
            span = frozenset({0, v1, v2, v1 ^ v2})
            canon = tuple(sorted([v1, v2]))
            subspaces.setdefault(span, canon)
    return [c for _, c in sorted(subspaces.items())]


def apply_matrix(B_cols: list[int], x: int) -> int:
    """B * x over F_2; B_cols is list of m-bit column ints, x is 4-bit int."""
    y = 0
    for j, col in enumerate(B_cols):
        if (x >> j) & 1:
            y ^= col
    return y


def bernoulli_product(p: Fraction, m: int) -> dict[int, Fraction]:
    """Return dict {e_prime: probability} for Bernoulli(p)^m."""
    q = Fraction(1) - p
    dist = {}
    for v in range(1 << m):
        w = v.bit_count()
        dist[v] = (p ** w) * (q ** (m - w))
    return dist


def sd_to_product(dist: dict[int, Fraction], product_dist: dict[int, Fraction]) -> Fraction:
    """Exact SD between dict dist (sums to 1) and product_dist."""
    keys = set(dist.keys()) | set(product_dist.keys())
    total = Fraction(0)
    for k in keys:
        total += abs(Fraction(dist.get(k, 0)) - Fraction(product_dist.get(k, 0)))
    return total / 2


def lpn_target_counts(m: int, p: Fraction) -> tuple[list[int], int]:
    """Integer counts and denominator for LPN_p distribution over (C, y)."""
    mask = (1 << m) - 1
    num_C = 1 << (2 * m)
    num_y = 1 << m
    size = num_C * num_y
    counts = [0] * size
    D = p.denominator ** m
    total_denom = num_C * 4 * D
    for C_key in range(num_C):
        c0 = (C_key >> m) & mask
        c1 = C_key & mask
        for x in range(1 << 2):
            cx = 0
            if x & 1:
                cx ^= c0
            if x & 2:
                cx ^= c1
            for eprime in range(num_y):
                w = eprime.bit_count()
                num = (p.numerator ** w) * ((p.denominator - p.numerator) ** (m - w))
                y = cx ^ eprime
                key = (C_key << m) | y
                counts[key] += num
    return counts, total_denom


def reduction_counts_for_B(B_cols: list[int], bases: list[tuple[int, int]], m: int) -> list[int]:
    """Integer counts for reduction output (C, y) for a fixed B."""
    mask = (1 << m) - 1
    size = 1 << (3 * m)
    counts = [0] * size
    for a0, a1 in bases:
        c0 = apply_matrix(B_cols, a0) & mask
        c1 = apply_matrix(B_cols, a1) & mask
        C_key = (c0 << m) | c1
        for x in range(1 << 2):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):  # ambient dimension 2n for n=2
                w = e.bit_count()
                v = a ^ e
                y = apply_matrix(B_cols, v) & mask
                key = (C_key << m) | y
                # 3**(4-w) comes from Bernoulli(1/4) noise weights after clearing denominators.
                counts[key] += 3 ** (4 - w)
    return counts


def exact_sd_counts(counts1: list[int], denom1: int, counts2: list[int], denom2: int) -> Fraction:
    """Exact SD between two integer-count distributions with different denominators."""
    num = 0
    for c1, c2 in zip(counts1, counts2):
        num += abs(c1 * denom2 - c2 * denom1)
    return Fraction(num, 2 * denom1 * denom2)


def num_lagrangian_subspaces(n: int) -> int:
    """Number of Lagrangian subspaces of F_2^{2n}."""
    if n < 1:
        raise ValueError("n must be >= 1")
    total = 1
    for i in range(1, n + 1):
        total *= (2 ** i + 1)
    return total


def randomized_uniform_B_counts(m: int, bases=None) -> tuple[list[int], int]:
    r"""Integer counts for (C, y) when B ~ Unif(F_2^{m x 4}) is drawn per A.

    Uses the three-case decomposition from the design spec:
      * v = 0            -> 2^{2m} matrices per (C, 0)
      * v in span(A)\{0} -> 2^{2m} matrices per graph point
      * v not in span(A) -> 2^{m} matrices per full-space point

    Returns (counts, denominator) so that counts[key] / denominator is the
    exact probability of output key = (C_key << m) | y.
    """
    if bases is None:
        bases = enumerate_lagrangian_bases()

    mask = (1 << m) - 1
    num_C = 1 << (2 * m)
    size = 1 << (3 * m)
    counts = [0] * size

    # Precompute c0/c1 for every C_key to avoid repeated bit slicing.
    c0_list = [(C_key >> m) & mask for C_key in range(num_C)]
    c1_list = [C_key & mask for C_key in range(num_C)]

    two_to_m = 1 << m
    two_to_2m = 1 << (2 * m)
    case3_weight_sum = 0

    for a0, a1 in bases:
        span_map = {
            0: (0, 0),
            a0: (1, 0),
            a1: (0, 1),
            a0 ^ a1: (1, 1),
        }
        for x in range(1 << 2):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):
                w = e.bit_count()
                weight = 3 ** (4 - w)
                v = a ^ e

                if v == 0:
                    # y is forced to 0; C is uniform.
                    add = weight * two_to_2m
                    for C_key in range(num_C):
                        counts[(C_key << m)] += add
                elif v in span_map:
                    alpha, beta = span_map[v]
                    add = weight * two_to_2m
                    for C_key in range(num_C):
                        y = 0
                        if alpha:
                            y ^= c0_list[C_key]
                        if beta:
                            y ^= c1_list[C_key]
                        counts[(C_key << m) | y] += add
                else:
                    # Full-space uniform contribution; delay the actual add.
                    case3_weight_sum += weight

    case3_add = case3_weight_sum * two_to_m
    for key in range(size):
        counts[key] += case3_add

    # Denominator = sum over (A, x, e) of weight_e * 2^{4m}.
    red_denom = len(bases) * (1 << 2) * 256 * (1 << (4 * m))
    return counts, red_denom


def matrix_rank_f2(rows: list[int], n_cols: int) -> int:
    """Rank of a matrix over F_2 given as a list of row bitmasks."""
    pivots = {}
    for r in rows:
        x = r & ((1 << n_cols) - 1)
        if x == 0:
            continue
        for p in sorted(pivots.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= pivots[p]
        if x:
            pivots[x.bit_length() - 1] = x
    return len(pivots)


def _rows_to_columns(rows: list[int], n_cols: int) -> list[int]:
    """Convert row representation to column representation for apply_matrix."""
    m = len(rows)
    cols = [0] * n_cols
    for j in range(n_cols):
        col_val = 0
        for i, r in enumerate(rows):
            if (r >> j) & 1:
                col_val |= 1 << i
        cols[j] = col_val
    return cols


def rank_conditioned_counts(m: int, rank: int, bases=None) -> tuple[list[int], int]:
    """Exact counts for (C, y) when B is uniform over m x 4 matrices of given rank."""
    if bases is None:
        bases = enumerate_lagrangian_bases()
    if rank > min(m, 4):
        raise ValueError("rank cannot exceed min(m, 4)")

    size = 1 << (3 * m)
    counts = [0] * size
    num_B = 1 << (4 * m)
    row_mask = (1 << 4) - 1
    matched = 0

    # Precompute all (A, x, e) triples once, hoisting the loop outside B enumeration.
    triples = []
    for a0, a1 in bases:
        for x in range(1 << 2):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):
                weight = 3 ** (4 - e.bit_count())
                v = a ^ e
                triples.append((a0, a1, v, weight))

    mask = (1 << m) - 1
    for bits in range(num_B):
        rows = [((bits >> (j * 4)) & row_mask) for j in range(m)]
        if matrix_rank_f2(rows, 4) != rank:
            continue
        matched += 1
        B_cols = _rows_to_columns(rows, 4)
        # Precompute B*x for all 4-bit vectors x once per B.
        Bx = [apply_matrix(B_cols, x) & mask for x in range(1 << 4)]
        for a0, a1, v, weight in triples:
            c0 = Bx[a0]
            c1 = Bx[a1]
            y = Bx[v]
            key = ((c0 << m) | c1) << m | y
            counts[key] += weight

    denom = matched * 15360
    return counts, denom


def bernoulli_rows_B_counts(m: int, p: Fraction, bases=None) -> tuple[list[int], int]:
    """Exact counts for (C, y) when each row of B is i.i.d. Bernoulli(p)^4.

    For each (A, x, e) triple we enumerate all assignments of m rows to the
    eight possible output-bit patterns (s0, s1, s2) = (r·a0, r·a1, r·v).  The
    per-row weight numerator is accumulated analytically, so we never iterate
    over the full 2^{4m} matrix space.
    """
    if bases is None:
        bases = enumerate_lagrangian_bases()
    if not (0 <= p <= 1):
        raise ValueError("p must be in [0, 1]")

    size = 1 << (3 * m)
    counts = [0] * size
    num_row_patterns = 1 << 4

    # Numerator of row-pattern weight, denominator is p.denominator^4.
    pattern_weights = [0] * num_row_patterns
    for r in range(num_row_patterns):
        w = r.bit_count()
        pattern_weights[r] = (
            p.numerator ** w
        ) * ((p.denominator - p.numerator) ** (4 - w))

    # Bits of the 8 output patterns: t = (s0<<2) | (s1<<1) | s2.
    t_bits = [((t >> 2) & 1, (t >> 1) & 1, t & 1) for t in range(8)]
    num_assignments = 8 ** m

    for a0, a1 in bases:
        span_map = {0: (0, 0), a0: (1, 0), a1: (0, 1), a0 ^ a1: (1, 1)}
        for x in range(1 << 2):
            a = 0
            if x & 1:
                a ^= a0
            if x & 2:
                a ^= a1
            for e in range(1 << 4):
                w_e = 3 ** (4 - e.bit_count())
                v = a ^ e

                # W[t] = total row-pattern weight producing output pattern t.
                W = [0] * 8
                if v == 0:
                    for r in range(num_row_patterns):
                        s0 = (r & a0).bit_count() & 1
                        s1 = (r & a1).bit_count() & 1
                        t = (s0 << 2) | (s1 << 1)
                        W[t] += pattern_weights[r]
                elif v in span_map:
                    alpha, beta = span_map[v]
                    for r in range(num_row_patterns):
                        s0 = (r & a0).bit_count() & 1
                        s1 = (r & a1).bit_count() & 1
                        s2 = ((alpha * s0) ^ (beta * s1)) & 1
                        t = (s0 << 2) | (s1 << 1) | s2
                        W[t] += pattern_weights[r]
                else:
                    for r in range(num_row_patterns):
                        s0 = (r & a0).bit_count() & 1
                        s1 = (r & a1).bit_count() & 1
                        s2 = (r & v).bit_count() & 1
                        t = (s0 << 2) | (s1 << 1) | s2
                        W[t] += pattern_weights[r]

                # Enumerate all row-to-output-pattern assignments.
                for assignment in range(num_assignments):
                    tmp = assignment
                    c0 = 0
                    c1 = 0
                    y = 0
                    prod = 1
                    for i in range(m):
                        t = tmp & 7
                        tmp >>= 3
                        prod *= W[t]
                        s0, s1, s2 = t_bits[t]
                        if s0:
                            c0 |= 1 << i
                        if s1:
                            c1 |= 1 << i
                        if s2:
                            y |= 1 << i
                    key = ((c0 << m) | c1) << m | y
                    counts[key] += w_e * prod

    red_denom = 15360 * (p.denominator ** (4 * m))
    return counts, red_denom


def symplectic_form_n(u: int, v: int, n: int) -> int:
    """Standard symplectic form on F_2^{2n}: omega(u, v)."""
    res = 0
    for i in range(n):
        ui = (u >> i) & 1
        vi = (v >> i) & 1
        ui2 = (u >> (i + n)) & 1
        vi2 = (v >> (i + n)) & 1
        res ^= (ui * vi2) ^ (ui2 * vi)
    return res & 1


def enumerate_lagrangian_bases_n(n: int) -> list[tuple[int, ...]]:
    """Return one ordered basis per Lagrangian subspace of F_2^{2n}.

    For n=2 this returns the same 15 subspaces as enumerate_lagrangian_bases.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    dim = 2 * n
    vectors = list(range(1, 1 << dim))
    subspaces = {}

    def is_isotropic(basis):
        for i in range(len(basis)):
            for j in range(i + 1, len(basis)):
                if symplectic_form_n(basis[i], basis[j], n) != 0:
                    return False
        return True

    def span_of(basis):
        span = [0]
        for v in basis:
            span += [s ^ v for s in span]
        return set(span)

    def extend(basis, start):
        if len(basis) == n:
            if not is_isotropic(basis):
                return
            span = [0]
            for v in basis:
                span += [s ^ v for s in span]
            span_set = frozenset(span)
            canon = tuple(sorted(basis))
            subspaces.setdefault(span_set, canon)
            return
        for idx in range(start, len(vectors)):
            v = vectors[idx]
            ok = True
            for b in basis:
                if symplectic_form_n(b, v, n) != 0:
                    ok = False
                    break
            if not ok:
                continue
            for s in span_of(basis):
                if s == v:
                    ok = False
                    break
            if not ok:
                continue
            extend(basis + [v], idx + 1)

    extend([], 0)
    return [c for _, c in sorted(subspaces.items())]


def lpn_target_counts_n(m: int, n: int, p: Fraction) -> tuple[list[int], int]:
    """Integer counts and denominator for LPN_p distribution over (C, y) with C in F_2^{m x n}."""
    mask = (1 << m) - 1
    num_C = 1 << (n * m)
    size = 1 << ((n + 1) * m)
    counts = [0] * size
    D = p.denominator ** m
    total_denom = num_C * (1 << n) * D

    # Precompute c_j for each C_key and basis index j.
    c_lists = [[0] * num_C for _ in range(n)]
    for C_key in range(num_C):
        tmp = C_key
        for j in range(n):
            c_lists[j][C_key] = tmp & mask
            tmp >>= m

    for C_key in range(num_C):
        for x in range(1 << n):
            cx = 0
            for j in range(n):
                if (x >> j) & 1:
                    cx ^= c_lists[j][C_key]
            for eprime in range(1 << m):
                w = eprime.bit_count()
                num = (p.numerator ** w) * ((p.denominator - p.numerator) ** (m - w))
                y = cx ^ eprime
                key = (C_key << m) | y
                counts[key] += num
    return counts, total_denom
