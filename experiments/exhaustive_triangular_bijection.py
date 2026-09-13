from __future__ import annotations

import argparse
from itertools import product

from collatz_relative_defect import (
    admissible_words,
    triangular_defect_residues,
    triangular_domain_ranges,
)


def audit(y0: int, m: int, max_depth: int) -> tuple[int, int]:
    total = 0
    failures = 0
    for d in range(1, max_depth + 1):
        for tau in admissible_words(d):
            ranges = triangular_domain_ranges(d, m)
            outputs = set()
            inputs = 1
            for r in ranges:
                inputs *= len(r)
            for qs in product(*ranges):
                outputs.add(triangular_defect_residues(y0, tau, m, qs))
                total += 1
            if len(outputs) != inputs:
                failures += 1
                print(f"BIJECTION FAILURE depth={d} tau={tau}: {len(outputs)} != {inputs}")
    return total, failures


def main() -> None:
    parser = argparse.ArgumentParser(description="Exhaustive finite audit of the triangular base-defect bijection")
    parser.add_argument("--y0", type=int, default=1)
    parser.add_argument("--m", type=int, default=1)
    parser.add_argument("--max-depth", type=int, default=3)
    args = parser.parse_args()
    total, failures = audit(args.y0, args.m, args.max_depth)
    print(f"Tuples tested: {total}")
    print(f"Failures: {failures}")
    if failures == 0:
        print("No counterexample found within the tested finite quotient domain.")


if __name__ == "__main__":
    main()
