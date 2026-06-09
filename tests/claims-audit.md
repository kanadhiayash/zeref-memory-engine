# Phase A — Claim Inventory + Evidence Grading

**Date:** 2026-06-04 | **Auditor:** Zeref OS audit team
**Method:** Manual claim extraction → 6-dim rubric grading → composite grade (HIGH/MEDIUM/LOW) → status (VERIFIED/PARTIAL/UNVERIFIED/FALSE)
**Source:** AGENTS.md, SOUL.md, zeref-registry.json, _shared/rules.md, 10 SKILL.md, CHANGELOG.md, PRIVACY/REDACT/SHARING_POLICY.md, config/*, references/*, team-packs/*, zeref/*.py, scripts/zeref-validate.py, pyproject.toml, tests/*

---

## Tally

| Metric | Count | % |
|---|---|---|
| Total claims | **85** | 100% |
| VERIFIED | 42 | 49% |
| PARTIAL | 29 | 34% |
| UNVERIFIED | 11 | 12% |
| **FALSE** | **3** | **3%** |

**Grades:** HIGH 31 · MEDIUM 50 · LOW 4

**Exit criteria:**
- ≥80 claims graded: **85 ≥ 80** ✔
- ≥3 contradictions surfaced: **5 (3 FALSE + 4 LOW)** ✔

---

## Contradictions (priority queue → `memory/CONFLICTS.md`)

### CRITICAL

**K1 — C61 (FALSE / HIGH grade):** `config/PROJECT.md` claims `project_name` and `project_root` populated. **Reality:** both blank. Zeref OS has never been `/start`-ed against itself. Self-dogfood failure. → Fix Phase D L6.

**K2 — C40 (FALSE / LOW grade):** `privacy-abstraction` has 1 trigger phrase. Violates SOUL principle 3 (Contracts Over Prose). Most safety-critical skill has weakest trigger spec. → Fix Phase D (trigger rewrite).

**K3 — C70 (FALSE / LOW grade):** `zeref init` advertised in CHANGELOG ("bootstraps fresh `memory/` layout"). **Reality:** not implemented in `zeref/cli.py`. False advertising. → Fix Phase D L5.

### HIGH (UNVERIFIED with LOW provenance)

**K4 — C05:** "Single-writer per resource — only memory-keeper writes" is prose-only. No file lock, no mutex, no advisory sentinel. → Fix Phase D L9.

**K5 — C20:** "Every write to memory/ and external transmission passes through privacy-guardian." Spec assertion with zero enforcement code. `zeref/privacy.py` exists but not auto-invoked on memory-keeper writes. → Fix Phase B (instrument) + Phase D (lock hook).

---

## VERIFIED Highlights

| Claim | Evidence |
|---|---|
| C01 Local-first | memory/ tree all .md; no DB primary |
| C13/C14/C15/C16 inventory | 6 agents, 10 skills, 8 commands, flat memory — validator green |
| C17/C18/C19 privacy templates | PRIVACY mode `abstract`, 6 REDACT classes, SHARING_POLICY all OFF |
| C22 Privacy-Deterministic | `zeref/privacy.py` shipped |
| C23 Contracts Over Prose | `zeref-registry.json` shipped |
| C26 Structured Memory | `zeref/db.py` tested |
| C31/C32/C33 trigger precision | 9/8/8 concrete phrases (3 of 10 skills) |
| C43 score rows | 40 rows across 2 versions |
| C46 demo offline | 20/20 PASSED verified |
| C48/C49 privacy classes | credentials always-on; 7 built-in regexes |
| C56 validator green | scripts/zeref-validate.py passes |
| C64 connectors OFF | github/linear/notion all `enabled: false` |
| C76 team packs | 6 .md files present |

---

## PARTIAL Patterns (Phase B+C focus)

29 PARTIAL claims fall into three buckets:

1. **Trigger debt** (C34-C39, C84): 7 of 10 skills still have original 2-3 vague triggers. Sprint 1 only fixed 30% of registry.
2. **Prose-only enforcement** (C02, C06-C09, C24, C27, C53-C55): runtime guarantees rest on harness compliance + LLM behavior.
3. **Live-untested workflows** (C10, C12, C42, C45, C72, C74, C77): pattern-to-skill, cross-harness, packaging install, team-packs activation.

---

## Methodology

- **Grade composite:** HIGH if avg(recency, provenance, corroboration) ≥ 1.7 on 2-pt scale; LOW if < 0.8; else MEDIUM. Same logic as `zeref/cli.py cmd_grade`.
- **Status mapping:**
  - VERIFIED = HIGH grade + artifact found in repo
  - PARTIAL = MEDIUM grade + spec/code partial overlap
  - UNVERIFIED = MEDIUM grade + no test/exercise yet
  - FALSE = claim contradicted by repo state
- **Skills deferred** (would inflate cost; manual extraction sufficient for 85 claims):
  - `/graphify` — defer to v3.0 if graph traversal becomes needed
  - `/ecc:agent-eval` — reserved for Phase B per-skill rubric
  - `/ecc:eval-harness` — reserved for Phase B test-code generation

---

## Hand-off to Phase B

- **Skills to stress-test first** (lowest claim grades): privacy-abstraction (C40), parent-sync (C38), pattern-to-skill (C10/C39), contradiction-resolution (C04/C34)
- **Risk-weighted order:** privacy-abstraction > pattern-to-skill > parent-sync > contradiction-resolution > rest
- **Inputs to inject:** PII payloads (homoglyph, base64), conflicting decisions, synthetic high-frequency PATTERNS.jsonl events
- **Output:** `tests/scores-vB.csv` (10 skills × 5 tests × 6 rubric dims = 300 rows)
- **Adversarial follow-up:** raptor/mantishack on K2 (privacy-abstraction trigger surface) and K4/K5 (writer/privacy enforcement gaps)
