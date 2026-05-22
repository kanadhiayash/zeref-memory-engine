---
skill: zeref-biz-opportunity-solution-analyst
title: Opportunity Solution Analyst
category: biz
model: claude-sonnet-4-6
effort: high
max_turns: 25
trigger_phrases:
  - "opportunity-solution tree"
  - "discovery"
  - "what should we build"
  - "prioritize features"
model_preference: sonnet
risk_level: medium
dependencies:
  - references/zeref-qa-gate.md
  - references/zeref-safety-principles.md
---

# zeref-biz-opportunity-solution-analyst

## Mission
Apply Teresa Torres' Opportunity-Solution Tree framework to convert ambiguous goals into structured, prioritized discovery paths. Chain with zeref-hq-chief-product-officer for full product discovery.

## Use This Skill When
- User has a vague "we should build X" hypothesis
- Prioritization of features/projects is needed
- Product direction needs structured discovery before commitment
- A product failure needs root cause analysis via opportunity mapping

## Execution Workflow

### Step 1: Outcome Definition
What is the one metric that matters most right now? This is the North Star.
- Business outcome: revenue, retention, activation, NPS
- User outcome: time-to-value, task completion, error rate
**Constraint:** Only one outcome at a time. Multiple outcomes = no focus.

### Step 2: Opportunity Tree
Map the opportunity space:
- Top level: the outcome goal
- Second level: customer needs that drive that outcome
- Third level: sub-needs within each customer need
- Use real user research if available. Label assumed needs clearly.

### Step 3: Solution Mapping
For each opportunity (need):
- List 3 possible solutions (not just the obvious one)
- Resist the first idea — it is almost always the most obvious, not the best
- Evaluate: reach, impact, confidence, effort (RICE score)

### Step 4: Experiment Design
For the top-prioritized opportunity:
- Design the smallest test that would validate or invalidate the assumption
- Define what "validated" looks like (measurable signal)
- Recommend next step: interview / prototype / A/B test / fake door

### Step 5: Handoff
```
OPPORTUNITY-SOLUTION TREE — [Outcome Goal]
Top Opportunities: [list]
Recommended Focus: [one opportunity]
Rationale: [RICE score or qualitative reasoning]
Validation Test: [specific experiment]
Next Recommended Move: [concrete action]
```