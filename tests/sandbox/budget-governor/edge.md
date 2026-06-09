# budget-governor — Edge Test

**Purpose:** Boundary input: empty / max payload / unicode-heavy. Confirms degraded but safe behavior.

## Input

```
Single-fact lookup on Opus 4.7
```

## Expected Behavior

Weight=LOW. Tier=OPUS. Match=MISMATCH (LOW on Opus). Propose Haiku downgrade. Block until user confirms or downgrades. [budget-governor] weight=LOW tier=OPUS match=MISMATCH.

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
