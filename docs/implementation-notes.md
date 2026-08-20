# Implementation Notes

## What is directly observed

The following facts come from the private AustinOS working tree, Git history, automation definition, runtime diagnostics, and supplied screenshots:

- the initial repository snapshot was created on 2026-05-11;
- the repository has recurring source-processing commits through 2026-08-19;
- the vault uses `raw/`, `wiki/`, `journal/`, and `crm/` plus root `AGENTS.md`, `index.md`, and `log.md`;
- the August snapshot contains 129 wiki pages and 1,374 raw/source files;
- the ChatGPT collection represents 473 conversations;
- the Codex automation is active and scheduled daily at 23:00 local time;
- a successful captured run updated compiled pages, index, and log, then pushed commit `ac9bf42`;
- Hermes is installed in WSL Ubuntu and its gateway user service is enabled and active;
- Hermes has Telegram routing configuration with allowlist and channel-prompt keys.

## What is reconstructed for public use

AustinOS did not store a standalone Python ingestion program in the vault. The agent behavior is primarily encoded as natural-language operational rules in `AGENTS.md` and executed by Codex.

The scripts in this repository are therefore **sanitized reference implementations** of deterministic supporting work:

- structural and provenance auditing;
- point-in-time metrics;
- public-release secret scanning.

They do not pretend to reproduce the LLM's synthesis judgment. This distinction is important: deterministic checks should be code; source interpretation and cross-domain synthesis remain agentic.

## Evolution

The Git history shows the project growing in stages:

1. Initial vault snapshot with Obsidian settings, operating rules, private layers, processed sources, index, and log.
2. Bulk ChatGPT export processing and domain synthesis.
3. Simplenote collection coverage across faith, IT/security certification, AI education, career, and personal operations.
4. Recurring raw-source ingests that update source summaries and durable topic pages.
5. Scheduled Codex processing with scoped commits and automation memory.
6. Hermes gateway integration for agent and messaging access.

## Why Markdown

Markdown makes the knowledge base:

- inspectable without Obsidian;
- diffable in Git;
- searchable with standard tools such as ripgrep;
- readable by multiple agent runtimes;
- portable across local and hosted tooling.

Obsidian is a high-value interface, not a storage dependency.
