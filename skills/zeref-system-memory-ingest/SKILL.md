---
skill: zeref-system-memory-ingest
title: Memory Ingest
description: "Memory Ingest. Use for: save to wiki, save session, log this, remember this, update wiki."
category: system
model: claude-haiku-4-5-20251001
effort: low
max_turns: 10
trigger_phrases:
  - "save to wiki"
  - "save session"
  - "log this"
  - "remember this"
  - "update wiki"
model_preference: haiku
risk_level: low
dependencies:
  - references/zeref-qa-gate.md
  - references/zeref-safety-principles.md
---

# zeref-system-memory-ingest

## Mission
Ingest any session output, decision, or context into the Zeref wiki (hot.md / index.md / log.md) using the Karpathy hot/index/log pattern. Compress and structure before writing. zeref-memory-keeper is the only writer.

## Use This Skill When
- User says "save session", "save to wiki", "log this", "remember this"
- Major task completed and context should carry forward
- Architecture or strategy decision made that affects future sessions
- At end of any session involving ZEREFPROJECT.md updates

## Execution Workflow

### Step 1: Classify What to Save
- Decision? → wiki/hot.md session entry + wiki/log.md append
- Project context? → wiki/hot.md + relevant project page
- Reference or research? → wiki/index.md entry + source page

### Step 2: Compress (Caveman-style)
Before writing, compress the content:
- Drop explanation prose
- Keep: decisions, paths, commands, constraints, risks, next actions
- Target: <150 words per session entry in hot.md

### Step 3: Write (via zeref-memory-keeper)
hot.md format:
```
## [Date] | [Project]
Decisions: [bullet list]
Context forward: [what next session needs to know]
Blocked: [anything blocked]
```
Append to log.md: `[timestamp] | hot.md updated | [1-line summary]`
Archive oldest hot.md entry to log.md if >3 sessions.

### Step 4: Confirm
State: "Saved to wiki/hot.md. Session entry: [1-line summary]."

## Safety
Never write to any file except wiki/hot.md, wiki/index.md, wiki/log.md without explicit instruction.
Never invent or paraphrase exact commands, paths, or constraints — preserve verbatim.