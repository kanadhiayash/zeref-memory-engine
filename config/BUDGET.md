---
model_tier: sonnet              # haiku | sonnet | opus
always_on_target_tokens: 2000   # context loaded on every /start
warn_at_tokens: 50000           # surface warning when session approaches
hard_cap_tokens: 180000         # block writes / require summarization above this
verbosity:
  haiku: terse
  sonnet: balanced
  opus: detailed
boundary_first: true            # always read INDEX before full pages
---

# Token Budget

The `budget-governor` skill scales output verbosity and read patterns to the active model tier and remaining budget.

## Targets

- **Always-on context** (loaded by AGENTS.md first-action sequence): ≤ 2000 tokens
- **Per-skill invocation**: ≤ 8000 tokens unless the skill's SKILL.md declares otherwise
- **Boundary-first reads**: always read `memory/wiki/INDEX.md` before any full page

## When budget warns

- Surface remaining tokens
- Offer to consolidate via `wiki-maintenance`
- Offer to snapshot + archive via `memory-keeper`

## When budget hits hard cap

- Block new writes
- Force summarization or `/done` before continuing
