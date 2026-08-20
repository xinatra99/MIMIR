#!/usr/bin/env python3
"""Validate repository-local Markdown links and image references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    checked = 0

    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8-sig")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            if not target or target.startswith("#") or target.casefold().startswith(EXTERNAL_SCHEMES):
                continue
            path_part = unquote(target.split("#", 1)[0])
            if not path_part:
                continue
            checked += 1
            resolved = (document.parent / path_part).resolve()
            if not resolved.exists():
                relative_doc = document.relative_to(root)
                errors.append(f"{relative_doc}: missing target '{target}'")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} broken local Markdown link(s)")
        return 1
    print(f"PASS: {checked} local Markdown links resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
