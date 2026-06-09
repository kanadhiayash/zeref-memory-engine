# Decision Log

Decisions span three layers:
1. **Canonical (D1–D11)** — `references/v4x-canon/DECISION_LOG.md`, foundational architecture decisions imported with v4.3
2. **Per-release ADRs** — `docs/adr/` per FAANG naming, capturing major version decisions
3. **Per-session arbitrations** — `memory/DECISIONS.md`, runtime decisions logged at ship time

## Canonical decisions (D1-D11, from v4.x canon)

| ID | Decision | Status |
|---|---|---|
| **D1** | Per-project canonical wiki in markdown (not DB) | ratified |
| **D2** | Append-only event log (`PATTERNS.jsonl`) — never edit lines | ratified |
| **D3** | Three privacy modes (`exact` / `abstract` / `local-only`); default `abstract` | ratified |
| **D4** | Pattern-observer window 48–80h; Jaccard ≥0.8; ≥3 occurrences | ratified |
| **D5** | God Mode unlocks via model detection (no separate gate) | ratified (v2.6 renamed to OPUS tier) |
| **D6** | Snapshots on `/done`; archive on supersede; never hard-delete | ratified (R2) |
| **D7** | AGENTS.md is source of truth; per-harness stubs defer | ratified (Core Principle 12) |
| **D8** | Privacy policy: PRIVACY/REDACT/SHARING_POLICY at repo root | ratified |
| **D9** | Archive content, never delete (non-deletion principle) | ratified (R2) |
| **D10** | Team packs are on-demand only (max 4 agents) | ratified |
| **D11** | Zero bundled MCP tools; recommendation-only per pattern-observer | ratified |

Full text: [`references/v4x-canon/DECISION_LOG.md`](https://github.com/kanadhiayash/zeref-os/blob/main/references/v4x-canon/DECISION_LOG.md).

## Architecture Decision Records (per release, `docs/adr/`)

Per FAANG brief naming: `zeref_<subject>_adr_<state>_yk_<yyyy-mm-dd>_v<major.minor>.md`.

### ADR-001 — Auto-Gated Execution (v2.6.0)

**File**: `docs/adr/zeref_auto-gated-execution_adr_approved_yk_2026-06-08_v1.0.md`

**Decision**: Ship 4-gate Auto-Activation chain. Every major task passes `budget-governor` (Gate #1) → `skill-router` (Gate #2) → `fleet-activator` (companion) → `prompt-context-engine` (Gate #3) before any execution-model token spend. Each gate declares output inline; user can override. Companion `caveman-handoff` preserves R6 chain across cross-model switches.

**Why**: cost variance 10× across same-domain tasks; skill-stack bloat (5-8 skills when 2-3 sufficed); prompt-injection rework loops; no enforcement of "use the right tier" principle.

**Consequences**: cost discipline by construction; smallest-useful-stack declared inline; UNSTRUCTURED prompts auto-restructured; R6 enforced; grep-able audit trail. Negative: 4 gates add ~500 tokens output per task (classification cost << execution cost); gate output initially prose-only (addressed in ADR-002); 10→14 skills.

**Alternatives rejected**: single combined gate (conflates concerns); silent background gate (no override path); manual user invocation (status-quo failed); hard-block at validator level (too rigid).

### ADR-002 — Audit + Hardening L1-L15 (v2.6.1)

**File**: `docs/adr/zeref_audit-hardening-l1-l15_adr_approved_yk_2026-06-08_v1.0.md`

**Decision**: Ship 15 L-items in Phase D after Phase F AskUserQuestion arbitration. All recommended paths chosen:
- L1: validator dynamic skill count from registry
- L2: model resolver (full Anthropic ids canonical)
- L3+L5+L14+L15: `lint_patterns_log()` event schema validator
- L4: R6 sweep (4 → 9 SKILL.md coverage)
- L9: marker-file probe (closes V03 probe-spoof HIGH)
- L10: injection filter (closes V02 prompt-injection CRITICAL)
- L11: 60s irreversibility cool-down (closes V06 race MEDIUM)
- L12: NFKC + homoglyph guard (closes V04 path HIGH)
- L13: dual-key override (closes V05 silent override MEDIUM)

**Why**: v2.6.0 4-gate chain was prose-only. Phase C surfaced 2 CRITICAL + 2 HIGH + 2 MEDIUM. Phase A claim audit found 30% PARTIAL or UNVERIFIED. Validator hardcoded `Skills: 10/10` despite 14 dirs.

**Consequences**: all CRITICAL+HIGH+MEDIUM closed; truthful validator state; explicit model versioning; R6 coverage 4→9 SKILL.md; PATTERNS.jsonl integrity validator; adversarial sandbox failures (probe-spoof / injection / homoglyph) blocked; rubric 8.00→9.88 (+1.88).

**Alternatives rejected**: `zeref/gate.py` enforcement module (higher cost, new dep); skip L4 R6 sweep (would leave 10 SKILL.md silent); defer V05 dual-key (slow leak).

## Per-session arbitrations (`memory/DECISIONS.md`)

Each `/done` may log a decision. Format:

```
### YYYY-MM-DD — [Title]
**Decided**: [what was decided]
**Why**: [reasoning]
**Evidence**: high | medium | low | unverified
**Provenance**: [session ts, plan, validator output, commit SHA]
**Supersedes**: [previous decision id, if any]
```

Notable v2.6.1 session entries:
- **2026-06-08** Ship v2.6.0 — Auto-Gated Execution (retroactive log; C1 memory-drift root cause)
- **2026-06-08** Ship v2.5.0 — Deep Audit Campaign (retroactive log)
- **2026-06-08** Phase F arbitration locked (4 decisions across L1-L15 paths)

## Rejected directions (kept for memory)

| Direction | Why rejected |
|---|---|
| Always-on multi-agent council | Theatrical; overhead doesn't pay |
| CEO persona for single user | Wrong abstraction for context engine; limits adoption |
| Auto-merge contradictions by recency or evidence | Silent resolve violates human-arbitration principle |
| Bundle MCP connectors in the plugin | Couples plugin to specific tools; OFF by default per D11 |
| Synthetic test data shipped with plugin | Pollutes user PATTERNS log; smoke tests live in `tests/` only |
| Hosted Zeref OS server | Violates local-first; introduces dependency + privacy surface |
| LLM as privacy enforcer | Per SOUL.md principle 2: privacy claims need code proof, not prose |
| Auto-bump skill count without registry update | Caused v2.6.0 validator silent under-report (L1) |
| Single-key override of cost-tier mismatch | Slow privacy/quality leak (V05); v2.6.1 L13 enforces dual-key |
| Prose-only gate enforcement | Phase C V01 gate-spoof CRITICAL; v2.6.1 L3 advisory lint |

## Decision provenance chain

Every decision should be traceable:
1. Triggering signal (PATTERNS event / claim audit row / Phase C finding / user request)
2. Arbitration (AskUserQuestion batch / inline confirm / Two-Strikes Rule)
3. Decision logged (DECISIONS.md / ADR / CONFLICTS.md resolution field)
4. Evidence cited (test artifact / validator output / commit SHA)
5. Forward references (ADRs that supersede; future ADRs that extend)

## Related

- [[Versioning-History]] — per-release narrative
- [[Architecture]] — current 14-skill state
- [[Glossary]] — D-numbers, L-items, R-rules definitions
- [`memory/CONFLICTS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/memory/CONFLICTS.md) — open + resolved contradictions
- [`memory/RISKS.md`](https://github.com/kanadhiayash/zeref-os/blob/main/memory/RISKS.md) — R1-R6 risks with mitigation refs
