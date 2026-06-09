# CONFLICTS

Contradiction queue. Detected by `memory-keeper`, arbitrated by user, resolved by `contradiction-resolution` skill.

## Format

```
### C[N] — YYYY-MM-DD — [Conflict title]
**Status**: open | snoozed-until-done | resolved
**Side A**: [claim + provenance]
**Side B**: [claim + provenance]
**Detected by**: [agent + event hash]
**Resolution**: [user decision + ts, blank until resolved]
```

---

### C1 — 2026-06-08 — Memory drift across v2.5 + v2.6 ship cycles
**Status**: open
**Side A**: hot.md, index.md, MEMORY.md, DECISIONS.md, CONFLICTS.md, OPEN_QUESTIONS.md, RISKS.md all stuck at 2026-05-31 v4.3 state; no v2.5 audit or v2.6 ship reflected. Implies `wiki-maintenance` never invoked post-ship in two cycles.
**Side B**: CHANGELOG.md documents v2.5.0 (2026-06-05, 8.00/10 rubric) + v2.6.0 (2026-06-08, 4-gate chain). tests/ contains v2.5 deliverables. skills/ on disk has 14 SKILL.md (10 original + 4 v2.6). Registry has 14 entries. AGENTS.md has 14 Core Principles + 3 Auto-Activation Gates.
**Detected by**: v2.6.1 audit activation, session 2026-06-08, Bash AGENTS.md §0 read.
**Resolution**: Logged as retroactive C1; addressed in v2.6.1 audit Phase G (wiki-maintenance pass mandatory). Root cause: `/done` was never run after v2.5 or v2.6 work — both shipped from worktree without invoking session-close hook. Codify in Two-Strikes Rule (this is occurrence #1 — next miss triggers automation requirement).

### C2 — 2026-06-08 — Validator Skills count mismatch (L1)
**Status**: resolved 2026-06-08 — L1 shipped (validator reads from zeref-registry.json; reports Skills: 14/14)
**Side A**: `scripts/zeref-validate.py:165` prints `Skills: 10/10` (literal); reads from hardcoded `EXPECTED["skills"]` list (10 names).
**Side B**: `skills/` has 14 dirs on disk; `zeref-registry.json` has 14 entries; AGENTS.md `## Skills (14)` table lists 14 rows.
**Detected by**: Phase 0 Explore agent, session 2026-06-08.
**Resolution**: Pending L1 — update validator to read from registry OR extend EXPECTED list to 14. Decision in Phase F arbitration.

### C3 — 2026-06-08 — Model-name format drift (L2)
**Status**: resolved 2026-06-08 — L2 shipped (registry normalized to full ids + model_alias; _shared/model-resolver.md canonical doc)
**Side A**: `zeref-registry.json` uses bare model names (`"model": "haiku"` / `"sonnet"` / `"opus"`) across all 14 entries.
**Side B**: New v2.6 SKILL.md files use full Anthropic ids in frontmatter (`model: claude-haiku-4-5` for skill-router/fleet-activator/caveman-handoff; `model: sonnet` for prompt-context-engine). `budget-governor` SKILL.md uses `model: claude-haiku-4-5`. AGENTS.md Model-Tier Routing references full ids (`claude-haiku-4-5` / `claude-sonnet-4-6` / `claude-opus-4-7`).
**Detected by**: v2.6 ship Session B + Phase 0 Explore.
**Resolution**: Pending L2 — introduce `_shared/model-resolver.md` bare → full mapping. Decision in Phase F arbitration.

### C4 — 2026-06-08 — Auto-Activation Gates are prose-only (L3)
**Status**: resolved 2026-06-08 — L3 shipped (advisory + validator lint via lint_patterns_log() in scripts/zeref-validate.py; covers L14 stack-cap + V07 fan-out)
**Side A**: AGENTS.md `## Auto-Activation Gates` declares 3 gates fire before every major task. Core Principle 13 says "CRITICAL / HIGH cannot proceed without stated tier."
**Side B**: No enforcement code in `zeref/`, no hook in `scripts/`, no validator check. Gates rely on agent self-discipline + inline declaration. Compromised if agent forgets or adversary injects fake gate output.
**Detected by**: v2.6 plan §"Risks" + Phase 0 Explore.
**Resolution**: Pending L3 — choose (a) advisory + validator lint, (b) `zeref/gate.py` enforcement module, (c) both. Decision in Phase F arbitration.
