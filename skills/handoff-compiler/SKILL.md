---
name: handoff-compiler
description: Produces compact cross-model/cross-harness handoff package. Invoked by handoff-orchestrator on /stop or model switch.
trigger:
  - handoff-orchestrator invokes
  - /stop with handoff requested
  - user says "handoff to ..."
model: claude-sonnet-4-6
max_turns: 15
---

# handoff-compiler

## Mission

Compress current project state into a package that any harness/model can pick up.

## Output package

Written to `memory/sync/outbound/handoff-<iso>/`:

### `SUMMARY.md` (target ≤ 1500 tokens)
- Project name + 1-line description
- Last 3 decisions (titles only)
- Top 3 open questions
- Active conflicts (titles only)
- Next recommended action

### `STATE.json` (machine-readable)
```json
{
  "schema_version": "1.0",
  "project_name": "...",
  "exported_at": "ISO-8601 UTC",
  "last_event_cursor": "sha256:...",
  "active_decisions_count": 12,
  "open_questions_count": 3,
  "active_conflicts_count": 0,
  "model_tier_recommended": "sonnet",
  "privacy_mode": "exact"
}
```

### `NEXT.md`
1-page: what the next session should do first. Concrete instruction, not abstract intent.

## Flow

1. Read INDEX + DECISIONS (recent) + OPEN_QUESTIONS + CONFLICTS
2. Read session events from current session
3. Pass everything through `privacy-guardian` per current mode
4. Compile to package
5. Write to `memory/sync/outbound/handoff-<iso>/`
6. Log `{"event": "handoff-compiled", "target": "..."}`

## Safety

- Target ≤ 1500 tokens for SUMMARY.md (the always-on portion)
- Never include credentials or `.gitignore`-matched content
- Respect privacy mode
