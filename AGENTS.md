# AGENTS.md — Zeref OS Canonical Spec (v1.0.0)

This is the canonical agent specification for **Zeref OS**. All harness-specific files (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/zeref.mdc`, `.windsurfrules`, `.aider.conf.yml`) defer to this document.

## Identity

Zeref OS is a local-first context and memory engine. Harness-agnostic, model-agnostic, privacy-first. Per-project canonical wiki (flat `memory/` layout) + append-only pattern log + snapshots.

The name comes from Zeref Dragneel in *Fairy Tail* — the immortal scholar whose ancient knowledge transcended form, time, and faction. Zeref OS is built in that lineage: long-horizon memory, faithful to the user's accumulated decisions, portable across every AI harness.

## First action every session (reading order — ZEREF_OS §0)

1. Read `config/PROJECT.md`. If missing, run `/start` (triggers project-setup interview).
2. Read `memory/hot.md` FIRST (≤500 words; current context).
3. Read `memory/index.md` if hot is insufficient (domain index).
4. Read `PRIVACY.md` (root) before any wiki write or tool use.
5. Read `REDACT.md` (root) before any external output.
6. Auto-load first 200 lines of `memory/MEMORY.md` (agent-written session notes).
7. Tail last 3 entries of `memory/patterns/PATTERNS.jsonl`.
8. Report: project, last session, active decisions, open questions, conflicts.

Do NOT read individual wiki pages for general coding questions or things already in current project context.

## Core principles

1. **Local-first**: canonical state is markdown on disk; no hosted dependency
2. **Privacy-first**: every write passes through `privacy-guardian` (PRIVACY.md + REDACT.md + SHARING_POLICY.md)
3. **Boundary-first reads**: hot → index → page section, never full pages by default
4. **Human arbitration**: contradictions surface; never silently resolved
5. **Single-writer per resource**: only `memory-keeper` writes to wiki files
6. **Append-only logs**: `memory/patterns/PATTERNS.jsonl` is never edited
7. **Progressive activation**: minimal agents auto-load; rest lazy on trigger
8. **Evidence discipline**: separate facts / assumptions / unknowns / risks
9. **Token discipline**: `budget-governor` scales verbosity to model tier (Free / Standard / God Mode)
10. **Review-first extension**: new skills are drafted to `skills/drafts/`, never auto-activated
11. **Two-Strikes Rule**: do not codify a rule on the first occurrence of an error. See `references/two-strikes-rule.md`.
12. **Harness Agnosticism**: AGENTS.md is source of truth; per-harness stubs defer. See `references/harness-translation-map.md`.

## Agents (6)

| Agent | Auto-load | Role |
|---|---|---|
| `memory-keeper` | yes | Single writer to flat `memory/`; reads, writes, logs |
| `privacy-guardian` | conditional | Enforces PRIVACY.md mode + REDACT.md classes + SHARING_POLICY.md allowlist |
| `sync-coordinator` | on `/start`/`/stop`/`/sync-parent` | Permissions, tool visibility, parent push |
| `evidence-curator` | conditional | Grades confidence, recency, provenance |
| `pattern-observer` | background | Watches `memory/patterns/PATTERNS.jsonl` for repeats |
| `handoff-orchestrator` | on `/stop` / model switch | Packages cross-harness handoff |

## Skills (10)

| Skill | Activation |
|---|---|
| `project-setup` | First `/start` or missing config |
| `wiki-maintenance` | After writes; consolidation |
| `contradiction-resolution` | When `memory-keeper` flags conflict |
| `privacy-abstraction` | Before writes when mode = abstract |
| `parent-sync` | Approved `/stop` or `/sync-parent` |
| `pattern-to-skill` | Threshold hit in `pattern-observer` |
| `memory-import-export` | Explicit migration request |
| `budget-governor` | `/start`, tier change, budget warning |
| `handoff-compiler` | Session end or model switch |
| `evidence-grader` | On write, review, sync, conflict |

## Commands (8)

- `/start` — interview if first run; otherwise boot session, restore context (hot.md → index.md per §0)
- `/done` — write summary, persist decisions, refresh hot.md, conflict scan, append PATTERNS.jsonl, snapshot
- `/stop` — end session, optional parent sync, optional handoff compile
- `/status` — current state: project, active decisions, open questions, active team
- `/sync-parent` — manual parent rollup
- `/reset-permissions` — clear session overrides, restore defaults from PERMISSIONS + SHARING_POLICY
- `/review-skill` — review pattern-detected skill drafts in `skills/drafts/`
- `/team [solo|build|research|red|audit|ship]` — activate on-demand team pack (per ZEREF_OS §8)

## Memory model (flat layout per ZEREF_OS §12)

- `memory/hot.md` — last 3 sessions, ≤500 words (read first)
- `memory/index.md` — domain index (boundary file)
- `memory/DECISIONS.md` — confirmed decisions w/ provenance + evidence grade
- `memory/OPEN_QUESTIONS.md` — unresolved questions w/ owner
- `memory/RISKS.md` — identified risks w/ severity
- `memory/CONFLICTS.md` — contradiction queue (user arbitrates)
- `memory/MEMORY.md` — agent-written session notes (NOT human-edited)
- `memory/archive/` — superseded snapshots (never deleted per D9)
- `memory/patterns/PATTERNS.jsonl` — append-only tool/event log for pattern detection
- `memory/snapshots/<iso>/` — point-in-time wiki state + manifest
- `memory/raw/` — untouched source material
- `memory/sync/outbound/` — staged parent updates
- `memory/sync/parent/` — received parent updates

## Privacy & sharing (per ZEREF_OS §4)

Three root files:

- `PRIVACY.md` — modes (`exact` / `abstract` / `local-only`) — **default `abstract`**
- `REDACT.md` — concrete sensitive classes (credentials, pii, internal_paths, client_data, financial, proprietary_code)
- `SHARING_POLICY.md` — per-connector allowlist; **all OFF by default**

Every write to `memory/` and every external transmission passes through `privacy-guardian` per these files.

## Event log schema

```jsonl
{"ts": "2026-05-28T14:23:11Z", "agent": "memory-keeper", "event": "wiki-write", "target": "memory/DECISIONS.md", "payload": {"summary": "..."}, "hash": "sha256:...", "evidence_grade": "high"}
```

Fields: `ts` (ISO-8601 UTC), `agent`, `event`, `target` (path), `payload` (free), `hash` (sha256 of payload), `evidence_grade` (high/medium/low — optional).

## Permission model

See `config/PERMISSIONS.md` (filesystem / network / shell) and `SHARING_POLICY.md` (MCP / connectors).

```yaml
defaults:
  filesystem: [read-project, write-memory]
  network: [denied]
  mcp_servers: []      # see SHARING_POLICY.md for connector allowlist
session_overrides:
  # ephemeral; cleared by /reset-permissions or /stop
```

## Contradiction handling

When `memory-keeper` detects a conflict between an incoming write and existing wiki state:
1. Halt write
2. Append both sides to `memory/CONFLICTS.md`
3. Surface to user immediately OR snooze until `/done` (user choice)
4. User arbitrates; never silent resolution
5. Resolved entries move to `memory/DECISIONS.md` with both-sides provenance

## Pattern detection

`pattern-observer` runs background scan of `memory/patterns/PATTERNS.jsonl` over rolling 48–80h window (per ZEREF_OS §3.5 / D4). If ≥3 semantically similar events (n-gram similarity ≥ 0.8), surface as candidate skill via `pattern-to-skill`. Draft written to `skills/drafts/<draft-name>/SKILL.md`. User reviews via `/review-skill`. Never auto-activate.

## Team Packs (on-demand per ZEREF_OS §8)

| Team | Agents | Use |
|---|---|---|
| solo | 1 primary + memory engine | default |
| build | Planner + Implementer + Reviewer | multi-module features |
| research | Investigator + Synthesizer + Fact-checker | tech evaluation |
| red | Attacker + Security reviewer + Constraint checker + Evidence recorder (read-only) | adversarial review |
| audit | Reader + Linter + Quality gate | pre-ship QA |
| ship | Changelog drafter + Release reviewer + Deploy verifier | release prep |

Max 4 agents per pack. Outputs land in `team/`. Activate via `/team [type]`. Definitions in `team-packs/`.

## Connector Advisory (per ZEREF_OS §9)

Zeref OS ships with **zero** bundled MCP tools. Recommendation-only after `pattern-observer` detects repeated manual behavior. All connectors OFF by default in `SHARING_POLICY.md`. Recommended free stack documented in `references/connector-advisory.md`.

## Harness Translation Map (per ZEREF_OS §10)

| Harness | Stub | Load |
|---|---|---|
| Claude Code | `CLAUDE.md` | See @AGENTS.md |
| Codex | native | AGENTS.md |
| Cursor | `.cursor/rules/zeref.mdc` | rules format → AGENTS.md |
| Gemini CLI / Antigravity | `GEMINI.md` | native AGENTS.md |
| Windsurf | `.windsurfrules` | rules format → AGENTS.md |
| Aider | `.aider.conf.yml.example` | convention-based |
| Hermes / Amp / Zed / Perplexity | native | AGENTS.md |

Full table + adding-a-harness procedure: `references/harness-translation-map.md`.

## Migration

- v3 → v4: `scripts/migrate-v3-to-v4.py`
- v4.2 → v4.3 (this version): `scripts/migrate-v4.2-to-v4.3.py` (flat memory layout, root privacy templates, PATTERNS.jsonl cutover)

See `MIGRATION.md`.

## What Zeref OS is not

- Not an agent harness
- Not a CEO persona
- Not a hosted service
- Not a multi-agent council
- Not a skill fleet
- Not bundled with any MCP tools
- Not dedicated to any single user or organization
