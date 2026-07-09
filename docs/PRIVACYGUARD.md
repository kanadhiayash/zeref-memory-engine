# PrivacyGuard

PrivacyGuard exposes the existing deterministic scrubber as a first-class guard
surface.

It can scan project files, classify text, and print suggested redactions without
making external calls. Product commands remain local-first.

Commands:

```bash
zeref privacy scan docs/
zeref privacy classify "public-safe copy"
zeref privacy redact docs/example.md --suggest
zeref privacy report --format json
```

Credential-shaped material is classified as `secret` and blocks guarded memory
writes. Other sensitive classes should be abstracted before public release.
