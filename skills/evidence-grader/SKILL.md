---
name: evidence-grader
description: Skill counterpart to evidence-curator agent. Provides on-demand grading for ad-hoc claims, source assessments, and review passes.
trigger:
  - user says "grade this claim"
  - wiki-maintenance consolidation
  - parent-sync filter step
model: claude-haiku-4-5
max_turns: 10
---

# evidence-grader

## Mission

Assess confidence + recency + provenance of a claim or wiki entry. Returns a grade with reasoning.

## Grades

| Grade | Criteria |
|---|---|
| **high** | Verified this session OR confirmed by user OR backed by primary source |
| **medium** | Reasonable inference OR named source < 30d OR indirect but corroborated |
| **low** | Unverified assumption OR > 90d OR derived from a single weak source |

## Operations

### GRADE_CLAIM (on demand)
1. Receive claim + optional source
2. Apply criteria
3. Return: `{grade, confidence_reasoning, recency_reasoning, provenance_reasoning, suggested_action}`

### REVIEW_PAGE (called by wiki-maintenance)
1. Walk every entry on a wiki page
2. Re-grade each
3. Report demotions, suggest re-verifications

### FILTER_SYNC (called by parent-sync)
1. Receive list of entries staged for outbound
2. Return only entries with grade ≥ medium

## Safety

- Grade is advisory only; user remains the arbiter
- Always include reasoning, never just a grade letter
