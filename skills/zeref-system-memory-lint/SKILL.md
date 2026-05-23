---
name: zeref-system-memory-lint
title: Memory Lint
description: "Memory Lint. Use for: clean up wiki, lint memory, check wiki health, wiki audit."
category: system
model: claude-haiku-4-5-20251001
effort: low
max_turns: 10
trigger_phrases:
  - "clean up wiki"
  - "lint memory"
  - "check wiki health"
  - "wiki audit"
model_preference: haiku
risk_level: low
dependencies:
  - references/zeref-qa-gate.md
  - references/zeref-safety-principles.md
---

# zeref-system-memory-lint

## Mission
Audit the Zeref wiki for staleness, orphans, bloat, and inconsistency. Report findings. Never delete — flag for user decision only.

## Use This Skill When
- hot.md has grown beyond 3 sessions (archive oldest to log.md)
- User requests wiki health check or cleanup
- Index.md references pages that may be stale
- Before a major new project starts (clear hot cache)

## Execution Workflow

### Step 1: Read All Three Files
Read wiki/hot.md, wiki/index.md, wiki/log.md.

### Step 2: Check Hot.md Health
- [ ] Fewer than or equal to 3 sessions? (if >3 → archive oldest)
- [ ] Each entry <150 words?
- [ ] No invented content (facts labeled, assumptions labeled)?
- [ ] Context-forward section present in each entry?

### Step 3: Check Index.md Health
- [ ] All entries have descriptions?
- [ ] Any entries marked stale or TBD?
- [ ] Domain coverage matches actual skills in registry?

### Step 4: Check Log.md Health
- [ ] Append-only format maintained?
- [ ] Timestamps present?
- [ ] No duplicate entries?

### Step 5: Report
Output structured lint report:
```
WIKI LINT REPORT — [Date]
hot.md: [pass / N issues]
index.md: [pass / N issues]
log.md: [pass / N issues]
Action needed: [specific items or "none"]
```

## Safety
NEVER delete wiki entries without explicit user approval.
Flag issues — do not auto-fix beyond archiving overflowed hot.md sessions.