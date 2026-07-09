# Zeref v1.1 Hardening Overview

Zeref v1.1 hardening turns the project from a Markdown-only continuity layer
into a local-first memory hardening layer.

The core rule stays the same: product commands do not call hosted services, do
not sync by default, and do not claim external benchmark performance without
dated reproducible evidence.

## Surfaces

- Memory model: [`docs/MEMORY_MODEL.md`](MEMORY_MODEL.md)
- Guarded writes: [`docs/MEMORY_WRITES.md`](MEMORY_WRITES.md)
- Audit logs: [`docs/AUDIT_LOGS.md`](AUDIT_LOGS.md)
- FactGuard: [`docs/FACTGUARD.md`](FACTGUARD.md)
- EvidenceGuard: [`docs/EVIDENCEGUARD.md`](EVIDENCEGUARD.md)
- ContradictionGuard: [`docs/CONTRADICTIONGUARD.md`](CONTRADICTIONGUARD.md)
- PrivacyGuard: [`docs/PRIVACYGUARD.md`](PRIVACYGUARD.md)
- Routing: [`docs/ROUTING.md`](ROUTING.md)
- Release gates: [`docs/RELEASE_GATES.md`](RELEASE_GATES.md)
- Doctor: [`docs/DOCTOR.md`](DOCTOR.md)
- Benchmark adapters: [`docs/BENCHMARK_ADAPTERS.md`](BENCHMARK_ADAPTERS.md)
- Public-safe copy: [`docs/PUBLIC_SAFE_COPY.md`](PUBLIC_SAFE_COPY.md)

## Release Position

Safe public wording:

> Zeref is a local-first memory hardening layer for AI agents.

Do not describe fixture adapter status as full external-dataset verification.
Do not describe benchmark status as ranking performance.
