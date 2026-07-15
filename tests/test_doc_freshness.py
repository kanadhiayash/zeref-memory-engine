"""
Documentation freshness guard.

Two checks, both driven off the repo's actual state so they stay correct
across version bumps and future operator-record splits:

1. Live public surfaces (README badge, docs/wiki/Installation.md) name the
   version that `zeref/VERSION` declares, and don't advertise some *other*
   `vX.Y.Z`-shaped version as the product's current release.
2. No operator-record files (command logs, model-use ledgers, raw audit
   findings, Linear seed files, release-evidence dumps) are tracked back
   under docs/ — this repo's tracked audit history now lives in the
   private `zeref-operator-records` repo (see docs/audits/README.md).
   Only git-tracked files count: zeref/release/checks.py legitimately
   writes local evidence blobs under docs/audits/release-evidence/ at
   runtime, and .gitignore keeps them out of the public tree.
"""

from __future__ import annotations

import fnmatch
import re
import subprocess
from pathlib import Path

VERSION_RE = re.compile(r"\bv(\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?)\b")

# Files that live in docs/wiki/Installation.md-style "live" public surfaces
# and are expected to mention the current version.
LIVE_VERSION_SURFACES = ("README.md", "docs/wiki/Installation.md")

# Operator-record filename patterns that must not be tracked under docs/
# after the WS6 public/private split (2026-07-14). Mirrors the "Move to a
# private maintainer repository" section of the 2026-07-13 cleanup audit.
OPERATOR_RECORD_PATTERNS = (
    "ZEREF_COMMAND_LOG*",
    "OPUS_LEDGER*",
    "linear-seed*",
    "ZEREF_FINDINGS*",
    "ZEREF_REMEDIATION_BACKLOG*",
    "ZEREF_AUDIT_BASELINE*",
    "ZEREF_CONSISTENCY_AUDIT*",
    "ZEREF_CONTRACT_GRAPH*",
    "ZEREF_COMPONENT_INVENTORY*",
    "ZEREF_PRIOR_AUDIT_RECONCILIATION*",
    "DECISIONS_RATIFIED*",
    "POST_AUDIT_VERIFICATION*",
    "RETROSPECTIVE*",
    "release-evidence/*",
)


def _current_version(repo_root: Path) -> str:
    version_file = repo_root / "zeref" / "VERSION"
    assert version_file.exists(), "zeref/VERSION is missing"
    return version_file.read_text(encoding="utf-8").strip()


def _tracked_docs_files(repo_root: Path) -> list[str]:
    r = subprocess.run(
        ["git", "ls-files", "--", "docs/"],
        capture_output=True, text=True, cwd=str(repo_root), check=True,
    )
    return [line for line in r.stdout.splitlines() if line]


def test_live_surfaces_mention_current_version_and_no_other(repo_root: Path) -> None:
    current = _current_version(repo_root)

    for rel in LIVE_VERSION_SURFACES:
        path = repo_root / rel
        assert path.exists(), f"expected live doc surface missing: {rel}"
        text = path.read_text(encoding="utf-8", errors="ignore")

        found = {m.group(1) for m in VERSION_RE.finditer(text)}
        assert current in found, (
            f"{rel} does not mention the current version v{current} "
            f"(zeref/VERSION). Found version strings: {sorted(found) or 'none'}"
        )

        stale = found - {current}
        assert not stale, (
            f"{rel} advertises other version string(s) as current: "
            f"{sorted(stale)}. Only v{current} (from zeref/VERSION) should "
            "appear as a current-release claim; historical version mentions "
            "belong in CHANGELOG.md / docs/RELEASE_LOG.md, not live surfaces."
        )


def test_no_operator_records_tracked_under_docs(repo_root: Path) -> None:
    tracked = _tracked_docs_files(repo_root)
    assert tracked, "docs/ has no tracked files — unexpected"

    hits: list[str] = []
    for rel in tracked:
        name = Path(rel).name
        tail = "/".join(Path(rel).parts[-2:])
        if any(
            fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(tail, pat)
            for pat in OPERATOR_RECORD_PATTERNS
        ):
            hits.append(rel)

    assert not hits, (
        "operator-record file(s) tracked back under docs/ — these belong in "
        "the private zeref-operator-records repo per the 2026-07-13 audit "
        f"(WS6 split): {sorted(hits)}"
    )


def test_audits_dir_tracks_only_the_stub_pointer(repo_root: Path) -> None:
    tracked = [
        rel for rel in _tracked_docs_files(repo_root)
        if rel.startswith("docs/audits/")
    ]
    assert tracked == ["docs/audits/README.md"], (
        "docs/audits/ should track only the private-repo pointer stub "
        f"README.md after the WS6 split; tracked: {tracked}"
    )

    stub = (repo_root / "docs" / "audits" / "README.md").read_text(encoding="utf-8")
    assert "zeref-operator-records" in stub
