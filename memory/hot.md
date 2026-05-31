# memory/hot.md

> Last 3 sessions, current context. Cap ≤500 words. Read FIRST per ZEREF_OS §0.

## Session 2026-05-31 — v4.3 upgrade (M4)

Shipped v4.3.0 — v4.x canon import + nomenclature alignment + team packs. Aligned repo with canonical v4.x spec per `references/v4x-canon/ZEREF_OS.md` §0–§13.

**What changed:**
- **Memory layout flattened**: `memory/wiki/{INDEX,DECISIONS,OPEN_QUESTIONS,RISKS,CONFLICTS}.md` → flat `memory/`. `memory/wiki/ARCHIVE/` → `memory/archive/`. `memory/logs/session-events.jsonl` archived; new `memory/patterns/PATTERNS.jsonl` as append target.
- **Root privacy templates**: `PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md` per §4.1. Default mode `abstract`; connectors OFF.
- **Team packs (6)**: `team-packs/{solo,build,research,red,audit,ship}.md` + `/team` command per §8.
- **Harness stubs**: `.cursor/rules/zeref.mdc`, `.windsurfrules`, `.aider.conf.yml.example` per §10.
- **References codified**: `two-strikes-rule.md`, `connector-advisory.md`, `harness-translation-map.md`. v4x canon imported read-only to `references/v4x-canon/`.
- **Migration script**: `scripts/migrate-v4.2-to-v4.3.py` — idempotent, `git mv`, pre-migration snapshot.
- **Bumped to v4.3.0** in `.claude-plugin/plugin.json` + `SKILL.md`.

**Reading order now (§0):** hot.md → index.md → PRIVACY.md → REDACT.md → MEMORY.md (200 lines) → tail PATTERNS.jsonl.

**Validation**: `python3 scripts/zeref-validate-v4.py` passes — 10 skills, 6 agents, 8 commands, 6 team packs, 3 root privacy templates, 6 v4x canon docs, 3 harness stubs.

**Counts touched**: ~30 created, ~25 updated, 8 moved (git mv), 2 archived, 0 deleted.

**Open**: `ruvector.db` (1.5 MB tracked binary) status — verify intentional / surface separately. Not addressed in this upgrade per user directive.

## Session 2026-05-30 — v4.2 ship (M3)

Shipped pattern-observer + pattern-to-skill production impl. Closed v4 roadmap (M1/M2/M3). Tag `v4.2.0`. See `memory/DECISIONS.md`.

## Session 2026-05-30 — v4.1 ship (M2)

Shipped contradiction-resolution + parent-sync production impl. Snooze-until-/done. Provenance preserved on parent push. Tag `v4.1.0`.

---

*Carry-forward open: confirm ruvector.db tracking decision; smoke-test Cursor/Windsurf/Aider after first user install.*
