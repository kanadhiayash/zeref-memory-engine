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
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from benchmarks import adaptivity, portability, retrieval, scalability, trust  # noqa: E402

AXES = [portability, adaptivity, scalability, retrieval, trust]


def _apply_verified_overrides(results: list[dict]) -> list[dict]:
    """Apply independent audit overrides that may lower deterministic drafts."""
    trust_audit = REPO / "docs" / "TRUST_AUDIT.md"
    if not trust_audit.exists():
        return results

    text = trust_audit.read_text(encoding="utf-8", errors="ignore")
    match = re.search(
        r"^- \*\*Verified score \(this audit\):\*\* \*\*([0-9]+(?:\.[0-9]+)?)\*\*",
        text,
        re.MULTILINE,
    )
    if not match:
        return results

    verified_trust = float(match.group(1))
    adjusted: list[dict] = []
    for result in results:
        if result.get("axis") != "trust":
            adjusted.append(result)
            continue

        published = dict(result)
        draft_score = float(result["score"])
        if verified_trust <= draft_score:
            published["draft_score"] = draft_score
            published["score"] = round(verified_trust, 2)
            published["summary_note"] = (
                f"Verified by TRUST_AUDIT.md; deterministic draft was {draft_score:.2f}."
            )
            published["note"] = (
                f"Deterministic draft score was {draft_score:.2f}. "
                f"Published trust score is {verified_trust:.2f} per "
                "docs/TRUST_AUDIT.md independent audit."
            )
        adjusted.append(published)
    return adjusted


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
        ("The `trust` axis is independently re-graded by the security audit "
         "before publication. When the audit score is lower than the "
         "deterministic draft, the verified score is the published score."),
        "",
        "## Scores",
        "",
        "| Axis | Score | Pass? | Note |",
        "|---|---:|:---:|---|",
    ]
    for r in results:
        ok = "✅" if r["score"] >= 9.0 else ("⚠️" if r["score"] >= 8.0 else "❌")
        note = r.get("summary_note", "")
        lines.append(f"| {r['axis']} | {r['score']:.2f} | {ok} | {note} |")
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
        "python3 -m benchmarks.retrieval",
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

    results = _apply_verified_overrides([axis.run() for axis in AXES])

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
