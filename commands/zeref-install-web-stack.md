---
description: Scaffolds a new web project with Zeref's recommended stack. Outputs folder structure, boilerplate files, README, and first-run instructions. Use at project kickoff.
---
Scaffold a new web project for `$ARGUMENTS` (required: `project_name`). Output:

1. **Folder tree** — standard structure for the chosen stack
2. **Boilerplate files** — index, config, README, `.env.example`
3. **Stack rationale note** — why this stack for this project type
4. **First-run instructions** — copy-paste commands to initialize and run

Default stack: Next.js + Tailwind + TypeScript. If `stack_preset` is specified, use that. If `include_auth=true`, add auth boilerplate. If `include_db=true`, add database layer. If `mobile_first=true`, configure viewport and base styles for mobile. Save scaffolded files to `projects/[project_name]/` if `output_path` is not specified.
