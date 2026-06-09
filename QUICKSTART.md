# Zeref OS — Quickstart (v2.5)

5 steps from zero to first decision.

---

## 1. Install

```bash
pipx install zeref-os                    # zero-dependency core
pipx install "zeref-os[all]"             # with litellm, duckdb, pyyaml
```

Or from this repo:

```bash
git clone https://github.com/kanadhiayash/zeref-os
cd zeref-os
pip install -e .
```

Verify:
```bash
zeref --help
zeref db-status          # shows backend availability
```

---

## 2. Initialise a Project

```bash
cd ~/my-project
zeref init --name "My Project" --privacy abstract --tier auto --parent ''
```

Scaffolds:
- `config/PROJECT.md`
- `PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md`
- `config/BUDGET.md`
- `memory/` flat layout (`hot.md`, `index.md`, `DECISIONS.md`, ...)
- `skills/drafts/`

Inspect:
```bash
zeref status
```

---

## 3. Write Your First Decision

```bash
zeref write-decision \
  --title "Use PostgreSQL for relational workloads" \
  --why "Better transactional guarantees than MongoDB" \
  --evidence "internal benchmark 2026-06-01" \
  --grade high
```

If input contains PII you'll see `PII scrubbed from inputs: N token(s)` — v2.5 L11 scrubs before write.

---

## 4. Grade a Claim

```bash
zeref grade "PostgreSQL beats MongoDB for relational data"
```

Heuristic without an API key. With `litellm` + key, it's LLM-graded.

---

## 5. Audit + Demo

```bash
zeref audit-privacy --directory memory/   # PII scan
zeref audit                               # structural validation
zeref demo                                # 20 deterministic checks
zeref dashboard                           # HTML chart → tests/dashboard.html
```

---

## Daily Loop

```bash
zeref status            # session start
# ...work...
zeref write-decision    # capture each decision
zeref grade <claim>     # grade open questions
# /done in harness consolidates hot.md
```

---

## Cheat Sheet

| Command | Purpose |
|---|---|
| `zeref init` | Scaffold new project |
| `zeref status` | hot.md + tier + registry |
| `zeref write-decision` | Append to DECISIONS.md (scrubs PII) |
| `zeref grade <claim>` | Evidence grader |
| `zeref audit-privacy` | Scan for PII hits |
| `zeref audit` | Structural validation |
| `zeref db-status` | Backend availability |
| `zeref dashboard` | Regenerate HTML chart |
| `zeref demo` | 20 regression checks |

---

## Next

- `AGENTS.md` — canonical spec
- `SOUL.md` — 6 operating principles
- `tests/zeref-rubric-v2.5.md` — current scorecard (8.0/10)
- `tests/security-audit-vC.md` — security findings + fixes
