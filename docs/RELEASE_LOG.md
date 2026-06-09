# Zeref OS — Release Log

Controlled baselines per FAANG architecture brief §3.4 + global GITHUB_OS §3.4. One row per tagged release. Source: `CHANGELOG.md` (post-rebrand) + `CHANGELOG-LEGACY.md` (pre-rebrand).

## Post-rebrand canonical chain

| Tag | Date | Summary | Migration |
|---|---|---|---|
| `v2.6.1` | 2026-06-08 | Audit + Hardening Campaign — 7-phase deep audit, 15 L-items, rubric 8.00 → 9.88 | `MIGRATION.md#v2.6.1` (none — additive only) |
| `v2.6.0` | 2026-06-08 | Auto-Gated Execution — 4-gate chain (budget → router → fleet → prompt → handoff); +4 skills (skill-router, fleet-activator, prompt-context-engine, caveman-handoff); +2 Core Principles (13, 14); +R6 Zero Context Loss | `MIGRATION.md#v2.6.0` (none — additive) |
| `v2.5.0` | 2026-06-05 | Deep Audit Campaign (Phases A-F); zeref/ runtime (privacy, lock, cli, db, demo, dashboard); 85-claim audit + 300-row sandbox + 8 attacks; L1-L11 workarounds; rubric 7.13 → 8.00 | `MIGRATION.md#v2.5.0` |
| `v1.0.0` | 2026-05-31 | Canonical release + rebrand (Zeref Skills Fleet/Agent OS → Zeref OS); flat memory layout, root privacy templates, team packs, harness translation map, Two-Strikes Rule | `MIGRATION.md` (v4.x → v1.0 rebrand notes) |

## Pre-rebrand legacy chain (GitHub `prerelease`)

| Tag | Date | Summary | Notes |
|---|---|---|---|
| `v4.3.0` | 2026-05-31 | v4.x canon import + nomenclature alignment + team packs (M4) | Last commit before v1.0.0 rebrand |
| `v4.2.0` | 2026-05-30 | M3 — pattern-observer + pattern-to-skill (full impl); v4 roadmap complete | |
| `v4.1.0` | 2026-05-30 | M2 — contradiction-resolution + parent-sync (full impl) | |
| `v4.0.0` | (earlier) | Philosophical reset — local-first context + memory engine; deleted 109 specialist skills; 10 disciplined skills | Major ideology shift |
| `v3.0.0` | (earlier) | Zeref Agent OS v3.0.0 — Context Engine + Agent Harness OS | |
| `v2.1.0` | (earlier) | Fleet consolidation 112 → 102 skills | |
| `v2.0.0` | (earlier) | CLAUDE.md + INSTALL.md + hardened gitignore + registry update + validator fix | |

## Conventions

- **SemVer**: `v<major>.<minor>.<patch>` on `main` only per GITHUB_OS §3.4
- **Pre-rebrand**: marked GitHub `prerelease=true`; commits exist but tags were deleted in past `[Unreleased]` cleanup and restored in v2.6.1 history-reconstruction campaign
- **Migration links**: `MIGRATION.md` documents breaking changes + transition steps where applicable

## Command center

Notion: https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3
