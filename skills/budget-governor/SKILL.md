---
name: budget-governor
description: Scales output verbosity and read patterns to active model tier (Free / Standard / God Mode per ZEREF_OS §5) and remaining token budget. Activates on /start, tier change, and budget warning. God Mode auto-detected from model.
trigger:
  - /start
  - config/BUDGET.md changes
  - session approaches warn_at_tokens
model: claude-haiku-4-5
max_turns: 10
---

# budget-governor

## Mission

Keep token cost in line with the active model tier. Surface budget pressure early. God Mode unlocks when a high-tier model is detected (no separate gate per D5).

## Tier table (per ZEREF_OS §5)

| Tier | Model target | Zeref OS behavior | Per-skill cap |
|---|---|---|---|
| **Free** | Gemini Flash, local Ollama, Mistral | Aggressive compaction, minimal wiki writes, short `/status` outputs | 4 000 tok |
| **Standard** | GPT-4o mini, Claude Haiku, Gemini Flash 3.5 | Normal operation, full wiki writes, standard conflict scans | 8 000 tok |
| **God Mode** | GPT-4o, Claude Opus / Sonnet, Gemini 3.5 Pro | Full parent-child sync, deep conflict analysis, pattern retrospectives | 16 000 tok |

God Mode activates **automatically** when a high-tier model is detected. No hardcoded limits. User sets the ceiling in `config/BUDGET.md`. Zeref OS warns before approaching it.

## Operations

### ON /start
1. Read `config/BUDGET.md`
2. Detect active model from harness env; resolve to Free / Standard / God Mode
3. Report active tier + always-on context size
4. Warn if always-on > target (default 2000 tok)

### MID-SESSION
1. Track cumulative tokens via session events
2. At `warn_at_tokens`: surface to user, offer consolidation via `wiki-maintenance`
3. At `hard_cap_tokens`: block writes, force `/done` or summarization

### TIER CHANGE
1. Reload verbosity rules
2. Suggest re-reading `memory/index.md` with new boundary policy
3. Log tier change as event in `memory/patterns/PATTERNS.jsonl`

## Auto-detection rules

| Detected model | Mapped tier |
|---|---|
| `claude-opus-*`, `claude-sonnet-*`, `gpt-4o`, `gemini-3.5-pro` | God Mode |
| `gpt-4o-mini`, `claude-haiku-*`, `gemini-flash-3.5` | Standard |
| `gemini-flash` (older), `mistral-*`, `ollama/*` | Free |
| unknown | Standard (safe default) |

User can override in `config/BUDGET.md` `model_tier:` frontmatter field.

## Safety

- Never silently truncate user content
- Always offer consolidation rather than auto-delete
- Per D9: archive consolidated content, never delete
