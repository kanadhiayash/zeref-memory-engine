---
description: Persist session work. Writes summary, updates wiki, refreshes hot.md, runs conflict scan, appends pattern log, snapshots state, optionally prepares parent sync.
---

1. Invoke `memory-keeper` WRITE: append session summary to relevant wiki pages (`memory/DECISIONS.md` / `memory/OPEN_QUESTIONS.md` / `memory/RISKS.md` as applicable). Append session notes to `memory/MEMORY.md`.
2. Run a contradiction scan via `contradiction-resolution` SNOOZED REVIEW — surface any flagged or snoozed entries from `memory/CONFLICTS.md`; block `/done` completion until user resolves or re-snoozes with explicit reason.
3. Invoke `wiki-maintenance` CONSOLIDATE: merge duplicates, archive stale entries to `memory/archive/` (never hard delete per D9), refresh `memory/index.md`.
4. Refresh `memory/hot.md` from last 3 session entries (≤500 words per §0).
5. Append session events to `memory/patterns/PATTERNS.jsonl`. Invoke `pattern-observer` background scan (48–80h window, 3× threshold per §3.5). Surface any new candidates (drafts land in `skills/drafts/` via `pattern-to-skill`).
6. Invoke `sync-coordinator`: snapshot flat `memory/` → `memory/snapshots/<iso>/` with manifest.
7. If `config/PARENT_SYNC.md` enabled and user approves: invoke `parent-sync` skill (filter via `evidence-curator` ≥ medium; run `privacy-guardian` per `PRIVACY.md` mode).
8. Report:
   ```
   Session persisted.
   Decisions added: <N>
   Questions opened: <N>
   Conflicts pending: <N> (snoozed: <N>)
   Pattern candidates: <N> (drafts in skills/drafts/)
   Snapshot: memory/snapshots/<iso>/
   Parent sync: <pushed | skipped | not configured>
   ```
