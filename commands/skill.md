---
description: Review and approve skill drafts proposed by pattern-observer + pattern-to-skill (M3).
---

1. Check `skills/_drafts/` for pending drafts.
2. If empty → report "No skill drafts pending." and exit.
3. For each draft:
   - Show frontmatter + body summary
   - Show provenance (which events triggered the draft)
   - Prompt user: **approve** / **edit** / **reject** / **defer**
4. On `approve`: `git mv skills/_drafts/<name> skills/<name>` and log `{"event": "skill-approved", "target": "skills/<name>/"}`.
5. On `edit`: open draft for user editing, then re-prompt.
6. On `reject`: `git rm -rf skills/_drafts/<name>` and log `{"event": "skill-rejected", "target": "..."}`.
7. On `defer`: leave draft in place.

(Full implementation: M3 / v4.2.0. Until then, draft directory may not exist.)
