---
description: Full system audit. Runs memory lint, skill registry validation, and a final executive review pass on recent outputs. Use periodically or before major milestones.
---
Run a full Zeref system audit with three sections:

1. **Memory Lint** — Check `wiki/hot.md`, `wiki/log.md`, `wiki/index.md` for staleness, missing entries, broken links, and unresolved contradictions.
2. **Skill Registry Validation** — Run `zeref-validate.py` logic against all skills in `skills/`. Report pass / warn / fail per skill with remediation notes.
3. **Executive Review** — If `$ARGUMENTS` includes a `recent_output_path`, review that output for completeness, hallucination risk, and professional quality.

End with a prioritized action list of issues found. If no issues, confirm system is healthy.
