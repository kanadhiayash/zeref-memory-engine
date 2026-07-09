"""
`zeref init` scaffolds the expected layout.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REQUIRED_DIRS = [
    "memory",
    "memory/archive",
    "memory/patterns",
    "memory/snapshots",
    "memory/raw",
    "memory/sync/outbound",
    "memory/sync/parent",
    "memory/l0_raw",
    "memory/l1_atoms",
    "memory/l2_scenes",
    "memory/l3_profiles",
    "memory/indexes",
    "memory/views",
    "memory/reports",
    "memory/handoffs",
    "memory/loops",
    "memory/archives",
    "config",
    "skills",
    "skills/drafts",
]

REQUIRED_FILES = [
    "config/PROJECT.md",
    "config/BUDGET.md",
    "PRIVACY.md",
    "memory/hot.md",
    "memory/index.md",
    "memory/DECISIONS.md",
    "memory/OPEN_QUESTIONS.md",
    "memory/RISKS.md",
    "memory/CONFLICTS.md",
    "memory/MEMORY.md",
    "memory/patterns/PATTERNS.jsonl",
    "memory/l1_atoms/facts.jsonl",
    "memory/l1_atoms/decisions.jsonl",
    "memory/l1_atoms/risks.jsonl",
    "memory/l1_atoms/tasks.jsonl",
    "memory/l1_atoms/preferences.jsonl",
    "memory/l1_atoms/contradictions.jsonl",
    "memory/l1_atoms/sources.jsonl",
    "memory/l1_atoms/errors.jsonl",
    "memory/l1_atoms/tests.jsonl",
    "memory/l1_atoms/events.jsonl",
]


def test_init_scaffolds_full_layout(repo_root: Path, tmp_path: Path) -> None:
    r = subprocess.run(
        [sys.executable, "-m", "zeref", "init",
         "--directory", str(tmp_path),
         "--name", "scaffold-test",
         "--privacy", "abstract",
         "--tier", "auto",
         "--parent", ""],
        capture_output=True, text=True, cwd=str(repo_root),
    )
    assert r.returncode == 0, (
        f"init crashed:\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"
    )

    for d in REQUIRED_DIRS:
        assert (tmp_path / d).is_dir(), f"directory {d!r} not created"

    for f in REQUIRED_FILES:
        assert (tmp_path / f).is_file(), f"file {f!r} not created"

    project = (tmp_path / "config" / "PROJECT.md").read_text(encoding="utf-8")
    assert "scaffold-test" in project
    assert "privacy_mode: abstract" in project
    assert "model_tier: auto" in project
