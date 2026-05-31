---
name: pattern-to-skill
description: Drafts new skill files from patterns detected by pattern-observer. Drafts only — never auto-activates. User reviews via /skill.
trigger:
  - pattern-observer emits candidate (≥3 similar events in 72h)
  - /skill review
model: claude-opus-4-7
max_turns: 25
status: M3-stub
---

# pattern-to-skill

## Status

**M3 stub** — full implementation lands in v4.2.0.

## Mission (target)

Turn repeated work into reusable skills. Draft, never auto-activate.

## Flow (target)

1. Receive candidate cluster from `pattern-observer`
2. Extract common task signature, inputs, outputs
3. Generate draft `skills/_drafts/<draft-name>/SKILL.md`:
   - YAML frontmatter (name, description, trigger, model, max_turns)
   - Body with mission, operations, safety
   - Source provenance (event hashes that triggered the draft)
4. Add to `/skill` review queue
5. Log `{"event": "skill-drafted", "target": "skills/_drafts/<draft-name>/"}`

## /skill review flow (target)

1. List all drafts in `skills/_drafts/`
2. User picks one
3. Show draft + provenance
4. User: approve (move to `skills/`) / edit / reject / defer
5. If approved → `git mv skills/_drafts/<name> skills/<name>`

## Safety

- Drafts never auto-activate
- Approval is the only path from draft → active skill
- Drafts can be edited before approval
