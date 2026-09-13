from collatz_relative_defect import accelerated_collatz, inverse_child, relative_state, relative_step


def test_terminal_family_t0():
    for y in (1, 5, 7, 11, 13, 17):
        x = inverse_child(y, 0, 0)
        assert x % 3 == 0
        assert accelerated_collatz(x) == y


def test_corrected_layered_precision_on_known_pair():
    assert relative_state(1, 7, 2) == relative_state(1, 61, 2)
    _, _, Da = relative_step(1, 7, 1, 0)
    _, _, Db = relative_step(1, 61, 1, 0)
    assert (Da, Db) == (12, 108)
    assert Da % 9 != Db % 9
    assert Da % 3 == Db % 3


def test_R2_H0_state_exists_without_transition():
    y, yp = 1, 85
    assert relative_state(y, yp, 1) == (1, 1)
