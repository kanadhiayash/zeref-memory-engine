# AGENTS.md — Zeref 4.0 Canonical Spec

This is the canonical agent specification for Zeref. All harness-specific files (`CLAUDE.md`, `GEMINI.md`) defer to this document.

## Identity

Zeref is a local-first context and memory engine. Harness-agnostic, model-agnostic, privacy-first. Per-project canonical wiki + append-only event log + snapshots.

## First action every session

1. Read `config/PROJECT.md`. If missing, run `/start`.
2. Read `memory/wiki/INDEX.md` (boundary-first — do not read full pages).
3. Tail last 3 entries of `memory/logs/session-events.jsonl`.
4. Report: project, last session, active decisions, open questions, conflicts.

## Core principles

1. **Local-first**: canonical state is markdown on disk; no hosted dependency
2. **Privacy-first**: every write passes through privacy mode check
3. **Boundary-first reads**: INDEX → page section, never full pages by default
4. **Human arbitration**: contradictions surface; never silently resolved
5. **Single-writer per resource**: only `memory-keeper` writes to `memory/wiki/`
6. **Append-only logs**: `memory/logs/session-events.jsonl` is never edited
7. **Progressive activation**: minimal agents auto-load; rest lazy on trigger
8. **Evidence discipline**: separate facts / assumptions / unknowns / risks
9. **Token discipline**: budget-governor scales verbosity to model tier
10. **Review-first extension**: new skills are drafted, never auto-activated

## Agents (6)

| Agent | Auto-load | Role |
|---|---|---|
| `memory-keeper` | yes | Single writer to `memory/wiki/`; reads, writes, logs |
| `privacy-guardian` | conditional | Enforces privacy mode on every write |
| `sync-coordinator` | on `/start`/`/stop`/`/sync-parent` | Permissions, tool visibility, parent push |
| `evidence-curator` | conditional | Grades confidence, recency, provenance |
| `pattern-observer` | background | Watches `session-events.jsonl` for repeats |
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

## Commands (7)

- `/start` — interview if first run; otherwise boot session, restore context
- `/done` — write summary, persist decisions, update INDEX, snapshot
- `/stop` — end session, optional parent sync
- `/status` — current state: project, active decisions, open questions
- `/sync-parent` — manual parent rollup
- `/reset-permissions` — clear session overrides, restore defaults
- `/skill` — review pattern-detected skill drafts

## Memory model

- `memory/raw/` — untouched source material (specs, transcripts, docs)
- `memory/wiki/` — canonical knowledge (single writer: `memory-keeper`)
  - `INDEX.md` — domain map (boundary file)
  - `DECISIONS.md` — confirmed decisions w/ provenance + evidence grade
  - `OPEN_QUESTIONS.md` — unresolved questions w/ owner
  - `RISKS.md` — identified risks w/ severity
  - `CONFLICTS.md` — contradiction queue (user arbitrates)
  - `ARCHIVE/` — superseded snapshots
- `memory/logs/session-events.jsonl` — append-only event log
- `memory/snapshots/<iso>/` — point-in-time wiki state + manifest
- `memory/sync/outbound/` — staged parent updates
- `memory/sync/parent/` — received parent updates

## Event log schema

```jsonl
{"ts": "2026-05-28T14:23:11Z", "agent": "memory-keeper", "event": "wiki-write", "target": "memory/wiki/DECISIONS.md", "payload": {"summary": "..."}, "hash": "sha256:...", "evidence_grade": "high"}
```

Fields: `ts` (ISO-8601 UTC), `agent`, `event`, `target` (path), `payload` (free), `hash` (sha256 of payload), `evidence_grade` (high/medium/low — optional).

## Privacy modes

- `exact` — write full detail
- `abstract` — `privacy-abstraction` rewrites before write (remove names, numbers, internals)
- `local-only` — block all `memory/sync/outbound/` writes

## Permission model

See `config/PERMISSIONS.md`. YAML frontmatter:

```yaml
defaults:
  filesystem: [read-project, write-memory]
  network: [denied]
  mcp_servers: []
session_overrides:
  # ephemeral; cleared by /reset-permissions or /stop
```

## Contradiction handling

When `memory-keeper` detects a conflict between an incoming write and existing wiki state:
1. Halt write
2. Append both sides to `memory/wiki/CONFLICTS.md`
3. Surface to user immediately OR snooze until `/done` (user choice)
4. User arbitrates; never silent resolution
5. Resolved entries move to `DECISIONS.md` with both-sides provenance

## Pattern detection

`pattern-observer` runs background scan of `session-events.jsonl` over rolling 72h window. If ≥3 semantically similar events (n-gram similarity ≥0.8), surface as candidate skill via `pattern-to-skill`. Draft written to `skills/_drafts/<draft-name>/SKILL.md`. User reviews via `/skill`. Never auto-activate.

## Parent sync

If `config/PARENT_SYNC.md` declares a parent path:
- On approved `/stop` or `/sync-parent`, `parent-sync` skill stages summary + decisions in `memory/sync/outbound/`
- Parent project reads `memory/sync/parent/<child-id>/`
- Provenance preserved (child id, ts, source events)
- Contradictions between child and parent surface to user

## Migration

v3 → v4: `scripts/migrate-v3-to-v4.py` reads old `wiki/hot.md` and `wiki/log.md`, emits new `memory/wiki/INDEX.md` + `memory/wiki/ARCHIVE/` + `memory/logs/session-events.jsonl`. See `MIGRATION.md`.

## What Zeref is not

- Not an agent harness
- Not a CEO persona
- Not Yash-specific
- Not Claude-only
- Not a hosted service
- Not a multi-agent council
- Not a skills empire
