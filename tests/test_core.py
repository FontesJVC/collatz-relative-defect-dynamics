from collatz_relative_defect import accelerated_collatz, base_exponent, inverse_child


def test_inverse_families_at_one():
    expected = {
        (0, 0): 21,
        (1, 0): 1,
        (2, 0): 5,
        (1, 1): 85,
        (2, 1): 341,
    }
    for (t, q), x in expected.items():
        assert inverse_child(1, t, q) == x
        assert accelerated_collatz(x) == 1
        assert x % 3 == t


def test_extended_base_exponent_domain():
    for y in range(-25, 26):
        if y % 3:
            for t in (0, 1, 2):
                b = base_exponent(y, t)
                assert 1 <= b <= 6
                assert (pow(2, b, 9) * (y % 9)) % 9 == (1 + 3 * t) % 9
