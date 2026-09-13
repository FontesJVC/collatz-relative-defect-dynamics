# Audit results

The standalone audit scripts automatically write timestamped text reports to this directory while also printing the same results to the console.

Reports include the command-line parameters, timestamps, elapsed time, Python/platform information, Git commit when available, and the complete audit output.

Generated `.txt` files are intentionally not committed automatically. A selected report may be added to the repository or archived with a release when it corresponds to a specific preprint version.

A successful finite report means only that no counterexample was found inside the tested domain. It does not replace the proofs in the manuscript and does not prove the Collatz conjecture.
