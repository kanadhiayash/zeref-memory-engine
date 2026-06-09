---
name: grep-with-context
description: Draft skill — wraps `grep -r -B2 -A2 <pattern>` for searching with surrounding lines. NOT AUTO-ACTIVATED — review via /review-skill.
trigger:
  - "grep with context"
  - "search with surrounding lines"
model: claude-haiku-4-5
max_turns: 5
status: draft
---

# grep-with-context (DRAFT)

## Mission

Repeated pattern detected in memory/patterns/PATTERNS.jsonl: 5 events of `grep -r -B2 -A2`. Draft skill proposes a wrapper.

## Operations

Run `grep -r -B2 -A2 "<pattern>" <directory>` and format output.

## Safety

DRAFT — awaits /review-skill approval. Will NOT auto-activate.
