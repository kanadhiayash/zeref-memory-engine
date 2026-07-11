# ZEREF_COMPONENT_INVENTORY.md

Baseline: `b82c6410bf17b1bc4d1c79227c3a55e075858ab9`. Counts derived, never copied.

## Derived counts (WS-B verified)

| Surface | Baseline | Post-Phase-0.3 | Doc claim | Delta |
|---|---|---|---|---|
| Agents | 6 | 6 | 6 (AGENTS.md:111) | ok |
| Skills on disk (SKILL.md) | 15 | 15 | 14 (AGENTS.md:122); 10 (AGENTS.md:255); 10 (skill-router SKILL.md × 3) | **drift** |
| Skills in registry | 14 | 14 | 15 on disk | `skill-importer` unregistered |
| Slash commands | 8 | 8 | 8 (AGENTS.md:141) | ok |
| Team packs | 9 | **10** | 6 (AGENTS.md:212); 6 (Architecture.md:5); 9 (Home.md:30) | **drift** |
| CLI top-level command families | 23 | 23 | not documented as slash | disjoint |
| Benchmark modules | 28 (files) / **23** (scoring axes) | same | "28 benchmark axes" (handoff) / "10/10" (public claim) | axis count wrong |
| Workflows | 5 | 5 | 5 | ok (see WS-F for validity) |
| Tracked files | 286 | +11 audit artifacts | — | — |

## Component matrix (partial, WS-B; append remediation rows as landed)

Status ∈ `{active, inactive, draft, compatibility, historical, orphaned, unknown}`.

### Agents (6/6 on disk; 0 in registry)

| Component | Type | Path | Registered | Documented | Runtime-backed | Tested | Status |
|---|---|---|---|---|---|---|---|
| memory-keeper | agent | agents/memory-keeper.md | no | AGENTS.md:115 | zeref/memory/* | conftest | active |
| privacy-guardian | agent | agents/privacy-guardian.md | no | AGENTS.md:116 | zeref/privacy.py | test_privacy_guard | active |
| sync-coordinator | agent | agents/sync-coordinator.md | no | AGENTS.md:117 | **none** | **none** | active (md-only) |
| evidence-curator | agent | agents/evidence-curator.md | no | AGENTS.md:118 | zeref/memory/evidence.py | test_evidence_guard | active |
| pattern-observer | agent | agents/pattern-observer.md | no | AGENTS.md:119 | **none** | **none** | active (md-only) |
| handoff-orchestrator | agent | agents/handoff-orchestrator.md | no | AGENTS.md:120 | zeref/handoff/* | test_prompt_handoff_loop | active |

### Skills (15 on disk; 14 registered)

| Component | Registered | Runtime-backed | Status |
|---|---|---|---|
| budget-governor | yes | none | active |
| skill-router | yes | none (md-only; `zeref route` = different concept) | active |
| fleet-activator | yes | none | active |
| prompt-context-engine | yes | zeref/cli.py cmd_prompt | active |
| handoff-compiler | yes | zeref/handoff/compiler.py | active |
| caveman-handoff | yes | none | active |
| evidence-grader | yes | zeref/cli.py cmd_grade | active |
| wiki-maintenance | yes | none | active |
| project-setup | yes | zeref/cli.py cmd_init | active |
| contradiction-resolution | yes | zeref/memory/contradictions.py | active |
| privacy-abstraction | yes | zeref/privacy.py | active |
| parent-sync | yes | none | active |
| pattern-to-skill | yes | none | active |
| memory-import-export | yes | none | active |
| **skill-importer** | **no** | none | **orphaned** (self-declares registered but missing) |

### Slash commands (8/8 on disk; 0 in registry — registry has no `commands[]` array)

`/start, /done, /stop, /status, /sync-parent, /reset-permissions, /review-skill, /team`

### CLI command families (23; disjoint from slash surface except `status`)

`status, write-decision, grade, audit-privacy, audit, init, db-status, memory, recall, explain-search, cost, factguard, evidence, facts, contradictions, privacy, route, release, doctor, prompt, handoff, loop, lineage`

### Team packs (10 on disk; two orthogonal schemas)

Role packs (6, Schema A): `solo, build, research, red, audit, ship`.
Execution profiles (3, Schema B): `small, medium, enterprise`.
Council pack (1, Schema B+): `faang-mangoes-council` (Phase-0.3).

`commands/team.md:3` argument-hint enumerates only role packs.
`scripts/zeref-validate.py:45` hard-codes 6 role packs and prints `Team packs: 6/6` regardless.

### Skill imports (Phase-0.2, reference-only)

`skills/imported/{gstack, ecc, mantishack, raptor, hacker-bob}/README.md` — no source vendored, no registry entry, no runtime touch. Classification: public (gstack, ecc) / restricted (mantishack, raptor, hacker-bob).

### skills/drafts/ contract

Referenced by AGENTS.md:46, 210, 255-256, scripts/zeref-validate.py:236-243, commands/review-skill.md:9, agents/pattern-observer.md, skills/pattern-to-skill/, skills/skill-importer/. **Directory does not exist.** Validator handles absence; workflows silently no-op.

## Documentation classification (WS-A)

Every root `.md` and `docs/*.md` classified per handoff schema.

### active-truth (keep)

Root: `README.md, AGENTS.md, CHANGELOG.md, CLAUDE.md, CODEX.md, GEMINI.md, LLAMA.md, INSTALL.md, PRIVACY.md, REDACT.md, SHARING_POLICY.md, SECURITY.md, SECURITY_CONTACTS.md, SKILL.md, GITHUB_OS.md, CONTRIBUTING.md, MIGRATION.md (compat-scoped).`

Docs: `AUDIT_LOGS.md, BENCHMARK_ADAPTERS.md, BENCHMARK_REPORT.md, CONTRADICTIONGUARD.md, DOCTOR.md, EVIDENCEGUARD.md, FACTGUARD.md, GETTING_STARTED.md, HARNESS_MATRIX.md, LINEAGE_UPGRADE_ROADMAP.md, MEMORY_MODEL.md, MEMORY_WRITES.md, PRIVACYGUARD.md, PUBLIC_SAFE_COPY.md, PUBLIC_SURFACE.md, RELEASE_GATES.md, RELEASE_PROCESS.md, RETRIEVAL_BENCHMARKS.md, RISK_LOG.md, ROUTING.md, SECURITY_HARDENING.md, TRUST_AUDIT.md`.

Wiki: `Architecture.md, FAQ.md, Glossary.md, Home.md, Inspirations.md, Installation.md, Memory-Model.md, Pattern-Detection.md, Privacy-Model.md, Stack.md, Team-Packs.md`.

### superseded (rewrite required)

- `QUICKSTART.md:1` labelled v2.5; install channel wrong (WSA-4).
- `docs/wiki/_Sidebar.md:4` labelled v2.6 (WSA-9).
- `HARDENING_OVERVIEW.md:1` labelled v1.1 vs CHANGELOG v1.0.0 (WSA-14).

### compatibility (keep with note)

- `MIGRATION.md` — historical v3/v4.2 chains; commands drift (WSA-6, WSA-7).
- `docs/wiki/Installation.md` — retains `zeref-os` install commands per compat policy.

### historical (archive-marker present, keep for reference)

- `docs/PIVOT_LOG.md, docs/RELEASE_LOG.md, docs/archive/*` — pre-v1 material.

### archive-candidate (move on remediation)

- `docs/archive/INSPIRATIONS.md` — duplicates `docs/wiki/Inspirations.md` (WSA-10).

## Boot-order file presence

| Step | Path | Present |
|---|---|---|
| 0 | `SOUL.md` | **no** (WSA-1, prior audit re-verified) |
| 1 | `config/PROJECT.md` | yes, but leaks abs path (WSD-1) |
| 2 | `memory/hot.md` | no (by-design; init-generated) |
| 3 | `memory/index.md` | no (by-design; init-generated) |
| 4a-c | `PRIVACY.md, REDACT.md, SHARING_POLICY.md` | yes |
| 5 | `_shared/rules.md` | (verify in remediation) |
| 6 | `memory/MEMORY.md` | no (by-design) |
| 7 | `memory/patterns/PATTERNS.jsonl` | no (by-design) |

## Fleet imports (Phase-0.2)

| Pack | Classification | Source | Runtime touch | Council-member |
|---|---|---|---|---|
| gstack | public | `~/.claude/skills/graphify/` + gstack global | none | support |
| ecc | public | global ecc plugin | none (MCP invoked via `mcp__plugin_ecc_*`) | primary MCP surface |
| mantishack | restricted | `~/security-workspace/mantishack/` | none | on-demand red-team |
| raptor | restricted | `~/security-workspace/raptor/` | none | on-demand red-team |
| hacker-bob | restricted | `~/security-workspace/` (MCP) | none | on-demand red-team |
