"""Reference-only guardrail benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import intake_skip, lineage_axis, lineage_reports


def run() -> dict:
    skipped = intake_skip("reference_only_guardrails")
    if skipped:
        return skipped
    reference = lineage_reports()["reference"]
    return lineage_axis("reference_only_guardrails", {
        "all_reference_rows": (reference["counts"]["reference_only_rows"] == 19, "19 reference-only rows detected"),
        "all_guarded": (reference["counts"]["implemented"] == 19, "19 reference-only battle tests implemented"),
        "evidence_only": (reference["counts"]["evidence_only"] == 19, "no reference-only runtime bundles"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
