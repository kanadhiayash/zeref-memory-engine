# CLAUDE.md — Zeref OS Project Instructions

**Layer:** 3 — Project Instructions  
**Authority:** Overrides ZerefClaude.md (Layer 2) defaults for this project. Overridden by explicit user requests (Layer 4).  
**Usage:** Place at repo root or `~/.claude/CLAUDE.md`. For Claude Projects, paste into Project Instructions field.

---

## PROJECT IDENTITY

**Project:** [PROJECT NAME]  
**Type:** [portfolio | client | learning | system | product]  
**Phase:** [Discovery | Design | Build | Launch | Post-launch]  
**Started:** [DATE]  
**Objective:** [What this project is trying to achieve in 1-2 sentences]

---

## INSTRUCTION HIERARCHY FOR THIS PROJECT

Follow instructions in this order:
1. Safety, privacy, security, and irreversible-action rules
2. Explicit request in this conversation
3. This CLAUDE.md (project scope)
4. ZerefClaude.md (global Zeref rules)
5. Zeref Skills Fleet conventions (smallest-useful-stack, Caveman, evidence discipline)

If instructions conflict: surface conflict, state interpretation, then act.

---

## PROJECT-SPECIFIC BEHAVIOR

### Tech stack
[List the actual tech stack for this project]
- Frontend: [e.g., React Native / SwiftUI / Next.js]
- Backend: [e.g., Firebase / Supabase / Node]
- Database: [e.g., Firestore / PostgreSQL]
- Design: [e.g., Figma]
- Deployment: [e.g., Expo EAS / Vercel / App Store]

### Coding conventions
- [Convention 1 — e.g., TypeScript strict mode, no `any`]
- [Convention 2 — e.g., Functional components only, no class components]
- [Convention 3 — e.g., Error handling: always return `{data, error}` pattern]

### Output preferences
- [e.g., Full file replacements, not diffs]
- [e.g., Beginner-readable comments on complex functions]
- [e.g., Accessibility notes on every UI component]

---

## SKILL ROUTING FOR THIS PROJECT

**Default routing by task type:**

| Task | Lead Skill | Support |
|------|-----------|---------|
| UX design | zeref-ux-product-designer | zeref-ux-user-flow-designer |
| Frontend code | zeref-dev-frontend-engineer | zeref-dev-[stack]-specialist |
| Backend code | zeref-dev-backend-engineer | zeref-dev-firebase-specialist |
| Content | zeref-cnt-[type] | — |
| Business | zeref-biz-business-strategist | — |
| QA | zeref-qa-lead | zeref-qa-[type]-tester |

**Skill overrides for this project:**
- [Override 1 — e.g., "zeref-cnt-copywriter: Always write in first person"]
- [Override 2 — e.g., "zeref-qa-lead: Skip functional testing for prototype deliverables"]

---

## MEMORY PROTOCOL

**Wiki location:** `wiki/projects/[project-slug].md`  
**Hot context:** Read `wiki/hot.md` before every major task  
**Notion page:** [Link to Notion project page if exists]  
**Linear project:** [Link to Linear project if exists]

**Key decisions log:** `wiki/decisions/[project-slug]/`

---

## EVIDENCE DISCIPLINE

For this project, never assume:
- Contents of files in `[critical directories]` without reading them
- API response shapes without checking
- Database schema without reading migration files
- Current state of [list external systems] without fetching

Always verify before building on prior session outputs.

---

## PROJECT-SPECIFIC CONSTRAINTS

- [Constraint 1 — e.g., "No paid services — free tier or open source only"]
- [Constraint 2 — e.g., "iOS-first, Android parity in v2"]
- [Constraint 3 — e.g., "Must ship by [date]"]
- [Constraint 4 — e.g., "Portfolio-ready: every output should be case-study documentable"]

---

## WORKSPACE UPDATES FOR THIS PROJECT

After major outputs, update:
- [ ] `wiki/projects/[project-slug].md` — project page
- [ ] `wiki/hot.md` — current session state
- [ ] Notion: [Project Name] — project tracker
- [ ] Linear: [Project Name] — if issue created
- [ ] GitHub: [repo-name] — if code committed

Do NOT claim updates happened unless they were actually executed.

---

## QUICK REFERENCE

**Key files:**
```
[List critical file paths for this project]
src/[main entry point]
[config file]
[schema file]
```

**Key commands:**
```bash
[Build command]
[Test command]
[Deploy command]
```

**Key URLs:**
- Design: [Figma URL]
- Staging: [URL]
- Production: [URL]
- Repo: [GitHub URL]
