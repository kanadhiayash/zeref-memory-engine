---
pack: medium
budget_target_tokens_per_session: 100000
budget_hard_cap_tokens_per_session: 200000
default_tier: sonnet
opus_allowed: limited         # only for CRITICAL-weight tasks
sonnet_allowed: true
agents_active: 4              # memory-keeper, privacy-guardian, evidence-curator, sync-coordinator
skills_active_max: 5
---

# Team Pack: medium

**For:** typical project work — feature builds, multi-file refactors,
research syntheses, design reviews. Balanced cost and quality.

## Composition

- **4 background agents:** `memory-keeper`, `privacy-guardian`,
  `evidence-curator`, `sync-coordinator`.
- **Up to 5 on-trigger skills** (the global stack cap).

## Cost envelope

- Soft target: **100k tokens / session**.
- Hard cap: **200k tokens / session**.
- Default tier: `sonnet`. `opus` is allowed *only* when a CRITICAL-weight
  task self-reports `sonnet` as insufficient, and after the dual-key
  override.

## When to use

- Default for any non-trivial development session.
- Cross-file refactors, schema changes, multi-step feature work.
- Research syntheses that touch more than one source.

## When to upgrade to `enterprise`

- Pre-release security audit.
- Public-facing API or contract design.
- Multi-stakeholder review where each axis needs an independent agent.
- Benchmark synthesis that grades the project against external rubrics.
