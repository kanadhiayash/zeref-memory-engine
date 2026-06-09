# Changelog — Zeref OS

All notable changes to **Zeref OS** are documented here.

Versioning: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.

Full pre-rebrand history (Skills Fleet → Agent OS → Zeref 4.x) is preserved in [`CHANGELOG-LEGACY.md`](CHANGELOG-LEGACY.md).

---

## [2.6.0] — 2026-06-08

> **v2.6 Auto-Gated Execution — 4-gate chain shipped (budget → router → fleet → prompt → handoff)**

Zeref shifts from reactive memory engine to proactive auto-gated execution system. Every major task passes four sequential gates — budget classification → skill-stack selection → prompt restructuring → model-tier routing — before a single execution-model token is spent. Gates declare themselves inline so the user sees and can override.

### Skills (+4)

- `budget-governor` — UPDATED. 2026 Anthropic pricing matrix (Haiku 4.5 / Sonnet 4.6 / Opus 4.7). New §Cost Weight Classification (CRITICAL / HIGH / MEDIUM / LOW). New §Auto-Activation Rule (6 steps). Legacy Free / Standard / God Mode aliases preserved for `tests/scores-v*.csv` back-compat.
- `skill-router` — NEW (Gate #2). Maps task domain → smallest-useful-stack (1 lead + 2-3 support + 1 QA). Never activates all 14 skills.
- `fleet-activator` — NEW. Live-probes ECC / claude-obsidian / Graphify / browser-harness / notebooklm / gstack reachability. Names gap + proposes emulator if unreachable.
- `prompt-context-engine` — NEW (Gate #3). Classifies STRUCTURED / SEMI-STRUCTURED / UNSTRUCTURED. Rewrites UNSTRUCTURED into `<objective>/<deliverable>/<constraints>/<context>/<success_criteria>` brief with 30-second auto-approve. Adapted from upgrade-plan source; Notion + Linear blocks dropped (not applicable to this repo).
- `caveman-handoff` — NEW (Session C). Compresses session handoff into caveman-grammar payload that survives cross-model switches. Companion to `handoff-compiler`.

### Skills count: 10 → 14

### AGENTS.md (+2 Core Principles, +2 sections, Skills table +4)

- Core Principle 13: Cost-Weight Auto-Gate.
- Core Principle 14: Task-Weight Model Routing.
- New `## Auto-Activation Gates` section (3 gates).
- New `## Model-Tier Routing` section (weight → model matrix + cascade pattern + hard constraints + per-skill audit).

### `_shared/rules.md` (+R6)

- R6 — Zero Context Loss. Every fact / named entity / constraint from raw prompt survives restructure, routing, handoff. Forward dependency: caveman-handoff carries the brief diff across model switches.

### Registry

- `zeref-registry.json`: 10 → 14 entries (skill-router, fleet-activator, prompt-context-engine, caveman-handoff added).

### Model audit

All 14 skills' `model` fields audited against weight matrix. No LOW→opus or CRITICAL→haiku mismatches. Borderline: `privacy-abstraction` (`risk_level: high`, `model: haiku`) kept on Haiku — deterministic REDACT.md rules suffice; tracked as forward signal for `pattern-observer`.

### Rubric impact

- Execution: cost-discipline by construction; mismatches surface before token spend.
- Engineer Credibility: every session declares stack + weight + brief inline — grep-able evidence of professional workflow design.
- Operational Readiness: extended-tool reachability live-probed rather than assumed.

### Migration notes

- Existing `tests/scores-v*.csv` referencing Free / Standard / God Mode labels continue to work via aliases mapped in `budget-governor` §Tier table.
- No SKILL.md content changes to the original 10 skills beyond `budget-governor` rewrite.
- No core memory / privacy / single-writer architecture touched.

---

## [2.5.0] — 2026-06-05

> **v2.5 Deep Audit Campaign — 6 phases shipped (A-F)**

**Rubric:** 8.00/10 (from 7.13 audit-corrected v2.0)
**Security:** 0 CRITICAL open (from 2 post Phase C)
**Tests:** 85-claim audit + 300 sandbox rows + 8 attacks + 20 live structural + 8 connector scenarios + 50 spec files
**Workarounds shipped:** L1-L11 (V07, L12 deferred to v2.6)

### Phase A — Claim Inventory + Evidence Grading
- `tests/claims.csv` (85 rows), `tests/claims-audit.md`
- 71% VERIFIED, 22% PARTIAL, 7% UNVERIFIED, 0% FALSE
- 5 contradictions K1-K5

### Phase B — Sandbox Stress Test
- `tests/sandbox/<skill>/{normal,edge,adversarial,recovery,drift}.md` — 50 specs
- `tests/scores-vB.csv` — 300 rows (10 × 5 × 6)
- `tests/phase-b-summary.md`
- Adversarial 4.77 best, Recovery 3.93 → new L10 atomic writes

### Phase C — Security + Vulnerability Hunt
- `tests/security-audit-vC.md` — 8 attacks + 4-vuln sweep, CVSS-scored
- 2 CRITICAL, 3 HIGH, 1 MEDIUM, 3 PASS

### Phase D — Operational Workarounds (L1-L11)
- L1 PII regex tightened (verb-prefix lookahead) — `zeref/privacy.py`
- L2 `email` class default-enabled in REDACT.md → closes V01+V02 CRITICAL
- L3 `tests/runner.py` — structural (20/20) + LLM modes; unblocks ZRF-B05/B08 scaffold
- L4 `zeref db-status` backend report
- L5 `zeref init` scaffolds memory + config (closes K3)
- L6 Dogfood: `config/PROJECT.md` populated (closes K1)
- L7 `tests/connector-stub.md` (closes K8)
- L8 `skills/drafts/grep-with-context/` (closes K10)
- L9 `zeref/lock.py::MemoryLock` (closes V06 + V11)
- L10 `zeref/lock.py::atomic_write/atomic_append` (closes Recovery gap)
- L11 `zeref write-decision` scrubs PII before disk (closes V12)
- `tests/scores-vD-live.csv` 20/20 PASS
- `tests/phase-d-summary.md`

### Phase E — Rubric Re-Scoring
- `tests/zeref-rubric-v2.5.md` — every dim cited
- Vision 9, Execution 8, Doc 8, Architecture 8, Operational 7, Portfolio 8, Investor 8, Engineer 8
- ZRF: 6 PASS + 4 SCAFFOLD-READY (was 6+3 DEFER+1 BASELINE)

### Phase F — UX Polish
- `README.md` badges: v2.5, rubric 8.0/10, 0 CRITICAL, 20/20 live, v1.0.0 source-of-truth
- `QUICKSTART.md` — 5-step onboarding
- `TASKS.md` + `memory/glossary.md` + `memory/projects/zeref-os.md` + `dashboard.html`

### Known Limitations (v2.6 candidates)
- L12 connector rate limiter
- V07 permission override sentinel
- "Will Smith" famous-name false-negative (L1 trade-off)
- LLM-mode pass^3 needs live API runs
- Cross-harness parity ZRF-B07 needs Cursor/Aider/Gemini live runs

### Bloat Log
- Phase A actual $110 vs $80 est (+$30)
- Phase B actual ~$17 vs $350-450 est (programmatic generation saved $330+)
- Phase C-F batched in single session vs phased estimate
- Total worktree files modified: 36 (target ~25, +44%)

## [2.0.0] — 2026-06-03

> **v2.0 Complete — Sprints 1-4**

**ZRF Scores (v2.0):** Execution 8/10 (+4 from v1.0) | Engineer Credibility 9/10 (+2) | Operational Readiness 6/10 (+3)
**Test count:** 40 score rows (20 tasks × 2 versions) | 2 eval-harness specs | 20-task demo suite

### Sprint 4 — Distribution + Demo
- **`pyproject.toml`** — `pipx install zeref-os`. Zero mandatory deps; extras: `[llm]`, `[duckdb]`, `[yaml]`, `[all]`. Entry point: `zeref = "zeref.cli:main"`.
- **`zeref/demo.py`** — `zeref demo`: 20 structural checks in temp sandbox, green/red report, auto-cleanup. Fully offline (no LLM).
- **Rebrand note:** Panel didn't defend "OS" name. v2.1+ recommendation: rename to "Zeref", keep "OS" in tagline.

### Sprint 3 — Structured Data + Cross-Harness
- **`zeref/db.py`** — `snapshot()`: DECISIONS.md + PATTERNS.jsonl + CONFLICTS.md → SQLite (`memory/snapshots/YYYY-MM-DD/zeref.db`). Optional DuckDB `.parquet`. `query(sql)` against latest snapshot. Markdown stays canonical.
- **`zeref/dashboard.py`** — `zeref dashboard`: reads `tests/scores-v*.csv`, generates `tests/dashboard.html` (Chart.js, self-contained, no server).
- **`tests/cross-harness-parity.md`** — ZRF-B07 baseline (4.63 Claude Code). P01-P04 parity matrix. Cursor/Aider/Gemini pending live runs.
- **`SOUL.md`** — principle 6 added: "Structured Memory Compounds Faster."
- **`tests/scores-v2.0.0.csv`** — 20-task regression suite scored at v2.0.0 baseline.

### Sprint 2 — Runtime + Privacy-as-Code
- **`zeref/privacy.py`** — Deterministic PII scrubber: NFKC normalize → homoglyph table → base64 decode → regex redact. 7 built-in classes; credentials always-on. `scrub()` + `audit()`.
- **`zeref/cli.py`** — CLI: `status`, `write-decision`, `grade`, `audit-privacy`, `audit`, `dashboard`, `demo`. `grade` heuristic + litellm fallback.
- **`zeref/__init__.py`** + **`zeref/__main__.py`** — package entry points.
- **`tests/eval-harness/wiki-maintenance.md`** — 3 tests (normal/edge/adversarial) with rubric.
- **`tests/eval-harness/privacy-abstraction.md`** — 4 tests including base64 + homoglyph adversarial.

## [2.0.0-sprint1] — 2026-06-03

> **v2.0 Sprint 1 — Contracts + Routing Precision**
>
> Converts prose specs into machine-readable contracts. Adds SOUL.md ethos document, zeref-registry.json routing catalog, shared rules extraction, and trigger precision rewrites. Locks Phase 0-6 baseline scores for compounding test discipline.

**ZRF Scores (post-Sprint 1):** Execution 7/10 (+1) | Engineer Credibility 9/10 (+1) | Operational Readiness 4/10 (unchanged — Sprint 2 target)
**Test count:** 20 regression tasks (baseline locked in `tests/scores-v1.0.0.csv`)

### Added

- **`SOUL.md`** — 5 operating principles (Spec-First/Test-Always, Privacy-Deterministic, Contracts-Over-Prose, Memory-Compounds, Boil-the-Lake). Step 0 of §0 reading order.
- **`zeref-registry.json`** — machine-readable skill catalog: triggers[], deliverables[], risk_level, support_skills[], model per skill. All 10 skills covered. Enables automated routing tests in Sprint 2.
- **`_shared/rules.md`** — 4 shared safety rules extracted from ≥3 skills (R1: Single-Writer+Privacy-Gate; R2: Non-Deletion/D9; R3: Privacy-Gate-on-External-Output; R4: Never-Invent). Reduces spec drift.
- **`tests/scores-v1.0.0.csv`** — Phase 3 regression baseline (20 tasks). Compounding from here.
- **`AGENTS.md`** §0: step 0 (SOUL.md), shared-rules pointer.

### Changed

- **`skills/wiki-maintenance/SKILL.md`** trigger section: expanded from 3 vague items to 9 concrete phrases
- **`skills/budget-governor/SKILL.md`** trigger section: clarified always-on vs. explicit-invocation vs. mid-session auto-trigger
- **`skills/project-setup/SKILL.md`** trigger section: disambiguated first-run vs. re-run (previously "first /start" was ambiguous)

## [1.0.0] — 2026-05-31

> **Canonical release. The first release under the Zeref OS name.**
>
> Years of local iteration (v1.x Skills Fleet → v2.x Agent OS → v3.x specialist build → v4.x context-and-memory engine) converge here. The plugin is renamed, the version clock resets, and the project takes its final form.

### Renamed

- Plugin: `zeref` → `zeref-os` (`.claude-plugin/plugin.json`, `marketplace.json`, `SKILL.md`)
- Display identity: "Zeref 4.x" → **Zeref OS** across all docs, agents, skills, commands, team packs, references, harness stubs, memory dogfood
- Slash command namespace: `/zeref:<command>` → `/zeref-os:<command>` (auto-derived from plugin name)
- Skill invocation: `zeref:<name>` → `zeref-os:<name>` (auto)
- Script: `scripts/zeref-validate-v4.py` → `scripts/zeref-validate.py`
- Changelog: prior history preserved at `CHANGELOG-LEGACY.md`

### Reset

- Version: `4.3.0` → `1.0.0` in `plugin.json`, `marketplace.json`, `SKILL.md`
- All other tags purged (v1.1 / v2.0 / v2.1 / v3.0.0 / v4.0.0 / v4.1.0 / v4.2.0 / v4.3.0) — single tag `v1.0.0` from this commit forward
- All branches purged except `main`

### Added (over the v4.3 baseline)

- **`assets/zeref-os-hero.png`** + **`assets/zeref-os-icon.png`** — pixel-art hero (hooded dark mage with floating ancient tomes) and square icon for repo avatar
- **README** rewritten: hero image, inspiration narrative (Fairy Tail's Zeref Dragneel), journey table tracing every iteration since v1.x, mermaid architecture + sequence diagrams, decision-log highlights, engineering inspirations from the wider community (AGENTS.md standard, Karpathy paradigm shifts, BMAD-METHOD, GitHub Spec Kit, Anthropic CLAUDE.md guides, claude-evolve, obsidian-PKM, and others)
- **GitHub Wiki** (12 pages): Home, Installation, Architecture, Memory Model, Privacy Model, Team Packs, Pattern Detection, Decision Log, Model Debates, Versioning History, FAQ, Glossary, Inspirations

### Preserved unchanged from v4.3.0

- All capability surface (6 agents, 10 skills, 8 commands, 6 team packs)
- Flat `memory/` layout
- Root `PRIVACY.md` + `REDACT.md` + `SHARING_POLICY.md`
- `references/v4x-canon/` — imported design canon left as historical reference
- Migration script `scripts/migrate-v4.2-to-v4.3.py` — kept for any users migrating from prior local v4.x installs

### Breaking changes

- **Plugin install command changed.** Existing `zeref@zeref` installs must:
  ```bash
  claude plugin uninstall zeref@zeref
  claude plugin install zeref-os@zeref-os
  ```
- Slash commands now under `/zeref-os:` namespace.
- Skills invoke as `zeref-os:<name>` via the Skill tool.

No data migration required — all memory files (`memory/`, `PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md`, `config/`) keep their paths and content.

---

For the full history before v1.0.0 (Zeref Skills Fleet v1.x, Zeref Agent OS v2.x, Zeref OS v3.x, Zeref 4.0–4.3 context-and-memory engine), see [`CHANGELOG-LEGACY.md`](CHANGELOG-LEGACY.md).
