from fractions import Fraction

from experiments.lib.lem_m2_exact import (
    bernoulli_product,
    enumerate_lagrangian_bases,
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
