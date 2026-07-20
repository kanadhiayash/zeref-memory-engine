"""Shared loader plumbing: offline checks and the --check CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

from benchmarks.external.schema import (
    DatasetCheck,
    DatasetMissingError,
    Task,
    missing_dataset_message,
    sha256_file,
)


def require_data_file(
    name: str, data_dir: str | Path, data_filename: str, official_url: str, instructions: str
) -> Path:
    directory = Path(data_dir)
    path = directory / data_filename
    if not path.exists():
        raise DatasetMissingError(
            missing_dataset_message(name, path, official_url, instructions)
        )
    return path


def run_check(
    *,
    name: str,
    data_dir: str | Path,
    data_filename: str,
    official_url: str,
    instructions: str,
    pinned_sha256: str | None,
    load: Callable[[str | Path], list[Task]],
) -> DatasetCheck:
    directory = Path(data_dir)
    errors: list[str] = []
    sha_actual: str | None = None
    task_count = 0
    path = directory / data_filename
    if not path.exists():
        errors.append(missing_dataset_message(name, path, official_url, instructions))
    else:
        sha_actual = sha256_file(path)
        if pinned_sha256 and sha_actual != pinned_sha256:
            errors.append(
                f"checksum mismatch for {path}: expected pinned sha256 "
                f"{pinned_sha256}, got {sha_actual}. The local copy does not "
                "match the pinned dataset version."
            )
        try:
            tasks = load(directory)
            task_count = len(tasks)
            if task_count == 0:
                errors.append(f"{path} parsed but contains zero tasks")
        except DatasetMissingError as exc:
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — surfaced verbatim in check output
            errors.append(f"failed to parse {path}: {exc}")
    return DatasetCheck(
        ok=not errors,
        dataset=name,
        path=str(directory),
        errors=tuple(errors),
        task_count=task_count,
        sha256_actual=sha_actual,
        sha256_pinned=pinned_sha256,
    )


def check_cli(module) -> int:
    parser = argparse.ArgumentParser(description=module.__doc__)
    parser.add_argument("--check", metavar="DATA_DIR", required=True,
                        help="validate a local dataset directory offline (no downloads)")
    args = parser.parse_args()
    result = module.check(args.check)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


def exit_cli(module) -> None:
    sys.exit(check_cli(module))
