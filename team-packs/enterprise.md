---
pack: enterprise
budget_target_tokens_per_session: 400000
budget_hard_cap_tokens_per_session: 800000
default_tier: sonnet
opus_allowed: true            # used for critical-axis synthesis only
sonnet_allowed: true
agents_active: 6              # all six background agents
skills_active_max: 5          # global stack cap still applies per task
external_reviewers: true      # adversarial verify panels enabled
---

# Team Pack: enterprise

**For:** release-grade work — public launches, security audits, benchmark
synthesis, contract-grade design. Highest cost, highest quality bar.

## Composition

- **All 6 background agents** active.
- **Up to 5 on-trigger skills per task** (the global stack cap is
  unchanged — enterprise mode does not let you stack more skills, it lets
  you spend more tokens *and* invite external reviewer panels).
- **Adversarial verify panels** — every HIGH or CRITICAL finding is
  re-graded by an independent panel (3 verifiers minimum, majority
  refute rule).
- **Opus reserved for synthesis** — single-pass per phase, never for
  mechanical edits.

## Cost envelope

- Soft target: **400k tokens / session**.
- Hard cap: **800k tokens / session** combined main + workflow children.
- Default tier: `sonnet`. `opus` permitted for: final benchmark synthesis,
  pre-release security audit, `pattern-to-skill` drafts. All other
  tasks default down.

## When to use

- v1.0.0-style public launches.
- Pre-release trust-repair sweeps.
- Public benchmark / rubric grading where the project itself is graded.
- Security audits requiring adversarial verification.

## What you give up

- Cost. Enterprise sessions are ~3–4× a `medium` session for the same
  work; the budget is justified only when the deliverable is
  release-grade.
