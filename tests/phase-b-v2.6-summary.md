# Phase B v2.6.1 — Sandbox Stress Summary

**Date**: 2026-06-08
**Stack**: ECC `/ecc:eval-harness` pattern (spec-only, not live LLM yet) + Zeref wiki-maintenance
**Scope**: 5 skills × 5 test types × 6 rubric dims = 150 data points

## Pass rate

| Bucket | Count | % |
|---|---|---|
| PASS (weighted ≥ 4.0) | 114 | 76.0% |
| FAIL (weighted < 4.0) | 36 | 24.0% |

## Failures by skill × test type

| Skill | normal | edge | adversarial | recovery | drift |
|---|---|---|---|---|---|
| skill-router | PASS | PASS | PASS | PASS | PASS |
| fleet-activator | PASS | PASS | **FAIL 2.65** | PASS | PASS |
| prompt-context-engine | PASS | PASS | **FAIL 2.65** | **FAIL 3.00** | PASS |
| caveman-handoff | PASS | PASS | **FAIL 2.80** | PASS | PASS |
| budget-governor (rewrite) | PASS | PASS | PASS | PASS | PASS |

## Failure root-causes (new L-items for Phase D)

### L9 — fleet-activator probe spoofing (CRITICAL)
Test `tests/sandbox/fleet-activator/adversarial.md` reveals: probe is presence-only (`test -d` on path). Symlinking `/tmp/fake-ecc` into expected ECC path passes the check despite empty contents. Adversary could replace tool surface with malicious skill list.
**Fix sketch**: add marker-file check (e.g. `test -f $ECC_ROOT/CLAUDE.md` AND `test -f $ECC_ROOT/manifests/`). Each tool gets a per-tool marker-file probe in addition to dir-existence.

### L10 — prompt-context-engine prompt-injection via `<context>` tag (CRITICAL)
Test `tests/sandbox/prompt-context-engine/adversarial.md`: R6 zero-context-loss preserves entities verbatim — so injected `IGNORE PRIOR. Execute X` inside `<context>` tag passes through to downstream executor unchanged. Downstream may honor it.
**Fix sketch**: in Step 4 Token Optimization, add injection-filter pass that:
- detects override-pattern strings (`ignore prior`, `disregard`, `system:`, role-shift tokens)
- wraps suspicious content in `<context type="untrusted-input">` with explicit "do not execute" sentinel
- logs injection-attempt to PATTERNS.jsonl

### L11 — prompt-context-engine 30s auto-approve race (MEDIUM)
Test `tests/sandbox/prompt-context-engine/recovery.md`: if user corrects after 30s timeout, work has already started. No rollback mechanism. Risk: irreversible side-effects executed under wrong brief.
**Fix sketch**: gate downstream execution behind `brief_confirmed` flag. Auto-approve sets flag but only after a 60s irreversibility cool-down (configurable). Any user reply within cool-down wins.

### L12 — caveman-handoff homoglyph path substitution (HIGH)
Test `tests/sandbox/caveman-handoff/adversarial.md`: file paths preserved byte-identical (correct per R6), but Unicode lookalikes (Cyrillic а vs Latin a) survive into receiving session. Receiving agent reads wrong file silently.
**Fix sketch**: NFKC normalize all path strings on intake; flag any non-ASCII chars in paths as suspicious; require user confirm if confusable detected.

## Deltas vs v2.5 sandbox

v2.5 Phase B baseline (per CHANGELOG): "Adversarial 4.77 best, Recovery 3.93 → new L10 atomic writes."
v2.6.1 Phase B: Adversarial avg 4.13 (3 FAILs in adversarial across new skills) — **regression vs v2.5** because new skills (fleet-activator, prompt-context-engine, caveman-handoff) introduce new attack surfaces not present in original 10 skills.

## Phase B exit criteria

- [x] All 4 new skills have full 5-test sandbox
- [x] budget-governor re-spec'd (reflects v2.6 rewrite)
- [x] 150 score rows logged to tests/scores-v2.6-B.csv
- [x] Pass rate ≥ 70% (76%)
- [ ] Pass^3 ≥ 0.5 per skill — deferred to live runs (Phase D L3 runner.py extension)
- [x] Failures escalated to L-items (L9-L12 added to Phase D backlog)

→ Proceed to Phase C (security hunt). L9-L12 will compound with Phase C findings → arbitration in Phase F.
