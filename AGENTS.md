# AGENTS

## Cursor Cloud specific instructions

### Project overview

Next.js 16 personal site for **chefwho.codes** (App Router, React 19,
TypeScript). Blog posts live in `content/blog/*.md`. The contact form
degrades gracefully when SendGrid is unset.

The **recovery pipeline** (`swm-recovery/` and `forensic-archive/`) is a
guest in this repo. Its intended house is a separate GitHub organization
(see `docs/RECOVERY_HOUSE.md`). Do not fold it into the public site
product.

This repository is now the operational home for **Smart Workforce
Movement (SWM)** under the **SWa Works** GitHub enterprise. See
`docs/SWM_ENTERPRISE_MIGRATION_PLAN.md` for consolidation strategy,
phases, and timeline.

It also mirrors the **Rose Rocket Engine** newsletter toolkit under
`rose-rocket-engine/` (CI/pytest/changelog staging for upstream
`kevlarkia/rose-rocket-engine`). Cloud agents can land changes here when
they lack write access to that separate repo; see
`rose-rocket-engine/UPSTREAM_APPLY.md`.

The **forensic archive runtime** lives under `forensic-archive/`. It is a
domain-neutral two-pass LLM pipeline (TEMP-ARC-001 extract, TEMP-ARC-002
validate) with an append-only `forensic_archive.sqlite` ledger. SWM is one
profile (`--profile swm`), not the whole toolkit. After a run,
`python3 -m forensic_archive verify <output-dir>` must pass. The OpenAI
provider uses the Responses API (`/v1/responses`) by default and records
`X-Client-Request-Id` plus `x-request-id` on each call.

### Quality gates

| Check | Command | CI |
| --- | --- | --- |
| Markdown lint | `markdownlint-cli2 "**/*.md" "#node_modules"` | Yes |
| Workflow lint | `actionlint` | Yes |
| ESLint | `npm run lint` | Local / PR hygiene |
| TypeScript | `npm run typecheck` | Local / PR hygiene |
| Build | `npm run build` | Local / PR hygiene |
| Forensic archive tests | `pytest` in `forensic-archive/` | Yes |

Pre-existing MD041 warning in `.github/PULL_REQUEST_TEMPLATE.md` — safe
to ignore.

### Running the dev server

```bash
cp .env.example .env   # first time only
npm install
npm run dev            # http://localhost:3000
```

### Environment variables

Copy `.env.example` to `.env`. See `README.md` § "Contact Form" for the
full list. No secrets are required for local development.

### Repository map

| Path | Role |
| --- | --- |
| `app/` | Next.js App Router pages and API routes |
| `content/blog/` | Markdown blog posts |
| `lib/` | Shared TypeScript helpers |
| `swm-recovery/` | SWM extraction suite (prompts, templates, plugin) |
| `rose-rocket-engine/` | Mirrored AI newsletter engine + CI/test staging |
| `forensic-archive/` | Dual-pass LLM archive runtime + SQLite ledger (SWM is one profile) |
| `docs/SYSTEMS_HEALTH.md` | Ecosystem maintenance runbook for AI + operator hygiene |
| `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md` | SWM → chefwho.codes consolidation plan under SWa Works enterprise |
| `docs/RECOVERY_HOUSE.md` | Separate GitHub house for the recovery pipeline (filled org form + inventory) |

### Gotchas

- `actionlint` is a standalone Go binary installed to `/usr/local/bin`;
  the update script re-downloads it on each session start if missing.
- `markdownlint-cli2` is installed globally via npm. When running it
  locally, pass `"#node_modules"` to exclude `node_modules/`.
- The blog `[slug]` route uses Next.js 16 async params — `params` is a
  `Promise` and must be awaited.
- SWM brand sources are authorized but Mac-local (`/Users/fcaf/...`).
  Cloud agents cannot ingest them until the operator runs
  `swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh` and commits
  metadata (content stays gitignored).
- Keep AI instructions truthful. If project status changes, update this
  file in the same PR — stale `AGENTS.md` is high-friction debt.

### Systems health

For cross-tool instruction hygiene, filing structure, and recurring
cleanup cadence, follow `docs/SYSTEMS_HEALTH.md`. Prefer that runbook
over inventing a parallel process.
