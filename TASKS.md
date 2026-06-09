# TASKS — Zeref OS v2.5 Audit Campaign

Last updated: 2026-06-04

## Active

### Phase B — Sandbox Stress Test
- [ ] Build `tests/sandbox/<skill>/` per skill (10 dirs)
- [ ] Per skill: 5 test specs (Normal, Edge, Adversarial, Recovery, Drift)
- [ ] Generate `tests/scores-vB.csv` (10 × 5 × 6 = 300 rows)
- [ ] Hand-off summary doc

### Phase C — Security + Vulnerability Hunt
- [ ] Privacy gate bypass tests
- [ ] Single-writer race test
- [ ] pattern-to-skill code injection test
- [ ] parent-sync exfiltration test
- [ ] Permission escalation test
- [ ] Boundary-first violation test
- [ ] YAML parsing sweep
- [ ] Validator coverage corruption test
- [ ] `tests/security-audit-vC.md` CVSS-scored

### Phase D — Operational Workarounds
- [ ] L1: PII name regex fix
- [ ] L2: REDACT.md email enabled true
- [ ] L3: `tests/runner.py` live-run harness
- [ ] L4: `zeref db status` backend report
- [ ] L5: `cmd_init()` in `cli.py`
- [ ] L6: Dogfood `zeref init` → populated `PROJECT.md`
- [ ] L7: Connector stub tests
- [ ] L8: pattern-to-skill draft flow exercise
- [ ] L9: Advisory `.lock` sentinel
- [ ] **L10: Atomic .tmp+rename writes — R5 added to `_shared/rules.md`** (Phase B finding)
- [ ] `tests/scores-vD.csv` re-run

### Phase E — Rubric Re-Scoring
- [ ] `tests/zeref-rubric-v2.5.md`
- [ ] Per-dim evidence citation
- [ ] v1.0 → v2.0 → v2.5 deltas

### Phase F — UX Polish
- [ ] `README.md` rewrite
- [ ] `QUICKSTART.md`
- [ ] Dashboard auto-regen
- [ ] `INSTALL.md` refresh
- [ ] Harness stub QA
- [ ] `CHANGELOG.md` v2.5 entry

## Bloat Log

| Date | Phase | Trigger | Note |
|---|---|---|---|
| 2026-06-04 | A | Phase A cost $110 vs $80 est | 85 claims (≥80 target) — modest over |
| 2026-06-04 | bootstrap | dashboard.html 97KB | known plugin asset |
| 2026-06-04 | B | Phase B cost ~$17 vs $350-450 est | **WAY UNDER** — programmatic generation paid off ($333+ saved) |
| 2026-06-04 | B | Phase B added L10 (atomic writes) | Recovery dim failed exit (3.93<4.0) → new workaround |

## Done

- [x] Phase A — claims.csv (85), claims-audit.md
- [x] Productivity bootstrap — TASKS.md, dashboard.html, memory subdirs, glossary, project profile
- [x] Phase B — 10 sandbox dirs, 50 specs, 300 rows, summary doc
- [x] Phase C — security-audit-vC.md (2 CRITICAL, 3 HIGH found)
- [x] Phase D — L1-L11 workarounds; scores-vD-live.csv 20/20; phase-d-summary.md
- [x] Phase E — zeref-rubric-v2.5.md (8.00/10); ZRF 6 PASS + 4 SCAFFOLD
- [x] Phase F — README badges, QUICKSTART.md, CHANGELOG v2.5 entry
