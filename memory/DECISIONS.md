# DECISIONS

Confirmed decisions for this project. Append-only at top. Single writer: `memory-keeper`.

## Format

```
### YYYY-MM-DD — [Decision title]
**Decided**: [what was decided]
**Why**: [reasoning]
**Evidence**: high | medium | low
**Provenance**: [source — session ts, event hash, person]
**Supersedes**: [previous decision id, if any]
```

---

### 2026-06-08 — Phase F arbitration locked (4 decisions) → Phase D shipped 15 L-items
**Decided**: User arbitrated 4 grouped decisions via AskUserQuestion batches during v2.6.1 audit campaign:
1. **Gate enforcement (D-2026-06-08-gates)**: Advisory + validator lint. `scripts/zeref-validate.py` extended with `lint_patterns_log()` parsing PATTERNS.jsonl event allowlist + per-event JSON-schema. No new module. Covers L3, V01, L14, V07.
2. **Validator full bundle (D-2026-06-08-validator)**: L1 (count from registry) + L4 (R6 sweep on 4 entity-preserving skills) + L5+L15 (event schema). Skills count now reads `len(EXPECTED['skills'])` dynamically. R6 referenced in 9 of 14 SKILL.md (was 4).
3. **Model names canonical (D-2026-06-08-model-names)**: Full Anthropic ids canonical (`claude-haiku-4-5` / `claude-sonnet-4-6` / `claude-opus-4-7`). Registry's 14 model fields normalized; `model_alias` field preserves bare names for back-compat. `_shared/model-resolver.md` documents mapping + pin overrides (Opus 4.6 vs 4.7 +35% tokenizer note).
4. **Security mitigations all 5 (D-2026-06-08-security)**: Shipped L9 (fleet-activator marker-file probe), L10 (prompt-context-engine injection filter), L11 (60s irreversibility cool-down), L12 (caveman-handoff NFKC + homoglyph guard), L13 (budget-governor dual-key override). Closes both Phase C CRITICALs (V01 gate-spoof via validator lint, V02 prompt-injection via filter); both HIGHs (V03 probe-spoof via marker, V04 homoglyph via NFKC); both MEDIUMs (V05 override via dual-key, V06 race via cool-down).
**Why**: Recommended path chosen on every batch — minimizes new module surface while closing all 2 CRITICAL + 2 HIGH + 2 MEDIUM Phase C findings + L1-L8 known gaps. Advisory + lint preserves harness-agnostic principle; no new Python module dependency. Full ids future-proof against Anthropic versioning + tokenizer drift.
**Evidence**: high (validator passes Skills 14/14, 0 PATTERNS lint findings; 11 file edits applied + verified; R6 sweep increases coverage 4→9 SKILL.md)
**Provenance**: AskUserQuestion 4-batch arbitration, session 2026-06-08 ~15:30 EDT; plan `resume-zeref-os-v2-6-enchanted-gizmo.md` Phases F + D.
**Supersedes**: v2.6.0 prose-only gate enforcement; v2.6.0 hardcoded validator `/10`; v2.6.0 registry bare model names; v2.6.0 unhardened fleet-activator / prompt-context-engine / caveman-handoff / budget-governor (single-key override).

### 2026-06-08 — Ship v2.6.0 — Auto-Gated Execution (4-gate chain: budget → router → fleet → prompt → handoff)
**Decided**: Shipped v2.6.0. +4 skills (skill-router, fleet-activator, prompt-context-engine, caveman-handoff). Rewrote budget-governor with 2026 Anthropic pricing (Haiku 4.5 $1/$5, Sonnet 4.6 $3/$15, Opus 4.7 $5/$25) + Cost Weight Classification (CRITICAL/HIGH/MEDIUM/LOW) + Auto-Activation Rule (6 steps). +2 Core Principles (13 Cost-Weight Auto-Gate, 14 Task-Weight Model Routing). +1 shared rule R6 Zero Context Loss. +1 AGENTS.md ## Auto-Activation Gates section (3 gates declared). +1 AGENTS.md ## Model-Tier Routing section (weight → model + cascade pattern). Registry 10 → 14. Legacy Free/Standard/God Mode aliases preserved for tests/scores-v*.csv back-compat.
**Why**: v2.5 left cost-discipline + skill-routing implicit. Every major task burned tokens before classification → frequent Opus runs on LOW work + manual skill selection across all 10 skills. v2.6 makes 4 gates auto-fire inline: declare weight, declare stack, classify prompt, route model — before execution-model call. User can override at any gate. Smallest useful stack (1 lead + 2-3 support + 1 QA).
**Evidence**: medium (no sandbox tests yet — Phase B baseline pending; validator hardcode masks Skills count L1)
**Provenance**: sessions 2026-06-06 (plan `cost-stop-distributed-prism.md` approved) → 2026-06-08 Sessions A+B+C executed under plan `resume-zeref-os-v2-6-enchanted-gizmo.md`. Worktree `compassionate-ride-66e134`. Uncommitted.
**Supersedes**: budget-governor v2.5 tier table (GPT-4o / Gemini Flash refs); pre-v2.6 manual skill invocation pattern.

### 2026-06-05 — Ship v2.5.0 — Deep Audit Campaign (Phases A-F, retroactively logged)
**Decided**: 6-phase audit campaign shipped against v2.0 baseline. Phase A claims audit (85 rows, 71% VERIFIED). Phase B sandbox stress (300 rows, 10 skills × 5 tests × 6 dims). Phase C security (8 attacks, 2 CRITICAL → mitigated). Phase D workarounds L1-L11 (PII regex, email default-enabled, runner.py, db-status, zeref init, dogfood, connector stub, drafts flow, MemoryLock, atomic_write, write-decision PII scrub). Phase E rubric re-score 8.00/10 (from 7.13 audit-corrected v2.0). Phase F human UX polish (README, QUICKSTART, dashboard, INSTALL, harness stub QA).
**Why**: v2.0 spec-first execution needed code-backed verification + adversarial stress before claims could be made. Hybrid stack (ECC eval-harness + raptor + gstack QA) outperformed Zeref-only spec audit.
**Evidence**: high (CHANGELOG.md v2.5.0 entry documents deliverables; tests/ contains claims.csv 85 rows, scores-vB.csv 300 rows, security-audit-vC.md, phase-*-summary.md, zeref-rubric-v2.5.md)
**Provenance**: CHANGELOG.md v2.5.0 entry dated 2026-06-05.
**Supersedes**: v2.0 7.13 rubric.
**Retroactive log note**: not written to DECISIONS.md at ship time (memory drift trap, see C1). Logged 2026-06-08 during v2.6.1 audit activation.

### 2026-05-31 — Ship v4.3.0 — v4.x canon import + nomenclature alignment + team packs (M4)
**Decided**: Adopted package nomenclature wholesale per user instruction. Flat `memory/` layout (no more `memory/wiki/`). Root privacy templates (`PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md`) per ZEREF_OS §4.1. Default privacy mode `abstract`. All connectors OFF by default. Renamed `memory/logs/session-events.jsonl` → `memory/patterns/PATTERNS.jsonl` (archived predecessor preserved). Renamed `skills/_drafts/` convention → `skills/drafts/`. Added 6 team packs (`team-packs/{solo,build,research,red,audit,ship}.md`) + `/team` command per §8. Added harness stubs `.cursor/rules/zeref.mdc`, `.windsurfrules`, `.aider.conf.yml.example` per §10. Codified Two-Strikes Rule, Connector Advisory, Harness Translation Map in `references/`. Imported v4.x design canon to `references/v4x-canon/`. Created idempotent migration script `scripts/migrate-v4.2-to-v4.3.py` with pre-migration snapshot + `git mv` for history preservation. Bumped to v4.3.0.
**Why**: Aligns repo with canonical v4.x specification while preserving all existing v4.2 functionality. Wholesale nomenclature adoption surfaces design intent directly (reading order, privacy model, team packs) instead of forcing readers to map between two conventions. Migration script ensures user repos can move without manual work; pre-migration snapshot guarantees rollback. All changes additive at the capability level; only paths and reading order changed. Maps to decisions D7 (harness agnosticism), D8 (privacy model), D9 (archive policy), D10 (team packs), D11 (connector advisory) in `references/v4x-canon/DECISION_LOG.md`.
**Evidence**: high
**Provenance**: session 2026-05-31, plan `you-are-being-handed-glowing-lynx.md`, validator passes (10 skills, 6 agents, 8 commands, 6 team packs, 3 root privacy, 6 v4x canon, 3 harness stubs)
**Supersedes**: v4.2.0 nested `memory/wiki/` layout; `config/PRIVACY.md` (archived at `memory/archive/config-PRIVACY-v4.2.md`)

### 2026-05-30 — Ship v4.2.0 — pattern-observer + pattern-to-skill (M3)
**Decided**: Promoted final 2 stubs to production. pattern-observer scans session-events.jsonl over 72h rolling window using Jaccard 3-gram similarity ≥0.8 with union-find clustering. pattern-to-skill drafts SKILL.md files to skills/_drafts/ with immutable PROVENANCE.md, requires explicit user review via /review-skill (approve/edit/reject/defer). v4 roadmap declared complete — no stubs remain.
**Why**: Closes the self-extension loop. Repeated work becomes reusable skills, review-first to prevent runaway auto-generation. Pure-markdown impl preserves harness-agnostic principle.
**Evidence**: high
**Provenance**: session 2026-05-30, commit fd4d2d1, tag v4.2.0
**Supersedes**: M3 stub from v4.0.0

### 2026-05-30 — Ship v4.1.0 — contradiction-resolution + parent-sync (M2)
**Decided**: Promoted 2 stubs to production. contradiction-resolution uses subject/predicate/value fingerprint matching against DECISIONS/OPEN_QUESTIONS/RISKS; halts write on conflict, queues to CONFLICTS.md, supports snooze-until-/done; 4 anti-patterns refused (recency-wins, grade-wins, silent-drop, indefinite-snooze). parent-sync stages to memory/sync/outbound/<iso>/ with manifest.json, requires explicit approval per push, sets parent files chmod 444, supports rollback via provenance pointers; local-only privacy mode blocks all parent sync.
**Why**: Memory integrity requires human arbitration on conflict (never silent resolve). Parent rollup needs provenance + approval gate to avoid contaminating parent state with low-quality child claims.
**Evidence**: high
**Provenance**: session 2026-05-30, commit cf94144, tag v4.1.0
**Supersedes**: M2 stubs from v4.0.0

### 2026-05-30 — Ship v4.0.0 — philosophical reset (M1)
**Decided**: Complete rewrite. Zeref OS is no longer an agent harness OS — it is a local-first context and memory engine. Deleted 109 specialist skills, 5 agents (fleet-router, council-convener, executive-qa, release-governor, context-engine), 3 identity files (ZEREF.md, ZEREFOS.md, ZEREFPROJECT.md), 14 zeref-prefixed commands, output-styles, registry, 5 v3 helper scripts. Built 10 disciplined skills, 6 disciplined agents, 7 commands, 5 config files, memory/ scaffold with append-only event log + snapshots, 3 privacy modes (exact/abstract/local-only). Net diff: −26,690 / +1,949 lines. Always-on context: 5,035 → 905 tokens (82% reduction).
**Why**: v3 OS framing was Yash-specific, CEO-themed, Claude-only — diverged from cross-harness/cross-model portability principle. v4 returns to first principles: persistent markdown memory, harness-agnostic AGENTS.md spec, privacy-first writes, human arbitration on contradictions, progressive activation.
**Evidence**: high
**Provenance**: session 2026-05-30, commit 1aeca5c → 1ee6f92, tag v4.0.0; v3 frozen at tag v3.0.0-frozen
**Supersedes**: all v3 architecture
