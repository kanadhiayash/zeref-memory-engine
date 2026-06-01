---
model_tier: auto                # auto | free | standard | god-mode (auto detects from active model)
always_on_target_tokens: 2000   # context loaded on every /start
warn_at_tokens: 50000           # surface warning when session approaches
hard_cap_tokens: 180000         # block writes / require summarization above this
verbosity:
  free: terse
  standard: balanced
  god-mode: detailed
boundary_first: true            # always read hot.md → index.md before full pages
pattern_detection: true         # set false to disable pattern-observer
---

# Token Budget

The `budget-governor` skill scales output verbosity and read patterns to the active model tier and remaining budget. God Mode activates automatically when a high-tier model is detected (per ZEREF_OS §5 + D5).

## Tier table

| Tier | Model target | Zeref OS behavior | Per-skill cap |
|---|---|---|---|
| **Free** | Gemini Flash, local Ollama, Mistral | Aggressive compaction, minimal wiki writes, short `/status` outputs | 4 000 tok |
| **Standard** | GPT-4o mini, Claude Haiku, Gemini Flash 3.5 | Normal operation, full wiki writes, standard conflict scans | 8 000 tok |
| **God Mode** | GPT-4o, Claude Opus / Sonnet, Gemini 3.5 Pro | Full parent-child sync, deep conflict analysis, pattern retrospectives | 16 000 tok |

## Auto-detection

| Detected model substring | Mapped tier |
|---|---|
| `claude-opus-*`, `claude-sonnet-*`, `gpt-4o`, `gemini-3.5-pro` | God Mode |
| `gpt-4o-mini`, `claude-haiku-*`, `gemini-flash-3.5` | Standard |
| `gemini-flash`, `mistral-*`, `ollama/*` | Free |
| unknown | Standard (safe default) |

Override above by setting `model_tier:` to `free` / `standard` / `god-mode`.

## Targets

- **Always-on context** (loaded by AGENTS.md first-action sequence): ≤ 2000 tokens
- **Per-skill invocation**: cap per tier table above; SKILL.md may override
- **Boundary-first reads**: always read `memory/hot.md` then `memory/index.md` before any full page

## When budget warns

- Surface remaining tokens
- Offer to consolidate via `wiki-maintenance`
- Offer to snapshot + archive via `memory-keeper`

## When budget hits hard cap

- Block new writes
- Force summarization or `/done` before continuing

## No hardcoded limits

User sets the ceiling above. Zeref OS warns before approaching it. Free to install; capability scales with the user's own model tier.
