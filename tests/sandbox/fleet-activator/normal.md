# fleet-activator — Normal Test

**Purpose:** Expected trigger phrase → expected output. Baseline pass criterion.

## Input

```
skill-router invokes with tool list ['ECC', 'Graphify']
```

## Expected Behavior

Probe both via Bash test -d / test -f. Emit [fleet-activator] ECC: reachable (path=~/Documents/Claude/11_MY-STACK/ECC-main/), Graphify: reachable (path=~/.claude/skills/graphify/SKILL.md). Log 2 tool-probe events.

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
| TD  | 4 | weight 10% |
| HR  | 4 | weight 10% |
| Saf | 5 | weight 15% |
| **Weighted** | **4.80** | pass ≥ 4.0 → **PASS** |

## Run Status

- **Spec review:** complete (this doc)
- **Live LLM run:** pending Phase D L3 `tests/runner.py` extension (or v2.7)
