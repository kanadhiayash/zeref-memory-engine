# Changelog

All notable changes to Zeref Agent OS are documented here.

Format: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`

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
