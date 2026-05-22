#!/usr/bin/env python3
"""
zeref-validate.py — Fleet Validation Script
Version: 3.0.0
Run: python3 scripts/zeref-validate.py
Purpose: Validates that all skills, agents, commands, and references exist and are properly formatted
"""

import os
import json
import re
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────
FLEET_ROOT = Path(__file__).parent.parent
SKILLS_DIR = FLEET_ROOT / "skills"
AGENTS_DIR = FLEET_ROOT / "agents"
COMMANDS_DIR = FLEET_ROOT / "commands"
REFERENCES_DIR = FLEET_ROOT / "references"
REGISTRY_PATH = FLEET_ROOT / "registry" / "zeref-skill-registry.json"

EXPECTED_SKILL_COUNT = 109
EXPECTED_AGENT_COUNT = 8
EXPECTED_COMMAND_COUNT = 14

REQUIRED_ROOT_FILES = [
    "ZEREFOS.md", "ZEREF.md", "AGENTS.md", "GEMINI.md", "README.md",
    "CHANGELOG.md", "SECURITY.md", "CONTRIBUTING.md", "ZEREFPROJECT.md",
    "CLAUDE.md", "zeref-mcp-stack.md"
]

REQUIRED_REFERENCES = [
    "zeref-qa-gate.md", "zeref-safety-principles.md",
    "shared-anti-hallucination.md", "shared-token-discipline.md"
]

PLUGIN_MANIFEST = FLEET_ROOT / ".claude-plugin" / "plugin.json"

errors = []
warnings = []
passes = []

# ─── Checks ──────────────────────────────────────────────────────────────────

def check_root_files():
    for f in REQUIRED_ROOT_FILES:
        path = FLEET_ROOT / f
        if path.exists():
            passes.append(f"✅ Root file exists: {f}")
        else:
            errors.append(f"❌ Missing root file: {f}")
    # Check plugin manifest separately (lives in .claude-plugin/)
    if PLUGIN_MANIFEST.exists():
        passes.append(f"✅ Plugin manifest exists: .claude-plugin/plugin.json")
    else:
        errors.append(f"❌ Missing plugin manifest: .claude-plugin/plugin.json")

def check_skill_count():
    if SKILLS_DIR.exists():
        skill_files = list(SKILLS_DIR.rglob("*.md"))
        count = len(skill_files)
        if count >= EXPECTED_SKILL_COUNT:
            passes.append(f"✅ Skill count: {count} (expected ≥{EXPECTED_SKILL_COUNT})")
        else:
            errors.append(f"❌ Skill count: {count} (expected ≥{EXPECTED_SKILL_COUNT})")
    else:
        errors.append(f"❌ skills/ directory missing")

def check_agent_count():
    if AGENTS_DIR.exists():
        agent_files = list(AGENTS_DIR.glob("*.md"))
        count = len(agent_files)
        if count >= EXPECTED_AGENT_COUNT:
            passes.append(f"✅ Agent count: {count} (expected ≥{EXPECTED_AGENT_COUNT})")
        else:
            errors.append(f"❌ Agent count: {count} (expected ≥{EXPECTED_AGENT_COUNT})")
    else:
        errors.append(f"❌ agents/ directory missing")

def check_registry():
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH) as f:
                registry = json.load(f)
            skill_count = len(registry.get("skills", []))
            passes.append(f"✅ Registry valid: {skill_count} skills registered")
            # Check each skill has triggers
            missing_triggers = [s["id"] for s in registry.get("skills", []) if not s.get("triggers")]
            if missing_triggers:
                warnings.append(f"⚠️  Skills missing trigger phrases: {len(missing_triggers)} — {missing_triggers[:5]}")
        except json.JSONDecodeError as e:
            errors.append(f"❌ Registry JSON invalid: {e}")
    else:
        errors.append(f"❌ Registry missing: {REGISTRY_PATH}")

def check_references():
    for ref in REQUIRED_REFERENCES:
        path = REFERENCES_DIR / ref
        if path.exists():
            passes.append(f"✅ Reference exists: {ref}")
        else:
            errors.append(f"❌ Missing reference: {ref}")

def check_skill_format():
    """Check each skill has v3 frontmatter: skill: or name: field + trigger_phrases"""
    if not SKILLS_DIR.exists():
        return
    missing_skill_id = []
    missing_triggers = []
    for skill_file in SKILLS_DIR.rglob("*.md"):
        content = skill_file.read_text(encoding="utf-8", errors="replace")
        has_id = "skill:" in content or "name:" in content
        has_triggers = "trigger_phrases:" in content
        if not has_id:
            missing_skill_id.append(skill_file.parent.name)
        if not has_triggers:
            missing_triggers.append(skill_file.parent.name)
    if missing_skill_id:
        warnings.append(f"⚠️  Skills missing skill/name field: {len(missing_skill_id)} — {missing_skill_id[:3]}")
    if missing_triggers:
        warnings.append(f"⚠️  Skills missing trigger_phrases: {len(missing_triggers)} — {missing_triggers[:3]}")
    if not missing_skill_id and not missing_triggers:
        passes.append(f"✅ All skill files have v3 frontmatter (skill id + trigger_phrases)")

def check_command_count():
    if COMMANDS_DIR.exists():
        command_files = list(COMMANDS_DIR.glob("*.md")) + list(COMMANDS_DIR.glob("*.toml"))
        count = len(command_files)
        if count >= EXPECTED_COMMAND_COUNT:
            passes.append(f"✅ Command count: {count} (expected ≥{EXPECTED_COMMAND_COUNT})")
        else:
            errors.append(f"❌ Command count: {count} (expected ≥{EXPECTED_COMMAND_COUNT})")
    else:
        errors.append(f"❌ commands/ directory missing")

def check_experience_log():
    # experience.jsonl lives at repo root
    log_path = FLEET_ROOT / "experience.jsonl"
    if log_path.exists():
        passes.append(f"✅ experience.jsonl exists (self-improvement loop ready)")
    else:
        warnings.append(f"⚠️  experience.jsonl not yet created — log your first session after v3.0 launch")

def check_scripts():
    """Verify all automation scripts exist."""
    required = [
        "scripts/zeref-validate.py",
        "scripts/self_eval.py",
        "scripts/skill_updater.py",
        "scripts/rebuild_registry.py",
    ]
    for script in required:
        path = FLEET_ROOT / script
        if path.exists():
            passes.append(f"✅ Script exists: {script}")
        else:
            errors.append(f"❌ Missing script: {script}")

# ─── Run All Checks ───────────────────────────────────────────────────────────

check_root_files()
check_skill_count()
check_agent_count()
check_command_count()
check_registry()
check_references()
check_skill_format()
check_scripts()
check_experience_log()

# ─── Report ───────────────────────────────────────────────────────────────────

print("\n" + "═" * 60)
print("  ZEREF FLEET VALIDATION REPORT — v3.0.0")
print("═" * 60)

print(f"\n✅ PASSED ({len(passes)})")
for p in passes:
    print(f"  {p}")

if warnings:
    print(f"\n⚠️  WARNINGS ({len(warnings)})")
    for w in warnings:
        print(f"  {w}")

if errors:
    print(f"\n❌ ERRORS ({len(errors)})")
    for e in errors:
        print(f"  {e}")
    print("\n🔴 VALIDATION FAILED — resolve errors before shipping v3.0.0")
else:
    print("\n🟢 VALIDATION PASSED — Zeref v3.0.0 is ready to ship")

print("═" * 60 + "\n")
