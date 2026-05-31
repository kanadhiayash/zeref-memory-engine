---
name: zeref
version: 4.3.0
description: Local-first context and memory engine for AI-assisted work. Harness-agnostic, model-agnostic, privacy-first. Flat memory layout, per-project wiki, append-only pattern log, snapshots, on-demand team packs. Makes AI work cumulative instead of stateless across every harness.
---

# Zeref 4.3

Zeref is a local-first context and memory engine. It is **not** an agent harness, **not** a CEO persona, **not** an operating system. It is the persistent memory layer your AI tools should have had from day one.

## What Zeref does

- **Remembers**: per-project flat `memory/` wiki + append-only `PATTERNS.jsonl` + snapshots
- **Persists across harnesses**: works in Claude Code, Codex, Gemini CLI / Antigravity, Cursor, Windsurf, Aider, Hermes, Amp, Zed, Perplexity Computer, or any tool that reads markdown (per ZEREF_OS §10)
- **Protects**: 3 privacy modes (exact / abstract / local-only) + REDACT.md sensitive classes + SHARING_POLICY.md connector allowlist (all OFF by default)
- **Arbitrates**: contradictions surface to the user; never silently resolved
- **Extends itself**: detects repeated patterns (Two-Strikes Rule), drafts new skills review-first to `skills/drafts/`
- **Activates teams on demand**: `/team [solo|build|research|red|audit|ship]` — max 4 agents per pack

## Entry points

- `/start` — session boot with context restored (hot.md → index.md per ZEREF_OS §0)
- `/done` — write summary, persist decisions, refresh hot.md, conflict scan, snapshot
- `/stop` — end session, optional parent push, optional handoff compile
- `/status` — current session state + active team + pending drafts
- `/team` — activate a team pack
- `/sync-parent` — manual parent rollup
- `/reset-permissions` — clear session overrides
- `/review-skill` — review pattern-detected skill drafts

## Architecture

See `AGENTS.md` (canonical), `CLAUDE.md` (Claude shim), `GEMINI.md` (Gemini shim), `.cursor/rules/zeref.mdc`, `.windsurfrules`, `.aider.conf.yml.example`.

## Memory layout (flat per ZEREF_OS §12)

```
memory/
  hot.md            # last 3 sessions, ≤500 words (read FIRST)
  index.md          # domain index
  MEMORY.md         # agent-written session notes
  DECISIONS.md / OPEN_QUESTIONS.md / RISKS.md / CONFLICTS.md
  archive/          # superseded entries (never deleted per D9)
  patterns/PATTERNS.jsonl  # append-only event log
  snapshots/        # point-in-time wiki state
  sync/             # outbound and parent rollup artifacts
  raw/              # untouched source material
```

## Promise

Zeref makes AI work feel cumulative instead of stateless — in every harness, with any model, with privacy on by default.
