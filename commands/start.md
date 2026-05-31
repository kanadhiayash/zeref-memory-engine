---
description: Boot a Zeref session. Runs interview if config/PROJECT.md missing, otherwise restores context from memory/wiki/ + memory/logs/.
---

If `config/PROJECT.md` does not exist OR `$ARGUMENTS` includes `--reset`:
1. Invoke `project-setup` skill to run the interview.
2. After interview completes, prompt user to re-run `/start` to boot the session.

Otherwise (normal boot):
1. Invoke `sync-coordinator` agent — apply permissions from `config/PERMISSIONS.md`, mount parent if enabled.
2. Invoke `memory-keeper` agent ORIENT operation:
   - Read `config/PROJECT.md`
   - Read `memory/wiki/INDEX.md` (boundary-first)
   - Tail last 3 entries of `memory/logs/session-events.jsonl`
3. Invoke `budget-governor` skill — report active tier + always-on context size.
4. If `memory/sync/outbound/handoff-*/` exists (newest), invoke `handoff-orchestrator` CONSUME.
5. Report:
   ```
   Project: <name>
   Last session: <iso>
   Active decisions: <count>
   Open questions: <count>
   Conflicts: <count>
   Privacy mode: <mode>
   Model tier: <tier>
   Always-on context: ~<N> tokens

   What do you want to work on?
   ```
