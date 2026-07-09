# Benchmark Report — Zeref OS v1.0.0

_Generated: 2026-07-09. Rubric: [`benchmarks/RUBRIC.md`](benchmarks/RUBRIC.md)._

## Verdict

**PASS** — every axis ≥ 9.0, no axis below 8.0.

The `trust` axis is independently re-graded by the security audit before publication. When the audit score is lower than the deterministic draft, the verified score is the published score.

## Scores

| Axis | Score | Pass? | Note |
|---|---:|:---:|---|
| portability | 10.00 | ✅ |  |
| adaptivity | 9.00 | ✅ |  |
| scalability | 10.00 | ✅ |  |
| retrieval | 10.00 | ✅ |  |
| trust | 9.70 | ✅ | Verified by TRUST_AUDIT.md; deterministic draft was 10.00. |

## Portability — 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `canonical_agents_md` | 10.00 | AGENTS.md present; 7/7 stubs cite it |
| `per_harness_stubs` | 10.00 | 7/7 harness stubs present: ['CLAUDE.md', 'CODEX.md', 'GEMINI.md', 'LLAMA.md', '.windsurfrules', '.aider.conf.yml.example', '.cursor/rules/zeref.mdc'] |
| `harness_probe` | 10.00 | probe ran clean; 7/7 stubs present |
| `harness_matrix` | 10.00 | HARNESS_MATRIX.md has ~8 harness rows |
| `cli_works` | 10.00 | CLI --version and status both clean |

## Adaptivity — 9.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `router_ranking` | 7.00 | router doc: ranking=True, recency=False |
| `importer_doc` | 10.00 | skill-importer present; provenance documented=True |
| `provenance` | 10.00 | sha=True, source_path=True |
| `review_gate` | 8.00 | review-gated=True, audit-logged=False |
| `privacy_filter` | 10.00 | privacy-filter=True, rejects-on-hit=True |

## Scalability — 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `packs_exist` | 10.00 | 3/3 packs present; 3/3 with token envelope |
| `budget_enforced` | 10.00 | soft=True, hard=True, override=True |
| `tier_routed` | 10.00 | 3/3 packs set default_tier; opus_reserved=True |
| `r6_preserved` | 10.00 | R6 in rules=True, R6 referenced in handoff skills=True |
| `decision_criteria` | 10.00 | 3/3 packs document upgrade/use criteria |

## Retrieval — 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `fixture_inventory` | 10.00 | 5/5 fixtures present |
| `continuity` | 10.00 | returns source_ref/confidence/authority/why_returned |
| `privacy_recall` | 10.00 | raw credential fixture scrubbed before recall |
| `contradiction` | 10.00 | conflicting same-entity assumptions both returned |
| `freshness` | 10.00 | updated item is freshest and history records update |
| `abstention` | 10.00 | unmatched query returns empty result set |
| `external_adapter_fixtures` | 10.00 | LoCoMo=fixture_pass, LongMemEval=fixture_pass, BEAM=fixture_pass, PersonaMem=fixture_pass, PersonaMem-v2=fixture_pass |

> _Deterministic lexical/FTS5 retrieval benchmark; external adapters are fixture-only unless marked verified._


## Trust — 9.70 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `version_consistency` | 10.00 | checker clean; ci_enforced=True |
| `test_suite` | 10.00 | 21 test files; pytest.ini=True; ci=True |
| `privacy_patterns` | 10.00 | 9 provider-shaped credential patterns wired |
| `security_md` | 10.00 | no_public_route=True, pvr=True, pgp=True, window=True |
| `ci_hardening` | 10.00 | 9/9 action refs SHA-pinned (100%); dependabot=True |

> _Deterministic draft score was 10.00. Published trust score is 9.70 per docs/TRUST_AUDIT.md independent audit._


## How to reproduce

```bash
python3 benchmarks/run-all.py
```

Per-axis scorers under `benchmarks/` are standalone:

```bash
python3 -m benchmarks.portability
python3 -m benchmarks.adaptivity
python3 -m benchmarks.scalability
python3 -m benchmarks.retrieval
python3 -m benchmarks.trust
```

## Rubric

Sub-criteria and weights: [`benchmarks/RUBRIC.md`](benchmarks/RUBRIC.md).
External re-scoring invited via PR.
