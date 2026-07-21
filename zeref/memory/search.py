"""Deterministic atom search with SQLite FTS and JSONL fallback."""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from zeref.memory.atom_store import AtomStore
from zeref.memory.indexer import INDEX_PATH


def tokenize(query: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9_]+", query)]


def search_atoms(
    root: Path | str,
    query: str,
    *,
    limit: int = 10,
    atom_type: str | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    db_path = root_path / INDEX_PATH
    tokens = tokenize(query)
    if db_path.exists() and tokens and not _index_stale(root_path, db_path):
        try:
            return _search_sqlite(db_path, query, tokens, limit, atom_type, status)
        except sqlite3.Error:
            pass
    return _search_jsonl(root_path, query, tokens, limit, atom_type, status)


def _index_stale(root: Path, db_path: Path) -> bool:
    """True when any atom file changed at/after the index was built.

    Guarantees add -> search coherence: a freshly appended atom is never
    hidden behind a stale SQLite index; we fall back to the canonical JSONL
    scan until `zeref memory index` rebuilds it.
    """
    try:
        index_mtime = db_path.stat().st_mtime
    except OSError:
        return True
    atom_dir = root / "memory" / "l1_atoms"
    if not atom_dir.exists():
        return False
    for path in atom_dir.glob("*.jsonl"):
        try:
            if path.stat().st_mtime >= index_mtime:
                return True
        except OSError:
            continue
    return False


def _search_sqlite(
    db_path: Path,
    query: str,
    tokens: list[str],
    limit: int,
    atom_type: str | None,
    status: str | None,
) -> dict[str, Any]:
    match_query = " OR ".join(tokens)
    filters = []
    params: list[Any] = [match_query]
    if atom_type:
        filters.append("atoms.type = ?")
        params.append(atom_type)
    if status:
        filters.append("atoms.status = ?")
        params.append(status)
    where = " AND " + " AND ".join(filters) if filters else ""
    params.append(limit)
    sql = f"""
        SELECT atoms.raw_json, bm25(atoms_fts) AS rank
        FROM atoms_fts
        JOIN atoms ON atoms_fts.id = atoms.id
        WHERE atoms_fts MATCH ?{where}
        ORDER BY rank
        LIMIT ?
    """
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(sql, params).fetchall()
    finally:
        conn.close()
    matches = []
    for row in rows:
        atom = json.loads(row[0])
        matches.append({
            "atom": atom,
            "score": round(float(row[1]), 6),
            "why": _why(atom, tokens, "SQLite FTS rank"),
        })
    return {
        "query": query,
        "tokens": tokens,
        "source": "sqlite",
        "matches": matches,
    }


def _search_jsonl(
    root: Path,
    query: str,
    tokens: list[str],
    limit: int,
    atom_type: str | None,
    status: str | None,
) -> dict[str, Any]:
    atoms = AtomStore(root).load(atom_type=atom_type, status=status)
    scored = []
    for atom in atoms:
        score = _score_atom(atom, tokens)
        if score > 0 or not tokens:
            scored.append({
                "atom": atom,
                "score": score,
                "why": _why(atom, tokens, "JSONL token scan"),
            })
    scored.sort(key=lambda item: (-item["score"], item["atom"]["created_at"], item["atom"]["id"]))
    return {
        "query": query,
        "tokens": tokens,
        "source": "jsonl",
        "matches": scored[:limit],
    }


def _score_atom(atom: dict[str, Any], tokens: list[str]) -> int:
    haystack = " ".join([
        atom.get("claim", ""),
        atom.get("summary", ""),
        atom.get("source", ""),
        " ".join(str(tag) for tag in atom.get("tags", [])),
    ]).lower()
    return sum(haystack.count(token) for token in tokens)


def _why(atom: dict[str, Any], tokens: list[str], method: str) -> str:
    fields = []
    for field in ("claim", "summary", "source"):
        text = str(atom.get(field, "")).lower()
        if any(token in text for token in tokens):
            fields.append(field)
    return f"{method}; matched fields: {', '.join(fields) if fields else 'none'}"
