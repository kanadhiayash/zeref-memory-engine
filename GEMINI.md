# GEMINI.md — Gemini harness shim

**Canonical spec: `AGENTS.md`** — read it first. This file only adds Gemini-specific notes.

## Gemini-specific

- Large-context-friendly: Gemini can load full `memory/wiki/` in a single call. Still prefer boundary-first (INDEX → section) for token discipline.
- No native skill registry: invoke skills by reading the relevant `skills/<name>/SKILL.md` directly.
- Commands map to user prompts containing `/start`, `/done`, etc. — interpret as instruction triggers.
- Tool-state awareness: surface MCP tool availability in session boot report.

## First action every session

Identical to AGENTS.md §"First action every session":
1. Read `config/PROJECT.md`
2. Read `memory/wiki/INDEX.md`
3. Tail last 3 entries of `memory/logs/session-events.jsonl`
4. Report state
