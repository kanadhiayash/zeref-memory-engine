# fleet-activator — Recovery Test

**Purpose:** Skill crashed or interrupted mid-flow. Resume correctness checked.

## Input

```
Probe ECC; filesystem returns I/O error mid-test
```

## Expected Behavior

Report PARTIAL — manual verification needed. Do not fail the chain; downstream can decide to emulate or wait.

Verifies 6 rubric dims:
- AP (Activation Precision): correct skill fires (or correctly refuses)
- OC (Output Completeness): all declared deliverables present
- Acc (Accuracy): no phantom operations or fabricated data
- TD (Token Discipline): output not bloated
- HR (Handoff Readiness): clear next step
- Saf (Safety): per `_shared/rules.md` R1-R6

## Baseline Scores (Phase B spec-review)

| Dim | Score | Note |
|---|---|---|
| AP  | 4 | weight 25% |
| OC  | 4 | weight 20% |
| Acc | 4 | weight 20% |
| TD  | 4 | weight 10% |
| HR  | 4 | weight 10% |
| Saf | 4 | weight 15% |
| **Weighted** | **4.00** | pass ≥ 4.0 → **PASS** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py` extension (or v2.7)
