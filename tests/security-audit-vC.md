# Phase C — Security + Vulnerability Audit

**Date:** 2026-06-04 | **Method:** Live exploit execution against zeref/privacy.py, scripts/zeref-validate.py, writers, SHARING_POLICY, pattern-to-skill review gate
**Scope:** 8 attack surfaces + 4-vuln sweep follow-up

---

## Executive Summary

| Severity | Count | IDs |
|---|---|---|
| **CRITICAL** | **2** | V01 homoglyph bypass, V02 base64 bypass |
| **HIGH** | **3** | V06 single-writer race, V07 no override gate, V12 write-decision unscrubbed |
| MEDIUM | 1 | V08 pattern-to-skill review gate untested |
| LOW | 0 | — |
| PASSED | 3 | V03 double-base64, V04 credentials always-on, V05 validator catches corruption |

**Exit criterion:** Zero CRITICAL.
**Actual:** **2 CRITICAL — FAILS exit. Phase D must close before Phase E claims "secure."**

---

## V01 — CRITICAL — Homoglyph Bypass on Email

**CVSS:** 7.5 (High) — `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`
**Surface:** `zeref/privacy.py::scrub()` homoglyph stage
**Attack:** `Email me at jоhn@аcme.com (cyrillic о/а)`
**Expected:** Cyrillic → ASCII → email regex → `[PII:email]`
**Actual:** Homoglyphs normalised but **0 tokens redacted** — `john@acme.com` survives in output.

**Root cause:** REDACT.md default has only `credentials, pii, internal_paths` enabled. `email` class disabled. `pii` regex needs Firstname-Lastname pattern; bare `john@acme.com` doesn't match.

**Fix (Phase D L2):** Enable `email` class default. Re-run ATTACK 1 → must show `[PII:email]`.

---

## V02 — CRITICAL — Base64-Encoded PII Survives

**CVSS:** 6.5 (Medium-High)
**Attack:** `Decoded: am9obkBldmlsLmNvbQ==` (base64 of `john@evil.com`)
**Expected:** Decode → email regex → redact
**Actual:** Decoded plaintext appears in output; email class disabled → no redaction.

**Root cause:** Same as V01.

**Fix:** Same as V01. Also verify decode-then-rescan pipeline order in `scrub()`.

---

## V03 — PASS — Double-Base64

Triple-nested `b64(b64(pii))` — pipeline decodes one layer only. Acceptable; document as known limitation.

---

## V04 — PASS — Credentials Always-On

Malicious REDACT.md with all classes `enabled: false` including `credentials` — `OPENAI_API_KEY=sk-1234...` STILL redacted to `OPENAI_[PII:credentials]`. Code path honours always-on rule. ✔

---

## V05 — PASS — Validator Catches Corruption

Corrupt `skills/wiki-maintenance/SKILL.md` frontmatter → validator exits 1 with `missing frontmatter key 'description'`. ✔

---

## V06 — HIGH — Single-Writer Race Confirmed (K4)

**CVSS:** 5.3
**Attack:** Two threads × 50 appends each to `/tmp/race-decisions.md`
**Result:** Both completed 100 writes; no lock, no abort. **K4 confirmed.**

**Real-world risk:** `wiki-maintenance` post-write racing `contradiction-resolution` queue on `DECISIONS.md` / `CONFLICTS.md` → torn writes.

**Fix (Phase D L9):** Advisory `memory/.lock` sentinel. Before write, check + abort if held.

---

## V07 — HIGH — No Permission Override Gate

**CVSS:** 6.5
**Surface:** `SHARING_POLICY.md`, `config/PERMISSIONS.md`
**Finding:** Spec requires "explicit user approval" for session overrides; zero enforcement code.

**Real-world risk:** Privilege escalation if harness honours mid-session policy rewrite without confirmation.

**Fix:** Defer to v2.6 unless ranked critical. Sentinel: `memory/.session-perms.json` captures approved set at `/start`; mismatch at tool-call surfaces confirmation.

---

## V08 — MEDIUM — pattern-to-skill Review Gate Untested

**By spec:** Drafts land in `skills/drafts/`, NOT auto-loaded; `/review-skill` gates. PASS by design.
**By exercise:** `skills/drafts/` empty. Flow never run end-to-end (Phase A K10).

**Fix (Phase D L8):** Inject synthetic pattern, verify draft + PROVENANCE.md.

---

## V09-V12 — Sweep

| ID | Surface | Result |
|---|---|---|
| V09 | YAML parse of blank `config/PROJECT.md` | NO crash (PASS) |
| V10 | dict-of-dicts vs list-of-dicts in `SHARING_POLICY.md` | Fix retroactive from Sprint 2 (PASS) |
| V11 | Concurrent CONFLICTS.md append | Same race as V06 — covered by L9 |
| V12 | `zeref write-decision` writes title+rationale+evidence WITHOUT calling `scrub()` | **HIGH** — PII in input lands on disk unscrubbed |

**V12 fix (new L11):** Call `zeref.privacy.scrub()` on all `write-decision` inputs before disk write.

---

## Fix Map → Phase D

| Vuln | Workaround | Phase D ID |
|---|---|---|
| V01, V02 | Enable `email` class in REDACT.md | L2 |
| V06, V11 | Advisory `.lock` sentinel | L9 |
| V08 | Live-test draft flow | L8 |
| V12 | Scrub on `write-decision` | **L11 (new)** |
| V07 | Permission override sentinel | defer to v2.6 |
| Recovery dim 3.93 | Atomic .tmp+rename writes | L10 (Phase B finding) |

---

## Hand-off to Phase D

**Priority order:**
1. **L2 (email default)** → closes V01, V02 (both CRITICAL)
2. **L9 (lock sentinel)** → closes V06, V11
3. **L11 (write-decision scrub)** → closes V12
4. **L1 (regex tighten)** → reinforces V01 + closes Phase A L1
5. **L10 (atomic writes)** → closes Phase B Recovery gap
6. **L5 + L6** → closes K1 + K3
7. **L3, L4, L7, L8** → round-out

**Phase D exit:** Zero open CRITICAL. Re-run ATTACK 1, 2, 6 must PASS.
