"""Guarded memory proposal and write pipeline."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from zeref.audit.logger import AuditLogger
from zeref.core.errors import GuardRejection, ValidationError
from zeref.core.schema import SOURCE_OPTIONAL_TYPES
from zeref.memory_state import MemoryStore


@dataclass(frozen=True)
class MemoryProposal:
    claim: str
    type: str = "preference"
    title: str = ""
    privacy_class: str = "internal"
    evidence_grade: str = "C"
    source_refs: list[str] | None = None
    confidence: str = "medium"
    tags: list[str] | None = None
    owner: str = "zeref"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["source_refs"] = self.source_refs or ["user-input"]
        data["tags"] = self.tags or []
        if not data["title"]:
            data["title"] = _title_from_claim(self.claim)
        return data


def propose_memory(claim: str, *, output: Path) -> dict[str, Any]:
    proposal = MemoryProposal(claim=claim).to_dict()
    output.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return proposal


def write_from_proposal(path: Path, store: MemoryStore) -> dict[str, Any]:
    audit = AuditLogger(store.memory_root)
    try:
        proposal = json.loads(path.read_text(encoding="utf-8"))
        _validate_gate(proposal, store)
        card = store.add_card(
            type=proposal["type"],
            title=proposal["title"],
            claim=proposal["claim"],
            privacy_class=proposal["privacy_class"],
            evidence_grade=proposal["evidence_grade"],
            source_refs=list(proposal.get("source_refs") or []),
            confidence=proposal.get("confidence", "medium"),
            tags=list(proposal.get("tags") or []),
            owner=proposal.get("owner", "zeref"),
        )
        store.record_event(
            event="memory-write-accepted",
            payload={"memory_id": card.id, "source": str(path)},
        )
        audit.append(
            event_type="memory_write",
            status="accepted",
            reason="accepted guarded write",
            file=str(path),
            memory_id=card.id,
            guards_run=["factguard", "evidenceguard", "privacyguard", "contradictionguard"],
        )
        return card.to_dict()
    except GuardRejection as exc:
        store.record_event(
            event="memory-write-rejected",
            payload={"source": str(path), "guard": exc.guard, "reason": exc.reason, "fix": exc.fix},
        )
        audit.append(
            event_type="guard_failure",
            status="blocked",
            reason=exc.reason,
            file=str(path),
            guards_run=[exc.guard.lower()],
            payload={"fix": exc.fix},
        )
        audit.append(
            event_type="memory_write",
            status="blocked",
            reason=exc.reason,
            file=str(path),
            guards_run=[exc.guard.lower()],
        )
        raise
    except (KeyError, ValidationError, json.JSONDecodeError) as exc:
        rejection = GuardRejection(
            "WriteGate",
            str(exc),
            "Fix the proposal JSON so it includes valid memory-card fields.",
        )
        store.record_event(
            event="memory-write-rejected",
            payload={"source": str(path), "guard": rejection.guard, "reason": rejection.reason, "fix": rejection.fix},
        )
        audit.append(
            event_type="guard_failure",
            status="blocked",
            reason=rejection.reason,
            file=str(path),
            guards_run=[rejection.guard.lower()],
            payload={"fix": rejection.fix},
        )
        audit.append(
            event_type="memory_write",
            status="blocked",
            reason=rejection.reason,
            file=str(path),
            guards_run=[rejection.guard.lower()],
        )
        raise rejection from exc


def _validate_gate(proposal: dict[str, Any], store: MemoryStore) -> None:
    required = ("type", "claim", "privacy_class", "evidence_grade")
    for field in required:
        if not str(proposal.get(field, "")).strip():
            raise GuardRejection(
                "WriteGate",
                f"The memory proposal is missing `{field}`.",
                f"Add `{field}` to the proposal JSON.",
            )

    privacy_class = proposal["privacy_class"]
    if privacy_class in {"secret", "do_not_store"}:
        raise GuardRejection(
            "PrivacyGuard",
            f"privacy_class `{privacy_class}` cannot be stored.",
            "Use a lower-risk abstraction or do not store this memory.",
        )

    memory_type = proposal["type"]
    source_refs = list(proposal.get("source_refs") or [])
    if memory_type not in SOURCE_OPTIONAL_TYPES and not source_refs:
        raise GuardRejection(
            "EvidenceGuard",
            "The memory claim is factual or decision-like but has no source_refs.",
            "Add at least one source reference or reclassify the memory as assumption or unknown.",
        )

    claim = str(proposal.get("claim", ""))
    lowered = claim.lower()
    if any(phrase in lowered for phrase in ("best memory engine", "beats every", "production-proven", "10/10 on all benchmarks")):
        raise GuardRejection(
            "FactGuard",
            "The memory claim uses unsupported success language.",
            "Rewrite the claim as a sourced, bounded statement.",
        )

    title = str(proposal.get("title") or _title_from_claim(claim)).lower()
    for existing in store.list_cards(status="active"):
        if existing.title.lower() == title and existing.claim.lower() != claim.lower():
            raise GuardRejection(
                "ContradictionGuard",
                "An active memory card with the same title already has a different claim.",
                "Resolve or supersede the existing card before writing this claim.",
            )


def _title_from_claim(claim: str) -> str:
    words = claim.strip().rstrip(".").split()
    return " ".join(words[:8]) or "memory proposal"
