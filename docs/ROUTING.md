# Routing

Zeref includes a local routing policy for classifying work before execution.

Commands:

```bash
zeref route classify "redact credentials before release"
zeref route explain "scan benchmark claims"
zeref route policy show
zeref route policy validate
zeref route report
```

The policy is deterministic and local. It does not call hosted services or
enable agent orchestration by itself.
