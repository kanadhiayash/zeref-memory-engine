"""Critical lineage adoption coverage benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import lineage_axis, lineage_reports


def run() -> dict:
    critical = lineage_reports()["critical"]
    return lineage_axis("critical_adoption_coverage", {
        "all_critical_rows": (critical["counts"]["critical_rows"] == 10, "10 critical rows detected"),
        "all_implemented": (critical["counts"]["implemented"] == 10, "10 critical gates implemented"),
        "core_or_gate": (critical["counts"]["core_or_gate"] == 10, "all critical rows implemented as core or gates"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
