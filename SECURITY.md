# Security Policy — Zeref OS

## Reporting a Vulnerability

**Do not open a public GitHub issue for a security vulnerability.** Public
issues are indexed and visible to anyone before a fix is available.

Use one of the private channels below.

### Preferred: GitHub Private Vulnerability Reporting

1. Go to the **Security** tab of
   [`kanadhiayash/zeref-os`](https://github.com/kanadhiayash/zeref-os/security).
2. Click **Report a vulnerability**.
3. Fill in the form with:
   - a clear description of the issue,
   - reproduction steps or a proof-of-concept (redact your own secrets first),
   - the affected version (`zeref --version`),
   - the harness you observed it in (Claude Code / Cursor / Aider / …),
   - your assessment of impact.

GitHub routes the report to the maintainer privately. You will get an
acknowledgement within **3 business days** and a triage verdict within
**10 business days**.

### Fallback: encrypted email

If GitHub PVR is unavailable, email the maintainer at the address listed in
`SECURITY_CONTACTS.md`. Encrypt the body with the PGP public key whose
fingerprint is published in the same file. Plain-text email is acceptable for
**triage only** — do not include credentials, PoC payloads, or victim data
in cleartext.

### What to put in the report

- A description of the vulnerability and its security impact.
- The version of Zeref OS affected (output of `python3 -m zeref --version`).
- A minimal reproduction.
- Any suggested mitigation if you have one.

### What **not** to include

- Real production secrets (rotate them first; report with redacted examples).
- Personally identifying data about third parties.
- Material covered by NDA without explicit authorisation.

## Coordinated Disclosure

Zeref OS uses a **90-day coordinated disclosure** window from the date the
report is acknowledged. If a fix is not yet published at day 90, we will
publish a public advisory with mitigation guidance and continue working
toward a patch. If you need a different window, say so in the report and we
will discuss it.

We will:

1. Acknowledge your report (≤ 3 business days).
2. Triage and confirm or reject (≤ 10 business days).
3. Develop and test a fix on a private branch.
4. Coordinate a release date with you.
5. Publish a fixed version and a CVE / GitHub Security Advisory.
6. Credit you in the advisory (unless you ask to remain anonymous).

## Scope

Zeref OS is a collection of AI agent skill definitions (Markdown files), a
Python reference runtime, and supporting scripts. In-scope issues include:

- Prompt-injection paths through skill definitions that bypass the
  Auto-Activation Gates.
- Trust-sentinel bypass patterns in `prompt-context-engine`.
- Privacy scrubber regressions — patterns that *should* redact but don't.
- Unsafe self-modification (`pattern-to-skill` approval-gate bypass).
- Irreversible action execution without explicit user confirmation.
- Credential leakage through any persisted file under `memory/`.
- Supply-chain risks in workflow definitions (`.github/workflows/`).
- Code execution paths in `zeref/cli.py` triggered by malformed
  `REDACT.md` / `PRIVACY.md` / `SHARING_POLICY.md`.

Out of scope:

- Issues against forks or vendor harnesses (report to the harness vendor).
- Reports that require local administrative access to the user's machine.
- "Vulnerabilities" demonstrated only by editing the project's own
  configuration files (e.g. setting `PRIVACY.md` to `exact` and then
  reporting that secrets persist — that's the documented behaviour).

## Safety Principles

See [`references/zeref-safety-principles.md`](references/zeref-safety-principles.md)
for the full safety framework. Key rules:

1. Untrusted content must be classified by the trust sentinel before
   routing.
2. `pattern-to-skill` only writes drafts; activation requires explicit
   user review via `/review-skill`.
3. Irreversible actions always require explicit user confirmation.
4. Opus-tier activations require a cost acknowledgement before the spend.

## Public advisories

Published advisories will live at
<https://github.com/kanadhiayash/zeref-os/security/advisories>.

## Contact

- GitHub Private Vulnerability Reporting (preferred).
- Encrypted email — see [`SECURITY_CONTACTS.md`](SECURITY_CONTACTS.md).
- Maintainer: Yash Kanadhia — <https://github.com/kanadhiayash>.
