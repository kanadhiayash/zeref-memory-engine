# Changelog — Zeref OS

All notable changes to **Zeref OS** are documented here.

Versioning: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.

Full pre-rebrand history (Skills Fleet → Agent OS → Zeref 4.x) is preserved in [`CHANGELOG-LEGACY.md`](CHANGELOG-LEGACY.md).

---

## [1.0.0] — 2026-05-31

> **Canonical release. The first release under the Zeref OS name.**
>
> Years of local iteration (v1.x Skills Fleet → v2.x Agent OS → v3.x specialist build → v4.x context-and-memory engine) converge here. The plugin is renamed, the version clock resets, and the project takes its final form.

### Renamed

- Plugin: `zeref` → `zeref-os` (`.claude-plugin/plugin.json`, `marketplace.json`, `SKILL.md`)
- Display identity: "Zeref 4.x" → **Zeref OS** across all docs, agents, skills, commands, team packs, references, harness stubs, memory dogfood
- Slash command namespace: `/zeref:<command>` → `/zeref-os:<command>` (auto-derived from plugin name)
- Skill invocation: `zeref:<name>` → `zeref-os:<name>` (auto)
- Script: `scripts/zeref-validate-v4.py` → `scripts/zeref-validate.py`
- Changelog: prior history preserved at `CHANGELOG-LEGACY.md`

### Reset

- Version: `4.3.0` → `1.0.0` in `plugin.json`, `marketplace.json`, `SKILL.md`
- All other tags purged (v1.1 / v2.0 / v2.1 / v3.0.0 / v4.0.0 / v4.1.0 / v4.2.0 / v4.3.0) — single tag `v1.0.0` from this commit forward
- All branches purged except `main`

### Added (over the v4.3 baseline)

- **`assets/zeref-os-hero.png`** + **`assets/zeref-os-icon.png`** — pixel-art hero (hooded dark mage with floating ancient tomes) and square icon for repo avatar
- **README** rewritten: hero image, inspiration narrative (Fairy Tail's Zeref Dragneel), journey table tracing every iteration since v1.x, mermaid architecture + sequence diagrams, decision-log highlights, engineering inspirations from the wider community (AGENTS.md standard, Karpathy paradigm shifts, BMAD-METHOD, GitHub Spec Kit, Anthropic CLAUDE.md guides, claude-evolve, obsidian-PKM, and others)
- **GitHub Wiki** (12 pages): Home, Installation, Architecture, Memory Model, Privacy Model, Team Packs, Pattern Detection, Decision Log, Model Debates, Versioning History, FAQ, Glossary, Inspirations

### Preserved unchanged from v4.3.0

- All capability surface (6 agents, 10 skills, 8 commands, 6 team packs)
- Flat `memory/` layout
- Root `PRIVACY.md` + `REDACT.md` + `SHARING_POLICY.md`
- `references/v4x-canon/` — imported design canon left as historical reference
- Migration script `scripts/migrate-v4.2-to-v4.3.py` — kept for any users migrating from prior local v4.x installs

### Breaking changes

- **Plugin install command changed.** Existing `zeref@zeref` installs must:
  ```bash
  claude plugin uninstall zeref@zeref
  claude plugin install zeref-os@zeref-os
  ```
- Slash commands now under `/zeref-os:` namespace.
- Skills invoke as `zeref-os:<name>` via the Skill tool.

No data migration required — all memory files (`memory/`, `PRIVACY.md`, `REDACT.md`, `SHARING_POLICY.md`, `config/`) keep their paths and content.

---

For the full history before v1.0.0 (Zeref Skills Fleet v1.x, Zeref Agent OS v2.x, Zeref OS v3.x, Zeref 4.0–4.3 context-and-memory engine), see [`CHANGELOG-LEGACY.md`](CHANGELOG-LEGACY.md).
