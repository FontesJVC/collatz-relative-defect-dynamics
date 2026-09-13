from __future__ import annotations

from itertools import product

from collatz_relative_defect import (
    accelerated_collatz,
    defect_recurrence_step,
    follow_inverse_path,
    inverse_child,
    layered_transition,
    local_isometry_holds,
    project_state,
    recharge_valuation_identity,
    reference_path,
    relative_state,
    v3,
)


def check(name, fn):
    try:
        count = fn()
    except Exception as exc:
        print(f"[FAIL] {name}: {exc}")
        return False, 0
    print(f"[PASS] {name:<38} ({count} cases)")
    return True, count


def inverse_families():
    count = 0
    for y in range(1, 80, 2):
        if y % 3 == 0:
            continue
        for t in (0, 1, 2):
            for q in range(4):
                x = inverse_child(y, t, q)
                assert accelerated_collatz(x) == y
                assert x % 3 == t
                count += 1
    return count


def defect_recurrence():
    count = 0
    words = [(1,), (2,), (0,), (1, 1), (1, 2), (2, 1), (2, 2), (1, 0), (2, 0)]
    for y0 in (1, 5, 7, 11, 13):
        if y0 % 3 == 0:
            continue
        for tau in words:
            for qs in product(range(3), repeat=len(tau)):
                ref = reference_path(y0, tau)
                full = follow_inverse_path(y0, tau, qs)
                D = 0
                for j, (t, q) in enumerate(zip(tau, qs)):
                    pred, _, _ = defect_recurrence_step(ref[j], D, t, q)
                    D = (full[j + 1] - ref[j + 1]) // 3
                    assert pred == D
                count += 1
    return count


def local_isometry():
    count = 0
    for y in range(1, 100, 2):
        if y % 3 == 0:
            continue
        for t in (0, 1, 2):
            for q in range(6):
                for qp in range(q + 1, 6):
                    assert local_isometry_holds(y, t, q, qp)
                    count += 1
    return count


def recharge():
    count = 0
    for y in range(1, 60, 2):
        if y % 3 == 0:
            continue
        for D in range(-20, 21):
            if D == 0 or D % 3 == 0:
                continue
            yp = y + 3 * D
            if yp <= 0 or yp % 2 == 0 or yp % 3 == 0:
                continue
            for t in (0, 1, 2):
                for q in range(3):
                    assert recharge_valuation_identity(y, yp, t, q)
                    count += 1
    return count


def layered():
    count = 0
    for r in (2, 3, 4):
        y, yp = 1, 85
        high = relative_state(y, yp, r + 1)
        low = project_state(high, r)
        for t in (0, 1, 2):
            for Q in range(3 ** r):
                lhs = project_state(layered_transition(high, r + 1, t, Q), r - 1)
                rhs = layered_transition(low, r, t, Q % (3 ** (r - 1)))
                assert lhs == rhs
                count += 1
    return count


def finite_state_obstruction_examples():
    count = 0
    for L in range(2, 12):
        for K in range(L + 1, 13):
            u = 1 + 2 * (3 ** L)
            v = 1 + 2 * (3 ** K)
            for _ in range(L - 1):
                u = inverse_child(u, 1, 0)
                v = inverse_child(v, 1, 0)
            assert v3(u - 1) == 1
            assert v3(v - 1) >= 2
            count += 1
    return count


def main():
    print("Paper 3 computational audit")
    print("=" * 32)
    checks = [
        ("Inverse families", inverse_families),
        ("Exact defect recurrence", defect_recurrence),
        ("Local lift-defect isometry", local_isometry),
        ("Countdown/recharge critical identity", recharge),
        ("Layered/projective compatibility", layered),
        ("Finite-state obstruction examples", finite_state_obstruction_examples),
    ]
    total = 0
    ok = True
    for name, fn in checks:
        passed, count = check(name, fn)
        ok &= passed
        total += count
    print("-" * 32)
    print(f"Total finite cases checked: {total}")
    if ok:
        print("Counterexamples found: 0")
        print("No counterexample found within the tested domain.")
        print("These computations support finite instances; they do not replace the proofs.")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
