"""
zeref.cli — Reference CLI for Zeref OS (Sprint 2).

Commands:
    zeref status          Print hot.md summary + active tier
    zeref write-decision  Append a decision to memory/DECISIONS.md
    zeref memory ...      Add/search/get/update/history/explain structured memory
    zeref grade <claim>   Grade a claim (evidence-grader heuristics + optional LLM)
    zeref audit-privacy   Run deterministic PII audit on memory/
    zeref audit           Structural validation (wraps zeref-validate.py)

Write commands: write-decision, memory add, memory update.
Wraps litellm for grade if available; degrades gracefully without it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _project_root() -> Path:
    """Walk up from cwd until AGENTS.md found (Zeref OS root)."""
    from zeref.memory import MemoryRoot

    return MemoryRoot.discover().root


def _read_file(path: Path, fallback: str = "") -> str:
    return path.read_text(errors="ignore") if path.exists() else fallback


def _print_section(title: str, body: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")
    print(body.strip())


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(args: argparse.Namespace) -> int:
    root = _project_root()

    hot = _read_file(root / "memory" / "hot.md", "(hot.md not found — run /start first)")
    _print_section("memory/hot.md (last 3 sessions)", hot[:1500])

    project = _read_file(root / "config" / "PROJECT.md", "(config/PROJECT.md missing — run /start)")
    _print_section("config/PROJECT.md (first 10 lines)", "\n".join(project.splitlines()[:10]))

    budget = _read_file(root / "config" / "BUDGET.md", "")
    tier = "Standard (default)"
    for line in budget.splitlines():
        if "model_tier:" in line:
            tier = line.split(":", 1)[-1].strip()
            break
    _print_section("Active tier", tier)

    reg_path = root / "zeref-registry.json"
    if reg_path.exists():
        reg = json.loads(reg_path.read_text())
        names = [s["skill"] for s in reg.get("skills", [])]
        _print_section("zeref-registry.json", f"{len(names)} skills: {', '.join(names)}")

    return 0


def cmd_write_decision(args: argparse.Namespace) -> int:
    """Write a decision: hold single-writer lock, atomic append, scrub PII first."""
    from zeref.lock import LockError
    from zeref.memory import MemoryWriter

    root = _project_root()

    title    = args.title    or input("Decision title: ").strip()
    why      = args.why      or input("Why (rationale): ").strip()
    evidence = args.evidence or input("Evidence/source (Enter to skip): ").strip()
    grade    = args.grade    or "medium"

    try:
        result = MemoryWriter.from_root(root).write_decision(
            title=title,
            why=why,
            evidence=evidence,
            grade=grade,
        )
    except LockError as e:
        print(f"✘ {e}")
        return 2

    print(f"✔ Decision appended to {result.target}")
    print(f"  Title: {result.title} | Date: {result.date} | Grade: {grade}")
    print(f"  Event: {result.event_hash}")
    if result.redacted:
        print(f"  PII scrubbed from inputs: {result.redacted} token(s)")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """v2.5 L5: scaffold memory/ + config/ + privacy templates (no LLM)."""
    from zeref.memory import normalize_init_values, scaffold_project

    root = Path(args.directory).resolve() if args.directory else Path.cwd()
    print(f"\nInitialising Zeref OS layout at {root}")

    # Use `is None` so empty-string CLI args (e.g. --parent "") skip the prompt
    name    = args.name    if args.name    is not None else (input("Project name: ").strip() or "(unnamed)")
    privacy = args.privacy if args.privacy is not None else (input("Privacy mode [abstract/exact/local-only] (default abstract): ").strip() or "abstract")
    tier    = args.tier    if args.tier    is not None else (input("Model tier [auto/free/standard/god-mode] (default auto): ").strip() or "auto")
    parent  = args.parent  if args.parent  is not None else input("Parent project path (Enter if none): ").strip()
    values = normalize_init_values(name=name, privacy=privacy, tier=tier, parent=parent)
    scaffold_project(root, name=name, privacy=privacy, tier=tier, parent=parent)

    print(f"\n✔ Scaffolded:")
    print(f"  config/PROJECT.md (name={values['name']}, privacy={values['privacy']}, tier={values['tier']})")
    print(f"  memory/ flat layout")
    print(f"  skills/drafts/ (review queue)")
    if values["parent"]:
        print(f"  parent: {values['parent']}")
    print(f"\nNext: edit config/PROJECT.md as needed, then `zeref status`.")
    return 0


def cmd_db_status(args: argparse.Namespace) -> int:
    """v2.5 L4: report backend (sqlite/duckdb) + extras availability."""
    backends = {"sqlite3": False, "duckdb": False, "yaml": False, "litellm": False}
    try: import sqlite3; backends["sqlite3"] = True
    except ImportError: pass
    try: import duckdb;  backends["duckdb"]  = True
    except ImportError: pass
    try: import yaml;    backends["yaml"]    = True
    except ImportError: pass
    try: import litellm; backends["litellm"] = True
    except ImportError: pass

    print("\nzeref backend status:")
    for k, v in backends.items():
        icon = "✔" if v else "✘"
        print(f"  {icon} {k:<10} {'available' if v else 'not installed'}")
    print(f"\n  Parquet export: {'enabled' if backends['duckdb'] else 'disabled (install duckdb)'}")
    print(f"  Rich YAML:      {'enabled' if backends['yaml'] else 'fallback regex parser'}")
    print(f"  LLM grading:    {'enabled' if backends['litellm'] else 'heuristic-only'}")
    return 0


def cmd_grade(args: argparse.Namespace) -> int:
    """Evidence-grader: heuristic + optional LLM via litellm."""
    claim = (args.claim or "").strip()
    if not claim:
        claim = input("Claim to grade: ").strip()

    low = claim.lower()

    # Recency
    if any(w in low for w in ["today", "this week", "just", "recently", "2026", "2025"]):
        recency = "high"
    elif any(w in low for w in ["last year", "2024", "2023", "old", "legacy"]):
        recency = "low"
    else:
        recency = "medium"

    # Provenance
    if any(w in low for w in ["source:", "ref:", "from ", "per ", "according to", "confirmed by"]):
        provenance = "high"
    elif any(w in low for w in ["i think", "probably", "maybe", "might", "guess"]):
        provenance = "low"
    else:
        provenance = "medium"

    # Corroboration
    if any(w in low for w in ["always", "never", "all ", "none ", "definitely"]):
        corroboration = "low"
    elif any(w in low for w in ["typically", "generally", "often", "usually"]):
        corroboration = "medium"
    else:
        corroboration = "medium"

    _s = {"high": 2, "medium": 1, "low": 0}
    avg = (_s[recency] + _s[provenance] + _s[corroboration]) / 3
    grade = "high" if avg >= 1.7 else ("low" if avg < 0.8 else "medium")

    llm_note = ""
    try:
        import litellm  # type: ignore
        resp = litellm.completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": (
                f"Grade this claim on recency, provenance, corroboration (high/medium/low each). "
                f"Claim: \"{claim}\"\n"
                f"Reply JSON only: {{\"recency\":\"?\",\"provenance\":\"?\",\"corroboration\":\"?\","
                f"\"grade\":\"?\",\"reasoning\":\"...\"}}"
            )}],
            max_tokens=200,
        )
        d = json.loads(resp.choices[0].message.content)
        grade, recency, provenance, corroboration = (
            d.get("grade", grade), d.get("recency", recency),
            d.get("provenance", provenance), d.get("corroboration", corroboration),
        )
        llm_note = f"\n  LLM reasoning: {d.get('reasoning', '')}"
    except Exception:
        llm_note = "\n  (litellm unavailable — heuristic grade)"

    print(f"\nClaim:          {claim}")
    print(f"  Grade:         {grade.upper()}")
    print(f"  Recency:       {recency}")
    print(f"  Provenance:    {provenance}")
    print(f"  Corroboration: {corroboration}{llm_note}")
    if grade == "low":
        print("\n  ⚠ Suggested action: demote or remove from wiki.")
    return 0


def cmd_audit_privacy(args: argparse.Namespace) -> int:
    from zeref.privacy import audit as _audit

    root = _project_root()
    redact = root / "REDACT.md"
    directory = Path(args.directory) if args.directory else root / "memory"

    print(f"Scanning {directory} …  (REDACT.md: {redact})")
    results = _audit(directory=directory, redact_md_path=redact)

    print(f"\nFiles scanned:  {results['scanned']}")
    print(f"Total PII hits: {results['total_hits']}")

    if results["by_class"]:
        print("\nHits by class:")
        for cls, cnt in sorted(results["by_class"].items(), key=lambda x: -x[1]):
            print(f"  [{cls}] {cnt} file(s)")

    if results["by_file"]:
        print("\nAffected files:")
        for fp, cnt in sorted(results["by_file"].items(), key=lambda x: -x[1]):
            print(f"  {cnt:3d}  {fp}")
    else:
        print("\n✔ No PII detected.")

    return 0 if results["total_hits"] == 0 else 1


def cmd_audit(args: argparse.Namespace) -> int:
    root = _project_root()
    script = root / "scripts" / "zeref-validate.py"
    if not script.exists():
        script = root / "scripts" / "zeref-validate-v4.py"
    if not script.exists():
        print("✘ zeref-validate.py not found in scripts/")
        return 1
    return subprocess.run([sys.executable, str(script)], cwd=str(root)).returncode


def cmd_memory(args: argparse.Namespace) -> int:
    from zeref.memory_state import event_to_dict, item_to_dict, MemoryStore

    store = MemoryStore.from_root(_project_root())

    try:
        if args.memory_command == "add":
            item = store.add(
                kind=args.kind,
                title=args.title or input("Title: ").strip(),
                body=args.body or input("Body: ").strip(),
                entity=args.entity or "",
                tags=args.tag or [],
                source_ref=args.source_ref or "",
                confidence=args.confidence,
                authority=args.authority,
            )
            return _print_item_result(item, json_output=args.json, verb="added")

        if args.memory_command == "search":
            items = store.search(
                args.query or "",
                entity=args.entity or "",
                kind=args.kind or "",
                limit=args.limit,
            )
            if args.json:
                print(json.dumps([item_to_dict(item) for item in items], indent=2, sort_keys=True))
            else:
                for item in items:
                    _print_memory_item(item)
                if not items:
                    print("No memory items found.")
            return 0

        if args.memory_command == "get":
            item = store.get(args.id)
            if item is None:
                print(f"✘ memory item {args.id} not found")
                return 1
            return _print_item_result(item, json_output=args.json, verb="found")

        if args.memory_command == "update":
            item = store.update(
                args.id,
                kind=args.kind,
                title=args.title,
                body=args.body,
                entity=args.entity,
                tags=args.tag,
                source_ref=args.source_ref,
                confidence=args.confidence,
                authority=args.authority,
            )
            return _print_item_result(item, json_output=args.json, verb="updated")

        if args.memory_command == "history":
            events = store.history(args.id, limit=args.limit)
            if args.json:
                print(json.dumps([event_to_dict(event) for event in events], indent=2, sort_keys=True))
            else:
                for event in events:
                    item = f" item={event.item_id}" if event.item_id is not None else ""
                    print(f"{event.ts} {event.event}{item} {event.hash}")
                if not events:
                    print("No memory events found.")
            return 0

        if args.memory_command == "explain":
            item = store.explain(args.id, query=args.query or "")
            return _print_item_result(item, json_output=args.json, verb="explained")
    except (KeyError, ValueError, RuntimeError) as exc:
        print(f"✘ {exc}")
        return 1

    print("✘ unknown memory command")
    return 1


def _print_item_result(item, *, json_output: bool, verb: str) -> int:
    from zeref.memory_state import item_to_dict

    if json_output:
        print(json.dumps(item_to_dict(item), indent=2, sort_keys=True))
    else:
        print(f"✔ memory item {verb}: {item.id}")
        _print_memory_item(item)
    return 0


def _print_memory_item(item) -> None:
    print(f"[{item.id}] {item.title}")
    print(f"  kind={item.kind} entity={item.entity or '(none)'}")
    print(f"  source_ref={item.source_ref or '(none)'} confidence={item.confidence} authority={item.authority}")
    if item.why_returned:
        print(f"  why_returned={item.why_returned}")
    if item.tags:
        print(f"  tags={', '.join(item.tags)}")
    print(f"  body={item.body}")


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    from zeref import __version__ as _v
    p = argparse.ArgumentParser(prog="zeref", description=f"Zeref OS CLI v{_v}")
    p.add_argument("--version", action="version", version=f"zeref {_v}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Print hot.md + tier")

    wd = sub.add_parser("write-decision", help="Append decision to memory/DECISIONS.md")
    wd.add_argument("--title");  wd.add_argument("--why")
    wd.add_argument("--evidence"); wd.add_argument("--grade", choices=["high","medium","low"], default="medium")

    gr = sub.add_parser("grade", help="Grade a claim")
    gr.add_argument("claim", nargs="?", default="")

    ap = sub.add_parser("audit-privacy", help="Scan memory/ for PII (read-only)")
    ap.add_argument("--directory", help="Directory to scan (default: memory/)")
    ap.add_argument("--strict", action="store_true",
                    help="Exit non-zero on any unredacted hit (suitable for CI gate)")

    sub.add_parser("audit", help="Structural validation")

    init_p = sub.add_parser("init", help="Scaffold memory/ + config/ + privacy templates")
    init_p.add_argument("--directory", help="Target dir (default: cwd)")
    init_p.add_argument("--name", help="Project name (non-interactive)")
    init_p.add_argument("--privacy", choices=["abstract","exact","local-only"])
    init_p.add_argument("--tier", choices=["auto","free","standard","god-mode"])
    init_p.add_argument("--parent", help="Parent project path")

    sub.add_parser("db-status", help="Report backend (sqlite/duckdb) + extras")

    memory = sub.add_parser("memory", help="Structured local memory state")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)

    mem_add = memory_sub.add_parser("add", help="Add a structured memory item")
    mem_add.add_argument("--kind", default="note")
    mem_add.add_argument("--title")
    mem_add.add_argument("--body")
    mem_add.add_argument("--entity")
    mem_add.add_argument("--tag", action="append")
    mem_add.add_argument("--source-ref")
    mem_add.add_argument("--confidence", choices=["high", "medium", "low"], default="medium")
    mem_add.add_argument("--authority", choices=["canonical", "confirmed", "inferred", "unknown"], default="unknown")
    mem_add.add_argument("--json", action="store_true")

    mem_search = memory_sub.add_parser("search", help="Search structured memory state")
    mem_search.add_argument("query", nargs="?", default="")
    mem_search.add_argument("--entity")
    mem_search.add_argument("--kind")
    mem_search.add_argument("--limit", type=int, default=10)
    mem_search.add_argument("--json", action="store_true")

    mem_get = memory_sub.add_parser("get", help="Get a memory item by id")
    mem_get.add_argument("id", type=int)
    mem_get.add_argument("--json", action="store_true")

    mem_update = memory_sub.add_parser("update", help="Update a memory item by id")
    mem_update.add_argument("id", type=int)
    mem_update.add_argument("--kind")
    mem_update.add_argument("--title")
    mem_update.add_argument("--body")
    mem_update.add_argument("--entity")
    mem_update.add_argument("--tag", action="append")
    mem_update.add_argument("--source-ref")
    mem_update.add_argument("--confidence", choices=["high", "medium", "low"])
    mem_update.add_argument("--authority", choices=["canonical", "confirmed", "inferred", "unknown"])
    mem_update.add_argument("--json", action="store_true")

    mem_history = memory_sub.add_parser("history", help="Show memory state event history")
    mem_history.add_argument("id", type=int, nargs="?")
    mem_history.add_argument("--limit", type=int, default=20)
    mem_history.add_argument("--json", action="store_true")

    mem_explain = memory_sub.add_parser("explain", help="Explain why a memory item is relevant")
    mem_explain.add_argument("id", type=int)
    mem_explain.add_argument("--query", default="")
    mem_explain.add_argument("--json", action="store_true")

    return p


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    handlers = {
        "status": cmd_status,
        "write-decision": cmd_write_decision,
        "grade": cmd_grade,
        "audit-privacy": cmd_audit_privacy,
        "audit": cmd_audit,
        "init": cmd_init,
        "db-status": cmd_db_status,
        "memory": cmd_memory,
    }
    handler = handlers.get(args.command)
    if not handler:
        parser.print_help(); sys.exit(1)
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
