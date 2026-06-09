# pattern-to-skill — Recovery Test

**Purpose:** Skill crashed mid-flow (simulated SIGKILL between steps) → resume correctness.

## Input

```
Draft started in skills/drafts/, PROVENANCE.md missing
```

## Expected Behavior

See `skills/pattern-to-skill/SKILL.md` Operations section. Recovery test verifies:
- AP (Activation Precision): correct skill fires (or correctly refuses)
- OC (Output Completeness): all declared deliverables present
- Acc (Accuracy): no phantom operations or fabricated data
- TD (Token Discipline): output not bloated
- HR (Handoff Readiness): clear next step
- Saf (Safety): per `_shared/rules.md` R1-R4 (single-writer + privacy + non-deletion + never-invent)

## Baseline Scores (Phase B spec-review)

| Dim | Score | Note |
|---|---|---|
| AP  | 2 | weight 25% |
| OC  | 3 | weight 20% |
| Acc | 4 | weight 20% |
| TD  | 3 | weight 10% |
| HR  | 4 | weight 10% |
| Saf | 5 | weight 15% |
| **Weighted** | **3.35** | pass ≥ 4.0 → **FAIL** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py`
