# zeref-routing-model.md — Canonical Routing Model

> **Concept page.** Stable. Update rarely. Log decisions in `wiki/log.md` when this changes.
> **Last updated:** 2026-05-12
> **Status:** Stable

---

## Purpose

This page documents Zeref's complete routing model — how tasks are classified, how skills are selected, what register applies, when Caveman activates, and how skill-to-skill handoffs work. This is the canonical reference for routing decisions.

**Read this page before:** designing a new skill, updating the router, writing registry entries, or debugging wrong-skill activations.

---

## 1. Smallest-Stack Principle

The core routing law for Zeref is **smallest useful stack**.

```
Rule: Use the minimum number of skills that can execute the task correctly.

Stack structure:
  1 lead skill          — owns the task and drives the output
  1–3 support skills    — provide specialized context or sub-outputs
  1 QA/final gate       — runs only when major, irreversible, or public-facing output is involved
  Caveman               — conditional, not default (see Section 5)

Never:
  - Activate all skills at once
  - Use Zeref ceremony for trivial tasks
  - Add a QA gate to a simple rewrite or lookup
  - Use Caveman for short, single-environment sessions
```

**Why it matters:** Large-skill activation is theatrical, not operational. It increases latency, token cost, and output noise without improving quality. The smallest-stack principle keeps Zeref fast, precise, and defensible.

---

## 2. Task Type Classification Codes

Before routing, classify the task. Use exactly one primary type. Add a secondary type only when the task genuinely spans two domains.

| Code | Name | Trigger |
|------|------|---------|
| `SYS` | System / Architecture / OS | Building or changing Zeref itself, OS rules, layers, routing |
| `DEV` | Development / Coding / GitHub | Writing code, debugging, repo management, CI/CD |
| `UX` | UX Research / Design / Flows | User journeys, wireframes, usability audits, accessibility |
| `UI` | UI Design / Design System | Visual components, typography, motion, tokens, Figma |
| `MKT` | Marketing / Growth / Content | Campaigns, SEO, social, brand voice, content strategy |
| `DOC` | Documentation / Wiki / Memory | Markdown files, wikis, READMEs, knowledge management |
| `QA` | Quality Assurance / Audit / Testing | QA audits, accessibility checks, code reviews, test plans |
| `PM` | Product Management / Roadmap / Specs | Feature specs, PRDs, roadmaps, metrics tracking |
| `CAR` | Career / Portfolio / LinkedIn / Resume | Portfolio case studies, job applications, LinkedIn, resume |
| `AUT` | Automation / Workflow / Toolchain | Scripts, automations, Zapier, n8n, tool integrations |
| `RES` | Research / Analysis / Competitive Intel | Market research, competitive analysis, deep dives |
| `BIZ` | Business / Scaling / Strategy | Business strategy, revenue models, system scaling |

**Log the task type** in `wiki/log.md` for every session that produces a meaningful output.

---

## 3. Register Classification

Zeref adopts the register model from the **impeccable** repo (brand vs. product register). Apply register as a second-level classifier after task type.

| Register | Definition | Signals | Applies To |
|----------|-----------|---------|------------|
| `BRAND` | Work that shapes perception, identity, trust, emotion | Tone, color, typography, narrative, campaign voice | MKT, UI (brand), CAR, content |
| `PRODUCT` | Work that shapes behavior, utility, function, flow | Features, flows, data models, architecture, code | DEV, UX, UI (product), PM, AUT |
| `SYS` | Work that shapes the operating system itself | Routing rules, memory protocols, skill definitions | SYS, DOC |
| `HYB` | Hybrid — work that spans both brand and product | Launch campaigns, onboarding flows, portfolio | Spans MKT+PM, CAR+UX |

**Routing implication:** Brand-register tasks prioritize skills in MKT, content, and brand-voice categories. Product-register tasks prioritize UX, DEV, PM, and QA skills. SYS-register tasks use system and DOC skills. Hybrid tasks use both stacks but still follow smallest-stack — pick the dominant register first.

---

## 4. Routing Table Summary

| Task Type | Lead Skill Category | Common Support Skills | QA Gate? | Caveman? |
|-----------|--------------------|-----------------------|----------|----------|
| SYS | system/ or HQ/ | doc/, any relevant | On major arch changes | On long sessions |
| DEV | development/ | QA/, UX/ if user-facing | Yes for ship-ready code | On cross-env handoffs |
| UX | UX/ | product-design/, QA/ | Yes for public-facing | On long research sessions |
| UI | UI/ or design/ | UX/, QA/ | Yes for design system changes | Rarely |
| MKT | marketing/ | content/, QA/ | On major campaigns | Rarely |
| DOC | doc/ or HQ/ | any relevant | On canonical/public docs | On long sessions |
| QA | QA/ | any relevant to audit | N/A (QA is the gate) | Rarely |
| PM | PM/ | product-design/, UX/ | On PRDs/roadmaps | On long sessions |
| CAR | career/ or portfolio/ | content/, QA/ | Yes for public-facing | On session transfers |
| AUT | system/ or dev/ | any relevant | On production automations | On cross-env handoffs |
| RES | research/ or HQ/ | any relevant | On major reports | On long sessions |
| BIZ | business/ | HQ/, PM/ | On major strategy docs | Rarely |

**Routing anti-pattern:** If you cannot name the lead skill within 5 seconds of reading the task, re-read the task objective. If still unclear, classify as the task type closest to the user's stated goal and proceed with a labeled assumption.

---

## 5. Caveman Trigger Rules

Caveman is a **conditional compression layer** for context preservation. It is not default behavior.

**Activate Caveman when:**
- Context is long (>50 messages or multi-session work)
- Work is moving between Claude Chat, Claude Code, Claude Cowork, ChatGPT, Notion, GitHub, Figma, Stitch, Wix, or local folders
- The session produced decisions, file paths, commands, risks, or next steps worth preserving across environments
- Yash explicitly asks for a compressed handoff
- A project is ending a long session and needs continuity into the next

**Do not activate Caveman when:**
- The session is short and self-contained
- The next session will be in the same environment with the same context
- The task is trivial (quick fix, short answer, single lookup)
- Activating Caveman would create ceremony instead of value

**Caveman must always preserve (never compress or paraphrase):**
```
- Code
- Commands
- File paths
- URLs
- Exact error messages
- Configuration values
- API key placeholders
- Security-sensitive instructions
- User-provided constraints
- Tool outputs that must remain exact
```

**Caveman handoff format:**
```
Objective:         [What was being achieved]
Current state:     [Where things stand right now]
Files inspected:   [List with paths]
Files changed:     [List with paths and what changed]
Decisions made:    [Architecture choices, confirmed rules]
Open risks:        [Unresolved issues, blockers]
Exact artifacts:   [Paths, commands, URLs, errors]
Next action:       [Single most logical next step]
```

---

## 6. Skill-to-Skill Handoff Protocol

When a task moves from one skill to another within a session:

1. **The outgoing skill** must produce a clear output before handing off — not a half-finished artifact.
2. **State the handoff explicitly:** `[Lead skill: UX/user-research] → handing off to [DEV/frontend] with the following context: ...`
3. **Pass exactly:** decisions made, files changed, constraints active, open risks.
4. **The incoming skill** reads the handoff before acting. It does not re-derive context from scratch.
5. **Log handoffs** in `wiki/hot.md` Last Handoff section if they are meaningful.

---

## 7. Anti-Hallucination Routing Rules

These rules are non-negotiable and override routing convenience.

| Rule | Detail |
|------|--------|
| **Never invent connector access** | Do not claim a tool, MCP, or API was used unless it was actually called and returned a real output. |
| **Never invent file contents** | Do not describe what a Figma, GitHub, Notion, Google Drive, or Wix file contains unless the file was actually read in the current session. |
| **Never invent tool outputs** | Do not summarize or paraphrase a tool output that was not actually returned. |
| **Never invent research findings** | Do not produce metrics, user data, competitive data, or market numbers that were not retrieved from a verified source. |
| **State what was not verified** | Every major output should label unverified claims. `[ASSUMPTION: ...]` or `[NOT VERIFIED: ...]` are required when proceeding without confirmed data. |
| **Preserve exact technical artifacts** | Paths, commands, URLs, error messages, config values — never paraphrase. Copy exactly. |
| **If unknown, say unknown** | "Unknown" is always more correct than an invented answer. |

**Why this matters for routing:** Wrong routing + hallucinated output is worse than no output. These rules ensure that even if routing is imperfect, the output remains honest and correctable.
