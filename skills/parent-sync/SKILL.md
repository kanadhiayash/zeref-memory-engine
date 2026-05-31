---
name: parent-sync
description: Stages approved summaries and decisions to memory/sync/outbound/, pushes to parent project's memory/sync/parent/<child-id>/. Activates on approved /stop or /sync-parent.
trigger:
  - approved /stop with parent sync enabled
  - /sync-parent
model: claude-sonnet-4-6
max_turns: 20
status: M2-stub
---

# parent-sync

## Status

**M2 stub** — full implementation lands in v4.1.0.

## Mission (target)

Push approved child project state up to a parent project. Preserve provenance. Surface conflicts at parent.

## Flow (target)

1. Read `config/PARENT_SYNC.md` — verify enabled + parent_path valid
2. Get content from `memory/wiki/` per `push_content:` config (summary, decisions, risks, open_questions)
3. Filter via `evidence-curator`: only grade ≥ medium
4. Pass through `privacy-guardian` per current mode
5. Stage in `memory/sync/outbound/<iso>/`
6. Show user the staging contents — require explicit approval
7. On approval: copy to `<parent_path>/memory/sync/parent/<child-id>/<iso>/`
8. Append provenance manifest: `{child_id, ts, source_events: [hash1, hash2, ...]}`
9. Log `{"event": "parent-sync-pushed", "target": "...", "payload": {...}}`

## Conflicts at parent

If pushed content conflicts with parent's existing decisions, parent's `memory-keeper` writes to parent's `CONFLICTS.md` on next parent `/start`.

## Safety

- Push requires explicit user approval every time (no auto-push)
- Pushed content is read-only at parent until parent's `memory-keeper` ingests it
