# hot.md — Zeref Active Session State

> **ZEREF READ ORDER: This is the FIRST file Zeref reads at the start of every session.**
> Read this file completely before touching any other wiki file, any skill, or any command.
> After reading, check `wiki/index.md` for navigation, then drill into relevant project or concept pages.
> Update this file at the end of every session. Do not let it go stale.

---

## How To Use This File

- `hot.md` = the live brain state of the current or most recent Zeref session
- It answers: what is happening right now, what was just done, what is blocked, what is next
- **Read it first. Update it last.**
- When starting a new session: read this file, orient quickly, then execute
- When ending a session: update Current Session, Last Handoff, Pending Decisions, Priority Queue
- This file should never be more than 1–2 screens. Keep it dense and current.
- Stale hot.md = broken memory. If it hasn't been updated in 3+ sessions, run a memory lint.

---

## Current Session

```
Date:        [YYYY-MM-DD]
Session #:   [N]
Status:      [Active / Handoff / Idle]
Working on:  [Brief description of active task]
Environment: [Claude Chat / Claude Code / Claude Cowork / Perplexity Computer / Other]
Skill stack: [Lead skill — support skills — QA gate]
Caveman:     [Needed / Not needed]
```

---

## Active Projects

| Project | Status | Priority | Last Touched | Wiki Page |
|---------|--------|----------|-------------|-----------|
| Zeref V2 Rebuild | In Progress | P0 | 2026-05-12 | `wiki/projects/zeref-v2-rebuild.md` |
| [Project Name] | [Status] | [P0–P3] | [YYYY-MM-DD] | `wiki/projects/[slug].md` |
| [Project Name] | [Status] | [P0–P3] | [YYYY-MM-DD] | `wiki/projects/[slug].md` |

**Priority scale:** P0 = active/blocking · P1 = this week · P2 = this month · P3 = backlog

---

## Last Handoff

```
Date:          2026-05-12
Session title: Zeref V2 Rebuild — Phase 4 Memory Layer
Output:        Generated 7 wiki memory layer files (hot, index, log, projects, concepts, sources)
Decisions:     Memory layer follows Karpathy LLM Wiki pattern — hot.md read first
Next session:  Begin Phase 1 integration testing — validate ZEREFOS.md kernel with live skill routing
Open risk:     hot.md will go stale if not updated each session — enforce read-first discipline
Files changed:
  - wiki/hot.md (created)
  - wiki/index.md (created)
  - wiki/log.md (created)
  - wiki/projects/zeref-v2-rebuild.md (created)
  - wiki/concepts/zeref-routing-model.md (created)
  - wiki/concepts/zeref-memory-protocol.md (created)
  - wiki/sources/zeref-reference-links.md (created)
```

---

## Pending Decisions

| Decision | Context | Blocking? | Owner | Due |
|----------|---------|-----------|-------|-----|
| Confirm Graphify pilot scope | Run on zeref-skills-fleet folder or full OS vault? | No | Yash | Next session |
| Skill registry format | JSON vs. YAML vs. Markdown table? | No | Zeref | Phase 3 |
| Obsidian vault sync method | Manual copy, iCloud, or GitHub sync? | No | Yash | Before Phase 5 |
| [Decision] | [Context] | [Yes/No] | [Owner] | [Date] |

---

## Active Constraints

- **Free-first policy:** Default to free models, open-source repos, free APIs. No paid spend without explicit approval from Yash.
- **Smallest-stack principle:** 1 lead skill + 1–3 support skills + 1 QA gate only when needed. Never activate all skills.
- **No hallucination rule:** Never invent file contents, tool outputs, connector access, GitHub contents, Figma contents, or research findings.
- **Approval required for:** Publishing, deploying, deleting, sending, scheduling, moving files, or any irreversible action.
- **Surgical changes only:** Touch only what is required. Every changed line must trace to the request.
- **Memory lint trigger:** If hot.md feels stale or inconsistent, run memory lint before continuing.

---

## Priority Queue

```
[P0] Phase 1 integration testing — validate ZEREFOS.md kernel
[P0] Confirm skill routing works correctly with V2 architecture
[P1] Build machine-readable skill registry
[P1] Rewrite highest-priority skill descriptions with precise trigger phrases
[P2] Graphify pilot on zeref-skills-fleet folder
[P2] Release governance files (LICENSE, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md)
[P3] LinkedIn/Substack content system
[P3] Portfolio packaging for Zeref V2 proof of work
```

---

## Notes

```
[Add session-specific notes here — blockers, observations, follow-ups, risks]
- Zeref V2 Rebuild confirmed 5-layer architecture: Identity → Skill → Memory → Graph → Command
- Memory layer (this wiki) is Phase 4 of the V2 rebuild
- hot.md read-first rule is the single most important memory discipline to enforce
- Karpathy pattern: index first → navigate wiki → drill into raw files only when needed
```
