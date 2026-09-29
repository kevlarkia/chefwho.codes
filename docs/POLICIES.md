# Repository Policies

**Last Updated:** 2026-08-13  
**Status:** Consolidated from AGENTS.md, SYSTEMS_HEALTH.md, README.md, and tribal knowledge

This document consolidates ALL repository policies in one canonical location. If a policy isn't documented here, it doesn't exist.

---

## Core Principles

1. **Single Source of Truth** — Every piece of information has exactly one canonical home
2. **Explicit Over Implicit** — All rules must be written down
3. **Fail Loud** — Systems should break obviously when misused, not silently
4. **Agent-First Documentation** — If an AI agent can't understand it from docs, it's not clear enough
5. **Update in Same PR** — Policy changes happen in the same PR as the code they govern

---

## Development Workflow

### Branching Strategy

**Branch Naming:**
- Format: `<prefix>/<descriptive-name>-<id>`
- Prefixes: `cursor/`, `docs/`, `feature/`, `fix/`, `refactor/`
- Always lowercase
- Cloud agent suffix: `-8666`
- Example: `cursor/brand-colors-cream-burgundy-8666`

**Workflow:**
1. Create feature branch from `main`
2. Make focused changes with clear commit messages
3. Open pull request
4. Ensure all CI checks pass
5. Merge after review
6. Delete feature branch after merge

### Commit Message Format

Follow Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**
- `feat(blog): add RSS feed generation`
- `fix(contact): handle rate limit correctly`
- `docs(agents): update quality gates section`

---

## Quality Gates

### Required Checks (CI)

- ✅ **Markdown linting** — `markdownlint-cli2 "**/*.md" "#node_modules"`
- ✅ **Workflow linting** — `actionlint`

### Local/PR Hygiene (Should Pass)

- ⚠️ **ESLint** — `npm run lint`
- ⚠️ **TypeScript** — `npm run typecheck`
- ⚠️ **Build** — `npm run build`

**Policy:** Local hygiene checks SHOULD pass before merging, but don't block CI yet. This will change after Phase 1 of rebuild.

### Pre-existing Warnings

- MD041 warning in `.github/PULL_REQUEST_TEMPLATE.md` is safe to ignore (no heading on first line is intentional for PR template)

---

## Environment Setup

### First-Time Setup

```bash
cp .env.example .env   # Copy environment template
npm install            # Install dependencies
npm run dev            # Start dev server (http://localhost:3000)
```

### Environment Variables

**Required:**
- `CONTACT_RECIPIENT_EMAIL` — Destination inbox for contact form

**Optional:**
- `CONTACT_SENDER_EMAIL` — Defaults to `no-reply@chefwho.codes`
- `CONTACT_SENDGRID_API_KEY` — If set, SendGrid delivers email; else logs only
- `CONTACT_RATE_LIMIT_WINDOW_SECONDS` — Defaults to `60`
- `CONTACT_RATE_LIMIT_MAX_REQUESTS` — Defaults to `5`

**Contract:** `.env.example` defines the contract for all required environment variables. Never add a new env var without updating `.env.example`.

---

## Security Policies

### Secrets Management

1. **Never commit production secrets** — Git history is permanent
2. **Use `.env.example`** — Contract for required env vars, no values
3. **Store real secrets in:**
   - Deployment platform (Vercel, Netlify, etc.)
   - GitHub repository secrets (for CI/CD)
   - Cursor Cloud secrets (for cloud agent runs)

### Secret Rotation

- Document rotation policy when secrets are added
- Rotate immediately if secret is exposed
- Use secret scanning tools (`git-secrets`, GitHub secret scanning)

---

## Repository Structure

### Directory Boundaries

| Path | Purpose | Concerns |
| --- | --- | --- |
| `app/` | Next.js App Router | Personal site UI, routes, API endpoints |
| `content/blog/` | Markdown blog posts | Blog content only, no code |
| `lib/` | Shared TypeScript utilities | Reusable helpers, type-safe |
| `swm-recovery/` | SWM extraction suite | Operational recovery tooling, separate from site |
| `rose-rocket-engine/` | Newsletter toolkit mirror | CI/pytest staging for upstream repo |
| `docs/` | Repository documentation | Systems health, migration, policies, guides |

### Separation of Concerns

- **Personal site** (`app/`, `content/`) — Marketing presence, blog, contact form
- **SWM recovery toolkit** (`swm-recovery/`) — Brand asset extraction, prompt harvesting
- **Rose Rocket Engine** (`rose-rocket-engine/`) — Upstream mirror, cannot push directly
- **Documentation** (`docs/`) — Cross-cutting concerns, maintenance, planning

**Policy:** Do not mix concerns. If a file serves multiple purposes, it belongs in the wrong place.

---

## Documentation Policies

### AGENTS.md Truthfulness

**Rule:** `AGENTS.md` MUST match reality at all times.

**Process:**
1. When making structural changes (new folders, new scripts, new dependencies), update `AGENTS.md` in the SAME PR
2. When changing quality gates or CI, update `AGENTS.md` immediately
3. When deprecating a feature, remove it from `AGENTS.md`
4. Monthly audit: diff `AGENTS.md` against actual repo state

**Failure mode:** Stale `AGENTS.md` causes agents to hallucinate bootstrap steps, invent non-existent commands, or skip necessary setup.

### Canonical Documentation Surfaces

**Do NOT create duplicates.** If tempted to create a new instruction file, first ask: which canonical surface does it update?

| Surface | Location | Purpose |
| --- | --- | --- |
| Cognitive governance | Notion (Personal Cognitive Charter v1.1) | Tone, reasoning, anti-fabrication |
| Operating posture | `kevlarkia/swm-system` → `GOVERNANCE.md` | HELD/TENTATIVE tiers, brand architecture |
| Life archive routing | Notion (CLOUT Intake + Routing Controls) | Capture → route → archive |
| Drive filing | Notion (Fernandez Filing System v1.0) | Google Drive top-level structure |
| This site + SWM toolkit | `AGENTS.md`, `README.md`, `swm-recovery/` | Repo-local agent pass-through |
| Repository policies | `docs/POLICIES.md` (this file) | All development rules |
| Naming conventions | `docs/NAMING_CONVENTIONS.md` | File, folder, variable, commit naming |
| Code/visual style | `docs/STYLE_GUIDE.md` | Code patterns, brand application |

---

## Brand Policies

### Color Usage

**Source of Truth:** `swm-recovery/registers/brand-token-register-document-kit-v2.1.md`

**Official Color Tokens:**
- INK `#1A1A1A` — Body text on light backgrounds
- PAPER `#FFFFFF` — Body ground (white)
- WARM PANEL `#F5F0EC` — Panels, grids
- WARM BORDER `#ECE7E3` — Panel borders, table rules
- SIGNAL BLUE `#2456C8` — Accent (SEALED Jul 8 2026, Gate G2)
- SEMANTIC RED `#8C2B2B` — Burgundy, critical callouts only
- CRITICAL FILL `#F8EFEF` — Critical callout background
- Heritage Cream `#F7F3EA` — Strategic Weekly Memo legacy only
- Heritage Gold `#B08D3C` — Strategic Weekly Memo legacy only
- Heritage Navy `#1B2A4A` — Strategic Weekly Memo legacy only

**Archived (NOT in use):**
- Growth Green `#2E7D5B`
- Amber `#C8772A`

**Policy:**
1. All colors MUST be defined as CSS variables in `app/globals.css` `:root`
2. Never hard-code hex values outside `:root`
3. Use semantic names: `var(--accent)` not `var(--red)`
4. Document rationale for color choice in comments

### Visual Hierarchy

- Typography, spacing, and component styling TBD in `docs/STYLE_GUIDE.md` (Phase 0)

---

## SWM Recovery Policies

### Operating Mode

**Context:** `swm-recovery/` is an extraction operation, not verification or publication.

**Rules:**
1. **Extract first, reject never** — Do not reject material for conflict, age, or governance labels
2. **Canon status irrelevant** — Recovery phase ignores canon gates
3. **Do not resolve disagreements** — Document conflicts, don't pick winners
4. **Do not invent content** — Only process supplied or authorized sources
5. **Process authorized sources only** — See `swm-recovery/sources/brand-assets/AUTHORIZED_SOURCE_INDEX.md`

### Evidence Labels

Apply exactly ONE label per extracted item:

- `VERBATIM` — Direct quote from source
- `SOURCE-SUMMARY` — Paraphrased from source
- `RECONSTRUCTED` — Rebuilt from fragments
- `INFERRED` — Logical deduction from evidence
- `REFERENCE-ONLY` — Cited but not ingested
- `CONFLICTING` — Contradicts other sources
- `INCOMPLETE` — Partial recovery
- `UNCERTAIN` — Low confidence
- `DUPLICATE` — Redundant with other item
- `SUPERSEDED-CLAIM` — Overridden by newer source

### Scope Boundary

**IN SCOPE:** SWM business material (brand, product, architecture, prompts, workflows)

**OUT OF SCOPE:** Legal, medical, crisis, private relationship material

**Policy:** Do not fabricate missing prompts, architecture, or business facts. Document gaps instead.

---

## Migration Policies

### Phased Approach

**Rule:** Complete Phase N before starting Phase N+1.

**Process:**
1. Each phase has explicit completion criteria
2. Phases can have parallel tasks within them
3. Create separate PR for each major phase
4. Document blockers immediately, don't guess

### No Calendar Timelines

**Rule:** All timelines are capability-driven, not date-driven.

**Rationale:** Autonomous agents work at variable speeds. Calendar pressure creates rushed, buggy work.

**Alternative:** Describe complexity (simple/moderate/complex) and dependencies.

### CLOUT Intake Before Large Changes

**Rule:** Before major structural changes, capture current state in CLOUT or Linear.

**Rationale:** Good work disappears when only in chat transcripts or uncommitted branches.

**Process:**
1. Document current state (screenshots, file list, decisions made)
2. Create CLOUT intake row (Status = Captured or Routed)
3. Then proceed with large refactor

---

## Next.js 16 Specific Policies

### Async Params

**Context:** Next.js 16 made params and searchParams async.

**Rule:** Always `await params` in page components and route handlers.

**Example:**
```typescript
// ✅ Correct
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  // ...
}

// ❌ Wrong
export default async function Page({ params }: { params: { slug: string } }) {
  const { slug } = params; // Will fail in Next.js 16
  // ...
}
```

---

## Maintenance Cadence

### Weekly
- CLOUT inbox triage
- Google Drive inbox processing
- Chat transcript capture (move valuable artifacts to CLOUT)

### Monthly
- AGENTS.md truth pass (diff against reality)
- README.md truth pass
- Draft PR purge (close or merge stale branches)

### Quarterly
- Filing system vs actual disk audit
- Cursor plugin/skill inventory
- Dependency updates (major versions)

### Annually
- Personal Cognitive Charter review (or after major life change)
- Repository structure review (is it still logical?)

---

## Failure Modes and Prevention

| Symptom | Likely Cause | Prevention | Fix |
| --- | --- | --- | --- |
| Agent hallucinates bootstrap | Stale AGENTS.md | Update in same PR | Audit AGENTS.md monthly |
| Good work vanishes | No CLOUT intake | Intake before session end | Document everything |
| Duplicate instruction docs | Parallel AGENTS/CLAUDE/Notion | Use canonical surfaces | Delete duplicates |
| Endless folder redesign | Fatigue reorganization | Archive aggressively | Search > browse |
| SWM recovery stuck | Mac paths not ingested | Operator ingest script | Run `INGEST_FROM_MAC.sh` |
| Secrets in git history | Forgot .gitignore | Use secret scanning | Rotate + force push (last resort) |
| CI passes, prod fails | Local/CI mismatch | Add missing checks to CI | Sync CI with local |

---

## Policy Amendment Process

**Rule:** Policies can only change via PR to this file.

**Process:**
1. Create feature branch
2. Edit `docs/POLICIES.md`
3. Document rationale in PR description
4. Tag operator for review
5. Merge after approval
6. Announce change in team channel (if multi-person)

**Exceptions:** Typo fixes and formatting do not require operator review.

---

## Questions and Clarifications

If a policy is unclear or contradictory:
1. File an issue in this repo
2. Tag operator (@kevlarkia) for clarification
3. Update this file with the answer

**Do not** invent policy interpretations. When in doubt, ask.

---

## Related Documentation

- `AGENTS.md` — Cloud agent instructions
- `README.md` — Repository overview
- `docs/NAMING_CONVENTIONS.md` — File and variable naming
- `docs/STYLE_GUIDE.md` — Code and visual style
- `docs/SYSTEMS_HEALTH.md` — Ecosystem maintenance
- `docs/COMPREHENSIVE_REBUILD_PLAN.md` — Rebuild strategy

---

**Philosophy:** Explicit policies prevent confusion. If it's not written down, it's not a rule.
