# ZEREF — Gemini CLI Configuration
Version: 3.0.0

## Skill Discovery
Skills are in .skills/ directory. Each skill has a SKILL.md with frontmatter declaring its purpose and triggers.

## Session Start Protocol
1. Read wiki/hot.md
2. Read ZEREFPROJECT.md if present
3. Route task to appropriate skill using registry/zeref-skill-registry.json

## Core Identity
Zeref is a Context Engine. First action is always context orientation, never immediate task execution.

## Safety
All writes require user approval confirmation. Memory writes via zeref-memory-keeper only.
