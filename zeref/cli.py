"""
zeref.cli — Reference CLI for Zeref OS (Sprint 2).

Commands:
    zeref status          Print hot.md summary + active tier
    zeref write-decision  Append a decision to memory/DECISIONS.md
    zeref grade <claim>   Grade a claim (evidence-grader heuristics + optional LLM)
    zeref audit-privacy   Run deterministic PII audit on memory/
    zeref audit           Structural validation (wraps zeref-validate.py)

All commands are read-only except write-decision.
Wraps litellm for grade if available; degrades gracefully without it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _project_root() -> Path:
    """Walk up from cwd until AGENTS.md found (Zeref OS root)."""
    p = Path.cwd()
    for _ in range(10):
        if (p / "AGENTS.md").exists():
            return p
        p = p.parent
    return Path.cwd()


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
    from zeref.lock import MemoryLock, atomic_append, LockError
    from zeref.privacy import scrub

    root = _project_root()
    path = root / "memory" / "DECISIONS.md"
    redact = root / "REDACT.md"

    title    = args.title    or input("Decision title: ").strip()
    why      = args.why      or input("Why (rationale): ").strip()
    evidence = args.evidence or input("Evidence/source (Enter to skip): ").strip()
    grade    = args.grade    or "medium"
    today    = date.today().isoformat()

    # scrub PII from all user-provided fields before persisting
    title_s,    title_r    = scrub(title, redact, provenance="write-decision/title")
    why_s,      why_r      = scrub(why, redact, provenance="write-decision/why")
    evidence_s, evidence_r = scrub(evidence, redact, provenance="write-decision/evidence")
    total_redacted = title_r.redacted + why_r.redacted + evidence_r.redacted

    entry = (
        f"\n---\n"
        f"**Decision:** {title_s}\n"
        f"**Date:** {today}\n"
        f"**Rationale:** {why_s}\n"
        f"**Evidence:** {evidence_s or '(none provided)'}\n"
        f"**Evidence grade:** {grade}\n"
        f"**Provenance:** zeref-cli write-decision (pii_scrubbed={total_redacted})\n"
        f"---\n"
    )

    # hold single-writer lock, atomic append
    memory_dir = root / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    try:
        with MemoryLock(memory_dir):
            atomic_append(path, entry)
    except LockError as e:
        print(f"✘ {e}")
        return 2

    print(f"✔ Decision appended to {path}")
    print(f"  Title: {title_s} | Date: {today} | Grade: {grade}")
    if total_redacted:
        print(f"  PII scrubbed from inputs: {total_redacted} token(s)")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """v2.5 L5: scaffold memory/ + config/ + privacy templates (no LLM)."""
    root = Path(args.directory).resolve() if args.directory else Path.cwd()
    print(f"\nInitialising Zeref OS layout at {root}")

    for d in [
        "memory",
        "memory/archive",
        "memory/patterns",
        "memory/snapshots",
        "memory/raw",
        "memory/sync/outbound",
        "memory/sync/parent",
        "memory/l0_raw",
        "memory/l1_atoms",
        "memory/l2_scenes",
        "memory/l3_profiles",
        "memory/indexes",
        "memory/views",
        "memory/reports",
        "memory/handoffs",
        "memory/loops",
        "memory/archives",
        "config",
        "skills",
        "skills/drafts",
    ]:
        (root / d).mkdir(parents=True, exist_ok=True)

    # Use `is None` so empty-string CLI args (e.g. --parent "") skip the prompt
    name    = args.name    if args.name    is not None else (input("Project name: ").strip() or "(unnamed)")
    privacy = args.privacy if args.privacy is not None else (input("Privacy mode [abstract/exact/local-only] (default abstract): ").strip() or "abstract")
    tier    = args.tier    if args.tier    is not None else (input("Model tier [auto/free/standard/god-mode] (default auto): ").strip() or "auto")
    parent  = args.parent  if args.parent  is not None else input("Parent project path (Enter if none): ").strip()
    if not name:    name    = "(unnamed)"
    if not privacy: privacy = "abstract"
    if not tier:    tier    = "auto"

    (root / "config" / "PROJECT.md").write_text(
        f"---\nproject_name: \"{name}\"\nproject_root: \"{root}\"\n"
        f"created: \"{date.today().isoformat()}\"\nlast_session: \"\"\n"
        f"active_agents:\n  - memory-keeper\n"
        f"active_skills:\n  - wiki-maintenance\n  - budget-governor\n  - evidence-grader\n"
        f"privacy_mode: {privacy}\nparent_project: {parent or 'null'}\n"
        f"model_tier: {tier}\nbudget_warn_at: 50000\n---\n\n# {name}\n\n"
        f"Project initialised via `zeref init` on {date.today().isoformat()}.\n"
    )

    if not (root / "PRIVACY.md").exists():
        (root / "PRIVACY.md").write_text(
            f"---\nmode: {privacy}\nabstract_rules:\n  strip_pii: true\n"
            f"  strip_internal_paths: true\n  strip_credentials: true\n"
            f"  strip_numbers: false\nlocal_only_blocks:\n  - memory/sync/outbound/\n"
            f"  - memory/sync/parent/\n---\n\n# PRIVACY.md\n\nMode: `{privacy}`.\n"
        )

    if not (root / "config" / "BUDGET.md").exists():
        (root / "config" / "BUDGET.md").write_text(
            f"---\nmodel_tier: {tier}\nalways_on_target_tokens: 2000\n"
            f"warn_at_tokens: 50000\nhard_cap_tokens: 180000\nboundary_first: true\n---\n"
        )

    if not (root / "memory" / "hot.md").exists():
        (root / "memory" / "hot.md").write_text(
            f"# memory/hot.md\n\n*(empty — populated on first /done)*\n"
        )
    for fname in ["index.md", "DECISIONS.md", "OPEN_QUESTIONS.md",
                  "RISKS.md", "CONFLICTS.md", "MEMORY.md"]:
        f = root / "memory" / fname
        if not f.exists():
            f.write_text(f"# {fname}\n")
    pat = root / "memory" / "patterns" / "PATTERNS.jsonl"
    if not pat.exists():
        pat.write_text("")
    from zeref.memory.atom_store import AtomStore
    AtomStore(root).ensure_layout()

    print(f"\n✔ Scaffolded:")
    print(f"  config/PROJECT.md (name={name}, privacy={privacy}, tier={tier})")
    print(f"  memory/ flat + layered layout")
    print(f"  skills/drafts/ (review queue)")
    if parent:
        print(f"  parent: {parent}")
    print(f"\nNext: edit config/PROJECT.md as needed, then `zeref status`.")
    return 0


def cmd_memory(args: argparse.Namespace) -> int:
    """Structured atom memory commands."""
    from zeref.memory.atom_store import AtomStore
    from zeref.memory.schemas import create_atom
    from zeref.privacy import scrub

    root = _project_root()
    store = AtomStore(root)

    if args.memory_command == "add":
        redact = root / "REDACT.md"
        claim, claim_report = scrub(args.claim, redact, provenance="memory/add/claim")
        summary_raw = args.summary or args.claim
        summary, summary_report = scrub(summary_raw, redact, provenance="memory/add/summary")
        source, source_report = scrub(args.source, redact, provenance="memory/add/source")
        provenance_raw = args.provenance or "zeref-cli memory add"
        provenance, provenance_report = scrub(
            provenance_raw,
            redact,
            provenance="memory/add/provenance",
        )
        redacted = (
            claim_report.redacted
            + summary_report.redacted
            + source_report.redacted
            + provenance_report.redacted
        )
        if redacted:
            provenance = f"{provenance} (pii_scrubbed={redacted})"

        atom = create_atom(
            atom_type=args.type,
            claim=claim,
            summary=summary,
            source=source,
            source_type=args.source_type,
            evidence=args.evidence,
            confidence=args.confidence,
            status=args.status,
            entities=args.entity or [],
            tags=args.tag or [],
            links=args.link or [],
            privacy=args.privacy,
            provenance=provenance,
        )
        written = store.append(atom)
        if args.json:
            print(json.dumps(written, indent=2, sort_keys=True))
        else:
            print(f"✔ Atom appended: {written['id']} ({written['type']})")
            if redacted:
                print(f"  PII scrubbed from inputs: {redacted} token(s)")
        return 0

    if args.memory_command == "list":
        atoms = store.load(atom_type=args.type, status=args.status)
        if args.json:
            print(json.dumps(atoms, indent=2, sort_keys=True))
        else:
            for atom in atoms:
                print(f"{atom['id']}\t{atom['type']}\t{atom['status']}\t{atom['claim']}")
            if not atoms:
                print("(no atoms)")
        return 0

    if args.memory_command == "patch":
        updates = {}
        if args.status is not None:
            updates["status"] = args.status
        if args.summary is not None:
            summary, report = scrub(
                args.summary,
                root / "REDACT.md",
                provenance="memory/patch/summary",
            )
            updates["summary"] = summary
            if report.redacted:
                updates["provenance"] = f"zeref-cli memory patch (pii_scrubbed={report.redacted})"
        if not updates:
            print("✘ No patch fields provided.")
            return 2
        patched = store.patch(args.id, updates)
        if args.json:
            print(json.dumps(patched, indent=2, sort_keys=True))
        else:
            print(f"✔ Atom patched: {patched['id']}")
        return 0

    if args.memory_command == "index":
        from zeref.memory.indexer import rebuild_index

        result = rebuild_index(root)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"✔ Indexed {result['atoms_indexed']} atom(s) at {result['path']}")
        return 0

    if args.memory_command == "health":
        from zeref.memory.refine import build_health_report, write_health_report

        result = build_health_report(root)
        if not args.no_write:
            result = {**result, "written": write_health_report(root, result)}
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"Memory health: {'pass' if result['passed'] else 'needs attention'}")
            print(f"Active atoms: {result['summary']['active_atoms']}")
            print(f"Duplicate groups: {result['summary']['duplicate_groups']}")
            if "written" in result:
                print(f"Report: {result['written']['markdown']}")
        return 0 if result["passed"] or not args.strict else 1

    if args.memory_command == "refine":
        from zeref.memory.refine import refine_memory

        result = refine_memory(root, dry_run=args.dry_run, strict=args.strict)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            mode = "dry run" if result["dry_run"] else "report written"
            print(f"Memory refine: {mode}")
            print(f"Proposals: {len(result['proposals'])}")
            for proposal in result["proposals"]:
                print(f"- {proposal['action']}: {proposal.get('atom_id') or ', '.join(proposal.get('atom_ids', []))}")
        return 0 if result["passed"] or not args.strict else 1

    if args.memory_command == "render":
        from zeref.memory.render import render_memory_view

        result = render_memory_view(root, args.view)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            if args.view == "all":
                for item in result["rendered"]:
                    print(f"✔ Rendered {item['view']} -> {item['path']}")
            else:
                print(f"✔ Rendered {result['view']} -> {result['path']}")
        return 0

    print("✘ memory subcommand required")
    return 2


def cmd_recall(args: argparse.Namespace) -> int:
    from zeref.memory.recall import recall

    result = recall(
        _project_root(),
        args.query,
        limit=args.limit,
        atom_type=args.type,
        status=args.status,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["answer"])
        print(f"Evidence: {result['evidence_grade']} | Source: {result['source']}")
        for match in result["matched_atoms"]:
            atom = match["atom"]
            print(f"- {atom['id']} [{atom['type']}/{atom['status']}] {atom['claim']}")
        if result["open_contradictions"]:
            print("Open contradictions:")
            for atom in result["open_contradictions"]:
                print(f"- {atom['id']} {atom['claim']}")
    return 0


def cmd_explain_search(args: argparse.Namespace) -> int:
    from zeref.memory.recall import explain_search

    result = explain_search(
        _project_root(),
        args.query,
        limit=args.limit,
        atom_type=args.type,
        status=args.status,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Query: {result['query']}")
        print(f"Tokens: {', '.join(result['tokens'])}")
        print(f"Source: {result['source']}")
        for candidate in result["candidates"]:
            print(
                f"- {candidate['id']} score={candidate['score']} "
                f"{candidate['why_selected']}"
            )
    return 0


def cmd_cost(args: argparse.Namespace) -> int:
    from zeref.memory.cost_router import audit_budgets, estimate_tokens, report, route_operation

    root = _project_root()
    if args.cost_command == "estimate":
        result = estimate_tokens(args.text or "")
    elif args.cost_command == "route":
        result = route_operation(
            args.operation,
            text=args.text or "",
            approval=args.approval,
            render_mode=args.render_mode,
            duplicate=args.duplicate,
            status_change=args.status_change,
            public_claim=args.public_claim,
            contradiction=args.contradiction,
        )
    elif args.cost_command == "report":
        result = report(root)
    elif args.cost_command == "audit":
        result = audit_budgets(root, strict=args.strict)
        if args.strict and not result["passed"]:
            print(json.dumps(result, indent=2, sort_keys=True))
            return 1
    else:
        print("✘ cost subcommand required")
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_evidence(args: argparse.Namespace) -> int:
    from zeref.memory.evidence import audit_evidence, grade_claim

    if args.evidence_command == "grade":
        result = grade_claim(args.claim, source=args.source or "", source_type=args.source_type)
    elif args.evidence_command == "audit":
        result = audit_evidence(_project_root())
    else:
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("passed", True) else 1


def cmd_facts(args: argparse.Namespace) -> int:
    from zeref.memory.fact_guard import audit_facts

    result = audit_facts(_project_root())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


def cmd_contradictions(args: argparse.Namespace) -> int:
    from zeref.memory.contradictions import (
        list_contradictions,
        propose_resolution,
        resolve_contradiction,
        scan_contradictions,
        show_contradiction,
    )

    root = _project_root()
    if args.contradictions_command == "scan":
        result = scan_contradictions(root)
    elif args.contradictions_command == "list":
        result = list_contradictions(root)
    elif args.contradictions_command == "show":
        result = show_contradiction(root, args.id)
    elif args.contradictions_command == "propose":
        result = propose_resolution(root, args.id)
    elif args.contradictions_command == "resolve":
        result = resolve_contradiction(root, args.id, winner=args.winner, reason=args.reason)
    else:
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
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

    mem = sub.add_parser("memory", help="Structured atom memory commands")
    mem_sub = mem.add_subparsers(dest="memory_command", required=True)

    mem_add = mem_sub.add_parser("add", help="Append a validated memory atom")
    mem_add.add_argument("--type", required=True, choices=[
        "fact", "decision", "risk", "task", "preference",
        "contradiction", "source", "error", "test", "event",
    ])
    mem_add.add_argument("--claim", required=True)
    mem_add.add_argument("--summary")
    mem_add.add_argument("--source", required=True)
    mem_add.add_argument("--source-type", choices=[
        "user", "file", "tool", "session", "git", "manual", "unknown",
    ], default="manual")
    mem_add.add_argument("--evidence", choices=["A", "B", "C", "D", "F", "unverified"], default="unverified")
    mem_add.add_argument("--confidence", choices=["high", "medium", "low", "unknown"], default="unknown")
    mem_add.add_argument("--status", choices=["active", "stale", "superseded", "disputed", "archived"], default="active")
    mem_add.add_argument("--privacy", choices=["public-safe", "private", "local-only", "unknown"], default="unknown")
    mem_add.add_argument("--provenance")
    mem_add.add_argument("--entity", action="append")
    mem_add.add_argument("--tag", action="append")
    mem_add.add_argument("--link", action="append")
    mem_add.add_argument("--json", action="store_true")

    mem_list = mem_sub.add_parser("list", help="List memory atoms")
    mem_list.add_argument("--type", choices=[
        "fact", "decision", "risk", "task", "preference",
        "contradiction", "source", "error", "test", "event",
    ])
    mem_list.add_argument("--status", choices=["active", "stale", "superseded", "disputed", "archived"])
    mem_list.add_argument("--json", action="store_true")

    mem_patch = mem_sub.add_parser("patch", help="Patch one memory atom")
    mem_patch.add_argument("id")
    mem_patch.add_argument("--status", choices=["active", "stale", "superseded", "disputed", "archived"])
    mem_patch.add_argument("--summary")
    mem_patch.add_argument("--json", action="store_true")

    mem_index = mem_sub.add_parser("index", help="Rebuild SQLite memory index")
    mem_index.add_argument("--json", action="store_true")

    mem_health = mem_sub.add_parser("health", help="Generate memory health reports")
    mem_health.add_argument("--json", action="store_true")
    mem_health.add_argument("--strict", action="store_true")
    mem_health.add_argument("--no-write", action="store_true", help="Report without writing memory/reports")

    mem_refine = mem_sub.add_parser("refine", help="Propose safe memory cleanup actions")
    mem_refine.add_argument("--dry-run", action="store_true")
    mem_refine.add_argument("--json", action="store_true")
    mem_refine.add_argument("--strict", action="store_true")

    mem_render = mem_sub.add_parser("render", help="Render Markdown views from atoms")
    mem_render.add_argument("view", choices=[
        "hot.md", "index.md", "decisions", "risks", "contradictions", "all",
    ])
    mem_render.add_argument("--json", action="store_true")

    rec = sub.add_parser("recall", help="Recall memory atoms by query")
    rec.add_argument("query")
    rec.add_argument("--limit", type=int, default=5)
    rec.add_argument("--json", action="store_true")
    rec.add_argument("--type", choices=[
        "fact", "decision", "risk", "task", "preference",
        "contradiction", "source", "error", "test", "event",
    ])
    rec.add_argument("--status", choices=["active", "stale", "superseded", "disputed", "archived"], default="active")

    exp = sub.add_parser("explain-search", help="Explain memory search ranking")
    exp.add_argument("query")
    exp.add_argument("--limit", type=int, default=3)
    exp.add_argument("--json", action="store_true")
    exp.add_argument("--type", choices=[
        "fact", "decision", "risk", "task", "preference",
        "contradiction", "source", "error", "test", "event",
    ])
    exp.add_argument("--status", choices=["active", "stale", "superseded", "disputed", "archived"])

    cost = sub.add_parser("cost", help="Estimate and route memory operation cost")
    cost_sub = cost.add_subparsers(dest="cost_command", required=True)
    cost_est = cost_sub.add_parser("estimate", help="Estimate text token cost")
    cost_est.add_argument("--text", default="")

    cost_route = cost_sub.add_parser("route", help="Route an operation to the cheapest safe executor")
    cost_route.add_argument("--operation", required=True)
    cost_route.add_argument("--text", default="")
    cost_route.add_argument("--approval", action="store_true")
    cost_route.add_argument("--render-mode", action="store_true")
    cost_route.add_argument("--duplicate", action="store_true")
    cost_route.add_argument("--status-change", action="store_true")
    cost_route.add_argument("--public-claim", action="store_true")
    cost_route.add_argument("--contradiction", action="store_true")

    cost_sub.add_parser("report", help="Print cost policy summary")
    cost_audit = cost_sub.add_parser("audit", help="Audit artifact token budgets")
    cost_audit.add_argument("--strict", action="store_true")

    evidence = sub.add_parser("evidence", help="Grade and audit evidence")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    evidence_grade = evidence_sub.add_parser("grade", help="Grade a claim")
    evidence_grade.add_argument("claim")
    evidence_grade.add_argument("--source")
    evidence_grade.add_argument("--source-type", default="unknown", choices=[
        "user", "file", "tool", "session", "git", "manual", "unknown",
    ])
    evidence_sub.add_parser("audit", help="Audit atom evidence")

    facts = sub.add_parser("facts", help="Audit unsupported fact claims")
    facts_sub = facts.add_subparsers(dest="facts_command", required=True)
    facts_sub.add_parser("audit", help="Audit atoms for unsupported claims")

    contradictions = sub.add_parser("contradictions", help="Scan and resolve contradictions")
    con_sub = contradictions.add_subparsers(dest="contradictions_command", required=True)
    con_sub.add_parser("scan", help="Create contradiction atoms for detected conflicts")
    con_sub.add_parser("list", help="List contradiction atoms")
    con_show = con_sub.add_parser("show", help="Show one contradiction")
    con_show.add_argument("id")
    con_prop = con_sub.add_parser("propose", help="Propose a resolution")
    con_prop.add_argument("id")
    con_res = con_sub.add_parser("resolve", help="Resolve by explicit winner")
    con_res.add_argument("id")
    con_res.add_argument("--winner", required=True)
    con_res.add_argument("--reason", required=True)

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
        "recall": cmd_recall,
        "explain-search": cmd_explain_search,
        "cost": cmd_cost,
        "evidence": cmd_evidence,
        "facts": cmd_facts,
        "contradictions": cmd_contradictions,
    }
    handler = handlers.get(args.command)
    if not handler:
        parser.print_help(); sys.exit(1)
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
