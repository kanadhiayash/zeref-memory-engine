---
description: Runs the skill registry validator. Checks all skill files for required frontmatter fields, valid layer/role values, non-empty sections, and route integrity.
---
Validate all Zeref skill files in `skills/`. For each skill check:

- Required frontmatter fields present: `name`, `description`
- Required sections present: Mission, When To Use, When NOT To Use, Required Inputs, Deliverables, Workflow, Output Format, Token Discipline, Handoff Protocol
- No empty required sections
- `routes_to` references (if present) point to existing skill folders

If `$ARGUMENTS` includes a `target_skill`, validate only that skill file. If `strict_mode=true`, treat warnings as failures. If `output_format=summary`, only show fail/warn counts.

Report results grouped as: **Pass**, **Warn**, **Fail**. Each entry lists: skill file, field/section checked, status, remediation note. End with a summary count and top-priority fixes.
