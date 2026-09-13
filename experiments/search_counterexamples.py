from __future__ import annotations

import argparse
from itertools import product

from collatz_relative_defect import local_isometry_holds, recharge_valuation_identity


def search(max_source: int, max_q: int) -> tuple[int, int]:
    checked = 0
    failures = 0
    units = [y for y in range(1, max_source + 1, 2) if y % 3]
    for y, t, q, qp in product(units, (0, 1, 2), range(max_q + 1), range(max_q + 1)):
        if q == qp:
            continue
        checked += 1
        if not local_isometry_holds(y, t, q, qp):
            failures += 1
            print("ISOMETRY FAILURE", y, t, q, qp)

    for y in units:
        for D in range(-max_source, max_source + 1):
            if D == 0 or D % 3 == 0:
                continue
            yp = y + 3 * D
            if yp <= 0 or yp % 2 == 0 or yp % 3 == 0:
                continue
            for t in (0, 1, 2):
                for q in range(max_q + 1):
                    checked += 1
                    if not recharge_valuation_identity(y, yp, t, q):
                        failures += 1
                        print("RECHARGE FAILURE", y, yp, t, q)
    return checked, failures


def main() -> None:
    parser = argparse.ArgumentParser(description="Finite counterexample search for Paper 3 identities")
    parser.add_argument("--max-source", type=int, default=75)
    parser.add_argument("--max-q", type=int, default=4)
    args = parser.parse_args()
    checked, failures = search(args.max_source, args.max_q)
    print(f"Checked cases: {checked}")
    print(f"Counterexamples found: {failures}")
    if failures == 0:
        print("No counterexample found within the tested domain.")


if __name__ == "__main__":
    main()
