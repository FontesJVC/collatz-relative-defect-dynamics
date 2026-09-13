#!/usr/bin/env python3
from __future__ import annotations

import argparse
from fractions import Fraction

from collatz_relative_defect import base_exponent, inverse_child, v3


def v3_fraction(x: Fraction) -> int:
    if x == 0:
        raise ValueError("v3(0) undefined")
    return v3(x.numerator) - v3(x.denominator)


def audit(max_source: int, max_defect: int, max_q: int) -> tuple[int, int]:
    countdown = 0
    critical = 0
    for y in range(1, max_source + 1, 2):
        if y % 3 == 0:
            continue
        for D in range(-max_defect, max_defect + 1):
            if D == 0 or D % 2:
                continue
            yp = y + 3 * D
            if yp <= 0 or yp % 2 == 0 or yp % 3 == 0:
                continue
            for t in (0, 1, 2):
                b = base_exponent(y, t)
                for q in range(max_q + 1):
                    x = inverse_child(y, t, q)
                    xp = inverse_child(yp, t, q)
                    if (xp - x) % 3:
                        raise AssertionError("destination difference is not divisible by 3")
                    Dp = (xp - x) // 3
                    if D % 3 == 0:
                        if base_exponent(yp, t) != b:
                            raise AssertionError("countdown base exponents differ")
                        predicted = (64**q) * (2**b) * D // 3
                        if Dp != predicted:
                            raise AssertionError((y, yp, t, q, Dp, predicted))
                        if v3(Dp) != v3(D) - 1:
                            raise AssertionError((y, yp, t, q, "countdown valuation"))
                        countdown += 1
                    else:
                        a = D % 3
                        bp = base_exponent(y + 3 * a, t)
                        center = (Fraction(2) ** (b - bp) - 1) * Fraction(y, 3)
                        if v3(xp - x) != v3_fraction(Fraction(D) - center):
                            raise AssertionError((y, yp, t, q, "recharge valuation"))
                        critical += 1
    return countdown, critical


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--max-source", type=int, default=300)
    p.add_argument("--max-defect", type=int, default=150)
    p.add_argument("--max-q", type=int, default=5)
    args = p.parse_args()
    c0, c1 = audit(args.max_source, args.max_defect, args.max_q)
    print("Exhaustive countdown/recharge audit")
    print(f"countdown cases: {c0}")
    print(f"critical cases:  {c1}")
    print(f"total cases:     {c0 + c1}")
    print("counterexamples: 0")
    print("No counterexample found within the tested domain.")


if __name__ == "__main__":
    main()
