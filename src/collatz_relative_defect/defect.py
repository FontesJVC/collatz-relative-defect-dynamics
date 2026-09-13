from __future__ import annotations

from fractions import Fraction

from .core import base_exponent, inverse_child, v3


def reference_path(y0: int, tau: tuple[int, ...] | list[int]) -> list[int]:
    ys = [y0]
    y = y0
    for t in tau:
        y = inverse_child(y, t, 0)
        ys.append(y)
    return ys


def exact_defects(full_path: list[int], reference: list[int]) -> list[int]:
    if len(full_path) != len(reference):
        raise ValueError("paths must have equal length")
    out = []
    for y, ybar in zip(full_path, reference):
        diff = y - ybar
        if diff % 3:
            raise AssertionError("path difference must be divisible by 3")
        out.append(diff // 3)
    return out


def defect_recurrence_step(ybar: int, defect: int, t: int, q: int) -> tuple[int, int, int]:
    """Return (D_next, A, U) for the exact defect recurrence."""
    a = defect % 3
    z = (defect - a) // 3
    b = base_exponent(ybar, t)
    b_tilde = base_exponent(ybar + 3 * a, t)
    A_num = (64 ** q) * (2 ** b_tilde) * (ybar + 3 * a) - (2 ** b) * ybar
    if A_num % 9:
        raise AssertionError("A numerator must be divisible by 9")
    A = A_num // 9
    U = (64 ** q) * (2 ** b_tilde)
    return A + U * z, A, U


def local_lift_defect_difference(y: int, t: int, q: int, qp: int) -> int:
    """Difference of child defects for two lift choices, with same reference."""
    if q == qp:
        return 0
    diff = inverse_child(y, t, q) - inverse_child(y, t, qp)
    if diff % 3:
        raise AssertionError("child difference must be divisible by 3")
    return diff // 3


def local_isometry_holds(y: int, t: int, q: int, qp: int) -> bool:
    if q == qp:
        return True
    d = local_lift_defect_difference(y, t, q, qp)
    return v3(d) == v3(q - qp)


def recharge_center(y: int, t: int, a: int) -> Fraction:
    """c_{t,a}(y) = ((2^(b-b')-1)y)/3 as a rational/3-adic center."""
    if a not in (1, 2):
        raise ValueError("a must be 1 or 2 in the critical regime")
    b = base_exponent(y, t)
    bp = base_exponent(y + 3 * a, t)
    return (Fraction(2) ** (b - bp) - 1) * Fraction(y, 3)


def v3_fraction(x: Fraction) -> int:
    if x == 0:
        raise ValueError("v3(0) is undefined")
    return v3(x.numerator) - v3(x.denominator)


def relative_step(y: int, yp: int, t: int, q: int = 0) -> tuple[int, int, int]:
    """Apply a common inverse edge and return (x, x', D')."""
    if (yp - y) % 3:
        raise ValueError("sources must agree modulo 3")
    x = inverse_child(y, t, q)
    xp = inverse_child(yp, t, q)
    if (xp - x) % 3:
        raise AssertionError("destination difference must be divisible by 3")
    return x, xp, (xp - x) // 3


def recharge_valuation_identity(y: int, yp: int, t: int, q: int = 0) -> bool:
    """Verify v3(x'-x)=v3(D-c) in the critical regime 3 does not divide D."""
    D = (yp - y) // 3
    if D % 3 == 0:
        raise ValueError("critical regime requires 3 not dividing D")
    a = D % 3
    c = recharge_center(y, t, a)
    x, xp, _ = relative_step(y, yp, t, q)
    return v3(xp - x) == v3_fraction(Fraction(D) - c)
