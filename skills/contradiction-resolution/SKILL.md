---
name: contradiction-resolution
description: Manages contradiction queue. Activates when memory-keeper flags a conflict. Surfaces to user, supports snooze-until-/done, never silent-resolves.
trigger:
  - memory-keeper emits conflict
  - user says "review conflicts"
model: claude-sonnet-4-6
max_turns: 20
status: M2-stub
---

# contradiction-resolution

## Status

**M2 stub** — full implementation lands in v4.1.0. M1 ships this file as a placeholder.

## Mission (target)

When two claims conflict, surface both sides with provenance and let the user arbitrate. Never silently resolve.

## Flow (target)

1. Receive conflict from `memory-keeper`
2. Read both sides from `memory/wiki/CONFLICTS.md`
3. Get evidence grades from `evidence-curator` for both sides
4. Surface to user:
   ```
   CONFLICT C[N]
   Side A: [claim] (evidence: high, source: ...)
   Side B: [claim] (evidence: medium, source: ...)
   Resolve now? Snooze until /done? Mark both valid (context-dependent)?
   ```
5. On resolution:
   - Move resolved entry to `DECISIONS.md` with both-sides provenance
   - Remove from `CONFLICTS.md`
   - Log `{"event": "conflict-resolved", "payload": {"conflict_id": "C[N]", "winner": "A|B|both", "user_ts": "..."}}`

## Safety

- Never auto-resolve based on evidence grade alone
- Snoozed conflicts surface again at next `/done` automatically
