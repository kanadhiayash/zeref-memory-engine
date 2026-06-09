# RISKS

Identified risks. Append-only at top.

## Format

```
### R[N] — YYYY-MM-DD — [Risk title]
**Severity**: high | medium | low
**Likelihood**: high | medium | low
**Impact**: [what happens if it materializes]
**Mitigation**: [if any]
**Status**: open | mitigated | accepted | retired
```

---

### R1 — 2026-06-08 — Gate output spoofing (no enforcement code)
**Severity**: high
**Likelihood**: medium
**Impact**: Adversary or careless agent emits fake `[budget-governor]` / `[skill-router]` / `[prompt-context-engine]` inline line, bypassing cost-classification + stack-selection + R6 brief. Token spend escalates silently; CRITICAL work runs on Haiku.
**Mitigation**: L3 — ship `zeref/gate.py` enforcement OR validator lint that parses recent PATTERNS.jsonl for gate-event presence per major task. Phase F arbitration.
**Status**: open

### R2 — 2026-06-08 — Validator under-reports skill count (false-pass)
**Severity**: medium
**Likelihood**: certain (already firing)
**Impact**: `python3 scripts/zeref-validate.py` shows `Skills: 10/10` despite 14 dirs + 14 registry entries. Audit / dashboard / investor-facing reports cite stale 10/10 number. Misleads anyone reading validator output as ground truth.
**Mitigation**: L1 — replace literal `10` with `len(EXPECTED['skills'])` + extend EXPECTED to 14 OR read from registry.
**Status**: open

### R3 — 2026-06-08 — Model-name format drift (registry vs SKILL.md)
**Severity**: medium
**Likelihood**: high
**Impact**: Tooling that maps registry `model: haiku` to actual API call must implement its own resolver. New skill (caveman-handoff) uses `claude-haiku-4-5` in SKILL.md; registry says `haiku`. Drift compounds as Anthropic releases new model versions — bare aliases lose version context.
**Mitigation**: L2 — `_shared/model-resolver.md` canonical mapping; audit `zeref/cli.py` parse path.
**Status**: open

### R4 — 2026-06-08 — R6 Zero Context Loss referenced by only 4 skills
**Severity**: medium
**Likelihood**: high
**Impact**: R6 written into `_shared/rules.md` but only `prompt-context-engine`, `skill-router`, `caveman-handoff`, and `handoff-compiler` cite it. Original 10 skills' Safety sections silent. Any of `memory-keeper` / `parent-sync` / `memory-import-export` / `pattern-to-skill` could drop entities during their own restructure / packaging / migration steps.
**Mitigation**: L4 — sweep all 14 SKILL.md Safety sections; add R6 ref where applicable.
**Status**: open

### R5 — 2026-06-08 — caveman-handoff event format unparsed
**Severity**: low
**Likelihood**: medium
**Impact**: `caveman-handoff` emits `event: handoff-compress` to PATTERNS.jsonl with payload `{original_tokens, compressed_tokens, ratio, model_from, model_to}`. `scripts/zeref-validate.py` has no allowlist entry; `tests/runner.py` has no handoff-replay mode. Malformed payloads could pollute log without detection.
**Mitigation**: L5 — extend validator known-event list + add runner.py mode.
**Status**: open

### R6 — 2026-06-08 — Worktree drift (uncommitted v2.6 + audit work)
**Severity**: high
**Likelihood**: certain
**Impact**: Worktree `compassionate-ride-66e134` holds entire v2.6 ship + v2.6.1 audit campaign uncommitted. Crash / branch switch / accidental discard = total loss of ~14 file changes including 4 new SKILL.md, AGENTS.md +2 Core Principles, CHANGELOG v2.6, all memory updates.
**Mitigation**: Commit per-phase to a feature branch. Push to remote at Phase G with manual confirm.
**Status**: open (mitigation in Phase G)
