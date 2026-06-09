# prompt-context-engine — Edge Test

**Purpose:** Boundary input: empty / max payload / unicode-heavy. Confirms degraded but safe behavior.

## Input

```
User: prompt that is exactly 1 word: 'help'
```

## Expected Behavior

Classification=UNSTRUCTURED (no deliverable). Brief generated with all 5 tags; <objective> marked TODO (R4). 30s wait then auto-approve.

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
