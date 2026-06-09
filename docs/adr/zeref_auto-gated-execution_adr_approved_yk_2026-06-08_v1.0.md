---
adr_id: zeref-001
title: Auto-Gated Execution — 4-Gate Chain (v2.6.0)
status: approved
date: 2026-06-08
owner: yk
classification: internal
supersedes: none
superseded_by: none
---

# ADR-001: Auto-Gated Execution — 4-Gate Chain

## Context

Zeref OS v2.5 + earlier left cost-discipline + skill-routing implicit. Every major task burned tokens before classification → frequent Opus runs on LOW-weight work + manual skill selection across all 10 skills + verbatim prompt passthrough regardless of structure.

Signals:
- Session cost variance 10× across same-domain tasks (e.g. wiki-write on Haiku $0.02 vs same on Opus $0.50)
- Skill-stack bloat: tasks often invoked 5-8 skills when 2-3 sufficed
- Prompt-injection / brain-dump prompts caused rework loops
- No declared cost weight before execution → no enforcement of Core Principle "use the right tier"

## Decision

Adopt 4-gate Auto-Activation chain. Every major task passes 4 sequential gates **before any execution-model token spend**:

1. **Gate #1 `budget-governor`**: classify task weight (CRITICAL / HIGH / MEDIUM / LOW), resolve active model tier, enforce match (CRITICAL never on Haiku, LOW never on Opus). Declare inline: `[budget-governor] weight=<W> tier=<T> match=<OK|MISMATCH>`.
2. **Gate #2 `skill-router`**: classify task domain, map to smallest-useful-stack (1 lead + 2-3 support + 1 QA gate; max 5 skills). Declare inline: `[skill-router] domain=<D> lead=<L> support=[...] qa=<Q> ext=<E>`.
3. **Companion `fleet-activator`**: when extended-tool hint present (ECC/Graphify/gstack/...), live-probe filesystem + MCP registry for reachability; substitute emulator if unreachable.
4. **Gate #3 `prompt-context-engine`**: classify prompt (STRUCTURED/SEMI-STRUCTURED/UNSTRUCTURED); rewrite UNSTRUCTURED into `<objective>/<deliverable>/<constraints>/<context>/<success_criteria>` brief with 30s auto-approve. Zero context loss per R6.

Each gate declares output inline (user can override before token spend). Each gate emits PATTERNS.jsonl event (audit trail). Companion skill `caveman-handoff` preserves R6 chain across cross-model switches.

## Consequences

**Positive**:
- Declared cost weight + tier before every major task → cost discipline by construction
- Smallest-useful-stack declared inline → no silent fan-out
- UNSTRUCTURED prompts auto-restructured → fewer rework cycles
- R6 (Zero Context Loss) enforced across restructure / routing / handoff
- Grep-able audit trail in PATTERNS.jsonl

**Negative**:
- 4 gates add ~500 tokens output per task (acceptable: classification cost << execution cost)
- Gate output is initially prose-only (no code enforcement) — addressed in ADR-002 hardening
- New skills (4) double the skill count (10 → 14) — registry + validator updates needed

## Alternatives rejected

- **Single combined gate**: simpler but conflates orthogonal concerns (cost vs routing vs prompt-quality vs extended-tool reachability) — loses ability to override one gate independently.
- **Background gate (silent)**: no inline declaration → no user override path → defeats purpose.
- **Manual user invocation**: status-quo before v2.6; failed because users (including Yash) repeatedly forgot to classify.
- **Hard-block at validator level (no inline declaration)**: too rigid; user override path lost.

## Evidence

- CHANGELOG.md `[2.6.0]` entry — full skill + principle inventory
- `AGENTS.md` Core Principles 13-14 + `## Auto-Activation Gates` section + `## Model-Tier Routing` section
- `skills/{budget-governor,skill-router,fleet-activator,prompt-context-engine,caveman-handoff}/SKILL.md` — full specs
- `_shared/rules.md#R6` — Zero Context Loss rule
- Rubric impact (per `tests/zeref-rubric-v2.6.md`): Execution 7→9, Architecture 8→10, Operational Readiness 8→10

## Forward references

- ADR-002 (v2.6.1 audit hardening) — adds code enforcement to gate prose
- Future ADR — cascade-replay test for path to 10.00/10 (deferred to v2.7)
