from __future__ import annotations

from itertools import product

from .core import follow_inverse_path
from .defect import reference_path


def admissible_words(depth: int) -> list[tuple[int, ...]]:
    if depth < 1:
        raise ValueError("depth must be >= 1")
    interior = list(product((1, 2), repeat=depth))
    terminal = [prefix + (0,) for prefix in product((1, 2), repeat=depth - 1)]
    return interior + terminal


def precisions(depth: int, m: int) -> list[int]:
    if depth < 1 or m < 1:
        raise ValueError("depth and m must be >= 1")
    return [m + depth - j for j in range(depth + 1)]


def triangular_defect_residues(
    y0: int,
    tau: tuple[int, ...],
    m: int,
    qs: tuple[int, ...],
) -> tuple[int, ...]:
    d = len(tau)
    if len(qs) != d:
        raise ValueError("qs must have the same length as tau")
    p = precisions(d, m)
    ref = reference_path(y0, tau)
    full = follow_inverse_path(y0, tau, qs)
    residues = []
    for j in range(1, d + 1):
        D = (full[j] - ref[j]) // 3
        residues.append(D % (3 ** p[j]))
    return tuple(residues)


def triangular_domain_ranges(depth: int, m: int) -> tuple[range, ...]:
    p = precisions(depth, m)
    return tuple(range(3 ** p[j + 1]) for j in range(depth))
