#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
from collections import Counter
from fractions import Fraction

from collatz_relative_defect import (
    accelerated_collatz,
    base_exponent,
    defect_recurrence_step,
    inverse_child,
    layered_transition,
    local_isometry_holds,
    relative_state,
    v3,
)


def random_interior(rng: random.Random, max_source: int) -> int:
    while True:
        y = rng.randrange(1, max_source + 1, 2)
        if y % 3:
            return y


def v3_fraction(z: Fraction) -> int:
    return v3(z.numerator) - v3(z.denominator)


def run(seed: int, cases: int, max_source: int, max_q: int) -> Counter:
    rng = random.Random(seed)
    counts: Counter[str] = Counter()

    for _ in range(cases):
        kind = rng.randrange(5)

        if kind == 0:
            y = random_interior(rng, max_source)
            t = rng.randrange(3)
            q = rng.randrange(max_q + 1)
            x = inverse_child(y, t, q)
            if accelerated_collatz(x) != y or x % 3 != t:
                raise AssertionError(("inverse", y, t, q))
            counts["inverse"] += 1

        elif kind == 1:
            y = random_interior(rng, max_source)
            t = rng.randrange(3)
            q = rng.randrange(max_q + 1)
            qp = rng.randrange(max_q + 1)
            if q == qp:
                qp += 1
            if not local_isometry_holds(y, t, q, qp):
                raise AssertionError(("isometry", y, t, q, qp))
            counts["isometry"] += 1

        elif kind == 2:
            ybar = random_interior(rng, max_source)
            D = 2 * rng.randint(-200, 200)
            y = ybar + 3 * D
            if y <= 0:
                continue
            t = rng.randrange(3)
            q = rng.randrange(min(max_q, 6) + 1)
            ref = inverse_child(ybar, t, 0)
            full = inverse_child(y, t, q)
            direct = (full - ref) // 3
            predicted, _, _ = defect_recurrence_step(ybar, D, t, q)
            if direct != predicted:
                raise AssertionError(("defect recurrence", ybar, D, t, q))
            counts["defect_recurrence"] += 1

        elif kind == 3:
            y = random_interior(rng, max_source)
            D = 2 * rng.randint(-200, 200)
            if D == 0:
                continue
            yp = y + 3 * D
            if yp <= 0 or yp % 3 == 0:
                continue
            t = rng.randrange(3)
            q = rng.randrange(min(max_q, 6) + 1)
            x = inverse_child(y, t, q)
            xp = inverse_child(yp, t, q)
            Dp = (xp - x) // 3
            if D % 3 == 0:
                b = base_exponent(y, t)
                if base_exponent(yp, t) != b:
                    raise AssertionError(("countdown exponent", y, yp, t, q))
                if Dp != (64**q) * (2**b) * D // 3:
                    raise AssertionError(("countdown", y, yp, t, q))
                if v3(Dp) != v3(D) - 1:
                    raise AssertionError(("countdown valuation", y, yp, t, q))
                counts["countdown"] += 1
            else:
                a = D % 3
                b = base_exponent(y, t)
                bp = base_exponent(y + 3 * a, t)
                center = (Fraction(2) ** (b - bp) - 1) * Fraction(y, 3)
                if v3(xp - x) != v3_fraction(Fraction(D) - center):
                    raise AssertionError(("recharge", y, yp, t, q))
                counts["recharge"] += 1

        else:
            r = rng.randint(2, 5)
            y = random_interior(rng, min(max_source, 20_000))
            D = 2 * rng.randint(0, 500)
            yp = y + 3 * D
            t = rng.randrange(3)
            q = rng.randrange(3 ** (r - 1))
            state = relative_state(y, yp, r)
            out = layered_transition(state, r, t, q)
            expected = relative_state(inverse_child(y, t, q), inverse_child(yp, t, q), r - 1)
            if out != expected:
                raise AssertionError(("layered", y, yp, r, t, q))
            counts["layered"] += 1

    return counts


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=20260913)
    p.add_argument("--cases", type=int, default=100_000)
    p.add_argument("--max-source", type=int, default=1_000_000)
    p.add_argument("--max-q", type=int, default=10)
    args = p.parse_args()

    counts = run(args.seed, args.cases, args.max_source, args.max_q)
    print("Random adversarial stress test")
    print(f"seed:              {args.seed}")
    print(f"requested cases:   {args.cases}")
    print(f"completed checks:  {sum(counts.values())}")
    for key in sorted(counts):
        print(f"{key:18s} {counts[key]}")
    print("counterexamples:   0")
    print("No counterexample found within the sampled domain.")


if __name__ == "__main__":
    main()
