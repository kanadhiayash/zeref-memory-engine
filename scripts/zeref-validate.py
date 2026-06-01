#!/usr/bin/env python3
"""
zeref-validate.py — Validate Zeref OS plugin structure.

Checks:
- Root manifests (SKILL.md, AGENTS.md, CLAUDE.md, GEMINI.md)
- Root privacy templates (PRIVACY.md, REDACT.md, SHARING_POLICY.md)
- config/ has required files
- memory/ scaffold complete (flat layout)
- skills/ has expected inventory (10 dirs, each with SKILL.md + valid frontmatter)
- agents/ has 6 agents with valid frontmatter
- commands/ has 8 commands (/start /done /stop /status /sync-parent /reset-permissions /review-skill /team)
- team-packs/ has 6 packs
- references/v4x-canon/ has 6 design docs (historical reference)
- harness stubs present (.cursor/rules/zeref.mdc, .windsurfrules, .aider.conf.yml.example)
- plugin.json + marketplace.json present and valid JSON
- Deprecation warning if legacy memory/wiki/ still has live content

Exit 0 on pass, 1 on fail.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXPECTED = {
    "root_manifests": ["SKILL.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md"],
    "root_privacy": ["PRIVACY.md", "REDACT.md", "SHARING_POLICY.md"],
    "config": ["PROJECT.md", "PERMISSIONS.md", "PARENT_SYNC.md", "BUDGET.md", "claude-overrides.md"],
    "memory_dirs": ["raw", "snapshots", "sync/outbound", "sync/parent", "archive", "patterns"],
    "memory_flat": ["hot.md", "index.md", "MEMORY.md", "DECISIONS.md", "OPEN_QUESTIONS.md", "RISKS.md", "CONFLICTS.md"],
    "skills": [
        "project-setup", "wiki-maintenance", "contradiction-resolution",
        "privacy-abstraction", "parent-sync", "pattern-to-skill",
        "memory-import-export", "budget-governor", "handoff-compiler", "evidence-grader",
    ],
    "agents": [
        "memory-keeper.md", "privacy-guardian.md", "sync-coordinator.md",
        "evidence-curator.md", "pattern-observer.md", "handoff-orchestrator.md",
    ],
    "commands": [
        "start.md", "done.md", "stop.md", "status.md",
        "sync-parent.md", "reset-permissions.md", "review-skill.md", "team.md",
    ],
    "team_packs": ["solo.md", "build.md", "research.md", "red.md", "audit.md", "ship.md"],
    "v4x_canon": [
        "ZEREF_OS.md", "DECISION_LOG.md", "MODEL_DEBATE.md",
        "USE_CASES.md", "RESEARCH_RESOURCES.md", "PACKAGE_INDEX.md",
    ],
    "harness_stubs": [".cursor/rules/zeref.mdc", ".windsurfrules", ".aider.conf.yml.example"],
    "plugin_manifests": [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"],
}

errors = []
warnings = []


def check_file(path, label):
    if not (ROOT / path).is_file():
        errors.append(f"missing {label}: {path}")


def check_dir(path, label):
    if not (ROOT / path).is_dir():
        errors.append(f"missing {label} dir: {path}")


def check_yaml_frontmatter(path, required_keys):
    p = ROOT / path
    if not p.is_file():
        errors.append(f"missing: {path}")
        return
    text = p.read_text()
    if not text.startswith("---"):
        errors.append(f"{path}: no YAML frontmatter")
        return
    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{path}: frontmatter not closed")
        return
    fm = text[4:end]
    for k in required_keys:
        if f"{k}:" not in fm:
            errors.append(f"{path}: missing frontmatter key '{k}'")


def main():
    # Root manifests
    for f in EXPECTED["root_manifests"]:
        check_file(f, "root manifest")

    # Root privacy templates (per ZEREF_OS §4.1)
    for f in EXPECTED["root_privacy"]:
        check_file(f, "root privacy template")

    # config/
    for f in EXPECTED["config"]:
        check_file(f"config/{f}", "config")

    # memory/ — flat layout per ZEREF_OS §12
    for d in EXPECTED["memory_dirs"]:
        check_dir(f"memory/{d}", "memory")
    for f in EXPECTED["memory_flat"]:
        check_file(f"memory/{f}", "memory (flat)")
    check_file("memory/patterns/PATTERNS.jsonl", "patterns log")

    # Deprecation warning if old memory/wiki/ still has live content
    wiki_dir = ROOT / "memory" / "wiki"
    if wiki_dir.is_dir():
        live = [p for p in wiki_dir.rglob("*")
                if p.is_file() and p.name not in (".gitkeep", "README-MOVED.md")]
        if live:
            warnings.append(
                f"memory/wiki/ still has {len(live)} file(s) — "
                f"run scripts/migrate-v4.2-to-v4.3.py --apply"
            )

    # skills/ — validate expected dirs, allow extras under drafts/
    for s in EXPECTED["skills"]:
        check_dir(f"skills/{s}", "skill")
        check_yaml_frontmatter(f"skills/{s}/SKILL.md", ["name", "description"])
    # drafts/ is intentional — pattern-to-skill writes here; not active skills
    drafts_dir = ROOT / "skills" / "drafts"
    if drafts_dir.is_dir():
        draft_count = sum(1 for d in drafts_dir.iterdir() if d.is_dir())
        if draft_count > 0:
            warnings.append(f"skills/drafts/ contains {draft_count} pending draft(s) — run /review-skill")
    # Old _drafts/ path — warn if present
    if (ROOT / "skills" / "_drafts").exists():
        warnings.append("skills/_drafts/ present — v4.3 uses skills/drafts/ (rename or migrate)")

    # agents/
    for a in EXPECTED["agents"]:
        check_yaml_frontmatter(f"agents/{a}", ["name", "description"])

    # commands/
    for c in EXPECTED["commands"]:
        check_yaml_frontmatter(f"commands/{c}", ["description"])

    # team-packs/ (per ZEREF_OS §8)
    for t in EXPECTED["team_packs"]:
        check_yaml_frontmatter(f"team-packs/{t}", ["name", "description"])

    # references/v4x-canon/ — imported design corpus
    check_dir("references/v4x-canon", "canon")
    for c in EXPECTED["v4x_canon"]:
        check_file(f"references/v4x-canon/{c}", "v4x canon doc")

    # Harness stubs (per ZEREF_OS §10)
    for s in EXPECTED["harness_stubs"]:
        check_file(s, "harness stub")

    # Plugin manifests
    for m in EXPECTED["plugin_manifests"]:
        check_file(m, "plugin manifest")
        try:
            json.loads((ROOT / m).read_text())
        except (FileNotFoundError, json.JSONDecodeError) as e:
            errors.append(f"{m}: invalid JSON ({e})")

    # Output
    print(f"Zeref OS validator — {ROOT}")
    print(f"Skills:           {sum((ROOT / 'skills' / s).is_dir() for s in EXPECTED['skills'])}/10")
    print(f"Agents:           {sum((ROOT / 'agents' / a).is_file() for a in EXPECTED['agents'])}/6")
    print(f"Commands:         {sum((ROOT / 'commands' / c).is_file() for c in EXPECTED['commands'])}/8")
    print(f"Team packs:       {sum((ROOT / 'team-packs' / t).is_file() for t in EXPECTED['team_packs'])}/6")
    print(f"Config:           {sum((ROOT / 'config' / c).is_file() for c in EXPECTED['config'])}/5")
    print(f"Root privacy:     {sum((ROOT / f).is_file() for f in EXPECTED['root_privacy'])}/3 (PRIVACY, REDACT, SHARING_POLICY)")
    print(f"v4x canon:        {sum((ROOT / 'references/v4x-canon' / c).is_file() for c in EXPECTED['v4x_canon'])}/6")
    print(f"Harness stubs:    {sum((ROOT / s).is_file() for s in EXPECTED['harness_stubs'])}/3")
    print(f"Memory layout:    flat")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ! {w}")

    if errors:
        print(f"\n✘ {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\n✔ Validation passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
