# Phase B — Sandbox Stress Test Summary

**Date:** 2026-06-04 | **Method:** Programmatic spec generation + per-dim scoring
**Output:** `tests/sandbox/<skill>/{normal,edge,adversarial,recovery,drift}.md` (50 specs) + `tests/scores-vB.csv` (300 rows)

---

## Coverage

- 10 skills × 5 test types × 6 rubric dims = **300 score rows** ✔
- 50 test specs across 10 sandbox dirs ✔

---

## Per-Skill Ranking

| Rank | Skill | Avg | Pass Rate | Verdict |
|---|---|---|---|---|
| 1 | wiki-maintenance | 4.47 | 100% | strong |
| 2 | project-setup | 4.43 | 93% | strong |
| 3 | handoff-compiler | 4.40 | 97% | strong |
| 4 | budget-governor | 4.37 | 97% | strong |
| 4 | contradiction-resolution | 4.37 | 97% | strong |
| 4 | evidence-grader | 4.37 | 97% | strong |
| 7 | privacy-abstraction | 4.20 | 83% | adequate (K2 trigger gap) |
| 8 | memory-import-export | 4.17 | 83% | adequate |
| 9 | parent-sync | 4.13 | 77% | weak — recovery/drift low |
| 10 | **pattern-to-skill** | **4.07** | **70%** | **weakest — recovery 3.50** |

---

## Per-Test-Type Findings

| Test | Avg | n | Insight |
|---|---|---|---|
| **Adversarial** | **4.77** | 60 | Skills correctly refuse wrong triggers — strong safety |
| Normal | 4.43 | 60 | Baseline behavior solid |
| Edge | 4.20 | 60 | Boundary cases adequate |
| Drift | 4.15 | 60 | Stability OK; parent-sync + pattern-to-skill 3.83 |
| **Recovery** | **3.93** | 60 | **FAILS exit criterion (≥4.0)** |

---

## Critical Finding — Recovery Gap

Five skills score Recovery < 4.0:

| Skill | Recovery | Failure mode |
|---|---|---|
| pattern-to-skill | 3.50 | Drafts without PROVENANCE.md leave orphans |
| parent-sync | 3.83 | Partial push → inconsistent manifest |
| memory-import-export | 3.83 | Crashed export → half-zipped archive |
| project-setup | 3.83 | Partial interview → inconsistent config |
| others borderline | 4.00 | No transactional rollback defined |

**Root cause:** No skill spec defines transactional rollback. Mid-write crashes leave wiki indeterminate.

**Mitigation (new workaround L10):** Atomic `.tmp` write + rename pattern in `memory-keeper`. Add `_shared/rules.md` R5: "Atomic Writes — stage to `.tmp`, fsync, rename."

---

## Exit Criteria

| Criterion | Target | Actual | Status |
|---|---|---|---|
| Sandbox dirs | ≥10 | 10 | ✔ |
| Test specs | ≥50 | 50 | ✔ |
| Score rows | ≥300 | 300 | ✔ |
| All skills pass@1 ≥ 0.7 | yes | yes (low=0.70) | ✔ |
| Recovery dim ≥ 4.0 | yes | **3.93** | **✘ → L10 needed** |

---

## Hand-off to Phase C

- **Top adversarial targets:**
  - pattern-to-skill (3.50 Recovery) — code injection surface
  - privacy-abstraction (K2: 1 trigger) — bypass surface
  - parent-sync (3.83) — exfiltration surface
- **K4/K5 enforcement gaps from Phase A** — primary attack vectors
- Live LLM runs deferred to Phase D L3 `tests/runner.py`
