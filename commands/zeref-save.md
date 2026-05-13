---
description: Saves current session state to memory. Writes hot.md update, log.md entry, and flags index.md delta. Use at the end of any work session to preserve state.
---
Save the current session state to the Zeref wiki memory layer. `$ARGUMENTS` must include `session_summary`.

1. **Update `wiki/hot.md`** — update Current Session block, update Last Handoff block with today's date, outputs, decisions, and next priority
2. **Append to `wiki/log.md`** — new log entry at the TOP with date, session title, task type, key outputs, decisions made, memory updated, next priority
3. **Flag `wiki/index.md`** — note any new or updated pages from this session

If `project_tag` is provided, update that project page's Last Touched date. If `decision_log_entry` is provided, add it to the decisions section. If `next_priority` is provided, insert it at the top of the Priority Queue.

Confirm what was written to each file. Do not skip the log entry.
