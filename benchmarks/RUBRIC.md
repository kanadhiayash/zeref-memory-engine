# Benchmark Rubric — Zeref OS v1.0.0

Public, versioned, contestable. Every axis is scored 0–10 with explicit
sub-criteria. The pass bar is **every axis ≥ 9.0 with no axis below 8.0**.

External re-scoring is invited via PR. See `CONTRIBUTING.md` for the
process.

---

## Axis 1 — Portability

> Can a fresh user, in any supported AI harness, boot Zeref OS and reach
> a working memory layer with no manual editing?

| Sub-criterion | Weight | 0–3 | 4–6 | 7–8 | 9–10 |
|---|---|---|---|---|---|
| Canonical `AGENTS.md` exists and is read first | 2 | absent | partial | present | present + cited by every stub |
| Per-harness stubs exist and defer to `AGENTS.md` | 2 | <3 stubs | 3–4 | 5–6 | ≥7 stubs (claude/codex/cursor/windsurf/aider/gemini/llama) |
| `scripts/harness-probe.py` reports stub + binary status | 2 | missing | partial | works for some | works for all |
| `docs/HARNESS_MATRIX.md` documents per-harness boot result | 2 | missing | aspirational only | partial evidence | every row verified |
| CLI works headless (`python3 -m zeref status` on any host) | 2 | crashes | partial | runs but unclear | clean exit + readable output |

**Score = weighted sum / 2** (range 0–10).

---

## Axis 2 — Adaptivity

> Can Zeref OS import and rank skills the user already has, rather than
> forcing them to re-author the same skill inside the project?

| Sub-criterion | Weight | 0–3 | 4–6 | 7–8 | 9–10 |
|---|---|---|---|---|---|
| `skill-router` ranks across project + user dirs | 2 | project only | hardcoded list | trigger-match | trigger-match + recency |
| `skill-importer` exists and is documented | 2 | missing | exists but undoc | exists + doc | exists + doc + provenance tracked |
| Imported skills carry SHA + source path provenance | 2 | none | partial | yes | yes + tamper-detect |
| Imports gated behind `/review-skill` (no auto-activate) | 2 | auto-activates | partial gate | gated | gated + audit-logged |
| Privacy filter rejects credential-laden imports | 2 | no filter | warns | rejects | rejects + diff surfaced |

**Score = weighted sum / 2**.

---

## Axis 3 — Scalability

> Can a user pick a team size that matches their budget without losing
> the invariants?

| Sub-criterion | Weight | 0–3 | 4–6 | 7–8 | 9–10 |
|---|---|---|---|---|---|
| `team-packs/{small,medium,enterprise}.md` exist with explicit token envelopes | 2 | missing | 1 pack | 2 packs | 3 packs + per-pack envelope |
| `budget-governor` enforces the envelope (soft + hard caps) | 2 | unenforced | soft only | both | both + override grammar |
| Default tier per pack documented + model choice routed accordingly | 2 | undocumented | partial | documented | documented + opus reserved |
| R6 invariant survives across all pack sizes | 2 | broken in small | broken in one | preserved | preserved + tested |
| Pack-up / pack-down decision criteria documented | 2 | none | implicit | per pack | per pack + measurable triggers |

**Score = weighted sum / 2**.

---

## Axis 4 — Trust

> Is every public claim operationally verified, not just conceptually
> stated?

| Sub-criterion | Weight | 0–3 | 4–6 | 7–8 | 9–10 |
|---|---|---|---|---|---|
| Version consistency across all surfaces (machine-checked) | 2 | drift | manual check | scripted check | scripted + CI-enforced |
| Reproducible `tests/` directory ≥ 85% coverage on `zeref/` | 2 | none | exists | covers most | ≥85% + matrix |
| Privacy scrubber catches the 11 documented patterns | 2 | catches <5 | 5–8 | 9–10 | all 11 + tested |
| `SECURITY.md` routes vuln reports privately (no public-issue path) | 2 | public path only | mixed | private path | private + 90-day window + PGP |
| CI workflows pinned to commit SHAs + dependabot upkeep | 2 | floating tags | partial pin | full pin | full pin + weekly refresh PRs |

**Score = weighted sum / 2**.

---

## Scoring procedure

1. Each axis is scored independently. The author of the rubric does
   **not** score the trust axis; that score comes from the Opus security
   audit pass (`agent-skills:security-auditor`).
2. `benchmarks/run-all.py` runs deterministic checks and emits a draft
   `BENCHMARK_REPORT.md` with the per-axis numbers and the underlying
   evidence pointers.
3. The Opus pass re-scores trust independently and may also lower any
   other axis if it finds undisclosed coverage gaps.
4. Final scores published in `docs/BENCHMARK_REPORT.md`. The rubric
   version that produced them is recorded inline.

## Versioning

This rubric is v1 (2026-06-19). Subsequent versions bump the document
header and preserve old scores under their original rubric version, so
the grading is reproducible.
