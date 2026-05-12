# zeref-memory-protocol.md — Canonical Memory Protocol

> **Concept page.** Stable. Update rarely. Log decisions in `wiki/log.md` when this changes.
> **Last updated:** 2026-05-12
> **Status:** Stable

---

## Purpose

This page documents Zeref's complete memory protocol — how sessions are tracked, how knowledge compounds, when files get updated, and how to avoid memory decay. This is the canonical reference for all memory operations.

**Read this page before:** creating new wiki pages, deciding whether to log a session, performing a memory lint, or modifying any hot/index/log file.

---

## 1. The Karpathy Pattern — Foundation

Zeref's memory layer is based on **Andrej Karpathy's LLM Wiki pattern** (gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

The core idea:

> The LLM maintains a wiki — a set of structured, evolving pages. Raw sources (files, logs, repos) feed the wiki. The wiki feeds the LLM's working context. The LLM never re-reads raw sources from scratch if the wiki already captures their meaning.

**Three-tier reading order (always follow this):**

```
Tier 1 — hot.md          → session state, last handoff, current priorities
Tier 2 — index.md        → navigate to the right wiki page
Tier 3 — wiki pages      → project pages, concept pages, source pages
Tier 4 — raw files       → only when wiki page doesn't contain what you need
```

**Never skip tiers.** Reading raw files first wastes tokens, loses context, and breaks compounding memory.

---

## 2. hot.md Read-First Rule

**This is the single most important memory discipline in Zeref.**

```
Rule: Read wiki/hot.md at the start of EVERY session before doing anything else.
```

- hot.md tells you what was last worked on, what was decided, what is blocked, and what to do next.
- Without reading hot.md, you are flying blind — even if you remember the last session.
- hot.md is intentionally short (1–2 screens). It is designed to be read in under 60 seconds.
- If hot.md looks stale (last updated >2 sessions ago), run a memory lint before continuing.

**Reading hot.md is not optional. It is how Zeref stays coherent.**

---

## 3. When To Update hot.md

Update hot.md at the **end** of any session that:

- Produced a meaningful output (file, decision, architecture change, design)
- Made a decision that affects future sessions
- Changed the priority queue
- Created or resolved a pending decision
- Changed the active constraint list
- Produced a handoff to another environment

**Do not update hot.md** for trivial sessions (quick fixes, one-off answers, small lookups that produced no lasting state).

**hot.md update checklist:**
```
[ ] Current Session block updated with today's date and session #
[ ] Active Projects table reflects current status
[ ] Last Handoff block updated with today's outputs, decisions, and next action
[ ] Pending Decisions updated — resolved items removed, new items added
[ ] Priority Queue updated — completed items removed, new items added
[ ] Notes section updated with any important observations
```

---

## 4. When To Write log.md Entries

`wiki/log.md` is append-only. Write an entry when the session:

- Produced a file (code, design, document, report)
- Made an architecture or system decision
- Confirmed or changed a constraint
- Completed a phase or milestone
- Produced a handoff to another environment or tool
- Updated the wiki itself

**Skip logging for:**
- Trivial fixes (typos, small rewrites, one-line patches)
- Quick factual lookups with no decision
- Sessions that produced nothing lasting

**Log format (always use this exactly):**
```
---
Date:              YYYY-MM-DD
Session title:     [Short descriptive title]
Task type:         [Code from routing model — SYS / DEV / UX / etc.]
Environment:       [Claude Chat / Claude Code / Claude Cowork / Perplexity Computer / Other]
Key outputs:       [What was produced]
Decisions made:    [What was confirmed or changed]
Memory updated:    [Which wiki pages were created or updated]
Next priority:     [Single most logical next step]
---
```

**Append rule:** New entries go at the **top** of the log, below the format block and above previous entries. Never edit or delete past entries.

---

## 5. index.md Maintenance Rules

`wiki/index.md` is the master navigation map. It must stay current.

**Register every new wiki page** in the correct section of index.md within the same session it is created.

**Maintenance rules:**
- One row per page. No duplicates.
- Update `Last Updated` every time a page is substantively edited (not for typo fixes).
- Valid status values: `Active` · `Stable` · `Draft` · `Paused` · `Complete` · `Deprecated` · `Planned` · `Archived`
- Do not add raw notes to index.md. It is a map, not a notebook.
- Do not remove rows for deprecated pages — change status to `Deprecated` instead.
- If a section grows beyond ~50 rows, create a sub-index and link to it.

**index.md is wrong until every wiki page appears in it.** If you create a page without registering it, it is invisible to future sessions.

---

## 6. When To Create New Pages

### New project page (`wiki/projects/[slug].md`)
Create when:
- A new project has a defined objective and will span more than one session
- A project needs its own architecture, decision log, and status tracking

Template minimum:
```
# [Project Name] — Project Memory Page
Objective / Architecture / Decisions / Status / Phases / Open Questions / Risks / Workspace Locations
```

### New concept page (`wiki/concepts/[slug].md`)
Create when:
- A rule, model, protocol, or decision is durable and needs to be referenced across multiple sessions or projects
- A concept is referenced in more than 2 sessions without a dedicated page

Template minimum:
```
# [Concept Name] — Canonical Documentation
Purpose / Core Rules / When To Apply / Anti-Patterns / Revision History
```

### New source page (`wiki/sources/[slug].md`)
Create when:
- A reference (URL, repo, guide, gist) is used in more than one session
- A reference needs a summary that would otherwise be re-fetched each time

Template minimum:
```
# [Source Name] — Reference
URL / Why It Matters / Key Takeaways / Last Reviewed
```

---

## 7. Memory Lint Triggers

A **memory lint** is a brief audit of the wiki to check for decay, inconsistency, or gaps.

**Run a memory lint when:**
- hot.md was last updated more than 3 sessions ago
- The Priority Queue in hot.md has items older than 2 weeks with no status update
- A concept page references a decision that was later reversed (without the reversal being logged)
- Index.md is missing pages that exist in the wiki folder
- log.md entries contradict hot.md
- Yash explicitly asks for a memory lint

**Memory lint checklist:**
```
[ ] hot.md is current (updated within last 2 sessions)
[ ] All wiki pages appear in index.md
[ ] No wiki pages listed in index.md are missing from the folder
[ ] log.md entries are consistent with decisions in concept pages
[ ] All Pending Decisions in hot.md are still unresolved (remove resolved ones)
[ ] Priority Queue reflects current reality (not last month's priorities)
[ ] No concept pages contain outdated rules that were formally changed
[ ] Source pages have been reviewed within a reasonable timeframe
```

**Lint output:** Update hot.md Notes section with lint result and date. Log if significant corrections were made.

---

## 8. Single-Writer Discipline

Following the claude-obsidian and Karpathy pattern: **Zeref is the sole writer of wiki pages within a session.**

- Yash can request updates and provide information, but does not write directly to wiki pages mid-session.
- Zeref writes all updates at the end of a session, not piecemeal during it.
- This prevents race conditions, contradictions, and half-states in the wiki.
- Exception: Yash may directly edit hot.md between sessions to add notes or adjust priorities.

---

## 9. Memory Layer File Reference

| File | Role | Read When | Update When |
|------|------|-----------|------------|
| `wiki/hot.md` | Live session state | Start of every session | End of any meaningful session |
| `wiki/index.md` | Navigation map | After reading hot.md | When any wiki page is created or status changes |
| `wiki/log.md` | Append-only session log | When reviewing history | End of any session with meaningful output |
| `wiki/projects/` | Per-project memory | Before working on a project | When project status, phases, or decisions change |
| `wiki/concepts/` | Canonical rules and models | Before applying a rule or protocol | When a rule is formally changed |
| `wiki/sources/` | Reference links and summaries | Before re-fetching a reference | When a source is reviewed or becomes stale |
