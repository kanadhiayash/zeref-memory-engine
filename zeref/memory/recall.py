"""Recall and explain-search response formatting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from zeref.memory.search import search_atoms


def recall(
    root: Path | str,
    query: str,
    *,
    limit: int = 5,
    atom_type: str | None = None,
    status: str | None = "active",
) -> dict[str, Any]:
    result = search_atoms(root, query, limit=limit, atom_type=atom_type, status=status)
    matches = result["matches"]
    top = matches[0]["atom"] if matches else None
    contradictions = [
        match["atom"] for match in search_atoms(
            root,
            query,
            limit=limit,
            atom_type="contradiction",
            status="active",
        )["matches"]
    ]
    return {
        "query": query,
        "answer": top["summary"] if top else "No matching memory atom found.",
        "matched_atoms": matches,
        "evidence_grade": top["evidence"] if top else "unverified",
        "source": result["source"],
        "open_contradictions": contradictions,
    }


def explain_search(
    root: Path | str,
    query: str,
    *,
    limit: int = 3,
    atom_type: str | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    result = search_atoms(root, query, limit=limit, atom_type=atom_type, status=status)
    return {
        "query": query,
        "tokens": result["tokens"],
        "source": result["source"],
        "candidates": [
            {
                "id": match["atom"]["id"],
                "type": match["atom"]["type"],
                "status": match["atom"]["status"],
                "score": match["score"],
                "why_selected": match["why"],
                "claim": match["atom"]["claim"],
                "evidence": match["atom"]["evidence"],
            }
            for match in result["matches"]
        ],
    }
