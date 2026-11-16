# Lab 6 — Code and Branch Coverage Analysis

## Purpose

The `highway_toll.py` module contains decisions for valid versus invalid axle counts, known versus fallback toll rates, peak pricing, FASTag discounts, exempt vehicles, and monthly-pass advice. The two test modules measure how thoroughly those statements and decision outcomes are exercised.

## Reproduce the results

From this `lab6` directory, install the dependencies and run the line-focused suite:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pytest coverage
.venv/bin/python -m coverage erase
.venv/bin/python -m coverage run --source=highway_toll -m pytest -q CodeCoverageTest_Nikhil_application.py
.venv/bin/python -m coverage report -m
```

Run the branch-focused suite separately with branch measurement enabled:

```bash
.venv/bin/python -m coverage erase
.venv/bin/python -m coverage run --branch --source=highway_toll -m pytest -q BranchCoverageTest_Nikhil_application.py
.venv/bin/python -m coverage report -m
```

## Results and interpretation

| Suite and measurement | Tests | Statements | Branches | Coverage.py total |
|---|---:|---:|---:|---:|
| `CodeCoverageTest_Nikhil_application.py`, line mode | 6 passed | 28/28 | Not measured | 100% |
| Same statement-focused suite, branch diagnostic | 6 passed | 28/28 | 16/18 outcomes (2 partial) | 96% combined |
| `BranchCoverageTest_Nikhil_application.py`, branch mode | 6 passed | 28/28 | 18/18 outcomes | 100% |

The line-focused suite executes every executable statement, so its line report is 100%. When branch tracing is enabled for that same suite, coverage.py identifies two untested arcs: the false outcome of `if is_peak` and the false outcome of `if has_fastag`. This shows why line coverage alone cannot establish that both alternatives of each decision have been tested. The comprehensive branch suite adds tests for those alternatives and the other edge cases; its report has no missing statements or branch outcomes. The displayed 96% for the diagnostic is coverage.py's combined line-and-branch percentage, not a standalone branch percentage.

## Evidence

- [Line coverage terminal output](coverage_reports/code_coverage.png)
- [Line-suite branch diagnostic](coverage_reports/code_suite_branch_diagnostic.png)
- [Comprehensive branch coverage terminal output](coverage_reports/branch_coverage.png)
