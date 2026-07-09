# FactGuard

FactGuard is a deterministic local scanner for unsupported public claims.

It flags:

- unsupported superlatives
- superiority claims without proof
- release-maturity claims without proof
- benchmark claims without dated reproducible evidence
- broad success claims with no named evidence
- factual claims with no source references

Commands:

```bash
zeref factguard scan README.md
zeref factguard scan docs/
zeref factguard check --claim "Zeref is ready for every team."
zeref factguard report --format md
```

FactGuard suggests safer, bounded wording instead of making marketing claims.
