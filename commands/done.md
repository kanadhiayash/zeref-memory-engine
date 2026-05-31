---
description: Persist session work. Writes summary, updates wiki, snapshots state, optionally prepares parent sync.
---

1. Invoke `memory-keeper` WRITE: append session summary to relevant wiki pages (DECISIONS / OPEN_QUESTIONS / RISKS as applicable).
2. Invoke `wiki-maintenance` CONSOLIDATE: merge duplicates, archive stale entries, refresh INDEX.
3. Surface any pending conflicts from `memory/wiki/CONFLICTS.md` — prompt user to resolve or keep snoozed.
4. Invoke `sync-coordinator`: snapshot `memory/wiki/` → `memory/snapshots/<iso>/` with manifest.
5. If `config/PARENT_SYNC.md` enabled and user approves: invoke `parent-sync` skill.
6. Report:
   ```
   Session persisted.
   Decisions added: <N>
   Questions opened: <N>
   Conflicts pending: <N> (snoozed: <N>)
   Snapshot: memory/snapshots/<iso>/
   Parent sync: <pushed | skipped | not configured>
   ```
