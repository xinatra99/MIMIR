# Security Policy

## Scope

This repository is a public reference implementation. The private AustinOS vault and its credentials are out of scope and are not distributed here.

## Never commit

- `.env` files or credential stores;
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
```

Review every image manually. Automated scanners cannot reliably detect all personal information embedded in screenshots.

## Reporting

If you find sensitive information in this public repository, contact Austin BC privately rather than opening an issue that repeats the data.
