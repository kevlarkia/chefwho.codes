# AGENTS

## Cursor Cloud specific instructions

### Project status

This repository is a runnable **Next.js 16 (App Router)** personal site
(`chefwho.codes`) written in TypeScript/React. Runtime dependencies live in
`package.json` and are locked via `package-lock.json`. Standard scripts and
routes are documented in `README.md`.

### Services

There is a single service: the Next.js web app. Routes include `/`,
`/about`, `/contact`, `/blog`, `/blog/[slug]`, and the `POST /api/contact`
endpoint. Blog posts are markdown files in `content/blog`.

### Quality gates (lint / test / build)

Use the scripts in `package.json`:

- **Lint:** `npm run lint` (ESLint flat config via `eslint-config-next`).
- **Typecheck:** `npm run typecheck` (`tsc --noEmit`).
- **Build:** `npm run build` (`next build`).
- **Dev server:** `npm run dev` — serves on `http://localhost:3000`.

There are no automated unit/integration tests in the repo yet.

CI (`.github/workflows/ci.yml`) only runs markdown lint
(`markdownlint-cli2`) and workflow lint (`actionlint`); it does not run the
Node build/lint. Keep any `.md` edits under 80 columns to satisfy the
default markdownlint rules.

### Environment variables

Copy `.env.example` to `.env` for local development. `SITE_URL` plus the
contact-form vars (`CONTACT_RECIPIENT_EMAIL`, `CONTACT_SENDER_EMAIL`, etc.)
are defined there. See `README.md` § "Contact Form" for details.

### Gotchas

- The `POST /api/contact` endpoint is log-only unless
  `CONTACT_SENDGRID_API_KEY` is set: it validates input, logs the payload
  server-side, and returns success so local development is unblocked. No
  real email is sent without SendGrid configured.
- `actionlint` and `markdownlint-cli2` are only needed to reproduce CI
  locally; they are not part of the app's `npm` dependencies.
