# Zeref OS — Troubleshooting

**Version:** 2.0.0 | **Updated:** May 2026

---

## Quick Diagnosis

**What's wrong?**

| Symptom | Jump to |
|---------|---------|
| Wrong skill being used | [Routing Problems](#routing-problems) |
| Skill not triggering | [Skill Activation Issues](#skill-activation-issues) |
| Memory not loading | [Memory Issues](#memory-issues) |
| MCP connector not responding | [MCP Issues](#mcp-issues) |
| Validation script fails | [Validation Errors](#validation-errors) |
| Plugin not installing | [Plugin Install Errors](#plugin-install-errors) |
| Zeref inventing information | [Hallucination Prevention](#hallucination-prevention) |
| Wrong tone or format | [Behavior Drift](#behavior-drift) |

---

## Routing Problems

### Symptom: Wrong skill activated

**Cause:** Task description matches multiple skill triggers. Zeref picks closest match.

**Fix:**
```
Be explicit about task type:
"UX task: Design the onboarding flow..."
"DEV task: Build the Firebase auth..."
"BIZ task: Validate the market for..."
```

Adding the layer prefix forces correct routing.

---

### Symptom: Too many skills activated

**Cause:** Complex request triggers over-routing.

**Fix:** Break into smaller tasks. One task per skill:
```
Step 1: "Summarize the research findings" (zeref-ux-research-lead)
Step 2: "Define the problem statement" (zeref-ux-problem-definition-specialist)
Step 3: "Build the user flow" (zeref-ux-user-flow-designer)
```

---

### Symptom: Support skills ignored

**Cause:** Lead skill handled the task alone. Support skills only activate when lead delegates.

**This is correct behavior** — smallest useful stack. If output is complete without support, no delegation needed.

---

## Skill Activation Issues

### Symptom: Custom skill not triggering

**Check 1 — Trigger phrases:**
```bash
cat skills/my-custom-skill/SKILL.md | grep -A5 "triggers:"
```
Ensure trigger phrases match what you're typing.

**Check 2 — Skill file validity:**
```bash
python zeref-validate.py --verbose
```
Output shows which files fail and why.

**Check 3 — YAML frontmatter:**
All required fields must be present:
```yaml
---
name: zeref-[layer]-[role]
layer: [valid layer]
role: [Role Title]
description: [one-line description]
triggers:
  - "phrase 1"
  - "phrase 2"
---
```

Missing any field = skill invisible to router.

---

### Symptom: Built-in skill behaving unexpectedly

**Step 1:** Check Layer 4 — does your request contain override language?
```
"Keep this brief" → overrides skill's default output length
"Don't use headers" → overrides skill's formatting defaults
```

**Step 2:** Check Layer 3 — does ZEREFOS.md have a skill override?
```markdown
## Skill Overrides
- zeref-cnt-copywriter: Always write in first person
```

**Step 3:** If neither — run `/zeref-validate` to confirm skill file integrity.

---

## Memory Issues

### Symptom: hot.md not being read

**Cause:** Session started without `/zeref-activate`.

**Fix:** Start every session with:
```
/zeref-activate
```

Zeref reads `hot.md` and reports current context.

---

### Symptom: hot.md shows stale context

**Fix:** If hot.md is outdated, clear it explicitly:
```
"Ignore hot.md — start fresh. Active project: [name]. Current task: [task]."
```

Then update hot.md at end of session with `/zeref-save`.

---

### Symptom: Memory from previous session not available

**Cause:** hot.md was not updated at end of last session.

**Prevention:** Always run `/zeref-handoff` or `/zeref-save` before ending a session.

**Recovery:** Tell Zeref what context to load manually:
```
"Last session context: I was building the auth system for [project]. Completed: email auth. Next: Google OAuth."
```

---

## MCP Issues

### Symptom: Notion connector returns empty or errors

**Check 1 — Integration access:**
In Notion, each page must explicitly share access with your integration:
- Open the page → Share → Invite → Select your integration

**Check 2 — API token:**
```bash
curl -H "Authorization: Bearer YOUR_NOTION_TOKEN" \
     -H "Notion-Version: 2022-06-28" \
     https://api.notion.com/v1/users/me
```
Should return your user. If 401, token is wrong or expired.

**Check 3 — Claude Desktop connector:**
Claude Desktop → Settings → Connectors → Notion → Reconnect

---

### Symptom: GitHub MCP — permission errors

**Cause:** Personal access token missing `repo` scope.

**Fix:**
1. GitHub → Settings → Developer Settings → Personal Access Tokens
2. Edit token → Add `repo` scope (full, not just `public_repo`)
3. Copy new token → Update `settings.json`

---

### Symptom: Google Drive returns no files

**Cause:** Drive API not enabled in Google Cloud Console.

**Fix:**
1. Google Cloud Console → APIs & Services → Enable APIs
2. Search: Google Drive API → Enable
3. Reconnect in Claude Desktop

---

### Symptom: MCP connector slow

**Cause:** Broad queries hit API limits.

**Fix — be specific:**
```
❌ "Search all my Notion pages"
✅ "Fetch the page titled 'Q2 Product Strategy'"

❌ "Search my GitHub repo for everything"
✅ "Read the file src/auth/firebase.js"
```

---

## Validation Errors

### `zeref-validate.py` error: Missing required field

```
ERROR: skills/zeref-ux-custom/SKILL.md — missing required field: 'triggers'
```

**Fix:** Open the skill file and add the missing frontmatter field:
```yaml
triggers:
  - "trigger phrase 1"
  - "trigger phrase 2"
```

---

### `zeref-validate.py` error: Invalid layer value

```
ERROR: skills/zeref-custom/SKILL.md — invalid layer: 'design' (must be one of: ux, dev, biz, mkt, cnt, qa, final, system, hq)
```

**Fix:** Update the `layer` field to a valid value. `design` is not a valid layer — use `ux`.

---

### `zeref-validate.py` error: Registry out of sync

```
ERROR: Registry missing 3 skills present in skills/ directory
```

**Fix:**
```bash
python zeref-validate.py --rebuild-registry
```

Regenerates `registry/skills.json` from current skill files.

---

## Plugin Install Errors

### `claude plugin install .` — file not found

**Cause:** Not in the repo root.

**Fix:**
```bash
cd /path/to/zeref-agent-os
ls manifest.json  # Should exist
claude plugin install .
```

---

### Plugin installed but `/zeref-activate` not found

**Cause:** Commands not in `commands/` directory, or manifest not pointing to them.

**Check:**
```bash
cat manifest.json | grep commands
ls commands/
```

Both should reference the same command files.

---

### Plugin version conflict

```
ERROR: Plugin 'zeref-agent-os' already installed (v1.x). Use --force to overwrite.
```

**Fix:**
```bash
claude plugin install . --force
```

---

## Hallucination Prevention

Zeref follows anti-hallucination rules. If it invents information, use these prompts:

### "You just made that up"

```
"Stop. You don't have access to [Notion/GitHub/file]. State what you actually know vs. what you're assuming."
```

Zeref will separate facts from assumptions explicitly.

---

### Force evidence mode

```
"Only state things you have direct evidence for. Label assumptions with [ASSUMPTION]."
```

---

### Verify before building

Before any code that depends on external state:
```
"First, confirm you've actually read [file/API/connector]. If not, say so."
```

---

## Behavior Drift

### Symptom: Responses getting verbose over long sessions

**Cause:** Context accumulates. Zeref over-explains to handle ambiguity.

**Fix:** Compress with Caveman:
```
/caveman
```

Or reset tone explicitly:
```
"Keep responses under 150 words. No headers. Direct answers only."
```

---

### Symptom: Skill routing headers disappeared

**Cause:** User request in Layer 4 suppressed them.

**Fix:**
```
"Resume full Zeref routing mode. Show skill stack for major tasks."
```

---

### Symptom: Wrong language or tone

**Cause:** ZerefClaude.md (Layer 2) not loaded in current session.

**Fix:** Paste the relevant section from `_templates/ZerefClaude.md` or start a new session with the project instructions loaded.

---

## Getting Help

**Validation first:**
```bash
python zeref-validate.py --full --verbose
```

**Check the layers:**
1. Layer 5 — Safety rule triggered? (unusual task refusal)
2. Layer 4 — Your request overriding skill behavior? (explicit instructions)
3. Layer 3 — ZEREFOS.md rule overriding skill? (check project instructions)
4. Layer 2 — Global instructions misaligned? (check ZerefClaude.md)
5. Layer 1 — Skill file corrupted or missing trigger? (run validate)

**GitHub Issues:**
[github.com/kanadhiayash/zeref-agent-os/issues](https://github.com/kanadhiayash/zeref-agent-os/issues)

---

## Next Steps

- [02_Prompt_Architecture.md](02_Prompt_Architecture.md) — Layer system deep dive
- [03_Skills_Fleet_Guide.md](03_Skills_Fleet_Guide.md) — All 112 skills
