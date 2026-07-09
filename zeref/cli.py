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
    if getattr(args, "audit_command", None) == "report":
        from zeref.audit.reports import audit_report

        print(audit_report(root, since=args.since or "", format=args.format), end="")
        return 0

    script = root / "scripts" / "zeref-validate.py"
    if not script.exists():
        script = root / "scripts" / "zeref-validate-v4.py"
    if not script.exists():
        print("✘ zeref-validate.py not found in scripts/")
        return 1
    return subprocess.run([sys.executable, str(script)], cwd=str(root)).returncode


def cmd_memory(args: argparse.Namespace) -> int:
    from zeref.core.errors import GuardRejection
    from zeref.guards.write_gate import propose_memory, write_from_proposal
    from zeref.memory_state import card_to_dict, event_to_dict, item_to_dict, MemoryStore

    store = MemoryStore.from_root(_project_root())

    try:
        if args.memory_command == "propose":
            proposal = propose_memory(args.claim, output=Path(args.out))
            if args.json:
                print(json.dumps(proposal, indent=2, sort_keys=True))
            else:
                print(f"✔ proposal written to {args.out}")
            return 0

        if args.memory_command == "write":
            card = write_from_proposal(Path(args.from_path), store)
            print(json.dumps(card, indent=2, sort_keys=True) if args.json else f"✔ memory card written: {card['id']}")
            return 0

        if args.memory_command == "list":
            cards = store.list_cards(type=args.type or "", status=args.status or "", limit=args.limit)
            if args.json:
                print(json.dumps([card_to_dict(card) for card in cards], indent=2, sort_keys=True))
            else:
                for card in cards:
                    print(f"{card.id} {card.type} {card.status} {card.title}")
                if not cards:
                    print("No memory cards found.")
            return 0

        if args.memory_command == "show":
            card = store.get_card(args.id)
            if card is None:
                print(f"✘ memory card {args.id} not found")
                return 1
            print(json.dumps(card_to_dict(card), indent=2, sort_keys=True))
            return 0

        if args.memory_command == "archive":
            card = store.archive_card(args.id)
            print(json.dumps(card_to_dict(card), indent=2, sort_keys=True) if args.json else f"✔ archived {card.id}")
            return 0

        if args.memory_command == "supersede":
            old_card, new_card = store.supersede_card(args.id, args.with_id)
            result = {"superseded": card_to_dict(old_card), "replacement": card_to_dict(new_card)}
            print(json.dumps(result, indent=2, sort_keys=True) if args.json else f"✔ {old_card.id} superseded by {new_card.id}")
            return 0

        if args.memory_command == "add":
            item = store.add(
                kind=args.kind,
                title=args.title or input("Title: ").strip(),
                body=args.body or input("Body: ").strip(),
                entity=args.entity or "",
                tags=args.tag or [],
                layer=args.layer,
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
                layer=args.layer or "",
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
                layer=args.layer,
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

        if args.memory_command == "views":
            written = store.generate_views()
            if args.json:
                print(json.dumps(written, indent=2, sort_keys=True))
            else:
                print("✔ generated markdown views")
                for name, path in sorted(written.items()):
                    print(f"  {name}: {path}")
            return 0
    except GuardRejection as exc:
        print(str(exc))
        return 1
    except (KeyError, ValueError, RuntimeError) as exc:
        print(f"✘ {exc}")
        return 1

    print("✘ unknown memory command")
    return 1


def cmd_factguard(args: argparse.Namespace) -> int:
    from zeref.guards.fact_guard import check_claim, report, scan_path

    if args.factguard_command == "check":
        findings = check_claim(args.claim, source_refs=args.source_ref or [])
    elif args.factguard_command == "scan":
        findings = scan_path(Path(args.path))
    elif args.factguard_command == "report":
        findings = scan_path(_project_root() / "docs")
    else:
        print("✘ unknown factguard command")
        return 1

    print(report(findings, format=args.format))
    return 1 if any(f.severity == "high" for f in findings) else 0


def cmd_evidence(args: argparse.Namespace) -> int:
    from zeref.guards.evidence_guard import (
        check_public_docs,
        check_store,
        grade_text,
        list_by_grade,
        report_findings,
        upgrade_evidence,
    )
    from zeref.memory_state import card_to_dict, MemoryStore

    store = MemoryStore.from_root(_project_root())
    if args.evidence_command == "grade":
        text = Path(args.path).read_text(errors="ignore") if Path(args.path).exists() else args.path
        print(grade_text(text))
        return 0
    if args.evidence_command == "check":
        path = Path(args.path)
        if path.exists() and path.name != "memory":
            issues = check_public_docs(path)
            print("\n".join(issues) if issues else "No EvidenceGuard findings.")
            return 1 if issues else 0
        findings = check_store(store)
        print(report_findings(findings), end="")
        return 1 if any(f.severity == "high" for f in findings) else 0
    if args.evidence_command == "list":
        cards = list_by_grade(store, args.grade)
        print(json.dumps([card_to_dict(card) for card in cards], indent=2, sort_keys=True))
        return 0
    if args.evidence_command == "upgrade":
        card = upgrade_evidence(store, args.id, args.source)
        print(json.dumps(card_to_dict(card), indent=2, sort_keys=True))
        return 0
    if args.evidence_command == "report":
        findings = check_store(store)
        print(report_findings(findings), end="")
        return 1 if any(f.severity == "high" for f in findings) else 0
    print("✘ unknown evidence command")
    return 1


def cmd_contradictions(args: argparse.Namespace) -> int:
    from zeref.guards.contradiction_guard import (
        archive_conflict,
        format_conflicts,
        list_conflicts,
        resolve_conflict,
        show_conflict,
        write_conflicts,
    )
    from zeref.memory_state import MemoryStore

    store = MemoryStore.from_root(_project_root())
    if args.contradictions_command == "scan":
        conflicts = list_conflicts(store)
        write_conflicts(store, conflicts)
        print(format_conflicts(conflicts, format=args.format), end="")
        return 1 if any(c.severity in {"high", "critical"} for c in conflicts) else 0
    if args.contradictions_command == "list":
        conflicts = list_conflicts(store)
        print(format_conflicts(conflicts, format=args.format), end="")
        return 0
    if args.contradictions_command == "show":
        conflict = show_conflict(store, args.id)
        if conflict is None:
            print(f"✘ conflict {args.id} not found")
            return 1
        print(json.dumps(conflict.to_dict(), indent=2, sort_keys=True))
        return 0
    if args.contradictions_command == "resolve":
        result = resolve_conflict(store, args.id, winner=args.winner, reason=args.reason)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if args.contradictions_command == "archive":
        result = archive_conflict(store, args.id)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    print("✘ unknown contradictions command")
    return 1


def cmd_privacy(args: argparse.Namespace) -> int:
    from zeref.guards.privacy_guard import classify_text, format_findings, redact_file, scan_path

    root = _project_root()
    redact_md = root / "REDACT.md"
    if args.privacy_command == "scan":
        findings = scan_path(Path(args.path), redact_md_path=redact_md)
        print(format_findings(findings, format=args.format), end="")
        return 1 if findings and args.strict else 0
    if args.privacy_command == "classify":
        print(json.dumps(classify_text(args.text, redact_md_path=redact_md), indent=2, sort_keys=True))
        return 0
    if args.privacy_command == "redact":
        cleaned, finding = redact_file(Path(args.path), redact_md_path=redact_md)
        if args.suggest:
            print(cleaned)
        elif finding:
            print(format_findings([finding]), end="")
        else:
            print("No PrivacyGuard findings.")
        return 1 if finding else 0
    if args.privacy_command == "report":
        findings = scan_path(root / "docs", redact_md_path=redact_md)
        print(format_findings(findings, format=args.format), end="")
        return 1 if findings and args.strict else 0
    print("✘ unknown privacy command")
    return 1


def cmd_route(args: argparse.Namespace) -> int:
    from zeref.routing.policy import classify_task, policy_json, route_report, validate_policy

    if args.route_command == "classify":
        decision = classify_task(args.text)
        print(json.dumps(decision.to_dict(), indent=2, sort_keys=True))
        return 0
    if args.route_command == "explain":
        decision = classify_task(args.text)
        print(f"{decision.domain} / {decision.weight} / {decision.lead}\n{decision.reason}")
        return 0
    if args.route_command == "policy":
        if args.policy_command == "show":
            print(policy_json(), end="")
            return 0
        if args.policy_command == "validate":
            issues = validate_policy()
            print("Route policy valid." if not issues else "\n".join(issues))
            return 1 if issues else 0
    if args.route_command == "report":
        print(route_report(), end="")
        return 0
    print("✘ unknown route command")
    return 1


def cmd_release(args: argparse.Namespace) -> int:
    from zeref.release.checks import format_release, release_passed, run_release_check

    if args.release_command == "check":
        findings = run_release_check(_project_root())
        print(format_release(findings, format=args.format), end="")
        return 0 if release_passed(findings) else 1
    print("✘ unknown release command")
    return 1


def cmd_doctor(args: argparse.Namespace) -> int:
    from zeref.release.doctor import doctor_passed, format_doctor, run_doctor

    checks = run_doctor(_project_root())
    print(format_doctor(checks, format=args.format), end="")
    return 0 if doctor_passed(checks) else 1


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
    print(f"  kind={item.kind} layer={item.layer} entity={item.entity or '(none)'}")
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

    audit_p = sub.add_parser("audit", help="Structural validation and audit reports")
    audit_sub = audit_p.add_subparsers(dest="audit_command")
    audit_report = audit_sub.add_parser("report", help="Generate audit report")
    audit_report.add_argument("--since", default="")
    audit_report.add_argument("--format", choices=["text", "md", "json"], default="text")

    init_p = sub.add_parser("init", help="Scaffold memory/ + config/ + privacy templates")
    init_p.add_argument("--directory", help="Target dir (default: cwd)")
    init_p.add_argument("--name", help="Project name (non-interactive)")
    init_p.add_argument("--privacy", choices=["abstract","exact","local-only"])
    init_p.add_argument("--tier", choices=["auto","free","standard","god-mode"])
    init_p.add_argument("--parent", help="Parent project path")

    sub.add_parser("db-status", help="Report backend (sqlite/duckdb) + extras")

    memory = sub.add_parser("memory", help="Structured local memory state")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)

    mem_propose = memory_sub.add_parser("propose", help="Create a guarded memory proposal JSON file")
    mem_propose.add_argument("claim")
    mem_propose.add_argument("--out", default="proposal.json")
    mem_propose.add_argument("--json", action="store_true")

    mem_write = memory_sub.add_parser("write", help="Write a guarded memory proposal")
    mem_write.add_argument("--from", dest="from_path", required=True)
    mem_write.add_argument("--json", action="store_true")

    mem_list_cards = memory_sub.add_parser("list", help="List memory cards")
    mem_list_cards.add_argument("--type")
    mem_list_cards.add_argument("--status")
    mem_list_cards.add_argument("--limit", type=int, default=200)
    mem_list_cards.add_argument("--json", action="store_true")

    mem_show = memory_sub.add_parser("show", help="Show a memory card")
    mem_show.add_argument("id")

    mem_archive = memory_sub.add_parser("archive", help="Archive a memory card")
    mem_archive.add_argument("id")
    mem_archive.add_argument("--json", action="store_true")

    mem_supersede = memory_sub.add_parser("supersede", help="Mark one memory card superseded by another")
    mem_supersede.add_argument("id")
    mem_supersede.add_argument("--with", dest="with_id", required=True)
    mem_supersede.add_argument("--json", action="store_true")

    mem_add = memory_sub.add_parser("add", help="Add a structured memory item")
    mem_add.add_argument("--kind", default="note")
    mem_add.add_argument("--title")
    mem_add.add_argument("--body")
    mem_add.add_argument("--entity")
    mem_add.add_argument("--tag", action="append")
    mem_add.add_argument("--layer", choices=["L0", "L1", "L2", "L3"], default="L1")
    mem_add.add_argument("--source-ref")
    mem_add.add_argument("--confidence", choices=["high", "medium", "low"], default="medium")
    mem_add.add_argument("--authority", choices=["canonical", "confirmed", "inferred", "unknown"], default="unknown")
    mem_add.add_argument("--json", action="store_true")

    mem_search = memory_sub.add_parser("search", help="Search structured memory state")
    mem_search.add_argument("query", nargs="?", default="")
    mem_search.add_argument("--entity")
    mem_search.add_argument("--kind")
    mem_search.add_argument("--layer", choices=["L0", "L1", "L2", "L3"])
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
    mem_update.add_argument("--layer", choices=["L0", "L1", "L2", "L3"])
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

    mem_views = memory_sub.add_parser("views", help="Generate Markdown views from structured state")
    mem_views.add_argument("--json", action="store_true")

    factguard = sub.add_parser("factguard", help="Scan or check unsupported claims")
    fact_sub = factguard.add_subparsers(dest="factguard_command", required=True)
    fact_scan = fact_sub.add_parser("scan", help="Scan Markdown path")
    fact_scan.add_argument("path")
    fact_scan.add_argument("--format", choices=["text", "md"], default="text")
    fact_check = fact_sub.add_parser("check", help="Check one claim")
    fact_check.add_argument("--claim", required=True)
    fact_check.add_argument("--source-ref", action="append")
    fact_check.add_argument("--format", choices=["text", "md"], default="text")
    fact_report = fact_sub.add_parser("report", help="Report on docs/")
    fact_report.add_argument("--format", choices=["text", "md"], default="text")

    evidence = sub.add_parser("evidence", help="Check and manage evidence grades")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    ev_grade = evidence_sub.add_parser("grade", help="Grade a file or text")
    ev_grade.add_argument("path")
    ev_check = evidence_sub.add_parser("check", help="Check memory or docs path")
    ev_check.add_argument("path")
    ev_list = evidence_sub.add_parser("list", help="List memory cards by evidence grade")
    ev_list.add_argument("--grade", required=True, choices=["A", "B", "C", "D", "F"])
    ev_upgrade = evidence_sub.add_parser("upgrade", help="Upgrade card evidence with a source")
    ev_upgrade.add_argument("id")
    ev_upgrade.add_argument("--source", required=True)
    evidence_sub.add_parser("report", help="Report low-evidence memory cards")

    contradictions = sub.add_parser("contradictions", help="Scan and resolve memory conflicts")
    contradictions_sub = contradictions.add_subparsers(dest="contradictions_command", required=True)
    con_scan = contradictions_sub.add_parser("scan", help="Scan memory cards for contradictions")
    con_scan.add_argument("path", nargs="?", default="memory/")
    con_scan.add_argument("--format", choices=["text", "json"], default="text")
    con_list = contradictions_sub.add_parser("list", help="List current contradictions")
    con_list.add_argument("--format", choices=["text", "json"], default="text")
    con_show = contradictions_sub.add_parser("show", help="Show one contradiction")
    con_show.add_argument("id")
    con_resolve = contradictions_sub.add_parser("resolve", help="Resolve a contradiction")
    con_resolve.add_argument("id")
    con_resolve.add_argument("--winner", required=True)
    con_resolve.add_argument("--reason", required=True)
    con_archive = contradictions_sub.add_parser("archive", help="Archive a contradiction")
    con_archive.add_argument("id")

    privacy = sub.add_parser("privacy", help="Scan, classify, and redact sensitive text")
    privacy_sub = privacy.add_subparsers(dest="privacy_command", required=True)
    privacy_scan = privacy_sub.add_parser("scan", help="Scan a path for sensitive material")
    privacy_scan.add_argument("path")
    privacy_scan.add_argument("--format", choices=["text", "json"], default="text")
    privacy_scan.add_argument("--strict", action="store_true")
    privacy_redact = privacy_sub.add_parser("redact", help="Print redacted file content or findings")
    privacy_redact.add_argument("path")
    privacy_redact.add_argument("--suggest", action="store_true")
    privacy_classify = privacy_sub.add_parser("classify", help="Classify a text snippet")
    privacy_classify.add_argument("text")
    privacy_report = privacy_sub.add_parser("report", help="Scan docs/ for sensitive material")
    privacy_report.add_argument("--format", choices=["text", "json"], default="text")
    privacy_report.add_argument("--strict", action="store_true")

    route = sub.add_parser("route", help="Classify tasks against the local routing policy")
    route_sub = route.add_subparsers(dest="route_command", required=True)
    route_classify = route_sub.add_parser("classify", help="Classify a task")
    route_classify.add_argument("text")
    route_explain = route_sub.add_parser("explain", help="Explain a task route")
    route_explain.add_argument("text")
    route_policy = route_sub.add_parser("policy", help="Show or validate route policy")
    route_policy_sub = route_policy.add_subparsers(dest="policy_command", required=True)
    route_policy_sub.add_parser("show", help="Print route policy")
    route_policy_sub.add_parser("validate", help="Validate route policy")
    route_sub.add_parser("report", help="Generate route report")

    release = sub.add_parser("release", help="Run release readiness checks")
    release_sub = release.add_subparsers(dest="release_command", required=True)
    release_check = release_sub.add_parser("check", help="Run local release checks")
    release_check.add_argument("--format", choices=["text", "md", "json"], default="text")

    doctor = sub.add_parser("doctor", help="Run local Zeref health checks")
    doctor.add_argument("--format", choices=["text", "json"], default="text")

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
        "factguard": cmd_factguard,
        "evidence": cmd_evidence,
        "contradictions": cmd_contradictions,
        "privacy": cmd_privacy,
        "route": cmd_route,
        "release": cmd_release,
        "doctor": cmd_doctor,
    }
    handler = handlers.get(args.command)
    if not handler:
        parser.print_help(); sys.exit(1)
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
