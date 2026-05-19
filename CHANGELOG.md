# Changelog

All notable changes to Zeref OS are documented here.

Format: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`

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
