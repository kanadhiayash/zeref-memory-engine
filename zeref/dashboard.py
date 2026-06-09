"""
zeref.dashboard — Static HTML score dashboard (Sprint 3).

Reads all tests/scores-v*.csv files and generates a single self-contained
HTML file with a Chart.js line chart of weighted scores per version.

Usage:
    from zeref.dashboard import generate
    generate(scores_dir=Path("tests"), output_path=Path("tests/dashboard.html"))

    # or via CLI:
    zeref dashboard [--output path/to/out.html]
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _version_key(v: str) -> tuple:
    """Convert semver-like string to sortable tuple."""
    parts = re.split(r"[.\-]", v)
    out = []
    for p in parts:
        try:
            out.append((0, int(p)))
        except ValueError:
            out.append((1, p))
    return tuple(out)


def _load_scores(scores_dir: Path) -> dict[str, list[float]]:
    """
    Load all scores-v*.csv files.
    Returns {version: [weighted_score, ...]} sorted by semver.
    """
    files = sorted(
        scores_dir.glob("scores-v*.csv"),
        key=lambda f: _version_key(f.stem.replace("scores-v", "")),
    )
    data: dict[str, list[float]] = {}
    for f in files:
        version = f.stem.replace("scores-v", "")
        scores: list[float] = []
        try:
            with f.open(newline="") as fh:
                for row in csv.DictReader(fh):
                    try:
                        scores.append(float(row.get("weighted", 0)))
                    except (ValueError, TypeError):
                        pass
        except Exception:
            continue
        if scores:
            data[version] = scores
    return data


def _summarise(data: dict[str, list[float]]) -> dict[str, dict]:
    summary: dict[str, dict] = {}
    for ver, scores in data.items():
        avg = sum(scores) / len(scores) if scores else 0.0
        passing = sum(1 for s in scores if s >= 4.0)
        summary[ver] = {
            "avg": round(avg, 3),
            "count": len(scores),
            "passing": passing,
            "pass_rate": round(passing / len(scores) * 100, 1) if scores else 0.0,
        }
    return summary


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Zeref OS — Score Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
         background:#0f1117;color:#e2e8f0;padding:2rem}}
    h1{{font-size:1.5rem;margin-bottom:.25rem;color:#a78bfa}}
    .sub{{color:#64748b;font-size:.875rem;margin-bottom:2rem}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
           gap:1rem;margin-bottom:2rem}}
    .card{{background:#1e2130;border-radius:8px;padding:1.25rem}}
    .clabel{{font-size:.7rem;color:#64748b;text-transform:uppercase;
             letter-spacing:.05em;margin-bottom:.5rem}}
    .cval{{font-size:2rem;font-weight:700;color:#a78bfa}}
    .csub{{font-size:.75rem;color:#94a3b8;margin-top:.25rem}}
    .wrap{{background:#1e2130;border-radius:8px;padding:1.5rem;
           margin-bottom:2rem;max-height:380px}}
    table{{width:100%;border-collapse:collapse;background:#1e2130;
           border-radius:8px;overflow:hidden}}
    th{{background:#2d3148;padding:.75rem 1rem;text-align:left;
        font-size:.7rem;color:#94a3b8;text-transform:uppercase}}
    td{{padding:.6rem 1rem;font-size:.875rem;border-top:1px solid #2d3148}}
    .pass{{color:#4ade80}}.warn{{color:#fbbf24}}.fail{{color:#f87171}}
  </style>
</head>
<body>
  <h1>Zeref OS — Score Dashboard</h1>
  <p class="sub">Regression scores · {n_versions} version(s) · {total_tasks} tasks tracked</p>
  <div class="grid">
    <div class="card"><div class="clabel">Latest Avg</div>
      <div class="cval">{latest_avg}</div>
      <div class="csub">v{latest_ver} · {latest_pr}% pass rate</div></div>
    <div class="card"><div class="clabel">Versions</div>
      <div class="cval">{n_versions}</div>
      <div class="csub">from v{first_ver}</div></div>
    <div class="card"><div class="clabel">Total Tasks</div>
      <div class="cval">{total_tasks}</div>
      <div class="csub">all versions</div></div>
    <div class="card"><div class="clabel">Harness Files</div>
      <div class="cval">{n_harness}</div>
      <div class="csub">skills with test specs</div></div>
  </div>
  <div class="wrap"><canvas id="c"></canvas></div>
  <table>
    <thead><tr><th>Version</th><th>Avg</th><th>Tasks</th><th>Pass Rate</th><th>Status</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <script>
    new Chart(document.getElementById("c"),{{
      type:"line",
      data:{{labels:{labels},datasets:[{{
        label:"Avg Weighted Score",data:{avgs},
        borderColor:"#a78bfa",backgroundColor:"rgba(167,139,250,.15)",
        borderWidth:2,pointRadius:5,fill:true,tension:.3
      }}]}},
      options:{{responsive:true,maintainAspectRatio:true,
        scales:{{
          y:{{min:0,max:5,grid:{{color:"#2d3148"}},ticks:{{color:"#94a3b8"}}}},
          x:{{grid:{{color:"#2d3148"}},ticks:{{color:"#94a3b8"}}}}
        }},
        plugins:{{legend:{{labels:{{color:"#e2e8f0"}}}}}}
      }}
    }});
  </script>
</body></html>
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate(scores_dir: Path, output_path: Path) -> None:
    """Generate self-contained HTML dashboard from scores CSVs."""
    data = _load_scores(scores_dir)
    summary = _summarise(data)

    versions = list(summary.keys())
    if not versions:
        output_path.write_text("<html><body><p>No score data found in " + str(scores_dir) + "</p></body></html>")
        return

    latest = versions[-1]
    first = versions[0]
    total_tasks = sum(v["count"] for v in summary.values())

    harness_dir = scores_dir / "eval-harness"
    n_harness = len(list(harness_dir.glob("*.md"))) if harness_dir.exists() else 0

    # Table rows
    rows_html = ""
    for ver in reversed(versions):
        s = summary[ver]
        avg = s["avg"]
        cls = "pass" if avg >= 4.5 else ("warn" if avg >= 4.0 else "fail")
        status = "✔ Good" if avg >= 4.5 else ("⚠ Review" if avg >= 4.0 else "✘ Failing")
        rows_html += (
            f"<tr><td>v{ver}</td><td class='{cls}'>{avg}</td>"
            f"<td>{s['count']}</td><td>{s['pass_rate']}%</td>"
            f"<td class='{cls}'>{status}</td></tr>"
        )

    html = _TEMPLATE.format(
        n_versions=len(versions),
        total_tasks=total_tasks,
        latest_avg=summary[latest]["avg"],
        latest_ver=latest,
        latest_pr=summary[latest]["pass_rate"],
        first_ver=first,
        n_harness=n_harness,
        labels=str(versions),
        avgs=str([summary[v]["avg"] for v in versions]),
        rows=rows_html,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
