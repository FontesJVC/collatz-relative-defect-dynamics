# Local testing guide

This repository is intentionally designed so that larger finite searches can be run on a local machine.

## Windows PowerShell setup

If the repository is already cloned with GitHub Desktop, open PowerShell in the repository folder and run:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONPATH="$PWD\src"
```

Using the virtual-environment Python directly avoids PowerShell execution-policy issues with `Activate.ps1`.

## Automatic text reports

The command-line audit scripts print their normal output to the console **and** automatically save a timestamped `.txt` report under:

```text
audit_results/
```

Each report records:

- local start and finish timestamps;
- elapsed time;
- Python and platform versions;
- Git commit, when Git is available on the command line;
- the exact command and parameters;
- the complete console result.

Example filenames:

```text
audit_results/audit_paper3_20260913_143012.txt
audit_results/exhaustive_recharge_20260913_144501.txt
audit_results/random_stress_20260913_151030.txt
```

## Light audit

This is the recommended first run.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe audit_paper3.py
.\.venv\Scripts\python.exe experiments\exhaustive_triangular_bijection.py
```

The `pytest` run includes deterministic unit tests, regression cases, and Hypothesis property-based tests. Pytest itself does not create a text report by default; the standalone audit scripts do.

## Medium audit

```powershell
.\.venv\Scripts\python.exe experiments\exhaustive_recharge.py --max-source 1000 --max-defect 500 --max-q 8
.\.venv\Scripts\python.exe experiments\finite_horizon_closure.py --max-R 5 --max-H 4 --q-cap 3
.\.venv\Scripts\python.exe experiments\random_stress_test.py --seed 20260913 --cases 1000000
```

## Heavy audit

These settings may take substantially longer and create very large integers.

```powershell
.\.venv\Scripts\python.exe experiments\exhaustive_recharge.py --max-source 5000 --max-defect 2000 --max-q 12
.\.venv\Scripts\python.exe experiments\finite_horizon_closure.py --max-R 6 --max-H 5 --q-cap 4
.\.venv\Scripts\python.exe experiments\random_stress_test.py --seed 20260913 --cases 10000000 --max-source 10000000 --max-q 12
.\.venv\Scripts\python.exe experiments\exhaustive_triangular_bijection.py --max-depth 4 --m 1
```

The triangular search grows particularly quickly. Start with depth 3 before attempting depth 4.

## Reproducibility

The random stress test records its seed. If a failure appears, rerun with the same seed and case count before changing any code.

For any failing command, keep the generated report. A useful bug report should include:

- the generated `.txt` report;
- the exact command;
- Python version;
- Git commit when available;
- the random seed, when applicable;
- the smallest failing example reported by Hypothesis or by the script.

## Interpretation

A successful finite run means only that no counterexample was found inside the tested domain. It does not replace the proofs in the manuscript and does not prove the Collatz conjecture.
