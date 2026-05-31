# Zeref 4.0

**Local-first context and memory engine for AI-assisted work.**

Harness-agnostic. Model-agnostic. Privacy-first. Developer-first. Free.

## What

Zeref is the persistent memory layer your AI tools should have had from day one. Per-project canonical wiki in markdown, append-only event log, point-in-time snapshots, contradiction safety, privacy modes.

## Why

AI sessions today are stateless. You re-explain your project every conversation. You lose decisions to context window resets. You can't switch from Claude to Codex to Gemini without abandoning your project memory.

Zeref makes AI work cumulative instead of stateless.

## How it works

```
/start  → boot session, restore last 3 sessions in <2k tokens
work    → memory-keeper writes decisions, open questions, risks to memory/wiki/
        → privacy-guardian filters per your privacy mode
        → memory-keeper detects contradictions and surfaces them
/done   → consolidate wiki, snapshot state, optional parent sync
/stop   → end session, optional cross-harness handoff package
```

## Architecture

- **6 agents**: memory-keeper, privacy-guardian, sync-coordinator, evidence-curator, pattern-observer, handoff-orchestrator
- **10 skills**: project-setup, wiki-maintenance, contradiction-resolution, privacy-abstraction, parent-sync, pattern-to-skill, memory-import-export, budget-governor, handoff-compiler, evidence-grader
- **7 commands**: `/start`, `/done`, `/stop`, `/status`, `/sync-parent`, `/reset-permissions`, `/review-skill`

See `AGENTS.md` for the full canonical spec. `CLAUDE.md` and `GEMINI.md` are harness-specific shims.

## Memory layout

```
memory/
  raw/          # source material
  wiki/         # canonical knowledge (INDEX, DECISIONS, OPEN_QUESTIONS, RISKS, CONFLICTS, ARCHIVE/)
  logs/         # append-only session-events.jsonl
  snapshots/    # point-in-time wiki state
  sync/         # outbound and parent rollup artifacts
```

## Privacy modes

- `exact` — write full detail
- `abstract` — strip PII, paths, credentials before write
- `local-only` — block all outbound sync

## What Zeref is not

Not an agent harness. Not a CEO persona. Not Yash-specific. Not Claude-only. Not a hosted service. Not a multi-agent council. Not a skills empire.

## Install

See `INSTALL.md`.

## Migrate from v3

See `MIGRATION.md` and `scripts/migrate-v3-to-v4.py`.

## Roadmap

- **v4.0 (M1)**: core engine — memory + commands + privacy ✅ shipped
- **v4.1 (M2)**: full contradiction-resolution + parent-sync ✅ shipped
- **v4.2 (M3, current)**: pattern detection + skill drafting ✅ shipped

## Version compatibility

| Tag | Status | Claude Code plugin schema | Notes |
|---|---|---|---|
| `v4.2.0` | **live** | ✔ current | Production. `claude plugin install zeref@zeref` |
| `v4.1.0` | live | ✔ current | M2 — adds contradiction-resolution + parent-sync |
| `v4.0.0` | live | ✔ current | M1 — philosophical reset, core engine |
| `v3.0.0` | legacy archive | ✘ obsolete | Pre-v4 Agent OS framing. Won't install under current schema. |
| `v2.1` | legacy archive | ✘ obsolete | Pre-marketplace fleet consolidation snapshot. |
| `v2.0` | legacy archive | ⚠ warning | Snapshot of v2 fleet. Loads with warnings. |
| `v1.1` | legacy archive | ✘ no manifest | Predates `.claude-plugin/` format. |

Tags `v1.x`, `v2.x`, `v3.x` are preserved as historical snapshots for archival reference only. Install only `v4.x` releases.

## License

MIT. Free for any user, any harness, any model.

