---
description: Recalls specific memory from the wiki layer. Takes a topic or keyword and returns relevant hot.md, index.md, concept page, or project page entries ranked by relevance.
---
Search the Zeref wiki for context on `$ARGUMENTS` (required: `topic`). Check in this order: `wiki/hot.md`, `wiki/index.md`, relevant concept pages in `wiki/concepts/`, relevant project pages in `wiki/projects/`, source pages in `wiki/sources/`.

Return ranked recall results. For each match include: the matching snippet, source file path, and a one-line relevance note. Group results by source type.

If `source_filter` is specified, only search that source type. If `max_results` is specified, cap the output. If nothing relevant is found, say so explicitly — do not fabricate wiki content.
