---
name: wiki-maintenance
description: Maintains canonical wiki state — INDEX consistency, page summaries, decisions log, risks register, open questions queue. Activates after writes and on consolidation requests.
trigger:
  - post-write (called by memory-keeper)
  - /done
  - user says "clean up wiki"
model: claude-haiku-4-5
max_turns: 15
---

# wiki-maintenance

## Mission

Keep `memory/wiki/` clean, indexed, and useful.

## Operations

### POST-WRITE (called by memory-keeper after every write)
1. Update `INDEX.md` row for the affected domain
2. If page > 1500 lines → propose archival to `ARCHIVE/`
3. Re-grade entries via `evidence-curator` if staleness threshold crossed

### CONSOLIDATE (on /done or explicit request)
1. Scan all wiki pages
2. Merge duplicate decisions
3. Move resolved questions to DECISIONS.md
4. Archive items > 90 days old to `ARCHIVE/`
5. Rewrite INDEX.md summaries

### LINT (on demand)
1. Check format compliance on all wiki pages
2. Report broken cross-references
3. Report orphaned domains (in INDEX but no page)

## Safety

- All writes via `memory-keeper`
- Archive moves are non-destructive (copy + mark superseded, never delete)
