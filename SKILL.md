---
name: zeref
version: 4.2.0
description: Local-first context and memory engine for AI-assisted work. Harness-agnostic, model-agnostic, privacy-first. Per-project wiki + append-only event log + snapshots. Makes AI work cumulative instead of stateless.
---

# Zeref 4.0

Zeref is a local-first context and memory engine. It is **not** an agent harness, **not** a CEO persona, **not** an operating system. It is the persistent memory layer your AI tools should have had from day one.

## What Zeref does

- **Remembers**: per-project wiki + append-only event log + snapshots
- **Persists across harnesses**: works in Claude Code, Codex, Gemini CLI, or any tool that reads markdown
- **Protects**: 3 privacy modes (exact / abstract / local-only)
- **Arbitrates**: contradictions surface to the user; never silently resolved
- **Extends itself**: detects repeated patterns, drafts new skills review-first

## Entry points

- `/start` — session boot with context restored
- `/done` — write summary, persist decisions, prepare parent-sync
- `/status` — current session state
- `/stop` — end session, snapshot, optional parent push
- `/sync-parent` — manual parent rollup
- `/reset-permissions` — clear session overrides
- `/review-skill` — review pattern-detected skill drafts

## Architecture

See `AGENTS.md` (canonical), `CLAUDE.md` (Claude shim), `GEMINI.md` (Gemini shim).

## Memory layout

```
memory/
  raw/          # untouched source material
  wiki/         # canonical knowledge (INDEX, DECISIONS, OPEN_QUESTIONS, RISKS, CONFLICTS, ARCHIVE/)
  logs/         # session-events.jsonl (append-only)
  snapshots/    # point-in-time wiki state
  sync/         # outbound and parent rollup artifacts
```

## Promise

Zeref makes AI work feel cumulative instead of stateless.
