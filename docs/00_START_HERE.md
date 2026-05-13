# Zeref Agent OS — Complete Installation & Setup Guidebook

**Version:** 2.0.0  
**Author:** Yash Kanadhia  
**Last Updated:** May 13, 2026  
**License:** MIT  

---

## What You're About To Install

**Zeref OS is not a chatbot configuration.**  
**It is not a prompt template.**  
**It is a 112-skill AI execution operating system built on top of Claude.**

Zeref transforms Claude from a generic assistant into a coordinated fleet of specialists:
- **UX Product Designer** who prototypes flows and design systems
- **Fullstack Engineer** who writes production code
- **Business Strategist** who validates market opportunities
- **Content Ghostwriter** who writes in your voice
- **QA Gatekeeper** who blocks bad work from shipping
- **107 more specialist skills** across 9 domains

Every task is routed to the **minimum useful skill stack**:
- **1 lead skill** (primary executor)
- **0–3 support skills** (only if they meaningfully improve output)
- **0–1 QA gate** (only when quality risk is high)

No over-loading. No hallucinated expertise. No generic outputs.

---

## Who This Is For

Zeref OS was built for **Yash Kanadhia** — a Toronto-based UX/Product Designer, Mobile Product Builder, and AI workflow operator.

But the system is designed to be **replicable and adaptable** for:

✅ **Product Designers** who want AI to think like a design team  
✅ **Developers** who want structured code reviews and architecture support  
✅ **Product Managers** who want strategic planning assistance  
✅ **Content Creators** who want brand-consistent ghostwriting  
✅ **Founders** who want business validation and GTM strategy  
✅ **Knowledge Workers** who want to build systems, not just complete tasks  

---

## What You'll Be Able To Do

After installation, you'll have:

### ✅ Structured Execution System
- Task classification (UX, Dev, PM, Content, Business, QA)
- Automatic routing to the right specialist skills
- Built-in quality gates before delivery
- Session memory that survives across conversations

### ✅ 112 Specialist Skills
- **Executive Leadership** (8 skills) — Strategy, operations, cross-functional coordination
- **UX/Design** (16 skills) — Product design, design systems, research, prototyping
- **Development** (17 skills) — Fullstack, mobile, AI systems, DevOps, security
- **Business** (14 skills) — Strategy, competitive intel, financial modeling, PMF
- **Marketing** (16 skills) — GTM, growth, SEO, branding, community
- **Content** (16 skills) — Writing, case studies, ghostwriting, scripts
- **QA** (15 skills) — Functional testing, accessibility, security, usability
- **Final Delivery** (4 skills) — Compilation, packaging, executive review
- **System Infrastructure** (6 skills) — Memory, routing, validation, compression

### ✅ Memory & Knowledge Management
- Obsidian vault with pre-configured structure
- Session handoffs with Caveman compression
- `hot.md` for current context (read-first protocol)
- Domain pages for long-term memory across sessions

### ✅ Quality & Discipline
- Anti-hallucination framework (never invent file contents, API responses, repo state)
- Token budget enforcement (smallest context that produces correct results)
- Karpathy principles (think before coding, simplicity first, surgical changes only)
- Validation system (`zeref-validate.py` + CI/CD)

### ✅ MCP Integration Ready
- Pre-configured for Notion, Linear, Google Drive, Figma, Canva
- Workflow automation with calendar, email, project management
- Multi-tool orchestration for complex tasks

---

## Installation Paths

### Tier 1: Full Zeref OS (Recommended)
**Time:** 30–45 minutes | **Complexity:** Medium

Everything — 112 skills, memory system, MCP connectors, Obsidian vault.

👉 **[01_Installation_Guide.md](01_Installation_Guide.md)**

---

### Tier 2: Core Skills Only
**Time:** 10–15 minutes | **Complexity:** Low

Claude Code plugin + ZEREFOS kernel. Skills work, no memory/MCP.

👉 **[01_Installation_Guide.md#tier-2-minimal-setup](01_Installation_Guide.md#tier-2-minimal-setup)**

---

### Tier 3: Custom Build
**Time:** 1–2 hours | **Complexity:** High

Fork, adapt, build your own skill fleet.

👉 **[03_Skills_Fleet_Guide.md#custom-skills](03_Skills_Fleet_Guide.md#custom-skills)**

---

## What Makes Zeref Different

### vs. Regular Claude
| Regular Claude | Zeref OS |
|----------------|----------|
| Generic responses | Specialist execution |
| No memory between sessions | Persistent memory via `hot.md` + wiki |
| All tasks handled the same | Auto-classified and routed |
| No quality gates | Multi-layer QA before delivery |
| Manual prompt engineering every time | Pre-configured specialists |

### vs. Custom GPT / Claude Project
| Custom GPT | Zeref OS |
|-----------|----------|
| Single monolithic prompt | 112 modular specialists |
| Static behavior | Adaptive routing |
| No validation | CI/CD validation |
| No memory protocol | Obsidian vault + handoff system |

---

## Core Philosophy

### 1. Systems Over Tasks
Every output should ship something, improve a system, create reusable documentation, or move you closer to becoming a systems scaler.

### 2. Minimum Useful Stack
1 lead + 0–3 support + 0–1 QA gate. Never more.

### 3. Evidence Over Invention
Never invent file contents, API responses, or repo state. State unknowns explicitly.

### 4. Proof of Work First
Functional deliverables + portfolio artifacts + career positioning + reusable systems.

---

## Prerequisites

### Required
- ✅ Claude Pro or Team account
- ✅ Claude Code CLI or Claude Desktop App
- ✅ Git

### Recommended
- ✅ Obsidian (free)
- ✅ Python 3.8+
- ✅ GitHub account
- ✅ Notion account (free)

### Optional (full MCP)
- Google Workspace, Linear, Figma, Canva, Wix

---

## Quick Start (3 Steps)

```bash
# 1. Clone
git clone https://github.com/kanadhiayash/zeref-agent-os.git
cd zeref-agent-os
claude plugin install .
```

```
# 2. Load kernel
Claude → Project Instructions → Paste ZEREFOS.md contents
```

```
# 3. Activate
/zeref-activate
```

---

## Document Navigation

| # | Document | Purpose |
|---|----------|---------|
| 01 | [Installation Guide](01_Installation_Guide.md) | Step-by-step setup |
| 02 | [Prompt Architecture](02_Prompt_Architecture.md) | Instruction hierarchy |
| 03 | [Skills Fleet Guide](03_Skills_Fleet_Guide.md) | All 112 skills |
| 04 | [MCP Integration](04_MCP_Integration.md) | Connector setup |
| 05 | [Memory System](05_Memory_System.md) | Wiki + Obsidian workflow |
| 06 | [Workflow Examples](06_Workflow_Examples.md) | Real use cases |
| 07 | [Troubleshooting](07_Troubleshooting.md) | Common issues |
| 08 | [Inspiration Deep Dive](08_Inspiration_Deep_Dive.md) | Karpathy, Agrici, Graphify |
| 09 | [Notion Dashboard](09_Notion_Dashboard.md) | Command center setup |

---

## License

MIT License — Copyright (c) 2026 Yash Kanadhia

See [LICENSE](../LICENSE) for full terms.

---

**Zeref OS v2.0.0** | *112 skills. 9 commands. 2 agents. One operating system.*
