# Benchmark Failure Analysis

## trust

- Expected: axis score >= 9.0
- Actual: axis score 8.8
- Likely cause: One or more benchmark sub-criteria are below the deterministic pass bar.
- Needed fix: Inspect the trust sub-criteria and implement the missing local behavior.
- Regression-test suggestion: Add or update a regression test for benchmarks.trust.
