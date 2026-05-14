# AGENTS

## Cursor Cloud specific instructions

### Project overview

Next.js 16 personal site (App Router, React 19, TypeScript). No external
services required — blog posts come from `content/blog/*.md` and the
contact form gracefully degrades without SendGrid.

### Quality gates

| Check | Command |
|-------|---------|
| ESLint | `npm run lint` |
| TypeScript | `npm run typecheck` |
| Markdown lint | `markdownlint-cli2 "**/*.md" "#node_modules"` |
| Workflow lint | `actionlint` |
| Build | `npm run build` |

Pre-existing MD041 warning in `.github/PULL_REQUEST_TEMPLATE.md` — safe to
ignore.

### Running the dev server

```bash
cp .env.example .env   # first time only
npm run dev             # http://localhost:3000
```

### Environment variables

Copy `.env.example` to `.env`. See `README.md` § "Contact Form" for the
full list. No secrets are required for local development.

### Gotchas

- `actionlint` is a standalone Go binary installed to `/usr/local/bin`;
  the update script re-downloads it on each session start if missing.
- `markdownlint-cli2` is installed globally via npm.
- When running `markdownlint-cli2` locally, pass `"#node_modules"` to
  exclude `node_modules/`. The CI action handles this automatically.
- The blog `[slug]` route uses Next.js 16 async params — in dev mode
  the `params` object must be awaited (`params` is a `Promise`).
