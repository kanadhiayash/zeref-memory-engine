# Model Debates

What each AI model needs from a memory engine, and how Zeref OS scores. Sourced from [`references/v4x-canon/MODEL_DEBATE.md`](https://github.com/kanadhiayash/zeref-os/blob/main/references/v4x-canon/MODEL_DEBATE.md) — synthesized from Anthropic, OpenAI, Google, and open-source community documentation (May 2026).

## Six things every model agrees on

1. Lean metadata at session start (not a wall of text)
2. Deep context on-demand (retrieved, not always-loaded)
3. External memory on disk (not in-context at all times)
4. Minimal tool count with high-leverage primitives
5. Deterministic scripts for reliability
6. Clear success criteria (declarative goals, not imperative steps)

Zeref OS satisfies all six via `memory/hot.md` startup, lean `AGENTS.md` protocol, token budget layer, connector advisory, and skill recommendation system.

## Claude (Anthropic) — top 10 needs

| # | Need | Zeref OS solution | Score /10 |
|---|---|---|---|
| 1 | Lean context loading (≤250 lines CLAUDE.md) | `CLAUDE.md` = 1-line stub to `AGENTS.md` | 10 |
| 2 | Persistent memory across sessions | `memory/hot.md` + `MEMORY.md` auto-loaded | 10 |
| 3 | Anti-sycophancy modes (Challenge / Steel-Man) | Defined in `AGENTS.md` §2 | 9 |
| 4 | Read/write memory separation | `AGENTS.md` (human) + `MEMORY.md` (agent-written) | 10 |
| 5 | Subagent context isolation | Team packs spawn with separate context windows | 9 |
| 6 | PreToolUse hooks for red lines | Red team pack + PRIVACY/REDACT gates | 8 |
| 7 | Two-Strikes Rule for file hygiene | Defined in §11 + `references/two-strikes-rule.md` | 10 |
| 8 | Rule lifecycle (active/dormant/dead) | `skills/drafts/` + `CONFLICTS.md` supersession | 9 |
| 9 | Path-scoped rules (zero token cost) | `AGENTS.md` + per-skill YAML frontmatter | 8 |
| 10 | Privacy-first output | `PRIVACY.md` + `REDACT.md` pre-write check | 10 |

**Gaps Zeref OS fixes:** zero-context session start (`hot.md`), sycophantic drift (challenge-first), CLAUDE.md rot (Two-Strikes).

## GPT-4o / OpenAI — top 10 needs

| # | Need | Zeref OS solution | Score /10 |
|---|---|---|---|
| 1 | Stable context prefix for prompt caching | `AGENTS.md` stable header structure | 9 |
| 2 | Append-only session history | `PATTERNS.jsonl` + `MEMORY.md` append model | 9 |
| 3 | External working memory (filesystem over context) | `memory/` file structure with handle-based retrieval | 10 |
| 4 | Narrow, namespaced tool set | Connector advisory: max 4 core tools | 9 |
| 5 | Clear success criteria per task | Schema interview enforces goal definition | 8 |
| 6 | No dead ends (closed tool loop) | Connector advisory: tools share filesystem | 8 |
| 7 | Codex-compatible AGENTS.md format | OpenAI Codex natively supports AGENTS.md | 10 |
| 8 | Versioned changelog | `CHANGELOG.md` + `CHANGELOG-LEGACY.md` | 9 |
| 9 | Oracle mode (cross-model consultation) | Red team + research team packs support multi-model input | 7 |
| 10 | Eval-driven rule validation | Two-Strikes + `skills/drafts/` review gate | 8 |

**Gaps Zeref OS fixes:** no persistent memory (`hot.md`), hallucinated tool calls (minimal tool set), sycophantic drift.

## Gemini (Google) — top 10 needs

| # | Need | Zeref OS solution | Score /10 |
|---|---|---|---|
| 1 | Native AGENTS.md support (Gemini CLI confirmed) | `AGENTS.md` as source of truth | 10 |
| 2 | Long context utilization (1M token window) | Deep wiki on demand; `hot.md` keeps startup lean | 9 |
| 3 | Grounding with web search | DuckDuckGo MCP recommended in core stack | 9 |
| 4 | Antigravity / Gemini CLI harness compatibility | `AGENTS.md` + harness translation map | 10 |
| 5 | Structured data output (JSON, schemas) | `WIKI.md` schema enforces structured entries | 8 |
| 6 | Cross-session state | `memory/` file structure | 10 |
| 7 | Multi-modal context (code + docs + images) | Team packs support vision-capable subagents | 8 |
| 8 | Tool calling with low hallucination | Narrow connector set + REDACT guard | 8 |
| 9 | God Mode auto-detection | Gemini 3.5 Pro triggers God Mode automatically | 10 |
| 10 | Pattern-based skill generation | `PATTERNS.jsonl` harness-agnostic log | 9 |

**Gaps Zeref OS fixes:** inconsistent tool call reliability (minimal tool set), over-explanation (imperative voice rules), long context dilution (`hot.md` startup).

## Open-source / Llama / Mistral / Ollama — top 10 needs

| # | Need | Zeref OS solution | Score /10 |
|---|---|---|---|
| 1 | Free tier operation without capability loss | Free tier in `BUDGET.md` with aggressive compaction | 10 |
| 2 | Local-only privacy (no cloud transmission) | Local canonical memory, no hosted service | 10 |
| 3 | Minimal context overhead | `hot.md` ≤500 words startup | 9 |
| 4 | Works without any external API | All memory files are local markdown | 10 |
| 5 | Graceful degradation with limited capability | Free tier behavior in `BUDGET.md` | 9 |
| 6 | Instruction compliance in smaller models | Lean `AGENTS.md` under 250 lines | 9 |
| 7 | No hallucinated tool calls | Narrow tool set reduces hallucination surface | 8 |
| 8 | Hermes compatibility | `PATTERNS.jsonl` file-based log works with Hermes | 9 |
| 9 | Upgrades to God Mode on stronger model switch | Auto-detection via `BUDGET.md` | 10 |
| 10 | Simple, predictable tool schemas | Core stack: simple, well-documented MCP only | 8 |

**Gaps Zeref OS fixes:** shorter context windows (`hot.md`), lower instruction compliance (lean `AGENTS.md`), no built-in memory.

## Cross-model summary

| Requirement | Claude | GPT | Gemini | Open-Source | Zeref OS satisfies? |
|---|---|---|---|---|---|
| Lean startup context | Critical | Critical | Critical | Critical | ✓ `hot.md` + stub CLAUDE.md |
| Persistent memory | ✓ | ✓ | ✓ | ✓ | ✓ `memory/` files |
| Privacy-first local memory | Medium | Medium | Medium | Critical | ✓ no hosted service |
| Anti-sycophancy | ✓ | Partial | Partial | Partial | ✓ challenge-first |
| Harness-agnostic | ✓ | ✓ | ✓ | ✓ | ✓ AGENTS.md |
| Free tier operation | N/A | N/A | N/A | Critical | ✓ Free tier in BUDGET.md |
| Tool set minimalism | ✓ | ✓ | ✓ | Critical | ✓ connector advisory |
| Rule lifecycle | ✓ | Partial | Partial | Partial | ✓ Two-Strikes + drafts/ |
| God Mode auto-detect | N/A | N/A | N/A | N/A | ✓ model-based |
| Pattern-based skills | Partial | Partial | Partial | Partial | ✓ PATTERNS.jsonl |

## Zeref OS ratings — cross-model average

| Parameter | Score /10 | Notes |
|---|---|---|
| Harness portability | 9.5 | AGENTS.md + translation map. Near-universal. |
| Memory persistence | 10 | File-based; works with any harness, any model |
| Privacy protection | 9.5 | PRIVACY + REDACT + SHARING_POLICY. Best-in-class |
| Token efficiency | 9 | hot.md startup + deep retrieval |
| Developer experience | 9 | Git-first, conversational setup, draft review |
| Rule compliance | 8 | 70% community baseline. Lean file + Two-Strikes improves it. |
| Scalability | 9 | Parent-child rollup handles org-wide knowledge |
| Free model support | 9.5 | Free tier explicitly designed |
| Pattern intelligence | 8.5 | 48–80h window, file-based log |
| Privacy-aware sharing | 9.5 | Strongest differentiator |
