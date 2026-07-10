"""Foreign code containment benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import lineage_axis, lineage_reports


def run() -> dict:
    reports = lineage_reports()
    critical = reports["critical"]
    high = reports["high"]
    reference = reports["reference"]
    return lineage_axis("foreign_code_containment", {
        "critical_no_foreign_code": (all(not item["foreign_code_imported"] for item in critical["findings"]), "critical gates report no vendored foreign code"),
        "high_no_core_dependency": (all(not item["core_dependency"] for item in high["findings"]), "21 high rows optional or gated"),
        "reference_no_runtime_bundle": (all(not item["runtime_bundled"] for item in reference["findings"]), "19 reference rows evidence-only"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
