# Security Policy — Zeref Agent OS

## Reporting Vulnerabilities

If you discover a security vulnerability in Zeref Agent OS, please report it by opening a GitHub Issue with the label `security`.

Do NOT include sensitive credentials, API keys, or access tokens in issue reports.

## Scope

Zeref Agent OS is a collection of AI agent skill definitions (Markdown files) and supporting scripts. Security concerns include:

- Prompt injection risks in skill definitions
- Trust sentinel bypass patterns
- Unsafe self-modification (skill_updater.py approval gate bypass)
- Irreversible action execution without user confirmation

## Safety Principles

See `references/zeref-safety-principles.md` for the full constitutional safety framework.

Key rules:
1. Trust sentinel must classify untrusted content before routing
2. skill_updater.py only applies changes where `"approved": true`
3. Irreversible actions always require explicit user confirmation
4. Council convener (Opus 4.7) requires cost warning before activation

## Contact

Maintainer: Yash Kanadhia — https://github.com/kanadhiayash
