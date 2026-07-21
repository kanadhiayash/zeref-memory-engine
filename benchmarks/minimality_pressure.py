"""Minimality pressure benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import intake_skip, lineage_axis, lineage_reports


def run() -> dict:
    skipped = intake_skip("minimality_pressure")
    if skipped:
        return skipped
    reports = lineage_reports()
    high = reports["high"]
    reference = reports["reference"]
    return lineage_axis("minimality_pressure", {
        "high_not_core": (high["counts"]["optional_or_gated"] == high["counts"]["high_rows"], "high rows did not become core dependencies"),
        "reference_not_runtime": (reference["counts"]["evidence_only"] == reference["counts"]["reference_only_rows"], "reference rows did not enter runtime"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
