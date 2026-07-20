"""
privacy-audit: allow-file "Task/provenance schema definitions with sha256 field names as spec; no user data."

Common task schema shared by all external benchmark loaders."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Turn:
    """One conversational turn inside a haystack session."""

    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(frozen=True)
class Task:
    """One benchmark item normalized to a common shape.

    - ``sessions``: the memory haystack — a list of sessions, each a list of
      turns, ingested into the memory backend before the question is asked.
    - ``answers``: acceptable gold answers per the benchmark's own key.
    - ``metric``: the benchmark's own scoring metric for this item
      (``exact_match``, ``token_f1``, or ``choice_accuracy``).
    """

    task_id: str
    benchmark: str
    question: str
    answers: tuple[str, ...]
    sessions: tuple[tuple[Turn, ...], ...]
    metric: str
    options: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DatasetCheck:
    """Result of a loader's offline --check validation."""

    ok: bool
    dataset: str
    path: str
    errors: tuple[str, ...]
    task_count: int
    sha256_actual: str | None = None
    sha256_pinned: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "dataset": self.dataset,
            "path": self.path,
            "errors": list(self.errors),
            "task_count": self.task_count,
            "sha256_actual": self.sha256_actual,
            "sha256_pinned": self.sha256_pinned,
        }


class DatasetMissingError(FileNotFoundError):
    """Raised when a dataset directory or file is absent locally."""


def missing_dataset_message(name: str, path: Path, official_url: str, instructions: str) -> str:
    return (
        f"{name} dataset not found at {path}. No network downloads happen "
        f"automatically. Manual download step required: fetch the dataset from "
        f"{official_url} and place it under {path}. {instructions}"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[Any]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
