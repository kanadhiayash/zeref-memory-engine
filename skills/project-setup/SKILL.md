---
name: project-setup
description: Conversational interview to populate config/PROJECT.md, config/PRIVACY.md, config/PERMISSIONS.md, config/PARENT_SYNC.md, config/BUDGET.md. Activates on first /start or when any required config is missing.
trigger:
  - first /start
  - missing config/PROJECT.md
  - user says "set up project"
model: claude-sonnet-4-6
max_turns: 20
---

# project-setup

## Mission

Convert any user's messy project goal into structured config in one conversation. Conversational, not formal.

## Interview (minimum)

Ask these in natural language flow, not as a numbered form:

1. What is this project? (1 sentence)
2. What problem does it solve?
3. What's out of scope?
4. Who else is involved? (stakeholders + decision authority)
5. What constraints are non-negotiable?
6. What tools / MCP servers / repos are in play?
7. Privacy mode? (`exact` / `abstract` / `local-only`)
8. Is there a parent project? (for rollup)
9. What model tier are you using? (Haiku / Sonnet / Opus)
10. Anything else memory should hold from day one?

## Output

Write 5 config files. Each gets YAML frontmatter from the answers + a markdown body the user can hand-edit later.

- `config/PROJECT.md`
- `config/PRIVACY.md`
- `config/PERMISSIONS.md` (defaults; ask if user wants overrides)
- `config/PARENT_SYNC.md` (enabled only if user said yes to Q8)
- `config/BUDGET.md`

After writing, confirm:
> "Wrote 5 config files to `config/`. Verify they exist before we proceed. Run `/start` again to boot the session."

## Safety

- All writes go through `memory-keeper` → `privacy-guardian`
- If user declines to answer a question, leave the field empty with a `# TODO` marker — never invent
