---
description: Review and approve skill drafts proposed by pattern-observer + pattern-to-skill. Approve, edit, reject, or defer each draft.
---

1. Read `memory/sync/outbound/patterns/` for new candidates emitted since last `/review-skill` run.
2. For each new candidate without a draft → invoke `pattern-to-skill` DRAFT operation.
3. Invoke `pattern-to-skill` REVIEW QUEUE operation:
   - List all `skills/_drafts/*/SKILL.md` with score, event count, drafted timestamp, description
   - Prompt user to pick one (numeric) OR `all` / `none` / `quit`
4. For each selected draft, invoke `pattern-to-skill` per-draft prompt:
   - Show frontmatter + body + provenance summary
   - Accept: `approve` / `edit` / `reject` / `defer`
5. Execute user choice via `pattern-to-skill`:
   - `approve` → `git mv skills/_drafts/<name> skills/<name>`, strip draft markers, log event, prompt for CHANGELOG line
   - `edit` → open file for user editing, re-prompt after save
   - `reject` → prompt for reason, `rm -rf` draft dir, mark candidate JSON `rejected_at`, log event
   - `defer` → leave in place, increment defer_count, log event
6. Report:
   ```
   Reviewed: <N> drafts
     approved: <N>
     edited: <N>
     rejected: <N>
     deferred: <N>
   ```

If no drafts pending → report "No skill drafts pending." and exit.
If no patterns detected yet → suggest "Run /done at the end of sessions to feed pattern-observer."
