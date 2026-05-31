# Zeref 4.3

**Local-first context and memory engine for AI-assisted work.**

Harness-agnostic. Model-agnostic. Privacy-first. Developer-first. Free.

## What

Zeref is the persistent memory layer your AI tools should have had from day one. Per-project canonical wiki in markdown (flat `memory/` layout), append-only pattern log, point-in-time snapshots, contradiction safety, privacy modes, on-demand team packs, cross-harness handoff.

## Why

AI sessions today are stateless. You re-explain your project every conversation. You lose decisions to context window resets. You can't switch from Claude to Codex to Gemini to Cursor without abandoning your project memory.

Zeref makes AI work cumulative instead of stateless — across every harness.

## How it works

```
/start  → boot session, restore last 3 sessions in <2k tokens (hot.md → index.md)
work    → memory-keeper writes decisions, open questions, risks to flat memory/
        → privacy-guardian filters per PRIVACY.md + REDACT.md + SHARING_POLICY.md
        → memory-keeper detects contradictions and surfaces them
        → pattern-observer logs every tool call to memory/patterns/PATTERNS.jsonl
/team   → activate on-demand team pack (solo/build/research/red/audit/ship)
/done   → consolidate wiki, refresh hot.md, snapshot state, optional parent sync
/stop   → end session, optional cross-harness handoff package
```

## Architecture

- **6 agents**: memory-keeper, privacy-guardian, sync-coordinator, evidence-curator, pattern-observer, handoff-orchestrator
- **10 skills**: project-setup, wiki-maintenance, contradiction-resolution, privacy-abstraction, parent-sync, pattern-to-skill, memory-import-export, budget-governor, handoff-compiler, evidence-grader
- **8 commands**: `/start`, `/done`, `/stop`, `/status`, `/sync-parent`, `/reset-permissions`, `/review-skill`, `/team`
- **6 team packs**: solo, build, research, red, audit, ship (per ZEREF_OS §8)

See `AGENTS.md` for the canonical spec. `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/zeref.mdc`, `.windsurfrules`, `.aider.conf.yml.example` are harness-specific stubs that all defer to `AGENTS.md`.

## Memory layout (flat per ZEREF_OS §12)

```
project-root/
├── AGENTS.md                    (canonical source of truth)
├── CLAUDE.md / GEMINI.md / ...  (harness stubs)
├── PRIVACY.md                   (modes — default abstract)
├── REDACT.md                    (sensitive classes)
├── SHARING_POLICY.md            (connectors — OFF by default)
├── memory/
│   ├── hot.md                   (last 3 sessions, ≤500 words — read FIRST)
│   ├── index.md                 (domain index)
│   ├── MEMORY.md                (agent-written session notes)
│   ├── DECISIONS.md / OPEN_QUESTIONS.md / RISKS.md / CONFLICTS.md
│   ├── archive/                 (superseded — never deleted per D9)
│   └── patterns/PATTERNS.jsonl  (append-only tool/event log)
├── skills/drafts/               (pattern-detected drafts pending approval)
├── team/                        (team pack outputs)
├── team-packs/                  (6 pack definitions)
└── config/
    ├── PROJECT.md / PERMISSIONS.md / PARENT_SYNC.md / BUDGET.md
    └── claude-overrides.md
```

## Privacy

Three root files govern privacy (per ZEREF_OS §4):

- `PRIVACY.md` — modes (`exact` / `abstract` / `local-only`) — default `abstract`
- `REDACT.md` — concrete sensitive classes (credentials, pii, internal_paths, client_data, financial, proprietary_code)
- `SHARING_POLICY.md` — per-connector allowlist (all OFF by default)

Every write to `memory/` and every external transmission passes through `privacy-guardian`.

## Token budget (per ZEREF_OS §5)

Three tiers, auto-detected from model:

| Tier | Models | Behavior |
|---|---|---|
| **Free** | Gemini Flash, local Ollama, Mistral | aggressive compaction |
| **Standard** | GPT-4o mini, Claude Haiku, Gemini Flash 3.5 | normal |
| **God Mode** | GPT-4o, Claude Opus/Sonnet, Gemini 3.5 Pro | full sync + deep analysis |

## Team packs (per ZEREF_OS §8)

On-demand only. Max 4 agents. Outputs land in `team/`.

| Team | Roster |
|---|---|
| solo | 1 primary + memory engine (default) |
| build | Planner + Implementer + Reviewer |
| research | Investigator + Synthesizer + Fact-checker |
| red | Attacker + Security reviewer + Constraint checker + Evidence recorder (read-only) |
| audit | Reader + Linter + Quality gate |
| ship | Changelog drafter + Release reviewer + Deploy verifier |

Activate via `/team [type]`. Definitions in `team-packs/<name>.md`.

## Connector advisory (per ZEREF_OS §9)

Zeref ships zero bundled MCP tools. Recommendation-only after detected repetition. Full free stack catalog: `references/connector-advisory.md`.

## What Zeref is not

Not an agent harness. Not a CEO persona. Not a hosted service. Not a multi-agent council. Not a skill fleet. Not bundled with any MCP tools. Not dedicated to any single user or organization.

## Install

See `INSTALL.md`. Supports Claude Code, Codex, Cursor, Gemini CLI / Antigravity, Windsurf, Aider, Hermes, Amp, Zed, Perplexity Computer.

## Migrate

- v3 → v4: `scripts/migrate-v3-to-v4.py` + `MIGRATION.md`
- v4.2 → v4.3: `scripts/migrate-v4.2-to-v4.3.py` (flat memory layout cutover) — see `MIGRATION.md`

## Roadmap

- **v4.0 (M1)**: core engine — memory + commands + privacy ✅ shipped
- **v4.1 (M2)**: full contradiction-resolution + parent-sync ✅ shipped
- **v4.2 (M3)**: pattern detection + skill drafting ✅ shipped
- **v4.3 (M4, current)**: v4.x canon import + flat memory layout + team packs + harness translation map + Two-Strikes Rule ✅ shipped

## Version compatibility

| Tag | Status | Claude Code plugin schema | Notes |
|---|---|---|---|
| `v4.3.0` | **live** | ✔ current | Production. Flat memory layout. Team packs. Cross-harness stubs. |
| `v4.2.0` | live | ✔ current | M3 — pattern detection + skill drafting |
| `v4.1.0` | live | ✔ current | M2 — contradiction-resolution + parent-sync |
| `v4.0.0` | live | ✔ current | M1 — philosophical reset, core engine |
| `v3.0.0` | legacy archive | ✘ obsolete | Pre-v4 Agent OS framing. Won't install under current schema. |
| `v2.x` / `v1.x` | legacy archive | ⚠ varies | Snapshots only. Do not install. |

Install only `v4.x` releases. v4.3 includes the v4.2 → v4.3 migration script for existing installs.

## License

MIT. Free for any user, any harness, any model.
