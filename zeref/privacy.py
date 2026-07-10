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
import os
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Homoglyph table — common lookalike substitutions used to evade regex
# ---------------------------------------------------------------------------
_HOMOGLYPHS: dict[str, str] = {
    # lowercase Cyrillic
    "а": "a",   # Cyrillic а  U+0430
    "е": "e",   # Cyrillic е  U+0435
    "о": "o",   # Cyrillic о  U+043E
    "р": "p",   # Cyrillic р  U+0440
    "с": "c",   # Cyrillic с  U+0441
    "х": "x",   # Cyrillic х  U+0445
    "і": "i",   # Cyrillic і  U+0456
    "ӏ": "l",   # Cyrillic ӏ  U+04CF
    "у": "y",   # Cyrillic у  U+0443
    # uppercase Cyrillic — needed to defend AKIA/AIza/PEM-style uppercase patterns
    "А": "A",   # Cyrillic А  U+0410
    "В": "B",   # Cyrillic В  U+0412
    "Е": "E",   # Cyrillic Е  U+0415
    "К": "K",   # Cyrillic К  U+041A
    "М": "M",   # Cyrillic М  U+041C
    "Н": "H",   # Cyrillic Н  U+041D (looks like H)
    "О": "O",   # Cyrillic О  U+041E
    "Р": "P",   # Cyrillic Р  U+0420
    "С": "C",   # Cyrillic С  U+0421
    "Т": "T",   # Cyrillic Т  U+0422
    "Х": "X",   # Cyrillic Х  U+0425
    "І": "I",   # Cyrillic І  U+0406
    "Ѕ": "S",   # Cyrillic Ѕ  U+0405
    "Ј": "J",   # Cyrillic Ј  U+0408
    "У": "Y",   # Cyrillic У  U+0423
    # Greek lookalikes
    "Α": "A",   # Greek Alpha   U+0391
    "Β": "B",   # Greek Beta    U+0392
    "Ε": "E",   # Greek Epsilon U+0395
    "Ζ": "Z",   # Greek Zeta    U+0396
    "Η": "H",   # Greek Eta     U+0397
    "Ι": "I",   # Greek Iota    U+0399
    "Κ": "K",   # Greek Kappa   U+039A
    "Μ": "M",   # Greek Mu      U+039C
    "Ν": "N",   # Greek Nu      U+039D
    "Ο": "O",   # Greek Omicron U+039F
    "Ρ": "P",   # Greek Rho     U+03A1
    "Τ": "T",   # Greek Tau     U+03A4
    "Υ": "Y",   # Greek Upsilon U+03A5
    "Χ": "X",   # Greek Chi     U+03A7
}


# ---------------------------------------------------------------------------
# Provider-shaped credential tokens — high-precision patterns that catch
# specific issuer prefixes regardless of whether a label precedes them.
# Order matters: these are evaluated before the generic credentials regex
# so a structured match wins.
# ---------------------------------------------------------------------------
_PROVIDER_PATTERNS: dict[str, re.Pattern] = {
    "credentials_openai_project": re.compile(
        r"sk-proj-[A-Za-z0-9_\-]{20,}",
    ),
    "credentials_openai_bare": re.compile(
        # bare sk-... but not the project-prefixed form (handled above)
        r"\bsk-(?!proj-)[A-Za-z0-9]{20,}\b",
    ),
    "credentials_github_pat": re.compile(
        r"github_pat_[A-Za-z0-9_]{20,}",
    ),
    "credentials_github_ghp": re.compile(
        r"\bghp_[A-Za-z0-9]{20,}\b",
    ),
    "credentials_slack_bot": re.compile(
        r"\bxoxb-[A-Za-z0-9\-]{10,}\b",
    ),
    "credentials_google_api": re.compile(
        r"\bAIza[A-Za-z0-9_\-]{30,}\b",
    ),
    "credentials_aws_access_key": re.compile(
        r"\bAKIA[A-Z0-9]{16}\b",
    ),
    "credentials_pem_block": re.compile(
        r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY-----"
        r"[\s\S]{1,8192}?"
        r"-----END (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY-----",
    ),
    "credentials_natural_language": re.compile(
        # "API key sk-...", "secret key abc123", "access token xoxb-..."
        r"""(?xi)
        \b(?:api\ key|secret\ key|access\ token)
        \s*[:=]?\s*
        ['"]?
        ([A-Za-z0-9_\-][A-Za-z0-9_\-./+=]{7,})
        ['"]?
        """,
    ),
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
                     Would|Shall|Did|Was|Were|Has|Have|Had|Benchmark|Failure|
                     Analysis)\b)
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

    # Stage 1.5 — provider-shaped credential tokens (always-on, high-precision)
    for name, pattern in _PROVIDER_PATTERNS.items():
        matches = list(pattern.finditer(working))
        if matches:
            report.redacted += len(matches)
            if "credentials" not in report.classes_hit:
                report.classes_hit.append("credentials")
            report.audit_trail.append({
                "class": name,
                "count": len(matches),
                "replacement": "[REDACTED:credentials]",
            })
            working = pattern.sub("[REDACTED:credentials]", working)

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
        if _is_macos_dataless_placeholder(md_file):
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


def _is_macos_dataless_placeholder(path: Path) -> bool:
    """Avoid blocking on cloud-backed files that have metadata but no local bytes."""
    try:
        flags = os.stat(path).st_flags
    except (AttributeError, OSError):
        return False
    # macOS exposes dataless cloud placeholders with an undocumented high bit.
    # Reading those can block while the OS attempts to materialize the file.
    return bool(flags & 0x40000000)
