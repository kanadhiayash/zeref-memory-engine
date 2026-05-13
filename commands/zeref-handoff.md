---
description: Runs Caveman compression and produces a full handoff block ready to paste into a new Claude session, GitHub, Notion, or local file. Use before ending a long session or switching contexts.
---
Compress the current session state using Caveman compression. Produce a handoff block containing: session state summary, active projects, key decisions made this session, pending items, and the single most important next move.

If `$ARGUMENTS` specifies a `destination` (github / notion / file), format the output accordingly. If `compression_level=max`, drop all non-essential context. If `include_decisions=true`, include the full decision log entries from this session.

Output the handoff block in a copy-paste-ready format. Follow with save instructions for the specified destination.
