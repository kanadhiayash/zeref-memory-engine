"""
zeref.db — Structured-data snapshot layer (Sprint 3).

On /done (or explicit call), emits a SQLite snapshot of parsed memory files.
DuckDB used if installed (enables .parquet export); falls back to sqlite3.

Tables:
  decisions(id, date, title, rationale, evidence_grade, provenance)
  events(id, ts, agent, event, target, payload_summary, evidence_grade)
  conflicts(id, detected_ts, side_a, side_b, status)

Usage:
    from zeref.db import snapshot, query
    result = snapshot(memory_dir=Path("memory"))
    rows   = query("SELECT * FROM decisions WHERE evidence_grade='high'")
"""

from __future__ import annotations

import re
import sqlite3
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def _parse_decisions(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text(errors="ignore")
    records: list[dict] = []
    for block in re.split(r"\n---\n", text):
        rec: dict = {}
        for line in block.splitlines():
            for pattern, key in [
                (r"\*\*Decision:\*\*\s*(.+)",       "title"),
                (r"\*\*Date:\*\*\s*(.+)",            "date"),
                (r"\*\*Rationale:\*\*\s*(.+)",       "rationale"),
                (r"\*\*Evidence grade:\*\*\s*(.+)",  "evidence_grade"),
                (r"\*\*Provenance:\*\*\s*(.+)",      "provenance"),
            ]:
                m = re.match(pattern, line.strip())
                if m:
                    rec[key] = m.group(1).strip()
        if rec.get("title"):
            records.append(rec)
    return records


def _parse_events(path: Path) -> list[dict]:
    import json
    if not path.exists():
        return []
    events: list[dict] = []
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            events.append({
                "ts":              d.get("ts", ""),
                "agent":           d.get("agent", ""),
                "event":           d.get("event", ""),
                "target":          d.get("target", ""),
                "payload_summary": str(d.get("payload", ""))[:200],
                "evidence_grade":  d.get("evidence_grade", ""),
            })
        except Exception:
            continue
    return events


def _parse_conflicts(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text(errors="ignore")
    records: list[dict] = []
    for block in re.split(r"\n---\n", text):
        rec: dict = {}
        for line in block.splitlines():
            for pattern, key in [
                (r"\*\*Detected:\*\*\s*(.+)",  "detected_ts"),
                (r"\*\*Side A:\*\*\s*(.+)",    "side_a"),
                (r"\*\*Side B:\*\*\s*(.+)",    "side_b"),
                (r"\*\*Status:\*\*\s*(.+)",    "status"),
            ]:
                m = re.match(pattern, line.strip())
                if m:
                    rec[key] = m.group(1).strip()
        if rec.get("side_a") or rec.get("detected_ts"):
            records.append(rec)
    return records


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def _write_sqlite(
    db_path: Path,
    decisions: list[dict],
    events: list[dict],
    conflicts: list[dict],
) -> None:
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, title TEXT, rationale TEXT,
            evidence_grade TEXT, provenance TEXT
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, agent TEXT, event TEXT,
            target TEXT, payload_summary TEXT, evidence_grade TEXT
        );
        CREATE TABLE IF NOT EXISTS conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detected_ts TEXT, side_a TEXT, side_b TEXT, status TEXT
        );
    """)
    c.executemany(
        "INSERT INTO decisions(date,title,rationale,evidence_grade,provenance)"
        " VALUES(?,?,?,?,?)",
        [(d.get("date",""), d.get("title",""), d.get("rationale",""),
          d.get("evidence_grade",""), d.get("provenance","")) for d in decisions],
    )
    c.executemany(
        "INSERT INTO events(ts,agent,event,target,payload_summary,evidence_grade)"
        " VALUES(?,?,?,?,?,?)",
        [(e["ts"], e["agent"], e["event"], e["target"],
          e["payload_summary"], e["evidence_grade"]) for e in events],
    )
    c.executemany(
        "INSERT INTO conflicts(detected_ts,side_a,side_b,status) VALUES(?,?,?,?)",
        [(cf.get("detected_ts",""), cf.get("side_a",""),
          cf.get("side_b",""), cf.get("status","")) for cf in conflicts],
    )
    conn.commit()
    conn.close()


def _try_parquet(db_path: Path, out_dir: Path) -> bool:
    """Export tables as .parquet if DuckDB is installed."""
    try:
        import duckdb  # type: ignore
        con = duckdb.connect()
        for table in ("decisions", "events", "conflicts"):
            con.execute(
                f"COPY (SELECT * FROM sqlite_scan('{db_path}', '{table}')) "
                f"TO '{out_dir / (table + '.parquet')}' (FORMAT PARQUET)"
            )
        con.close()
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def snapshot(
    memory_dir: Path = Path("memory"),
    output_dir: Path | None = None,
) -> dict:
    """
    Parse memory/ and emit structured snapshot (SQLite + optional Parquet).

    Returns: {snapshot_dir, decisions, events, conflicts, db_path, parquet}.
    Markdown stays canonical; snapshot is derived, never primary.
    """
    if output_dir is None:
        output_dir = memory_dir / "snapshots" / date.today().isoformat()
    output_dir.mkdir(parents=True, exist_ok=True)

    decisions = _parse_decisions(memory_dir / "DECISIONS.md")
    events    = _parse_events(memory_dir / "patterns" / "PATTERNS.jsonl")
    conflicts = _parse_conflicts(memory_dir / "CONFLICTS.md")

    db_path = output_dir / "zeref.db"
    _write_sqlite(db_path, decisions, events, conflicts)
    parquet_ok = _try_parquet(db_path, output_dir)

    return {
        "snapshot_dir": str(output_dir),
        "decisions":    len(decisions),
        "events":       len(events),
        "conflicts":    len(conflicts),
        "db_path":      str(db_path),
        "parquet":      parquet_ok,
    }


def query(
    sql: str,
    snapshots_dir: Path = Path("memory/snapshots"),
) -> list[dict]:
    """
    Run SQL against the most recent snapshot DB.

    Example:
        query("SELECT title, evidence_grade FROM decisions WHERE evidence_grade='high'")
    """
    candidates = sorted(snapshots_dir.rglob("zeref.db"), reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No zeref.db found under {snapshots_dir}")
    conn = sqlite3.connect(str(candidates[0]))
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(sql).fetchall()]
    conn.close()
    return rows
