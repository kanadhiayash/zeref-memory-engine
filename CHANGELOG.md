# Changelog

All notable changes to Zeref are documented here.

Format: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`

---

## [4.2.0] — 2026-05-30

### M3 — pattern detection + skill drafting (full impl)

Closes the v4 roadmap. Final 2 stubs promoted to production:

- **`agents/pattern-observer.md`** — fleshed out
  - 72h rolling window scan of `session-events.jsonl`
  - Task signature extraction: verb + subject + 3-gram qualifiers (stop-words stripped)
  - Jaccard similarity (≥0.8 threshold) over qualifier 3-gram sets
  - Union-find clustering; discard clusters < 3 members
  - Scoring: `frequency × (1 / recency_span_hours)` (favors dense recent repetition)
  - Emits candidates to `memory/sync/outbound/patterns/<cluster-id>.json` with full schema
  - Dedupe by cluster_id; update existing candidates with new members
  - Quiet hours: top-3 by score per scan; rest logged as suppressed
  - Activation: `/done`, `/stop`, `/status`, manual
  - Background only — never blocks active work
  - User can disable via `config/BUDGET.md` `pattern_detection: false`

- **`skills/pattern-to-skill/SKILL.md`** — fleshed out
  - DRAFT operation: load candidate → synthesize metadata (name, description, trigger, model, max_turns) → synthesize body (mission, when-to-use, operations, safety) → write `skills/_drafts/<name>/SKILL.md` + immutable `PROVENANCE.md`
  - REVIEW QUEUE: list pending drafts with score + event count + description
  - Per-draft prompt: show frontmatter + body + provenance summary
  - 4 actions: approve (git mv preserves history + strip draft markers + log), edit (open file, re-prompt), reject (prompt reason, rm dir, mark candidate JSON rejected_at), defer (leave in place, increment counter, auto-prompt after 3 defers)
  - PROVENANCE.md immutable — never edited after creation

- **`commands/review-skill.md`** — fleshed out (was placeholder)
  - Picks up new candidates → invokes pattern-to-skill DRAFT
  - Then invokes REVIEW QUEUE for user processing
  - Final report: counts of approved/edited/rejected/deferred

- **`scripts/zeref-validate-v4.py`** — `skills/_drafts/` allowlisted, surfaces warning if drafts pending

### Unchanged from v4.1.0
- 10 skills (all 10 fully impl now)
- 6 agents (all 6 fully impl now)
- 7 commands (all fully impl)
- 5 config files
- Memory scaffold
- Root manifests
- v3 → v4 migration tooling

### v4 roadmap complete
- v4.0 (M1): core engine ✅
- v4.1 (M2): contradiction-resolution + parent-sync ✅
- v4.2 (M3): pattern-observer + pattern-to-skill ✅

No stubs remain. Plugin fully production-ready.

---

## [4.1.0] — 2026-05-30

### M2 — contradiction + parent sync (full impl)

Previously stubs in v4.0.0; now production-ready:

- **`skills/contradiction-resolution/SKILL.md`** — fleshed out
  - DETECT algorithm: subject/predicate/value fingerprint match against DECISIONS/OPEN_QUESTIONS/RISKS
  - QUEUE flow: halt write → append to CONFLICTS.md → surface to user
  - SNOOZE: snooze-until-done with reason capture; re-surfaces at /done
  - RESOLVE: 3 modes (single winner with [SUPERSEDED] marker, both-valid context-dependent, merge synthesis)
  - SNOOZED REVIEW: /done blocks completion until pending conflicts processed
  - Evidence grade comparison surfaced but never auto-resolves
  - 4 explicit anti-patterns refused (recency-wins, grade-wins, silent-drop, indefinite-snooze)

- **`skills/parent-sync/SKILL.md`** — fleshed out
  - Pre-flight: parent_path validation, child_id assignment
  - STAGE: read push_content per config, filter via evidence-curator (≥ medium), pass through privacy-guardian, write to `memory/sync/outbound/<iso>/` with `manifest.json` (schema_version, child_id, source_events, privacy_mode, entry_counts)
  - APPROVE: explicit user confirmation with preview support
  - PUSH: copy to `<parent_path>/memory/sync/parent/<child_id>/<iso>/`, set read-only, log PUSHED
  - PARENT-SIDE INGEST: parent's `/start` runs conflict detection on incoming entries; clean entries merge with child provenance, conflicts to parent's CONFLICTS.md
  - ROLLBACK: recover bad pushes via provenance pointers
  - Local-only privacy mode blocks all parent sync

- **`agents/sync-coordinator.md`** — wired
  - /start: applies permissions + mounts parent + ingests pending parent pushes
  - /stop: prompts for parent push, snapshots wiki with manifest
  - /sync-parent: direct invocation of parent-sync skill
  - /reset-permissions: clears overrides, restores defaults
  - Parent ingest orchestration: walks memory/sync/parent/*/ for unprocessed pushes

- **`agents/memory-keeper.md`** — WRITE flow now invokes `contradiction-resolution` DETECT/QUEUE instead of inline conflict logic

### Unchanged from v4.0.0
- 10 skills (8 fully impl, 2 still stub: pattern-to-skill → M3)
- 6 agents (5 fully impl, 1 still stub: pattern-observer → M3)
- 7 commands
- 5 config files
- Memory scaffold
- Root manifests

### Roadmap
- v4.2 (M3): pattern-observer + pattern-to-skill (last 2 stubs)

---

## [4.0.0] — 2026-05-28

### Philosophical reset
Zeref is no longer an agent harness OS. It is now a **local-first context and memory engine** — harness-agnostic, model-agnostic, privacy-first, developer-first, free.

### Removed (clean break)
- 109 specialist skills (`zeref-biz-*`, `zeref-cnt-*`, `zeref-dev-*`, `zeref-mkt-*`, `zeref-qa-*`, `zeref-ux-*`, `zeref-hq-*`, `zeref-final-*`)
- Agents: `zeref-fleet-router`, `zeref-council-convener`, `zeref-executive-qa-agent`, `zeref-release-governor`, `zeref-context-engine`
- Identity files: `ZEREF.md`, `ZEREFOS.md`, `ZEREFPROJECT.md`
- All CEO / Yash-specific / Ruflo / council framing
- `registry/zeref-skill-registry.json`
- `output-styles/`
- 5 v3 helper scripts (`rebuild_registry.py`, `skill_updater.py`, `self_eval.py`, `upgrade_frontmatter.py`, `add_skill_descriptions.py`)
- v3 `wiki/` (replaced by `memory/wiki/`)

### Added
- **Root manifests**: `AGENTS.md` (canonical), `CLAUDE.md` (shim), `GEMINI.md` (shim), `SKILL.md` (entry)
- **config/** (5 files): PROJECT, PRIVACY, PERMISSIONS, PARENT_SYNC, BUDGET
- **memory/** scaffold: raw, wiki (INDEX + DECISIONS + OPEN_QUESTIONS + RISKS + CONFLICTS + ARCHIVE), logs (session-events.jsonl), snapshots, sync (outbound + parent)
- **10 skills**: `project-setup`, `wiki-maintenance`, `contradiction-resolution` *(M2 stub)*, `privacy-abstraction`, `parent-sync` *(M2 stub)*, `pattern-to-skill` *(M3 stub)*, `memory-import-export`, `budget-governor`, `handoff-compiler`, `evidence-grader`
- **6 agents**: `memory-keeper` (refactored), `privacy-guardian` (refactored from trust-sentinel), `sync-coordinator` (new), `evidence-curator` (refactored from evaluator), `pattern-observer` *(M3 stub)*, `handoff-orchestrator` (new)
- **7 commands**: `/start`, `/done`, `/stop`, `/status`, `/sync-parent`, `/reset-permissions`, `/review-skill`
- **Scripts**: `zeref-validate-v4.py` (new schema validator), `migrate-v3-to-v4.py` (one-shot migration)
- `MIGRATION.md` documenting v3 → v4 changes
- Append-only event log + snapshot system
- 3 privacy modes (exact / abstract / local-only)
- Parent sync mechanism (full impl in v4.1.0)

### Renamed
- `agents/zeref-memory-keeper.md` → `agents/memory-keeper.md`
- `agents/zeref-trust-sentinel.md` → `agents/privacy-guardian.md`
- `agents/zeref-evaluator.md` → `agents/evidence-curator.md`
- Commands lost `zeref-` prefix and merged: `/zeref-activate` → `/start`, `/zeref-save` → `/done`, etc.

### Migration
v3 frozen at git tag `v3.0.0-frozen`. Use `scripts/migrate-v3-to-v4.py` for data migration. No backward compat shims — clean break.

### Roadmap
- v4.1 (M2): full `contradiction-resolution` + `parent-sync`
- v4.2 (M3): `pattern-observer` + `pattern-to-skill` draft generation

---

## [3.0.0] — 2026-05-21

### Identity Upgrade
**FROM:** zeref-skills-fleet — CEO-level strategic execution OS
**TO:** zeref-agent-os — Context Engine + Agent Harness OS

> Agent = Model + Harness. The model is a commodity. The harness is the moat.

### Architecture: 5-Layer → 7-Layer OS
| Layer | Name |
|-------|------|
| 0 | Activation Kernel (ZEREF.md, ZEREFOS.md, CLAUDE.md) |
| 1 | Context Engine (zeref-context-engine, ZEREFPROJECT.md) |
| 2 | Skill Execution Fleet (109 skills, 9 guilds) |
| 3 | Memory / Knowledge (wiki hot/index/log) |
| 4 | Quality Harness (QA gate, trust sentinel, register audit) |
| 5 | Self-Improvement Loop (experience.jsonl, self_eval.py) |
| 6 | Automation / Delivery (install script, marketplace, CI) |

### Agents: 2 → 8 (Privilege-Scoped Pipeline)
Added:
- `zeref-context-engine` — grills user context, creates ZEREFPROJECT.md
- `zeref-memory-keeper` — single writer to wiki/ (hot/index/log)
- `zeref-evaluator` — quality scoring, READ only
- `zeref-trust-sentinel` — classifies untrusted content before routing
- `zeref-release-governor` — 3-lane skill deployment (experimental/staging/main)
- `zeref-council-convener` — multi-model debate (Opus 4.7, cost warning required)

Upgraded:
- `zeref-fleet-router` — orient auto-run, trust pre-check, council gate, model tier routing
- `zeref-executive-qa-agent` — mid-task checkpoints, register-aware review, hard READ-ONLY scope

### Skills: 104 → 109
New skills added:
- `zeref-ux-register-classifier` — brand vs. product register classification
- `zeref-biz-opportunity-solution-analyst` — Teresa Torres OST framework
- `zeref-dev-ui-quality-enforcer` — 10-category UI priority audit
- `zeref-system-memory-ingest` — wiki save/ingest skill
- `zeref-system-memory-lint` — wiki health audit skill

### All 109 Skills: Frontmatter Upgrade
Every skill upgraded from thin v2 frontmatter to rich v3 frontmatter:
- `trigger_phrases` — enables precision routing vs. probabilistic description matching
- `model_preference` — Haiku/Sonnet/Opus tier routing per skill
- `risk_level` — low/medium/high for routing confidence
- `dependencies` — references/zeref-qa-gate.md + zeref-safety-principles.md

### Specialist Injections (11 skills)
1. `zeref-system-caveman-compressor` — 4 intensity levels + Auto-Clarity Rule
2. `zeref-ux-design-qa-auditor` — 10-category priority framework
3. `zeref-ux-accessibility-specialist` — Priority 1/2 checks + motion accessibility
4. `zeref-ux-product-designer` — Step 0: Register Classification
5. `zeref-ux-interaction-designer` — Motion gap analysis protocol
6. `zeref-cnt-copywriter` — AI prose anti-patterns
7. `zeref-cnt-linkedin-ghostwriter` — validateProse discipline
8. `zeref-dev-code-quality-reviewer` — Karpathy overcomplicate test
9. `zeref-hq-chief-product-officer` — Opportunity-Solution Tree integration
10. `zeref-biz-kpi-analyst` — North Star framework
11. `zeref-final-executive-reviewer` — Register-aware review gate (Step 0)

### Memory Layer (New)
- `wiki/hot.md` — active session cache (max 500 words, last 3 sessions)
- `wiki/index.md` — domain knowledge map
- `wiki/log.md` — append-only operation history
- `/zeref-save` `/zeref-orient` `/zeref-recall` — 3 memory commands (TOML)
- `ZEREFPROJECT.md` — per-project context template (12-field scaffold)

### Self-Improvement Loop (New)
- `experience.jsonl` — append-only session log
- `zeref-trace.jsonl` — routing trace
- `scripts/self_eval.py` — weekly pattern analysis
- `scripts/skill_updater.py` — approval-gated skill updates (approved:true required)
- `/zeref-weekly-report` command

### Cross-Agent Portability (New)
- `ZEREF.md` — universal harness identity (Claude Code entrypoint)
- `AGENTS.md` — Codex-compatible identity
- `GEMINI.md` — Gemini CLI identity + skill discovery
- `zeref-install.sh` — one-command multi-runtime install

### Infrastructure (New)
- `scripts/zeref-validate.py` — fleet validation script
- `.github/workflows/zeref-validate.yml` — CI validation on push
- `references/zeref-safety-principles.md` — 7 constitutional rules with WHY explanations
- `references/zeref-qa-gate.md` — universal QA checklist
- `zeref-mcp-stack.md` — 5-tier MCP connector documentation
- `plugin.json` — updated: name `zeref-agent-os`, v3.0.0, adds agents + references fields

### Three Hard Limits (Publicly Declared)
1. Fully autonomous cross-session memory — est. resolved 2027–2028
2. Fully autonomous self-improvement without human review — est. resolved 2028+
3. Horizontal scaling at enterprise volume — est. resolved 2027

---

## [2.1.0] — 2026-05-18

### Fleet Consolidation — 112 → 102 Active Skills

**Retired (18 skills)** — replaced by broader or unified skills, or removed as low-value:

| Skill | Reason |
|-------|--------|
| `zeref-dev-ios-engineer` | Absorbed into `zeref-dev-mobile-engineer` |
| `zeref-dev-android-engineer` | Absorbed into `zeref-dev-mobile-engineer` |
| `zeref-dev-firebase-specialist` | Absorbed into `zeref-dev-cloud-infrastructure-engineer` |
| `zeref-dev-mongodb-specialist` | Covered by `zeref-dev-database-architect` |
| `zeref-dev-github-repository-manager` | Covered by `zeref-dev-devops-engineer` |
| `zeref-dev-technical-documentation-writer` | Covered by `zeref-cnt-documentation-writer` |
| `zeref-biz-grant-funding-analyst` | Low routing frequency, niche scope |
| `zeref-cnt-ux-case-study-writer` | Merged into `zeref-cnt-case-study-writer` |
| `zeref-cnt-technical-case-study-writer` | Merged into `zeref-cnt-case-study-writer` |
| `zeref-cnt-visual-asset-prompt-engineer` | Low routing frequency, easily handled inline |
| `zeref-qa-lead` | Role absorbed by routing model (ZEREFOS selects QA gate) |
| `zeref-qa-analytics-specialist` | Covered by `zeref-mkt-analytics-specialist` |
| `zeref-qa-marketing-auditor` | Covered by `zeref-mkt-chief-marketing-strategist` |
| `zeref-qa-rubric-alignment-auditor` | Low routing frequency, redundant with final gate |
| `zeref-hq-chief-operating-officer` | Scope overlap with `zeref-biz-operations-strategist` |
| `zeref-hq-fleet-activator` | Role absorbed by `zeref-system-skill-router` + routing model |
| `zeref-hq-quality-gatekeeper` | Replaced by 2-tier QA gate model |
| `zeref-mkt-affiliate-marketing-strategist` | Low routing frequency, niche scope |

**Added (8 skills)** — new capabilities and consolidations:

| Skill | Purpose |
|-------|---------|
| `zeref-dev-mobile-engineer` | Unified cross-platform mobile (iOS + Android + React Native/Expo) |
| `zeref-dev-cloud-infrastructure-engineer` | Cloud, serverless, BaaS, containers (absorbs firebase-specialist) |
| `zeref-dev-test-engineer` | Automated testing strategy and implementation |
| `zeref-dev-agentic-workflow-engineer` | AI agent design, LLM pipelines, MCP, multi-agent orchestration |
| `zeref-system-live-researcher` | Real-time web research and source synthesis |
| `zeref-ux-motion-designer` | Motion systems, animation specs, Lottie/Framer |
| `zeref-biz-startup-operator` | Zero-to-one startup execution, early-stage operations |
| `zeref-cnt-case-study-writer` | Unified case study skill (UX + technical) |

**QA Architecture change:**
- Introduced **2-tier QA gate model**
  - Tier 1: Domain-specific QA skill (functional, accessibility, UI consistency, etc.)
  - Tier 2: `zeref-final-executive-reviewer` for any deliverable leaving the workspace

**Registry:**
- `registry/zeref-skill-registry.json` rebuilt from active skill files → 102 entries, v2.1.0

**Wiki:**
- All 8 fleet domain pages updated with new counts and routing tables
- `wiki/brain/02_fleet_map.md` updated to reflect 102 active skills
- `wiki/hot.md` + `wiki/log.md` updated

---

## [2.0.0] — 2026-05-12

### Full OS Rebuild — V1 Fleet → V2 Architecture

- **Plugin manifest:** `.claude-plugin/plugin.json` created and validated
- **Skill architecture:** All skills converted to subdirectory format (`skills/[name]/SKILL.md`)
- **Shared references layer:** `references/shared-token-discipline.md`, `references/shared-anti-hallucination.md`
- **Registry:** `registry/zeref-skill-registry.json` — machine-readable skill index (112 skills)
- **Commands:** 9 commands converted to `.md` format (zeref-activate, orient, save, recall, handoff, ship, audit, validate, install-web-stack)
- **Agents:** `zeref-fleet-router`, `zeref-executive-qa-agent`
- **Wiki memory layer:** `wiki/` scaffold — hot.md, index.md, log.md, brain/ (7 files), fleet/ (9 domain pages)
- **Output styles:** `output-styles/zeref-executive.md`
- **GitHub:** Pushed to `https://github.com/kanadhiayash/zeref-agent-os`
- **CI:** `.github/workflows/zeref-sync-skills.yml` — validates skills on push to main

---

## [1.1.2] — 2026-05-07

### Marketplace Release

- Plugin installed via Claude Code marketplace
- 112 skills across original domain structure
- `plugin.json` v1.1.2 registered under `zeref-skills` marketplace

---

## [1.0.0] — 2026-05-06

### Initial Fleet

- Original 112-skill fleet scaffold
- Flat SKILL.md structure
- No registry, no commands, no wiki
