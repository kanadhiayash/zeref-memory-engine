# Memory Model

> Imagine handing a six-month-old project to a brand-new collaborator. Where do they read first? What do they read second? When do they stop? Zeref OS answers those three questions with files on disk.

Zeref OS stores everything in plain markdown under `memory/`, with append-only event logs and snapshots. Single-writer enforced via `memory-keeper` agent (per shared rule R1). PATTERNS.jsonl event schema is validator-checked.

_Placeholder: `assets/poc-memory-tree.png` — real per-project memory tree on disk._

## Flat layout

```
memory/
├── hot.md                   ← last 3 sessions, ≤500 words (read FIRST per AGENTS.md §0)
├── index.md                 ← domain index (read if hot insufficient)
├── MEMORY.md                ← agent-written session notes (NOT human-edited)
├── DECISIONS.md             ← confirmed decisions w/ provenance + evidence grade
├── OPEN_QUESTIONS.md        ← unresolved questions w/ owner
├── RISKS.md                 ← identified risks w/ severity
├── CONFLICTS.md             ← contradiction queue (user arbitrates)
├── glossary.md              ← project-specific term definitions
├── projects/                ← per-sub-project context (if multi-project repo)
├── patterns/
│   └── PATTERNS.jsonl       ← append-only event log; schema-validated
├── snapshots/<iso>/         ← point-in-time wiki state + manifest
├── archive/                 ← superseded snapshots (never deleted per R2)
├── raw/                     ← untouched source material
└── sync/
    ├── outbound/            ← staged parent updates
    └── parent/              ← received parent updates
```

## Boundary-first reading

The "boundary file" pattern prevents unbounded reads:

1. **First**: read `memory/hot.md` (≤500 words, current context)
2. **Second**: read `memory/index.md` if hot is insufficient — find the relevant domain row
3. **Third**: read only the named section of the named page
4. **Never**: load a full page just to scan it

This caps always-on context to ~3-4k tokens regardless of project age.

## Single-writer (R1) + privacy gate (R3)

All writes flow:

```
skill output
    ↓
memory-keeper (conflict detect, advisory lock via zeref/lock.py)
    ↓
privacy-guardian (PRIVACY.md mode + REDACT.md classes + SHARING_POLICY.md allowlist)
    ↓
disk (with PII scrub)
```

No skill writes to `memory/` directly. Concurrent writes blocked by `zeref/lock.py::MemoryLock`. Atomic write semantics via `atomic_write` / `atomic_append`.

## Contradiction handling

When `memory-keeper` detects a conflict:

1. Halt write
2. Subject/predicate/value fingerprint match against DECISIONS / OPEN_QUESTIONS / RISKS
3. Append both sides to `memory/CONFLICTS.md`
4. Surface to user immediately OR snooze until `/done` (user choice)
5. User arbitrates (via `contradiction-resolution` skill) — never silent
6. Resolved entry moves to `memory/DECISIONS.md` with both-sides provenance

**4 anti-patterns refused**: recency-wins · grade-wins · silent-drop · indefinite-snooze.

## PATTERNS.jsonl event schema

Append-only event log. Every event is a single JSON line:

```jsonl
{"ts":"2026-06-08T14:00:00Z","agent":"memory-keeper","event":"wiki-write","target":"memory/DECISIONS.md","payload":{"summary":"..."},"hash":"sha256:...","evidence_grade":"high"}
```

**Allowlisted event types** (validated by `scripts/zeref-validate.py::lint_patterns_log()`):

| Event | Required payload | Optional payload |
|---|---|---|
| `wiki-write` | summary | — |
| `session-start` | — | trigger, scope, budget_ceiling_usd, team, force_multipliers |
| `memory-drift-detected` | finding | — |
| `budget-gate` | weight, tier, match | est_cost_usd, budget_remaining_usd, override_reason |
| `skill-route` | domain, lead, support, qa | ext |
| `tool-probe` | tool, reachable | path, fallback, marker_verified |
| `prompt-gate` | classification | restructured, brief_tokens, stripped_context_tokens, injection_detected |
| `handoff-compress` | original_tokens, compressed_tokens, ratio | model_from, model_to, harness_from, harness_to |
| `tier-change` | from, to | — |
| `grep-with-context` | — | action |
| `log-cutover` | — | from, to, note |

**Value enums** (enforced):
- `weight` ∈ {CRITICAL, HIGH, MEDIUM, LOW}
- `tier` ∈ {OPUS, SONNET, HAIKU, OPUS-equivalent, SONNET-equivalent, HAIKU-equivalent}

**Hard constraints**:
- `skill-route` with stack > 5 → lint error
- `budget-gate` with `(CRITICAL, HAIKU)` or `(LOW, OPUS)` unless `match=OVERRIDE` → lint error

## Pattern detection (per `pattern-observer`)

Background scan of `PATTERNS.jsonl` over rolling 48–80h window:

- Task signature: verb + subject + 3-gram qualifiers
- Jaccard similarity ≥ 0.8 over qualifier 3-gram sets
- Union-find clustering; discard clusters < 3 members
- Scoring: `frequency × (1 / recency_span_hours)`
- Top-3 by score per scan; rest logged as suppressed
- Emits candidates → `pattern-to-skill` (review-first)

Activation: `/done`, `/stop`, `/status`, manual. Background only — never blocks active work.

## Snapshots

On `/done`, full `memory/` state copied to `memory/snapshots/<iso>/` with `manifest.json`. Never deleted (R2 non-deletion). Used by `parent-sync` for rollback + by `memory-import-export` for backup.

## Parent sync (multi-project rollup)

Per `parent-sync` skill:

1. **STAGE**: filter via `evidence-curator` (≥medium); pass through `privacy-guardian`; write to `memory/sync/outbound/<iso>/` with `manifest.json`
2. **APPROVE**: explicit user confirmation with preview
3. **PUSH**: copy to `<parent_path>/memory/sync/parent/<child_id>/<iso>/`; chmod 444; log PUSHED
4. **PARENT INGEST**: parent's `/start` runs conflict detection on incoming entries
5. **ROLLBACK**: via provenance pointers
6. **R6**: every staged entity must survive verbatim into parent; re-diff after privacy-abstraction

`local-only` privacy mode blocks all parent sync.

## Always-on context budget

Per `budget-governor`:

| Tier | Per-skill cap | Behavior |
|---|---|---|
| HAIKU | 4 000 tok | Aggressive compaction, minimal wiki writes |
| SONNET | 8 000 tok | Normal operation, full wiki writes |
| OPUS | 16 000 tok | Full parent-child sync, deep conflict analysis |

`warn_at_tokens` (default 50000) → consolidation suggested. `hard_cap_tokens` → blocks writes; forces `/done`.

## Validation

```bash
python3 scripts/zeref-validate.py
# Skills:           14/14 (from zeref-registry.json)
# Memory layout:    flat
# PATTERNS lint:    0 finding(s)
# ✔ Validation passed
```

## Related

- [[Privacy-Model]] — modes + classes + connectors
- [[Pattern-Detection]] — Two-Strikes Rule + drafting
- [[Architecture]] — agents + skills + 4-gate chain
- [[Glossary]] — boundary file, evidence grade, R6, gate event types
- [`_shared/rules.md`](https://github.com/kanadhiayash/zeref-memory-engine/blob/main/_shared/rules.md) — R1-R6
