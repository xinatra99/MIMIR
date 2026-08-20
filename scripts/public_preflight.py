#!/usr/bin/env python3
"""Fail closed on common secrets and private-vault material before release."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SKIP_DIRECTORIES = {".git", "__pycache__", ".venv", "venv", "node_modules"}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".toml", ".yaml", ".yml", ".json", ".py", ".ps1",
    ".sh", ".service", ".ini", ".cfg", ".conf", ".xml", ".js", ".ts",
}
FORBIDDEN_ROOT_DIRECTORIES = {"raw", "journal", "crm", "private", "exports"}
FORBIDDEN_FILENAMES = {".env", "credentials.json", "state.db", "cookies.txt"}
SECRET_PATTERNS = {
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "Telegram bot token": re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def is_example_private_path(relative: Path) -> bool:
    parts = tuple(part.casefold() for part in relative.parts)
    return len(parts) >= 3 and parts[:2] == ("examples", "vault")


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in SKIP_DIRECTORIES for part in relative.parts):
            continue
        yield path, relative


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    findings: list[str] = []

    for name in FORBIDDEN_ROOT_DIRECTORIES:
        if (root / name).exists():
            findings.append(f"forbidden production/private directory at repository root: {name}/")

    for path, relative in iter_files(root):
        if path.name.casefold() in FORBIDDEN_FILENAMES:
            findings.append(f"forbidden credential/state filename: {relative}")

        if relative.parts and relative.parts[0].casefold() in FORBIDDEN_ROOT_DIRECTORIES:
            if not is_example_private_path(relative):
                findings.append(f"private vault path outside fabricated example: {relative}")

        if path.suffix.casefold() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{label} pattern in {relative}:{line}")

    if findings:
        for finding in sorted(set(findings)):
            print(f"ERROR: {finding}")
        print(f"FAILED: {len(set(findings))} release-boundary finding(s)")
        return 1

    print(f"PASS: no obvious secrets or production private-vault directories in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
