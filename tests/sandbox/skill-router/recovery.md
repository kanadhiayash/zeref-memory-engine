# skill-router — Recovery Test

**Purpose:** Skill crashed or interrupted mid-flow. Resume correctness checked.

## Input

```
Mid-routing: skill-router has selected 3-skill stack, then fleet-activator reports ECC unreachable
```

## Expected Behavior

Substitute emulator (agent-skills:*) + reissue [skill-router] declaration with ext=ECC→fallback:agent-skills. Log mid-flight reroute event.

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
| TD  | 3 | weight 10% |
| HR  | 4 | weight 10% |
| Saf | 4 | weight 15% |
| **Weighted** | **3.90** | pass ≥ 4.0 → **FAIL** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py` extension (or v2.7)
