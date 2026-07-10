# Benchmark Report - Zeref Memory Engine

_Generated: 2026-07-10. Rubric: [`benchmarks/RUBRIC.md`](benchmarks/RUBRIC.md)._

## Verdict

**PASS** - deterministic local benchmark gates passed.

This report is local and deterministic. It does not claim external superiority, production readiness, or a final perfect-score verdict.

The `trust` axis is independently re-graded by the security audit before publication. When the audit score is lower than the deterministic draft, the verified score is the published score.

Lineage axes validate local intake metadata, implementation registries, and guardrails. They are not external-dataset verification of the referenced projects.

## Scores

| Axis | Score | Status | Note |
|---|---:|---|---|
| portability | 10.00 | pass |  |
| adaptivity | 9.00 | pass |  |
| scalability | 10.00 | pass |  |
| retrieval | 10.00 | pass |  |
| trust | 9.70 | pass | Verified by TRUST_AUDIT.md; deterministic draft was 10.00. |
| token_efficiency | 10.00 | pass |  |
| retrieval_accuracy | 10.00 | pass |  |
| contradiction_detection | 10.00 | pass |  |
| privacy_safety | 10.00 | pass |  |
| prompt_rewrite_quality | 10.00 | pass |  |
| handoff_success | 10.00 | pass |  |
| loop_control | 10.00 | pass |  |
| memory_refinement | 10.00 | pass |  |
| lineage_import_coverage | 10.00 | pass |  |
| foreign_code_containment | 10.00 | pass |  |
| critical_adoption_coverage | 10.00 | pass |  |
| high_adoption_coverage | 10.00 | pass |  |
| reference_only_guardrails | 10.00 | pass |  |
| adapter_value | 10.00 | pass |  |
| minimality_pressure | 10.00 | pass |  |
| security_containment | 10.00 | pass |  |
| license_boundary | 10.00 | pass |  |
| public_claim_safety | 10.00 | pass |  |

## Portability - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `canonical_agents_md` | 10.00 | AGENTS.md present; 7/7 stubs cite it |
| `per_harness_stubs` | 10.00 | 7/7 harness stubs present: ['CLAUDE.md', 'CODEX.md', 'GEMINI.md', 'LLAMA.md', '.windsurfrules', '.aider.conf.yml.example', '.cursor/rules/zeref.mdc'] |
| `harness_probe` | 10.00 | probe ran clean; 7/7 stubs present |
| `harness_matrix` | 10.00 | HARNESS_MATRIX.md has ~8 harness rows |
| `cli_works` | 10.00 | CLI --version and status both clean |

## Adaptivity - 9.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `router_ranking` | 7.00 | router doc: ranking=True, recency=False |
| `importer_doc` | 10.00 | skill-importer present; provenance documented=True |
| `provenance` | 10.00 | sha=True, source_path=True |
| `review_gate` | 8.00 | review-gated=True, audit-logged=False |
| `privacy_filter` | 10.00 | privacy-filter=True, rejects-on-hit=True |

## Scalability - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `packs_exist` | 10.00 | 3/3 packs present; 3/3 with token envelope |
| `budget_enforced` | 10.00 | soft=True, hard=True, override=True |
| `tier_routed` | 10.00 | 3/3 packs set default_tier; opus_reserved=True |
| `r6_preserved` | 10.00 | R6 in rules=True, R6 referenced in handoff skills=True |
| `decision_criteria` | 10.00 | 3/3 packs document upgrade/use criteria |

## Retrieval - 10.00 / 10

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


## Trust - 9.70 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `version_consistency` | 10.00 | checker clean; ci_enforced=True |
| `test_suite` | 10.00 | 34 test files; pytest.ini=True; ci=True |
| `privacy_patterns` | 10.00 | 9 provider-shaped credential patterns wired |
| `security_md` | 10.00 | no_public_route=True, pvr=True, pgp=True, window=True |
| `ci_hardening` | 10.00 | 9/9 action refs SHA-pinned (100%); dependabot=True |

> _Deterministic draft score was 10.00. Published trust score is 9.70 per docs/TRUST_AUDIT.md independent audit._


## Token Efficiency - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `markdown_guard` | 10.00 | markdown rewrite executor=blocked |
| `minimalism_ladder` | 10.00 | duplicate=link-existing, append=atom-append, patch=atom-patch |
| `flagship_gate` | 10.00 | public claim executor=flagship |
| `deterministic_estimator` | 10.00 | estimate=4 deterministic=True |

## Retrieval Accuracy - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `sqlite_indexed_recall` | 10.00 | top=decision_58a41da65ceb8ea0 |
| `jsonl_fallback_recall` | 10.00 | top=decision_58a41da65ceb8ea0 |
| `explain_search` | 10.00 | candidates=1 |

## Contradiction Detection - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `case_creation` | 10.00 | created=1 |
| `arbitration_required` | 10.00 | User arbitration required. Pick a winner with resolve --winner and provide --reason. |
| `no_silent_resolution` | 10.00 | before_status=active |
| `explicit_resolution` | 10.00 | after_status=superseded |

## Privacy Safety - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `credential_scrub` | 10.00 | redacted=2 |
| `handoff_field_scrub` | 10.00 | atom_id_preserved=True |
| `redaction_metadata` | 10.00 | field_redactions=1 |

## Prompt Rewrite Quality - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `classification` | 10.00 | SEMI_STRUCTURED |
| `brief_fields` | 10.00 | fields=['classification', 'constraints', 'context', 'deliverable', 'execution_loop', 'missing_info', 'objective', 'risks', 'source_prompt', 'success_criteria', 'verification'] |
| `wording_preserved` | 10.00 | I want to change the dashboard screen buttons just like we did on settings page. |
| `inject_target` | 10.00 | codex |
| `unsafe_flag` | 10.00 | UNSAFE |
| `markdown_output` | 10.00 | markdown generated |

## Handoff Success - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `artifact_files` | 10.00 | markdown_exists=True json_exists=True |
| `source_backed_content` | 10.00 | atom ids present in markdown |
| `machine_readable_json` | 10.00 | target=human |
| `verification_checklist` | 10.00 | checklist present |

## Loop Control - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `bounded_contract` | 10.00 | max=2 |
| `run_stops` | 10.00 | iterations=1 |
| `no_direct_memory_write` | 10.00 | proposal={'direct_memory_write': False, 'loop_id': 'loop_f739bd7783a0', 'note': 'Loop runtime emits proposals only; durable memory writes require separate commands.', 'proposed_atoms': []} |
| `status_available` | 10.00 | latest status read |
| `report_available` | 10.00 | report read |

## Memory Refinement - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `duplicate_detection` | 10.00 | groups=1 |
| `unsupported_detection` | 10.00 | unsupported=1 |
| `dry_run_no_write` | 10.00 | report_after_dry=False |
| `report_write` | 10.00 | json_written=True markdown_written=True |
| `view_render` | 10.00 | rendered=5 |

## Lineage Import Coverage - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `all_rows_validated` | 10.00 | 64 intake rows validated |
| `deduped_source_scopes` | 10.00 | sources=59 |
| `dry_run_no_writes` | 10.00 | metadata-only dry-run fixture |

## Foreign Code Containment - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `critical_no_foreign_code` | 10.00 | critical gates report no vendored foreign code |
| `high_no_core_dependency` | 10.00 | 21 high rows optional or gated |
| `reference_no_runtime_bundle` | 10.00 | 19 reference rows evidence-only |

## Critical Adoption Coverage - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `all_critical_rows` | 10.00 | 10 critical rows detected |
| `all_implemented` | 10.00 | 10 critical gates implemented |
| `core_or_gate` | 10.00 | all critical rows implemented as core or gates |

## High Adoption Coverage - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `all_high_rows` | 10.00 | 21 high rows detected |
| `all_implemented` | 10.00 | 21 high boundaries implemented |
| `optional_or_gated` | 10.00 | all high rows optional or gated |

## Reference Only Guardrails - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `all_reference_rows` | 10.00 | 19 reference-only rows detected |
| `all_guarded` | 10.00 | 19 reference-only battle tests implemented |
| `evidence_only` | 10.00 | no reference-only runtime bundles |

## Adapter Value - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `optional_adapters_present` | 10.00 | 4 optional adapter targets gated |
| `fixtures_present` | 10.00 | 4 benchmark fixture adaptations |
| `connector_policy_present` | 10.00 | connector boundary represented |

## Minimality Pressure - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `high_not_core` | 10.00 | high rows did not become core dependencies |
| `reference_not_runtime` | 10.00 | reference rows did not enter runtime |
| `rejection_preserved` | 10.00 | reject verdict preserved |

## Security Containment - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `security_references_contained` | 10.00 | raptor/mantishack/hacker-bob evidence-only |
| `defensive_fixture_only` | 10.00 | Purple Llama adapted as safety fixture only |
| `critical_rails_present` | 10.00 | critical rail gates included |

## License Boundary - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `license_metadata_recorded` | 10.00 | sources=59 |
| `concept_source_marked` | 10.00 | Software 2.0 marked citation |
| `archived_reference_marked` | 10.00 | archived PromptBench fixture marked |

## Public Claim Safety - 10.00 / 10

| Sub-criterion | Score | Evidence |
|---|---:|---|
| `no_superiority_verdict` | 10.00 | escalation policy avoids superiority claims |
| `strict_council_passed` | 10.00 | strict council gate passed |
| `reference_rows_not_promoted` | 10.00 | 19 reference-only rows retained |

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
python3 -m benchmarks.token_efficiency
python3 -m benchmarks.retrieval_accuracy
python3 -m benchmarks.contradiction_detection
python3 -m benchmarks.privacy_safety
python3 -m benchmarks.prompt_rewrite_quality
python3 -m benchmarks.handoff_success
python3 -m benchmarks.loop_control
python3 -m benchmarks.memory_refinement
python3 -m benchmarks.lineage_import_coverage
python3 -m benchmarks.foreign_code_containment
python3 -m benchmarks.critical_adoption_coverage
python3 -m benchmarks.high_adoption_coverage
python3 -m benchmarks.reference_only_guardrails
python3 -m benchmarks.adapter_value
python3 -m benchmarks.minimality_pressure
python3 -m benchmarks.security_containment
python3 -m benchmarks.license_boundary
python3 -m benchmarks.public_claim_safety
```

## Rubric

Sub-criteria and weights: [`benchmarks/RUBRIC.md`](benchmarks/RUBRIC.md).
External re-scoring invited via PR.
