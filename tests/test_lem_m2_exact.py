from experiments.lib.lem_m2_exact import enumerate_lagrangian_bases, symplectic_form


def test_lagrangian_count():
    bases = enumerate_lagrangian_bases()
    assert len(bases) == 15


def test_symplectic_form_basis():
    assert symplectic_form(1, 4) == 1
    assert symplectic_form(2, 8) == 1
    assert symplectic_form(1, 2) == 0
    assert symplectic_form(4, 8) == 0
