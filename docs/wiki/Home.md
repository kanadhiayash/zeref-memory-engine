# Zeref OS Wiki

<p align="center"><img src="https://raw.githubusercontent.com/kanadhiayash/zeref-os/main/assets/zeref-os-hero.png" alt="Zeref OS" width="640"></p>

> Imagine you are an **architect** working on a major building. Every morning a different contractor shows up. Before they can lay a single brick, you have to re-explain the blueprint, the constraints, the decisions you and the prior contractor made, and what's already been built. Every conversation starts from zero.
>
> That is what working with AI assistants is like today. Each new session — Claude, Codex, Gemini, Cursor, Aider — starts blind. Context evaporates the moment the window closes.
>
> **Zeref OS is the persistent memory layer that fixes this.** A per-project markdown wiki that AI sessions read first, write to safely, and hand off cleanly. Your project memory travels with the project — not the tool.

**Current version**: v1.0.0 · [`CHANGELOG`](https://github.com/kanadhiayash/zeref-os/blob/main/CHANGELOG.md) · [`BENCHMARK_REPORT`](https://github.com/kanadhiayash/zeref-os/blob/main/docs/BENCHMARK_REPORT.md) · [Notion Command Center](https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3)

_Placeholder: `assets/poc-stateless-vs-zeref.png` — add screenshot of two sessions, before / after Zeref OS._

## Quick links

- 📦 **[[Installation]]** — per-harness setup, verification, uninstall
- 🏗️ **[[Architecture]]** — 6 agents · 14 skills · 8 commands · 6 team packs · 4 Auto-Activation Gates · Model-Tier Routing
- 🧠 **[[Memory-Model]]** — flat layout, boundary-first reads, contradiction handling, PATTERNS.jsonl event schema
- 🔒 **[[Privacy-Model]]** — PRIVACY / REDACT / SHARING_POLICY, modes, connectors, R6 Zero Context Loss
- 👥 **[[Team-Packs]]** — solo / build / research / red / audit / ship
- 🔍 **[[Pattern-Detection]]** — Two-Strikes Rule, pattern-observer, skill drafting
- ❓ **[[FAQ]]** — common questions
- 📖 **[[Glossary]]** — boundary file, evidence grade, Two-Strikes Rule, R6, 4-gate chain, model-resolver
- 🌱 **[[Inspirations]]** — engineering lineage and influences

## What v1.0.0 ships

Per-project flat `memory/` wiki in plain markdown · append-only `PATTERNS.jsonl` event log with schema validator · point-in-time snapshots · contradiction safety with human arbitration · three privacy modes (`exact` / `abstract` / `local-only`) · six on-demand team packs · cross-harness handoff format with caveman-grammar compression · and a **4-gate auto-activation chain** that classifies every major task on cost weight, picks the smallest useful skill stack, probes extended-tool reachability, and restructures unstructured prompts before any token spend.

## The 4-gate chain (every major task)

```
[budget-governor]       classify weight (CRITICAL/HIGH/MEDIUM/LOW) + match model tier
       ↓
[skill-router]          pick smallest stack (1 lead + 2-3 support + 1 QA, max 5 skills)
       ↓
[fleet-activator]       live-probe ECC / claude-obsidian / Graphify / browser-harness / notebooklm / gstack
       ↓
[prompt-context-engine] classify STRUCTURED / SEMI-STRUCTURED / UNSTRUCTURED; restructure if needed; R6 zero context loss
       ↓
                        execute (declared stack, declared brief, declared tier)
       ↓
[caveman-handoff]       compress cross-model handoff (40-60% reduction; NFKC + R6 diff)
```

Each gate declares its result inline. User can override before token spend. Per AGENTS.md `## Auto-Activation Gates`.

## Where to start

| If you want to… | Read |
|---|---|
| Install in 5 minutes | [[Installation]] |
| Understand the system | [[Architecture]] → [[Memory-Model]] |
| Lock down privacy first | [[Privacy-Model]] |
| See how teams work | [[Team-Packs]] |
| Understand who we built on | [[Inspirations]] |
| Run the validator yourself | [`scripts/zeref-validate.py`](https://github.com/kanadhiayash/zeref-os/blob/main/scripts/zeref-validate.py) |

---

[`README`](https://github.com/kanadhiayash/zeref-os) · [`AGENTS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/AGENTS.md) · [`CHANGELOG`](https://github.com/kanadhiayash/zeref-os/blob/main/CHANGELOG.md) · [`GITHUB_OS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/GITHUB_OS.md) · [`_shared/model-resolver.md`](https://github.com/kanadhiayash/zeref-os/blob/main/_shared/model-resolver.md)
