#!/usr/bin/env python3
"""
zeref-validate-v4.py — Validate Zeref 4.0 plugin structure.

Checks:
- Root manifests (SKILL.md, AGENTS.md, CLAUDE.md, GEMINI.md)
- config/ has 5 required files
- memory/ scaffold complete
- skills/ has expected M1 inventory (10 dirs, each with SKILL.md + valid frontmatter)
- agents/ has 6 agents with valid frontmatter
- commands/ has 7 commands
- plugin.json + marketplace.json present and valid JSON

Exit 0 on pass, 1 on fail.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXPECTED = {
    "root_manifests": ["SKILL.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md"],
    "config": ["PROJECT.md", "PRIVACY.md", "PERMISSIONS.md", "PARENT_SYNC.md", "BUDGET.md"],
    "memory_dirs": ["raw", "wiki", "logs", "snapshots", "sync/outbound", "sync/parent"],
    "memory_wiki": ["INDEX.md", "DECISIONS.md", "OPEN_QUESTIONS.md", "RISKS.md", "CONFLICTS.md"],
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
        "sync-parent.md", "reset-permissions.md", "review-skill.md",
    ],
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

    # config/
    for f in EXPECTED["config"]:
        check_file(f"config/{f}", "config")

    # memory/
    for d in EXPECTED["memory_dirs"]:
        check_dir(f"memory/{d}", "memory")
    for f in EXPECTED["memory_wiki"]:
        check_file(f"memory/wiki/{f}", "memory/wiki")
    check_file("memory/logs/session-events.jsonl", "session events log")

    # skills/
    for s in EXPECTED["skills"]:
        check_dir(f"skills/{s}", "skill")
        check_yaml_frontmatter(f"skills/{s}/SKILL.md", ["name", "description"])

    # agents/
    for a in EXPECTED["agents"]:
        check_yaml_frontmatter(f"agents/{a}", ["name", "description"])

    # commands/
    for c in EXPECTED["commands"]:
        check_yaml_frontmatter(f"commands/{c}", ["description"])

    # Plugin manifests
    for m in EXPECTED["plugin_manifests"]:
        check_file(m, "plugin manifest")
        try:
            json.loads((ROOT / m).read_text())
        except (FileNotFoundError, json.JSONDecodeError) as e:
            errors.append(f"{m}: invalid JSON ({e})")

    # Output
    print(f"Zeref 4.0 validator — {ROOT}")
    print(f"Skills: {sum((ROOT / 'skills' / s).is_dir() for s in EXPECTED['skills'])}/10")
    print(f"Agents: {sum((ROOT / 'agents' / a).is_file() for a in EXPECTED['agents'])}/6")
    print(f"Commands: {sum((ROOT / 'commands' / c).is_file() for c in EXPECTED['commands'])}/7")
    print(f"Config: {sum((ROOT / 'config' / c).is_file() for c in EXPECTED['config'])}/5")

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
