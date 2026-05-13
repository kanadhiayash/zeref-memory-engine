---
description: Activates Zeref OS for a session. Reads hot.md, states current context, active projects, and pending decisions. Sets the working register and task type for the session.
---
Read `wiki/hot.md` to load the current session state. Report: active projects, pending decisions, top priority from the queue, and last handoff summary. If `$ARGUMENTS` includes a `task_override`, classify that task and select the minimum Zeref skill stack (1 lead + 0–3 support + 0–1 QA gate) to execute it. Otherwise end with a prompt asking what to work on first.
