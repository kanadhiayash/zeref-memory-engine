# Zeref Skills Fleet V2

**Personal AI Execution OS for Yash Kanadhia**
Version: 2.0.0 | License: MIT | Owner: [Yash Kanadhia](https://github.com/kanadhiayash)

---

## What is Zeref?

Zeref is a modular, role-based execution operating system built on top of Claude. It is not a chatbot configuration — it is a structured skills fleet that makes AI behave less like a generic assistant and more like a coordinated team of specialists. Zeref routes every task to the minimum required skill stack: one lead skill, one to three support skills, and one QA gate when needed. It enforces evidence discipline, workspace handoff readiness, token economy, and anti-hallucination rules across all 18 skills. For Yash Kanadhia — a Toronto-based UX/Product Designer, Mobile Product Builder, and AI workflow operator — Zeref is the execution layer that converts chaos into systems, systems into deliverables, deliverables into proof of work, and proof of work into professional leverage.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         ZEREF SKILLS FLEET V2                        │
├──────────────────────────────────────────────────────────────────────┤
│  Layer 7 — HQ / Executive                                            │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  zeref-hq-chief-product-officer  (executive, strategic gate) │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  Layer 6 — QA / Final                                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  zeref-final-executive-reviewer  (terminal QA gate)          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  Layer 4 — Business         Layer 3 — Content                       │
│  ┌────────────────────┐     ┌────────────────────────────────┐      │
│  │  biz-kpi-analyst   │     │  cnt-copywriter                 │      │
│  │  biz-opp-solution  │     │  cnt-linkedin-ghostwriter       │      │
│  └────────────────────┘     └────────────────────────────────┘      │
│                                                                      │
│  Layer 2 — Development                                               │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  dev-code-quality-reviewer  │  dev-ui-quality-enforcer   │       │
│  └──────────────────────────────────────────────────────────┘       │
│                                                                      │
│  Layer 1 — UX (Core Design Engine)                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  ux-product-designer  ux-design-systems-architect             │   │
│  │  ux-interaction-designer  ux-motion-designer (NEW)            │   │
│  │  ux-accessibility-specialist  ux-design-qa-auditor            │   │
│  │  ux-register-classifier (NEW)                                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Layer 5 — System          Layer 8 — Memory / Infrastructure        │
│  ┌─────────────────────┐   ┌──────────────────────────────────┐     │
│  │  caveman-compressor  │   │  memory-ingest (NEW)             │     │
│  └─────────────────────┘   │  memory-lint   (NEW)             │     │
│                             └──────────────────────────────────┘     │
│                                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│  ZEREFOS — Global Routing + Evidence Discipline + Anti-Hallucination │
│  ─────────────────────────────────────────────────────────────────  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Load ZEREFOS into Claude

Copy the contents of `ZEREFOS.md` (or `CLAUDE.md`) into your Claude Project Instructions or Custom System Prompt. This activates the global operating baseline, routing logic, and anti-hallucination rules.

```
Claude Project → Project Instructions → Paste ZEREFOS.md content
```

### 2. Load a hot.md context file (optional but recommended)

At the start of any session involving an active project, attach or paste your `hot.md` context file. This gives Zeref your most recent project state without requiring a recap.

### 3. Use slash commands

Zeref ships with activatable slash commands in `commands/`:

```
/zeref-activate    — Activates the skill stack for a task
/zeref-release     — Packages the fleet for release
```

### 4. Let ZEREFOS route automatically

ZEREFOS classifies your task and selects the minimum skill stack. You can also name a skill explicitly:

```
Use zeref-ux-product-designer to design the onboarding flow.
```

### 5. Run validation locally

```bash
python3 zeref-validate.py
python3 zeref-validate.py --verbose
python3 zeref-validate.py --file skills/zeref-ux-product-designer.md
```

---

## Folder Structure

```
zeref-skills-fleet/
├── README.md                          ← You are here
├── ZEREFOS.md                         ← Global operating baseline (load into Claude)
├── zeref-validate.py                  ← Skill file validator script
├── zeref-settings-recommended.json   ← Recommended Claude settings
│
├── skills/                            ← 18 V2 skill files
│   ├── zeref-system-caveman-compressor.md
│   ├── zeref-ux-design-qa-auditor.md
│   ├── zeref-ux-accessibility-specialist.md
│   ├── zeref-ux-interaction-designer.md
│   ├── zeref-ux-product-designer.md
│   ├── zeref-cnt-copywriter.md
│   ├── zeref-cnt-linkedin-ghostwriter.md
│   ├── zeref-dev-code-quality-reviewer.md
│   ├── zeref-hq-chief-product-officer.md
│   ├── zeref-biz-kpi-analyst.md
│   ├── zeref-final-executive-reviewer.md
│   ├── zeref-ux-design-systems-architect.md
│   ├── zeref-ux-motion-designer.md          ← NEW
│   ├── zeref-ux-register-classifier.md      ← NEW
│   ├── zeref-system-memory-ingest.md        ← NEW
│   ├── zeref-system-memory-lint.md          ← NEW
│   ├── zeref-biz-opportunity-solution-analyst.md  ← NEW
│   └── zeref-dev-ui-quality-enforcer.md     ← NEW
│
├── registry/
│   └── zeref-skill-registry.json     ← Machine-readable skill index (18 skills)
│
├── references/
│   ├── shared-token-discipline.md    ← Canonical token discipline rules
│   └── shared-anti-hallucination.md  ← Canonical anti-hallucination rules
│
├── commands/
│   ├── zeref-activate.md
│   └── zeref-package-release.md
│
├── agents/
│   ├── zeref-fleet-router.md
│   └── zeref-executive-qa-agent.md
│
├── output-styles/
│   └── zeref-executive.md
│
├── themes/
│   └── zeref-dark.json
│
├── memory/
│   ├── hot.md                         ← Current session context (update after each major session)
│   ├── 00_Project_Brain.md
│   ├── 01_Product_Strategy.md
│   ├── 02_User_Research.md
│   ├── 03_Problem_Definition.md
│   ├── 04_UX_Flows.md
│   ├── 05_UI_System.md
│   ├── 06_Technical_Architecture.md
│   ├── 07_Data_Model.md
│   ├── 08_Development_Notes.md
│   ├── 09_Portfolio_Content.md
│   ├── 10_LinkedIn_Substack_Content.md
│   ├── 11_QA_Audit.md
│   ├── 12_Decision_Log.md
│   ├── 13_Changelog.md
│   └── 14_Final_Compiler.md
│
├── .claude-plugin/
│   └── plugin.json
│
└── .github/
    └── workflows/
        └── zeref-sync-skills.yml     ← CI validation on push to main
```

---

## Skill Fleet Overview

| Skill ID | Layer | Role | Purpose |
|---|---|---|---|
| zeref-system-caveman-compressor | 5 — System | support | Compresses long or messy context into portable handoff briefs |
| zeref-ux-design-qa-auditor | 1 — UX | qa-gate | Audits UI/UX designs for visual and interaction issues before dev handoff |
| zeref-ux-accessibility-specialist | 1 — UX | support | WCAG audits, contrast, tap targets, screen reader, inclusive design |
| zeref-ux-interaction-designer | 1 — UX | lead | Designs interaction patterns, gestures, states, and micro-interactions |
| zeref-ux-product-designer | 1 — UX | lead | End-to-end UX/product design — brief, flows, wireframe specs, rationale |
| zeref-cnt-copywriter | 3 — Content | lead | Persuasive, on-brand copy for landing pages, products, campaigns |
| zeref-cnt-linkedin-ghostwriter | 3 — Content | support | Ghostwrites LinkedIn posts in Yash's professional voice |
| zeref-dev-code-quality-reviewer | 2 — Development | qa-gate | Code review — quality, maintainability, performance, security hygiene |
| zeref-hq-chief-product-officer | 7 — HQ | executive | Product vision, roadmap, prioritization, and strategic direction |
| zeref-biz-kpi-analyst | 4 — Business | support | KPI frameworks, metric hierarchies, north star, success criteria |
| zeref-final-executive-reviewer | 6 — QA / Final | qa-gate | Terminal QA gate — Go/No-Go on all major outputs |
| zeref-ux-design-systems-architect | 1 — UX | lead | Design systems, component libraries, tokens, Figma library architecture |
| zeref-ux-motion-designer | 1 — UX | support | **NEW** Motion systems, animation specs, easing curves, Lottie/Framer |
| zeref-ux-register-classifier | 1 — UX | support | **NEW** Classifies UX tasks and routes to the correct UX skill stack |
| zeref-system-memory-ingest | 8 — Memory | support | **NEW** Ingests decisions and outputs into the memory file system |
| zeref-system-memory-lint | 8 — Memory | qa-gate | **NEW** Validates memory files for staleness and inconsistency |
| zeref-biz-opportunity-solution-analyst | 4 — Business | support | **NEW** Opportunity-Solution Trees and JTBD problem framing |
| zeref-dev-ui-quality-enforcer | 2 — Development | qa-gate | **NEW** Design-to-code gap analysis and UI implementation QA |

---

## Commands Overview

| Command | What It Does |
|---|---|
| `/zeref-activate` | Activates the correct skill stack for the current task. ZEREFOS classifies the task type, selects lead + support + QA skills, and begins execution. |
| `/zeref-release` | Packages the fleet for marketplace or GitHub release. Runs validation, checks README file tree, confirms plugin.json is current, and produces a release checklist. |

---

## Memory Layer

Zeref uses a 15-file structured memory system stored in `memory/`:

| File | Purpose |
|---|---|
| `hot.md` | Current session context — read this first at every session start |
| `00_Project_Brain.md` | Master project overview |
| `01_Product_Strategy.md` | Strategy decisions and direction |
| `02_User_Research.md` | Research insights, personas, findings |
| `03_Problem_Definition.md` | Problem statements and framing |
| `04_UX_Flows.md` | User flows and navigation architecture |
| `05_UI_System.md` | UI design system and component decisions |
| `06_Technical_Architecture.md` | Technical decisions and system architecture |
| `07_Data_Model.md` | Data structures, schemas, entity relationships |
| `08_Development_Notes.md` | Dev decisions, environment config, notes |
| `09_Portfolio_Content.md` | Case study drafts and portfolio material |
| `10_LinkedIn_Substack_Content.md` | Content calendar, drafts, published posts |
| `11_QA_Audit.md` | QA reports, accessibility audits, issue logs |
| `12_Decision_Log.md` | All major decisions with rationale |
| `13_Changelog.md` | Version history and updates |
| `14_Final_Compiler.md` | Final deliverable assembly |

**Context loading order:** `hot.md` → skill file(s) → `references/` → registry (if routing needed).

Memory is managed by `zeref-system-memory-ingest` and validated by `zeref-system-memory-lint`.

---

## Validation

Run the skill validator from the repo root:

```bash
# Validate all skills in skills/ directory
python3 zeref-validate.py

# Verbose output — shows all PASS messages
python3 zeref-validate.py --verbose

# Validate a single skill file
python3 zeref-validate.py --file skills/zeref-ux-product-designer.md

# Custom skills directory
python3 zeref-validate.py --skills-dir path/to/skills
```

The validator checks:
- Required frontmatter fields: `id`, `name`, `version`, `layer`, `role`, `routes_to`, `receives_from`
- Valid layer values: 1–8
- Valid role values: `lead`, `support`, `qa-gate`, `executive`
- Required sections present: Mission, When To Use, When NOT To Use, Required Inputs, Deliverables, Workflow, Output Format, Token Discipline, Handoff Protocol
- `routes_to` references point to existing skill files
- No empty required sections

**Exit codes:** `0` = all pass, `1` = any fail

**CI:** Validation runs automatically on push to `main` when files in `skills/` or `commands/` change. See `.github/workflows/zeref-sync-skills.yml`.

---

## Contributing

This is personal infrastructure for Yash Kanadhia. It is not an open-source project accepting public contributions.

- No public pull requests
- No external contributors
- No issue tracker for feature requests
- This repo exists as proof of work, portfolio signal, and personal execution tooling

If you want to build your own version of this architecture, fork the repo and adapt it to your own operating system. Attribution is appreciated but not required.

---

## License

MIT License

Copyright (c) 2026 Yash Kanadhia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

*Zeref Skills Fleet V2 — Built by Yash Kanadhia | Toronto | 2026*
