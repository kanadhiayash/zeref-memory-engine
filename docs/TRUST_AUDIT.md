# Trust Axis — Independent Re-grade

The `trust` axis is one of the internal quality axes in `benchmarks/`. It is a score this repository assigns itself against its own rubric, used as a release gate. **It is not a benchmark ranking and is not comparable to any other system's numbers.**

The deterministic scorer at `benchmarks/trust.py` produces a draft score. Per [`benchmarks/RUBRIC.md`](../benchmarks/RUBRIC.md), that draft must be re-graded by an independent skeptical reader before it may be published. This file records that re-grade.

## Why this file is load-bearing

`benchmarks/run-all.py` parses two fields below and will only lower a deterministic draft to a verified score when both are satisfied:

1. A **verified score** is present and is less than or equal to the deterministic draft. The override can lower a score, never raise one.
2. A **bound commit SHA** is present *and matches `HEAD`*.

If the bound SHA does not match `HEAD`, the override is refused, the deterministic draft publishes instead, and the report carries a note saying so. A re-grade cannot silently carry forward onto code it never examined — the binding expires the moment the tree moves.

This is the intended steady state, not a failure: on any commit after the graded one, the repository publishes its unoverridden deterministic score until someone re-runs the re-grade.

## Re-grade record

- **Rubric version:** 1
- **Bound-commit-SHA:** `33060a1`
- **Verified score (this audit):** **9.70**

The verified score applies only at the bound commit. At any other `HEAD`, the deterministic draft is what publishes.

## Sub-criterion breakdown

| Sub-criterion | Draft | Verified | Δ | Reason |
|---|---:|---:|---:|---|
| `version_consistency` | 10.0 | 10.0 | 0.0 | A single version source is enforced across live surfaces and machine-checked. |
| `test_suite` | 10.0 | 10.0 | 0.0 | Suite passes; the coverage floor published is the honestly measured one rather than an aspirational target. |
| `privacy_patterns` | 10.0 | 10.0 | 0.0 | Provider credential patterns plus built-in classes; normalization-bypass resistance is covered by tests. |
| `security_md` | 10.0 | 9.5 | -0.5 | Required reporting items are present; one contact detail remains unpublished. |
| `ci_hardening` | 10.0 | 9.0 | -1.0 | Actions are pinned to commit SHAs. Deduction for absence of a defence-in-depth workflow lint step. |

Verified axis score = (10 + 10 + 10 + 9.5 + 9) / 5 = **9.70**.

## Deductions carried forward

Each deduction above is non-blocking and tracked as an issue rather than being written off.

1. **Unpublished security contact detail.** The primary private reporting channel works without it; publishing it closes the gap.
2. **No workflow lint step.** A lint pass would catch malformed action references and missing permission scopes before they merge.
3. **Coverage gate sits at the measured floor.** Subprocess-style CLI tests undercount in-process coverage, so the published gate reflects what is actually measured rather than what the suite morally covers. Raising it requires instrumenting those paths, not adjusting the number.
4. **Normalization coverage is partial.** The scripts folded to ASCII cover the common look-alike cases; broader coverage would harden it further.

## Blocking findings

None.

## How to re-run

```bash
python3 benchmarks/run-all.py        # regenerate the deterministic draft
python3 -m pytest -q
```

To rebind the re-grade after a code change: re-perform the independent review, then update **both** the verified score and the bound commit SHA above to the commit reviewed. Updating the SHA without redoing the review defeats the entire mechanism — the binding is the only thing standing between a stale grade and a false claim.

## Related

- [`benchmarks/RUBRIC.md`](../benchmarks/RUBRIC.md) — axis definitions and re-grade requirement
- [`docs/RELEASE_GATES.md`](RELEASE_GATES.md) — where this axis is consumed
- [`docs/PUBLIC_SAFE_COPY.md`](PUBLIC_SAFE_COPY.md) — rules on what may be claimed publicly
