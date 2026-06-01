# Inspirations

Zeref OS stands on the work of many engineers in the AI agent and LLM tooling space. This page documents the direct influences. Full reference: [`references/v4x-canon/RESEARCH_RESOURCES.md`](https://github.com/kanadhiayash/zeref-os/blob/main/references/v4x-canon/RESEARCH_RESOURCES.md).

## Foundations

### AGENTS.md standard

- [agents.md](https://agents.md) — Linux Foundation-hosted open standard. 60,000+ repos, 20+ tools natively supported.
- [redreamality blog — CLAUDE.md / AGENTS.md deep dive](https://redreamality.com/blog/claude-md-agents-md-deep-dive/) — 6000+ word survey
- [Anthropic CLAUDE.md best practices](https://docs.anthropic.com/claude/docs/claude-md-best-practices)
- [HumanLayer — Writing a good CLAUDE.md](https://humanlayer.dev/blog/writing-a-good-claude-md)
- [Modern Agent Harness Blueprint 2026 (@amazingvince)](https://gist.github.com/amazingvince/52158d00fb8b3ba1b8476bc62bb562e3)

**What Zeref OS takes:** AGENTS.md as the single source of truth; per-harness files are thin stubs. Lean-file discipline (under 250 lines for compliance). Read/write memory separation.

## Karpathy paradigm shifts

- [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — `program.md` pattern, structured reasoning flow
- [karpathy/llm-council `CLAUDE.md`](https://github.com/karpathy/llm-council) — referenced as rejected direction (Zeref OS does NOT adopt LLM council; team packs replace it)
- [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — 43k installs in one week
- [affaan-m/ecc (AgentShield)](https://github.com/affaan-m/ecc) — safety gates
- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — wiki-as-canonical-memory pattern
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
- [@karpathy on context engineering](https://x.com/karpathy) (June 25, 2025)

**What Zeref OS takes:** Skill discipline (not skill bloat). Boundary-first reads. Wiki-as-canon. Safety-gated extension. Karpathy's "context engineering" framing as a first-class concern.

## Canonical AGENTS.md / CLAUDE.md samples studied

- [openai/codex AGENTS.md](https://github.com/openai/codex)
- [vercel/vercel AGENTS.md](https://github.com/vercel/vercel)
- [openai/openai-agents-python AGENTS.md](https://github.com/openai/openai-agents-python)
- [vercel-labs/open-agents](https://github.com/vercel-labs/open-agents)
- [vercel-labs/agent-skills SKILL.md](https://github.com/vercel-labs/agent-skills)
- [anthropics/anthropic-cookbook AGENTS.md](https://github.com/anthropics/anthropic-cookbook)

**What Zeref OS takes:** YAML frontmatter conventions. Skill activation triggers. Compatibility with the de facto multi-vendor format.

## Community mental models

- [Armin Ronacher — Logs as APIs, No Dead Ends](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)
- [Geoffrey Huntley — stdlib and the Ralph Wiggum technique](https://ghuntley.com/specs/)
- Harrison Chase — Model / Harness / Context layers (Sequoia podcast)
- [Hamel Husain — Evals as living PRD](https://hamel.dev)
- [Simon Willison on AGENTS.md](https://simonwillison.net)

**What Zeref OS takes:** `PATTERNS.jsonl` as a "log as API" — the harness-agnostic event surface. Closed-tool-loop discipline (connectors share filesystem). Eval-driven rule validation (the validator + CI).

## Memory and evolution patterns

- [jack60810/claude-evolve](https://github.com/jack60810/claude-evolve) — Darwinian memory with EMA rule ratings
- **MEMORY.md read/write separation** — community-wide pattern, multiple sources
- **Two-Strikes Rule** — derived from Anthropic CLAUDE.md best practices
- **Auto Dream (relative → absolute date hygiene)** — community pattern

**What Zeref OS takes:** Confidence decay + supersession (the contradiction-resolution + archive flow). AGENTS.md = human-written / MEMORY.md = agent-written. Two-Strikes Rule for rule lifecycle. Auto-hygiene on every `/done` (relative dates → absolute).

## Spec-driven development

- [BMAD-METHOD](https://github.com/bmad-method) — 43k stars, structured phases
- [GitHub Spec Kit](https://github.com/github-spec-kit) — 6-phase, human-gated
- [Martin Fowler — SDD Tools Comparison](https://martinfowler.com)
- **Kiro** — AWS VS Code fork with steering files

**What Zeref OS takes:** Human-gated phase progression (the conversational `project-setup` interview). Steering-file pattern adapted as harness stubs.

## Knowledge management

- [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm) — PARA starter kit
- [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — Karpathy-style LLM Wiki

**What Zeref OS takes:** Per-domain wiki organization. Boundary-first read protocol.

## Key community data points (May 2026)

| Metric | Value | Source |
|---|---|---|
| AGENTS.md repos | 60,000+ | agents.md community |
| forrestchang/andrej-karpathy-skills installs | 43,000 in one week | community telemetry |
| BMAD-METHOD GitHub stars | 43,000 | github.com/bmad-method |
| CLAUDE.md instruction compliance | ~70% | community consensus; red lines need PreToolUse hooks |
| Optimal CLAUDE.md length | 60–250 lines | typical projects |
| Frontier-model reliable instruction count | ~150–200 before compliance decays | community testing |
| Context window utilization target | 40–60% (Huntley) | above 60% = quality drops |

## Where Zeref OS diverges from community defaults

| Community default | Zeref OS choice | Reason |
|---|---|---|
| `CLAUDE.md` as primary file | `AGENTS.md` primary, `CLAUDE.md` = stub | Harness-agnostic |
| Skills bundled in harness | Skills recommended only | User consent + portability |
| Memory in hosted service | Memory in local markdown | Privacy-first |
| Team agents always available | On-demand only | Token budget |
| Immediate skill activation | Review-first, approval required | Prevents misdetection |
| Single-user persona | Free for all users | Adoption |

## How to credit when forking

If you fork Zeref OS or adopt its patterns, attribution to the upstream community is appreciated:

```markdown
Built on Zeref OS (https://github.com/kanadhiayash/zeref-os) — itself inspired by:
- agents.md standard (Linux Foundation)
- Karpathy paradigm shifts (autoresearch, llm-council, LLM Wiki)
- BMAD-METHOD spec-driven development
- jack60810/claude-evolve memory evolution
- Anthropic CLAUDE.md best practices
- ...and the broader AI engineering community
```

The full reference list lives in [`references/v4x-canon/RESEARCH_RESOURCES.md`](https://github.com/kanadhiayash/zeref-os/blob/main/references/v4x-canon/RESEARCH_RESOURCES.md).
