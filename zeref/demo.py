"""
zeref.demo — Sandbox demo runner (Sprint 4).

`zeref demo` spawns a temp project, initialises a minimal Zeref OS layout,
runs 20 structural regression checks, prints green/red report, then cleans up.

All checks are deterministic (no LLM calls) — works offline, no credentials.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ---------------------------------------------------------------------------
# 20 regression tasks (deterministic shell checks)
# ---------------------------------------------------------------------------

_TASKS: list[tuple[str, str]] = [
    ("AGENTS.md exists",               "test -f AGENTS.md"),
    ("SOUL.md exists",                 "test -f SOUL.md"),
    ("zeref-registry.json exists",     "test -f zeref-registry.json"),
    ("_shared/rules.md exists",        "test -f _shared/rules.md"),
    ("memory/hot.md exists",           "test -f memory/hot.md"),
    ("memory/index.md exists",         "test -f memory/index.md"),
    ("memory/DECISIONS.md exists",     "test -f memory/DECISIONS.md"),
    ("memory/CONFLICTS.md exists",     "test -f memory/CONFLICTS.md"),
    ("memory/RISKS.md exists",         "test -f memory/RISKS.md"),
    ("memory/patterns/PATTERNS.jsonl", "test -f memory/patterns/PATTERNS.jsonl"),
    ("config/PROJECT.md exists",       "test -f config/PROJECT.md"),
    ("PRIVACY.md exists",              "test -f PRIVACY.md"),
    ("REDACT.md exists",               "test -f REDACT.md"),
    ("SHARING_POLICY.md exists",       "test -f SHARING_POLICY.md"),
    ("skills/ has ≥1 skill",           "test $(ls skills/ 2>/dev/null | wc -l) -gt 0"),
    ("registry is valid JSON",
     "python3 -c \"import json,sys; json.load(open('zeref-registry.json'))\""),
    ("registry has ≥10 skills",
     "python3 -c \"import json,sys; d=json.load(open('zeref-registry.json')); "
     "sys.exit(0 if len(d.get('skills',[]))>=10 else 1)\""),
    ("SOUL.md has ≥5 sections",        "test $(grep -c '^## ' SOUL.md) -ge 5"),
    ("_shared/rules.md has R1-R4",
     "grep -q 'R1' _shared/rules.md && grep -q 'R4' _shared/rules.md"),
    ("CHANGELOG.md mentions ZRF",      "grep -q 'ZRF' CHANGELOG.md"),
]


# ---------------------------------------------------------------------------
# Scaffolding
# ---------------------------------------------------------------------------

def _find_zeref_root() -> Path | None:
    p = Path.cwd()
    for _ in range(10):
        if (p / "AGENTS.md").exists() and (p / "zeref-registry.json").exists():
            return p
        p = p.parent
    return None


def _scaffold_memory(root: Path) -> None:
    mem = root / "memory"
    mem.mkdir(exist_ok=True)
    (mem / "hot.md").write_text("# hot.md\n\n*(demo session)*\n")
    (mem / "index.md").write_text("# index.md\n")
    (mem / "DECISIONS.md").write_text("# DECISIONS.md\n")
    (mem / "CONFLICTS.md").write_text("# CONFLICTS.md\n")
    (mem / "RISKS.md").write_text("# RISKS.md\n")
    pat = mem / "patterns"
    pat.mkdir(exist_ok=True)
    (pat / "PATTERNS.jsonl").write_text("")


def _scaffold_config(root: Path) -> None:
    cfg = root / "config"
    cfg.mkdir(exist_ok=True)
    (cfg / "PROJECT.md").write_text("---\nname: demo-project\n---\n")


def _scaffold_temp(root: Path) -> None:
    """Copy real project files if available; else generate minimal stubs."""
    src = _find_zeref_root()

    if src:
        for fname in [
            "AGENTS.md", "SOUL.md", "zeref-registry.json", "PRIVACY.md",
            "REDACT.md", "SHARING_POLICY.md", "CHANGELOG.md",
        ]:
            if (src / fname).exists():
                shutil.copy2(src / fname, root / fname)

        if (src / "_shared").exists():
            shutil.copytree(src / "_shared", root / "_shared")

        skills_src = src / "skills"
        if skills_src.exists():
            (root / "skills").mkdir()
            for d in skills_src.iterdir():
                if d.is_dir():
                    (root / "skills" / d.name).mkdir()
    else:
        # Minimal stubs
        (root / "AGENTS.md").write_text("# AGENTS.md\n")
        (root / "SOUL.md").write_text(
            "# Soul\n## 1. A\n## 2. B\n## 3. C\n## 4. D\n## 5. E\n"
        )
        (root / "zeref-registry.json").write_text(
            json.dumps({"version": "2.0.0", "skills": [{"skill": f"s{i}"} for i in range(10)]})
        )
        (root / "PRIVACY.md").write_text("---\nmode: abstract\n---\n")
        (root / "REDACT.md").write_text("---\nclasses: []\n---\n")
        (root / "SHARING_POLICY.md").write_text("---\ndefault: deny\n---\n")
        (root / "CHANGELOG.md").write_text("# Changelog\n\n## [2.0.0]\n\nZRF: Execution 8/10\n")
        sh = root / "_shared"
        sh.mkdir()
        (sh / "rules.md").write_text("# Rules\n## R1\n## R2\n## R3\n## R4\n")
        (root / "skills" / "demo-skill").mkdir(parents=True)

    _scaffold_memory(root)
    _scaffold_config(root)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_demo() -> int:
    print("\n" + "═" * 60)
    print("  Zeref OS — Demo Runner  (20 regression checks)")
    print("═" * 60)

    with tempfile.TemporaryDirectory(prefix="zeref-demo-") as tmp:
        root = Path(tmp)
        print(f"\n  Scaffolding temp project …")
        _scaffold_temp(root)
        print(f"  Running {len(_TASKS)} checks …\n")

        passed = failed = 0
        results: list[tuple[str, bool, str]] = []

        for name, check in _TASKS:
            r = subprocess.run(
                check, shell=True, cwd=str(root),
                capture_output=True, text=True,
            )
            ok = r.returncode == 0
            results.append((name, ok, r.stderr.strip()))
            passed += ok
            failed += not ok

        GREEN, RED, YELLOW, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[0m"
        for name, ok, err in results:
            icon = "✔" if ok else "✘"
            col = GREEN if ok else RED
            extra = f"  ← {err}" if (not ok and err) else ""
            print(f"  {col}{icon}{RESET}  {name}{extra}")

        total = len(_TASKS)
        rate = round(passed / total * 100, 1)
        col = GREEN if rate >= 90 else (YELLOW if rate >= 70 else RED)
        print(f"\n{'═' * 60}")
        print(f"  {col}{passed}/{total} PASSED  ({rate}%){RESET}")
        print(f"{'═' * 60}\n")

    return 0 if failed == 0 else 1
