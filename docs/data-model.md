# Data Model

## Directory schema

| Path | Owner | Mutability | Purpose |
|---|---|---|---|
| `raw/` | User/importers | Append/move only | Immutable source-of-truth material |
| `raw/processed/` | Ingest workflow | Append | Sources already represented in compiled knowledge |
| `wiki/` | Agent | Mutable | Source summaries and reusable knowledge pages |
| `journal/` | User + private agent | Append/update | Personal reflection and devotional continuity |
| `crm/` | User + private agent | Update | One private relationship record per person |
| `AGENTS.md` | System owner | Controlled | Schema, ingest, query, privacy, and maintenance contract |
| `index.md` | Agent | Regenerated/update | Content-oriented navigation and coverage state |
| `log.md` | Agent | Append-only | Chronology of ingests, queries, and maintenance |

## Wiki frontmatter

```yaml
---
title: Source Ingestion
type: workflow
sources:
  - raw/processed/example-source.md
source_links:
  - https://example.com/source
privacy: public-example
updated: 2026-08-20
---
```

`sources` answers “what preserved vault paths support this page?” `source_links` answers “what external or canonical sources materially support it?” They are deliberately separate.

## Page types

- `source-summary`: faithful representation of one ingested source;
- `concept`: a durable idea recurring across sources;
- `entity`: person, company, tool, product, book, or project;
- `workflow`: repeatable procedure or operating model;
- `synthesis`: higher-level integration across multiple sources;
- `comparison`: explicit contrast between claims, options, or strategies.

## Link model

Obsidian `[[wikilinks]]` create the explicit knowledge graph. Links are not decorative: they represent extension, contradiction, application, provenance, or dependency.

The reference auditor resolves links by page stem and flags missing destinations. The production system also uses human review because two pages with similar titles can still represent distinct concepts.
