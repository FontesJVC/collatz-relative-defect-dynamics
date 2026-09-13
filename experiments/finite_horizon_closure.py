#!/usr/bin/env python3
from __future__ import annotations

import argparse
from itertools import product

from collatz_relative_defect import inverse_child, layered_transition, relative_state
from collatz_relative_defect.reporting import run_with_report


def admissible_words(H: int):
    if H == 0:
        yield ()
        return
    yield from product((1, 2), repeat=H)
    for prefix in product((1, 2), repeat=H - 1):
        yield prefix + (0,)


def verify_case(y: int, yp: int, R: int, tau: tuple[int, ...], qs: tuple[int, ...]) -> int:
    H = len(tau)
    r0 = R + H - 1
    state = relative_state(y, yp, r0)
    yd, ypd = y, yp
    checked = 1
    for j, (t, q) in enumerate(zip(tau, qs)):
        r = r0 - j
        if r < 2:
            raise AssertionError("A_r should only be used for r >= 2")
        qres = q % (3 ** (r - 1))
        state = layered_transition(state, r, t, qres)
        yd = inverse_child(yd, t, q)
        ypd = inverse_child(ypd, t, q)
        if state != relative_state(yd, ypd, r - 1):
            raise AssertionError((y, yp, R, tau, qs, j))
        checked += 1
    return checked


def representative_independence(y: int, yp: int, R: int, tau: tuple[int, ...], qs: tuple[int, ...]) -> int:
    H = len(tau)
    r0 = R + H - 1
    D = (yp - y) // 3

    y2 = y + 2 * (3 ** (r0 + 1))
    D2 = D + 2 * (3 ** r0)
    yp2 = y2 + 3 * D2
    if relative_state(y, yp, r0) != relative_state(y2, yp2, r0):
        raise AssertionError("alternate representatives changed the initial state")

    qs2 = tuple(q + 3 ** (r0 - j - 1) for j, q in enumerate(qs))

    s1 = relative_state(y, yp, r0)
    s2 = relative_state(y2, yp2, r0)
    checked = 1
    for j, t in enumerate(tau):
        r = r0 - j
        s1 = layered_transition(s1, r, t, qs[j])
        s2 = layered_transition(s2, r, t, qs2[j])
        if s1 != s2:
            raise AssertionError((y, yp, R, tau, qs, j, "representative independence"))
        checked += 1
    return checked


def audit(max_R: int, max_H: int, q_cap: int) -> int:
    pairs = ((1, 7), (1, 61), (1, 85), (5, 113), (7, 85))
    total = 0
    for R in range(2, max_R + 1):
        for H in range(0, max_H + 1):
            for tau in admissible_words(H):
                q_ranges = []
                r0 = R + H - 1
                for j in range(H):
                    modulus = 3 ** (r0 - j - 1)
                    q_ranges.append(range(min(modulus, q_cap + 1)))
                tuples = product(*q_ranges) if q_ranges else [()]
                for qs in tuples:
                    qs = tuple(qs)
                    for y, yp in pairs:
                        total += verify_case(y, yp, R, tau, qs)
                        total += representative_independence(y, yp, R, tau, qs)
    return total


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--max-R", type=int, default=4)
    p.add_argument("--max-H", type=int, default=3)
    p.add_argument("--q-cap", type=int, default=2)
    args = p.parse_args()
    total = audit(args.max_R, args.max_H, args.q_cap)
    print("Finite-horizon closure audit")
    print(f"max_R:             {args.max_R}")
    print(f"max_H:             {args.max_H}")
    print(f"q_cap:             {args.q_cap}")
    print(f"state comparisons: {total}")
    print("counterexamples:   0")
    print("Includes H=0, R=2, final-edge t=0, source/defect representative changes,")
    print("and lift representative changes.")


if __name__ == "__main__":
    run_with_report("finite_horizon_closure", main)
