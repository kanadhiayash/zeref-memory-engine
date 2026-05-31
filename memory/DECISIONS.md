# DECISIONS

Confirmed decisions for this project. Append-only at top. Single writer: `memory-keeper`.

## Format

```
### YYYY-MM-DD — [Decision title]
**Decided**: [what was decided]
**Why**: [reasoning]
**Evidence**: high | medium | low
**Provenance**: [source — session ts, event hash, person]
**Supersedes**: [previous decision id, if any]
```

---

### 2026-05-31 — Ship v4.3.0 — v4.x canon import + nomenclature alignment + team packs (M4)
**Decided**: Adopted package nomenclature wholesale per user instruction. Flat `memory/` layout (no more `memory/wiki/`). Root privacy templates (`PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md`) per ZEREF_OS §4.1. Default privacy mode `abstract`. All connectors OFF by default. Renamed `memory/logs/session-events.jsonl` → `memory/patterns/PATTERNS.jsonl` (archived predecessor preserved). Renamed `skills/_drafts/` convention → `skills/drafts/`. Added 6 team packs (`team-packs/{solo,build,research,red,audit,ship}.md`) + `/team` command per §8. Added harness stubs `.cursor/rules/zeref.mdc`, `.windsurfrules`, `.aider.conf.yml.example` per §10. Codified Two-Strikes Rule, Connector Advisory, Harness Translation Map in `references/`. Imported v4.x design canon to `references/v4x-canon/`. Created idempotent migration script `scripts/migrate-v4.2-to-v4.3.py` with pre-migration snapshot + `git mv` for history preservation. Bumped to v4.3.0.
**Why**: Aligns repo with canonical v4.x specification while preserving all existing v4.2 functionality. Wholesale nomenclature adoption surfaces design intent directly (reading order, privacy model, team packs) instead of forcing readers to map between two conventions. Migration script ensures user repos can move without manual work; pre-migration snapshot guarantees rollback. All changes additive at the capability level; only paths and reading order changed. Maps to decisions D7 (harness agnosticism), D8 (privacy model), D9 (archive policy), D10 (team packs), D11 (connector advisory) in `references/v4x-canon/DECISION_LOG.md`.
**Evidence**: high
**Provenance**: session 2026-05-31, plan `you-are-being-handed-glowing-lynx.md`, validator passes (10 skills, 6 agents, 8 commands, 6 team packs, 3 root privacy, 6 v4x canon, 3 harness stubs)
**Supersedes**: v4.2.0 nested `memory/wiki/` layout; `config/PRIVACY.md` (archived at `memory/archive/config-PRIVACY-v4.2.md`)

### 2026-05-30 — Ship v4.2.0 — pattern-observer + pattern-to-skill (M3)
**Decided**: Promoted final 2 stubs to production. pattern-observer scans session-events.jsonl over 72h rolling window using Jaccard 3-gram similarity ≥0.8 with union-find clustering. pattern-to-skill drafts SKILL.md files to skills/_drafts/ with immutable PROVENANCE.md, requires explicit user review via /review-skill (approve/edit/reject/defer). v4 roadmap declared complete — no stubs remain.
**Why**: Closes the self-extension loop. Repeated work becomes reusable skills, review-first to prevent runaway auto-generation. Pure-markdown impl preserves harness-agnostic principle.
**Evidence**: high
**Provenance**: session 2026-05-30, commit fd4d2d1, tag v4.2.0
**Supersedes**: M3 stub from v4.0.0

### 2026-05-30 — Ship v4.1.0 — contradiction-resolution + parent-sync (M2)
**Decided**: Promoted 2 stubs to production. contradiction-resolution uses subject/predicate/value fingerprint matching against DECISIONS/OPEN_QUESTIONS/RISKS; halts write on conflict, queues to CONFLICTS.md, supports snooze-until-/done; 4 anti-patterns refused (recency-wins, grade-wins, silent-drop, indefinite-snooze). parent-sync stages to memory/sync/outbound/<iso>/ with manifest.json, requires explicit approval per push, sets parent files chmod 444, supports rollback via provenance pointers; local-only privacy mode blocks all parent sync.
**Why**: Memory integrity requires human arbitration on conflict (never silent resolve). Parent rollup needs provenance + approval gate to avoid contaminating parent state with low-quality child claims.
**Evidence**: high
**Provenance**: session 2026-05-30, commit cf94144, tag v4.1.0
**Supersedes**: M2 stubs from v4.0.0

### 2026-05-30 — Ship v4.0.0 — philosophical reset (M1)
**Decided**: Complete rewrite. Zeref is no longer an agent harness OS — it is a local-first context and memory engine. Deleted 109 specialist skills, 5 agents (fleet-router, council-convener, executive-qa, release-governor, context-engine), 3 identity files (ZEREF.md, ZEREFOS.md, ZEREFPROJECT.md), 14 zeref-prefixed commands, output-styles, registry, 5 v3 helper scripts. Built 10 disciplined skills, 6 disciplined agents, 7 commands, 5 config files, memory/ scaffold with append-only event log + snapshots, 3 privacy modes (exact/abstract/local-only). Net diff: −26,690 / +1,949 lines. Always-on context: 5,035 → 905 tokens (82% reduction).
**Why**: v3 OS framing was Yash-specific, CEO-themed, Claude-only — diverged from cross-harness/cross-model portability principle. v4 returns to first principles: persistent markdown memory, harness-agnostic AGENTS.md spec, privacy-first writes, human arbitration on contradictions, progressive activation.
**Evidence**: high
**Provenance**: session 2026-05-30, commit 1aeca5c → 1ee6f92, tag v4.0.0; v3 frozen at tag v3.0.0-frozen
**Supersedes**: all v3 architecture
