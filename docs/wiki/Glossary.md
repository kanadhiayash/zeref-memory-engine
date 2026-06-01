# Glossary

## A

**AGENTS.md**
The Linux Foundation-hosted open standard for agent specifications. 60k+ repos use it; 20+ tools natively support it. Zeref OS adopts AGENTS.md as the single source of truth; every harness-specific file (CLAUDE.md, GEMINI.md, .cursor/rules/zeref.mdc, .windsurfrules, .aider.conf.yml) is a thin stub.

**Abstract mode**
The default privacy mode. `privacy-abstraction` skill rewrites payloads before write, stripping enabled `REDACT.md` classes.

**Append-only log**
A file where new entries are appended but existing entries are never edited or deleted. `memory/patterns/PATTERNS.jsonl` is the canonical append-only log.

**Archive**
The directory `memory/archive/` where superseded entries are moved. Never hard delete per D9.

## B

**Boundary-first reads**
The discipline of reading `memory/hot.md` → `memory/index.md` → named section of named page, in that order. Never load a full page just to scan. Enforced by `budget-governor`.

**Budget-governor**
The skill that scales output verbosity and read patterns to the active model tier (Free / Standard / God Mode). Auto-detects from model.

## C

**Connector advisory**
Zeref OS recommends MCP tools but never bundles them. Recommendations triggered by `pattern-observer` detecting repeated manual behavior. See `references/connector-advisory.md`.

**Contradiction resolution**
When `memory-keeper` detects a conflict, both sides go to `memory/CONFLICTS.md`. User arbitrates. Never silent.

## D

**Decision log**
`memory/DECISIONS.md` — confirmed decisions with provenance + evidence grade. Single-writer (`memory-keeper` only).

**Domain index**
`memory/index.md` — boundary file. Lists domains and points to detail pages. Read after `hot.md`, before any page.

## E

**Evidence grade**
A confidence label on every wiki entry: **high** (verified this session / user-confirmed / primary source), **medium** (reasonable inference, named source, <30 days), **low** (unverified / >90 days / indirect). `evidence-curator` re-grades on staleness.

**Exact mode**
Privacy mode that writes full detail. Only used when user explicitly enables per project.

## F

**Free tier**
Budget tier for Gemini Flash, local Ollama, Mistral. Aggressive compaction, minimal wiki writes, short `/status` outputs.

## G

**God Mode**
Highest budget tier. Auto-activated when a high-tier model is detected (Claude Opus/Sonnet, GPT-4o, Gemini 3.5 Pro). Full parent-child sync, deep conflict analysis, pattern retrospectives.

## H

**Handoff**
A cross-harness package compiled at `/stop --handoff`: `SUMMARY.md` (≤1500 tokens), `STATE.json` (machine-readable), `NEXT.md` (next action), `HARNESS-MAP.md` (per-harness load instructions). Lives in `memory/sync/outbound/handoff-<iso>/`.

**Harness**
The AI tool the user is running in (Claude Code, Cursor, Codex, Gemini CLI, Windsurf, Aider, etc.). Zeref OS is harness-agnostic — same memory across all.

**Harness Translation Map**
`references/harness-translation-map.md` — table of per-harness config files + load methods. Adding a new harness = creating a new stub that points to AGENTS.md.

**Hot file**
`memory/hot.md` — ≤500 words, last 3 sessions + current context. Read FIRST every session.

## I

**Index**
See "Domain index".

## L

**Local-only mode**
Privacy mode that blocks all writes to `memory/sync/outbound/` and `memory/sync/parent/`. Project never propagates externally.

## M

**MEMORY.md**
`memory/MEMORY.md` — agent-written session notes. AGENTS.md = human-written, agent-read. MEMORY.md = agent-written, agent-read. First 200 lines auto-load on every session start.

**Memory engine**
The combination of `memory-keeper` + `privacy-guardian` + `pattern-observer` (background). Active in every team pack.

**Memory-keeper**
The single agent allowed to write to wiki files in `memory/`. Reads boundary-first. Logs every write to `PATTERNS.jsonl`.

## P

**PATTERNS.jsonl**
`memory/patterns/PATTERNS.jsonl` — append-only tool/event log. Source for `pattern-observer` scans.

**Pattern-observer**
Background agent that scans `PATTERNS.jsonl` over a rolling 48–80h window for repeated work (≥3 similar events, Jaccard ≥ 0.8). Surfaces candidates for `pattern-to-skill` to draft.

**Pattern-to-skill**
Skill that drafts new `SKILL.md` files from `pattern-observer` candidates. Drafts land in `skills/drafts/`. User reviews via `/zeref-os:review-skill`. Never auto-activates.

**Privacy-guardian**
Agent that enforces `PRIVACY.md` mode + `REDACT.md` classes + `SHARING_POLICY.md` allowlist on every write and every external transmission.

**Provenance**
Source attribution on every wiki entry: session ts, event hash, agent that produced it. Preserved across parent-sync.

## R

**REDACT.md**
Root file listing concrete sensitive classes (credentials, pii, internal_paths, client_data, financial, proprietary_code) with enable flags and replacement strategies.

**Red team**
Team pack for adversarial review. **Read-only by default.** Roster: Attacker + Security reviewer + Constraint checker + Evidence recorder.

**Review-first**
The discipline that new skills are drafted to `skills/drafts/` but never auto-activated. User must approve via `/zeref-os:review-skill`.

## S

**SHARING_POLICY.md**
Root file with per-connector allowlist. All connectors OFF by default. Each entry: `enabled`, `read_project_context`, `allowed_surfaces`, `redact_classes`.

**Single-writer**
Discipline that only `memory-keeper` writes to wiki files. Any other agent attempting these paths is blocked and the violation is logged.

**Snapshot**
Point-in-time wiki state at `memory/snapshots/<iso>/` with `manifest.json`. Created on every `/zeref-os:done`.

**Standard tier**
Budget tier for GPT-4o mini, Claude Haiku, Gemini Flash 3.5. Normal operation, full wiki writes, standard conflict scans.

## T

**Team pack**
A pre-defined multi-agent configuration. Six: solo, build, research, red, audit, ship. Max 4 agents. Outputs land in `team/`. Activate via `/zeref-os:team [type]`.

**Two-Strikes Rule**
Never codify a rule on the first occurrence of an error. Log it in `MEMORY.md` first. On second occurrence within 30 days, promote to a rule (skill / agent rule / AGENTS.md line / privacy entry). Prevents rule bloat. Codified in `references/two-strikes-rule.md`.

## V

**v4x-canon**
`references/v4x-canon/` — imported design corpus from the v4.x design phase: ZEREF_OS.md, DECISION_LOG.md, MODEL_DEBATE.md, USE_CASES.md, RESEARCH_RESOURCES.md, PACKAGE_INDEX.md. Read-only historical reference.

## W

**Wiki**
The collection of canonical markdown files in `memory/` that hold project knowledge: `index.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, `RISKS.md`, `CONFLICTS.md`, `MEMORY.md`, `hot.md`. Flat layout per ZEREF_OS §12.
