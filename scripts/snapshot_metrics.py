#!/usr/bin/env python3
"""Emit a point-in-time JSON inventory for an AustinOS-style vault."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def count_files(path: Path, pattern: str = "*") -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob(pattern) if item.is_file())


def loose_raw_files(raw: Path) -> int:
    if not raw.is_dir():
        return 0
    return sum(1 for item in raw.iterdir() if item.is_file())


def snapshot(vault: Path) -> dict[str, object]:
    raw = vault / "raw"
    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "vault": str(vault),
        "wiki_markdown_pages": count_files(vault / "wiki", "*.md"),
        "raw_files": count_files(raw),
        "loose_unprocessed_raw_files": loose_raw_files(raw),
        "journal_markdown_files": count_files(vault / "journal", "*.md"),
        "crm_markdown_files": count_files(vault / "crm", "*.md"),
        "all_markdown_files": count_files(vault, "*.md"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    vault = args.vault.resolve()
    data = snapshot(vault)
    payload = json.dumps(data, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
