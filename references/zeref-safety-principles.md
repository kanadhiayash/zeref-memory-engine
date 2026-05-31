# Zeref 4.0 Safety Principles

**Shared reference — used by all skills and agents.**

These rules exist not as arbitrary restrictions but because Zeref handles persistent project memory across long horizons. A mistake here erases knowledge that took weeks to build.

---

## Rule 1 — Single writer to memory/wiki/
**Why**: Concurrent writes cause silent data loss and corrupt INDEX consistency.
**What**: Only `memory-keeper` writes to `memory/wiki/`. Any other agent attempting to write triggers a block + violation log event.

## Rule 2 — Append-only logs
**Why**: Mutable logs destroy audit trail. Migration, debugging, and pattern detection all depend on event immutability.
**What**: `memory/logs/session-events.jsonl` is append-only. Never edit existing lines. Never delete the file. Rotate by snapshotting, never by truncating.

## Rule 3 — Privacy mode enforcement before every write
**Why**: A single accidental write of credentials or sensitive paths poisons the wiki and any downstream sync.
**What**: Every payload passes through `privacy-guardian` before reaching `memory-keeper`. Always-block patterns (credentials, .gitignore contents) reject regardless of mode.

## Rule 4 — Contradictions never silently resolved
**Why**: Silent resolution destroys both sides of a real disagreement and erodes user trust in the wiki as canonical state.
**What**: When `memory-keeper` detects a conflict, both sides go to `CONFLICTS.md`. User arbitrates. `contradiction-resolution` skill orchestrates.

## Rule 5 — Boundary-first reads
**Why**: Loading full wiki pages on every operation blows the token budget and defeats progressive activation.
**What**: Always read `memory/wiki/INDEX.md` first. Find the relevant domain. Read only the named section of the named page.

## Rule 6 — Irreversible actions require explicit confirmation
**Why**: Destructive operations (file deletion outside ARCHIVE, force-push, dropping permissions) cannot be undone from inside Zeref.
**What**: Always prompt the user with the exact action + target + consequence before executing. Never infer approval from session context.

## Rule 7 — Evidence is graded, not inferred
**Why**: Unverified assumptions silently elevated to "fact" cause downstream decisions to compound on bad ground.
**What**: Every wiki entry carries an evidence grade (high / medium / low). `evidence-curator` re-grades on staleness. User remains the arbiter.

## Rule 8 — Never invent
**Why**: Hallucinated provenance, source references, or user metrics poison the wiki permanently.
**What**: When uncertain, label `[ASSUMPTION]`, `[UNKNOWN]`, `[RISK]`. Never present inference as fact. Preserve exact commands, paths, URLs, errors verbatim.

## Rule 9 — Review-first skill extension
**Why**: Auto-activating drafted skills creates a feedback loop where the agent invents its own scope creep.
**What**: `pattern-to-skill` only drafts. `/review-skill` is the only path from `skills/_drafts/` to `skills/`.

## Rule 10 — Honest limits declared publicly
**Why**: Overpromised capabilities erode trust when reality disappoints. Better to declare what Zeref doesn't do.
**What**: Three honest limits in README:
1. No real-time collaborative merge
2. No hosted backend
3. No silent semantic conflict resolution (feature, not bug)

---

## Evidence discipline (every output)

```
Facts (verified this session):
Assumptions (labeled [ASSUMPTION: ...]):
Unknowns ([UNKNOWN: not verified]):
Risks ([RISK: potential failure]):
```
