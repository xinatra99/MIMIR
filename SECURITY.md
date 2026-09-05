# Security Policy

## Scope

This repository is a public reference implementation. The private AustinOS vault and its credentials are out of scope and are not distributed here.

## Never commit

- `.env` variants or credential stores (only clearly synthetic `.env.example`, `.env.sample`, and `.env.template` files are allowed);
- Telegram bot tokens or chat IDs;
- OpenAI device codes, refresh tokens, or API keys;
- Hermes state databases, sessions, logs, or personal memory;
- `raw/`, `journal/`, or `crm/` content from the production vault;
- ChatGPT exports or other private conversation archives;
- SSH keys, certificates, cookies, or browser profiles.

## Before publication

```bash
python scripts/public_preflight.py .
python scripts/vault_audit.py examples/vault
python scripts/check_markdown_links.py .
gitleaks git --redact --no-banner .
```

CI additionally scans full Git history and tests the release-boundary guard. Review every image manually because automated scanners cannot reliably detect personal information embedded in screenshots.

## Reporting

If you find sensitive information in this public repository, contact Austin BC privately rather than opening an issue that repeats the data.
