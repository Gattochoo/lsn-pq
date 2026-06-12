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
