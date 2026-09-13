from __future__ import annotations

from .core import inverse_child


def relative_state(y: int, yp: int, r: int) -> tuple[int, int]:
    if r < 1:
        raise ValueError("r must be >= 1")
    if (yp - y) % 3:
        raise ValueError("sources must agree modulo 3")
    D = (yp - y) // 3
    return y % (3 ** (r + 1)), D % (3 ** r)


def project_state(state: tuple[int, int], r: int) -> tuple[int, int]:
    """rho_r : S_{r+1} -> S_r."""
    if r < 1:
        raise ValueError("r must be >= 1")
    y, D = state
    return y % (3 ** (r + 1)), D % (3 ** r)


def layered_transition(state: tuple[int, int], r: int, t: int, q_residue: int) -> tuple[int, int]:
    """A_r from level r to level r-1 for r>=2.

    Canonical representatives of the residue state are sufficient because the
    theorem asserts representative independence.
    """
    if r < 2:
        raise ValueError("A_r is used only for r >= 2")
    y_res, D_res = state
    y = y_res % (3 ** (r + 1))
    D = D_res % (3 ** r)
    yp = y + 3 * D
    q = q_residue % (3 ** (r - 1))
    x = inverse_child(y, t, q)
    xp = inverse_child(yp, t, q)
    Dp = (xp - x) // 3
    return x % (3 ** r), Dp % (3 ** (r - 1))
