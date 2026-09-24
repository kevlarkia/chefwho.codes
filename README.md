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
- `/contact`
- `/blog`
- `/blog/[slug]`
- `/bank-accounts` (bank account management)
- `/bank-accounts/[id]` (bank account details)
- `/api/contact` (POST)
- `/api/bank-accounts` (GET, POST)
- `/api/bank-accounts/[id]` (GET, POST)
- `/api/bank-accounts/[id]/archive` (POST)
- `/api/bank-accounts/[id]/send-microdeposits` (POST)
- `/api/bank-accounts/[id]/confirm-microdeposits` (POST)

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

## US Bank Accounts (Stripe Integration)

The application integrates with Stripe's v2 Core Vault API to manage US bank
accounts for ACH payment collection.

### Features

- Add new bank accounts with routing and account numbers
- List all stored bank accounts
- View individual bank account details
- Archive (soft delete) bank accounts
- Verify bank accounts via microdeposits
- Secure storage using Stripe's vault (never stores raw account numbers)

### Required Environment Variables

Get your Stripe API keys from <https://dashboard.stripe.com/apikeys>:

- `STRIPE_SECRET_KEY` - Your Stripe secret key (sk_test_... for test mode)
- `STRIPE_PUBLISHABLE_KEY` - Your Stripe publishable key (pk_test_... for test mode)
- `STRIPE_API_VERSION` - API version (defaults to `2026-08-26.preview`)

### API Endpoints

All bank account endpoints return JSON responses. Successful responses include
`ok: true` and `data` fields. Errors include an `error` field with a
user-friendly message.

#### Create Bank Account

`POST /api/bank-accounts`

Request body:

```json
{
  "account_holder_name": "John Doe",
  "account_holder_type": "individual",
  "account_number": "000123456789",
  "routing_number": "110000000",
  "account_type": "checking"
}
```

#### List Bank Accounts

`GET /api/bank-accounts?limit=10&starting_after=ba_xxx`

Query parameters:

- `limit` (optional, default 10, max 100)
- `starting_after` (optional, bank account ID for pagination)

#### Retrieve Bank Account

`GET /api/bank-accounts/:id`

#### Update Bank Account

`POST /api/bank-accounts/:id`

Request body (all fields optional):

```json
{
  "account_holder_name": "Jane Doe",
  "metadata": {"custom_field": "value"}
}
```

#### Archive Bank Account

`POST /api/bank-accounts/:id/archive`

Soft deletes the bank account, preventing it from being used for new payments.

#### Send Microdeposits

`POST /api/bank-accounts/:id/send-microdeposits`

Initiates microdeposit verification. Stripe will send two small deposits to the
bank account within 1-2 business days.

#### Confirm Microdeposits

`POST /api/bank-accounts/:id/confirm-microdeposits`

Request body:

```json
{
  "amounts": [32, 45]
}
```

Verifies the bank account by confirming the two microdeposit amounts (in cents).

### Frontend Routes

- `/bank-accounts` - Main bank accounts management page
- `/bank-accounts/[id]` - Individual bank account detail page with verification

### Security Notes

- Bank account numbers are never exposed in full (only last 4 digits)
- All sensitive data is stored in Stripe's PCI-compliant vault
- Routing number validation ensures 9-digit format
- Account number validation ensures 4-17 digit format
- Consider adding authentication middleware before production use

### Testing with Stripe Test Mode

Use Stripe's test mode credentials for development:

- Test routing number: `110000000`
- Test account number: `000123456789`
- See <https://stripe.com/docs/testing> for more test data

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
