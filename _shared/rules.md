# Zeref OS — Shared Rules

Rules repeated across ≥3 skills, extracted here to reduce drift. Reference this file from individual SKILL.md Safety sections as "per `_shared/rules.md`."

---

## R1 — Single-Writer + Privacy Gate

**All writes to `memory/` must pass through `memory-keeper` → `privacy-guardian`.**

No skill writes directly. The chain is always:

```
skill output → memory-keeper (conflict check, single-write lock) → privacy-guardian (PRIVACY.md mode + REDACT.md classes) → disk
```

Applies to: wiki-maintenance, project-setup, contradiction-resolution, handoff-compiler, memory-import-export, parent-sync, pattern-to-skill.

---

## R2 — Non-Deletion (D9)

**Archive content; never hard-delete.**

- Superseded items are marked `[SUPERSEDED]` with a timestamp — they are never removed.
- Consolidated content moves to `memory/archive/` via copy-then-mark, not rename-then-delete.
- `memory/patterns/PATTERNS.jsonl` is append-only — no line ever removed.

Applies to: wiki-maintenance, budget-governor, contradiction-resolution, memory-import-export, parent-sync.

---

## R3 — Privacy Gate on External Output

**Before any external output or sync, pass the full payload through `privacy-guardian`.**

External = outbound to parent project, handoff package, MCP connector, or any tool outside the local `memory/` tree.

Reading `PRIVACY.md` mode and `REDACT.md` classes is not enough — the payload must actually be rewritten by `privacy-abstraction` when mode = `abstract`, and blocked when mode = `local-only`.

Applies to: handoff-compiler, memory-import-export, parent-sync, pattern-to-skill.

---

## R4 — Never Invent

**When a field value is unknown or the user declines to answer, leave it blank with a `# TODO` marker. Never fabricate.**

This applies to config fields, evidence grades, decision provenance, and any metadata field in `memory/`.

Applies to: project-setup, evidence-grader, contradiction-resolution, memory-import-export.

