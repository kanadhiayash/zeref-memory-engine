# Zeref Memory Engine — Wiki

<p align="center"><img src="https://raw.githubusercontent.com/kanadhiayash/zeref-os/main/assets/zeref-os-hero.png" alt="Zeref Memory Engine" width="640"></p>

> Imagine you are an **architect** working on a major building. Every morning a different contractor shows up. Before they can lay a single brick, you have to re-explain the blueprint, the constraints, the decisions you and the prior contractor made, and what's already been built. Every conversation starts from zero.
>
> That is what working with AI assistants is like today. Each new session — Claude, Codex, Gemini, Cursor, Aider — starts blind. Context evaporates the moment the window closes.
>
> **Zeref is the local-first memory hardening layer for AI agents.** A per-project Markdown wiki plus structured local state that AI sessions read first, write to safely, and hand off cleanly. Your project memory travels with the project — not the tool.

**Current version**: v1.0.0 · [`CHANGELOG`](https://github.com/kanadhiayash/zeref-os/blob/main/CHANGELOG.md) · [`BENCHMARK_REPORT`](https://github.com/kanadhiayash/zeref-os/blob/main/docs/BENCHMARK_REPORT.md) · [`TRUST_AUDIT`](https://github.com/kanadhiayash/zeref-os/blob/main/docs/TRUST_AUDIT.md)

## Disclaimers (read first)

- **Zeref is not an operating system.** It is a persistent memory and
  context layer. The legacy product name was "Zeref OS"; the repo
  identifier (`zeref-os`) is retained only for install-URL
  backward-compatibility. The product name is **Zeref Memory Engine**.
- **v1.0.0 is the current public release** under this name. Architecture
  carries forward from pre-public v2.6.x. Pre-v1 history is archived to
  [`kanadhiayash/zeref-os-archive`](https://github.com/kanadhiayash/zeref-os-archive).
- **MIT licensed, no warranty.** Use at your own risk. The privacy
  scrubber is defense-in-depth, not a substitute for not pasting
  production credentials into prompts.
- Known gaps live in [[Risk-Log]] and [[Trust-Audit]]. Nothing is hidden.

## Quick links

- 📦 **[[Installation]]** — per-harness setup, verification, uninstall
- 🏗️ **[[Architecture]]** — 6 agents · 14 skills · 8 commands · 9 team packs · 4 Auto-Activation Gates · Model-Tier Routing
- 🧠 **[[Memory-Model]]** — flat layout, boundary-first reads, contradiction handling, PATTERNS.jsonl event schema
- 🔒 **[[Privacy-Model]]** — PRIVACY / REDACT / SHARING_POLICY, modes, connectors, R6 Zero Context Loss
- 👥 **[[Team-Packs]]** — solo / build / research / red / audit / ship / small / medium / enterprise
- 🔍 **[[Pattern-Detection]]** — Two-Strikes Rule, pattern-observer, skill drafting
- 📊 **[[Benchmarks]]** — local rubric, results, and fixture adapter status
- 🛡️ **[[Trust-Audit]]** — independent re-score, deductions, follow-ups
- ⚠ **[[Risk-Log]]** — accepted risks, mitigations, open items
- 🧩 **[[Stack]]** — the projects Zeref routes alongside (credits)
- ❓ **[[FAQ]]** — common questions
- 📖 **[[Glossary]]** — boundary file, evidence grade, Two-Strikes Rule, R6, 4-gate chain, model-resolver
- 🌱 **[[Inspirations]]** — engineering lineage and influences

## What Zeref ships

Per-project flat `memory/` wiki in plain Markdown · append-only
`PATTERNS.jsonl` event log with schema validator · point-in-time
snapshots · contradiction safety with human arbitration · three privacy
modes (`exact` / `abstract` / `local-only`) · nine on-demand team packs
(legacy six + small/medium/enterprise size envelopes) · cross-harness
handoff format with caveman-grammar compression · a **4-gate
auto-activation chain** that classifies every major task on cost weight,
picks the smallest useful skill stack, probes extended-tool
reachability, and restructures unstructured prompts before any token
spend · **pytest suite**, **9 provider-shaped credential
patterns** in the privacy scrubber, **CI actions pinned to commit
SHAs**, and a **local benchmark verdict** (portability 10 ·
adaptivity 9 · scalability 10 · retrieval 10 · trust 9.7).

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
| See the published benchmark verdict | [[Benchmarks]] |
| Inspect the independent trust audit | [[Trust-Audit]] |
| Understand who we built on | [[Inspirations]] · [[Stack]] |
| Run the validator yourself | [`scripts/zeref-validate.py`](https://github.com/kanadhiayash/zeref-os/blob/main/scripts/zeref-validate.py) |

## Help test it, fork it, scale it

Zeref ships at v1.0.0 with an explicit, conservative trust posture. It
is good enough for daily use. It is not finished. If you can verify a
harness, fork it for your team's constraints, or scale it in a direction
the maintainer hasn't (shared multi-device memory, GUI, harness adapter
for a tool that doesn't exist yet, higher coverage on the privacy
scrubber), open an issue with a short proposal. See the README's
[Help test it, fork it, scale it](https://github.com/kanadhiayash/zeref-os#help-test-it-fork-it-scale-it-in-a-direction-i-havent)
section for direction prompts.

---

[`README`](https://github.com/kanadhiayash/zeref-os) · [`AGENTS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/AGENTS.md) · [`CHANGELOG`](https://github.com/kanadhiayash/zeref-os/blob/main/CHANGELOG.md) · [`SECURITY.md`](https://github.com/kanadhiayash/zeref-os/blob/main/SECURITY.md) · [`CONTRIBUTING.md`](https://github.com/kanadhiayash/zeref-os/blob/main/CONTRIBUTING.md) · [`GITHUB_OS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/GITHUB_OS.md) · [`_shared/model-resolver.md`](https://github.com/kanadhiayash/zeref-os/blob/main/_shared/model-resolver.md)
