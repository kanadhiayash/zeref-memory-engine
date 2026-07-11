#!/usr/bin/env python3
"""
privacy-audit: allow-file "Validator error messages document pattern-shaped tokens (schema examples) that trigger the scanner as expected."

zeref-validate.py — Validate Zeref OS plugin structure.

Checks:
- Root manifests (SKILL.md, AGENTS.md, CLAUDE.md, GEMINI.md)
- Root privacy templates (PRIVACY.md, REDACT.md, SHARING_POLICY.md)
- config/ has required files
- memory/ scaffold complete (flat layout)
- skills/ — count read from zeref-registry.json (no more hardcoded /10) [L1]
- agents/ has 6 agents with valid frontmatter
- commands/ has 8 commands
- team-packs/ has 6 packs
- references/v4x-canon/ has 6 design docs (historical reference)
- harness stubs present
- plugin.json + marketplace.json present and valid JSON
- Deprecation warning if legacy memory/wiki/ still has live content
- PATTERNS.jsonl event allowlist + per-event JSON-schema
- skill-route stack-length lint (max 5)
- Auto-Activation Gate presence lint (warn if missing gate events in recent log)

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

# PATTERNS.jsonl event allowlist + per-event required payload keys
EVENT_SCHEMA = {
    "wiki-write":       {"required": ["summary"], "optional": []},
    "session-start":    {"required": [], "optional": ["trigger", "scope", "budget_ceiling_usd", "team", "force_multipliers"]},
    "memory-drift-detected": {"required": ["finding"], "optional": []},
    "budget-gate":      {"required": ["weight", "tier", "match"], "optional": ["est_cost_usd", "budget_remaining_usd", "override_reason"]},
    "skill-route":      {"required": ["domain", "lead", "support", "qa"], "optional": ["ext"]},
    "tool-probe":       {"required": ["tool", "reachable"], "optional": ["path", "fallback", "marker_verified"]},
    "prompt-gate":      {"required": ["classification"], "optional": ["restructured", "brief_tokens", "stripped_context_tokens", "injection_detected"]},
    "handoff-compress": {"required": ["original_tokens", "compressed_tokens", "ratio"], "optional": ["model_from", "model_to", "harness_from", "harness_to"]},
    "tier-change":      {"required": ["from", "to"], "optional": []},
    # Legacy / pre-v2.6
    "grep-with-context": {"required": [], "optional": ["action"]},
    "log-cutover":       {"required": [], "optional": ["from", "to", "note"]},
}

VALID_WEIGHTS = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
VALID_TIERS = {"OPUS", "SONNET", "HAIKU", "OPUS-equivalent", "SONNET-equivalent", "HAIKU-equivalent"}
# CRITICAL never on Haiku; LOW never on Opus (Core Principle 14)
TIER_MISMATCHES = {("CRITICAL", "HAIKU"), ("CRITICAL", "HAIKU-equivalent"), ("LOW", "OPUS"), ("LOW", "OPUS-equivalent")}

errors = []
warnings = []
gate_lint = []


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


def load_skill_inventory():
    """Load skill list from zeref-registry.json (dynamic skill count)."""
    reg_path = ROOT / "zeref-registry.json"
    if not reg_path.is_file():
        errors.append("missing zeref-registry.json (required for dynamic skill count)")
        return []
    try:
        reg = json.loads(reg_path.read_text())
        return [s["skill"] for s in reg.get("skills", [])]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        errors.append(f"zeref-registry.json: invalid structure ({e})")
        return []


def lint_patterns_log(skill_inventory):
    """Validate PATTERNS.jsonl event schema + stack-length cap.
    Advisory: warn if no recent gate events.
    skill-route lead/support may be either skill names OR agent names (memory-keeper / privacy-guardian etc.).
    """
    # Extend inventory with agent names (skill-router lead can be an agent — e.g. memory-keeper)
    agent_names = [a.replace(".md", "") for a in EXPECTED["agents"]]
    valid_actors = set(skill_inventory) | set(agent_names)
    p = ROOT / "memory" / "patterns" / "PATTERNS.jsonl"
    if not p.is_file():
        # Empty scaffold (no hot.md) → already reported by main(); stay quiet here.
        if (ROOT / "memory" / "hot.md").is_file():
            warnings.append("memory/patterns/PATTERNS.jsonl missing")
        return
    lines = p.read_text().splitlines()
    if not lines:
        return
    inventory_set = valid_actors  # use combined skill + agent set
    gate_events_seen = {"budget-gate": 0, "skill-route": 0, "prompt-gate": 0}
    for i, ln in enumerate(lines, 1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            ev = json.loads(ln)
        except json.JSONDecodeError as e:
            gate_lint.append(f"PATTERNS.jsonl line {i}: invalid JSON ({e})")
            continue
        etype = ev.get("event")
        if etype not in EVENT_SCHEMA:
            gate_lint.append(f"PATTERNS.jsonl line {i}: unknown event type '{etype}' (not in allowlist)")
            continue
        schema = EVENT_SCHEMA[etype]
        payload = ev.get("payload", {}) or {}
        for req in schema["required"]:
            if req not in payload:
                gate_lint.append(f"PATTERNS.jsonl line {i}: event '{etype}' missing required payload key '{req}'")
        # Core Principle 14 lint — stack cap of 5
        if etype == "skill-route":
            support = payload.get("support", [])
            stack_size = 1 + len(support) + (1 if payload.get("qa") else 0)
            if stack_size > 5:
                gate_lint.append(f"PATTERNS.jsonl line {i}: skill-route stack size {stack_size} > 5 (stack cap; AGENTS.md skill-router §Anti-patterns)")
            lead = payload.get("lead")
            if lead and lead not in inventory_set:
                gate_lint.append(f"PATTERNS.jsonl line {i}: skill-route lead '{lead}' not in registry")
        if etype == "budget-gate":
            w = payload.get("weight")
            t = payload.get("tier")
            if w and w not in VALID_WEIGHTS:
                gate_lint.append(f"PATTERNS.jsonl line {i}: budget-gate invalid weight '{w}'")
            if t and t not in VALID_TIERS:
                gate_lint.append(f"PATTERNS.jsonl line {i}: budget-gate invalid tier '{t}'")
            if (w, t) in TIER_MISMATCHES and payload.get("match") != "OVERRIDE":
                gate_lint.append(f"PATTERNS.jsonl line {i}: budget-gate {w}->{t} mismatch (Core Principle 14 violation; only allowed with match=OVERRIDE)")
        if etype in gate_events_seen:
            gate_events_seen[etype] += 1
    # advisory
    if sum(gate_events_seen.values()) == 0 and len(lines) > 5:
        warnings.append("no Auto-Activation Gate events (budget-gate/skill-route/prompt-gate) in PATTERNS.jsonl despite >5 entries — gates may be skipped")


def main():
    # L1: load skill inventory from registry
    skill_inventory = load_skill_inventory()
    skill_count_expected = len(skill_inventory)
    skill_count_actual = sum((ROOT / "skills" / s).is_dir() for s in skill_inventory)

    # Root manifests
    for f in EXPECTED["root_manifests"]:
        check_file(f, "root manifest")

    # Root privacy templates (per ZEREF_OS §4.1)
    for f in EXPECTED["root_privacy"]:
        check_file(f, "root privacy template")

    # config/
    for f in EXPECTED["config"]:
        check_file(f"config/{f}", "config")

    # memory/ — flat layout per ZEREF_OS §12.
    # Memory is per-user-project: this repo ships an empty scaffold (memory/README.md
    # + .gitkeep). Missing dirs/files are warnings, not errors, in that case;
    # a populated project should `python3 -m zeref init` to scaffold them.
    memory_root = ROOT / "memory"
    memory_populated = any(
        (memory_root / f).exists()
        for f in EXPECTED["memory_flat"]
    )
    if memory_populated:
        for d in EXPECTED["memory_dirs"]:
            check_dir(f"memory/{d}", "memory")
        for f in EXPECTED["memory_flat"]:
            check_file(f"memory/{f}", "memory (flat)")
        check_file("memory/patterns/PATTERNS.jsonl", "patterns log")
    else:
        warnings.append("memory/ is empty scaffold — run `python3 -m zeref init` in your project to populate")

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

    # skills/ — L1: registry-driven count
    for s in skill_inventory:
        check_dir(f"skills/{s}", "skill")
        check_yaml_frontmatter(f"skills/{s}/SKILL.md", ["name", "description"])
    # drafts/ is intentional — pattern-to-skill writes here; not active skills
    drafts_dir = ROOT / "skills" / "drafts"
    if drafts_dir.is_dir():
        draft_count = sum(1 for d in drafts_dir.iterdir() if d.is_dir())
        if draft_count > 0:
            warnings.append(f"skills/drafts/ contains {draft_count} pending draft(s) — run /review-skill")
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

    # references/v4x-canon/
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

    # PATTERNS.jsonl validation (schema + stack-cap)
    lint_patterns_log(skill_inventory)

    # Output
    print(f"Zeref OS validator — {ROOT}")
    print(f"Skills:           {skill_count_actual}/{skill_count_expected} (from zeref-registry.json)")
    print(f"Agents:           {sum((ROOT / 'agents' / a).is_file() for a in EXPECTED['agents'])}/6")
    print(f"Commands:         {sum((ROOT / 'commands' / c).is_file() for c in EXPECTED['commands'])}/8")
    print(f"Team packs:       {sum((ROOT / 'team-packs' / t).is_file() for t in EXPECTED['team_packs'])}/6")
    print(f"Config:           {sum((ROOT / 'config' / c).is_file() for c in EXPECTED['config'])}/5")
    print(f"Root privacy:     {sum((ROOT / f).is_file() for f in EXPECTED['root_privacy'])}/3 (PRIVACY, REDACT, SHARING_POLICY)")
    print(f"v4x canon:        {sum((ROOT / 'references/v4x-canon' / c).is_file() for c in EXPECTED['v4x_canon'])}/6")
    print(f"Harness stubs:    {sum((ROOT / s).is_file() for s in EXPECTED['harness_stubs'])}/3")
    print(f"Memory layout:    flat")
    print(f"PATTERNS lint:    {len(gate_lint)} finding(s)")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ! {w}")

    if gate_lint:
        print(f"\nPATTERNS.jsonl lint findings ({len(gate_lint)}):")
        for g in gate_lint[:20]:  # cap to 20
            print(f"  ~ {g}")
        if len(gate_lint) > 20:
            print(f"  ... and {len(gate_lint) - 20} more")

    if errors:
        print(f"\n✘ {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\n✔ Validation passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
