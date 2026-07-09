"""Contradiction detection and explicit resolution."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from zeref.memory.atom_store import AtomStore
from zeref.memory.schemas import create_atom


PAIRS = [
    ("enabled", "disabled"),
    ("true", "false"),
    ("pass", "fail"),
    ("public", "private"),
    ("supported", "unsupported"),
]


def scan_contradictions(root: Path | str = Path(".")) -> dict[str, Any]:
    store = AtomStore(root)
    atoms = [atom for atom in store.load(status="active") if atom["type"] != "contradiction"]
    existing_claims = {atom["claim"] for atom in store.load(atom_type="contradiction")}
    created = []
    for index, left in enumerate(atoms):
        for right in atoms[index + 1:]:
            if not _contradicts(left["claim"], right["claim"]):
                continue
            claim = f"Contradiction between {left['id']} and {right['id']}"
            if claim in existing_claims:
                continue
            contradiction = create_atom(
                atom_type="contradiction",
                claim=claim,
                summary=f"{left['claim']} <> {right['claim']}",
                source="zeref contradictions scan",
                source_type="tool",
                evidence="A",
                confidence="medium",
                status="active",
                links=[
                    {"target_id": left["id"], "relation": "left_claim"},
                    {"target_id": right["id"], "relation": "right_claim"},
                ],
                privacy="private",
                provenance="zeref-cli contradictions scan",
            )
            created.append(store.append(contradiction))
            existing_claims.add(claim)
    return {"created": created, "count": len(created)}


def list_contradictions(root: Path | str = Path(".")) -> list[dict[str, Any]]:
    return AtomStore(root).load(atom_type="contradiction")


def show_contradiction(root: Path | str, contradiction_id: str) -> dict[str, Any]:
    atom = AtomStore(root).get(contradiction_id)
    if atom is None or atom["type"] != "contradiction":
        raise KeyError(contradiction_id)
    return atom


def propose_resolution(root: Path | str, contradiction_id: str) -> dict[str, Any]:
    contradiction = show_contradiction(root, contradiction_id)
    return {
        "id": contradiction_id,
        "proposal": "User arbitration required. Pick a winner with resolve --winner and provide --reason.",
        "linked_claims": contradiction.get("links", []),
    }


def resolve_contradiction(
    root: Path | str,
    contradiction_id: str,
    *,
    winner: str,
    reason: str,
) -> dict[str, Any]:
    if not reason.strip():
        raise ValueError("resolution reason is required")
    store = AtomStore(root)
    contradiction = show_contradiction(root, contradiction_id)
    linked = [link["target_id"] for link in contradiction.get("links", []) if isinstance(link, dict)]
    if winner not in linked:
        raise ValueError("winner must be one of the contradiction linked atom ids")
    superseded = []
    for atom_id in linked:
        if atom_id == winner:
            continue
        superseded.append(store.patch(atom_id, {
            "status": "superseded",
            "provenance": f"superseded by contradiction resolution {contradiction_id}: {reason}",
        }))
    resolved = store.patch(contradiction_id, {
        "status": "archived",
        "summary": f"Resolved winner={winner}. Reason: {reason}",
    })
    return {"resolved": resolved, "winner": winner, "superseded": superseded}


def _contradicts(left: str, right: str) -> bool:
    l_norm = _normalize(left)
    r_norm = _normalize(right)
    if l_norm != r_norm:
        return False
    l_low = left.lower()
    r_low = right.lower()
    return any((a in l_low and b in r_low) or (b in l_low and a in r_low) for a, b in PAIRS)


def _normalize(text: str) -> str:
    lowered = text.lower()
    for a, b in PAIRS:
        lowered = re.sub(rf"\b({a}|{b})\b", "<state>", lowered)
    return re.sub(r"\s+", " ", lowered).strip()
