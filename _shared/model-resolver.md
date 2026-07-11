<!-- privacy-audit: allow-file "Model-id mapping spec. Documents Anthropic model IDs + API paths as canonical routing, not user data." -->

# Model Resolver

Canonical mapping between bare tier names (legacy / human-friendly) and full Anthropic model IDs (API-callable + version-explicit). Per `_shared/rules.md#R6` + AGENTS.md `## Model-Tier Routing`.

## Canonical table (full IDs are the source of truth)

| Bare alias | Full model ID (API) | Tier | $/1M in | $/1M out | Tokenizer note | Target profile |
|---|---|---|---|---|---|---|
| `haiku`  | `claude-haiku-4-5`  | HAIKU  | $1 | $5  | baseline | (Tier-2) |
| `sonnet` | `claude-sonnet-4-6` | SONNET | $3 | $15 | baseline | (Tier-2) |
| `opus`   | `claude-opus-4-7`   | OPUS   | $5 | $25 | **+35% vs Sonnet** for same English text (Anthropic 2026); pin `claude-opus-4-6` for cost-sensitive flagship work | (Tier-2) |
| `opus48` | `claude-opus-4-8`   | OPUS   | $5 | $25 | current flagship; largest system prompt (~45k tokens with tools) | [`claude-opus-4-8`](../references/target-model-profiles/claude-opus-4-8.md) |
| `gpt55-instant` | `gpt-5-5-instant` | INSTANT | $0.4 | $2 | small system prompt (~3.8k); markdown-verbose default | [`gpt-5-5-instant`](../references/target-model-profiles/gpt-5-5-instant.md) |

## Pin overrides (version-explicit)

When stability matters more than getting the latest tier:

| Use case | Pinned model | Reason |
|---|---|---|
| Cost-sensitive Opus work | `claude-opus-4-6` | Avoids +35% tokenizer inflation of 4.7 |
| Long-context Sonnet | `claude-sonnet-4-6` | Current default; revisit when 4.7 lands |
| Background batch | `claude-haiku-4-5` + Batch API (0.5x) | Cheapest path for log-summarization, pattern-scan, validator-lint |

## How to use

**In `zeref-registry.json`**: write the full ID in the `model` field. Optionally include `model_alias` for legacy back-compat.

```json
{
  "skill": "skill-router",
  "model": "claude-haiku-4-5",
  "model_alias": "haiku"
}
```

**In `skills/<name>/SKILL.md` frontmatter**: full ID is canonical.

```yaml
model: claude-haiku-4-5
```

**Bare aliases remain accepted at the SKILL.md level** for skills written prior to v2.6.1. They resolve via this table at registry-load time. New SKILL.md should use full IDs.

## Resolver function (Python contract — referenced by `zeref/cli.py`)

```python
RESOLVER = {
    "haiku":  "claude-haiku-4-5",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-7",
}

def resolve_model(name: str) -> str:
    """Bare alias OR full ID → full ID. Unknown name returns input unchanged + emits warning."""
    if name in RESOLVER:
        return RESOLVER[name]
    if name.startswith("claude-"):
        return name  # already full ID
    # unknown — pass through with warning event
    return name
```

## Update policy

- New Anthropic release → add new row + tokenizer/pricing note.
- Deprecation → mark row `[DEPRECATED yyyy-mm-dd]`; keep for back-compat one major version.
- Pricing change → update row; log to `memory/DECISIONS.md` with provenance + effective date.

## Applied to (R6 chain)

- `skills/budget-governor/SKILL.md` — tier table cites these IDs
- `skills/skill-router/SKILL.md` — model field `claude-haiku-4-5`
- `skills/fleet-activator/SKILL.md` — model field `claude-haiku-4-5`
- `skills/prompt-context-engine/SKILL.md` — frontmatter `model: sonnet` → resolved at load to `claude-sonnet-4-6`
- `skills/caveman-handoff/SKILL.md` — model field `claude-haiku-4-5`
- `zeref-registry.json` — all 14 entries normalized to full Anthropic ids
- `AGENTS.md` `## Model-Tier Routing` — Tier table column "Model" cites full IDs
