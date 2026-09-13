from __future__ import annotations


def v2(n: int) -> int:
    """2-adic valuation for a nonzero integer."""
    if n == 0:
        raise ValueError("v2(0) is undefined")
    n = abs(n)
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def v3(n: int) -> int:
    """3-adic valuation for a nonzero integer."""
    if n == 0:
        raise ValueError("v3(0) is undefined")
    n = abs(n)
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k


def accelerated_collatz(n: int) -> int:
    """Accelerated Collatz map on positive odd integers."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")
    m = 3 * n + 1
    return m // (2 ** v2(m))


def is_interior(y: int) -> bool:
    return y > 0 and y % 2 == 1 and y % 3 != 0


def base_exponent(y: int, t: int) -> int:
    """Unique b in {1,...,6} with 2^b y = 1+3t (mod 9).

    The congruence only needs y to be a unit modulo 3; y need not be positive
    or odd. This matches the extended convention used in the paper.
    """
    if y % 3 == 0:
        raise ValueError("y must be a unit modulo 3")
    if t not in (0, 1, 2):
        raise ValueError("t must be 0, 1, or 2")
    target = (1 + 3 * t) % 9
    matches = [b for b in range(1, 7) if (pow(2, b, 9) * (y % 9)) % 9 == target]
    if len(matches) != 1:
        raise AssertionError(f"expected unique base exponent, got {matches}")
    return matches[0]


def inverse_child(y: int, t: int, q: int = 0) -> int:
    """X_t(y,q) = (2^(b_t(y)+6q) y - 1)/3."""
    if q < 0:
        raise ValueError("q must be nonnegative")
    b = base_exponent(y, t)
    num = (2 ** (b + 6 * q)) * y - 1
    if num % 3:
        raise AssertionError("inverse formula numerator is not divisible by 3")
    return num // 3


def admissible_family_word(tau: tuple[int, ...] | list[int]) -> bool:
    """t=0 may occur only at the final edge."""
    for j, t in enumerate(tau):
        if t not in (0, 1, 2):
            return False
        if t == 0 and j != len(tau) - 1:
            return False
    return True


def follow_inverse_path(y0: int, tau: tuple[int, ...] | list[int], qs: tuple[int, ...] | list[int]) -> list[int]:
    if len(tau) != len(qs):
        raise ValueError("tau and qs must have the same length")
    if not admissible_family_word(tau):
        raise ValueError("family word is not admissible")
    ys = [y0]
    y = y0
    for t, q in zip(tau, qs):
        y = inverse_child(y, t, q)
        ys.append(y)
    return ys
