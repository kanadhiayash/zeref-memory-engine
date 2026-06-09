# INDEX (domain map)

Read after `memory/hot.md`. Find the relevant domain row, then read only the named section of the named page.

Per ZEREF_OS §0 — boundary file. Never load full pages unless the requested domain is found here.

## Format

| Domain | Page | Last Updated | Evidence | Summary |
|---|---|---|---|---|

## Domains

| Domain | Page | Last Updated | Evidence | Summary |
|---|---|---|---|---|
| zeref-meta | `memory/DECISIONS.md` | 2026-06-08 | high | v2.6.1 audit + hardening shipped (9.88/10 rubric). v2.6.0 4-gate chain shipped. v2.5 deep-audit retroactively logged. v4.3 wholesale nomenclature adoption. |
| architecture | `AGENTS.md` (root) | 2026-06-08 | high | Local-first context + memory engine + auto-gated execution. 14 Core Principles. 6 agents + 14 skills + 8 commands + 6 team packs + 3 Auto-Activation Gates + Model-Tier Routing matrix. |
| audit-v2.6.1 | `tests/claims-audit-v2.6.md`, `tests/scores-v2.6-B.csv`, `tests/security-audit-v2.6-C.md`, `tests/zeref-rubric-v2.6.md` | 2026-06-08 | high | 52 claims graded, 150 sandbox score rows, 8 attacks CVSS-scored (0 CRITICAL open), composite 9.88/10. |
| gates-v2.6 | `AGENTS.md` §Auto-Activation Gates, §Model-Tier Routing | 2026-06-08 | high | 3 sequential gates + per-skill model audit + cascade pattern. |
| model-resolver | `_shared/model-resolver.md` | 2026-06-08 | high | Bare alias → full Anthropic id mapping. Canonical full ids: claude-haiku-4-5 / claude-sonnet-4-6 / claude-opus-4-7. Pin overrides documented (Opus 4.6 vs 4.7 tokenizer). |
| privacy-templates | `PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md` (root) | 2026-05-31 | high | Root privacy templates per ZEREF_OS §4.1. Default mode `abstract`. Connectors OFF. |
| team-packs | `team-packs/{solo,build,research,red,audit,ship}.md` | 2026-05-31 | high | 6 on-demand packs per §8 + D10. Max 4 agents. Outputs land in `team/`. `/team [type]` activator. |
| connector-advisory | `references/connector-advisory.md` | 2026-05-31 | high | No bundled tools per D11. Free MCP stack (GitHub, Linear, Notion, DuckDuckGo) + workflow + power tiers. All OFF by default. |
| harness-map | `references/harness-translation-map.md` | 2026-05-31 | high | AGENTS.md is source of truth per D7. Per-harness stubs for Claude / Codex / Cursor / Gemini / Windsurf / Aider / Hermes / Amp / Zed / Perplexity. |
| v4x-canon | `references/v4x-canon/` | 2026-05-31 | high | Imported design corpus (read-only): ZEREF_OS, DECISION_LOG, MODEL_DEBATE, USE_CASES, RESEARCH_RESOURCES, PACKAGE_INDEX. |
| migration | `MIGRATION.md` (root), `scripts/migrate-v4.2-to-v4.3.py` | 2026-05-31 | high | v4.2 → v4.3 nomenclature migration. Idempotent. `git mv` preserves history. Pre-migration snapshot in `memory/snapshots/pre-v4.3-<iso>/`. |

---

## Standard pages (flat layout per §12)

- `memory/hot.md` — last 3 sessions, ≤500 words (read FIRST)
- `memory/DECISIONS.md` — confirmed decisions
- `memory/OPEN_QUESTIONS.md` — unresolved questions
- `memory/RISKS.md` — identified risks
- `memory/CONFLICTS.md` — contradiction queue
- `memory/MEMORY.md` — agent-written session notes
- `memory/archive/` — superseded entries (never deleted per D9)
- `memory/patterns/PATTERNS.jsonl` — append-only event log

## Reading rules (per ZEREF_OS §0)

1. Read `memory/hot.md` first.
2. If hot is insufficient, read this INDEX.
3. Find the relevant domain row.
4. Read only the named section of the named page.
5. Never load a full page just to scan it.
