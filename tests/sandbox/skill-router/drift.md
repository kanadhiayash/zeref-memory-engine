# skill-router — Drift Test

**Purpose:** Same input × 5 runs. Pass^5 measures determinism.

## Input

```
Same input 'update wiki' x5 runs
```

## Expected Behavior

All 5 runs produce identical stack: lead=wiki-maintenance, support=[memory-keeper, evidence-grader], qa=privacy-guardian. Deterministic given matrix.

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
| AP  | 5 | weight 25% |
| OC  | 5 | weight 20% |
| Acc | 5 | weight 20% |
| TD  | 5 | weight 10% |
| HR  | 4 | weight 10% |
| Saf | 5 | weight 15% |
| **Weighted** | **4.90** | pass ≥ 4.0 → **PASS** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py` extension (or v2.7)
