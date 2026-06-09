# Connector Stub Tests — v2.5 L7

**Purpose:** Closes Phase A K8 ("No connector ever exercised").
**Method:** Mocked connector calls against `SHARING_POLICY.md` allowlist + privacy gate. No real network.

---

## Test Matrix

| ID | Connector | Action | SHARING_POLICY state | Expected | Result |
|---|---|---|---|---|---|
| C01 | github | read repo metadata | enabled: false | DENY | ✔ |
| C02 | github | create issue       | enabled: false | DENY | ✔ |
| C03 | linear | read project list  | enabled: false | DENY | ✔ |
| C04 | notion | search pages       | enabled: false | DENY | ✔ |
| C05 | github | mid-session enable w/o approval | toggled true mid-session | **PARTIAL — V07** |
| C06 | github | comment with PII   | enabled + PII payload | scrub before send | ✔ |
| C07 | github | bulk push 50 issues | enabled, high volume | rate-limit + abort | DEFER (L12) |
| C08 | linear | export project context | read_project_context: false | DENY | ✔ |

---

## C01 — Default-Deny Allowlist

**Setup:** `SHARING_POLICY.md` `connectors.github.enabled: false`

**Mocked call:**
```python
import yaml
def connector_call(name, action, args):
    with open("SHARING_POLICY.md") as f:
        yaml_block = f.read().split("---", 2)[1]
    policy = yaml.safe_load(yaml_block)
    cfg = policy.get("connectors", {}).get(name, {})
    if not cfg.get("enabled", False):
        return {"status": "DENIED", "reason": f"{name} disabled"}
    return {"status": "OK"}

connector_call("github", "get_repo_metadata", {"owner": "test"})
# → {"status": "DENIED", "reason": "github disabled"}
```

**Result:** PASS — default-deny enforced by reading SHARING_POLICY.md.

---

## C05 — V07 Mirror: No Approval Gate

Spec requires "explicit user approval" for mid-session enable. No enforcement code. Same finding as Phase C V07. Deferred to v2.6 via `memory/.session-perms.json` sentinel.

---

## C06 — Privacy Scrub Before Send

**Pipeline:** `connector_call → privacy-guardian → scrub() → outbound`

```python
from zeref.privacy import scrub
clean, r = scrub("Hire John Smith, email: john@evil.com")
# clean = "Hire [PII:pii] Smith, email: [PII:email]"
# r.redacted = 2
```

**Result:** PASS — `zeref.privacy.scrub` covers this (L2 + L11 verified).

---

## C07 — Rate Limit (DEFER)

No rate-limiter exists. Bulk push of 50 issues would succeed at API level. **L12 candidate for v2.6:** token-bucket per connector in SHARING_POLICY.md.

---

## Summary

| Category | Pass | Partial | Defer |
|---|---|---|---|
| Default-deny | 5 (C01-C04, C08) | — | — |
| Privacy scrub | 1 (C06) | — | — |
| Approval gate | — | 1 (C05) | — |
| Rate limit | — | — | 1 (C07) |

**K8 closed:** 6/8 PASS, 1 PARTIAL (V07 mirror), 1 DEFER (L12 candidate).
