# Zeref OS — Memory System

**Version:** 2.0.0 | **Updated:** May 2026

---

## Overview

Zeref memory works in two tiers:

| Tier | Location | Purpose | Persistence |
|------|----------|---------|-------------|
| **Hot** | `wiki/hot.md` | Current session state | Read every session start |
| **Cold** | `wiki/` subdirectories | Long-term knowledge | Retrieved on demand |

**Rule:** Read `hot.md` before every major task. Write to `hot.md` at session end.

---

## hot.md — The Session Context File

`hot.md` is Zeref's working memory. It answers: *What is happening right now?*

### Structure

```markdown
# Hot Context — [Date]

## Active Project
[Current project name and one-line status]

## Current Task
[What Zeref is working on right now]

## Pending Decisions
- [Decision 1 that needs resolution]
- [Decision 2]

## Recent Outputs
- [File or deliverable created this session]

## Open Risks
- [Risk 1 that could affect the plan]

## Next Recommended Move
[Single most important next action]
```

### hot.md Rules

**Read protocol:**
- Zeref reads `hot.md` before any major task in a session
- If `hot.md` is empty or stale (>48 hrs), Zeref starts fresh and notes the gap

**Write protocol:**
- At session end (or before handoff), update `hot.md` with current state
- Overwrite — don't append. Only current state matters.
- Keep it under 50 lines. If it grows beyond that, archive to `log.md`.

**Never put in hot.md:**
- Completed tasks (move to `log.md`)
- Long-term strategy (move to domain pages)
- Research or reference material (move to `sources/`)

---

## wiki/ Directory Structure

```
wiki/
  hot.md          ← Session context (read first, always)
  index.md        ← Master index of all wiki pages
  log.md          ← Session history (append-only)
  brain/          ← Long-term strategy and system design
  career/         ← Career positioning, job targets, interview prep
  decisions/      ← Decision log (major choices + reasoning)
  fleet/          ← Skills fleet documentation
  learning/       ← Notes from courses, books, projects
  memory/         ← Project-specific memory files
  meta/           ← System documentation for Zeref itself
  projects/       ← Active and past project pages
  sources/        ← Research, references, external content
```

---

## log.md — Session History

`log.md` is append-only. Each session end, add an entry:

```markdown
## [Date] — [Session Topic]

**Objective:** [What was being worked on]
**Outputs:** [Files created, decisions made]
**Key decisions:** [What was decided and why]
**Next move:** [What to do next time]
**Status:** [complete | in-progress | blocked]
```

Never edit old entries. Log is a record, not a living doc.

---

## Domain Pages

Long-term knowledge lives in domain pages under `wiki/` subdirectories.

### brain/ — Strategy Layer

```
brain/
  positioning.md      ← Core positioning statement (update quarterly)
  transformation.md   ← Chaos → Systems → Execution chain
  system-design.md    ← How Zeref OS itself is architected
```

### career/ — Career Layer

```
career/
  targets.md          ← Companies and roles on radar
  narrative.md        ← Career story for interviews and applications
  portfolio.md        ← Portfolio projects and case study status
  applications.md     ← Active job applications log
```

### projects/ — Project Layer

Each active project gets its own page:

```markdown
# [Project Name]

## Status
[active | paused | complete]

## Objective
[What this project is trying to achieve]

## Current Phase
[Discovery | Design | Build | Launch | Post-launch]

## Outputs
- [Output 1 with file path or link]
- [Output 2]

## Open Questions
- [Question 1]

## Key Decisions
- [Decision 1: what was decided and why]

## Next Move
[Single most important next action]
```

---

## Memory + MCP: The Full Picture

When MCP connectors are active, memory expands:

| Memory Layer | Without MCP | With MCP |
|-------------|-------------|----------|
| **hot.md** | Local file | Local file (unchanged) |
| **Projects** | wiki/projects/*.md | + Linear issues, Notion pages |
| **Documents** | Copy-paste required | Fetched directly |
| **Decisions** | wiki/decisions/*.md | + Notion Decision Log page |
| **Calendar** | Unknown | Google Calendar → session planning |

**Best practice:** Keep `hot.md` as source of truth. MCP is for fetching, not for replacing the wiki.

---

## Caveman Handoff Protocol

At the end of a long session, run `/zeref-handoff` to produce a compressed handoff block.

Handoff format:

```
## Zeref Handoff — [Date]

**Objective:** [What the session was working toward]
**State:** [What got done vs. not done]
**Files:** [Key files touched, with exact paths]
**Decisions:** [Choices made and reasoning]
**Risks:** [What could break or needs attention]
**Commands:** [Exact bash commands if any were run]
**Next move:** [Single most important next action]
```

Paste handoff into:
- `wiki/log.md` entry for this session
- New Claude session at start (if continuing)
- GitHub commit message body (if relevant)

---

## Memory Discipline Rules

**Never invent:**
- File contents you haven't read
- API responses you haven't called
- Notion page contents you haven't fetched
- Repo state you haven't checked

**Always verify before acting:**
- If hot.md says "file exists at X" — confirm with `ls` before using
- If memory says "decision was made" — read the decision log before building on it
- If prior session output is referenced — read the file before assuming it's current

**State unknowns explicitly:**
```
"hot.md shows project Y was active — I don't have current status. Proceeding with assumption it's still active."
```

---

## Obsidian Configuration

Obsidian is the recommended viewer for the wiki. It renders Markdown with backlinks, graph view, and search.

### Recommended plugins (free)
- **Dataview** — query wiki pages as a database
- **Calendar** — visualize log.md entries by date
- **Templater** — auto-populate new project pages from template

### Vault settings
- Default new note location: `wiki/`
- Attachment folder: `wiki/assets/`
- Excluded files: none (Obsidian reads all)

### Link format
Use wikilinks: `[[hot]]`, `[[projects/zeref-os]]`  
These work in Obsidian but not GitHub — use relative Markdown links in docs meant for GitHub.

---

## Next Steps

- [06_Workflow_Examples.md](06_Workflow_Examples.md) — See memory in real workflows
- [09_Notion_Dashboard.md](09_Notion_Dashboard.md) — Mirror wiki structure in Notion
