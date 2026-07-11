# ZEREF_PRIOR_AUDIT_RECONCILIATION.md

Baseline: `b82c6410bf17b1bc4d1c79227c3a55e075858ab9`. Every prior claim in the handoff §Phase-4 challenge list re-tested against this SHA.

## Verdict table

| Prior ID | Prior claim | Current verdict | Evidence (this audit) | Correction to prior audit |
|---|---|---|---|---|
| PA-01 | `SOUL.md` missing | **verified** | `ls SOUL.md` → not found. AGENTS.md:21 + CLAUDE.md still reference it. | Confirmed. See `ZRF-AUDIT-015`. |
| PA-02 | Malformed CI workflow | **verified** | PyYAML `.github/workflows/ci.yml` → fails at 27-29 (`with:` dedent). See `ZRF-AUDIT-011`. | Confirmed. Whole workflow non-executing at baseline. |
| PA-03 | Private local path in tracked file | **verified + expanded** | `config/PROJECT.md:3` + `references/shared-anti-hallucination.md:89`. Two leaks, not one. See `ZRF-AUDIT-003`, `ZRF-AUDIT-004`, `ZRF-AUDIT-005`. | Prior audit undercounted by one; scanner-scope root cause identified. |
| PA-04 | Unscrubbed memory writes | **partially verified** | `MemoryWriter.write_decision` (`zeref/memory/core.py:227`) DOES scrub via `zeref.privacy.scrub`. However, LLM egress path `cmd_grade` (`cli.py:409-427`) sends raw claim unscrubbed. Not a memory-write leak but an egress leak. See `ZRF-AUDIT-001`. | Prior claim shape wrong; correct root cause is egress-path scrubbing, not memory-write scrubbing. |
| PA-05 | Unenforced network policy | **verified + expanded** | `config/PERMISSIONS.md` + `SHARING_POLICY.md` unparsed. `litellm.completion` + `urllib.request.urlopen` bypass both. See `ZRF-AUDIT-001`, `ZRF-AUDIT-002`, `ZRF-AUDIT-006`, `ZRF-AUDIT-007`, `ZRF-AUDIT-008`. | Confirmed and broken into constituent findings. |
| PA-06 | Competing canonical memory stores | **verified** | Contract graph identifies three "primary" stores (Markdown decisions, JSONL atoms, JSONL events) + derived SQLite + spec registry. No documented arbiter rule. Not resolved silently — architectural decision surfaced to owner. | Confirmed; decision withheld per Non-Negotiable #10. |
| PA-07 | Registry incompleteness | **verified + expanded** | Registry: no `agents[]`, no `commands[]`; 14 skills registered vs 15 on disk; `skill-importer` orphaned; two frontmatter schemas. See `ZRF-AUDIT-016`, `ZRF-AUDIT-017`. | Broader than prior audit stated. |
| PA-08 | Stale benchmark acceptance | **verified** | `benchmarks/run-all.py:81-117` clamps trust axis to `docs/TRUST_AUDIT.md`'s 9.70; no SHA binding. See `ZRF-AUDIT-013`. | Confirmed; commit-binding is the fix. |
| PA-09 | Missing lineage input | **verified** | `ZRF_64_repo_lineage_intake.csv` absent from tree. 10 lineage axes silently fail-open; `results.json` still records "passed: true". See `ZRF-AUDIT-012`, `ZRF-AUDIT-014`. | Confirmed; results semantics also broken. |
| PA-10 | Required version bump (v1.1.0) | **rejected as a fact; recommended as a decision** | The tag-vs-VERSION delta (`v2.6.1` on `main` vs `zeref/VERSION=1.0.0`) is real (`ZRF-AUDIT-020`). Whether the correct response is to bump to `v1.1.0` is a decision, not a defect. Prior audit conflated observation with recommendation. | Prior audit's version choice is not adopted; version number is on the council-review list. |
| PA-11 | Broken embedded installation | **verified + expanded** | `pip install .` fails at build-backend id (`ZRF-AUDIT-009`); `zeref init` doesn't produce a discoverable project (`ZRF-AUDIT-010`); `zeref init` prompts even under flags (`ZRF-AUDIT-023`). Three distinct install-path breaks. | Prior audit right on the symptom, missed the root cause (build-backend id typo). |
| PA-12 | Security reporting conflict | **verified + expanded** | Public issue templates lack security-redirect banner (`ZRF-AUDIT-026`); fallback contact self-flagged placeholder + no PGP (`ZRF-AUDIT-027`); `.github/` URLs point at two different repos (`ZRF-AUDIT-028`). Three distinct security-reporting fractures. | Confirmed; more fractures than prior audit named. |
| PA-13 | Proposed `zeref-me` compatibility identifier | **rejected** | Zero active-surface hits for `zeref-me` (WS-A `rg` sweep). Identifier appears only inside `docs/audits/ZEREF_AUDIT_BASELINE.md:87` as "proposed alias — not adopted". No consumers to migrate. The choice is architectural, not a defect. | Prior recommendation not adopted; council will consider identifier choice among {`zeref-os` retain, `zeref` rename, `zeref-me` new}. |
| PA-14 | Proposed JSONL canonical authority | **rejected as a fact; escalated as a decision** | Markdown is the current documented canon (`PRIVACY.md §4.4`, AGENTS.md core principles). JSONL is used for atoms + events + patterns. Making JSONL the canonical authority is a load-bearing architectural decision. Runtime authority is currently mixed, not JSONL. Escalated to council. | Prior audit's answer not adopted; escalated. |
| PA-15 | Proposed `v1.1.0` release number | **rejected as a fact; escalated as a decision** | The right number depends on which of `v1.0.1` (patch), `v1.1.0` (minor), `v1.0.0-hotfix` (labeled), or `v1.0.0` (re-tag) fits the intended semantics. Escalated to council. | Not silently adopted. |

## New findings not in prior audit

These are net-new to this audit (not present in the prior OODA hypothesis set):

- `ZRF-AUDIT-018` — skill count contradiction in 4 canonical texts (14 vs 10 vs 15).
- `ZRF-AUDIT-019` — team-pack count contradiction + Schema-A/B taxonomy collision + `commands/team.md` omits 4 packs.
- `ZRF-AUDIT-020` — `check-version-consistency.py` does not compare against `git tag`.
- `ZRF-AUDIT-021` — `zeref release check` misses 8+ substantive gates.
- `ZRF-AUDIT-022` — `HARNESS_MATRIX.md ✅` marks self-attested.
- `ZRF-AUDIT-024` — `QUICKSTART.md` labeled v2.5, wrong install channel.
- `ZRF-AUDIT-025` — `MIGRATION.md` commands + validator filename stale.
- `ZRF-AUDIT-029` — 6 axes miscategorized as behavioral benchmarks.
- `ZRF-AUDIT-030` — coverage floor at 15% under-signals regressions.
- `ZRF-AUDIT-031` through `ZRF-AUDIT-040` — doc drift set.

## False positives / rejected prior claims

- Adoption of `zeref-me` — no consumers found; rejected.
- Adoption of JSONL as canonical — cannot be adopted silently; escalated as decision.
- Adoption of `v1.1.0` — escalated as decision.

## Confidence classification

All 15 prior-claim rows: **high** confidence based on direct file:line evidence at baseline SHA. The three rejected-as-fact rows (PA-10, PA-13, PA-14, PA-15) are labelled as **decisions requiring owner approval** to preserve Non-Negotiable #10 (do not silently resolve product architecture decisions).
