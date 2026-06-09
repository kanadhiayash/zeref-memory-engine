# Model Debates

Zeref OS is model-agnostic by design. Different model families need slightly different handling. v2.6 added explicit Model-Tier Routing per Core Principle 14; v2.6.1 added the canonical model resolver.

## v2.6 model tiers + canonical IDs

| Tier | Full Anthropic ID | Bare alias | $/1M in | $/1M out | Pin override |
|---|---|---|---|---|---|
| **HAIKU** | `claude-haiku-4-5` | `haiku` | $1 | $5 | — |
| **SONNET** | `claude-sonnet-4-6` | `sonnet` | $3 | $15 | — |
| **OPUS** | `claude-opus-4-7` | `opus` | $5 | $25 | `claude-opus-4-6` (cost-sensitive flagship; avoids 4.7 +35% tokenizer) |

Non-Anthropic equivalents (mapped at runtime):

| Detected model | Mapped tier | Legacy alias |
|---|---|---|
| `gpt-4o`, `gemini-3.5-pro` | OPUS-equivalent | God Mode |
| `gpt-4o-mini`, `gemini-flash-3.5` | SONNET-equivalent | Standard |
| `mistral-*`, `ollama/*`, `gemini-flash` (older) | HAIKU-equivalent | Free |
| unknown | SONNET (safe default) | Standard |

Full table + pin policy: [`_shared/model-resolver.md`](https://github.com/kanadhiayash/zeref-os/blob/main/_shared/model-resolver.md).

## Per-model needs (what each family wants for context engineering)

### Claude (Sonnet 4.6 / Opus 4.7 / Haiku 4.5)

- **Strength**: long context, XML tags, plan-mode, instruction following
- **Sensitivity**: prompt-injection if `<context>` tags aren't sanitized (v2.6.1 L10 closes this)
- **Best for**: Gate #3 prompt-context-engine (Sonnet medium); pattern-to-skill draft synthesis (Opus high); validator + gate ops (Haiku low)
- **Honors**: AGENTS.md as canonical; `<override-acknowledged>` blocks (v2.6.1 L13)

### GPT-4o / 4o-mini

- **Strength**: tool use, structured output
- **Sensitivity**: tighter context window than Claude; prefers explicit step lists
- **Best for**: SONNET-equivalent workloads; cost-balanced executor
- **Note**: not yet validated cross-harness (ZRF-B07 deferred to v2.7)

### Gemini (Flash + Pro)

- **Strength**: cost (Flash is cheapest); multimodal
- **Sensitivity**: prefers system-prompt at top, not interleaved
- **Best for**: HAIKU-equivalent batch workloads (Flash); OPUS-equivalent reasoning (Pro)
- **Harness**: GEMINI.md stub defers to AGENTS.md

### Open-source (Mistral / Llama / Ollama)

- **Strength**: local execution (privacy + zero cost)
- **Sensitivity**: smaller context window; weaker instruction following at smaller sizes
- **Best for**: HAIKU-equivalent workloads on `local-only` privacy mode
- **Tradeoff**: accept lower output quality; pair with deterministic validators (`scripts/zeref-validate.py` + `lint_patterns_log`)

## Cascade pattern (v2.6 Core Principle 14)

```
orchestrator @ Sonnet medium     ← plans + decomposes
    ↓
executor @ Sonnet|Haiku by weight ← does the work per sub-task
    ↓
final gate @ Opus high            ← only when stakes warrant (irreversible writes, security)
```

Default orchestrator is Sonnet — cost-balanced. Escalate to Opus only when:
- Irreversible writes (parent-sync export, memory-import-export)
- Architecture decisions (ADR-worthy)
- Security-sensitive payloads (privacy abstraction edge cases)

## Hard constraints (Core Principle 14)

- **LOW never on Opus** — flagged by `budget-governor` Step 4. Propose Haiku downgrade.
- **CRITICAL never on Haiku** — hard block. v2.6.1 L13 dual-key override required.
- **HIGH on Haiku** — warn, allow with user confirm.
- **MEDIUM on Opus** — warn, allow. `pattern-observer` logs for retrospective tuning.

## Per-skill model audit (v2.6.1)

All 14 skills audited; no LOW→opus or CRITICAL→haiku mismatches.

| Skill | Weight | Model | Note |
|---|---|---|---|
| `wiki-maintenance` | MEDIUM | `claude-haiku-4-5` | mechanical consolidation |
| `budget-governor` | LOW | `claude-haiku-4-5` | classification only |
| `project-setup` | HIGH | `claude-sonnet-4-6` | interview |
| `contradiction-resolution` | HIGH | `claude-sonnet-4-6` | arbitration |
| `evidence-grader` | LOW-MEDIUM | `claude-haiku-4-5` | grade |
| `handoff-compiler` | HIGH | `claude-sonnet-4-6` | cross-harness package |
| `memory-import-export` | HIGH | `claude-sonnet-4-6` | schema crossing |
| `parent-sync` | HIGH | `claude-sonnet-4-6` | irreversible push |
| `pattern-to-skill` | **CRITICAL** | **`claude-opus-4-7`** | code synthesis |
| `privacy-abstraction` | MEDIUM | `claude-haiku-4-5` | deterministic REDACT rules |
| `skill-router` | LOW | `claude-haiku-4-5` | routing |
| `fleet-activator` | LOW | `claude-haiku-4-5` | probe |
| `prompt-context-engine` | HIGH | `claude-sonnet-4-6` | restructure |
| `caveman-handoff` | LOW | `claude-haiku-4-5` | mechanical compression |

**Borderline**: `privacy-abstraction` (`risk_level: high`, `model: haiku`) kept on Haiku because redaction follows deterministic REDACT.md rules. Tracked as forward signal for `pattern-observer` — if PATTERNS.jsonl shows redaction misses on adversarial input, bump to Sonnet.

## What Zeref OS does NOT debate

- **Best model overall**: no answer. Use the tier the task weight demands.
- **Best model for code**: depends on code complexity. CRITICAL refactor → Opus. Single-file edit → Haiku.
- **Vendor lock-in**: zero. Bring any model; harness translation map handles the rest.

## Future (deferred to v2.7)

- Cross-harness live runs (ZRF-B07): validate same AGENTS.md spec works identically in Cursor / Aider / Gemini
- Cascade-replay test: end-to-end orchestrator→executor→final-gate live measurement (path to 10.00/10 Execution)
- Model-specific prompt-context-engine tuning (Sonnet-optimized brief format vs GPT-optimized vs Gemini-optimized)

## Related

- [[Architecture]] §Model-Tier Routing
- [`_shared/model-resolver.md`](https://github.com/kanadhiayash/zeref-os/blob/main/_shared/model-resolver.md) — canonical mapping + pin policy
- [`skills/budget-governor/SKILL.md`](https://github.com/kanadhiayash/zeref-os/blob/main/skills/budget-governor/SKILL.md) — Cost Weight Classification + Auto-Activation Rule
- [`AGENTS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/AGENTS.md) §Core Principle 14 + §Model-Tier Routing
- [`docs/adr/zeref_auto-gated-execution_adr_approved_yk_2026-06-08_v1.0.md`](https://github.com/kanadhiayash/zeref-os/blob/main/docs/adr/zeref_auto-gated-execution_adr_approved_yk_2026-06-08_v1.0.md) — ADR-001
