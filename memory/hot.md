# memory/hot.md

> Last 3 sessions, current context. Cap ≤500 words. Read FIRST per ZEREF_OS §0.

## Session 2026-06-08 — v2.6.1 Audit + Hardening Campaign (Phases A-G)

Shipped v2.6.1 — full deep-audit campaign against v2.6.0. Six phases: claim audit + sandbox stress + security hunt + arbitration + workarounds + rubric + push.

**What landed:**
- **Phase A**: `tests/claims-v2.6.csv` (52 claims) + `tests/claims-audit-v2.6.md`. 60% VERIFIED, 30% PARTIAL/UNVERIFIED, 1 FALSE (validator hardcode → L1).
- **Phase B**: `tests/sandbox/{skill-router,fleet-activator,prompt-context-engine,caveman-handoff,budget-governor}/{normal,edge,adversarial,recovery,drift}.md` (25 specs) + `tests/scores-v2.6-B.csv` (150 rows). Pass rate 76% (114/150). Failures = adversarial gaps → L9-L12.
- **Phase C**: `tests/security-audit-v2.6-C.md` (8 attacks CVSS-scored). 2 CRITICAL (V01 gate-spoof, V02 prompt-injection) + 2 HIGH (V03 probe-spoof, V04 homoglyph) + 2 MEDIUM (V05 override, V06 race) + 2 LOW. All closed by Phase D.
- **Phase F**: AskUserQuestion 4-batch arbitration — gate enforcement = advisory+lint, validator bundle full, model names canonical full ids, security ship all 5.
- **Phase D L1-L15**: validator dynamic skill count from registry (Skills: 14/14); R6 sweep 4→9 SKILL.md; event-schema allowlist with per-event JSON-schema; model resolver (_shared/model-resolver.md); fleet-activator marker-file probe (L9); prompt-context-engine injection filter (L10) + 60s cool-down (L11); caveman-handoff NFKC + homoglyph guard (L12); budget-governor dual-key override (L13); skill-router stack-cap lint (L14); PATTERNS.jsonl schema validator (L15).
- **Phase E**: `tests/zeref-rubric-v2.6.md` composite **9.88/10** (up from v2.5 8.00). Path to 10 documented (cascade-replay test).
- **Phase G**: wiki-maintenance pass (this hot.md refresh + DECISIONS.md + CONFLICTS.md + RISKS.md retroactive logs of v2.5 + v2.6 + v2.6.1 ship). CHANGELOG v2.6.1 entry. Manual-confirm push to origin.

**Validator**: Skills 14/14, Agents 6/6, Commands 8/8, Team packs 6/6, Config 5/5, Privacy 3/3, v4x canon 6/6, Harness stubs 3/3, PATTERNS lint 0 findings. ✔ Validation passed.

**Open** (carry-forward): C1 memory-drift lessons codified into wiki-maintenance trigger; ZRF-B07 cross-harness deferred to v2.7; cascade-replay test → 10.00 deferred.

## Session 2026-06-08 (earlier) — v2.6.0 Ship (4-gate chain)

Shipped v2.6.0 in Sessions A+B+C: +4 skills (skill-router, fleet-activator, prompt-context-engine, caveman-handoff) + budget-governor rewrite. +Core Principle 13 + 14. +R6 Zero Context Loss. Skills 10→14. Auto-Activation Gates declared; enforcement deferred to v2.6.1 audit.

## Session 2026-06-05 — v2.5 Deep Audit (Phases A-F, retroactively logged)

8.00/10 rubric. Phase D L1-L11 workarounds. Phase F README/QUICKSTART polish. Logged retroactively to DECISIONS.md on 2026-06-08 (C1 memory-drift root cause).

---

*Carry-forward open: ZRF-B07 cross-harness (Cursor/Aider/Gemini); cascade-replay test; pipx PyPI publish; "Zeref" rebrand.*
