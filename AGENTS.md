# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a single Next.js 16 (App Router) personal site (`chefwho.codes`) with TypeScript. No database, Docker, or external services required for local development.

### Prerequisites

- **Node.js 20+** via nvm at `/home/ubuntu/.nvm`. Load with:
  ```
  export NVM_DIR="/home/ubuntu/.nvm" && source "$NVM_DIR/nvm.sh"
  ```
- **npm 10+** (ships with the nvm-managed Node)

### Key commands

See `package.json` scripts; summary:

| Task | Command |
|------|---------|
| Install deps | `npm install` |
| Dev server | `npm run dev` (port 3000) |
| Lint | `npm run lint` |
| Type check | `npm run typecheck` |
| Prod build | `npm run build` |

### Environment variables

Copy `.env.example` to `.env` before first run. No secrets are required for local development; without `CONTACT_SENDGRID_API_KEY`, the contact form endpoint logs submissions to the console instead of sending email.

### Known caveats

- **Blog detail pages 404 in dev mode**: The dynamic route `app/blog/[slug]/page.tsx` uses `params.slug` directly instead of `await`-ing the `params` promise, which Next.js 16 requires in dev/Turbopack mode. The production build (`npm run build`) pre-renders these pages via `generateStaticParams` and they work correctly. This is a pre-existing code issue.
- **CI pipeline**: GitHub Actions CI (`.github/workflows/ci.yml`) runs markdown linting and actionlint only; it does not run `npm run build`, `lint`, or `typecheck`.
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
