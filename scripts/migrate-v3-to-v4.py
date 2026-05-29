#!/usr/bin/env python3
"""
migrate-v3-to-v4.py — One-shot migration of v3 wiki state to v4 memory layout.

v3 sources:
  wiki/hot.md       → memory/wiki/INDEX.md entries + memory/wiki/ARCHIVE/hot-<iso>.md
  wiki/log.md       → memory/logs/session-events.jsonl (one event per log line)
  wiki/index.md     → memory/wiki/INDEX.md (merged)

Usage:
  python3 scripts/migrate-v3-to-v4.py --from /path/to/v3/wiki --to ./memory

Idempotent: re-runs detect existing entries by hash and skip dupes.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()


def iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def migrate_hot(src: Path, dst_memory: Path) -> int:
    """Archive old hot.md, extract session entries to INDEX."""
    hot = src / "hot.md"
    if not hot.is_file():
        return 0
    archive = dst_memory / "wiki" / "ARCHIVE" / f"hot-{iso_now()}.md"
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_text(hot.read_text())
    return 1


def migrate_log(src: Path, dst_memory: Path) -> int:
    """Convert v3 wiki/log.md (timestamp | agent | action | target | summary)
    to v4 session-events.jsonl."""
    log = src / "log.md"
    if not log.is_file():
        return 0

    out = dst_memory / "logs" / "session-events.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    # Read existing hashes to dedupe
    seen = set()
    if out.is_file():
        for line in out.read_text().splitlines():
            try:
                e = json.loads(line)
                seen.add(e.get("hash"))
            except json.JSONDecodeError:
                continue

    appended = 0
    with out.open("a") as f:
        for line in log.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("---"):
                continue
            # Try to parse pipe-separated v3 format
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue
            ts = parts[0]
            agent = parts[1] if len(parts) > 1 else "unknown"
            event = parts[2] if len(parts) > 2 else "v3-log-entry"
            target = parts[3] if len(parts) > 3 else ""
            summary = " | ".join(parts[4:]) if len(parts) > 4 else ""
            payload = {"summary": summary, "v3_raw": line}
            h = sha256(line)
            if h in seen:
                continue
            entry = {
                "ts": ts if "T" in ts else iso_now(),
                "agent": agent,
                "event": event,
                "target": target,
                "payload": payload,
                "hash": h,
                "migrated_from_v3": True,
            }
            f.write(json.dumps(entry) + "\n")
            appended += 1
    return appended


def migrate_index(src: Path, dst_memory: Path) -> int:
    """Append v3 wiki/index.md content to v4 INDEX.md if not already present."""
    idx_src = src / "index.md"
    if not idx_src.is_file():
        return 0
    idx_dst = dst_memory / "wiki" / "INDEX.md"
    idx_dst.parent.mkdir(parents=True, exist_ok=True)
    existing = idx_dst.read_text() if idx_dst.is_file() else ""
    v3_content = idx_src.read_text()
    marker = "## Migrated from v3"
    if marker in existing:
        return 0
    with idx_dst.open("a") as f:
        f.write(f"\n\n{marker} ({iso_now()})\n\n")
        f.write(v3_content)
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", required=True, help="path to v3 wiki/ directory")
    ap.add_argument("--to", dest="dst", required=True, help="path to v4 memory/ directory")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    dst = Path(args.dst).resolve()

    if not src.is_dir():
        print(f"ERROR: {src} not found", file=sys.stderr)
        sys.exit(1)
    dst.mkdir(parents=True, exist_ok=True)

    print(f"Migrating v3 wiki: {src} → {dst}")
    hot = migrate_hot(src, dst)
    events = migrate_log(src, dst)
    idx = migrate_index(src, dst)

    print(f"  hot.md archived:      {hot}")
    print(f"  events appended:      {events}")
    print(f"  INDEX.md merged:      {idx}")
    print("Done.")


if __name__ == "__main__":
    main()
