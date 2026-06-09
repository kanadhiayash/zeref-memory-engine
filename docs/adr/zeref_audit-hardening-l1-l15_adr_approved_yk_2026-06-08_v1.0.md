---
adr_id: zeref-002
title: Audit + Hardening Campaign — L1-L15 (v2.6.1)
status: approved
date: 2026-06-08
owner: yk
classification: internal
supersedes: none
superseded_by: none
---

# ADR-002: Audit + Hardening Campaign — L1-L15

## Context

v2.6.0 shipped 4-gate Auto-Gated Execution (ADR-001). All gates were **prose-only** — no code enforcement. Phase A claim audit (52 claims, `tests/claims-audit-v2.6.md`) graded ~30% of claims as PARTIAL or UNVERIFIED. Phase C security hunt (8 attacks, `tests/security-audit-v2.6-C.md`) surfaced:

- **2 CRITICAL** (V01 gate-spoof — fake `[budget-governor]` line; V02 prompt-injection via `<context>` tag)
- **2 HIGH** (V03 probe-spoof — empty dir at expected path; V04 homoglyph in file paths via R6 verbatim)
- **2 MEDIUM** (V05 silent override of cost-tier mismatch; V06 30s auto-approve race with irreversible ops)
- **2 LOW** (V07 stack fan-out beyond cap; V08 PATTERNS.jsonl event-schema unparsed)

Plus pre-known gaps:
- L1: validator hardcoded `Skills: 10/10` despite 14 dirs on disk
- L2: registry bare model names vs SKILL.md full Anthropic ids
- L4: R6 referenced in only 4 of 14 SKILL.md Safety sections

## Decision

Ship 15 L-items in Phase D after Phase F AskUserQuestion arbitration (4 batches). All recommended paths chosen:

| L# | Surface | Fix |
|---|---|---|
| L1 | `scripts/zeref-validate.py` | Read skill count from `zeref-registry.json`; reports `Skills: 14/14` |
| L2 | `zeref-registry.json` + `_shared/model-resolver.md` | Full Anthropic ids canonical; `model_alias` field preserves bare-name back-compat |
| L3 + V01 | `scripts/zeref-validate.py::lint_patterns_log()` | Parse PATTERNS.jsonl event allowlist + per-event JSON-schema (advisory + lint, not blocking) |
| L4 | 4 original SKILL.md Safety sections | Sweep — add R6 ref to parent-sync, memory-import-export, pattern-to-skill, handoff-compiler |
| L5 + L15 + L14 | `scripts/zeref-validate.py` event allowlist | 11 event types with required + optional payload keys; weight/tier enum checks; stack-cap (≤5) lint |
| L9 + V03 | `skills/fleet-activator/SKILL.md` §Marker-file probe | Per-tool marker (ECC: CLAUDE.md+manifests/; Graphify: SKILL.md frontmatter; etc.) — empty-dir cannot spoof |
| L10 + V02 CRITICAL | `skills/prompt-context-engine/SKILL.md` §Injection filter | Pattern-scan for `ignore prior`/`system:`/`</context>`/role-shift; wrap suspicious content in `<context type="untrusted-input">` + `<sentinel>` |
| L11 + V06 | `skills/prompt-context-engine/SKILL.md` §Irreversibility cool-down | 30s auto-approve → 60s read-only/dry-run only; user reply within 90s window wins |
| L12 + V04 | `skills/caveman-handoff/SKILL.md` §Path normalization + homoglyph guard | NFKC normalize all path strings; flag Cyrillic/Greek/fullwidth lookalikes; require user confirm |
| L13 + V05 | `skills/budget-governor/SKILL.md` §Dual-key override | Single-key "override" rejected; require typed directive + `<override-acknowledged>` block in brief diff |

Plus Memory layer reconciled retroactively (C1 memory-drift root cause): v2.5.0 + v2.6.0 + v2.6.1 logged to `memory/DECISIONS.md`; C1-C5 surfaced; R1-R6 logged with mitigation refs.

## Consequences

**Positive**:
- All Phase C CRITICAL + HIGH + MEDIUM closed
- Validator reports truthful state (Skills 14/14, not 10/10)
- Model versioning explicit (full Anthropic ids → no drift across Anthropic releases)
- R6 coverage 4 → 9 of 14 SKILL.md Safety sections
- PATTERNS.jsonl integrity validator catches malformed events
- Adversarial sandbox failures (probe-spoof, injection, homoglyph) now blocked
- Rubric 8.00 → 9.88 (+1.88 absolute, +23.5% relative)

**Negative**:
- Validator complexity grew (165 → ~300 lines)
- 4 SKILL.md files gained 50-100 line hardening blocks (skill body weight ↑)
- Cost-tier override path now requires dual-key (slightly more friction)
- Cascade-replay test deferred to v2.7 → Execution dim stuck at 9/10 (path to 10.00 documented)

## Alternatives rejected

- **`zeref/gate.py` enforcement module** (Phase F option b): higher cost, new dependency, harder to maintain; advisory+lint sufficient for current threat model.
- **Skip L4 R6 sweep**: would leave 10 SKILL.md Safety sections silent on R6 → R6 enforcement fragile.
- **Defer V05 dual-key**: MEDIUM severity but silent override is exactly the kind of slow leak that compounds; ship now.

## Evidence

- `tests/claims-audit-v2.6.md` — 52 claims, 1 FALSE → L1
- `tests/scores-v2.6-B.csv` — 150 rows, 76% pass; failures map to L9-L12
- `tests/security-audit-v2.6-C.md` — 8 attacks CVSS-scored; all CRITICAL+HIGH+MEDIUM closed
- `tests/zeref-rubric-v2.6.md` — 8-dim re-score 9.88/10
- `CHANGELOG.md` `[2.6.1]` entry — full L-item inventory
- `scripts/zeref-validate.py` — post-update; passes Skills 14/14 + PATTERNS lint 0

## Forward references

- Future ADR-003 — cascade-replay test (path to 10.00 Execution)
- Future ADR-004 — cross-harness validation (ZRF-B07 Cursor/Aider/Gemini, deferred to v2.7)
