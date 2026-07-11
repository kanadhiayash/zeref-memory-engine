---
pack: faang-mangoes-council
budget_target_tokens_per_session: 600000
budget_hard_cap_tokens_per_session: 1200000
default_tier: opus
opus_allowed: true
sonnet_allowed: true
haiku_allowed: false
agents_active: 6                    # all Zeref background agents remain active
skills_active_max: 5
external_reviewers: true
personas: 12
activation: on-demand               # not part of default /team menu
scope: architectural-decisions-only
output_dir: docs/audits/council/
handoff_format: caveman-compressed
imported_at: 2026-07-10
---

# Team Pack: FAANG MANGOES LLM Model Engineer Council

> A 12-persona architectural-decision panel convened **only** for load-bearing architecture calls surfaced by the Repository-Wide Consistency Audit (Phase 5 §Orient + §Decide). Not a default team pack — activated explicitly by the audit reconciler or by the user.

## Why this exists

The audit's §Decide section enumerates architectural decisions that must not be silently resolved: canonical memory store, compatibility identifier, version number, team taxonomy, gate taxonomy, package publication, supported harness list. Each of those calls has multi-lens trade-offs (infra scale, on-device constraints, enterprise operability, alignment / safety, developer ergonomics). One reviewer collapses the trade space; twelve reviewers surface it.

## Roster — 12 personas

Each persona is a model-engineering perspective drawn from a company known for that lens. Persona = perspective, not endorsement or affiliation.

| # | Persona | Primary lens |
|---|---|---|
| 1 | **F**acebook / Meta | large-scale training infra, PyTorch ergonomics, open-model ecosystems |
| 2 | **A**pple | on-device inference, privacy-by-default, silicon-tuned model design |
| 3 | **A**mazon | cost-per-token economics, MLOps at fleet scale, Bedrock-style multi-vendor routing |
| 4 | **N**etflix | reliability, canary deployments, cost-vs-quality experiments |
| 5 | **G**oogle | search-scale retrieval, TPU-shaped training, Gemini-family multi-modal |
| 6 | **M**icrosoft | enterprise operability, Azure integration surface, Copilot productization |
| 7 | **A**nthropic | alignment, constitutional constraints, tool-use safety, harness-agnostic design |
| 8 | **N**vidia | hardware efficiency, CUDA-native serving, TensorRT + Triton |
| 9 | **G**itHub | developer workflow integration, PR-native surfaces, CODEOWNERS + CI ergonomics |
| 10 | **O**penAI | product-shaped model routing, function-calling contracts, assistants API patterns |
| 11 | **E**lastic | retrieval / RAG, index freshness, memory-as-search |
| 12 | **S**tripe | idempotency, observability, developer-experience-as-contract |

The letter grouping is a mnemonic: **F A A N G  M A N G O E S**.

## When to convene

- Phase 5 §Decide of the Repository-Wide Consistency Audit.
- Any architectural call surfaced by the reconciler that lacks a documented owner decision.
- Any user-triggered `/team faang-mangoes-council <decision-topic>` invocation.

## When NOT to convene

- P2 / P3 findings (cost outweighs signal).
- Reversible file-level fixes.
- Cosmetic naming inside a single doc.
- Anything the [`enterprise`](enterprise.md) pack can resolve on its own.

## Activation

```
/team faang-mangoes-council <decision-topic>
```

Example: `/team faang-mangoes-council canonical-memory-store`.

Optional args:

- `--personas=<comma-list>` — narrow the panel (e.g. `--personas=Anthropic,Google,Apple`).
  Default is all 12.
- `--rounds=<n>` — number of debate rounds before synthesis. Default 1.
- `--synth-model=opus` — synthesis model. Default Opus 4.7.

## Sequencing (Opus-budget-aware)

Twelve concurrent Opus 4.7 calls would spike the token budget. The council instead runs in **three parallel batches of four**:

1. **Infra batch:** Facebook / Google / Nvidia / Amazon
2. **Product batch:** Apple / Microsoft / OpenAI / GitHub
3. **Reliability batch:** Netflix / Anthropic / Elastic / Stripe

Batches execute in parallel (four concurrent agents per batch, matching the existing 4-agent ceiling). Each persona emits a **caveman-compressed** verdict per [`skills/caveman-handoff/SKILL.md`](../skills/caveman-handoff/SKILL.md) — drop articles / filler / pleasantries; keep file paths, exact errors, commands, code blocks verbatim.

A single reconciler agent (Opus 4.7) reads the 12 caveman verdicts and produces the synthesized decision packet.

## Decision packet schema

Every council-produced decision writes to `docs/audits/council/<decision-slug>.md` with this exact shape (mirrors the handoff §Phase 5 §Decide contract):

```
## Decision: <slug>
Current state:
Options:
Trade-offs:
Recommended decision:
Migration impact:
Evidence needed:
Decision owner:      (never the council itself)
Persona votes:       (per-persona 1-line verdicts)
Reconciler synthesis:
Confidence:          (high | medium | low)
Blocks lifted:       (list of P0/P1 findings this unblocks)
```

The `Decision owner` field is always a human — the audit is advisory. The council never merges anything.

## Model routing

| Role | Model |
|---|---|
| Persona verdicts (all 12) | Opus 4.7 |
| Reconciler synthesis | Opus 4.7 |
| Meta-check quality gate | Opus 4.7 |
| Council orchestration | Sonnet |
| Prep + evidence packaging | Haiku |

Rationale: the user constraint says Opus only for critical and ambitious tasks. Architectural decisions with irreversible migration blast radius meet that bar.

## Output rules

- Every council output lands under `docs/audits/council/`.
- Nothing council-produced modifies product code.
- Persona verdicts never leave `docs/audits/council/`; they are not published without user approval.
- Synthesized decision packet may be linked from `ZEREF_CONSISTENCY_AUDIT.md` §"Architecture decisions requiring owner approval".

## Fleet dependencies

- Uses [`skills/imported/ecc/`](../skills/imported/ecc/README.md) for GitHub-side operational tooling.
- Uses [`skills/imported/gstack/`](../skills/imported/gstack/README.md) for surface-mapping subskills.
- Red-team packs ([`mantishack`](../skills/imported/mantishack/README.md) / [`raptor`](../skills/imported/raptor/README.md) / [`hacker-bob`](../skills/imported/hacker-bob/README.md)) are **not** default council members. They are on-demand consultants for security-classified decisions only.

## Non-negotiables

- Council output is advisory. Owner approval required to merge any implementation.
- Council never edits product code.
- Council never publishes, tags, or deploys.
- Every persona verdict is caveman-compressed.
- Every synthesized decision names an owner (never itself).
- Council convocations are logged to `memory/DECISIONS.md` via `memory-keeper` after user acceptance.
