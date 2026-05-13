# Zeref OS — Notion Dashboard

**Version:** 2.0.0 | **Updated:** May 2026

---

## Overview

The Notion dashboard is Zeref's command center — a visual layer on top of the wiki system that surfaces active work, decisions, and project health in one place.

This guide covers building the dashboard from scratch and connecting it to Zeref workflows via MCP.

---

## Workspace Structure

Create a top-level page called **Zeref OS** with this structure:

```
📋 Zeref OS/
  🏠 Command Center          ← Primary dashboard (this page)
  🎯 Active Projects         ← Project tracker database
  🧠 Decision Log            ← All major decisions
  📚 Resources               ← Research, references, links
  ⚡ Skills Fleet            ← Skill documentation (optional mirror)
  🔌 MCP Tracker             ← Connector status
  📁 Templates               ← Reusable page templates
```

---

## Page 1: Command Center

The Command Center is your daily entry point. Single page with linked database views.

### Layout

```
# Zeref OS — Command Center
[Last updated: auto-timestamp]

---

## 🔴 Active Right Now
[Linked view: Active Projects — filter: status = In Progress]

## ⚡ Decision Needed
[Linked view: Decision Log — filter: status = Needs Decision]

## 📅 This Week
[Linked view: Active Projects — filter: updated this week]

## 🎯 Portfolio Pipeline
[Linked view: Active Projects — filter: type = Portfolio]

---

## Quick Links
- [hot.md](obsidian://open?vault=ZerefOS-Wiki&file=hot) — Current session context
- [GitHub](https://github.com/kanadhiayash/zeref-agent-os) — Repo
- [Figma](https://figma.com) — Design files
```

---

## Page 2: Active Projects Database

### Database setup

Create a full-page database called **Active Projects**.

**Properties:**

| Property | Type | Options |
|----------|------|---------|
| Name | Title | — |
| Status | Select | Discovery, Design, Build, Launch, Complete, Paused |
| Type | Multi-select | Portfolio, Client, Learning, System |
| Priority | Select | P0, P1, P2 |
| Phase | Select | Research, UX, Dev, Content, Launch |
| Next Move | Text | One-line next action |
| Due Date | Date | — |
| Last Updated | Last edited time | Auto |
| GitHub | URL | Repo link |
| Figma | URL | Design file link |

**Views to create:**

1. **Board view** — grouped by Status
2. **Table view** — sorted by Priority then Last Updated
3. **Gallery view** — for portfolio projects (cover image)
4. **Filtered: Active** — Status ≠ Complete, ≠ Paused

### Project page template

Each project row opens to a full page. Use this template:

```markdown
# [Project Name]

## Overview
Type: [portfolio | client | learning | system]
Status: [current status]
Phase: [current phase]

---

## Objective
[What this project is trying to achieve]

## Key Insight
[The most important thing learned so far]

---

## Current Phase Notes
[What's happening in this phase]

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

---

## Outputs
| File | Type | Status |
|------|------|--------|
| [file name] | [doc/design/code] | [done/in-progress] |

---

## Decision Log
| Date | Decision | Reason |
|------|----------|--------|
| [date] | [what was decided] | [why] |

---

## Next Move
> [Single most important next action]
```

---

## Page 3: Decision Log Database

All major decisions across every project in one place. Searchable, filterable, permanent.

### Database setup

**Properties:**

| Property | Type | Options |
|----------|------|---------|
| Decision | Title | — |
| Project | Relation | → Active Projects |
| Status | Select | Made, Revisiting, Reversed |
| Impact | Select | High, Medium, Low |
| Date | Date | — |
| Made By | Text | — |
| Context | Text | Brief reason |

**Views:**

1. **Timeline** — sorted by Date, most recent first
2. **By Project** — grouped by Project relation
3. **High Impact** — filter: Impact = High

### Adding a decision via Zeref

```
"Add this decision to my Notion Decision Log:
Decision: Use Firebase Auth over custom JWT
Project: journaling-app
Impact: High
Reason: Faster to build, Google-managed security, fits 12-week timeline"
```

With Notion MCP active, Zeref creates the entry directly.

---

## Page 4: Resources Database

Research, articles, design inspiration, competitive analysis — all in one place.

### Database setup

**Properties:**

| Property | Type | Options |
|----------|------|---------|
| Title | Title | — |
| Type | Select | Article, Research, Competitive, Tool, Template, Reference |
| Project | Relation | → Active Projects |
| Tags | Multi-select | UX, Dev, Business, Marketing, AI |
| URL | URL | Source link |
| Notes | Text | Key takeaway |
| Date Saved | Created time | Auto |

**Views:**

1. **By Type** — grouped by Type
2. **By Project** — grouped by Project
3. **Recent** — sorted by Date Saved, last 30 days

---

## Page 5: MCP Tracker

Track connector status and what each connector enables.

### Structure

```markdown
# MCP Connector Tracker

| Connector | Status | What it enables | Last verified |
|-----------|--------|-----------------|---------------|
| Notion | ✅ Connected | Read/write pages and databases | [date] |
| Google Drive | ✅ Connected | Read documents | [date] |
| Linear | ❌ Not connected | Issue tracking | — |
| Gmail | ✅ Connected | Search email | [date] |
| Google Calendar | ✅ Connected | Events and scheduling | [date] |
| Figma | ⚠️ Token expired | Design file access | [date] |
| GitHub | ✅ Connected | Repo context and PRs | [date] |
| Canva | ❌ Not connected | Brand asset creation | — |

---

## Setup Priority
1. Linear — needed for task tracking integration
2. Figma — token needs renewal
3. Canva — nice-to-have for brand assets

---

## Quick verify commands
```
Test Notion: "List my Notion pages"
Test Drive: "List recent Google Drive files"
Test Linear: "What issues are assigned to me?"
Test GitHub: "What's in the root of my zeref-agent-os repo?"
```
```

---

## Zeref + Notion: Active Workflows

### Daily workflow
```
Morning: Open Command Center → review Active Right Now → check Decision Needed
```

### Adding project via Zeref
```
"Create a new project in my Notion Active Projects database:
Name: AI Portfolio Website
Status: Discovery
Type: Portfolio
Priority: P1
Next Move: Define IA and key pages"
```

### Pulling context for a task
```
"Pull the project page for 'journaling-app' from Notion and give me a status summary"
```

### Updating after a work session
```
"Update the journaling-app Notion project page:
- Status → Build
- Phase → Dev
- Next Move → Complete Firebase auth integration
- Add decision: Chose Expo over bare RN for faster iteration"
```

---

## Zeref OS Memory ↔ Notion Sync

The wiki (Obsidian) and Notion serve different purposes — don't try to keep them perfectly in sync.

| Use Obsidian wiki for | Use Notion for |
|----------------------|----------------|
| hot.md (session context) | Command Center (daily dashboard) |
| log.md (session history) | Active Projects (status tracking) |
| brain/ (deep strategy) | Decision Log (searchable decisions) |
| Raw project notes | Shareable project pages |
| Caveman handoffs | Portfolio-ready project summaries |

**Rule:** When something needs to be shared, presented, or searched across projects → Notion. When it's raw working memory → wiki.

---

## Templates Page

Store reusable page templates in Notion for:

- New project kickoff
- Research synthesis
- Case study draft
- Post-mortem
- Sprint plan

Each template should match the wiki structure from [05_Memory_System.md](05_Memory_System.md) so content can be mirrored between systems.

---

## Next Steps

- Connect Notion MCP: [04_MCP_Integration.md](04_MCP_Integration.md)
- Mirror wiki to Notion: [05_Memory_System.md](05_Memory_System.md)
- See Notion in real workflows: [06_Workflow_Examples.md](06_Workflow_Examples.md)
