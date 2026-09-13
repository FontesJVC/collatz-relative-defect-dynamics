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

The unit-test suite additionally checks representative independence for layered transitions.

## What is tested

| Manuscript result / structure | Computational check |
|---|---|
| Inverse families \(X_t(y,q)\) | `tests/test_core.py`, `audit_paper3.py` |
| Exact defect recurrence | `tests/test_defect.py`, `audit_paper3.py` |
| Local lift–defect isometry | `tests/test_defect.py`, `experiments/search_counterexamples.py` |
| Finite triangular base–defect bijection | `tests/test_triangular.py`, `experiments/exhaustive_triangular_bijection.py`, `audit_paper3.py` |
| Countdown/recharge dichotomy | `tests/test_defect.py`, `experiments/search_counterexamples.py` |
| Explicit recharge-center formula | `tests/test_defect.py` |
| Layered relative transition | `tests/test_layered.py` |
| Representative independence | `tests/test_layered.py` |
| Projective compatibility | `tests/test_layered.py`, `audit_paper3.py` |
| Precision lower-bound construction | `audit_paper3.py` |
| Finite-state obstruction family | `audit_paper3.py` |

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

Run the unit tests:

```bash
PYTHONPATH=src pytest -q
```

Run the consolidated finite audit:

```bash
PYTHONPATH=src python audit_paper3.py
```

Run a broader counterexample search:

```bash
PYTHONPATH=src python experiments/search_counterexamples.py --max-source 200 --max-q 6
```

Run the exhaustive finite triangular audit at its default scope:

```bash
PYTHONPATH=src python experiments/exhaustive_triangular_bijection.py
```

The expected conclusion, if all tested identities survive, is phrased conservatively:

```text
Counterexamples found: 0
No counterexample found within the tested domain.
```

## Repository layout

```text
.
├── README.md
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
│   ├── test_layered.py
│   └── test_triangular.py
└── experiments/
    ├── exhaustive_triangular_bijection.py
    └── search_counterexamples.py
```

## Scope

The repository is intended to make the finite checks transparent and reproducible. It is especially useful for:

- reproducing numerical examples from the paper;
- checking exact integer identities against direct evaluation;
- testing residue-level transitions at many precisions;
- attempting to falsify formulas by exhaustive finite search;
- documenting exactly which computational domains were tested.

Future versions may add finite-horizon closure stress tests, larger search domains, machine-readable audit summaries, and archived outputs associated with a specific preprint version.
