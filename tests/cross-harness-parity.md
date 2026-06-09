# Cross-Harness Parity — ZRF-B07

**Date:** 2026-06-03 | **Target:** ZRF-B07 ≤10% drift across harnesses
**Status:** Baseline established. Live parity runs: Sprint 3 deploy.

---

## Harnesses Under Test

| Harness | Stub file | Status |
|---|---|---|
| Claude Code | `CLAUDE.md` | Primary — all tests run here |
| Cursor | `.cursor/rules/zeref.mdc` | Stub exists; parity pending |
| Aider | `.aider.conf.yml` | Stub exists; parity pending |
| Gemini CLI | `GEMINI.md` | Stub exists; parity pending |
| Codex | (no stub) | Out of scope Sprint 3 |

---

## Parity Test Matrix

### P01 — §0 Reading Order Compliance

**Test:** On `/start` with empty hot.md, does harness follow steps 0-8 in order?

| Harness | Steps 0-8 | SOUL.md (step 0) |
|---|---|---|
| Claude Code | 8/8 ✔ | ✔ |
| Cursor | untested | untested |
| Aider | untested | untested |
| Gemini | untested | untested |

### P02 — Skill Activation (3 skills)

**Test:** Do zeref-registry.json trigger phrases fire the correct skill?

| Trigger | Expected skill | Claude Code | Cursor | Aider |
|---|---|---|---|---|
| "update wiki" | wiki-maintenance | ✔ | untested | untested |
| "grade this claim" | evidence-grader | ✔ | untested | untested |
| "set up project" | project-setup | ✔ | untested | untested |

### P03 — Privacy Gate on Write

**Test:** Decision with PII — does privacy-guardian intercept before disk write?

| Harness | Intercepts PII | zeref.privacy available |
|---|---|---|
| Claude Code | ✔ (spec + module) | ✔ Sprint 2 |
| Cursor | untested | untested |
| Aider | untested | untested |

### P04 — /done Sequence

**Test:** Does `/done` produce: hot.md refresh + PATTERNS.jsonl append + conflict scan?

| Harness | hot.md | PATTERNS.jsonl | conflict scan |
|---|---|---|---|
| Claude Code | ✔ | ✔ | ✔ |
| Cursor | untested | untested | untested |

---

## Gaps

| Gap | Severity | Sprint |
|---|---|---|
| Cursor .mdc no test suite | MEDIUM | Sprint 3 live |
| Aider no test procedure | MEDIUM | Sprint 3 live |
| GEMINI.md not validated vs AGENTS.md §0 | MEDIUM | Sprint 3 live |
| Codex stub absent | LOW | Sprint 4 |

---

## Methodology

1. Load `AGENTS.md` + relevant skill spec into target harness
2. Run trigger phrase as user input
3. Grade output against 6-dimension rubric
4. Compare weighted score to Claude Code baseline
5. Flag as drift if delta > 0.5 on any single dimension

## ZRF-B07 Current Status

| Metric | Value |
|---|---|
| Claude Code baseline | avg 4.63 weighted, 20/20 tasks |
| Cross-harness tested | 0/3 harnesses (pending live runs) |
| Drift threshold | ≤0.46 weighted delta (10% of 4.63) |
| Status | **DEFER** — needs live harness access |
