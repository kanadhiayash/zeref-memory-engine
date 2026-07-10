"""High lineage adoption coverage benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import lineage_axis, lineage_reports


def run() -> dict:
    high = lineage_reports()["high"]
    return lineage_axis("high_adoption_coverage", {
        "all_high_rows": (high["counts"]["high_rows"] == 21, "21 high rows detected"),
        "all_implemented": (high["counts"]["implemented"] == 21, "21 high boundaries implemented"),
        "optional_or_gated": (high["counts"]["optional_or_gated"] == 21, "all high rows optional or gated"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
