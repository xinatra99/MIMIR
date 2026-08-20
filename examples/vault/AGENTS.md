# Public Example Vault Contract

## Layers

- `raw/` stores preserved source material.
- `wiki/` stores compiled knowledge.
- `index.md` navigates the compiled layer.
- `log.md` records chronological changes.

## Ingest

1. Read the source without rewriting it.
2. Preserve the canonical URL and literal raw path.
3. Create or update a source-specific wiki page.
4. Add reusable topic pages only when warranted.
5. Cross-link related pages.
6. Update `index.md`.
7. Append `log.md`.
8. Move loose handled sources into `raw/processed/`.

## Required wiki evidence

Every compiled page must include frontmatter with `type`, `sources`, and `source_links`, plus `Original Source Links`, `Raw Note Links`, and `Sources` sections.
