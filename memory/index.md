# INDEX (domain map)

Read after `memory/hot.md`. Find the relevant domain row, then read only the named section of the named page.

Per ZEREF_OS §0 — boundary file. Never load full pages unless the requested domain is found here.

## Format

| Domain | Page | Last Updated | Evidence | Summary |
|---|---|---|---|---|

## Domains

| Domain | Page | Last Updated | Evidence | Summary |
|---|---|---|---|---|
| zeref-meta | `memory/DECISIONS.md` | 2026-05-31 | high | v4.3 shipped — wholesale nomenclature adoption, flat memory layout, team packs, harness translation map, Two-Strikes Rule. |
| architecture | `AGENTS.md` (root) | 2026-05-31 | high | Local-first context + memory engine. Harness-agnostic. Privacy-first. Boundary-first reads. Single-writer wiki. 6 agents + 10 skills + 8 commands + 6 team packs. |
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
