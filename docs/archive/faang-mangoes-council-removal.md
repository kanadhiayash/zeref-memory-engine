> **ARCHIVED MIGRATION RECORD — historical reference only. The council does not exist in Zeref ≥ 2.0.0-alpha.1.**

# FAANG-MANGOES council — removal record

## What it was

`team-packs/faang-mangoes-council.md` was a 12-persona architectural-review panel, activated on demand (not part of the default `/team` menu), for load-bearing architecture decisions surfaced by the Repository-Wide Consistency Audit. Each persona was a model-engineering perspective named after a FAANG-MANGOES-lettered company (Facebook, Apple, Amazon, Netflix, Google, Microsoft, Anthropic, Nvidia, GitHub, OpenAI, Elastic, Stripe) — persona as perspective, not endorsement or affiliation.

Key characteristics:

- **Opus-tier by default.** All 12 persona verdicts and the reconciler synthesis ran on Opus 4.7; the constraint was "Opus only for critical and ambitious tasks," and irreversible-migration architecture calls were judged to meet that bar.
- **Batched execution.** Twelve concurrent Opus calls would spike token budget, so personas ran in three parallel batches of four (infra / product / reliability), each emitting a caveman-compressed verdict.
- **Dedicated output directory.** Every council decision packet wrote to `docs/audits/council/<decision-slug>.md`, never touching product code, never merging anything — the `Decision owner` field was always a human.
- **Registry presence.** Registered as the 10th entry in `zeref-registry.json`'s `team_packs` array, and referenced from `SOUL.md` and imported-skill READMEs as an on-demand, non-default pack.

## Why it was removed

Per `ZEREF_VNEXT_AGENTIC_OPERATIONS_UPGRADE_PLAN.md` §3.1 (see `docs/adr/ADR-0003-council-removal.md` for the full decision record):

- Persona review panels are not a Zeref team-pack type under the vNext model — team packs became dynamic mission compilation (mission blueprint + execution policy + compiled team), and a fixed 12-persona roster is exactly the kind of static named-agent concept that model replaces.
- The council's deliberation value over simpler review (single grader, same-model jury) was never benchmarked. The architecture plan requires council-style protocols to prove measurable benefit, not be assumed valuable because they existed.
- Council agreement must never be allowed to silently upgrade weak source evidence to a strong grade — a risk a hardcoded, always-Opus council could not be checked against without runtime instrumentation the old team-pack markdown didn't have.

## What replaces it

Two separate replacements, per the architecture plan:

1. **Dynamic mission compilation (PR 6-7).** Architecture decisions that used to route to the council instead go through normal mission blueprint → execution policy → compiled team resolution, with independence constraints (e.g. a verifier seat that cannot be the same capability as the implementer seat) enforced by the team compiler/resolver rather than a fixed persona roster.
2. **Optional evaluator adapters (PR 11).** The council's genuinely reusable protocol ideas — blind-first independent review, problem restatement, method/provider diversity, anti-conformity instructions, dissent preservation, independent synthesis — are reimplemented as runtime state transitions inside `zeref/evaluators/council_high_intelligence/`, integrating the external `0xNyk/council-of-high-intelligence` protocol as one optional, provider-neutral evaluator backend in Zeref's evidence system. It remains **experimental** until the council value benchmark (comparing it against a single grader, same-model jury, and cross-provider jury) shows measurable benefit, honestly reporting benefit, no benefit, or regression.

## Where history remains

- `CHANGELOG.md` — the 2.0.0-alpha.1 entry records the removal.
- `docs/audits/` — prior audit artifacts that reference the council (e.g. `ZEREF_COMPONENT_INVENTORY.md`, `ZEREF_CONSISTENCY_AUDIT.md`) are left as historical record and are not rewritten.
- This file — the only place the full persona roster, model routing, and decision-packet schema are preserved for reference.

No alias or compatibility shim exists for `faang-mangoes-council` — unlike the execution-policy and component renames in `docs/DEPRECATIONS.md`, this was a hard removal, not a rename.
