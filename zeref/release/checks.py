"""Local release readiness checks."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from zeref.guards.evidence_guard import check_public_docs, check_store
from zeref.guards.fact_guard import scan_path as fact_scan
from zeref.memory import MEMORY_FILES, MemoryRoot
from zeref.memory_state import MemoryStore


@dataclass(frozen=True)
class ReleaseFinding:
    name: str
    status: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def run_release_check(root: Path) -> list[ReleaseFinding]:
    memory_root = MemoryRoot.from_path(root)
    store = MemoryStore(memory_root)
    findings: list[ReleaseFinding] = []
    findings.append(_check_version_file(root))
    findings.append(_check_memory_layout(root))
    findings.append(_check_audit_logs(memory_root))
    findings.append(_check_benchmarks(root))
    findings.append(_check_factguard(root))
    findings.append(_check_evidence(store, root))
    return findings


def format_release(findings: list[ReleaseFinding], *, format: str = "text") -> str:
    if format == "json":
        return json.dumps([finding.to_dict() for finding in findings], indent=2, sort_keys=True) + "\n"
    if format == "md":
        lines = ["# Zeref Release Check", ""]
        for finding in findings:
            lines.append(f"- **{finding.status}** `{finding.name}` - {finding.reason}")
        return "\n".join(lines) + "\n"
    return "\n".join(f"{f.status.upper()} {f.name}: {f.reason}" for f in findings) + "\n"


def release_passed(findings: list[ReleaseFinding]) -> bool:
    return all(finding.status == "pass" for finding in findings)


def _check_version_file(root: Path) -> ReleaseFinding:
    return _pass("version", "zeref/VERSION exists") if (root / "zeref" / "VERSION").exists() else _fail("version", "zeref/VERSION missing")


def _check_memory_layout(root: Path) -> ReleaseFinding:
    missing = [rel for rel in MEMORY_FILES if not (root / rel).exists()]
    if missing:
        if _tracked_memory_scaffold_present(root):
            return _pass(
                "memory_layout",
                "tracked memory scaffold present; runtime memory files are generated locally",
            )
        return _fail("memory_layout", "missing " + ", ".join(missing[:5]))
    return _pass("memory_layout", "required memory files exist")


def _check_audit_logs(memory_root: MemoryRoot) -> ReleaseFinding:
    required = ("writes.jsonl", "reads.jsonl", "routes.jsonl", "guard_failures.jsonl", "redactions.jsonl", "releases.jsonl")
    missing = [name for name in required if not (memory_root.layout.audit_dir / name).exists()]
    if missing:
        if _tracked_memory_scaffold_present(memory_root.root):
            return _pass(
                "audit_logs",
                "tracked memory scaffold present; audit logs are generated locally",
            )
        return _fail("audit_logs", "missing " + ", ".join(missing))
    return _pass("audit_logs", "audit logs present")


def _check_benchmarks(root: Path) -> ReleaseFinding:
    results = root / "benchmarks" / "results.json"
    if not results.exists():
        return _fail("benchmarks", "benchmarks/results.json missing")
    data = json.loads(results.read_text(encoding="utf-8"))
    if data.get("passed") is True or str(data.get("verdict", "")).upper() == "PASS":
        return _pass("benchmarks", "local benchmark report is present and passing")
    return _fail("benchmarks", "local benchmark verdict is not PASS")


def _check_factguard(root: Path) -> ReleaseFinding:
    findings = fact_scan(root / "README.md")
    if findings:
        return _fail("factguard", f"{len(findings)} unsupported public claim(s)")
    return _pass("factguard", "README has no FactGuard findings")


def _check_evidence(store: MemoryStore, root: Path) -> ReleaseFinding:
    store_findings = check_store(store)
    doc_issues = check_public_docs(root / "docs")
    if store_findings or doc_issues:
        return _fail("evidenceguard", f"{len(store_findings) + len(doc_issues)} evidence issue(s)")
    return _pass("evidenceguard", "no release-blocking evidence issues")


def _pass(name: str, reason: str) -> ReleaseFinding:
    return ReleaseFinding(name=name, status="pass", reason=reason)


def _fail(name: str, reason: str) -> ReleaseFinding:
    return ReleaseFinding(name=name, status="fail", reason=reason)


def _tracked_memory_scaffold_present(root: Path) -> bool:
    return (root / "memory" / ".gitkeep").exists() and (root / "memory" / "README.md").exists()
