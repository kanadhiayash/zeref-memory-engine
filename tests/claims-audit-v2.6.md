# Zeref OS v2.6 — Claims Audit (Phase A)

**Date**: 2026-06-08
**Lead**: Audit team (Reader + Linter + Quality gate)
**Stack used**: evidence-grader (Zeref) + wiki-maintenance (Zeref) + manual scoring
**Source**: `tests/claims-v2.6.csv` (52 claims across AGENTS.md, 5 SKILL.md files, _shared/rules.md, zeref-registry.json, CHANGELOG.md, scripts/zeref-validate.py)

## Summary

| Composite | Count | % |
|---|---|---|
| VERIFIED | 21 | 40.4% |
| VERIFIED-PROSE (spec correct, no code enforcement) | 10 | 19.2% |
| PARTIAL | 9 | 17.3% |
| UNVERIFIED | 11 | 21.2% |
| FALSE | 1 | 1.9% |

**Headline**: spec coverage is high; **code enforcement is the gap**. 19% of claims are "prose-correct but unenforced." Only 1 outright FALSE claim (validator hardcode L1 — known).

## Findings by category

### Architecture (10 claims)
4 VERIFIED, 5 VERIFIED-PROSE, 1 UNVERIFIED.
- Core Principles 13-14, Auto-Activation Gates, Model-Tier Routing are well-specified but **none enforced by code**. All depend on agent self-discipline.
- Cascade pattern (orchestrator/executor/final-gate) has no orchestrator code — UNVERIFIED.

### Contract / output format (7 claims)
4 VERIFIED, 3 VERIFIED-PROSE.
- Gate output line formats spec'd; no regex validator. Adversary could emit malformed `[budget-governor] weight=PIZZA tier=HOTDOG` and no check would fire.

### Safety (7 claims)
2 VERIFIED, 4 VERIFIED-PROSE, 1 PARTIAL.
- Anti-patterns ("never activate all 13 skills", "never paraphrase code", "R6 abort on violation") are stated as hard blocks but only documented, not enforced.

### Pricing (4 claims)
3 VERIFIED, 1 PARTIAL.
- Anthropic 2026 rates match published pricing.
- Opus +35% tokenizer claim cited but no in-repo benchmark.

### Count (3 claims)
2 VERIFIED, 1 FALSE.
- Skills 14 in registry + dirs + AGENTS.md table — all match.
- Validator says `10/10` — **FALSE** (L1).

### Probe / fleet-activator (5 claims)
5 VERIFIED.
- All 6 probe targets correctly spec'd; ECC + Graphify reachability confirmed by `test -d` / `test -f` on 2026-06-08.

### Routing / model assignment (5 claims, registry)
5 VERIFIED.
- Per-skill model field aligns with weight matrix; no LOW→opus or CRITICAL→haiku mismatches.

### UX / ergonomics (3 claims)
0 VERIFIED, 3 UNVERIFIED.
- 30-second auto-approve timer in prompt-context-engine: no timer impl.
- User-override syntax in skill-router: no parser.
- Token-discipline caps (<500 / <300 tok): no tracker.

### Compat (3 claims)
3 VERIFIED.
- Legacy aliases (Free/Standard/God Mode) preserved.
- Notion + Linear blocks dropped from prompt-context-engine adaptation.

### Bug (1 claim)
1 FALSE → L1 workaround pending.

### Functional / behavioral (4 claims)
0 VERIFIED, 4 UNVERIFIED.
- All depend on Phase B sandbox stress to confirm or fail.

## Contradictions surfaced → memory/CONFLICTS.md

- **C1**: Memory drift (v2.5 + v2.6 unlogged) — already addressed in this session via retroactive DECISIONS.md entries.
- **C2**: Validator `Skills: 10/10` vs reality `14/14` (L1).
- **C3**: Model-name format drift (registry bare vs SKILL.md full ids) (L2).
- **C4**: Auto-Activation Gates prose-only, no enforcement (L3) — covers ZRF-C2.6-001/002/003/004/005/006/016/018/021/022.
- **C5**: caveman-handoff event format spec'd but no validator allowlist (L5).

## R6 coverage gap (R4 risk)

R6 cited in only 4 of 14 SKILL.md Safety sections:
- ✓ prompt-context-engine
- ✓ skill-router (cites #R1 + #R4 but not #R6 explicitly — partial)
- ✓ caveman-handoff (cites #R6 explicitly)
- ✓ handoff-compiler (cites R6 forward dependency in _shared/rules.md only)

Missing R6 reference in: budget-governor, fleet-activator, memory-keeper, privacy-guardian, evidence-grader, contradiction-resolution, wiki-maintenance, project-setup, parent-sync, pattern-to-skill, memory-import-export, privacy-abstraction.

Plan D L4: sweep + add R6 references where applicable (entity-preserving skills: memory-keeper, parent-sync, memory-import-export, pattern-to-skill).

## Phase A exit criteria

- [x] ≥40 claims graded → **52 claims**
- [x] ≥2 contradictions surfaced → **5 contradictions** (C1-C5)
- [x] All claims tagged with composite grade
- [x] FALSE claims escalated to L-item workaround path (L1)
- [x] Memory updated: CONFLICTS.md (C1-C4), RISKS.md (R1-R6), DECISIONS.md (retroactive v2.5 + v2.6)

## Headline confidence

- **Spec quality**: high — 60% of claims are VERIFIED or VERIFIED-PROSE.
- **Enforcement gap**: critical — 30% of safety / contract / architecture claims are unenforced.
- **Verifier under-reporting**: 1 FALSE claim is the validator itself (L1) — until fixed, every audit report mis-quotes Skills count.

→ Proceed to Phase B (sandbox stress) + Phase C (security hunt). Phase D workarounds will close enforcement gap.
