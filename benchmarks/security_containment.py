"""Security containment benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import lineage_axis, lineage_reports


def run() -> dict:
    reports = lineage_reports()
    reference_forms = reports["reference"]["forms"]
    high_forms = reports["high"]["forms"]
    return lineage_axis("security_containment", {
        "security_references_contained": (reference_forms.get("security-containment", 0) == 3, "raptor/mantishack/hacker-bob evidence-only"),
        "defensive_fixture_only": (high_forms.get("security-fixture", 0) == 1, "Purple Llama adapted as safety fixture only"),
        "critical_rails_present": (reports["critical"]["counts"]["implemented"] == 10, "critical rail gates included"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
