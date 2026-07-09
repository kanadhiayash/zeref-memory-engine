# Getting Started

From a repo root:

```bash
python3 -m zeref --version
python3 -m zeref init --name "My Project" --privacy abstract --tier auto --parent ""
python3 -m zeref status
```

Add structured memory:

```bash
python3 -m zeref memory propose "User prefers public-safe copy by default."
python3 -m zeref memory write --from proposal.json
python3 -m zeref memory search "public-safe copy"
```

Run local gates:

```bash
python3 -m pytest -q
python3 scripts/zeref-validate.py
python3 -m zeref audit
python3 -m zeref audit-privacy --strict
python3 scripts/check-version-consistency.py
python3 benchmarks/run-all.py
git diff --check
```

Useful hardening commands:

```bash
python3 -m zeref factguard scan README.md
python3 -m zeref evidence check memory/
python3 -m zeref contradictions scan memory/
python3 -m zeref privacy scan docs/
python3 -m zeref route policy validate
python3 -m zeref release check
python3 -m zeref doctor
```

`privacy scan` is report-only by default. Use `--strict` when it should fail the
gate on findings.
