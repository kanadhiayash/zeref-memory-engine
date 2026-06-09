# caveman-handoff — Edge Test

**Purpose:** Boundary input: empty / max payload / unicode-heavy. Confirms degraded but safe behavior.

## Input

```
Handoff package already terse: 350 tokens, no prose
```

## Expected Behavior

Compression <20% (limit). Emit verbose payload + note 'already terse'. No abort.

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
| TD  | 5 | weight 10% |
| HR  | 4 | weight 10% |
| Saf | 4 | weight 15% |
| **Weighted** | **4.10** | pass ≥ 4.0 → **PASS** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py` extension (or v2.7)
