# Migration: Zeref v3 → v4

## TL;DR

v4 is a clean philosophical reset. The 109 v3 specialist skills, CEO/fleet/council framing, Yash-specific identity, and `ZEREF.md`/`ZEREFOS.md`/`ZEREFPROJECT.md` stack are all gone. v4 is a pure context + memory engine.

v3 is frozen at git tag `v3.0.0-frozen` for archive.

## Why

v3 had become a theatrical multi-agent operating system. v4 returns to first principles:
- Local-first markdown memory
- Harness-agnostic (Claude / Codex / Gemini / any)
- Model-agnostic
- Privacy-first
- Human arbitration (no silent conflict resolution)
- Progressive activation (small default, optional power)

## What's gone

- 109 specialist skills (`zeref-biz-*`, `zeref-cnt-*`, `zeref-dev-*`, `zeref-mkt-*`, `zeref-qa-*`, `zeref-ux-*`, `zeref-hq-*`, `zeref-final-*`)
- `zeref-fleet-router`, `zeref-council-convener`, `zeref-executive-qa-agent`, `zeref-release-governor`, `zeref-context-engine` agents
- `commands/zeref-*` (14 commands)
- `ZEREF.md`, `ZEREFOS.md`, `ZEREFPROJECT.md`
- `registry/zeref-skill-registry.json`
- `output-styles/zeref-executive.md`
- All CEO / Yash-specific / Ruflo / council framing

## What's renamed

| v3 | v4 |
|---|---|
| `agents/zeref-memory-keeper.md` | `agents/memory-keeper.md` |
| `agents/zeref-trust-sentinel.md` | `agents/privacy-guardian.md` |
| `agents/zeref-evaluator.md` | `agents/evidence-curator.md` |
| `wiki/hot.md` | `memory/wiki/INDEX.md` (entries) + `memory/wiki/ARCHIVE/hot-<iso>.md` |
| `wiki/log.md` | `memory/logs/session-events.jsonl` |
| `wiki/index.md` | `memory/wiki/INDEX.md` |
| `/zeref-activate` | `/start` |
| `/zeref-save` | `/done` |
| `/zeref-orient` | (folded into `/start` boot) |
| `/zeref-recall` | (folded into `memory-keeper` READ op) |

## What's new

- `config/` (5 files): PROJECT, PRIVACY, PERMISSIONS, PARENT_SYNC, BUDGET
- `memory/` scaffold: raw, wiki, logs, snapshots, sync/{outbound,parent}
- `AGENTS.md` canonical spec (addyosmani convention)
- `GEMINI.md` harness shim
- 10 disciplined skills (down from 109)
- 6 disciplined agents (down from 8)
- 7 commands (down from 14)
- Append-only `session-events.jsonl` event log
- Snapshot system
- Parent sync mechanism (M2 in v4.1.0)
- Pattern-to-skill detection (M3 in v4.2.0)

## How to migrate your data

```bash
# 1. Back up your v3 wiki first
cp -r /path/to/v3-project/wiki ~/zeref-v3-backup-$(date +%Y%m%d)

# 2. Install v4
claude plugin install zeref@zeref

# 3. Run migration script
python3 scripts/migrate-v3-to-v4.py --from /path/to/v3-project/wiki --to ./memory

# 4. Run /start in a fresh session
# Interview will guide you through the new config/ files
```

## Backward compatibility

None. v4 is a clean break. Run `/start` and re-enter project context — it takes ~5 min and produces a much more disciplined state.

## Roadmap

- **v4.0 (M1, ships now)**: core engine
- **v4.1 (M2)**: full contradiction-resolution + parent-sync (currently stubs)
- **v4.2 (M3)**: pattern-observer + pattern-to-skill (currently stubs)
