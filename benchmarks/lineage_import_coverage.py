"""Lineage import coverage benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import lineage_axis, lineage_reports


def run() -> dict:
    reports = lineage_reports()
    audit = reports["audit"]
    imported = reports["import"]
    return lineage_axis("lineage_import_coverage", {
        "all_rows_validated": (audit["counts"]["rows"] == 64 and audit["passed"], "64 intake rows validated"),
        "deduped_source_scopes": (imported["source_count"] == 59 and imported["passed"], f"sources={imported['source_count']}"),
        "dry_run_no_writes": (imported["dry_run"] is True, "metadata-only dry-run fixture"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
