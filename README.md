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

## Next Recommended Enhancements

- Add content source for blog posts (MDX or CMS)
- Add analytics and SEO metadata strategy
- Add form backend for contact submissions
- Add automated tests and coverage
