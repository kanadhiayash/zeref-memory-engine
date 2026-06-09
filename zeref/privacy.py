"""
zeref.privacy — Deterministic PII abstraction module (Sprint 2).

Replaces prose-only privacy-abstraction skill with code-level enforcement.
Reads REDACT.md classes; applies unicode-normalize → base64-decode →
homoglyph-normalize → regex-redact pipeline in that order.

Usage:
    from zeref.privacy import scrub, audit

    clean, report = scrub("My name is John Doe, email: john@example.com")
    print(clean)   # "My name is [PII:pii], email: [PII:email]"
    print(report)  # ScrubReport(redacted=2, classes_hit=['pii', 'email'], ...)
"""

from __future__ import annotations

import base64
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Homoglyph table — common lookalike substitutions used to evade regex
# ---------------------------------------------------------------------------
_HOMOGLYPHS: dict[str, str] = {
    "а": "a",   # Cyrillic а
    "е": "e",   # Cyrillic е
    "о": "o",   # Cyrillic о
    "р": "p",   # Cyrillic р
    "с": "c",   # Cyrillic с
    "х": "x",   # Cyrillic х
    "і": "i",   # Cyrillic і
    "ӏ": "l",   # Cyrillic ӏ
}


# ---------------------------------------------------------------------------
# Built-in regex patterns per REDACT.md class
# ---------------------------------------------------------------------------
_BUILTIN_PATTERNS: dict[str, re.Pattern] = {
    "credentials": re.compile(
        r"""(?xi)
        (?:api[_\-]?key|token|secret|password|passwd|bearer|auth)
        [_\-\s:='"]{0,4}
        [A-Za-z0-9+/=\-_]{8,}
        """,
    ),
    "pii": re.compile(
        r"""(?x)
        (?:
            # v2.5 L1: negative lookahead blocks action verbs as first name token
            \b(?!(?:Hire|Call|Email|Tell|Send|Meet|Ask|See|Visit|With|Hired|Called|
                     Emailed|Told|Sent|Met|Asked|Saw|Visited|Will|Can|May|Should|
                     Would|Shall|Did|Was|Were|Has|Have|Had)\b)
            [A-Z][a-z]{1,20}\ [A-Z][a-z]{1,20}\b      # Firstname Lastname
            | \b\d{3}-\d{2}-\d{4}\b                    # SSN
            | \b\d{3}[.\-\ ]\d{3}[.\-\ ]\d{4}\b        # Phone
        )
        """,
    ),
    "email": re.compile(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    ),
    "internal_paths": re.compile(
        r"""(?x)
        (?:
            /(?:Users|home|var|etc|opt|srv)/[^\s"'<>]+
            | [A-Za-z]:\\[^\s"'<>]+
        )
        """,
    ),
    "client_data": re.compile(
        r"""(?xi)
        \b(?:client|customer|account|contract)[_\- ]?
        (?:id|name|number|ref)[_\- :='"]{0,4}[A-Za-z0-9\-]{3,}
        """,
    ),
    "financial": re.compile(
        r"""(?x)
        (?:
            \b\d{4}[\ \-]?\d{4}[\ \-]?\d{4}[\ \-]?\d{4}\b
            | \$[ ]*\d[\d,]*(?:\.\d{2})?
            | \b(?:IBAN|BIC|SWIFT)[:\s]+[A-Z0-9]{8,34}
        )
        """,
    ),
    "proprietary_code": re.compile(
        r"""(?xi)
        \b(?:
            [A-Z]{2,6}-\d{3,8}
            | v\d+\.\d+\.\d+[-\w]+
        )\b
        """,
    ),
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class RedactClass:
    name: str
    enabled: bool
    replacement: str = "[REDACTED]"
    pattern: Optional[str] = None


@dataclass
class ScrubReport:
    redacted: int = 0
    classes_hit: list[str] = field(default_factory=list)
    provenance: str = ""
    audit_trail: list[dict] = field(default_factory=list)

    def summary(self) -> str:
        if self.redacted == 0:
            return "No PII detected."
        lines = [f"Redacted {self.redacted} token(s) across {len(self.classes_hit)} class(es):"]
        for entry in self.audit_trail:
            lines.append(f"  [{entry['class']}] {entry['count']} hit(s) → {entry['replacement']}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# REDACT.md parser
# ---------------------------------------------------------------------------
def _load_redact_md(path: Path) -> list[RedactClass]:
    """Parse REDACT.md YAML frontmatter into RedactClass list."""
    if not path.exists():
        return [
            RedactClass(name=n, enabled=True, replacement=f"[PII:{n}]")
            for n in _BUILTIN_PATTERNS
        ]

    text = path.read_text()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                data = yaml.safe_load(parts[1])
                if isinstance(data, dict):
                    return _parse_yaml_classes(data)
            except ImportError:
                pass

    # Regex fallback parser
    classes: list[RedactClass] = []
    for m in re.finditer(
        r"-\s+name:\s*(\S+).*?enabled:\s*(true|false)(?:.*?replacement:\s*(.+?))?(?=\s+-\s+name:|\Z)",
        text,
        re.DOTALL,
    ):
        classes.append(RedactClass(
            name=m.group(1),
            enabled=m.group(2) == "true",
            replacement=(m.group(3) or f"[PII:{m.group(1)}]").strip(),
        ))

    return classes or [
        RedactClass(name=n, enabled=True, replacement=f"[PII:{n}]")
        for n in _BUILTIN_PATTERNS
    ]


def _parse_yaml_classes(data: dict) -> list[RedactClass]:
    out: list[RedactClass] = []
    raw = data.get("classes", [])

    # Format A: list of {name, enabled, ...} dicts
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                name = item.get("name", "unknown")
                out.append(RedactClass(
                    name=name,
                    enabled=bool(item.get("enabled", False)),
                    replacement=item.get("replacement", f"[PII:{name}]"),
                    pattern=item.get("pattern"),
                ))
    # Format B: dict of {name: {enabled, patterns, ...}} — actual REDACT.md format
    elif isinstance(raw, dict):
        for name, cfg in raw.items():
            if isinstance(cfg, dict):
                out.append(RedactClass(
                    name=name,
                    enabled=bool(cfg.get("enabled", False)),
                    replacement=cfg.get("replacement", f"[PII:{name}]"),
                    pattern=cfg.get("pattern"),
                ))

    # Fallback: all built-ins enabled
    return out or [
        RedactClass(name=n, enabled=True, replacement=f"[PII:{n}]")
        for n in _BUILTIN_PATTERNS
    ]


# ---------------------------------------------------------------------------
# Core pipeline stages
# ---------------------------------------------------------------------------
def _unicode_normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def _homoglyph_normalize(text: str) -> str:
    return "".join(_HOMOGLYPHS.get(ch, ch) for ch in text)


def _decode_base64_fragments(text: str) -> str:
    """Decode base64-looking blobs (>=16 chars) so downstream regex can catch embedded PII."""
    def _try(m: re.Match) -> str:
        try:
            decoded = base64.b64decode(m.group(0) + "==").decode("utf-8", errors="ignore")
            return decoded if decoded.isprintable() and len(decoded) > 3 else m.group(0)
        except Exception:
            return m.group(0)
    return re.sub(r"[A-Za-z0-9+/]{16,}={0,2}", _try, text)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def scrub(
    text: str,
    redact_md_path: Path = Path("REDACT.md"),
    provenance: str = "",
) -> tuple[str, ScrubReport]:
    """
    Scrub PII from text using the deterministic pipeline.

    Pipeline: unicode-normalize → homoglyph-normalize → base64-decode → regex-redact.
    credentials class is ALWAYS applied regardless of REDACT.md enabled flag.

    Returns (cleaned_text, ScrubReport).
    """
    classes = _load_redact_md(redact_md_path)
    report = ScrubReport(provenance=provenance)

    # Stage 1 — normalise text surface
    working = _unicode_normalize(text)
    working = _homoglyph_normalize(working)
    working = _decode_base64_fragments(working)

    # Stage 2 — apply enabled classes; credentials always-on
    for cls in classes:
        if not cls.enabled and cls.name != "credentials":
            continue
        pattern = (
            re.compile(cls.pattern, re.IGNORECASE | re.VERBOSE)
            if cls.pattern
            else _BUILTIN_PATTERNS.get(cls.name)
        )
        if pattern is None:
            continue
        matches = list(pattern.finditer(working))
        if matches:
            report.redacted += len(matches)
            if cls.name not in report.classes_hit:
                report.classes_hit.append(cls.name)
            report.audit_trail.append({
                "class": cls.name,
                "count": len(matches),
                "replacement": cls.replacement,
            })
            working = pattern.sub(cls.replacement, working)

    return working, report


def audit(
    directory: Path = Path("."),
    redact_md_path: Path = Path("REDACT.md"),
) -> dict:
    """
    Read-only audit: scan markdown files under directory for PII hits.
    Skips skills/, _shared/, agents/, docs/, references/ (spec text).
    Returns {scanned, total_hits, by_file, by_class}.
    """
    _SKIP = {"skills", "_shared", "agents", "docs", "references", "team-packs", "team"}
    results: dict = {"scanned": 0, "total_hits": 0, "by_file": {}, "by_class": {}}

    for md_file in sorted(directory.rglob("*.md")):
        if any(p in md_file.parts for p in _SKIP):
            continue
        text = md_file.read_text(errors="ignore")
        _, report = scrub(text, redact_md_path)
        results["scanned"] += 1
        if report.redacted:
            results["total_hits"] += report.redacted
            results["by_file"][str(md_file)] = report.redacted
            for cls in report.classes_hit:
                results["by_class"][cls] = results["by_class"].get(cls, 0) + 1

    return results
