# Inspirations

Zeref OS draws from multiple lineages. Naming the influences makes the design legible and helps situate the project in the broader landscape.

## Naming — Zeref Dragneel (Fairy Tail)

The project is named after **Zeref Dragneel** from *Fairy Tail* — the immortal scholar whose ancient knowledge transcended form, time, and faction. He carried centuries of context with him; he never started from zero.

That's the design north star. **AI sessions today start from zero, every time.** You re-explain your project every conversation. You lose decisions to context window resets. You can't switch from Claude to Codex to Gemini to Cursor without abandoning your project memory.

Zeref OS is built in that lineage: **long-horizon memory, faithful to the user's accumulated decisions, portable across every AI harness**.

## Engineering lineage

### AGENTS.md as canonical interface

Heavily influenced by [agents.md](https://agents.md) and the cross-harness AGENTS convention. Source of truth lives in markdown, not vendor-specific config. Every harness reads the same file (or a thin stub that defers).

### Decision Records (ADRs)

The `docs/adr/` pattern + FAANG-brief naming convention (`zeref_<subject>_adr_<state>_yk_<date>_v<major.minor>.md`) draws from the [Architecture Decision Records](https://adr.github.io/) movement. Every non-trivial architectural choice gets its rationale captured.

### Append-only event logs

`memory/patterns/PATTERNS.jsonl` follows the event-sourcing tradition (Datomic, Kafka). Append-only; never edited; replay reconstructs state. Pattern detection scans the log as a stream.

### Two-Strikes Rule

Original to Zeref OS but inspired by lean / agile retrospective practice: don't codify a rule on the first error. Wait for the second. Prevents brittle premature rules.

### Privacy-deterministic (not LLM-judged)

SOUL.md principle 2: "Privacy claims need code proof, not prose." LLM is not a privacy enforcer. Heavily influenced by [secure-by-design](https://www.cisa.gov/securebydesign) principles + records-management discipline (deterministic redaction over heuristic judgement).

### Local-first

[Local-first software](https://www.inkandswitch.com/local-first/) (Ink & Switch). Your data on your disk. Your tools synthesize on top. No vendor lock-in.

### Cross-model handoff (caveman-handoff)

v2.6 caveman-handoff skill draws from caveman/grammar prompting research + structured token-compression patterns. Drop articles/filler/pleasantries; preserve technical substance verbatim. ~40-60% token reduction without entity loss.

## Doctrinal lineage

### GITHUB_OS (per-repo doctrine)

Per-repo `GITHUB_OS.md` (v2.6.1) customizes the global `~/Documents/Claude/00_COMMAND/GITHUB_OS.md` doctrine. Branch naming (`<type>/zeref__<desc>`), Conventional Commits with scope, trunk-based with protected `main`, SemVer tags on main only.

### FAANG architecture brief

Knowledge-OS naming + classification levels (`public` / `internal` / `confidential` / `restricted`) + retention-class archive model. Per `~/Documents/Claude/00_COMMAND/yash_faang_architecture_brief.md`.

### v4.x design canon

`references/v4x-canon/ZEREF_OS.md` is the immediate ancestor — the universal behavioral constitution that v1.0.0 inherited from v4.3. Read-only; never edited.

## Cultural influences

### Karpathy on AI engineering

Andrej Karpathy's writing on building AI systems (eval-first, version everything, treat prompts as code). Validated in v2.5 audit campaign (85-claim graded inventory; 300 sandbox rows; CVSS-scored security).

### "Eventually, draw a line"

The v1.0.0 rebrand decision — iteration is necessary; permanence is also necessary. After years of v1.x → v4.x rework, the v1.0.0 line was the deliberate stop. v2.6.1 hardens the line; doesn't redraw it.

### Hybrid stack discipline

Force multipliers used in v2.5 + v2.6.1 audit campaigns: ECC (eval-harness, security-scan, agent-eval), gstack (qa, review, ship), raptor/mantishack (adversarial), Graphify (knowledge graph), agent-skills (security-and-hardening, code-simplification). Zeref OS doesn't try to be all of these — it orchestrates them.

## What Zeref OS is NOT

- **Not a CEO persona** — context engine, not a leader (v3.0 rejected this framing)
- **Not a fleet of 109 skills** — disciplined 14 (post-v2.6)
- **Not an always-on multi-agent council** — team packs are on-demand only, max 4 agents
- **Not bundled with MCP tools** — recommendation-only per D11; all connectors OFF by default
- **Not a hosted service** — no Zeref OS server
- **Not vendor-locked** — bring any model; any harness

## Going forward

Influences shaping v2.7+:
- Cross-harness validation patterns (Cursor / Aider / Gemini live runs — ZRF-B07)
- Cascade-replay test design (path to 10.00/10 Execution)
- Model-resolver pin policy as new Anthropic releases ship

## Related

- [[Versioning-History]] — full iteration narrative
- [[Architecture]] — the shape that settled
- [[Decision-Log]] — rejected directions + ratified ADRs
- [`SOUL.md`](https://github.com/kanadhiayash/zeref-os/blob/main/SOUL.md) — 5 builder principles
- [`GITHUB_OS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/GITHUB_OS.md) — per-repo doctrine
