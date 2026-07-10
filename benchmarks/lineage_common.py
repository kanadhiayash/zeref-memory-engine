"""Shared lineage benchmark helpers."""

from __future__ import annotations

from typing import Any

from benchmarks.helpers import axis_result
from zeref.lineage.council import run_council
from zeref.lineage.critical import audit_critical
from zeref.lineage.high import audit_high
from zeref.lineage.importer import import_lineage
from zeref.lineage.intake import audit_csv
from zeref.lineage.reference import audit_reference_only


def lineage_reports() -> dict[str, Any]:
    """Run deterministic local lineage gates once for benchmark axes."""
    return {
        "audit": audit_csv(_csv_path()),
        "import": import_lineage(_csv_path(), sandbox=True, latest_default=True, dry_run=True, resolver=_fake_resolver),
        "council": run_council(_csv_path(), strict=True),
        "critical": audit_critical(_csv_path(), strict=True),
        "high": audit_high(_csv_path(), strict=True),
        "reference": audit_reference_only(_csv_path(), strict=True),
    }


def lineage_axis(axis: str, subs: dict[str, tuple[bool, str]]) -> dict[str, Any]:
    return axis_result(axis, {
        key: (10.0 if passed else 0.0, evidence)
        for key, (passed, evidence) in subs.items()
    })


def _csv_path():
    from zeref.lineage.importer import default_csv_path

    return default_csv_path()


def _fake_resolver(row):
    from zeref.lineage.importer import SourceIdentity

    if row.source_kind != "github":
        return SourceIdentity(
            repo_url=row.repo_url,
            owner_name=row.repo_name,
            default_branch="",
            commit_sha="",
            archived=False,
            private=False,
            updated_at="",
            license="citation",
            subdirectory=row.subdirectory,
            row_ids=[row.id],
            source_kind="non_github",
            notes=["concept_source"],
        )
    return SourceIdentity(
        repo_url=f"https://github.com/{row.github_repo}",
        owner_name=row.github_repo,
        default_branch="default",
        commit_sha=f"fixture-{row.id:02d}",
        archived=row.github_repo.lower() == "microsoftarchive/promptbench",
        private=False,
        updated_at="fixture",
        license="NOASSERTION",
        subdirectory=row.subdirectory,
        row_ids=[row.id],
        source_kind="github",
        notes=["local_fixture_metadata"],
    )
