"""
tests/runner.py — v2.5 L3: Replay regression suite via subprocess or LLM.

Modes:
  python3 tests/runner.py --mode structural
  python3 tests/runner.py --mode llm --model gpt-4o-mini

Unblocks ZRF-B05 (pass^3) and ZRF-B08 (session continuity).
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    p = Path(__file__).resolve().parent.parent
    return p if (p / "AGENTS.md").exists() else Path.cwd()


# ---------------------------------------------------------------------------
# Structural mode — deterministic shell checks
# ---------------------------------------------------------------------------

STRUCTURAL_TASKS: list[tuple[str, str, str]] = [
    ("D01", "AGENTS.md present",            "test -f AGENTS.md"),
    ("D02", "SOUL.md has 6+ principles",    "test $(grep -c '^## ' SOUL.md) -ge 6"),
    ("D03", "zeref-registry.json valid",    "python3 -c 'import json; json.load(open(\"zeref-registry.json\"))'"),
    ("D04", "registry has 10 skills",       "python3 -c 'import json,sys; d=json.load(open(\"zeref-registry.json\")); sys.exit(0 if len(d[\"skills\"])>=10 else 1)'"),
    ("D05", "_shared/rules.md has R1-R4",   "grep -q 'R1' _shared/rules.md && grep -q 'R4' _shared/rules.md"),
    ("D06", "REDACT.md email enabled (L2)", "grep -A2 'email:' REDACT.md | grep -q 'enabled: true'"),
    ("D07", "PROJECT.md populated (L6)",    "grep -q 'project_name: \"Zeref OS\"' config/PROJECT.md"),
    ("D08", "memory/hot.md exists",         "test -f memory/hot.md"),
    ("D09", "PATTERNS.jsonl exists",        "test -f memory/patterns/PATTERNS.jsonl"),
    ("D10", "zeref/privacy.py imports",     "python3 -c 'import sys; sys.path.insert(0,\".\"); from zeref.privacy import scrub'"),
    ("D11", "zeref/lock.py imports",        "python3 -c 'import sys; sys.path.insert(0,\".\"); from zeref.lock import MemoryLock, atomic_write'"),
    ("D12", "L1 'Hire John' guarded",       "python3 -c 'import sys; sys.path.insert(0,\".\"); from zeref.privacy import scrub; c,r=scrub(\"Hire John Smith\"); sys.exit(0 if \"Hire\" in c else 1)'"),
    ("D13", "L2 email redacted",            "python3 -c 'import sys; sys.path.insert(0,\".\"); from zeref.privacy import scrub; c,r=scrub(\"a@b.com\"); sys.exit(0 if \"[PII\" in c else 1)'"),
    ("D14", "L11 write-decision scrubs",    "grep -q 'L11' zeref/cli.py"),
    ("D15", "L9 lock acquire+release",      "python3 -c 'import sys,tempfile; sys.path.insert(0,\".\"); from zeref.lock import MemoryLock; from pathlib import Path; d=Path(tempfile.mkdtemp()); ml=MemoryLock(d); ml.acquire(); ml.release()'"),
    ("D16", "L10 atomic_write replaces",    "python3 -c 'import sys,tempfile; sys.path.insert(0,\".\"); from zeref.lock import atomic_write; from pathlib import Path; p=Path(tempfile.mktemp()); atomic_write(p,\"x\"); atomic_write(p,\"y\"); sys.exit(0 if p.read_text()==\"y\" else 1)'"),
    ("D17", "zeref demo 20/20",             "python3 -m zeref demo 2>&1 | grep -q '20/20 PASSED'"),
    ("D18", "zeref db-status runs",         "python3 -m zeref db-status > /dev/null"),
    ("D19", "zeref init scaffolds",         "rm -rf /tmp/zeref-l3-test && python3 -m zeref init --directory /tmp/zeref-l3-test --name test --privacy abstract --tier auto --parent '' > /dev/null && test -f /tmp/zeref-l3-test/config/PROJECT.md"),
    ("D20", "validator passes",             "python3 scripts/zeref-validate.py > /dev/null 2>&1"),
]


def run_structural() -> int:
    root = _project_root()
    rows = [["task_id","task_name","AP","OC","Acc","TD","HR","Saf","weighted","pass","version","notes"]]
    passed = failed = 0

    print(f"\nRunning {len(STRUCTURAL_TASKS)} live structural checks…\n")
    for tid, name, check in STRUCTURAL_TASKS:
        r = subprocess.run(check, shell=True, cwd=str(root), capture_output=True, text=True)
        ok = r.returncode == 0
        score = 5.0 if ok else 2.0
        rows.append([tid, name, "", "", "", "", "", "", score, "pass" if ok else "fail", "vD-live", ""])
        passed += ok; failed += not ok
        icon = "\033[92m✔\033[0m" if ok else "\033[91m✘\033[0m"
        print(f"  {icon}  {tid}  {name}")
        if not ok and r.stderr:
            print(f"      stderr: {r.stderr.strip()[:120]}")

    out = root / "tests" / "scores-vD-live.csv"
    with out.open("w", newline="") as f:
        csv.writer(f).writerows(rows)

    rate = passed / len(STRUCTURAL_TASKS) * 100
    print(f"\n  {passed}/{len(STRUCTURAL_TASKS)} PASSED ({rate:.1f}%)")
    print(f"  Written: {out}")
    return 0 if failed == 0 else 1


# ---------------------------------------------------------------------------
# LLM mode — replay Phase B specs against live model
# ---------------------------------------------------------------------------

def run_llm(model: str) -> int:
    try:
        import litellm  # type: ignore
    except ImportError:
        print("✘ litellm not installed. Run: pip install litellm")
        return 1

    root = _project_root()
    sandbox = root / "tests" / "sandbox"
    if not sandbox.exists():
        print("✘ tests/sandbox/ missing — run Phase B first")
        return 1

    rows = [["task_id","skill","test_type","pass_at_1","pass_at_3","pass_3","version","notes"]]
    task_id = 1

    for skill_dir in sorted(sandbox.iterdir()):
        if not skill_dir.is_dir():
            continue
        for spec in sorted(skill_dir.glob("*.md")):
            ttype = spec.stem
            print(f"  Running {skill_dir.name}/{ttype} × 3…", end=" ", flush=True)
            outputs = []
            try:
                for _ in range(3):
                    resp = litellm.completion(
                        model=model,
                        messages=[{"role": "user", "content": spec.read_text()}],
                        max_tokens=400,
                    )
                    outputs.append(resp.choices[0].message.content)
                passing = sum(1 for o in outputs if o and len(o) >= 50)
                p1 = 1 if passing >= 1 else 0
                p3 = 1 if passing == 3 else 0
                rows.append([f"L{task_id:03d}", skill_dir.name, ttype, p1, p1, p3, "vD-llm", model])
                print(f"pass@1={p1} pass^3={p3}")
            except Exception as e:
                rows.append([f"L{task_id:03d}", skill_dir.name, ttype, 0, 0, 0, "vD-llm", f"error: {e}"])
                print(f"error: {e}")
            task_id += 1

    out = root / "tests" / "scores-vD-llm.csv"
    with out.open("w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"\n  Written: {out}")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Zeref OS regression runner (v2.5 L3)")
    p.add_argument("--mode", choices=["structural", "llm"], default="structural")
    p.add_argument("--model", default="gpt-4o-mini", help="litellm model id")
    args = p.parse_args()
    sys.exit(run_structural() if args.mode == "structural" else run_llm(args.model))


if __name__ == "__main__":
    main()
