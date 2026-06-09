# parent-sync — Drift Test

**Purpose:** Same input × 5 runs → measure pass^5 stability.

## Input

```
Same /sync-parent × 5 → no duplicate pushes
```

## Expected Behavior

See `skills/parent-sync/SKILL.md` Operations section. Drift test verifies:
- AP (Activation Precision): correct skill fires (or correctly refuses)
- OC (Output Completeness): all declared deliverables present
- Acc (Accuracy): no phantom operations or fabricated data
- TD (Token Discipline): output not bloated
- HR (Handoff Readiness): clear next step
- Saf (Safety): per `_shared/rules.md` R1-R4 (single-writer + privacy + non-deletion + never-invent)

## Baseline Scores (Phase B spec-review)

| Dim | Score | Note |
|---|---|---|
| AP  | 3 | weight 25% |
| OC  | 4 | weight 20% |
| Acc | 4 | weight 20% |
| TD  | 3 | weight 10% |
| HR  | 4 | weight 10% |
| Saf | 5 | weight 15% |
| **Weighted** | **3.8** | pass ≥ 4.0 → **FAIL** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py`
