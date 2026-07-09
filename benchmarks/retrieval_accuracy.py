"""Retrieval accuracy axis for atom recall and explain-search."""

from __future__ import annotations

import sys

from benchmarks.helpers import add_atom, axis_result, print_json_result, temp_memory_root
from zeref.memory.indexer import rebuild_index
from zeref.memory.recall import explain_search, recall


def run() -> dict:
    with temp_memory_root() as root:
        decision = add_atom(
            root,
            atom_type="decision",
            claim="Use SQLite FTS before optional vector search.",
            source="benchmarks/retrieval_accuracy.py",
            source_type="file",
        )
        add_atom(root, atom_type="risk", claim="Do not load full Markdown memory by default.")
        rebuild_index(root)
        indexed = recall(root, "SQLite FTS", atom_type="decision")
        fallback_db = root / "memory" / "indexes" / "zeref.sqlite"
        fallback_db.unlink()
        fallback = recall(root, "SQLite FTS", atom_type="decision")
        explained = explain_search(root, "SQLite FTS", atom_type="decision")

    indexed_ok = indexed["matched_atoms"][0]["atom"]["id"] == decision["id"]
    fallback_ok = fallback["matched_atoms"][0]["atom"]["id"] == decision["id"]
    explain_ok = explained["candidates"][0]["id"] == decision["id"] and "why_selected" in explained["candidates"][0]
    return axis_result("retrieval_accuracy", {
        "sqlite_indexed_recall": (10.0 if indexed_ok else 0.0, f"top={indexed['matched_atoms'][0]['atom']['id'] if indexed['matched_atoms'] else 'none'}"),
        "jsonl_fallback_recall": (10.0 if fallback_ok else 0.0, f"top={fallback['matched_atoms'][0]['atom']['id'] if fallback['matched_atoms'] else 'none'}"),
        "explain_search": (10.0 if explain_ok else 0.0, f"candidates={len(explained['candidates'])}"),
    })


if __name__ == "__main__":
    sys.exit(print_json_result(run()))
