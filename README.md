# chefwho.codes

Personal site and codebase for **chefwho.codes**.

## Project Status

This repository is currently in bootstrap mode with foundational engineering
standards in place:

- repository hygiene files (`.gitignore`, `.editorconfig`, `LICENSE`)
- GitHub collaboration templates (issues + pull request)
- CI checks for markdown and workflow quality
- Dependabot for GitHub Actions updates

## Development Workflow

1. Create a feature branch from `main`.
2. Make focused changes with clear commit messages.
3. Open a pull request and ensure all checks pass.
4. Merge after review.

## Quality Gates

GitHub Actions runs on push and pull request:

- Markdown linting
- GitHub Actions workflow linting (`actionlint`)

## Security and Secrets

- Never commit production secrets.
- Use `.env.example` as the contract for required environment variables.
- Store real secrets in deployment platform and GitHub repository secrets.

## Next Recommended Setup

Pick and scaffold a web stack (for example Next.js, Astro, or Eleventy), then
add:

- runtime version pinning (`.nvmrc`, etc.)
- formatter/linter config for the selected stack
- automated tests and coverage
- deployment workflow (Vercel, Netlify, or GitHub Pages)
