# Zeref OS — Installation Guide

**Version:** 2.0.0 | **Updated:** May 2026

---

## Overview

This guide covers all three installation tiers:

- **[Tier 1: Full Zeref OS](#tier-1-full-zeref-os)** — 112 skills + memory + MCP (30–45 min)
- **[Tier 2: Minimal Setup](#tier-2-minimal-setup)** — Skills only, no memory (10–15 min)
- **[Tier 3: Custom Build](#tier-3-custom-build)** — Fork and adapt (1–2 hrs)

---

## Tier 1: Full Zeref OS

### Step 1 — Clone the Repository

```bash
git clone https://github.com/kanadhiayash/zeref-agent-os.git
cd zeref-agent-os
```

Verify contents:
```bash
ls -la
# Should show: skills/, commands/, agents/, registry/, wiki/, docs/
```

---

### Step 2 — Install as Claude Plugin

**Via Claude Code CLI:**
```bash
claude plugin install .
```

**Via Claude Desktop App:**
1. Open Claude Desktop
2. Click **Plugins** in sidebar
3. Click **Add Plugin**
4. Enter: `https://github.com/kanadhiayash/zeref-agent-os`
5. Click **Install**

**Verify installation:**
```
/zeref-validate
```
Should return: `✅ Zeref Agent OS v2.0.0 — All systems nominal`

---

### Step 3 — Load the Kernel (ZEREFOS.md)

The kernel is the global operating instructions for Claude.

**Option A — Claude Project (Recommended):**
1. Open Claude → **Projects** → Create new project or open existing
2. Click **Project Instructions**
3. Copy full contents of `ZEREFOS.md` from repo root
4. Paste into Project Instructions field
5. Save

**Option B — Claude Code CLAUDE.md:**
```bash
cp ZEREFOS.md ~/.claude/CLAUDE.md
```

**Option C — Per-session (not recommended):**
Paste ZEREFOS.md content at the start of each conversation.

---

### Step 4 — Set Up Obsidian Memory Vault

Zeref uses Obsidian as its external memory system.

**Install Obsidian:**
- Download from [obsidian.md](https://obsidian.md) (free)

**Create the vault:**
```bash
# Copy the pre-configured wiki structure
cp -r wiki/ ~/Documents/ZerefOS-Wiki
```

Open Obsidian → **Open folder as vault** → Select `ZerefOS-Wiki`

**Configure hot.md as homepage:**
1. Obsidian → Settings → Core Plugins → Daily Notes → Off
2. Settings → Options → Files & Links → Default location for new notes: `wiki/`
3. Open `hot.md` — this is your session context file

**Vault structure:**
```
ZerefOS-Wiki/
  hot.md          ← Current session context (read every session start)
  index.md        ← Full wiki index
  log.md          ← Session history
  brain/          ← Long-term strategy docs
  career/         ← Career positioning docs
  decisions/      ← Decision log
  fleet/          ← Skills fleet documentation
  learning/       ← Learning notes
  memory/         ← Project memory files
  meta/           ← System documentation
  projects/       ← Active project pages
  sources/        ← Reference materials
```

---

### Step 5 — Configure MCP Connectors

MCP (Model Context Protocol) connects Claude to external tools.

**Minimum useful connectors:**
```json
{
  "notion": "For project dashboard and knowledge base",
  "google-drive": "For document storage and retrieval",
  "linear": "For task and project tracking"
}
```

**Full connector list:**
See [04_MCP_Integration.md](04_MCP_Integration.md) for complete setup.

**Quick Notion setup:**
1. Claude Desktop → Settings → Integrations → Add MCP
2. Search: Notion
3. Click Connect → Authorize with Notion account
4. Grant access to your workspace

---

### Step 6 — Install Python Validation (Optional but Recommended)

```bash
cd zeref-agent-os
pip install -r requirements.txt  # if exists, else:
pip install pyyaml jsonschema
python zeref-validate.py
```

Expected output:
```
✅ Checking skill files...
✅ 112/112 skills valid
✅ Registry sync confirmed
✅ Manifest integrity OK
Zeref Agent OS v2.0.0 — All systems nominal
```

---

### Step 7 — First Activation

```
/zeref-activate
```

Zeref reads `hot.md`, loads context, and reports current state.

**First-run output looks like:**
```
Zeref OS v2.0.0 active.
Memory: wiki/hot.md loaded — no prior context.
Skills: 112 available.
Active project: none.
Pending decisions: none.
Ready.
```

---

### Step 8 — Verify with a Test Task

Run a simple task to confirm routing works:

```
Write a 3-bullet product strategy for a mobile app that helps people track sleep.
```

Zeref should route to: `Lead: zeref-biz-business-strategist | Support: zeref-ux-product-designer`

If you see explicit skill routing in the response header, installation is successful.

---

## Tier 2: Minimal Setup

For users who want skills without memory or MCP.

### Step 1 — Install Plugin
```bash
git clone https://github.com/kanadhiayash/zeref-agent-os.git
cd zeref-agent-os
claude plugin install .
```

### Step 2 — Load Kernel
Copy `ZEREFOS.md` into Claude Project Instructions.

### Step 3 — Activate
```
/zeref-activate
```

**What works:** All 112 skills, task routing, quality gates, Caveman mode  
**What doesn't:** Memory persistence across sessions, MCP connectors, Obsidian vault

**When to upgrade to Tier 1:**
- When you find yourself re-explaining context every session
- When you need to connect to Notion, Linear, or Drive
- When you want session handoffs to work

---

## Tier 3: Custom Build

For developers building their own skill fleet.

### Fork the Repo
```bash
git clone https://github.com/kanadhiayash/zeref-agent-os.git my-custom-os
cd my-custom-os
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Understand the Architecture
Before modifying:
1. Read [02_Prompt_Architecture.md](02_Prompt_Architecture.md) — instruction hierarchy
2. Read [03_Skills_Fleet_Guide.md](03_Skills_Fleet_Guide.md) — skill file format
3. Run `python zeref-validate.py` — confirms your changes are valid

### Skill File Format
```yaml
---
name: my-custom-skill
layer: ux  # ux | dev | biz | mkt | cnt | qa | final | system | hq
role: My Custom Role
description: One-line description for routing decisions
triggers:
  - "phrase that activates this skill"
  - "another trigger phrase"
---

# My Custom Role

## Core Responsibilities
...

## Output Format
...

## Quality Gates
...
```

### Customize the Kernel
Edit `ZEREFOS.md`:
- Change `User:` block to your identity
- Update `Core Positioning` to your professional context
- Modify transformation chain if needed

### Validate
```bash
python zeref-validate.py --full
```

All 4 checks must pass before using custom build.

---

## Updating Zeref OS

### Pull latest version
```bash
cd zeref-agent-os
git fetch origin
git pull origin main
```

### Check for breaking changes
```bash
python zeref-validate.py
git log --oneline origin/main..HEAD
```

### Re-install plugin after updates
```bash
claude plugin install . --force
```

---

## Uninstalling

```bash
# Remove plugin
claude plugin uninstall zeref-agent-os

# Remove Obsidian vault (optional — keep if you want to preserve memory)
# rm -rf ~/Documents/ZerefOS-Wiki

# Remove repo
rm -rf zeref-agent-os
```

---

## Next Steps

- [02_Prompt_Architecture.md](02_Prompt_Architecture.md) — Understand how instructions layer
- [03_Skills_Fleet_Guide.md](03_Skills_Fleet_Guide.md) — Learn what each skill does
- [06_Workflow_Examples.md](06_Workflow_Examples.md) — See real use cases
