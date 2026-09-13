from __future__ import annotations

from hypothesis import assume, given, settings, strategies as st

from collatz_relative_defect import (
    accelerated_collatz,
    base_exponent,
    defect_recurrence_step,
    inverse_child,
    layered_transition,
    local_isometry_holds,
    relative_state,
    v3,
)


@st.composite
def interior_sources(draw, max_k: int = 20_000):
    k = draw(st.integers(min_value=0, max_value=max_k))
    r = draw(st.sampled_from((1, 5)))
    return 6 * k + r


@settings(max_examples=400, deadline=None)
@given(y=interior_sources(), t=st.integers(0, 2), q=st.integers(0, 8))
def test_inverse_family_property(y, t, q):
    x = inverse_child(y, t, q)
    assert accelerated_collatz(x) == y
    assert x % 3 == t


@settings(max_examples=400, deadline=None)
@given(
    y=interior_sources(),
    t=st.integers(0, 2),
    q=st.integers(0, 12),
    qp=st.integers(0, 12),
)
def test_local_isometry_property(y, t, q, qp):
    assume(q != qp)
    assert local_isometry_holds(y, t, q, qp)


@settings(max_examples=400, deadline=None)
@given(
    ybar=interior_sources(max_k=2_000),
    D=st.integers(-500, 500).map(lambda x: 2 * x),
    t=st.integers(0, 2),
    q=st.integers(0, 5),
)
def test_exact_defect_recurrence_against_direct_integer_map(ybar, D, t, q):
    y = ybar + 3 * D
    assume(y > 0)
    ref_child = inverse_child(ybar, t, 0)
    full_child = inverse_child(y, t, q)
    direct = (full_child - ref_child) // 3
    predicted, _, _ = defect_recurrence_step(ybar, D, t, q)
    assert direct == predicted


@settings(max_examples=400, deadline=None)
@given(
    y=interior_sources(max_k=2_000),
    D=st.integers(-500, 500).map(lambda x: 2 * x),
    t=st.integers(0, 2),
    q=st.integers(0, 5),
)
def test_recharge_valuation_against_direct_integer_map(y, D, t, q):
    from fractions import Fraction

    assume(D != 0 and D % 3 != 0)
    yp = y + 3 * D
    assume(yp > 0 and yp % 3 != 0)

    b = base_exponent(y, t)
    a = D % 3
    bp = base_exponent(y + 3 * a, t)
    center = (Fraction(2) ** (b - bp) - 1) * Fraction(y, 3)
    x = inverse_child(y, t, q)
    xp = inverse_child(yp, t, q)

    def v3_fraction(z: Fraction) -> int:
        return v3(z.numerator) - v3(z.denominator)

    assert v3(xp - x) == v3_fraction(Fraction(D) - center)


@settings(max_examples=300, deadline=None)
@given(
    y=interior_sources(max_k=500),
    D=st.integers(0, 500).map(lambda x: 2 * x),
    r=st.integers(2, 5),
    t=st.integers(0, 2),
    q=st.integers(0, 100),
)
def test_layered_transition_is_representative_independent(y, D, r, t, q):
    yp = y + 3 * D
    state = relative_state(y, yp, r)

    y2 = y + 2 * (3 ** (r + 1))
    D2 = D + 2 * (3 ** r)
    yp2 = y2 + 3 * D2
    assert relative_state(y2, yp2, r) == state

    q2 = q + 3 ** (r - 1)
    out1 = layered_transition(state, r, t, q)
    out2 = relative_state(inverse_child(y2, t, q2), inverse_child(yp2, t, q2), r - 1)
    assert out1 == out2
