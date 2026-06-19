#!/usr/bin/env python3
"""
benchmarks/run-all.py — Run all axes and emit docs/BENCHMARK_REPORT.md
plus machine-readable benchmarks/results.json.

Exit code:
    0  every axis ≥ 9.0 and no axis below 8.0 (the 10/10 pass bar)
    1  otherwise

Usage:
    python3 benchmarks/run-all.py
    python3 benchmarks/run-all.py --rubric benchmarks/RUBRIC.md
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from benchmarks import adaptivity, portability, scalability, trust  # noqa: E402

AXES = [portability, adaptivity, scalability, trust]


def _render_report(results: list[dict], rubric_rel: str, passed: bool) -> str:
    today = date.today().isoformat()  # noqa: DTZ011 — public report only
    lines = [
        "# Benchmark Report — Zeref OS v1.0.0",
        "",
        f"_Generated: {today}. Rubric: [`{rubric_rel}`]({rubric_rel})._",
        "",
        "## Verdict",
        "",
        ("**PASS** — every axis ≥ 9.0, no axis below 8.0."
         if passed else
         "**FAIL** — at least one axis falls below the pass bar (≥ 9.0 / "
         "≥ 8.0)."),
        "",
        "## Scores",
        "",
        "| Axis | Score | Pass? |",
        "|---|---:|:---:|",
    ]
    for r in results:
        ok = "✅" if r["score"] >= 9.0 else ("⚠️" if r["score"] >= 8.0 else "❌")
        lines.append(f"| {r['axis']} | {r['score']:.2f} | {ok} |")
    lines.append("")

    for r in results:
        lines += [
            f"## {r['axis'].title()} — {r['score']:.2f} / 10",
            "",
            "| Sub-criterion | Score | Evidence |",
            "|---|---:|---|",
        ]
        for k, v in r["sub"].items():
            lines.append(f"| `{k}` | {v['score']:.2f} | {v['evidence']} |")
        if "note" in r:
            lines += ["", f"> _{r['note']}_", ""]
        lines.append("")

    lines += [
        "## How to reproduce",
        "",
        "```bash",
        "python3 benchmarks/run-all.py",
        "```",
        "",
        "Per-axis scorers under `benchmarks/` are standalone:",
        "",
        "```bash",
        "python3 -m benchmarks.portability",
        "python3 -m benchmarks.adaptivity",
        "python3 -m benchmarks.scalability",
        "python3 -m benchmarks.trust",
        "```",
        "",
        "## Rubric",
        "",
        f"Sub-criteria and weights: [`{rubric_rel}`]({rubric_rel}).",
        "External re-scoring invited via PR.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rubric", default="benchmarks/RUBRIC.md")
    ap.add_argument("--out-report", default="docs/BENCHMARK_REPORT.md")
    ap.add_argument("--out-json", default="benchmarks/results.json")
    args = ap.parse_args()

    results = [axis.run() for axis in AXES]

    passed = all(r["score"] >= 9.0 for r in results) and \
             all(r["score"] >= 8.0 for r in results)

    report = _render_report(results, args.rubric, passed)
    (REPO / args.out_report).write_text(report, encoding="utf-8")
    (REPO / args.out_json).write_text(
        json.dumps({"passed": passed, "axes": results}, indent=2),
        encoding="utf-8",
    )

    for r in results:
        print(f"{r['axis']:<14} {r['score']:.2f}")
    print("-" * 24)
    print("VERDICT:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
