# Install Zeref OS

Three ways to install. Pick one.

---

## Option 1 — GitHub (Recommended)

**Requirement:** Claude Code CLI or Desktop App

```
Claude Code → Plugins → Add Plugin
→ Enter: https://github.com/kanadhiayash/zeref-agent-os
→ Confirm install
```

All 104 active skills, 9 commands, and 2 agents install automatically.

---

## Option 2 — Local ZIP

1. Download ZIP from GitHub: `Code → Download ZIP`
2. Unzip to any directory (e.g. `~/Documents/zeref-agent-os/`)
3. In Claude Code:
```
Claude Code → Plugins → Add Plugin (Local)
→ Browse to unzipped folder
→ Select zeref-agent-os/
→ Confirm install
```

---

## Option 3 — Git Clone + CLI

```bash
git clone https://github.com/kanadhiayash/zeref-agent-os.git
cd zeref-agent-os
claude plugin install .
```

---

## Step 2 — Activate the OS Kernel

After installing the plugin, activate ZEREFOS:

1. Open Claude → **Project** (or create one for Zeref)
2. Go to **Project Instructions**
3. Paste the full contents of `ZEREFOS.md`

This loads the OS kernel — identity, routing rules, Karpathy principles, Caveman triggers.

**Without this step, skills install but routing and discipline rules don't apply.**

---

## Step 3 — Start a Session

Run the activation command:

```
/zeref-activate
```

Zeref reads `wiki/hot.md`, reports current context, and asks what to work on.

---

## Step 4 — Use the Obsidian Vault (Optional but Recommended)

The repo ships with a pre-configured Obsidian vault at `wiki/`:

1. Download and install [Obsidian](https://obsidian.md) (free)
2. Open Obsidian → **Open folder as vault**
3. Select the `zeref-agent-os/` folder (the whole repo root)
4. Obsidian reads `.obsidian/` config automatically — vault opens with theme and settings applied
5. Start at `wiki/brain/00_master.md`

---

## Validate the Install

```bash
python3 zeref-validate.py             # validates all 104 skills
python3 zeref-validate.py --verbose   # shows PASS for each skill
```

Expected output: `104 skills validated. 0 failures.`

---

## Troubleshooting

**Skills not showing up after install:**
- Verify `skills/` folder has 104 subdirectories
- Each subdirectory must contain `SKILL.md`
- Run `zeref-validate.py` to check for file issues

**ZEREFOS not routing correctly:**
- Confirm ZEREFOS.md content is in Claude Project Instructions (not just uploaded as a file)
- The kernel must be in the system prompt layer, not the conversation

**Obsidian vault not loading:**
- Make sure you opened the repo root folder, not the `wiki/` subfolder
- `.obsidian/` must be at the root of the vault folder

**Plugin.json schema errors:**
- Check `.claude-plugin/plugin.json` matches the installed Claude Code version
- Run `/zeref-audit` to diagnose

---

## Directory Structure After Install

```
zeref-agent-os/
├── .claude-plugin/plugin.json   ← Claude Code plugin manifest
├── ZEREFOS.md                   ← Paste into Project Instructions
├── CLAUDE.md                    ← Vault structure reference
├── INSTALL.md                   ← This file
├── README.md                    ← Full documentation
├── zeref-validate.py            ← Skill validator
├── zeref-settings-recommended.json
├── skills/                      ← 104 skills (skills/<id>/SKILL.md)
├── commands/                    ← 9 slash commands
├── agents/                      ← 2 subagents
├── references/                  ← Shared rules (anti-hallucination, token discipline)
├── output-styles/               ← zeref-executive output style
├── themes/                      ← zeref-dark Obsidian theme
├── registry/                    ← Machine-readable skill index (104 skills)
├── wiki/                        ← Obsidian brain (ships with vault)
│   ├── brain/                   ← Master knowledge hub (start here)
│   ├── fleet/                   ← 9 domain pages for all 104 skills
│   ├── projects/                ← Active project pages
│   ├── concepts/                ← Architecture and concept docs
│   └── ...
└── .obsidian/                   ← Vault config (opens instantly in Obsidian)
```
