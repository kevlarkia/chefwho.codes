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
