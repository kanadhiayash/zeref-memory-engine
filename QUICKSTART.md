<!-- privacy-audit: allow-file "Quickstart with example install / env-var / decision commands. No real user data." -->

# Zeref Memory Engine — Quickstart

5 steps from zero to first decision. Match [INSTALL.md](INSTALL.md) for the
canonical install channels.

---

## 1. Install

```bash
# From the current release (published on PyPI as `zeref-os` for URL compat, per D2):
pip install zeref-os                    # zero-dependency core
pip install "zeref-os[all]"             # with litellm, duckdb, pyyaml
```

Or from this repo:

```bash
git clone https://github.com/kanadhiayash/zeref-memory-engine
cd zeref-memory-engine
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

If input contains PII you'll see `PII scrubbed from inputs: N token(s)` — `zeref write-decision` scrubs before write.

---

## 4. Grade a Claim

```bash
zeref grade "PostgreSQL beats MongoDB for relational data"
```

Heuristic without an API key. With `litellm` + key, it's LLM-graded.

---

## 5. Audit

```bash
zeref audit-privacy --directory memory/   # PII scan
zeref audit                               # structural validation
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

---

## Next

- `AGENTS.md` — canonical spec
- `CHANGELOG.md` — release notes
- `GITHUB_OS.md` — per-repo doctrine
- `docs/wiki/` — full documentation
