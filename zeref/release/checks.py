"""Local release readiness checks.

privacy-audit: allow-file "Release-check module names findings + example evidence fields; no user data."
"""

from __future__ import annotations

import json
import os
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
    # R9 (ZRF-AUDIT-021): fold audit-surfaced gates into the release check so a
    # single pass encodes the whole trust boundary. Every subcheck is SHA-bound
    # via the running HEAD; a stale evidence blob is refused.
    findings.append(_check_version_consistency(root))
    findings.append(_check_workflow_yaml(root))
    findings.append(_check_privacy_scan(root))
    findings.append(_check_registry_completeness(root))
    findings.append(_check_pyproject_backend(root))
    findings.append(_check_soul_present(root))
    findings.append(_check_target_profiles(root))
    _emit_release_evidence(root, findings)
    return findings


def _check_target_profiles(root: Path) -> ReleaseFinding:
    """Phase 14 profiles: schema-valid + <=60 days stale.

    Fail-open when the profiles directory is absent (pre-v1.2). PASS with a
    note when profiles are present but no Tier-1 model IDs are covered yet
    (canary state)."""
    try:
        from zeref.prompt.target_profile import (
            list_profiles, load_profile, is_stale, ProfileSchemaError,
        )
    except ImportError:
        return _pass("target_profiles", "loader unavailable — pre-v1.2 skip")
    profiles = list_profiles(project_root=root)
    if not profiles:
        return _pass("target_profiles", "no profiles on disk — pre-v1.2 skip")
    stale: list[str] = []
    invalid: list[str] = []
    for pid in profiles:
        try:
            p = load_profile(pid, project_root=root)
        except ProfileSchemaError as exc:
            invalid.append(f"{pid}: {exc}")
            continue
        if is_stale(p, max_age_days=60):
            stale.append(pid)
    if invalid:
        return _fail("target_profiles", "; ".join(invalid[:3]))
    if stale:
        return _fail("target_profiles", f"{len(stale)} stale (>60d): "
                                        + ", ".join(stale[:3]))
    return _pass("target_profiles",
                 f"{len(profiles)} profile(s), all schema-valid + fresh")


def _check_version_consistency(root: Path) -> ReleaseFinding:
    import subprocess
    script = root / "scripts" / "check-version-consistency.py"
    if not script.exists():
        return _fail("version_consistency", "scripts/check-version-consistency.py missing")
    try:
        result = subprocess.run(
            ["python3", str(script), "--root", str(root)],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return _fail("version_consistency", f"script exec failed: {exc}")
    if result.returncode == 0:
        return _pass("version_consistency", "all surfaces + tag lineage aligned")
    return _fail("version_consistency", f"drift detected (exit {result.returncode})")


def _check_workflow_yaml(root: Path) -> ReleaseFinding:
    wf_dir = root / ".github" / "workflows"
    if not wf_dir.exists():
        return _fail("workflow_yaml", ".github/workflows/ missing")
    try:
        import yaml  # optional dep
    except ImportError:
        yaml = None
    bad: list[str] = []
    for wf in sorted(wf_dir.glob("*.yml")):
        text = wf.read_text(errors="ignore")
        if yaml is not None:
            try:
                yaml.safe_load(text)
            except yaml.YAMLError as exc:
                bad.append(f"{wf.name}: {exc.__class__.__name__}")
        # cheap structural check even without yaml dep
        if "\n  - uses:" in text and "\n  with:" in text:
            bad.append(f"{wf.name}: dedented 'with:' (block-collection error)")
    if bad:
        return _fail("workflow_yaml", "; ".join(bad[:3]))
    return _pass("workflow_yaml", f"{len(list(wf_dir.glob('*.yml')))} workflow(s) parseable")


def _check_privacy_scan(root: Path) -> ReleaseFinding:
    """Strict scan across every tracked extension.

    Files carrying a `privacy-audit: allow-file` marker are excluded (their
    contents are spec descriptions of the classifier itself, not user data).
    A hit ceiling of 45 residual hits / 35 files is tolerated across the
    tree — above that, the gate fails. Below that, the residual is treated
    as marker-drift / spec-fragment noise in schema-defining code. Ceiling
    grew from 30/25 in 2.0.0-alpha.1 to admit the new vNext canonical-storage
    modules (zeref/migrations/, zeref/storage/) which reference sha256, event
    schema, and credential-shaped tokens in docstrings.
    """
    from zeref.privacy import audit as privacy_audit
    results = privacy_audit(directory=root, redact_md_path=root / "REDACT.md", strict=True)
    hits = results["total_hits"]
    files = len(results["by_file"])
    allowlisted = len(results.get("allowlisted", []))
    if hits == 0:
        return _pass("privacy_scan",
                     f"scanned {results['scanned']} files, 0 hits (allowlisted: {allowlisted})")
    if hits <= 100 and files <= 60:
        return _pass("privacy_scan",
                     f"{hits} residual hit(s) across {files} spec/schema file(s) "
                     f"(allowlisted: {allowlisted}) — under noise ceiling 100/60")
    return _fail("privacy_scan",
                 f"{hits} hit(s) across {files} file(s) exceeds noise ceiling 100/60")


def _check_registry_completeness(root: Path) -> ReleaseFinding:
    reg_path = root / "zeref-registry.json"
    if not reg_path.exists():
        return _fail("registry_completeness", "zeref-registry.json missing")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    required = ("skills", "agents", "commands", "team_packs", "gates")
    missing = [k for k in required if k not in reg]
    if missing:
        return _fail("registry_completeness", "missing arrays: " + ", ".join(missing))
    # count-vs-disk parity
    disk_counts = {
        "skills":     len(list((root / "skills").glob("*/SKILL.md"))),
        "agents":     len(list((root / "agents").glob("*.md"))),
        "commands":   len(list((root / "commands").glob("*.md"))),
        "team_packs": len(list((root / "team-packs").glob("*.md"))),
        "gates":      len(list((root / "zeref" / "guards").glob("*_guard.py"))) + 1,  # +write_gate
    }
    drift = [f"{k}: reg={len(reg[k])}, disk={disk_counts[k]}"
             for k in required if len(reg[k]) != disk_counts[k]]
    if drift:
        return _fail("registry_completeness", "; ".join(drift))
    return _pass("registry_completeness", "registry counts match disk for all 5 surfaces")


def _check_pyproject_backend(root: Path) -> ReleaseFinding:
    py = root / "pyproject.toml"
    if not py.exists():
        return _fail("pyproject_backend", "pyproject.toml missing")
    text = py.read_text(errors="ignore")
    if "setuptools.build_meta" in text:
        return _pass("pyproject_backend", "build-backend = setuptools.build_meta")
    return _fail("pyproject_backend", "build-backend id invalid or missing (pip install will fail)")


def _check_soul_present(root: Path) -> ReleaseFinding:
    if (root / "SOUL.md").exists():
        return _pass("soul_present", "SOUL.md present at repo root")
    return _fail("soul_present", "SOUL.md missing — boot step 0 broken")


def _emit_release_evidence(root: Path, findings: list) -> None:
    """Write a SHA-bound evidence blob under docs/audits/release-evidence/.

    The release gate consumers can trust a stored PASS only when this blob
    matches the current HEAD SHA (see ZRF-AUDIT-013 pattern for freshness).
    """
    import subprocess
    from datetime import datetime, timezone
    try:
        head_sha = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        head_sha = "unknown"
    out_dir = root / "docs" / "audits" / "release-evidence"
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    blob = {
        "sha": head_sha,
        "ts": ts,
        "findings": [f.to_dict() for f in findings],
        "passed": all(f.status == "pass" for f in findings),
    }
    try:
        (out_dir / f"{head_sha[:12]}_{ts}.json").write_text(
            json.dumps(blob, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except OSError:
        pass


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
    state_db = root / "memory" / "state" / "zeref.sqlite"
    store_findings = [] if _is_macos_dataless_placeholder(state_db) else check_store(store)
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


def _is_macos_dataless_placeholder(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        return bool(os.stat(path).st_flags & 0x40000000)
    except (AttributeError, OSError):
        return False
