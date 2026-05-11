# AGENTS

## Cursor Cloud specific instructions

### Project status

This repository is in bootstrap mode — no application framework or runtime
dependencies exist yet. The `.gitignore` and CI pipeline anticipate a Node.js
stack. See `README.md` § "Next Recommended Setup" for planned next steps.

### Quality gates (lint / test / build)

The only CI checks are linting — no tests or builds to run.

- **Markdown lint:** `markdownlint-cli2 "**/*.md"` — runs on all `.md`
  files. Pre-existing warning in
  `.github/PULL_REQUEST_TEMPLATE.md` (MD041).
- **Workflow lint:** `actionlint` — lints
  `.github/workflows/*.yml`.

### Environment variables

Copy `.env.example` to `.env` for local development. Currently only
`SITE_URL` is defined.

### Gotchas

- `actionlint` is a standalone Go binary installed to `/usr/local/bin`;
  the update script re-downloads it on each session start if missing.
- `markdownlint-cli2` is installed globally via npm.
- There is no `package.json` in the repo yet, so `npm install` at the
  root is a no-op until a web stack is scaffolded.
