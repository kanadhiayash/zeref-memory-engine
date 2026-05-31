---
description: End session. Runs /done logic + clears session overrides + optional handoff compile + optional parent sync prompt.
---

1. Run all `/done` steps first (including pattern scan + hot.md refresh + snapshot).
2. Invoke `sync-coordinator` STOP: clear session permission overrides; restore defaults from `config/PERMISSIONS.md` + `SHARING_POLICY.md`.
3. If `config/PARENT_SYNC.md` enabled AND events from this session qualify (per `evidence-curator` ≥ medium): prompt "Push to parent? [yes / no]". If yes → invoke `parent-sync` (STAGE → APPROVE → PUSH).
4. If `$ARGUMENTS` includes `--handoff` OR user is switching harnesses: invoke `handoff-orchestrator` COMPILE (writes `handoff/SUMMARY.md` + `STATE.json` + `NEXT.md` + `HARNESS-MAP.md` to `memory/sync/outbound/handoff-<iso>/`).
5. Final report:
   ```
   Session ended.
   Snapshot: memory/snapshots/<iso>/
   Session overrides cleared.
   Parent sync: <pushed | skipped | not configured>
   Handoff: <memory/sync/outbound/handoff-<iso>/ | not requested>

   To resume: run /start in a new session.
   ```
