from fractions import Fraction
from experiments.lib.lem_m2_exact import (
    apply_matrix,
    bernoulli_product,
    enumerate_lagrangian_bases,
    exact_sd_counts,
    lpn_target_counts,
    num_lagrangian_subspaces,
    reduction_counts_for_B,
    sd_to_product,
    symplectic_form,
)


def test_lagrangian_count():
    bases = enumerate_lagrangian_bases()
    assert len(bases) == 15


def test_symplectic_form_basis():
    assert symplectic_form(1, 4) == 1
    assert symplectic_form(2, 8) == 1
    assert symplectic_form(1, 2) == 0
    assert symplectic_form(4, 8) == 0


def test_sd_to_self_zero():
    dist = {0: Fraction(1, 2), 1: Fraction(1, 2)}
    assert sd_to_product(dist, dist) == Fraction(0)


def test_sd_to_disjoint_one():
    a = {0: Fraction(1)}
    b = {1: Fraction(1)}
    assert sd_to_product(a, b) == Fraction(1)


def test_bernoulli_product_normalized():
    dist = bernoulli_product(Fraction(1, 4), 3)
    assert sum(dist.values()) == Fraction(1)


def test_bernoulli_product_support():
    dist = bernoulli_product(Fraction(1, 4), 3)
    assert len(dist) == 2 ** 3


def test_lpn_target_counts_normalized():
    counts, denom = lpn_target_counts(m=3, p=Fraction(1, 4))
    assert sum(counts) == denom


def test_reduction_counts_zero_B():
    m = 3
    B_cols = [0, 0, 0, 0]
    counts = reduction_counts_for_B(B_cols, enumerate_lagrangian_bases(), m)
    # 15360 = 15 bases * 4 x-values * 256 total error weight
    assert sum(counts) == 15360
    assert counts[0] == 15360
    assert all(c == 0 for c in counts[1:])


def test_full_joint_sd_zero_B():
    m = 3
    p = Fraction(1, 4)
    lpn_counts, lpn_denom = lpn_target_counts(m, p)
    red_counts = reduction_counts_for_B([0, 0, 0, 0], enumerate_lagrangian_bases(), m)
    sd = exact_sd_counts(red_counts, 15360, lpn_counts, lpn_denom)
    assert sd > Fraction(9, 10)


def test_exact_sd_identical():
    counts = [0, 2, 1]
    denom = 3
    sd = exact_sd_counts(counts, denom, counts, denom)
    assert sd == Fraction(0)


def test_num_lagrangian_subspaces():
    assert num_lagrangian_subspaces(1) == 3
    assert num_lagrangian_subspaces(2) == 15
    assert num_lagrangian_subspaces(3) == 135

from experiments.lib.lem_m2_exact import randomized_uniform_B_counts


def test_randomized_uniform_B_counts_normalized():
    for m in (2, 3, 4):
        counts, denom = randomized_uniform_B_counts(m)
        assert sum(counts) == denom


def test_randomized_uniform_B_counts_matches_brute_force():
    """For m=2, sum reduction_counts_for_B over all B equals the randomized counts."""
    from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases, reduction_counts_for_B

    m = 2
    bases = list(enumerate_lagrangian_bases())
    red_counts, _ = randomized_uniform_B_counts(m, bases)

    num_B = 1 << (4 * m)
    mask = (1 << m) - 1
    size = 1 << (3 * m)
    brute = [0] * size
    for bits in range(num_B):
        B_cols = [((bits >> (j * m)) & mask) for j in range(4)]
        counts = reduction_counts_for_B(B_cols, bases, m)
        for i in range(size):
            brute[i] += counts[i]

    assert red_counts == brute


from experiments.lib.lem_m2_exact import matrix_rank_f2, rank_conditioned_counts


def test_matrix_rank_f2():
    # rows of identity-like matrix in F2^4
    rows = [1, 2, 4, 8]
    assert matrix_rank_f2(rows, 4) == 4
    rows = [1, 2, 3, 0]
    assert matrix_rank_f2(rows, 4) == 2
    rows = [0, 0, 0]
    assert matrix_rank_f2(rows, 4) == 0


def test_rank_conditioned_counts_full_rank_m3():
    m = 3
    counts, denom = rank_conditioned_counts(m, rank=m)
    # sum of counts must equal number of full-rank 3x4 matrices * 15360
    num_full_rank = (2 ** 4 - 1) * (2 ** 4 - 2) * (2 ** 4 - 4)
    assert denom == num_full_rank * 15360
    assert sum(counts) == denom


def test_rank_conditioned_counts_matches_brute_force_m2():
    """For m=2, rank=2, compare helper with brute-force rank-conditioned sum."""
    from experiments.lib.lem_m2_exact import (
        enumerate_lagrangian_bases,
        matrix_rank_f2,
        reduction_counts_for_B,
        _rows_to_columns,
    )

    m = 2
    rank = 2
    bases = list(enumerate_lagrangian_bases())
    red_counts, _ = rank_conditioned_counts(m, rank=rank, bases=bases)

    num_B = 1 << (4 * m)
    row_mask = (1 << 4) - 1
    size = 1 << (3 * m)
    brute = [0] * size
    for bits in range(num_B):
        rows = [((bits >> (j * 4)) & row_mask) for j in range(m)]
        if matrix_rank_f2(rows, 4) != rank:
            continue
        B_cols = _rows_to_columns(rows, 4)
        counts = reduction_counts_for_B(B_cols, bases, m)
        for i in range(size):
            brute[i] += counts[i]

    assert red_counts == brute


from experiments.lib.lem_m2_exact import bernoulli_rows_B_counts


def test_bernoulli_rows_B_counts_matches_brute_force():
    """For m=2, p=1/3, compare analytic helper with full B enumeration."""
    from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases, reduction_counts_for_B

    m = 2
    p = Fraction(1, 3)
    bases = list(enumerate_lagrangian_bases())
    red_counts, red_denom = bernoulli_rows_B_counts(m, p, bases)
    assert sum(red_counts) == red_denom

    # Brute-force weighted sum over all B.
    num_B = 1 << (4 * m)
    row_mask = (1 << 4) - 1
    size = 1 << (3 * m)
    brute = [0] * size
    D = p.denominator ** (4 * m)
    for bits in range(num_B):
        rows = [((bits >> (j * 4)) & row_mask) for j in range(m)]
        weight_num = 1
        for r in rows:
            w = r.bit_count()
            weight_num *= (p.numerator ** w) * ((p.denominator - p.numerator) ** (4 - w))
        B_cols = []
        for j in range(4):
            col_val = 0
            for i, r in enumerate(rows):
                if (r >> j) & 1:
                    col_val |= 1 << i
            B_cols.append(col_val)
        counts = reduction_counts_for_B(B_cols, bases, m)
        for i in range(size):
            brute[i] += counts[i] * weight_num

    assert red_counts == brute

from experiments.lib.lem_m2_exact import symplectic_form_n, enumerate_lagrangian_bases_n


def test_symplectic_form_n_matches_existing():
    for u in range(1 << 4):
        for v in range(1 << 4):
            assert symplectic_form_n(u, v, 2) == symplectic_form(u, v)


def test_enumerate_lagrangian_bases_n_counts():
    assert len(enumerate_lagrangian_bases_n(1)) == 3
    assert len(enumerate_lagrangian_bases_n(2)) == 15
    assert len(enumerate_lagrangian_bases_n(3)) == 135
