# Zeref OS — Agent Operating System for Claude

**Version:** 3.0.0 | **License:** MIT | **Skills:** 109 | **Commands:** 11 | **Agents:** 8

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-orange.svg)](https://github.com/kanadhiayash/zeref-os)
[![Skills](https://img.shields.io/badge/skills-109-green.svg)](skills/)
[![Version](https://img.shields.io/badge/version-3.0.0-purple.svg)](.claude-plugin/plugin.json)

Built by [Yash Kanadhia](https://github.com/kanadhiayash) · Toronto · 2026

---

## What is Zeref OS?

Zeref is a **102-skill AI execution operating system** built on top of Claude. It is not a chatbot configuration or a simple prompt template — it is a structured fleet of specialist AI skills that transforms Claude from a generic assistant into a coordinated team of experts.

**Zeref is not a tool you use. It is an OS you run.**

Every session starts by loading a kernel (`ZEREFOS.md`), reading the current context (`wiki/hot.md`), and routing each task to the minimum useful skill stack: one lead specialist, zero to three support skills, and zero to one quality gate. No over-loading. No hallucinated expertise. No generic outputs.

The system was built for **Yash Kanadhia** — a Toronto-based UX/Product Designer, Mobile Product Builder, and AI workflow operator — as a personal execution OS that compresses chaos into systems, systems into deliverables, and deliverables into professional proof of work.

---

## Inspiration

Zeref OS was built at the intersection of three ideas:

### 1. Karpathy-Style LLM Operation
Andrej Karpathy's principles for working with LLMs — think before coding, simplicity first, surgical changes only, no invented behavior, verify before claiming success — are baked directly into ZEREFOS.md as non-negotiable operating rules. These aren't suggestions. Every skill and every agent in this fleet enforces them.

### 2. Tiago Forte's Second Brain (PARA)
The wiki memory layer is inspired by Building a Second Brain and the PARA method. The vault is structured for capture, organization, distillation, and expression — with `hot.md` as the session handshake, `brain/` as the knowledge hub, and domain pages as the long-term memory that survives across sessions.

### 3. FAANG Execution Discipline
The skill fleet is modeled on how high-performing product teams actually operate — specialists with clear scope, explicit handoff protocols, defined deliverable formats, and quality gates before anything ships. Instead of one generalist AI, Zeref gives you a UX Designer, a Backend Engineer, a KPI Analyst, a QA Lead, and 108 more specialists, each with a defined role and explicit "When NOT To Use" constraints.

---

## AI Usage

This OS was built with AI at every layer — and that is intentional and documented:

| Layer | AI Involvement |
|-------|---------------|
| **Architecture design** | Claude (Sonnet) designed the 9-layer skill architecture, routing model, and anti-hallucination framework through iterative conversation |
| **Skill generation** | 102 skill files in active fleet (18 legacy skills retired in v2.1.0), reviewed, and refined using Claude with structured prompts and YAML frontmatter templates |
| **Routing logic** | ZEREFOS routing table was built by analyzing task taxonomies and testing routing decisions across real work sessions |
| **Wiki brain** | Obsidian wiki structure, brain folder, and domain pages were generated and organized with Claude Code using the `wiki-ingest` skill |
| **Registry generation** | `zeref-skill-registry.json` is auto-generated from skill file frontmatter using a Python script |
| **Validation** | `zeref-validate.py` was written to enforce skill file schema and catch structural drift |
| **CI/CD** | GitHub Actions workflow validates all skills on every push to `main` |

**Why document AI usage?** Because Zeref is itself proof of work. The system demonstrates that AI-assisted infrastructure can be rigorous, documented, validated, and portfolio-worthy — not just fast.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ZEREF OS v3.0                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Layer 0 — ZEREFOS.md (Kernel)                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Identity · Routing Rules · Karpathy Principles · Caveman Triggers│  │
│  │  Anti-Hallucination · Token Discipline · Register Classification  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              ↓                                           │
│  Layer 1 — Skill Router                                                 │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Task Type: UX / DEV / PM / CNT / SYS / BIZ / HQ / FIN          │  │
│  │  Register: BRAND / PRODUCT / PORTFOLIO / OPERATIONS / CONTENT    │  │
│  │  Stack: 1 Lead + 0–3 Support + 0–1 QA Gate                       │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              ↓                                           │
│  Layer 2 — Skill Fleet (109 active skills)                                     │
│  ┌────────────┬─────────────┬─────────────┬─────────────────────────┐  │
│  │ HQ (5)     │ UX (19)     │ Dev (16)    │ Biz (15)                │  │
│  │ Mkt (15)   │ Cnt (15)    │ QA (11)     │ Final (4) · System (9)  │  │
│  └────────────┴─────────────┴─────────────┴─────────────────────────┘  │
│                                                                         │
│  Layer 3 — Shared References                                            │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  shared-token-discipline.md · shared-anti-hallucination.md        │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  Layer 4 — Memory / Wiki (Obsidian Vault)                               │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  hot.md → index.md → brain/ → fleet/ → projects/ → concepts/     │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  Layer 5 — Infrastructure                                               │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  zeref-validate.py · registry/ · .github/workflows/ · commands/  │  │
│  │  agents/ (8 privilege-scoped agents)                              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### Routing Model
Zeref classifies every task by **type** (UX, DEV, PM, CNT, SYS, BIZ, HQ, FIN) and **register** (BRAND, PRODUCT, PORTFOLIO, OPERATIONS, CONTENT), then routes to the **minimum useful stack**:

```
Lead:     1 skill — primary executor
Support:  0–3 skills — only if they meaningfully change output
QA Gate:  0–1 skill — only when quality risk is high
Caveman:  yes/no — only when context is long or crossing environments
```

Over-routing wastes tokens and dilutes responsibility. Under-routing misses specialist judgment. The routing table in ZEREFOS.md encodes the right defaults.

### Memory Protocol
Sessions are stateless by default. Zeref solves this with a layered wiki memory:

```
hot.md (≤500 words) → session state, read first
index.md → full page catalog
brain/00_master.md → entry point
domain pages → fleet, projects, concepts, decisions
```

At session end, `/zeref-save` triggers `zeref-system-caveman-compressor`, which compresses context into a handoff brief and updates `hot.md`. Code, commands, paths, URLs, and error messages are preserved verbatim. Prose is compressed.

### Anti-Hallucination Discipline
Built into every skill via `references/shared-anti-hallucination.md`:
- Never invent file contents, API responses, or repo state
- State unknowns explicitly
- Verify before claiming success
- Preserve exact values: paths, commands, URLs, errors, configs

### Token Discipline
Built into every skill via `references/shared-token-discipline.md`:
- Use smallest context set that produces a correct result
- Don't load unnecessary skill files
- Don't repeat background already established
- Four token tiers: XS / S / M / L — each skill declares its tier

### Karpathy Principles (Non-Negotiable)
Applied to every code and system task:
1. Think before coding
2. Simplicity first
3. Surgical changes only
4. No invented behavior
5. Verify before claiming success
6. Expose uncertainty
7. Preserve exact values
8. One concern per change

---

## How to Use

### Quick Start (3 steps)

**1. Install the plugin**
```
Claude Code → Plugins → Add Plugin
→ https://github.com/kanadhiayash/zeref-os
```
Or: download the repo ZIP → Claude Code → Plugins → Import from ZIP

**2. Activate the kernel**
```
Claude → Project Instructions → Paste contents of ZEREFOS.md
```

**3. Start a session**
```
/zeref-activate
```

→ [Full installation guide →](INSTALL.md)

---

### Slash Commands (9)

| Command | What It Does |
|---------|-------------|
| `/zeref-activate` | Load hot.md, state current context, select working register |
| `/zeref-orient` | Map codebase/project structure before executing |
| `/zeref-save` | Compress session with Caveman, update hot.md and log.md |
| `/zeref-recall` | Reload prior session context from wiki |
| `/zeref-handoff` | Package work for cross-environment or cross-person handoff |
| `/zeref-ship` | Final quality gate — Go/No-Go before shipping |
| `/zeref-audit` | Audit fleet health, registry count, plugin.json consistency |
| `/zeref-validate` | Run zeref-validate.py against all skill files |
| `/zeref-install-web-stack` | Scaffold a new web project with stack and tooling |

---

## Skill Fleet — All 102 Active Skills

### HQ — Executive (8)

| Skill | Role |
|-------|------|
| zeref-hq-chief-product-officer | Product vision, roadmap, strategic direction |
| zeref-hq-chief-strategy-officer | Business strategy, competitive positioning |
| zeref-hq-chief-operating-officer | Operations, process design, execution |
| zeref-hq-chief-of-staff | Cross-functional coordination |
| zeref-hq-chief-research-officer | Research strategy and synthesis |
| zeref-hq-documentation-architect | Documentation systems and structure |
| zeref-hq-fleet-activator | Fleet activation and routing orchestration |
| zeref-hq-quality-gatekeeper | Cross-domain quality gate |

### UX — Design (16)

| Skill | Role |
|-------|------|
| zeref-ux-product-designer | End-to-end UX/product design |
| zeref-ux-interaction-designer | Interaction patterns and micro-interactions |
| zeref-ux-user-flow-designer | User flows and navigation architecture |
| zeref-ux-design-systems-architect | Design systems, tokens, component libraries |
| zeref-ux-visual-designer | Visual design and brand expression |
| zeref-ux-information-architect | IA, taxonomy, navigation |
| zeref-ux-prototype-specialist | Interactive prototyping |
| zeref-ux-figma-architecture-specialist | Figma file structure and organization |
| zeref-ux-accessibility-specialist | WCAG, contrast, inclusive design |
| zeref-ux-design-qa-auditor | Design QA before dev handoff |
| zeref-ux-developer-handoff-lead | Design-to-code handoff and specs |
| zeref-ux-research-lead | User research strategy and synthesis |
| zeref-ux-synthetic-research-analyst | AI-assisted research simulation |
| zeref-ux-persona-strategist | Persona creation and audience mapping |
| zeref-ux-problem-definition-specialist | Problem framing and HMW statements |
| zeref-ux-writer | UX copy, microcopy, empty states |

### Development (17)

| Skill | Role |
|-------|------|
| zeref-dev-fullstack-engineer | Full-stack development |
| zeref-dev-frontend-engineer | Frontend implementation |
| zeref-dev-backend-engineer | Backend and APIs |
| zeref-dev-android-engineer | Android/mobile development |
| zeref-dev-ios-engineer | iOS development |
| zeref-dev-ai-systems-engineer | AI/ML systems and LLM integration |
| zeref-dev-api-integration-engineer | API integration and connectors |
| zeref-dev-firebase-specialist | Firebase, Firestore, Cloud Functions |
| zeref-dev-database-architect | Database design and optimization |
| zeref-dev-mongodb-specialist | MongoDB and NoSQL |
| zeref-dev-devops-engineer | CI/CD, deployment, infrastructure |
| zeref-dev-github-repository-manager | GitHub repos, PRs, releases |
| zeref-dev-security-engineer | Security review and threat modeling |
| zeref-dev-solution-architect | Solution design and system integration |
| zeref-dev-technical-architect | Technical architecture and patterns |
| zeref-dev-code-quality-reviewer | Code review and quality gate |
| zeref-dev-technical-documentation-writer | Technical docs and READMEs |

### Business (14)

| Skill | Role |
|-------|------|
| zeref-biz-business-strategist | Business strategy and model design |
| zeref-biz-business-validator | Business idea validation |
| zeref-biz-competitive-intelligence-analyst | Competitive research and SWOT |
| zeref-biz-financial-analyst | Financial modeling and projections |
| zeref-biz-grant-funding-analyst | Grant research and applications |
| zeref-biz-investor-pitch-strategist | Pitch decks and investor narrative |
| zeref-biz-kpi-analyst | KPI frameworks and north star |
| zeref-biz-legal-advisor | Legal review and risk identification |
| zeref-biz-market-research-analyst | Market sizing and industry research |
| zeref-biz-monetization-strategist | Revenue model and pricing strategy |
| zeref-biz-operations-strategist | Ops planning and process optimization |
| zeref-biz-partnership-strategist | Partner outreach and co-marketing |
| zeref-biz-product-market-fit-analyst | PMF hypothesis and validation |
| zeref-biz-risk-analyst | Risk assessment and mitigation |

### Marketing (16)

| Skill | Role |
|-------|------|
| zeref-mkt-chief-marketing-strategist | Marketing strategy and brand direction |
| zeref-mkt-brand-strategist | Brand positioning and identity |
| zeref-mkt-positioning-strategist | Competitive positioning and messaging |
| zeref-mkt-gtm-strategist | Go-to-market and launch planning |
| zeref-mkt-growth-marketer | Growth, acquisition, retention |
| zeref-mkt-content-marketing-strategist | Content strategy and editorial |
| zeref-mkt-seo-strategist | SEO strategy and keyword research |
| zeref-mkt-analytics-specialist | Marketing analytics and attribution |
| zeref-mkt-performance-marketing-specialist | Paid advertising and campaigns |
| zeref-mkt-affiliate-marketing-strategist | Affiliate programs and partner marketing |
| zeref-mkt-email-marketing-specialist | Email campaigns and sequences |
| zeref-mkt-community-strategist | Community building and engagement |
| zeref-mkt-pr-communications-specialist | PR, press, and media relations |
| zeref-mkt-social-media-strategist | Social media strategy and content |
| zeref-mkt-personal-branding-strategist | Personal brand and thought leadership |
| zeref-mkt-conversion-rate-optimizer | CRO, landing pages, A/B strategy |

### Content (16)

| Skill | Role |
|-------|------|
| zeref-cnt-copywriter | Persuasive on-brand copy |
| zeref-cnt-linkedin-ghostwriter | LinkedIn posts in Yash's voice |
| zeref-cnt-long-form-writer | Articles, essays, newsletters |
| zeref-cnt-scriptwriter | Video and podcast scripts |
| zeref-cnt-seo-content-writer | SEO-optimized content |
| zeref-cnt-technical-case-study-writer | Technical case studies |
| zeref-cnt-ux-case-study-writer | UX/product case studies |
| zeref-cnt-documentation-writer | Product and process documentation |
| zeref-cnt-editorial-director | Editorial strategy and style |
| zeref-cnt-brand-voice-editor | Brand voice enforcement |
| zeref-cnt-content-qa-editor | Content QA and proofreading |
| zeref-cnt-repurposing-specialist | Cross-channel content repurposing |
| zeref-cnt-resume-career-writer | Resumes, cover letters, career docs |
| zeref-cnt-presentation-designer | Slide decks and pitch presentations |
| zeref-cnt-video-content-strategist | Video strategy and scripting |
| zeref-cnt-visual-asset-prompt-engineer | AI image and visual prompt engineering |

### QA — Quality Assurance (15)

| Skill | Role |
|-------|------|
| zeref-qa-lead | QA strategy and test planning |
| zeref-qa-functional-tester | Functional test execution |
| zeref-qa-accessibility-tester | Accessibility testing, WCAG |
| zeref-qa-ui-consistency-auditor | UI consistency and design fidelity |
| zeref-qa-ux-usability-tester | Usability testing and UX QA |
| zeref-qa-performance-tester | Performance and load testing |
| zeref-qa-security-tester | Security testing and vulnerability |
| zeref-qa-edge-case-tester | Edge cases and failure modes |
| zeref-qa-regression-tester | Regression testing |
| zeref-qa-ab-testing-strategist | A/B testing design and analysis |
| zeref-qa-analytics-specialist | Analytics QA and tracking validation |
| zeref-qa-marketing-auditor | Marketing QA and campaign audit |
| zeref-qa-rubric-alignment-auditor | Rubric and spec compliance |
| zeref-qa-final-quality-gatekeeper | Final QA gate before delivery |
| zeref-qa-launch-readiness-manager | Launch readiness and sign-off |

### Final — Delivery (4)

| Skill | Role |
|-------|------|
| zeref-final-executive-reviewer | Terminal Go/No-Go executive review |
| zeref-final-project-compiler | Project compilation and assembly |
| zeref-final-deliverable-packager | Packaging for handoff or release |
| zeref-final-source-validator | Source validation and citation checking |

### System — Infrastructure (6)

| Skill | Role |
|-------|------|
| zeref-system-caveman-compressor | Context compression and handoff briefs |
| zeref-system-skill-router | Dynamic skill routing |
| zeref-system-evidence-memory-keeper | Evidence collection and memory |
| zeref-system-marketplace-packager | Plugin packaging and marketplace prep |
| zeref-system-plugin-update-diagnostician | Plugin health diagnostics |
| zeref-system-token-budget-controller | Token economy enforcement |

---

## Wiki / Memory Layer

The repo ships with a seed wiki structure at `wiki/`. It starts minimal and grows as you work — each session appends context, each `/zeref-save` compresses the session into `hot.md`.

### Wiki Structure

```
wiki/
├── hot.md              ← Current session context (read first, max 500 words)
├── index.md            ← Domain knowledge map (updated as domains are covered)
├── log.md              ← Append-only operation log
├── concepts/           ← Architecture decisions, routing rules, data model
├── projects/           ← One page per active project
└── sources/            ← Reference links, ingested documents
```

### Memory Workflow

```
Session start:  /zeref-activate → reads hot.md → states context
During work:    Notes go to domain pages as decisions/artifacts are made
Session end:    /zeref-save → Caveman compresses → hot.md updated
```

---

## Validation

```bash
# Validate all 102 active skills
python3 zeref-validate.py

# Verbose output
python3 zeref-validate.py --verbose

# Single skill
python3 zeref-validate.py --file skills/zeref-ux-product-designer/SKILL.md
```

The validator checks:
- Required frontmatter: `name`, `description`
- Required sections: Mission, When To Use, When NOT To Use, Required Inputs, Deliverables, Workflow, Output Format, Token Discipline, Handoff Protocol
- Route references point to existing skill files

**CI:** Validation runs automatically on push to `main` (see `.github/workflows/`).

---

## Folder Structure

```
zeref-os/
├── README.md                          ← You are here
├── INSTALL.md                         ← Installation guide
├── ZEREFOS.md                         ← OS kernel (paste into Project Instructions)
├── CLAUDE.md                          ← Vault structure guide
├── zeref-validate.py                  ← Skill file validator
├── zeref-settings-recommended.json    ← Recommended Claude settings
├── .claude-plugin/
│   └── plugin.json                    ← Claude Code plugin manifest
├── .gitignore
├── skills/                            ← 102 active skill directories
│   └── <skill-id>/
│       └── SKILL.md
├── commands/                          ← 9 slash commands
├── agents/                            ← 2 subagents
├── references/                        ← Shared canonical rules
│   ├── shared-token-discipline.md
│   └── shared-anti-hallucination.md
├── output-styles/
│   └── zeref-executive.md
├── themes/
│   └── zeref-dark.json
├── registry/
│   └── zeref-skill-registry.json      ← Machine-readable index (102 active skills)
├── wiki/                              ← Obsidian vault (ships with package)
│   ├── brain/                         ← Master knowledge hub
│   ├── fleet/                         ← 9 skill domain pages
│   ├── projects/                      ← Project pages
│   ├── concepts/                      ← Concept pages
│   └── ...
└── .obsidian/                         ← Vault config (theme + settings)
```

---

## License

MIT License

Copyright (c) 2026 Yash Kanadhia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

---

## Contributing

This is personal infrastructure for Yash Kanadhia. It is not an open-source project accepting public contributions.

- No public pull requests
- No external contributors
- No issue tracker for feature requests

This repo exists as **proof of work**, **portfolio signal**, and **personal execution tooling**.

If you want to build your own version, fork the repo and adapt the architecture to your own operating system. Attribution appreciated but not required.

---

*Zeref OS v3.0.0 — Built by Yash Kanadhia | Toronto | 2026*
*109 active skills. 11 commands. 8 agents. One operating system.*
