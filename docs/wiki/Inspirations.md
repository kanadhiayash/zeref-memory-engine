# Inspirations

Zeref OS draws from multiple lineages. Naming the influences makes the design legible and helps situate the project in the broader landscape.

## Naming — Zeref Dragneel (Fairy Tail)

The project is named after **Zeref Dragneel** from *Fairy Tail* — the immortal scholar whose ancient knowledge transcended form, time, and faction. He carried centuries of context with him; he never started from zero.

That is the design north star. **AI sessions today start from zero, every time.** You re-explain your project every conversation. You lose decisions to context window resets. You can't switch from Claude to Codex to Gemini to Cursor without abandoning your project memory.

Zeref OS is built in that lineage: **long-horizon memory, faithful to the user's accumulated decisions, portable across every AI harness**.

## Engineering lineage

### AGENTS.md as canonical interface

Heavily influenced by [agents.md](https://agents.md) and the cross-harness AGENTS convention. Source of truth lives in markdown, not vendor-specific config. Every harness reads the same file (or a thin stub that defers).

### Append-only event logs

`memory/patterns/PATTERNS.jsonl` follows the event-sourcing tradition (Datomic, Kafka). Append-only; never edited; replay reconstructs state. Pattern detection scans the log as a stream.

### Two-Strikes Rule

Original to Zeref OS but inspired by lean / agile retrospective practice: don't codify a rule on the first error. Wait for the second. Prevents brittle premature rules.

### Privacy-deterministic (not LLM-judged)

LLMs are not privacy enforcers. Deterministic regex + Unicode normalization + base64 decode + homoglyph tables enforce REDACT classes. Heavily influenced by [secure-by-design](https://www.cisa.gov/securebydesign) principles and records-management discipline.

### Local-first

[Local-first software](https://www.inkandswitch.com/local-first/) (Ink & Switch). Your data on your disk. Your tools synthesize on top. No vendor lock-in.

### Cross-model handoff (caveman-handoff)

Draws from caveman / grammar-prompting research and structured token-compression patterns. Drop articles / filler / pleasantries; preserve technical substance verbatim. Token reduction varies by content; entity preservation is the design goal (unmeasured claim removed per 2026-07-13 audit).

## Doctrinal lineage

### Per-repo doctrine

`GITHUB_OS.md` customizes a global GitHub Operating System: branch naming (`<type>/zeref__<desc>`), Conventional Commits with scope, trunk-based with protected `main`, SemVer tags on `main` only.

### v4.x design canon

`references/v4x-canon/ZEREF_OS.md` is the immediate ancestor — the universal behavioral constitution that v1.0.0 inherited from v4.3. Read-only; never edited.

## Cultural influences

### Karpathy on AI engineering

Andrej Karpathy's writing on building AI systems (eval-first, version everything, treat prompts as code).

### "Eventually, draw a line"

The v1.0.0 rebrand decision — iteration is necessary; permanence is also necessary. After years of rework, the v1.0.0 line was the deliberate stop.

### Hybrid stack discipline

Force multipliers used during build: ECC (eval-harness, security-scan, agent-eval), gstack (qa, review, ship), Graphify (knowledge graph), agent-skills (security-and-hardening, code-simplification). Zeref OS doesn't try to be all of these — it orchestrates them.

## What Zeref OS is NOT

- **Not a CEO persona** — context engine, not a leader.
- **Not a fleet of specialist skills** — 14 disciplined skills.
- **Not an always-on multi-agent council** — team packs are on-demand only, max 4 agents.
- **Not bundled with MCP tools** — recommendation-only; all connectors OFF by default.
- **Not a hosted service** — no Zeref OS server.
- **Not vendor-locked** — bring any model; any harness.

## Related

- [[Architecture]] — the shape that settled
- [[Memory-Model]] — how memory lives on disk
- [`GITHUB_OS.md`](https://github.com/kanadhiayash/zeref-memory-engine/blob/main/GITHUB_OS.md) — per-repo doctrine
