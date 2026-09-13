# Local testing guide

This repository is intentionally designed so that larger finite searches can be run on a local machine.

## Windows PowerShell setup

```powershell
git clone https://github.com/FontesJVC/collatz-relative-defect-dynamics.git
cd collatz-relative-defect-dynamics
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
$env:PYTHONPATH="src"
```

## Light audit

This is the recommended first run.

```powershell
pytest -q
python audit_paper3.py
python experiments/exhaustive_triangular_bijection.py
```

The `pytest` run includes deterministic unit tests, regression cases, and Hypothesis property-based tests.

## Medium audit

```powershell
python experiments/exhaustive_recharge.py --max-source 1000 --max-defect 500 --max-q 8
python experiments/finite_horizon_closure.py --max-R 5 --max-H 4 --q-cap 3
python experiments/random_stress_test.py --seed 20260913 --cases 1000000
```

## Heavy audit

These settings may take substantially longer and create very large integers.

```powershell
python experiments/exhaustive_recharge.py --max-source 5000 --max-defect 2000 --max-q 12
python experiments/finite_horizon_closure.py --max-R 6 --max-H 5 --q-cap 4
python experiments/random_stress_test.py --seed 20260913 --cases 10000000 --max-source 10000000 --max-q 12
python experiments/exhaustive_triangular_bijection.py --max-depth 4 --m 1
```

The triangular search grows particularly quickly. Start with depth 3 before attempting depth 4.

## Reproducibility

The random stress test prints its seed. If a failure appears, rerun with the same seed and case count before changing any code.

For any failing command, save the complete console output. A useful bug report should include:

- the exact command;
- Python version (`python --version`);
- the Git commit being tested (`git rev-parse HEAD`);
- the random seed, when applicable;
- the smallest failing example reported by Hypothesis or by the script.

## Interpretation

A successful finite run means only that no counterexample was found inside the tested domain. It does not replace the proofs in the manuscript and does not prove the Collatz conjecture.
