# Collatz Relative Defect Dynamics — Computational Audit

Computational stress tests, finite-instance verification, and counterexample searches for the relative ternary defect dynamics of the accelerated Collatz inverse relation.

This repository accompanies the preprint **“Relative Ternary Defect Dynamics in the Accelerated Collatz Inverse Relation”**. Its purpose is deliberately adversarial: reproduce examples, verify finite instances of the stated identities, and search systematically for counterexamples within explicit finite domains.

> **Important.** The computations in this repository are **not proofs** of the mathematical results and do **not** constitute a proof of the Collatz conjecture. The proofs are contained in the manuscript. Passing a finite computational audit means only that no counterexample was found in the tested domain.

## Current finite audit

The default consolidated audit currently checks **13,331 finite cases**, including:

- 8,919 tuples for the finite triangular base–defect bijection at depths 1–3 with \(m=1\);
- 1,485 local lift–defect isometry comparisons;
- 1,854 critical recharge checks;
- 351 layered/projective compatibility checks;
- 28 instances of the precision lower-bound construction;
- 55 instances of the finite-state obstruction family;
- direct checks of inverse families and the exact defect recurrence.

The repository now also includes:

- regression tests for previously discovered edge cases and false fixed-precision formulations;
- Hypothesis property-based tests that generate adversarial inputs automatically;
- an exhaustive countdown/recharge audit including positive and negative defects;
- a finite-horizon closure audit including \(R=2\), \(H=0\), terminal \(t=0\), and representative changes;
- a seeded random stress test for large reproducible searches.

## What is tested

| Manuscript result / structure | Computational check |
|---|---|
| Inverse families \(X_t(y,q)\) | `tests/test_core.py`, `tests/test_properties.py`, `audit_paper3.py` |
| Exact defect recurrence | `tests/test_defect.py`, `tests/test_properties.py`, `audit_paper3.py` |
| Local lift–defect isometry | `tests/test_defect.py`, `tests/test_properties.py`, `experiments/search_counterexamples.py` |
| Finite triangular base–defect bijection | `tests/test_triangular.py`, `experiments/exhaustive_triangular_bijection.py`, `audit_paper3.py` |
| Countdown/recharge dichotomy | `tests/test_defect.py`, `tests/test_properties.py`, `experiments/exhaustive_recharge.py` |
| Explicit recharge-center formula | `tests/test_defect.py`, `tests/test_properties.py` |
| Negative-defect example and fixed-point loop | `tests/test_regressions.py` |
| Terminal family \(t=0\) and corrected precision loss | `tests/test_edge_cases.py` |
| Layered relative transition | `tests/test_layered.py`, `tests/test_properties.py` |
| Representative independence | `tests/test_layered.py`, `tests/test_properties.py`, `experiments/finite_horizon_closure.py` |
| Projective compatibility | `tests/test_layered.py`, `audit_paper3.py` |
| Finite-horizon closure | `experiments/finite_horizon_closure.py` |
| Precision lower-bound construction | `audit_paper3.py` |
| Finite-state obstruction family | `audit_paper3.py` |
| Mixed large-domain stress testing | `experiments/random_stress_test.py` |

## Mathematical conventions

The accelerated odd Collatz map is

\[
T(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}.
\]

For an interior source \(y\) and family \(t\in\{0,1,2\}\), the code uses the unique base exponent \(b_t(y)\in\{1,\ldots,6\}\) satisfying

\[
2^{b_t(y)}y\equiv 1+3t\pmod 9,
\]

and

\[
X_t(y,q)=\frac{2^{b_t(y)+6q}y-1}{3}.
\]

The implementation also follows the paper's extended convention that \(b_t(u)\) is defined for every integer \(u\) that is a unit modulo \(3\).

## Running the audit

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Run the unit and property-based tests:

```bash
PYTHONPATH=src pytest -q
```

Run the consolidated finite audit:

```bash
PYTHONPATH=src python audit_paper3.py
```

Run broader adversarial searches:

```bash
PYTHONPATH=src python experiments/exhaustive_recharge.py --max-source 300 --max-defect 150 --max-q 5
PYTHONPATH=src python experiments/finite_horizon_closure.py --max-R 4 --max-H 3 --q-cap 2
PYTHONPATH=src python experiments/random_stress_test.py --seed 20260913 --cases 100000
```

Run the exhaustive finite triangular audit at its default scope:

```bash
PYTHONPATH=src python experiments/exhaustive_triangular_bijection.py
```

Windows PowerShell commands and larger suggested domains are documented in [`LOCAL_TESTING.md`](LOCAL_TESTING.md).

The expected conclusion, if all tested identities survive, is phrased conservatively:

```text
Counterexamples found: 0
No counterexample found within the tested domain.
```

## Repository layout

```text
.
├── README.md
├── LOCAL_TESTING.md
├── audit_paper3.py
├── requirements.txt
├── src/
│   └── collatz_relative_defect/
│       ├── __init__.py
│       ├── core.py
│       ├── defect.py
│       ├── layered.py
│       └── triangular.py
├── tests/
│   ├── test_core.py
│   ├── test_defect.py
│   ├── test_edge_cases.py
│   ├── test_layered.py
│   ├── test_properties.py
│   ├── test_regressions.py
│   └── test_triangular.py
└── experiments/
    ├── exhaustive_recharge.py
    ├── exhaustive_triangular_bijection.py
    ├── finite_horizon_closure.py
    ├── random_stress_test.py
    └── search_counterexamples.py
```

## Scope

The repository is intended to make the finite checks transparent and reproducible. It is especially useful for:

- reproducing numerical examples from the paper;
- checking exact integer identities against direct evaluation;
- testing residue-level transitions at many precisions;
- preserving regression cases that previously exposed false formulations;
- attempting to falsify formulas by exhaustive and property-based search;
- documenting exactly which computational domains were tested.

Future versions may add machine-readable audit summaries, archived outputs associated with a specific preprint version, and release snapshots corresponding to arXiv revisions.
