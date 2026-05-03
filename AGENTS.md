## Cursor Cloud specific instructions

- The runnable application lives in `web/` (Next.js App Router). Use that directory as the service root.
- For standard commands, use `web/package.json` scripts (`npm run dev`, `npm run lint`, `npm run test`, `npm run build`) instead of duplicating custom command wrappers.
- `web/AGENTS.md` states this project targets the currently installed Next.js behavior; check `web/node_modules/next/dist/docs/` when making framework-level changes.
