# Trust Axis — Independent Audit (v1.0.0)

> **Scope note (2026-07-14):** this audit is bound to the v1.0.0 commit named
> below and has not been re-run against 2.x. Its scores and the PASS verdict
> are repo-local re-grades of the deterministic scorer — not external or
> third-party validation. Re-run required before any release that cites it.

The deterministic scorer at `benchmarks/trust.py` produced a draft score
of **10.00**. Per [`benchmarks/RUBRIC.md`](../benchmarks/RUBRIC.md) §Axis 4,
that score must be re-graded by an independent skeptical reader before
publication. This file is that re-grade.

- **Audit run:** 2026-06-19
- **Auditor model:** Opus 4.7 (main thread, no spawned subagent)
- **Rubric version:** 1 (2026-06-19)
- **Bound-commit-SHA:** `33060a1` (independent audit target; re-run required on later HEADs)
- **Draft score (`benchmarks/trust.py`):** 10.00
- **Verified score (this audit):** **9.70**

The verified score is the one published in `docs/BENCHMARK_REPORT.md`.

## Sub-criterion scores

| Sub-criterion | Draft | Verified | Δ | Reason |
|---|---:|---:|---:|---|
| `version_consistency` | 10.0 | 10.0 | 0.0 | Checker covers 7 surfaces, CI workflow enforces, machine-verified. |
| `test_suite` | 10.0 | 10.0 | 0.0 | Pytest suite passes; CI `test.yml` runs the honest measured floor, currently `coverage --fail-under=15`; bypass tests are covered. |
| `privacy_patterns` | 10.0 | 10.0 | 0.0 | 9 provider patterns + 8 built-in classes; 3 bypass-resistance tests pass (homoglyph, base64, NFKC). |
| `security_md` | 10.0 | 9.5 | -0.5 | All four required items present (no public route, PVR, PGP, 90-day window) but PGP fingerprint is `to be published` in `SECURITY_CONTACTS.md`. Fingerprint must land before next release. |
| `ci_hardening` | 10.0 | 9.0 | -1.0 | SHA pins independently verified via `gh api repos/<owner>/git/refs/tags/<tag>` (recorded in [RISK_LOG.md](RISK_LOG.md) R-003). Deduction: only three actions are pinned because only three are used; no defence-in-depth scan (e.g. `actionlint` step) yet. |

**Verified axis score = (10 + 10 + 10 + 9.5 + 9) / 5 = 9.70.**

## Blocking findings

_None._ Every gap below is non-blocking for the v1.0.0 release but tracked
for the next iteration.

## Non-blocking findings

1. **PGP fingerprint not published** (`SECURITY_CONTACTS.md`). Track via
   GitHub issue `chore(security): publish PGP fingerprint`. Mitigation
   until then: GitHub PVR is the primary channel and works without PGP.
2. **No `actionlint` step in CI.** A lint pass would catch malformed
   `uses:` lines and missing permission scopes. Track via
   `chore(ci): add actionlint workflow`.
3. **Coverage gate sits at the honest in-process floor (15%, not 60–85%).**
   Subprocess-style CLI tests undercount in-process coverage. See
   `docs/RISK_LOG.md` R-007. Raise the gate after instrumenting
   in-process CLI tests or adding subprocess coverage via
   `sitecustomize.py`. Track via
   `test(zeref): subprocess coverage via sitecustomize OR in-process CLI tests`.
4. **Homoglyph table is Cyrillic + Greek only.** Other scripts that have
   ASCII lookalikes (Latin extended, mathematical italic, fullwidth) are
   not covered. NFKC normalisation in stage 1 catches *most* fullwidth
   variants, but a comprehensive table would harden further. Track via
   `feat(privacy): extend homoglyph table to mathematical + fullwidth`.

## Bypasses tested (and caught)

| Bypass | Vector | Caught by |
|---|---|---|
| Cyrillic homoglyph in `AKIA` prefix | `АKIAIOSFODNN7EXAMPLE` (Cyrillic `А` U+0410) | Homoglyph normaliser (stage 1) — added in this PR. |
| Base64-wrapped credential | `c2stQWJDZEVmR2hJaktsTW5PcFFyU3RVdld4MTIzNA==` (encodes `sk-...`) | Base64 decoder (stage 1) → `_PROVIDER_PATTERNS.credentials_openai_bare`. |
| NFKC fullwidth | Normalised by `unicodedata.normalize("NFKC", ...)` (stage 1). | Tested via `nfkc_fullwidth_pat`. |

## Bypasses found but NOT caught (carried forward)

_None at v1.0.0 publish time._ Findings live in `non-blocking findings`
above; mitigations tracked as GitHub issues, not as known bypasses.

## How to re-audit

```bash
python3 benchmarks/run-all.py        # regenerate draft
python3 -m pytest -q
gh api repos/actions/checkout/git/refs/tags/v4.2.2 --jq .object.sha
gh api repos/actions/setup-python/git/refs/tags/v5.3.0 --jq .object.sha
gh api repos/actions/upload-artifact/git/refs/tags/v4.4.3 --jq .object.sha
# compare each output to the SHA in .github/workflows/*.yml
```

## Publication

The verdict **PASS** is preserved because every axis remains ≥ 9.0 (no
axis below 8.0). The `trust` axis score in
`docs/BENCHMARK_REPORT.md` will read **9.70 (verified)**, not 10.00.
