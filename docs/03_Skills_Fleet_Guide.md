# Zeref OS — Skills Fleet Guide

**Version:** 2.0.0 | **Updated:** May 2026

---

## Overview

Zeref OS contains **112 specialist skills** organized across 9 layers. Each skill is a self-contained expert with defined responsibilities, output formats, and quality gates.

This guide covers:
- [How skills work](#how-skills-work)
- [All 9 layers and their skills](#skill-layers)
- [Routing examples](#routing-examples)
- [Building custom skills](#custom-skills)

---

## How Skills Work

Each skill file (`skills/zeref-[layer]-[role]/`) contains:

```
1. Identity — Who this specialist is
2. Core Responsibilities — What they own
3. Output Format — How they structure deliverables
4. Quality Gates — What they verify before handing off
5. Triggers — Phrases that activate this skill
6. Anti-patterns — What they explicitly don't do
```

Skills activate when:
- Task classification matches the skill's layer
- User request contains trigger phrases
- Lead skill delegates to support skill

Skills do NOT activate when:
- Task is simpler than the skill's scope (avoid over-engineering)
- Another skill in the same layer already covers it
- User explicitly requests a different approach

---

## Skill Layers

### Layer: HQ — Executive Leadership (8 skills)

The HQ layer handles cross-functional strategy, system orchestration, and high-level decision making.

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-hq-fleet-activator` | Fleet Activator | Session start, system orientation |
| `zeref-hq-chief-strategy-officer` | Chief Strategy Officer | Long-term positioning, strategic pivots |
| `zeref-hq-chief-product-officer` | Chief Product Officer | Product vision, roadmap decisions |
| `zeref-hq-chief-operating-officer` | Chief Operating Officer | Workflow systems, operational efficiency |
| `zeref-hq-chief-research-officer` | Chief Research Officer | Research synthesis, knowledge management |
| `zeref-hq-chief-of-staff` | Chief of Staff | Task coordination, session management |
| `zeref-hq-quality-gatekeeper` | HQ Quality Gatekeeper | Pre-delivery review for major outputs |
| `zeref-hq-documentation-architect` | Documentation Architect | System documentation, knowledge architecture |

---

### Layer: UX — Design & Product (16 skills)

The UX layer covers the full design process from research through developer handoff.

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-ux-product-designer` | Product Designer | End-to-end product design decisions |
| `zeref-ux-research-lead` | UX Research Lead | Research planning, methodology, synthesis |
| `zeref-ux-synthetic-research-analyst` | Synthetic Research Analyst | AI-simulated user research when real data unavailable |
| `zeref-ux-persona-strategist` | User Persona Strategist | Persona creation, user segmentation |
| `zeref-ux-problem-definition-specialist` | Problem Definition Specialist | Problem framing, HMW statements |
| `zeref-ux-information-architect` | Information Architect | IA, navigation, content structure |
| `zeref-ux-user-flow-designer` | User Flow Designer | Task flows, journey maps |
| `zeref-ux-interaction-designer` | Interaction Designer | Micro-interactions, state transitions |
| `zeref-ux-visual-designer` | Visual Designer | Visual hierarchy, layout, aesthetics |
| `zeref-ux-design-systems-architect` | Design Systems Architect | Component libraries, tokens, consistency |
| `zeref-ux-prototype-specialist` | Prototype Specialist | Prototyping strategy, fidelity decisions |
| `zeref-ux-figma-architecture-specialist` | Figma Architecture Specialist | Figma file structure, component organization |
| `zeref-ux-accessibility-specialist` | Accessibility Specialist | WCAG compliance, inclusive design |
| `zeref-ux-writer` | UX Writer | Microcopy, error messages, empty states |
| `zeref-ux-developer-handoff-lead` | Developer Handoff Lead | Design specs, annotation, dev-ready files |
| `zeref-ux-design-qa-auditor` | Design QA Auditor | Pre-handoff design quality review |

---

### Layer: DEV — Development (17 skills)

The DEV layer covers the full engineering stack from architecture through deployment.

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-dev-solution-architect` | Solution Architect | System architecture, tech stack decisions |
| `zeref-dev-technical-architect` | Technical Architect | Deep architecture for complex systems |
| `zeref-dev-fullstack-engineer` | Full-Stack Engineer | Feature development, general coding |
| `zeref-dev-frontend-engineer` | Frontend Engineer | React, UI components, browser behavior |
| `zeref-dev-backend-engineer` | Backend Engineer | APIs, databases, server logic |
| `zeref-dev-ios-engineer` | Mobile iOS Engineer | Swift, SwiftUI, iOS-specific patterns |
| `zeref-dev-android-engineer` | Mobile Android Engineer | Kotlin, Jetpack Compose, Android patterns |
| `zeref-dev-ai-systems-engineer` | AI Systems Engineer | LLM integration, prompt engineering, agents |
| `zeref-dev-firebase-specialist` | Firebase Specialist | Firestore, Auth, Functions, Storage |
| `zeref-dev-mongodb-specialist` | MongoDB Specialist | Schema design, aggregations, indexing |
| `zeref-dev-database-architect` | Database Architect | Data modeling, migrations, performance |
| `zeref-dev-api-integration-engineer` | API Integration Engineer | Third-party APIs, webhooks, OAuth |
| `zeref-dev-devops-engineer` | DevOps Engineer | CI/CD, Docker, deployment pipelines |
| `zeref-dev-security-engineer` | Security Engineer | Auth flows, vulnerabilities, data protection |
| `zeref-dev-github-repository-manager` | GitHub Repository Manager | Repo structure, branching, releases |
| `zeref-dev-code-quality-reviewer` | Code Quality Reviewer | Code review, refactoring, tech debt |
| `zeref-dev-technical-documentation-writer` | Technical Documentation Writer | READMEs, API docs, runbooks |

---

### Layer: BIZ — Business (14 skills)

The BIZ layer handles business strategy, validation, and financial thinking.

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-biz-business-strategist` | Business Strategist | Business model, strategic direction |
| `zeref-biz-business-validator` | Business Validator | Assumption testing, validation frameworks |
| `zeref-biz-product-market-fit-analyst` | PMF Analyst | PMF signals, retention, engagement |
| `zeref-biz-market-research-analyst` | Market Research Analyst | Market sizing, competitive landscape |
| `zeref-biz-competitive-intelligence-analyst` | Competitive Intelligence Analyst | Competitor deep-dives, differentiation |
| `zeref-biz-financial-analyst` | Financial Analyst | Unit economics, P&L, projections |
| `zeref-biz-monetization-strategist` | Monetization Strategist | Pricing, revenue models, upsell paths |
| `zeref-biz-operations-strategist` | Operations Strategist | Process design, operational scaling |
| `zeref-biz-partnership-strategist` | Partnership Strategist | Partnership frameworks, BD strategy |
| `zeref-biz-kpi-analyst` | Business KPI Analyst | Metric selection, dashboard design |
| `zeref-biz-risk-analyst` | Risk Analyst | Risk identification, mitigation planning |
| `zeref-biz-investor-pitch-strategist` | Investor Pitch Strategist | Pitch decks, investor narratives |
| `zeref-biz-grant-funding-analyst` | Grant/Funding Analyst | Grant identification, application strategy |
| `zeref-biz-legal-advisor` | Legal Advisor | Contracts, IP, compliance (non-legal advice) |

---

### Layer: MKT — Marketing (16 skills)

The MKT layer covers go-to-market execution and growth.

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-mkt-chief-marketing-strategist` | Chief Marketing Strategist | Full marketing strategy |
| `zeref-mkt-brand-strategist` | Brand Strategist | Brand positioning, identity, voice |
| `zeref-mkt-positioning-strategist` | Positioning Strategist | Market positioning, messaging hierarchy |
| `zeref-mkt-gtm-strategist` | GTM Strategist | Launch strategy, channel selection |
| `zeref-mkt-growth-marketer` | Growth Marketer | Acquisition loops, retention tactics |
| `zeref-mkt-seo-strategist` | SEO Strategist | Keyword strategy, content SEO |
| `zeref-mkt-content-marketing-strategist` | Content Marketing Strategist | Content calendar, topic clusters |
| `zeref-mkt-social-media-strategist` | Social Media Strategist | Platform strategy, posting cadence |
| `zeref-mkt-personal-branding-strategist` | Personal Branding Strategist | LinkedIn, Substack, public positioning |
| `zeref-mkt-email-marketing-specialist` | Email Marketing Specialist | Sequences, newsletters, automation |
| `zeref-mkt-performance-marketing-specialist` | Performance Marketing Specialist | Paid ads, conversion optimization |
| `zeref-mkt-pr-communications-specialist` | PR & Communications Specialist | Press releases, media outreach |
| `zeref-mkt-analytics-specialist` | Marketing Analytics Specialist | Attribution, funnel analysis |
| `zeref-mkt-community-strategist` | Community Strategist | Community building, engagement |
| `zeref-mkt-conversion-rate-optimizer` | Conversion Rate Optimizer | Landing pages, A/B testing, UX |
| `zeref-mkt-affiliate-marketing-strategist` | Affiliate Marketing Strategist | Partner programs, referral systems |

---

### Layer: CNT — Content (16 skills)

The CNT layer handles all written and multimedia content creation.

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-cnt-editorial-director` | Editorial Director | Content strategy, editorial calendar |
| `zeref-cnt-long-form-writer` | Long-Form Writer | Articles, essays, reports |
| `zeref-cnt-copywriter` | Copywriter | Headlines, CTAs, persuasive copy |
| `zeref-cnt-seo-content-writer` | SEO Content Writer | SEO-optimized articles |
| `zeref-cnt-ux-case-study-writer` | UX Case Study Writer | Portfolio case studies |
| `zeref-cnt-technical-case-study-writer` | Technical Case Study Writer | Engineering and systems case studies |
| `zeref-cnt-linkedin-ghostwriter` | LinkedIn Ghostwriter | LinkedIn posts, engagement copy |
| `zeref-cnt-scriptwriter` | Scriptwriter | Video scripts, podcast scripts |
| `zeref-cnt-documentation-writer` | Documentation Writer | User docs, help articles |
| `zeref-cnt-resume-career-writer` | Resume & Career Writer | Resumes, cover letters, bios |
| `zeref-cnt-brand-voice-editor` | Brand Voice Editor | Tone consistency, voice editing |
| `zeref-cnt-content-qa-editor` | Content QA Editor | Proofreading, fact-checking |
| `zeref-cnt-repurposing-specialist` | Content Repurposing Specialist | Multi-format adaptation |
| `zeref-cnt-presentation-designer` | Presentation Designer | Deck structure, slide narratives |
| `zeref-cnt-visual-asset-prompt-engineer` | Visual Asset Prompt Engineer | AI image prompts, visual direction |
| `zeref-cnt-video-content-strategist` | Video Content Strategist | Video content planning, thumbnails |

---

### Layer: QA — Quality Assurance (15 skills)

The QA layer validates output quality before delivery.

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-qa-lead` | QA Lead | QA strategy, test planning |
| `zeref-qa-functional-tester` | Functional QA Tester | Feature testing, acceptance criteria |
| `zeref-qa-ux-usability-tester` | UX Usability Tester | Usability heuristics, flow testing |
| `zeref-qa-ui-consistency-auditor` | UI Consistency Auditor | Design system compliance |
| `zeref-qa-accessibility-tester` | Accessibility Tester | WCAG 2.1 AA compliance |
| `zeref-qa-performance-tester` | Performance Tester | Load time, Core Web Vitals |
| `zeref-qa-security-tester` | Security QA Tester | Auth flows, data exposure |
| `zeref-qa-regression-tester` | Regression Tester | Change impact analysis |
| `zeref-qa-edge-case-tester` | Edge Case Tester | Boundary conditions, failure states |
| `zeref-qa-analytics-specialist` | Analytics QA Specialist | Event tracking, data accuracy |
| `zeref-qa-marketing-auditor` | Marketing QA Auditor | Campaign and content accuracy |
| `zeref-qa-ab-testing-strategist` | A/B Testing Strategist | Test design, statistical validity |
| `zeref-qa-rubric-alignment-auditor` | Rubric Alignment Auditor | Output vs. brief alignment |
| `zeref-qa-launch-readiness-manager` | Launch Readiness Manager | Pre-launch checklist |
| `zeref-qa-final-quality-gatekeeper` | Final Quality Gatekeeper | Final delivery gate |

---

### Layer: FINAL — Final Delivery (4 skills)

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-final-project-compiler` | Project Compiler | Multi-artifact compilation |
| `zeref-final-executive-reviewer` | Executive Reviewer | Leadership-level review |
| `zeref-final-deliverable-packager` | Deliverable Packager | Portfolio/client packaging |
| `zeref-final-source-validator` | Source Validator | Fact-checking, citation verification |

---

### Layer: SYSTEM — Infrastructure (6 skills)

| Skill | Role | When to use |
|-------|------|-------------|
| `zeref-system-skill-router` | System Skill Router | Manual routing decisions |
| `zeref-system-caveman-compressor` | Caveman Compressor | Context compression |
| `zeref-system-evidence-memory-keeper` | Evidence Memory Keeper | Memory management |
| `zeref-system-token-budget-controller` | Token Budget Controller | Context efficiency |
| `zeref-system-marketplace-packager` | Marketplace Packager | Plugin packaging |
| `zeref-system-plugin-update-diagnostician` | Plugin Update Diagnostician | Plugin debugging |

---

## Routing Examples

### Example 1: UX Design Task
**Request:** "Design the onboarding flow for a mobile journaling app"

```
Task type: UX flow design
Lead: zeref-ux-user-flow-designer
Support: zeref-ux-product-designer, zeref-ux-interaction-designer
QA: zeref-qa-ux-usability-tester
```

### Example 2: Development Task
**Request:** "Build a Firebase auth system with email and Google OAuth"

```
Task type: Backend development
Lead: zeref-dev-backend-engineer
Support: zeref-dev-firebase-specialist, zeref-dev-security-engineer
QA: zeref-qa-security-tester
```

### Example 3: Content Task
**Request:** "Write a LinkedIn post about my UX case study"

```
Task type: Personal brand content
Lead: zeref-cnt-linkedin-ghostwriter
Support: zeref-mkt-personal-branding-strategist
QA: (skipped — low risk, quick iteration)
```

### Example 4: Business Strategy
**Request:** "Validate whether there's a market for a B2B AI workflow tool in Toronto"

```
Task type: Business validation
Lead: zeref-biz-business-validator
Support: zeref-biz-market-research-analyst, zeref-biz-product-market-fit-analyst
QA: zeref-qa-rubric-alignment-auditor
```

### Example 5: Portfolio Output
**Request:** "Package this project as a case study for my portfolio"

```
Task type: Final delivery
Lead: zeref-final-deliverable-packager
Support: zeref-cnt-ux-case-study-writer, zeref-mkt-personal-branding-strategist
QA: zeref-qa-final-quality-gatekeeper
```

---

## Custom Skills

### When to build a custom skill
- Existing skills don't cover your domain
- You have highly specific output format requirements
- You need specialized terminology or expertise

### Custom skill template

```markdown
---
name: zeref-[layer]-[role-name]
layer: [ux|dev|biz|mkt|cnt|qa|final|system|hq]
role: [Role Title]
description: [One-line description for routing decisions]
version: 1.0.0
triggers:
  - "[trigger phrase 1]"
  - "[trigger phrase 2]"
---

# [Role Title]

## Identity
You are the [Role Title] for Zeref Skills Fleet work.

## Core Responsibilities
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

## Output Format
[Describe exact output structure]

## Quality Gates
Before handing off, verify:
- [ ] [Gate 1]
- [ ] [Gate 2]

## Anti-patterns
Never:
- [Anti-pattern 1]
- [Anti-pattern 2]
```

### Validate after adding
```bash
python zeref-validate.py
```

All fields required. Validation fails if `name`, `layer`, `role`, `description`, or `triggers` are missing.

---

## Next Steps

- [04_MCP_Integration.md](04_MCP_Integration.md) — Connect external tools
- [06_Workflow_Examples.md](06_Workflow_Examples.md) — See skills in action
