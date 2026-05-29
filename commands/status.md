---
description: Show current session state without modifying anything. Read-only.
---

Read-only. Do not write to memory or modify config.

1. Read `config/PROJECT.md` — report project name, privacy mode, model tier, parent sync status.
2. Read `memory/wiki/INDEX.md` — report domain count, last updated.
3. Count entries in `DECISIONS.md`, `OPEN_QUESTIONS.md`, `RISKS.md`, `CONFLICTS.md`.
4. Read tail 10 lines of `memory/logs/session-events.jsonl` — report event types + counts.
5. List active permission overrides (in-memory, if any).
6. Output:
   ```
   == Zeref Status ==
   Project: <name>
   Privacy: <mode> | Tier: <tier> | Parent sync: <on|off>

   Wiki:
     Domains: <N>
     Decisions: <N> (recent: <last decision title>)
     Open questions: <N>
     Risks: <N>
     Conflicts: <N> (snoozed: <N>)

   Recent events (last 10):
     <ts> <agent> <event>
     ...

   Active session overrides: <list or "none">
   ```
