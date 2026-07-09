# FactGuard

FactGuard is a deterministic local scanner for unsupported public claims.

It flags:

- unsupported superlatives
- best-in-class or "beats every tool" claims
- production-ready claims without proof
- benchmark claims without dated reproducible evidence
- broad success claims such as "all gates pass"
- factual claims with no source references

Commands:

```bash
zeref factguard scan README.md
zeref factguard scan docs/
zeref factguard check --claim "Zeref is production-ready."
zeref factguard report --format md
```

FactGuard suggests safer, bounded wording instead of making marketing claims.
