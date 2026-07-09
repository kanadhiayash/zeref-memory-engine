# Audit Logs

Zeref writes append-only JSONL audit logs under `memory/audit/`.

Files:

- `writes.jsonl`
- `reads.jsonl`
- `routes.jsonl`
- `guard_failures.jsonl`
- `redactions.jsonl`
- `releases.jsonl`

Every audit event includes an event id, event type, status, actor, file,
optional memory id, guards run, reason, timestamp, and payload.

Generate a report:

```bash
zeref audit report
zeref audit report --since 2026-07-09
zeref audit report --format md
```

Corrupt JSONL lines are reported instead of crashing the report.
