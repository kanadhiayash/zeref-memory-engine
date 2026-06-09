# Zeref OS Wiki

<p align="center"><img src="https://raw.githubusercontent.com/kanadhiayash/zeref-os/main/assets/zeref-os-hero.png" alt="Zeref OS" width="640"></p>

> **Local-first context and memory engine for AI-assisted work.**
> Harness-agnostic · Model-agnostic · Privacy-first · Free
>
> Named after **Zeref Dragneel** from *Fairy Tail* — the immortal scholar who carried ancient knowledge across forms and ages. Zeref OS is built in that lineage: long-horizon memory, faithful to the user's accumulated decisions, portable across every AI harness.

**Current version**: v2.6.1 (June 8, 2026) — [`CHANGELOG`](https://github.com/kanadhiayash/zeref-os/blob/main/CHANGELOG.md) · [`docs/RELEASE_LOG.md`](https://github.com/kanadhiayash/zeref-os/blob/main/docs/RELEASE_LOG.md) · [Notion Command Center](https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3)

**Rubric**: 9.88/10 (8 dims, every score cites artifact) — [`tests/zeref-rubric-v2.6.md`](https://github.com/kanadhiayash/zeref-os/blob/main/tests/zeref-rubric-v2.6.md)

## Quick links

- 📦 **[Installation](Installation)** — per-harness setup, verification, uninstall
- 🏗️ **[Architecture](Architecture)** — **6 agents · 14 skills · 8 commands · 6 team packs · 4 Auto-Activation Gates · Model-Tier Routing**
- 🧠 **[Memory Model](Memory-Model)** — flat layout, boundary-first reads, contradiction handling, PATTERNS.jsonl event schema (L5+L15)
- 🔒 **[Privacy Model](Privacy-Model)** — PRIVACY/REDACT/SHARING_POLICY, modes, connectors, R6 Zero Context Loss
- 👥 **[Team Packs](Team-Packs)** — solo / build / research / red / audit / ship
- 🔍 **[Pattern Detection](Pattern-Detection)** — Two-Strikes Rule, pattern-observer, skill drafting
- 📜 **[Decision Log](Decision-Log)** — D1–D11 + v2.6 + v2.6.1 arbitrations
- 🤖 **[Model Debates](Model-Debates)** — what Claude / GPT / Gemini / open-source each need + v2.6 model-resolver
- 🕰️ **[Versioning History](Versioning-History)** — Skills Fleet → Agent OS → Zeref OS → v2.5 audit → v2.6 4-gate → v2.6.1 hardening
- ❓ **[FAQ](FAQ)** — common questions
- 📖 **[Glossary](Glossary)** — boundary file, evidence grade, Two-Strikes, R6, 4-gate chain, model-resolver, etc.
- 🌱 **[Inspirations](Inspirations)** — engineering lineage and influences

## What Zeref OS is (one paragraph, v2.6.1)

Per-project flat `memory/` wiki in plain markdown, append-only `PATTERNS.jsonl` event log with schema validator, point-in-time snapshots, contradiction safety with human arbitration, three privacy modes (`exact` / `abstract` / `local-only`), six on-demand team packs, cross-harness handoff format with caveman-grammar compression, and a **4-gate auto-activation chain** (`budget-governor` → `skill-router` → `fleet-activator` → `prompt-context-engine`) that classifies every major task on cost weight, picks the smallest useful skill stack, probes extended-tool reachability, and restructures unstructured prompts before any token spend. AI sessions become cumulative across every harness you use.

## v2.6 four-gate chain (every major task)

```
[budget-governor]      classify weight (CRITICAL/HIGH/MEDIUM/LOW) + match model tier
       ↓
[skill-router]         pick smallest stack (1 lead + 2-3 support + 1 QA, max 5 skills)
       ↓
[fleet-activator]      live-probe ECC / claude-obsidian / Graphify / browser-harness / notebooklm / gstack
       ↓
[prompt-context-engine] classify STRUCTURED / SEMI-STRUCTURED / UNSTRUCTURED; restructure if needed; R6 zero context loss
       ↓
                       execute (declared stack, declared brief, declared tier)
       ↓
[caveman-handoff]      compress cross-model handoff (40-60% reduction; NFKC + R6 diff)
```

Each gate declares its result inline. User can override before token spend. Per AGENTS.md `## Auto-Activation Gates`.

## Where to start

| If you want to... | Read |
|---|---|
| Install in 5 minutes | [Installation](Installation) |
| Understand the system | [Architecture](Architecture) → [Memory Model](Memory-Model) |
| Lock down privacy first | [Privacy Model](Privacy-Model) |
| See how teams work | [Team Packs](Team-Packs) |
| Trace design decisions | [Decision Log](Decision-Log) |
| Trace the iteration history | [Versioning History](Versioning-History) |
| Understand who we built on | [Inspirations](Inspirations) |
| Run the audit yourself | [`scripts/zeref-validate.py`](https://github.com/kanadhiayash/zeref-os/blob/main/scripts/zeref-validate.py) — Skills 14/14, PATTERNS lint 0 |

---

[`README`](https://github.com/kanadhiayash/zeref-os) · [`AGENTS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/AGENTS.md) · [`CHANGELOG`](https://github.com/kanadhiayash/zeref-os/blob/main/CHANGELOG.md) · [`GITHUB_OS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/GITHUB_OS.md) · [`docs/adr/`](https://github.com/kanadhiayash/zeref-os/tree/main/docs/adr) · [`_shared/model-resolver.md`](https://github.com/kanadhiayash/zeref-os/blob/main/_shared/model-resolver.md)
