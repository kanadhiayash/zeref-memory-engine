---
description: End session. Runs /done logic + clears session overrides + optional handoff compile.
---

1. Run all `/done` steps first.
2. Invoke `sync-coordinator` STOP: clear session permission overrides.
3. If `$ARGUMENTS` includes `--handoff` OR user is switching harnesses: invoke `handoff-orchestrator` COMPILE.
4. Final report:
   ```
   Session ended.
   Snapshot: memory/snapshots/<iso>/
   Session overrides cleared.
   Handoff: <memory/sync/outbound/handoff-<iso>/ | not requested>

   To resume: run /start in a new session.
   ```
