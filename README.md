# Zeref OS

<p align="center"><img src="assets/zeref-os-hero.png" alt="Zeref OS — pixel-art mage with floating tomes" width="720"></p>

<p align="center">
  <strong>Local-first context and memory engine for AI-assisted work.</strong><br>
  Harness-agnostic · Model-agnostic · Privacy-first · Developer-first · Free to install
</p>

<p align="center">
  <a href="https://github.com/kanadhiayash/zeref-os/releases/tag/v2.6.1"><img src="https://img.shields.io/badge/version-2.6.1-blueviolet" alt="v2.6.1"></a>
  <a href="tests/zeref-rubric-v2.6.md"><img src="https://img.shields.io/badge/rubric-9.88%2F10-success" alt="rubric 9.88/10"></a>
  <a href="tests/security-audit-v2.6-C.md"><img src="https://img.shields.io/badge/CRITICAL-0%20open-success" alt="0 CRITICAL"></a>
  <a href="tests/scores-v2.6-B.csv"><img src="https://img.shields.io/badge/sandbox-114%2F150%20pass-success" alt="sandbox pass"></a>
  <a href="AGENTS.md#auto-activation-gates-v26"><img src="https://img.shields.io/badge/gates-3%20active-blue" alt="3 gates"></a>
  <a href="https://github.com/kanadhiayash/zeref-os/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/source--of--truth-v1.0.0-blueviolet" alt="v1.0.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT"></a>
  <a href="https://agents.md"><img src="https://img.shields.io/badge/AGENTS.md-canonical-blue" alt="AGENTS.md"></a>
  <a href="https://github.com/kanadhiayash/zeref-os/actions/workflows/zeref-validate.yml"><img src="https://github.com/kanadhiayash/zeref-os/actions/workflows/zeref-validate.yml/badge.svg" alt="CI"></a>
</p>

> **Zeref OS Command Center (Notion)**: <https://copper-tv-288.notion.site/Zeref-Agent-OS-Command-Center-358d695d836a81af9f6adf30770217c3>
> **Repo doctrine (per-repo)**: [`GITHUB_OS.md`](GITHUB_OS.md) — branch naming, audit cycle, R6 gate, model-resolver pinning
> **Decision records**: [`docs/adr/`](docs/adr/) (FAANG naming `zeref_<subject>_adr_<state>_yk_<date>_v<major.minor>.md`)
> **Release log**: [`docs/RELEASE_LOG.md`](docs/RELEASE_LOG.md) — controlled baselines per FAANG §3.4

---

## What Zeref OS is

The persistent memory layer your AI tools should have had from day one.

A per-project canonical wiki in plain markdown, an append-only pattern log, point-in-time snapshots, contradiction safety, three privacy modes, on-demand team packs, and a cross-harness handoff format. AI sessions become cumulative instead of stateless — across **every** harness you use.

> **Read once. Remember forever. Travel with you, not the tool.**

---

## Inspiration — Where the name comes from

Zeref OS is named after **Zeref Dragneel** from *Fairy Tail* — the immortal scholar whose ancient knowledge transcended form, time, and faction. He carried centuries of context with him; he never started from zero.

That's the design north star. AI sessions today start from zero, every time. You re-explain your project every conversation. You lose decisions to context window resets. You can't switch from Claude to Codex to Gemini to Cursor without abandoning your project memory.

Zeref OS is built in that lineage: **long-horizon memory, faithful to the user's accumulated decisions, portable across every AI harness**.

---

## The Journey — Iterations that led here

This is not version 1.0 in the literal sense — it's the line drawn under a long iteration. Every prior attempt taught the design what it should *not* be.

| Era | Form | What we learned | Status |
|---|---|---|---|
| **v1.x** (2025) | Zeref Skills Fleet — 109 specialist skills | Too broad. Wrong shape. Skill bloat = scope creep. | archived |
| **v2.0–v2.1** (2025) | Zeref Agent OS | Closer, but Claude-locked. Harness coupling broke portability. | archived |
| **v3.0** (early 2026) | Zeref OS w/ CEO persona + LLM council | Theatrical. Single-user. Off-mission. CEO framing was wrong for a context engine. | archived |
| **v4.0** (May 2026) | Philosophical reset → pure context + memory engine | Removed: 109 skills, 5 agents, CEO/fleet/council framing. The shape clicked. | archived |
| **v4.1** (May 2026) | Full contradiction-resolution + parent-sync | Human arbitration on conflicts; child→parent rollup with provenance. | archived |
| **v4.2** (May 2026) | Pattern detection + skill drafting | `pattern-observer` + `pattern-to-skill`. Review-first extension. | archived |
| **v4.3** (May 2026) | v4.x canon alignment + team packs + harness translation map | Flat memory layout, Free/Standard/God Mode tiers, Two-Strikes Rule. | merged → v1.0.0 |
| **v1.0.0** (May 31, 2026) | **Zeref OS** — canonical release. Rebrand + version reset. | shipped |
| **v2.5.0** (Jun 5, 2026) | **Deep Audit Campaign** — runtime + code-backed privacy + 85-claim audit + 8 attacks + L1-L11 workarounds. Rubric 8.00/10. | shipped |
| **v2.6.0** (Jun 8, 2026) | **Auto-Gated Execution** — 4-gate chain (budget → router → fleet → prompt → handoff). +4 skills. +2 Core Principles. +R6 Zero Context Loss. | shipped |
| **v2.6.1** (Jun 8, 2026) | **Audit + Hardening** — 7-phase audit on v2.6.0. 15 L-items closed all CRITICAL+HIGH+MEDIUM findings. Rubric 9.88/10. | **You are here.** |

Years of local iteration converge here. Full pre-rebrand history preserved in [`CHANGELOG-LEGACY.md`](CHANGELOG-LEGACY.md); post-rebrand release notes in [`CHANGELOG.md`](CHANGELOG.md); per-release rows in [`docs/RELEASE_LOG.md`](docs/RELEASE_LOG.md).

---

## Architecture Evolution (v1 → v2.6)

**The shape Zeref OS settled into** — each version's contribution to the final design, sourced from `CHANGELOG.md` + `CHANGELOG-LEGACY.md`.

| Era | Mental model | What it removed | What it added |
|---|---|---|---|
| **v1.x → v2.x** (legacy) | "Specialist skill fleet" | — | 109+ Claude-locked skills |
| **v3.0** (legacy) | "CEO + LLM council" | — | Always-on multi-agent theater (rejected v4.0) |
| **v4.0** (May 2026) | **Local-first context + memory engine** | 109 skills, 5 agents, CEO/fleet/council framing | 10 disciplined skills + AGENTS.md canon + flat memory + 3 privacy modes |
| **v4.1–v4.3** (May 2026) | Refinement | — | Contradiction resolution + parent sync + pattern detection + team packs + harness translation map + Two-Strikes Rule |
| **v1.0.0** (May 31, 2026) | Canonical release + rebrand | — | Version reset; consolidated v4.x learnings into single canonical line |
| **v2.5.0** (Jun 5, 2026) | **Code-backed runtime** (not spec-only) | spec-only privacy enforcement | `zeref/{privacy,lock,cli,db,demo,dashboard}.py` + 85-claim audit + L1-L11 workarounds + 300-row sandbox |
| **v2.6.0** (Jun 8, 2026) | **Reactive → Proactive auto-gated execution** | implicit cost-discipline + manual skill selection + verbatim prompt passthrough | 4-gate chain + 4 skills (skill-router, fleet-activator, prompt-context-engine, caveman-handoff) + Core Principles 13-14 + Model-Tier Routing + R6 |
| **v2.6.1** (Jun 8, 2026) | **Prose-only → code-enforced gates** | hardcoded validator count + bare model names + R6 coverage gaps + 2 CRITICAL/2 HIGH/2 MEDIUM security findings | dynamic registry-driven validator + event-schema lint + model-resolver (full Anthropic ids) + L9 marker-file probe + L10 injection filter + L11 cool-down + L12 NFKC homoglyph guard + L13 dual-key override |

See [`docs/adr/`](docs/adr/) for the two architectural decision records covering v2.6.0 + v2.6.1 in full.

---

## Tests & Validation

Run locally before every push. CI mirrors these on PR + main.

| Check | Command | Threshold |
|---|---|---|
| **Structural validator** | `python3 scripts/zeref-validate.py` | Skills 14/14, all sub-checks pass, PATTERNS lint 0 findings |
| **PATTERNS.jsonl event schema** | `python3 scripts/zeref-validate.py` (built-in) | 11 event types allowlisted; weight/tier enum enforced; stack-cap ≤5 |
| **Claim audit** | inspect `tests/claims-v2.6.csv` (52 rows) + `tests/claims-audit-v2.6.md` | ≥60% VERIFIED |
| **Sandbox stress** | inspect `tests/scores-v2.6-B.csv` (150 rows) + `tests/phase-b-v2.6-summary.md` | ≥70% pass; 0 CRITICAL adversarial failure unresolved |
| **Security audit** | inspect `tests/security-audit-v2.6-C.md` (8 attacks CVSS-scored) | 0 CRITICAL open at ship |
| **Rubric** | inspect `tests/zeref-rubric-v2.6.md` | 8 dims, every score cites artifact |
| **Live regression** | `python3 tests/runner.py --mode structural` | 20/20 |
| **Zeref-scope sweep** (push gate) | `.github/workflows/ci.yml` runs allowlist regex against diff | no non-zeref paths in diff |

Historical baselines available: `tests/scores-vB.csv` (300 rows from v2.5 sandbox), `tests/scores-vD-live.csv` (20/20 live), `tests/zeref-rubric-v2.5.md` (v2.5 8.00 baseline).

---

## Doctrine + Repo Operations

This repo follows the operating doctrine documented at:
- **Global**: `~/Documents/Claude/00_COMMAND/GITHUB_OS.md` — Yash GitHub Operating System (branch model, PR review, security gates, configuration management)
- **Per-repo**: [`GITHUB_OS.md`](GITHUB_OS.md) — Zeref-specific overrides (audit cycle, R6 gate, model-resolver pinning, memory layer discipline, classification levels)
- **Knowledge-OS**: `~/Documents/Claude/00_COMMAND/yash_faang_architecture_brief.md` — FAANG-grade naming, classification, archive model

**Branch convention**: `<type>/zeref__<short-description>` (e.g. `feat/zeref__skill-router-v2`, `chore/zeref__history-reconstruction-v2.6.1`). Release-snapshot branches `release/v<major>.<minor>` per FAANG §3.4 controlled baselines.

**Commits**: Conventional Commits with scope `(zeref)`. See `git log --oneline` for examples.

**Decision records**: [`docs/adr/`](docs/adr/) — FAANG naming `zeref_<subject>_adr_<state>_yk_<date>_v<major.minor>.md`.

---

## What Zeref OS does

| Capability | Mechanism |
|---|---|
| **Remembers across sessions** | Per-project flat `memory/` (hot.md → index.md → DECISIONS/OPEN_QUESTIONS/RISKS/CONFLICTS/MEMORY) |
| **Works in any harness** | `AGENTS.md` is source of truth; per-harness stubs for Claude / Codex / Cursor / Gemini / Windsurf / Aider / Hermes / Amp / Zed / Perplexity |
| **Protects sensitive data** | Root `PRIVACY.md` (3 modes, default `abstract`) + `REDACT.md` (concrete classes) + `SHARING_POLICY.md` (connector allowlist, all OFF) |
| **Catches contradictions** | `memory-keeper` flags conflicts → `memory/CONFLICTS.md` → user arbitrates. Never silent. |
| **Detects repeated work** | `pattern-observer` scans `memory/patterns/PATTERNS.jsonl` (48–80h, 3× threshold) → drafts skill to `skills/drafts/` for review |
| **Activates teams on demand** | `/team [solo\|build\|research\|red\|audit\|ship]` — max 4 agents, outputs land in `team/` |
| **Pushes child→parent** | `/sync-parent` — staged, approved-per-push, provenance preserved |
| **Crosses harnesses losslessly** | `/stop --handoff` compiles `STATE.json` + `SUMMARY.md` + `NEXT.md` package |
| **Scales to model tier** | `budget-governor` auto-detects Free / Standard / God Mode; scales verbosity |
| **Self-extends safely** | Two-Strikes Rule: no rule on 1st error. `pattern-to-skill` drafts only — never auto-activates. |

---

## Architecture

```mermaid
flowchart TB
  subgraph Harnesses["Any harness"]
    CC[Claude Code]
    CX[Codex]
    CU[Cursor]
    GM[Gemini CLI / Antigravity]
    WS[Windsurf]
    AD[Aider]
    OT["Hermes · Amp · Zed · Perplexity"]
  end

  AG["AGENTS.md (source of truth)<br/>14 Core Principles · 4-Gate Auto-Activation"]
  Harnesses --> AG

  AG --> Gates
  Gates --> Agents
  Gates --> Skills
  AG --> Commands
  AG --> TeamPacks

  subgraph Gates["Auto-Activation Gates (v2.6, every major task)"]
    G1["Gate #1<br/>budget-governor<br/>weight + tier"]
    G2["Gate #2<br/>skill-router<br/>smallest stack"]
    GFA["fleet-activator<br/>tool reachability"]
    G3["Gate #3<br/>prompt-context-engine<br/>STRUCTURED brief + R6"]
    G1 --> G2 --> GFA --> G3
  end

  subgraph Agents["6 agents (background)"]
    MK[memory-keeper]
    PG[privacy-guardian]
    SC[sync-coordinator]
    EC[evidence-curator]
    PO[pattern-observer]
    HO[handoff-orchestrator]
  end

  subgraph Skills["14 skills (on-trigger)"]
    PS[project-setup]
    WM[wiki-maintenance]
    CR[contradiction-resolution]
    PA[privacy-abstraction]
    PSY[parent-sync]
    P2S[pattern-to-skill]
    MIE[memory-import-export]
    BG["budget-governor ★ Gate #1"]
    SR["skill-router ★ Gate #2"]
    FA["fleet-activator ★"]
    PCE["prompt-context-engine ★ Gate #3"]
    HC[handoff-compiler]
    CH["caveman-handoff ★"]
    EG[evidence-grader]
  end

  subgraph Commands["8 commands"]
    CMD1["/start"]
    CMD2["/done"]
    CMD3["/stop"]
    CMD4["/status"]
    CMD5["/team"]
    CMD6["/sync-parent"]
    CMD7["/reset-permissions"]
    CMD8["/review-skill"]
  end

  subgraph TeamPacks["6 team packs (on-demand, max 4 agents)"]
    TP1[solo]
    TP2[build]
    TP3[research]
    TP4["red (read-only)"]
    TP5[audit]
    TP6[ship]
  end

  MK <--> Memory[(memory/<br/>flat layout)]
  PG -. enforces .-> Memory
  PO -. logs .-> PATTERNS["memory/patterns/PATTERNS.jsonl<br/>event-schema validator (L5+L15)"]
  G1 -. event .-> PATTERNS
  G2 -. event .-> PATTERNS
  G3 -. event .-> PATTERNS
  CH -. R6 chain .-> HO

  classDef gate fill:#e1d5ff,stroke:#5b21b6,color:#000
  class G1,G2,G3,GFA,BG,SR,FA,PCE,CH gate
```

**★ = new in v2.6.** 4 gates fire sequentially before any execution-model call. Output declared inline; user can override before token spend. PATTERNS.jsonl event schema validated by `scripts/zeref-validate.py::lint_patterns_log()` (v2.6.1 L3+L5+L15).

---

## How it works — session lifecycle

```mermaid
sequenceDiagram
  participant User
  participant Harness
  participant Gates as Auto-Activation Gates
  participant ZerefOS as Zeref OS
  participant Memory as memory/
  participant Patterns as PATTERNS.jsonl

  User->>Harness: /start
  Harness->>ZerefOS: boot
  ZerefOS->>Memory: read hot.md (≤500 words)
  ZerefOS->>Memory: read index.md if needed
  ZerefOS->>Memory: load PRIVACY.md + REDACT.md
  ZerefOS-->>User: project, last session, active decisions, model tier

  loop major task
    User->>Harness: prompt
    Harness->>Gates: invoke (v2.6 4-gate chain)
    Gates->>Gates: Gate #1 budget-governor (weight + tier match)
    Gates->>Patterns: event budget-gate
    Gates->>Gates: Gate #2 skill-router (smallest stack)
    Gates->>Gates: fleet-activator (probe extended tools)
    Gates->>Patterns: event skill-route + tool-probe
    Gates->>Gates: Gate #3 prompt-context-engine (STRUCTURED brief + R6)
    Gates->>Patterns: event prompt-gate
    Gates-->>User: declared stack + brief (30s auto-approve if UNSTRUCTURED)
    Gates->>ZerefOS: execute per stack
    ZerefOS->>Memory: read (boundary-first)
    ZerefOS->>Memory: write via memory-keeper
    Note over Memory,Patterns: every write filtered by privacy-guardian
    ZerefOS->>Patterns: append wiki-write event
  end

  User->>Harness: /done
  ZerefOS->>Memory: consolidate · conflict scan
  ZerefOS->>Patterns: pattern-observer scans (48-80h)
  ZerefOS->>Memory: refresh hot.md + snapshot
  ZerefOS->>Patterns: lint_patterns_log (v2.6.1 L3 advisory)
  alt parent sync configured
    ZerefOS->>ZerefOS: stage + approve + push (R6 chain preserved)
  end

  User->>Harness: /stop --handoff
  ZerefOS->>ZerefOS: handoff-compiler builds STATE.json + SUMMARY.md + NEXT.md
  ZerefOS->>ZerefOS: caveman-handoff compresses (40-60% reduction; NFKC + R6 diff)
  ZerefOS-->>User: cross-model handoff package ready
```

---

## Memory layout (flat, per ZEREF_OS §12)

```
project-root/
├── AGENTS.md                    (canonical source of truth)
├── CLAUDE.md / GEMINI.md / ...  (harness stubs — defer to AGENTS.md)
├── PRIVACY.md                   (modes — default abstract)
├── REDACT.md                    (sensitive classes)
├── SHARING_POLICY.md            (connectors — OFF by default)
├── memory/
│   ├── hot.md                   (last 3 sessions, ≤500 words — read FIRST)
│   ├── index.md                 (domain index — read if hot insufficient)
│   ├── MEMORY.md                (agent-written session notes)
│   ├── DECISIONS.md             (confirmed decisions w/ provenance)
│   ├── OPEN_QUESTIONS.md        (unresolved questions)
│   ├── RISKS.md                 (identified risks w/ severity)
│   ├── CONFLICTS.md             (contradiction queue — user arbitrates)
│   ├── archive/                 (superseded entries — never deleted)
│   ├── patterns/PATTERNS.jsonl  (append-only tool/event log)
│   ├── snapshots/<iso>/         (point-in-time wiki state)
│   ├── sync/outbound/           (staged parent updates)
│   ├── sync/parent/             (received parent updates)
│   └── raw/                     (source material)
├── skills/<10 skills>/SKILL.md
├── skills/drafts/               (pattern-detected drafts pending approval)
├── agents/<6 agents>.md
├── commands/<8 commands>.md
├── team-packs/<6 packs>.md
├── team/                        (team pack outputs)
├── references/                  (qa-gate, safety, two-strikes, advisory, harness map, v4x-canon)
└── config/                      (PROJECT, PERMISSIONS, PARENT_SYNC, BUDGET, claude-overrides)
```

---

## Privacy model

Three root files govern privacy (per ZEREF_OS §4):

| File | Purpose | Default |
|---|---|---|
| `PRIVACY.md` | Modes: `exact` / `abstract` / `local-only` | **`abstract`** |
| `REDACT.md` | Sensitive classes: credentials, pii, internal_paths, client_data, financial, proprietary_code | credentials + pii + internal_paths enabled |
| `SHARING_POLICY.md` | Per-connector allowlist for MCP transmission | **all OFF** |

Every write to `memory/` and every external transmission passes through `privacy-guardian` per these files. Connectors recommended only after `pattern-observer` detects repeated manual behavior.

---

## Token budget (per ZEREF_OS §5)

Three tiers, auto-detected from the active model:

| Tier | Models | Behavior |
|---|---|---|
| **Free** | Gemini Flash, local Ollama, Mistral | aggressive compaction, minimal wiki writes |
| **Standard** | GPT-4o mini, Claude Haiku, Gemini Flash 3.5 | normal operation, full wiki writes |
| **God Mode** | GPT-4o, Claude Opus/Sonnet, Gemini 3.5 Pro | full parent-child sync, deep conflict analysis |

No hardcoded limits. User sets the ceiling in `config/BUDGET.md`. Zeref OS warns before approaching it.

---

## Team packs (per ZEREF_OS §8)

On-demand only. Max 4 agents. Outputs land in `team/`. Activate via `/team [type]`.

| Team | Roster | Use |
|---|---|---|
| solo | 1 primary + memory engine | default |
| build | Planner + Implementer + Reviewer | multi-module features |
| research | Investigator + Synthesizer + Fact-checker | tech evaluation, architecture |
| red | Attacker + Security reviewer + Constraint checker + Evidence recorder (**read-only**) | adversarial review |
| audit | Reader + Linter + Quality gate | pre-ship QA |
| ship | Changelog drafter + Release reviewer + Deploy verifier | release prep |

---

## Install

```bash
# Claude Code
claude plugin marketplace add kanadhiayash/zeref-os
claude plugin install zeref-os@zeref-os

# Cursor
git clone https://github.com/kanadhiayash/zeref-os.git .zeref
mkdir -p .cursor/rules && cp .zeref/.cursor/rules/zeref.mdc .cursor/rules/

# Windsurf
git clone https://github.com/kanadhiayash/zeref-os.git .zeref && cp .zeref/.windsurfrules .

# Aider
git clone https://github.com/kanadhiayash/zeref-os.git .zeref && cp .zeref/.aider.conf.yml.example .aider.conf.yml

# Codex / Gemini / Antigravity / Hermes / Amp / Zed / Perplexity
git clone https://github.com/kanadhiayash/zeref-os.git .zeref
# Point your harness at .zeref/AGENTS.md
```

Then in your harness: `/zeref-os:start` (or `/start`).

Full per-harness instructions: [`INSTALL.md`](INSTALL.md).

---

## Validation

```
$ python3 scripts/zeref-validate.py
Zeref OS validator — /path/to/project
Skills:           10/10
Agents:            6/6
Commands:          8/8
Team packs:        6/6
Config:            5/5
Root privacy:      3/3 (PRIVACY, REDACT, SHARING_POLICY)
v4x canon:         6/6
Harness stubs:     3/3
Memory layout:    flat
✔ Validation passed

$ claude plugin validate .
✔ Validation passed
```

CI runs `zeref-validate.py` on every push to `main` and every PR — see [`.github/workflows/zeref-validate.yml`](.github/workflows/zeref-validate.yml).

---

## Decision log highlights

Sourced from [`references/v4x-canon/DECISION_LOG.md`](references/v4x-canon/DECISION_LOG.md):

| # | Decision | Why |
|---|---|---|
| D1 | One wiki per project/repo, child→parent rollup | Project boundary maps to git boundary |
| D4 | Pattern detection: 48–80h window, 3× threshold, drafts only | Catches recurring workflows without auto-creating noise |
| D5 | Token budget auto-detected by model | Free install; capability scales with user's own tier |
| D6 | Developers first → Knowledge workers → End users | Git-first defaults, clean SKILL.md output |
| D7 | Harness Agnosticism: AGENTS.md is source of truth | Linux Foundation standard, 60k+ repos, 20+ tools |
| D8 | Privacy-first local memory; PRIVACY/REDACT/SHARING_POLICY at every project | Local-only canonical state, opt-in external sharing |
| D9 | Never hard delete — archive instead | Audit trail intact across iterations |
| D10 | Team packs on-demand, max 4 agents, red team read-only | Avoid always-on overhead; safety on adversarial mode |
| D11 | No bundled MCP tools — recommendation only | Respect user consent and harness portability |

Full table + rejected directions: [`references/v4x-canon/DECISION_LOG.md`](references/v4x-canon/DECISION_LOG.md).

---

## Model debate (cross-model design check)

From [`references/v4x-canon/MODEL_DEBATE.md`](references/v4x-canon/MODEL_DEBATE.md) — what each model needs and how Zeref OS scores:

| Parameter | Score /10 | Notes |
|---|---|---|
| Harness portability | 9.5 | AGENTS.md standard + translation map |
| Memory persistence | 10 | File-based; works with any harness, any model |
| Privacy protection | 9.5 | PRIVACY + REDACT + SHARING_POLICY. Best-in-class |
| Token efficiency | 9 | hot.md startup + deep retrieval |
| Developer experience | 9 | Git-first, conversational setup, draft-review |
| Rule compliance | 8 | 70% community baseline; lean file + Two-Strikes Rule |
| Scalability | 9 | Parent-child rollup handles org-wide knowledge |
| Free model support | 9.5 | Free tier explicitly designed |
| Pattern intelligence | 8.5 | 48–80h window, file-based log |
| Privacy-aware sharing | 9.5 | Strongest differentiator vs comparable systems |

---

## Engineering inspirations

Zeref OS stands on the work of many engineers in the AI agent and LLM tooling space. The most direct influences:

### Foundations
- **AGENTS.md** — Linux Foundation hosted open standard (60k+ repos, 20+ tools natively support). Zeref OS adopts AGENTS.md as the single source of truth.
- **Anthropic CLAUDE.md best practices** — informed the lean stub pattern, Two-Strikes Rule.
- **HumanLayer — "Writing a good CLAUDE.md"** — informed the boundary-first reads discipline.
- **Modern Agent Harness Blueprint 2026** (@amazingvince) — informed the harness-vs-context layering.

### Karpathy paradigm shifts
- **karpathy/autoresearch** (`program.md` pattern) — informed the structured reasoning flow.
- **karpathy/llm-council `CLAUDE.md`** — informed the rejected-direction "LLM council" framing (Zeref OS explicitly rejects this in favor of team packs).
- **forrestchang/andrej-karpathy-skills** (43k installs/week) — informed skill discipline.
- **affaan-m/ecc (AgentShield)** — informed safety gates.
- **Karpathy LLM Wiki gist** — informed the wiki-as-canonical-memory pattern.

### Memory + evolution patterns
- **jack60810/claude-evolve** (Darwinian memory, EMA rule ratings) — informed the confidence-decay + supersession model.
- **MEMORY.md read/write separation** — community-wide pattern. AGENTS.md = human-written, MEMORY.md = agent-written.
- **Auto Dream (relative→absolute date hygiene)** — informed the MEMORY.md auto-hygiene pass on `/done`.

### Community mental models
- **Armin Ronacher — "Logs as APIs, No Dead Ends"** — informed `PATTERNS.jsonl` as the harness-agnostic append-only log.
- **Geoffrey Huntley — stdlib + Ralph Wiggum technique** — informed the "skills are recommendations, not bundled tools" stance.
- **Harrison Chase — Model / Harness / Context layers** — informed the layered architecture (harness ≠ memory engine ≠ model).
- **Hamel Husain — "Evals as living PRD"** — informed the validator + CI structure.
- **Simon Willison on AGENTS.md** — informed adoption rationale.

### Spec-driven development
- **BMAD-METHOD** (43k stars) — informed the human-gated phase structure (project-setup interview).
- **GitHub Spec Kit** (6-phase, human-gated) — informed the conversational schema interview pattern.
- **Martin Fowler — SDD Tools Comparison** — informed the rejection of always-on agent fleets.
- **Kiro (AWS VS Code fork)** — informed the steering-files pattern (Zeref OS uses harness stubs instead).

### Knowledge management
- **ballred/obsidian-claude-pkm** (PARA starter kit) — informed the per-domain wiki structure.
- **AgriciDaniel/claude-obsidian** (Karpathy-style LLM Wiki) — informed the boundary-first read protocol.

### Canonical AGENTS.md samples studied
- `openai/codex`, `vercel/vercel`, `openai/openai-agents-python`, `vercel-labs/open-agents`, `vercel-labs/agent-skills`, `anthropics/anthropic-cookbook` — all carry production AGENTS.md files; Zeref OS adopts conventions consistent with all of them.

Full inspiration table with links: [`references/v4x-canon/RESEARCH_RESOURCES.md`](references/v4x-canon/RESEARCH_RESOURCES.md) and the **Inspirations** page on the [Wiki](https://github.com/kanadhiayash/zeref-os/wiki/Inspirations).

---

## Where Zeref OS diverges from community defaults

| Community default | Zeref OS choice | Reason |
|---|---|---|
| CLAUDE.md as primary file | AGENTS.md primary; CLAUDE.md = stub | Harness-agnostic |
| Skills bundled with the harness | Skills recommended only | User consent + portability |
| Memory in hosted service | Memory in local markdown | Privacy-first |
| Team agents always available | On-demand only | Token budget |
| Immediate skill activation | Review-first, approval required | Prevents misdetection |
| Single-user persona / "CEO" | Free for all users, no persona | Adoption |

---

## Documentation

- **[GitHub Wiki](https://github.com/kanadhiayash/zeref-os/wiki)** — full pages: Architecture, Memory model, Privacy model, Team packs, Pattern detection, Decision log, Model debates, Versioning history, FAQ, Glossary, Inspirations
- **[`AGENTS.md`](AGENTS.md)** — canonical agent spec
- **[`INSTALL.md`](INSTALL.md)** — per-harness install
- **[`MIGRATION.md`](MIGRATION.md)** — pre-1.0 migration paths
- **[`CHANGELOG.md`](CHANGELOG.md)** — v1.0.0 release notes
- **[`CHANGELOG-LEGACY.md`](CHANGELOG-LEGACY.md)** — pre-1.0 history
- **[`references/v4x-canon/`](references/v4x-canon/)** — imported design canon (ZEREF_OS spec, decision log, model debates, use cases, research resources)

---

## Roadmap

- **v1.0.0 (current)** — Zeref OS canonical release ✅
- **v1.x** — additive improvements, no breaking changes
- **v2.x** — only if a fundamental design assumption changes (unlikely)

---

## What Zeref OS is NOT (and what those mean)

- **Not itself a harness.** Zeref OS plugs *into* your existing harness (Claude Code, Cursor, Codex, Gemini CLI, Windsurf, Aider, etc.). It's the memory layer they read — not a replacement for the harness itself.
- **Not a hosted service.** No Zeref OS server, no account, no cloud. Your memory lives in local markdown files in your repo. Optional MCP connectors can talk to hosted services (GitHub, Linear, Notion, etc.) — but only after you explicitly enable them in `SHARING_POLICY.md`.
- **Not bundled with any MCP tools.** Recommendation-only. Zeref OS never installs a connector on your behalf.
- **Not a sprawling skill catalog.** 10 disciplined skills with strict triggers — not the v1.x "fleet of 109 specialist skills" approach.
- **Not an always-on multi-agent council.** Team packs are on-demand only and capped at 4 agents. No background swarm.
- **Not a CEO persona.** Zeref OS is a context + memory engine, not a leader. (Historical reject of the v3.x framing.)
- **Not dedicated to any single user or organization.** Free to install. Use with any project, any model you bring.

---

## License

MIT licensed. Free to install — bring your own models, your own harness.

---

<p align="center"><sub>Inspired by <a href="https://fairytail.fandom.com/wiki/Zeref_Dragneel">Zeref Dragneel</a>. Carry your memory with you.</sub></p>
