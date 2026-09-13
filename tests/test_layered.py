from collatz_relative_defect import layered_transition, project_state, relative_state


def test_layered_transition_matches_integer_representatives():
    pairs = [(1, 7), (1, 61), (5, 113), (7, 85)]
    for r in (2, 3, 4):
        for y, yp in pairs:
            if (yp - y) % 3:
                continue
            state = relative_state(y, yp, r)
            for t in (0, 1, 2):
                for q in range(3 ** (r - 1)):
                    out = layered_transition(state, r, t, q)
                    from collatz_relative_defect import inverse_child
                    x = inverse_child(y, t, q)
                    xp = inverse_child(yp, t, q)
                    expected = relative_state(x, xp, r - 1)
                    assert out == expected


def test_projective_compatibility():
    for r in (2, 3, 4):
        y, yp = 1, 85
        high = relative_state(y, yp, r + 1)
        low = project_state(high, r)
        for t in (0, 1, 2):
            for Q in range(3 ** r):
                lhs = project_state(layered_transition(high, r + 1, t, Q), r - 1)
                rhs = layered_transition(low, r, t, Q % (3 ** (r - 1)))
                assert lhs == rhs


def test_representative_independence_directly():
    from collatz_relative_defect import inverse_child

    for r in (2, 3, 4):
        y, yp = 1, 85
        D = (yp - y) // 3
        for cy in (-2, -1, 1, 2):
            for cD in (-2, -1, 1, 2):
                y2 = y + cy * (3 ** (r + 1))
                D2 = D + cD * (3 ** r)
                yp2 = y2 + 3 * D2
                for t in (0, 1, 2):
                    for q in range(3 ** (r - 1)):
                        x1 = inverse_child(y, t, q)
                        xp1 = inverse_child(yp, t, q)
                        x2 = inverse_child(y2, t, q)
                        xp2 = inverse_child(yp2, t, q)
                        assert relative_state(x1, xp1, r - 1) == relative_state(x2, xp2, r - 1)
