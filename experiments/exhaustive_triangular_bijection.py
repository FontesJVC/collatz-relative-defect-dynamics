from __future__ import annotations

import argparse
from itertools import product

from collatz_relative_defect import (
    admissible_words,
    triangular_defect_residues,
    triangular_domain_ranges,
)
from collatz_relative_defect.reporting import run_with_report


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
    print("Exhaustive triangular base-defect audit")
    print(f"y0:            {args.y0}")
    print(f"m:             {args.m}")
    print(f"max_depth:     {args.max_depth}")
    print(f"tuples tested: {total}")
    print(f"failures:      {failures}")
    if failures == 0:
        print("No counterexample found within the tested finite quotient domain.")


if __name__ == "__main__":
    run_with_report("exhaustive_triangular_bijection", main)
