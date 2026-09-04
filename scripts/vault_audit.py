#!/usr/bin/env python3
"""Audit structural and provenance invariants in a MIMIR-compatible vault.

The checker intentionally uses only the Python standard library. It validates
deterministic concerns and leaves source interpretation to the agent/human.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_ROOT_FILES = ("AGENTS.md", "index.md", "log.md")
REQUIRED_DIRECTORIES = ("raw", "wiki")
REQUIRED_FRONTMATTER = ("type", "sources", "source_links")
REQUIRED_SECTIONS = (
    "Original Source Links",
    "Raw Note Links",
    "Sources",
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
LOG_HEADING_RE = re.compile(
    r"^\[\d{4}-\d{2}-\d{2}\]\s+"
    r"(?:ingest|journal|crm|query|lint|maintenance)\s+\|\s+.+$"
)


@dataclass
class AuditReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    pages_checked: int = 0
    links_checked: int = 0

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_frontmatter(text: str) -> dict[str, object]:
    """Parse the small YAML subset used for presence validation.

    This is not a general YAML parser. Values remain strings/lists because the
    audit only needs to determine whether required fields are populated.
    """

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}

    result: dict[str, object] = {}
    active_key: str | None = None
    for raw_line in lines[1:end]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.lstrip().startswith("-") and active_key:
            current = result.setdefault(active_key, [])
            if isinstance(current, list):
                current.append(raw_line.split("-", 1)[1].strip().strip('"\''))
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        active_key = key.strip()
        cleaned = value.strip().strip('"\'')
        result[active_key] = cleaned if cleaned else []
    return result


def populated(value: object) -> bool:
    if isinstance(value, list):
        return any(str(item).strip() for item in value)
    return bool(str(value).strip())


def build_title_index(vault: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in vault.rglob("*.md"):
        key = path.stem.casefold()
        index.setdefault(key, []).append(path)
    return index


def audit_structure(vault: Path, report: AuditReport) -> None:
    for name in REQUIRED_ROOT_FILES:
        if not (vault / name).is_file():
            report.error(f"missing root control file: {name}")
    for name in REQUIRED_DIRECTORIES:
        if not (vault / name).is_dir():
            report.error(f"missing required directory: {name}/")


def audit_wiki(vault: Path, report: AuditReport) -> None:
    wiki = vault / "wiki"
    if not wiki.is_dir():
        return

    title_index = build_title_index(vault)
    index_text = read_text(vault / "index.md") if (vault / "index.md").is_file() else ""

    for path in sorted(wiki.rglob("*.md")):
        report.pages_checked += 1
        relative = path.relative_to(vault)
        text = read_text(path)
        metadata = parse_frontmatter(text)

        if not metadata:
            report.error(f"{relative}: missing or invalid YAML frontmatter")
        for field_name in REQUIRED_FRONTMATTER:
            if field_name not in metadata or not populated(metadata[field_name]):
                report.error(f"{relative}: missing populated frontmatter field '{field_name}'")

        headings = set(HEADING_RE.findall(text))
        for section in REQUIRED_SECTIONS:
            if section not in headings:
                report.error(f"{relative}: missing '## {section}' section")

        if f"[[{path.stem}]]" not in index_text:
            report.error(f"{relative}: page is not linked from index.md")

        for target in WIKILINK_RE.findall(text):
            report.links_checked += 1
            normalized = Path(target.strip()).stem.casefold()
            matches = title_index.get(normalized, [])
            if not matches:
                report.error(f"{relative}: unresolved Obsidian link [[{target}]]")
            elif len(matches) > 1:
                locations = ", ".join(str(p.relative_to(vault)) for p in matches)
                report.warn(f"{relative}: ambiguous link [[{target}]] -> {locations}")


def audit_log(vault: Path, report: AuditReport) -> None:
    log_path = vault / "log.md"
    if not log_path.is_file():
        return
    headings = HEADING_RE.findall(read_text(log_path))
    if not headings:
        report.error("log.md: no chronological entries found")
        return
    for heading in headings:
        if not LOG_HEADING_RE.match(heading):
            report.error(f"log.md: invalid entry heading '## {heading}'")


def run(vault: Path) -> AuditReport:
    report = AuditReport()
    audit_structure(vault, report)
    audit_wiki(vault, report)
    audit_log(vault, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", type=Path, help="Path to the vault root")
    args = parser.parse_args()
    vault = args.vault.resolve()

    if not vault.is_dir():
        print(f"ERROR: vault does not exist: {vault}", file=sys.stderr)
        return 2

    report = run(vault)
    print(f"Vault: {vault}")
    print(f"Wiki pages checked: {report.pages_checked}")
    print(f"Obsidian links checked: {report.links_checked}")

    for warning in report.warnings:
        print(f"WARNING: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")

    if report.errors:
        print(f"FAILED: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1

    print(f"PASS: 0 errors, {len(report.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
