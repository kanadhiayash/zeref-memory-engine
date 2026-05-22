# Install Zeref OS

Two ways to install. Pick one.

> **Warning:** Do NOT use "Add marketplace" in Claude Code — that is for multi-plugin registries, not individual plugins. It will fail with "no manifest found". Use the paths below.

---

## Path A — GitHub Download ZIP (Recommended)

**Requirements:** Claude Code CLI or Desktop App (v1.x+)

1. Go to [github.com/kanadhiayash/zeref-os](https://github.com/kanadhiayash/zeref-os)
2. Click **Code → Download ZIP**
3. In Claude Code: **Settings → Plugins → Local uploads → +**
4. Select the downloaded `zeref-os-main.zip`
5. Click **Install**

All 109 active skills, 11 commands, and 8 agents install automatically.

> **Always use GitHub Download ZIP — do not zip the local repo folder.** Local zips include runtime database files (`ruvector.db`, `agentdb.rvf`) that trigger Claude Code's compression security scanner. The GitHub ZIP excludes them automatically.

---

## Path B — Git Clone

```bash
git clone https://github.com/kanadhiayash/zeref-os.git
cd zeref-os
claude plugin install .
```

---

## Step 2 — Activate the OS Kernel

After installing the plugin, load the OS kernel:

1. Open Claude → **Project** (or create one for Zeref)
2. Go to **Project Instructions**
3. Paste the full contents of `ZEREFOS.md`

This loads the routing kernel, identity rules, Karpathy principles, and Caveman triggers.

**Without this step, skills install but routing and discipline rules don't apply.**

---

## Step 3 — Start a Session

Run the activation command:

```
/zeref-activate
```

Zeref reads `wiki/hot.md`, reports current context, and asks what to work on.

---

## Validate the Install

```bash
python3 scripts/zeref-validate.py             # validates full fleet
python3 scripts/zeref-validate.py --verbose   # shows PASS for each skill
```

Expected output: `🟢 VALIDATION PASSED — 109 skills, 8 agents, 11 commands`

---

## Troubleshooting

**"This repository isn't a marketplace" error:**
- You used "Add marketplace" — that's the wrong dialog. Use **Local uploads** (Path A above).

**Skills not showing up after install:**
- Verify `skills/` folder has 109 subdirectories
- Each subdirectory must contain `SKILL.md`
- Run `python3 scripts/zeref-validate.py` to check for file issues

**Compression warning on ZIP upload:**
- You zipped the local repo folder instead of using GitHub Download ZIP
- Delete the local zip, download fresh from GitHub (`Code → Download ZIP`), re-upload

**ZEREFOS not routing correctly:**
- Confirm `ZEREFOS.md` content is in Claude Project Instructions (not just uploaded as a file)
- The kernel must be in the system prompt layer, not the conversation

**Plugin.json schema errors:**
- Check `.claude-plugin/plugin.json` matches your installed Claude Code version
- Run `/zeref-audit` to diagnose

---

## Directory Structure After Install

```
zeref-os/
├── .claude-plugin/plugin.json   ← Claude Code plugin manifest
├── ZEREF.md                     ← OS identity and routing kernel
├── ZEREFOS.md                   ← Paste into Project Instructions
├── AGENTS.md                    ← Agent harness definitions (Codex compatible)
├── GEMINI.md                    ← Gemini agent harness definitions
├── CLAUDE.md                    ← Session start protocol
├── INSTALL.md                   ← This file
├── README.md                    ← Full documentation
├── CHANGELOG.md                 ← Version history
├── LICENSE                      ← MIT
├── skills/                      ← 109 skills across 9 guilds
├── commands/                    ← 11 slash commands
├── agents/                      ← 8 privilege-scoped agents
├── references/                  ← Shared rules (QA gate, safety, anti-hallucination)
├── output-styles/               ← Output style definitions
├── registry/                    ← Machine-readable skill index
├── scripts/                     ← Validation and upgrade tools
│   └── zeref-validate.py        ← Run to validate fleet
├── experience.jsonl             ← Self-improvement log
└── wiki/                        ← Session memory (hot.md, log.md, index.md)
    ├── hot.md                   ← Last 3 sessions context
    ├── log.md                   ← Append-only operation history
    ├── index.md                 ← Domain knowledge map
    ├── concepts/
    ├── projects/
    └── sources/
```
