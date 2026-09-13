from collatz_relative_defect import inverse_child, reference_path, follow_inverse_path


def test_loop():
    assert inverse_child(1, 1, 0) == 1


def test_negative_defect():
    tau = (2, 2, 1)
    reference = reference_path(1, tau)
    full = follow_inverse_path(1, tau, (1, 0, 0))
    assert (full[-1] - reference[-1]) // 3 == -138
