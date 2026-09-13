from fractions import Fraction

from collatz_relative_defect import (
    defect_recurrence_step,
    follow_inverse_path,
    local_isometry_holds,
    recharge_center,
    recharge_valuation_identity,
    reference_path,
    relative_step,
    v3,
)


def test_exact_defect_recurrence():
    cases = [
        (1, (2, 2, 1), (1, 0, 0)),
        (5, (1, 2), (2, 1)),
        (7, (2, 1), (0, 2)),
    ]
    for y0, tau, qs in cases:
        ref = reference_path(y0, tau)
        full = follow_inverse_path(y0, tau, qs)
        D = 0
        for j, (t, q) in enumerate(zip(tau, qs)):
            predicted, _, _ = defect_recurrence_step(ref[j], D, t, q)
            actual = (full[j + 1] - ref[j + 1]) // 3
            assert predicted == actual
            D = actual


def test_local_isometry_grid():
    sources = [1, 5, 7, 11, 13, 17, 19, 23, 25]
    for y in sources:
        if y % 3 == 0:
            continue
        for t in (0, 1, 2):
            for q in range(5):
                for qp in range(5):
                    if q != qp:
                        assert local_isometry_holds(y, t, q, qp)


def test_recharge_examples():
    x, xp, _ = relative_step(1, 85, 2, 0)
    assert (x, xp) == (5, 113)
    assert v3(xp - x) == 3

    x, xp, _ = relative_step(1, 85, 1, 0)
    assert (x, xp) == (1, 1813)
    assert v3(xp - x) == 1


def test_recharge_center_simplification():
    c = recharge_center(1, 2, 1)
    assert isinstance(c, Fraction)
    assert recharge_valuation_identity(1, 85, 2, 0)
    assert recharge_valuation_identity(1, 85, 1, 0)
