# chefwho.codes

Personal site and codebase for **chefwho.codes**.

## Stack

- [Next.js](https://nextjs.org/) (App Router)
- React
- TypeScript
- ESLint (flat config via `eslint-config-next`)

## Project Status

This repository includes both foundational engineering standards and a runnable
website scaffold.

## Development Workflow

1. Create a feature branch from `main`.
2. Make focused changes with clear commit messages.
3. Open a pull request and ensure all checks pass.
4. Merge after review.

## Quality Gates

GitHub Actions runs on push and pull request:

- Markdown linting
- GitHub Actions workflow linting (`actionlint`)

## Local Development

### Prerequisites

- Node.js 20+
- npm 10+

### Install

```bash
npm install
```

### Run development server

```bash
npm run dev
```

Open `http://localhost:3000`.

### Build and run production mode

```bash
npm run build
npm run start
```

### Lint

```bash
npm run lint
```

## Security and Secrets

- Never commit production secrets.
- Use `.env.example` as the contract for required environment variables.
- Store real secrets in deployment platform and GitHub repository secrets.

## Routes Included

- `/` (home)
- `/about`
- `/smart-workforce`
- `/swm` (alias redirect)
- `/contact`
- `/blog`
- `/blog/[slug]`
- `/api/contact` (POST)

## Blog Content

Posts are loaded from markdown files in `content/blog`.

Each post file supports front matter:

```md
---
title: "Post title"
date: "2026-05-01"
summary: "One-line summary"
---
```

## Contact Form

The contact form submits to `POST /api/contact`.

Required runtime env var:

- `CONTACT_RECIPIENT_EMAIL` (destination inbox)

Optional env vars:

- `CONTACT_SENDER_EMAIL` (defaults to `no-reply@chefwho.codes`)
- `CONTACT_SENDGRID_API_KEY` (if set, SendGrid is used to deliver email)
- `CONTACT_RATE_LIMIT_WINDOW_SECONDS` (defaults to `60`)
- `CONTACT_RATE_LIMIT_MAX_REQUESTS` (defaults to `5`)

If SendGrid is not configured, the endpoint logs payload server-side and returns
success so local development is unblocked.

## Agent and systems hygiene

- Cursor / cloud agents: see `AGENTS.md` (must stay truthful to the stack).
- Cross-ecosystem maintenance (AI instructions, CLOUT routing, Drive/disk
  tidy): see `docs/SYSTEMS_HEALTH.md`.
- SWM recovery toolkit: see `swm-recovery/README.md`.
- **SWM enterprise migration:** see `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md`
  and `docs/SWM_MIGRATION_QUICK_REF.md`.

## Enterprise Context

This repository is part of the **SWa Works** GitHub enterprise
(<https://github.com/enterprises/swa-works>). The Chefwho.Codes organization
is the first member org. See migration plan for consolidation strategy.

## Next Recommended Enhancements

- Add analytics and SEO metadata strategy
- Add automated tests and coverage
