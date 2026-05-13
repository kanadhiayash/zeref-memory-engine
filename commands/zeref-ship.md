---
description: Pre-ship checklist. Runs final executive review on any deliverable before it leaves the workspace. Checks completeness, hallucination risk, positioning alignment, and professional quality.
---
Run a pre-ship executive review on `$ARGUMENTS` (required: `deliverable`). Produce a review report with:

1. **Completeness Check** — are all expected sections present? Any missing context?
2. **Hallucination Risk** — any claims that look invented, unverifiable, or unsupported?
3. **Positioning Alignment** — does the tone and register match the `audience` and `destination`?
4. **Professional Quality Score** — is this portfolio / recruiter / client ready?
5. **Specific Revision Notes** — if anything needs fixing, list exact revisions with locations

End with a verdict: **PASS** (ship as-is), **REVISE** (minor fixes needed — list them), or **BLOCK** (do not ship — major issue found).

Default quality bar is `professional`. If `quality_bar=portfolio`, apply the highest standard.
