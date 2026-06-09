# Pattern Detection

Zeref OS extends itself **only via review-first drafts**. The loop:

```
session events → PATTERNS.jsonl → pattern-observer (background scan)
    → 48-80h rolling window, Jaccard ≥0.8, ≥3 occurrences
    → cluster + score → top-3 surfaced per scan
    → pattern-to-skill drafts SKILL.md to skills/drafts/
    → user reviews via /review-skill (approve/edit/reject/defer)
    → approved drafts promoted to skills/<name>/ via git mv (preserves history)
```

Never auto-activated. Per Core Principle 10 (Review-First Extension).

## Two-Strikes Rule (Core Principle 11)

**Do not codify a rule on the first occurrence of an error.** Wait for the second.

| Occurrence | Action |
|---|---|
| First | Log to `memory/MEMORY.md` as a trap noticed |
| Second | Promote to a rule — codify in `_shared/rules.md`, agent prompt, or new skill |

**Why**: Premature codification creates brittle rules that don't generalize. Two occurrences = pattern; one = noise.

**v2.6.1 example**: C1 memory drift (ship cycles without `wiki-maintenance`) — first occurrence logged to `memory/MEMORY.md`. Second occurrence will trigger automation requirement (auto-fire wiki-maintenance on `/stop`).

See [`references/two-strikes-rule.md`](https://github.com/kanadhiayash/zeref-os/blob/main/references/two-strikes-rule.md) for full doctrine.

## `pattern-observer` algorithm

Per AGENTS.md + skill spec:

1. **Window**: rolling 48-80h scan of `memory/patterns/PATTERNS.jsonl`
2. **Task signature**: verb + subject + 3-gram qualifiers (stop-words stripped)
3. **Similarity**: Jaccard 3-gram ≥ 0.8 over qualifier sets
4. **Clustering**: union-find; discard clusters < 3 members
5. **Scoring**: `frequency × (1 / recency_span_hours)` (favors dense recent repetition)
6. **Output**: top-3 by score per scan → `memory/sync/outbound/patterns/<cluster-id>.json`
7. **Dedupe**: by `cluster_id`; update existing candidates with new members
8. **Quiet hours**: rest logged as suppressed (no overflow)
9. **Activation**: `/done`, `/stop`, `/status`, manual
10. **Background only**: never blocks active work

User can disable via `config/BUDGET.md` `pattern_detection: false`.

## `pattern-to-skill` workflow

When a candidate cluster surfaces:

1. **DRAFT** operation:
   - Load candidate JSON
   - Synthesize metadata: `name`, `description`, `trigger`, `model`, `max_turns`
   - Synthesize body: mission, when-to-use, operations, safety
   - Write `skills/drafts/<name>/SKILL.md`
   - Write immutable `skills/drafts/<name>/PROVENANCE.md` (cites every source event by hash)
   - **v2.6.1 R6**: PROVENANCE.md must preserve every entity that contributed to the pattern (tool names, file paths, repeated arguments)
2. **REVIEW QUEUE** (`/review-skill`):
   - Lists pending drafts with score + event count + description
3. **Per-draft prompt**:
   - Show frontmatter + body + provenance summary
   - 4 actions:
     - **approve** → `git mv skills/drafts/<name>/ skills/<name>/`; strip draft markers; log to DECISIONS.md
     - **edit** → open file in editor; re-prompt after save
     - **reject** → prompt reason; `rm -rf` draft dir; mark candidate JSON `rejected_at`
     - **defer** → leave in place; increment counter; auto-prompt again after 3 defers

PROVENANCE.md is **immutable** — never edited after creation. Approval doesn't touch it.

## Validator integration

`scripts/zeref-validate.py` surfaces drafts as warnings:

```
Warnings:
  ! skills/drafts/ contains 1 pending draft(s) — run /review-skill
```

Validator does NOT block on drafts. Drafts are read-only artifacts until promoted.

## v2.6.1 example: `grep-with-context` draft

Single draft currently in `skills/drafts/grep-with-context/` (v2.5 L8 dogfood). Demonstrates the full pipeline:
- 4 events in `PATTERNS.jsonl` with `event: grep-with-context, action: "grep -r -B2 -A2 trigger"` clustered together
- `pattern-observer` surfaced cluster (score > threshold)
- `pattern-to-skill` drafted SKILL.md with PROVENANCE
- Awaits user `/review-skill` decision

## What triggers a candidate?

Examples of patterns the system would surface:
- Repeated `grep -r --include` over `skills/` (3+ in 24h) → draft `skill-search` skill
- Repeated PII regex addition to `REDACT.md` (4 distinct patterns added) → draft `redact-helper` skill
- Repeated tier-override (5 instances of `CRITICAL on HAIKU`) → suggest reclassifying CRITICAL or accepting Haiku for that workload (v2.6.1 L13 dual-key triggers this)
- Repeated `wiki-maintenance` skip on ship cycles → trigger memory-drift remediation (C1)

## Safety + anti-patterns

- **Never auto-activate**: review-first per Core Principle 10
- **Never overwrite PROVENANCE**: immutable per `pattern-to-skill` spec
- **Never delete rejected candidates**: mark `rejected_at` in JSON for future revisit (R2 non-deletion)
- **Never surface candidates that share signature with a user-rejected one** within retention window
- **R6 (v2.6.1)**: draft must preserve every entity from PATTERNS source events

## Related

- [[Memory-Model]] — PATTERNS.jsonl schema + 11 event types
- [[Architecture]] — `pattern-observer` agent + `pattern-to-skill` skill
- [[Glossary]] — Two-Strikes Rule, pattern signature, cluster_id
- [`references/two-strikes-rule.md`](https://github.com/kanadhiayash/zeref-os/blob/main/references/two-strikes-rule.md)
