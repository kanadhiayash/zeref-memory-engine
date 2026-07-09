# Zeref Memory Engine

Local-first memory for AI-assisted work.

Zeref gives AI tools a project memory they can read first, write to safely, and hand off cleanly. It is not a hosted service, not an operating system, and not a model provider. It is a repo-native memory layer that keeps project context, decisions, risks, contradictions, evidence, and handoffs close to the code.

## What Zeref does

Zeref helps AI sessions avoid starting from zero.

It provides:

- A canonical `AGENTS.md` for agent and harness behavior.
- Local project memory under `memory/`.
- Privacy-first write rules.
- Guarded memory writes.
- Evidence, fact, contradiction, and privacy checks.
- Append-only audit logs.
- Cross-harness handoff files.
- Deterministic local benchmark gates.
- Fixture-first benchmark adapters for external memory benchmarks.

## What Zeref is not

- Not an operating system.
- Not a hosted service.
- Not a vector database.
- Not a replacement for human review.
- Not a claim of external benchmark leadership.
- Not bundled with third-party connectors by default.

## Core guarantees

| Guarantee | Meaning |
|---|---|
| Local-first | Memory lives in the project by default. |
| Harness-agnostic | Claude Code, Codex, Cursor, Gemini, Aider, Windsurf, and other tools can point to the same project memory. |
| Privacy-first | Defaults avoid external sharing unless explicitly allowed. |
| Evidence-disciplined | Facts, assumptions, unknowns, and risks are separated. |
| Human arbitration | Contradictions are surfaced, not silently resolved. |
| Audit-friendly | Writes and guard events are logged in append-only local files. |
| Benchmark-gated | Release readiness depends on deterministic local checks. |

## Install

Clone Zeref into a project:

    git clone https://github.com/kanadhiayash/zeref-memory-engine.git .zeref

Point your AI harness at:

    .zeref/AGENTS.md

For Claude Code plugin compatibility, the legacy `zeref-os` identifier may still appear in install paths. The product name is Zeref Memory Engine.

Full install instructions live in [`INSTALL.md`](INSTALL.md).

## Quickstart

From the repo root:

    python3 -m zeref --version
    python3 -m zeref status
    python3 scripts/zeref-validate.py
    python3 -m pytest -q
    python3 benchmarks/run-all.py

For local setup and verification, read [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md).

## Memory model

Zeref uses a project-local memory layout:

    memory/
      hot.md
      index.md
      MEMORY.md
      DECISIONS.md
      OPEN_QUESTIONS.md
      RISKS.md
      CONFLICTS.md
      state/
      views/
      audit/
      archive/
      patterns/
      snapshots/
      sync/
      raw/

Markdown remains human-auditable. Structured local state supports search, recall, history, and explanation.

## Guarded writes

Memory writes can pass through:

- FactGuard
- EvidenceGuard
- PrivacyGuard
- ContradictionGuard

Rejected writes produce actionable feedback. Accepted writes are stored with local audit traces.

## Privacy and security

Zeref defaults to conservative privacy behavior.

| File | Purpose |
|---|---|
| [`PRIVACY.md`](PRIVACY.md) | Privacy mode. Default is `abstract`. |
| [`REDACT.md`](REDACT.md) | Sensitive classes and redaction rules. |
| [`SHARING_POLICY.md`](SHARING_POLICY.md) | Connector and external sharing policy. |
| [`SECURITY.md`](SECURITY.md) | Vulnerability reporting policy. |

Security issues should be reported privately. Do not open public issues for vulnerabilities.

## Benchmarks

Zeref includes deterministic local benchmark gates and fixture-first adapters for external memory benchmark formats.

Current benchmark reports are local and repo-scoped. They are not public leaderboard claims.

Read:

- [`benchmarks/RUBRIC.md`](benchmarks/RUBRIC.md)
- [`docs/BENCHMARK_REPORT.md`](docs/BENCHMARK_REPORT.md)
- [`docs/BENCHMARK_ADAPTERS.md`](docs/BENCHMARK_ADAPTERS.md)
- [`docs/RELEASE_GATES.md`](docs/RELEASE_GATES.md)

## Documentation

| Document | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Canonical agent and harness behavior. |
| [`INSTALL.md`](INSTALL.md) | Install instructions. |
| [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md) | Local setup and verification. |
| [`docs/HARDENING_OVERVIEW.md`](docs/HARDENING_OVERVIEW.md) | Hardening surfaces. |
| [`docs/RELEASE_GATES.md`](docs/RELEASE_GATES.md) | Release readiness checks. |
| [`docs/PUBLIC_SAFE_COPY.md`](docs/PUBLIC_SAFE_COPY.md) | Public claim rules. |
| [`docs/RISK_LOG.md`](docs/RISK_LOG.md) | Known risks and mitigations. |
| [`docs/TRUST_AUDIT.md`](docs/TRUST_AUDIT.md) | Trust posture notes. |
| [`docs/archive/README.md`](docs/archive/README.md) | Public-safe archive index. |

## Contributing

Open an issue before large changes. Keep PRs focused. Security issues must be reported privately.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT. Bring your own models, harnesses, and workflows. No warranty.
