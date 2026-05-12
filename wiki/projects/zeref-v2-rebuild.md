# Zeref V2 Rebuild — Project Memory Page

> **Last updated:** 2026-05-12
> **Status:** Active — Phase 4 complete, Phase 5 next
> **Owner:** Yash Kanadhia
> **System:** Zeref OS — Perplexity Computer

---

## Project Objective

Rebuild Zeref from a 112-skill flat prompt fleet (V1) into a layered, register-aware, command-chaining execution OS with:
- A durable wiki memory layer
- A motion/UI quality enforcement layer
- A PM workflow layer baked into routing logic
- A machine-readable skill registry
- Graph-first structural retrieval via Graphify

**Success definition:** Zeref V2 behaves consistently across Claude Chat, Claude Code, Claude Cowork, and Perplexity Computer. It routes deterministically, remembers across sessions, and produces portfolio-quality proof of work.

---

## Confirmed Architecture — 5 Layers

| Layer | Name | Core File(s) | Purpose |
|-------|------|-------------|---------|
| 1 | Identity Layer | `ZEREFOS.md` / `ZerefClaude.md` | Cross-environment behavioral constitution |
| 2 | Skill Layer | `zeref-skills-fleet/` (112 skills) | Modular execution — UX, DEV, PM, MKT, QA, BIZ |
| 3 | Memory Layer | `wiki/hot.md`, `wiki/index.md`, `wiki/log.md`, `wiki/projects/`, `wiki/concepts/`, `wiki/sources/` | Session continuity, compounding knowledge |
| 4 | Graph Layer | Graphify reports, `graph.json`, `GRAPHREPORT.md` | Structural retrieval, token-efficient reading |
| 5 | Command Layer | `commands/` (orient, save, capture, recall, trace, lint, package, caveman) | Thin reusable interfaces to skills and memory |

**Architecture principle:** Each layer has a different job — policy, execution, continuity, retrieval, interface. No layer substitutes for another.

---

## Confirmed File Manifest

### Identity Layer
```
ZEREFOS.md                          — Master OS kernel (refined from ZerefClaude.md)
ZerefClaude.md                      — Original global baseline (preserved as reference)
```

### Skill Layer
```
zeref-skills-fleet/
  .claude-plugin/
    plugin.json                     — Plugin manifest v1.1.2
  agents/
    zeref-fleet-router.md           — Fleet routing agent
    zeref-executive-qa-agent.md     — Executive QA agent
  commands/
    zeref-activate.md               — Activation command
    zeref-package-release.md        — Package/release command
  output-styles/
    zeref-executive.md              — Executive output style
  themes/
    zeref-dark.json                 — UI theme
  skills/[112 skill folders]        — DEV(17), UX(16), MKT(16), CON(16), QA(15), BIZ(14), HQ(8), SYS(6), FIN(4)
  README.md
  skills/registry.md                — [PLANNED — Phase 3] Machine-readable registry
```

### Memory Layer (this wiki)
```
wiki/
  hot.md                            — Active session state (read first)
  index.md                          — Master wiki index
  log.md                            — Append-only session log
  projects/
    zeref-v2-rebuild.md             — This file
    [project-slug].md               — Future project pages
  concepts/
    zeref-routing-model.md          — Canonical routing model
    zeref-memory-protocol.md        — Canonical memory protocol
    [concept-slug].md               — Future concept pages
  sources/
    zeref-reference-links.md        — Reference links and summaries
    [source-slug].md                — Future source pages
```

### Graph Layer
```
graphify/
  GRAPHREPORT.md                    — [PLANNED — Phase 5] Structural analysis report
  graph.json                        — [PLANNED — Phase 5] Knowledge graph
  graph.html                        — [PLANNED — Phase 5] Interactive visualization
```

### Command Layer
```
commands/
  orient.md                         — [PLANNED — Phase 5] Orient command
  save.md                           — [PLANNED — Phase 5] Save command
  capture.md                        — [PLANNED — Phase 5] Capture command
  recall.md                         — [PLANNED — Phase 5] Recall command
  trace.md                          — [PLANNED — Phase 5] Trace command
  lint.md                           — [PLANNED — Phase 5] Memory lint command
  package.md                        — [PLANNED — Phase 5] Package command
  caveman.md                        — [PLANNED — Phase 5] Caveman handoff command
```

---

## Confirmed Decisions

| # | Decision | Rationale | Date |
|---|----------|-----------|------|
| D1 | 5-layer architecture (Identity, Skill, Memory, Graph, Command) | Separation of concerns — each layer has a distinct job | 2026-05-11 |
| D2 | Memory layer based on Karpathy LLM Wiki pattern | Compounding memory, index-first navigation, wiki as source of truth | 2026-05-11 |
| D3 | hot.md is the first file read every session | Ensures session continuity without relying on chat history | 2026-05-12 |
| D4 | Free-first policy — no paid spend without explicit Yash approval | Cost discipline as architecture, not preference | 2026-05-11 |
| D5 | Smallest-stack routing principle (1 lead + 1–3 support + 1 QA gate) | Prevents theatrical over-activation, keeps execution focused | 2026-05-11 |
| D6 | Register model adopted from impeccable repo (brand vs. product) | Universal design classification for routing precision | 2026-05-11 |
| D7 | Machine-readable skill registry required before fleet expansion | Without registry, routing remains partly performative | 2026-05-11 |
| D8 | Graphify pilot scoped to contained folder before global hooks | Automation after manual validation, not before | 2026-05-11 |
| D9 | Commands stay thin — logic lives in skills and concept pages | Prevents command bloat, enforces single source of truth | 2026-05-12 |

---

## Current Status

**Active phase:** Phase 4 — Memory Layer ✅ COMPLETE
**Next phase:** Phase 1 — Integration Testing

### Phase Completion Status

| Phase | Name | Status | Notes |
|-------|------|--------|-------|
| Phase 0 | Analysis & Brain Reports | ✅ Complete | V1 + V2 brain reports generated |
| Phase 1 | Stabilize the platform (release governance) | 🔲 Pending | LICENSE, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md missing |
| Phase 2 | Improve routing quality (skill description rewrites) | 🔲 Pending | Priority: router, fleet activator, Caveman, product design, fullstack, QA gate |
| Phase 3 | Shared references + machine-readable skill registry | 🔲 Pending | Extract boilerplate, generate registry.md |
| Phase 4 | Memory layer (this wiki) | ✅ Complete | hot.md, index.md, log.md, projects/, concepts/, sources/ |
| Phase 5 | Graph-first retrieval (Graphify pilot) | 🔲 Planned | Run on zeref-skills-fleet/, validate report quality, then add hooks |

---

## Open Questions

| # | Question | Priority | Notes |
|---|----------|----------|-------|
| Q1 | Which folder should the Graphify pilot run on first — zeref-skills-fleet/ or full OS vault? | P2 | Recommendation: skills-fleet first, then expand |
| Q2 | Should registry.md be JSON, YAML, or Markdown table? | P1 | Markdown table is most portable and LLM-readable |
| Q3 | What is the Obsidian vault sync method — manual, iCloud, or GitHub? | P2 | Decide before Phase 5 |
| Q4 | Which skills need the highest-priority description rewrites? | P1 | Fleet router, activator, Caveman, product design, fullstack, QA gate |
| Q5 | What are the trigger phrases for each major skill? | P1 | Required for registry.md |

---

## Risks

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|-----------|------------|
| R1 | hot.md goes stale if not updated each session | Memory layer becomes unreliable | High | Enforce read-first/update-last discipline. Add memory lint trigger. |
| R2 | Skill routing remains ambiguous without registry | Wrong skill activations at scale | Medium | Phase 3 priority: build registry before expanding fleet |
| R3 | Maintenance debt from 112-skill boilerplate duplication | Global edits become error-prone | Medium | Phase 3: extract shared references |
| R4 | Release governance gap (missing LICENSE, SECURITY.md etc.) | Weak GitHub/marketplace credibility | Medium | Phase 1 priority: close governance files |
| R5 | Graphify hook automation before manual validation | Automation on a broken baseline | Low | Phase 5 rule: manual first, then hooks |
| R6 | ZerefOS used across environments without consistent ZEREFOS.md | Identity layer drift | Low | Sync ZEREFOS.md to GitHub and use as canonical source |

---

## Workspace Locations

| Resource | Location | Notes |
|----------|----------|-------|
| Mac skill fleet source | `/Users/yashkanadhia/Documents/Claude/00SKILLS/zeref-skills-fleet` | Original — do not edit sandbox without explicit approval |
| Mac repos folder | `/Users/yashkanadhia/Documents/Claude/01REPOS` | Impeccable, pm-skills, graphify, claude-obsidian etc. |
| Sandbox copy | `/home/user/workspace/zerefanalysis/zeref-skills-fleet` | Analysis copy — not live |
| Wiki (this layer) | `/home/user/workspace/wiki/` | Memory layer files |
| GitHub repo | `github.com/kanadhiayash/zeref-skills-fleet` | Public repo — current state unknown |
| Notion Command Center | `copper-tv-288.notion.site/Zeref-Skills-Fleet-Command-Center-...` | Dashboard — not confirmed live |
| ZerefClaude.md | `/Users/yashkanadhia/Documents/Claude/ZerefClaude.md` | Global baseline — in use |
