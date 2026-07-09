# Release Process

Zeref releases must be evidence-based and reproducible.

## Release branch

Use:

    release/zeref__vX.Y.Z

## Required gates

Run:

    python3 -m pytest -q
    python3 scripts/zeref-validate.py
    python3 -m zeref audit
    python3 -m zeref audit-privacy --strict
    python3 scripts/check-version-consistency.py
    python3 benchmarks/run-all.py
    python3 -m zeref release check
    git diff --check

## Release notes

Release notes must include:

- Summary.
- Compatibility notes.
- Security notes.
- Benchmark scope.
- Known risks.
- Migration notes if needed.

## Tags

Use SemVer tags:

    vX.Y.Z

Do not delete tags unless there is a security, legal, or severe public-trust reason. Prefer deprecation notes over deletion.

## Benchmark claims

Allowed:

- Local deterministic benchmark gate passed.
- Fixture adapter passed.
- External benchmark run verified on a named date.

Not allowed without evidence:

- World best.
- Top ranked.
- 10/10 globally.
- Production secure.
