# CLAUDE.md — Claude harness shim

**Canonical spec: `AGENTS.md`** — read it first. This file only adds Claude-specific notes.

## Claude-specific

- Use Claude Code's Skill tool to invoke skills as `zeref:<skill-name>` (post-install).
- Slash commands resolve under `/zeref:<command>` namespace.
- Sub-agents (Task tool) are not required — Zeref uses lightweight markdown agents.
- Prefer Haiku for `memory-keeper` writes; Sonnet for `project-setup` interview; Opus only for `pattern-to-skill` draft generation.

## First action every session

Identical to AGENTS.md §"First action every session":
1. Read `config/PROJECT.md`
2. Read `memory/wiki/INDEX.md` (boundary-first)
3. Tail last 3 entries of `memory/logs/session-events.jsonl`
4. Report state

## Safety

See `references/zeref-safety-principles.md`. Irreversible actions always require explicit user confirmation.
