# prompt-context-engine — Recovery Test

**Purpose:** Skill crashed or interrupted mid-flow. Resume correctness checked.

## Input

```
Brief shown, user replies after 35s with correction
```

## Expected Behavior

Auto-approve fired at 30s; correction arrives 5s late. Behavior: accept correction, regenerate brief, re-display. Risk: race condition if work already started.

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
| AP  | 3 | weight 25% |
| OC  | 3 | weight 20% |
| Acc | 3 | weight 20% |
| TD  | 3 | weight 10% |
| HR  | 3 | weight 10% |
| Saf | 3 | weight 15% |
| **Weighted** | **3.00** | pass ≥ 4.0 → **FAIL** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py` extension (or v2.7)
