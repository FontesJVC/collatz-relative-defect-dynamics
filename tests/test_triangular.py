from itertools import product

from collatz_relative_defect import admissible_words, triangular_defect_residues, triangular_domain_ranges


def test_triangular_bijection_depths_1_to_3_m1():
    total = 0
    for d in range(1, 4):
        for tau in admissible_words(d):
            ranges = triangular_domain_ranges(d, 1)
            outputs = {
                triangular_defect_residues(1, tau, 1, qs)
                for qs in product(*ranges)
            }
            domain_size = 1
            for r in ranges:
                domain_size *= len(r)
            assert len(outputs) == domain_size
            total += domain_size
    assert total == 8919
