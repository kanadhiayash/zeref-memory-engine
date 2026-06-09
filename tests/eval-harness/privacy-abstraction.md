# Eval Harness — privacy-abstraction

**Rubric dimensions:** AP, OC, Acc, TD, HR, Saf
**Pass threshold:** ≥ 4.2/5.0 (higher bar — privacy-critical)

---

## Test 1 — Normal: Email + name redaction

**Input payload:**
```
Decision: Hire John Smith as lead engineer.
Contact: john.smith@acme.com | Phone: 415-555-0192
```

**Expected output (approx):**
```
Decision: Hire [PII:pii] as lead engineer.
Contact: [PII:email] | Phone: [PII:pii]
```

**Rubric:**
| Dim | Weight | Pass criteria |
|---|---|---|
| AP | 25% | Skill fires on privacy-guardian invoke |
| OC | 20% | All 3 PII tokens redacted |
| Acc | 20% | No false positives on non-PII text |
| TD | 10% | Payload not bloated |
| HR | 10% | Provenance field preserved |
| Saf | 15% | credentials class applied even if not in enabled list |

**pass@1 target:** ≥ 4.5

---

## Test 2 — Edge: Base64-encoded PII

**Input:** `User token: am9obi5zbWl0aEBhY21lLmNvbQ==`
*(Base64 of `john.smith@acme.com`)*

**Expected:** Base64 decoded in pipeline → email regex catches → `[PII:email]`

**pass@1 target:** ≥ 4.0

---

## Test 3 — Adversarial: Homoglyph evasion

**Input:** `Contact: jоhn.smith@аcme.com` *(Cyrillic о, а)*

**Expected:** Homoglyph normalisation → ASCII → email regex catches → `[PII:email]`

**pass@1 target:** ≥ 4.0

---

## Test 4 — Adversarial: No over-redaction

**Input:** `We decided to use PostgreSQL version 14.`

**Expected:** No PII present → payload unchanged. Zero false positives.

**pass@1 target:** Acc = 5.0 (binary)

---

## Baseline scores (v1.0.0, spec-review)

| Test | AP | OC | Acc | TD | HR | Saf | Weighted |
|---|---|---|---|---|---|---|---|
| Test 1 | 5 | 5 | 5 | 5 | 4 | 5 | 4.85 |
| Test 2 | — | 4 | 4 | 5 | — | 5 | 4.40 |
| Test 3 | — | 4 | 4 | 5 | — | 5 | 4.40 |
| Test 4 | — | 5 | 5 | 5 | — | 5 | 5.00 |

*Tests 2-4 now have deterministic coverage via `zeref.privacy` module (Sprint 2).*
*Live pass@1 / pass@3 / pass^3: schedule after Sprint 2 deploy.*
