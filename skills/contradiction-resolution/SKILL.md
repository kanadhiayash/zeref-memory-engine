---
name: contradiction-resolution
description: Detects conflicting claims in wiki state, surfaces them via CONFLICTS.md, supports snooze-until-/done, never silent-resolves. User arbitrates every conflict.
trigger:
  - memory-keeper detects conflict during write
  - /done — surface snoozed conflicts
  - user says "review conflicts"
model: claude-sonnet-4-6
max_turns: 25
---

# contradiction-resolution

## Mission

When two claims conflict, surface both sides with provenance. User decides. Never silent resolution.

## What counts as a conflict

| Type | Example |
|---|---|
| **Direct negation** | "DB is Postgres" vs "DB is MySQL" |
| **Mutually exclusive** | "Ship Friday" vs "Ship next Monday" |
| **Quantitative drift** | "Budget $50k" vs "Budget $80k" — flag if delta > 20% |
| **Decision supersession** | New decision contradicts existing decision still marked active |
| **Source disagreement** | Two pushed-in claims from different sources disagree |

Not a conflict:
- Refined detail (more specific version of same fact)
- Status update (open → resolved)
- Same claim with stronger evidence

## DETECT (called by memory-keeper before write)

1. Compute fingerprint of incoming claim:
   - subject (extracted noun phrase)
   - predicate (verb + complement)
   - quantitative value (if any)
2. Scan `memory/wiki/DECISIONS.md`, `OPEN_QUESTIONS.md`, `RISKS.md` for matching subjects
3. If match found AND predicate/value conflicts per types above → CONFLICT
4. Emit to `memory-keeper`: `{"verdict": "conflict", "side_a_id": "...", "side_a_hash": "...", "side_b_payload": {...}}`
5. If no match → pass-through (proceed with write)

## QUEUE (called by memory-keeper after conflict detected)

1. Halt original write
2. Append to `memory/wiki/CONFLICTS.md`:
   ```
   ### C<N> — <iso-date> — <conflict-title>
   **Status**: open
   **Side A**: <claim-a> (evidence: <grade>, source: <hash>, ts: <iso>)
   **Side B**: <claim-b> (evidence: <grade>, source: <hash>, ts: <iso>)
   **Detected by**: memory-keeper, event-hash <hash>
   **Resolution**: <blank>
   ```
3. Log: `{"event": "conflict-queued", "target": "memory/wiki/CONFLICTS.md", "payload": {"conflict_id": "C<N>"}}`
4. Surface to user immediately:
   ```
   ⚠ CONFLICT detected: <title>
   A: <side-a-short>
   B: <side-b-short>
   Resolve now? [now / snooze-until-done / both-valid]
   ```

## SNOOZE

User picks `snooze-until-done`:
1. Mark conflict status → `snoozed-until-done`
2. Append `**Snooze reason**: <user-input>` to CONFLICTS.md entry
3. Conflict re-surfaces at next `/done` automatically

## RESOLVE

User picks `now` and selects winner (A / B / both / merge):

### Single winner (A or B)
1. Move winning claim to `DECISIONS.md` with both-sides provenance:
   ```
   ### <iso-date> — <decision-title>
   **Decided**: <winning-claim>
   **Why**: <user-reasoning>
   **Evidence**: <grade>
   **Provenance**: resolved conflict C<N> — sides: <hash-a>, <hash-b>; user-ts: <iso>
   **Supersedes**: <hash-loser>
   ```
2. Mark loser entry in source page as `[SUPERSEDED by C<N>]` (do not delete)
3. Update `CONFLICTS.md` entry → status `resolved`, fill `Resolution:` line
4. Log: `{"event": "conflict-resolved", "payload": {"conflict_id": "C<N>", "winner": "A|B", "user_ts": "..."}}`

### Both valid (context-dependent)
1. Move both to `DECISIONS.md` with discriminating context (e.g. "in dev: A; in prod: B")
2. Update `CONFLICTS.md` entry → status `resolved` with `winner: both-context-dependent`
3. Log: `{"event": "conflict-resolved-both", ...}`

### Merge
1. Compose synthesis claim from both sides
2. Move to `DECISIONS.md` with both-sides provenance + `Synthesis:` marker
3. Log: `{"event": "conflict-resolved-merge", ...}`

## SNOOZED REVIEW (called by /done)

1. Scan `CONFLICTS.md` for entries with status `snoozed-until-done`
2. For each, surface to user with same prompt as DETECT
3. Block `/done` completion until user processes each (either resolves or re-snoozes with explicit reason)

## EVIDENCE GRADE COMPARISON

When surfacing conflict, request evidence grades from `evidence-curator` for both sides. Display in prompt:
```
A: <claim> [evidence: high — verified this session]
B: <claim> [evidence: medium — assumed from 30-day-old source]
```
**Never auto-resolve based on grade alone.** Grade is advisory only.

## Safety

- Never silent resolution
- All resolutions logged to event log
- Loser claims marked `[SUPERSEDED]` but never deleted (auditability)
- Snoozed conflicts always re-surface at `/done` — cannot escape arbitration indefinitely
- If user attempts to `/stop` with open conflicts, warn and require explicit acknowledgment

## Anti-patterns to refuse

- Auto-resolve based on recency alone ("newest wins") → REFUSE
- Auto-resolve based on evidence grade alone → REFUSE
- Silently drop loser without `[SUPERSEDED]` mark → REFUSE
- Allow indefinite snooze across multiple `/done` cycles without user intervention → REFUSE (warn after 3 snoozes)
