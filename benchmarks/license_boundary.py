"""License boundary benchmark axis."""

from __future__ import annotations

import sys

from benchmarks.helpers import print_json_result
from benchmarks.lineage_common import intake_skip, lineage_axis, lineage_reports


def run() -> dict:
    skipped = intake_skip("license_boundary")
    if skipped:
        return skipped
    imported = lineage_reports()["import"]
    sources = [source["identity"] for source in imported["sources"]]
    return lineage_axis("license_boundary", {
        "license_metadata_recorded": (all("license" in source for source in sources), f"sources={len(sources)}"),
        "concept_source_marked": (any(source["source_kind"] == "non_github" and source["license"] == "citation" for source in sources), "Software 2.0 marked citation"),
        "archived_reference_marked": (any(source["archived"] for source in sources), "archived PromptBench fixture marked"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
