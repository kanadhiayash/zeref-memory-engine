"""
zeref.cli — Reference CLI for Zeref OS (Sprint 2).

Commands:
    zeref status          Print hot.md summary + active tier
    zeref write-decision  Append a decision to memory/DECISIONS.md
    zeref grade <claim>   Grade a claim (evidence-grader heuristics + optional LLM)
    zeref audit-privacy   Run deterministic PII audit on memory/
    zeref audit           Structural validation (wraps zeref-validate.py)
    zeref dashboard       Generate scores HTML dashboard (Sprint 3)
    zeref demo            Run sandbox demo (Sprint 4)

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
    """v2.5: L9 lock + L10 atomic + L11 scrub input before disk write."""
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

    # L11: scrub PII from all user-provided fields before persisting
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

    # L9 + L10: hold lock, atomic append
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

    for d in ["memory", "memory/archive", "memory/patterns", "memory/snapshots",
              "memory/raw", "memory/sync/outbound", "memory/sync/parent",
              "config", "skills", "skills/drafts"]:
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

    print(f"\n✔ Scaffolded:")
    print(f"  config/PROJECT.md (name={name}, privacy={privacy}, tier={tier})")
    print(f"  memory/ flat layout")
    print(f"  skills/drafts/ (review queue)")
    if parent:
        print(f"  parent: {parent}")
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


def cmd_dashboard(args: argparse.Namespace) -> int:
    from zeref.dashboard import generate

    root = _project_root()
    out = Path(args.output) if args.output else root / "tests" / "dashboard.html"
    generate(scores_dir=root / "tests", output_path=out)
    print(f"✔ Dashboard → {out}\n  Open: file://{out.resolve()}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    from zeref.demo import run_demo
    return run_demo()


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="zeref", description="Zeref OS CLI v2.0")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Print hot.md + tier")

    wd = sub.add_parser("write-decision", help="Append decision to memory/DECISIONS.md")
    wd.add_argument("--title");  wd.add_argument("--why")
    wd.add_argument("--evidence"); wd.add_argument("--grade", choices=["high","medium","low"], default="medium")

    gr = sub.add_parser("grade", help="Grade a claim")
    gr.add_argument("claim", nargs="?", default="")

    ap = sub.add_parser("audit-privacy", help="Scan memory/ for PII (read-only)")
    ap.add_argument("--directory", help="Directory to scan (default: memory/)")

    sub.add_parser("audit", help="Structural validation")

    db = sub.add_parser("dashboard", help="Generate HTML score dashboard")
    db.add_argument("--output", help="Output path (default: tests/dashboard.html)")

    sub.add_parser("demo", help="Run sandbox demo (20 regression tasks)")

    # v2.5 L5 — init
    init_p = sub.add_parser("init", help="Scaffold memory/ + config/ + privacy templates")
    init_p.add_argument("--directory", help="Target dir (default: cwd)")
    init_p.add_argument("--name", help="Project name (non-interactive)")
    init_p.add_argument("--privacy", choices=["abstract","exact","local-only"])
    init_p.add_argument("--tier", choices=["auto","free","standard","god-mode"])
    init_p.add_argument("--parent", help="Parent project path")

    # v2.5 L4 — db status
    sub.add_parser("db-status", help="Report backend (sqlite/duckdb) + extras")

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
        "dashboard": cmd_dashboard,
        "demo": cmd_demo,
        "init": cmd_init,           # v2.5 L5
        "db-status": cmd_db_status, # v2.5 L4
    }
    handler = handlers.get(args.command)
    if not handler:
        parser.print_help(); sys.exit(1)
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
