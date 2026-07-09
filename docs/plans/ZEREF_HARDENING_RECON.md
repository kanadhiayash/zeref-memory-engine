# Zeref Hardening Recon

## Facts

- Existing CLI entry point: `zeref/cli.py`, exposed through `pyproject.toml` as `zeref = "zeref.cli:main"`.
- Existing package manager: Python packaging via `pyproject.toml`; core runtime is stdlib-only.
- Existing test command: `python3 -m pytest -q`.
- Existing validation commands: `python3 scripts/zeref-validate.py`, `python3 -m zeref audit`, `python3 -m zeref audit-privacy --strict`, `python3 scripts/check-version-consistency.py`, `python3 benchmarks/run-all.py`.
- Existing memory folder: root `memory/` ships as an empty scaffold with `memory/README.md`; initialized projects use the flat `memory/` layout from `zeref/memory.py`.
- Existing docs folder: `docs/` plus `docs/wiki/`; benchmark report, trust audit, release log, risk log, and retrieval benchmark docs already exist on the current stack.
- Existing guard modules: `zeref/privacy.py` provides deterministic privacy scrubbing and read-only audit; no dedicated `zeref/guards/` package exists yet.
- Existing audit modules: structural audit is currently the `zeref audit` wrapper around `scripts/zeref-validate.py`; no append-only `zeref/audit/` package exists yet.
- Existing memory core: current stack includes `zeref/memory.py` for layout/writes and `zeref/memory_state.py` for SQLite-backed structured state, FTS5 search, Markdown views, layers, and state events.
- Existing benchmark core: current stack includes `benchmarks/retrieval.py`, `benchmarks/run-all.py`, and `docs/RETRIEVAL_BENCHMARKS.md`.

## Assumptions

- The hardening release continues from `test/zeref__retrieval-benchmarks`.
- Stacked PRs remain the review shape.
- The CLI stays in `zeref/cli.py`; new command groups are added without a CLI package refactor.
- Product commands remain local-first and do not perform network calls.
- Benchmark adapters may be added, but default tests use offline fixtures only.

## Unknowns

- Whether all previous stacked PRs will merge before this hardening stack lands.
- Whether benchmark adapter full-dataset runs will be executed outside default CI.
- Whether v1.1 will keep package metadata as `zeref-os` for install compatibility or rename in a later release.

## Risks

- The current stack already includes benchmark work, while the original pasted hardening brief marked benchmarks as a non-goal; latest user direction permits full benchmark work.
- Public docs still contain v1.0.0 positioning and benchmark language that FactGuard may flag.
- Adding many command groups to one argparse file can make `zeref/cli.py` large; keep command handlers thin and delegate behavior to modules.
- Existing initialized projects may have older SQLite state; schema changes must be additive.
- Release checks must not make external calls or require full benchmark datasets.

## Recommended Implementation Path

- Add small subsystem modules under `zeref/core`, `zeref/guards`, `zeref/audit`, `zeref/routing`, and `zeref/release`.
- Extend `zeref/memory_state.py` for memory-card persistence instead of creating a second memory store.
- Use append-only JSONL audit logs under `memory/audit/`.
- Implement guard command groups in `zeref/cli.py` as thin wrappers.
- Keep benchmark adapters fixture-first and clearly mark non-verified external datasets.
- Update public docs only after command behavior and guards are implemented.
