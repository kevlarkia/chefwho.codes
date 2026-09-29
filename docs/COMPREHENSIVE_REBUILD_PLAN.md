# Comprehensive Rebuild Plan

**Context:** "While things aren't perfect, we might as well just start messing everything up and rebuild from the ashes."

**Goal:** Build it right the first time with proper documentation, naming conventions, and structure so we don't have to keep doing this over and over.

**Created:** 2026-08-13  
**Status:** Policy Review → Rebuild Strategy → Execution

---

## Current State Assessment

### What We Have Today

| Component | Status | Issues |
| --- | --- | --- |
| **Website** (chefwho.codes) | ✅ Working | ⚠️ Wrong brand colors (PR #30 fixes) |
| **SWM Recovery Toolkit** | ✅ Operational | ✅ Well-structured, good naming |
| **Rose Rocket Engine Mirror** | ✅ Functional | ✅ Clean CI/pytest setup |
| **Migration Docs** (PR #28, #29) | ✅ Complete | ✅ Comprehensive planning |
| **Repository Structure** | ⚠️ Mixed | ⚠️ Inconsistent naming, unclear boundaries |
| **Documentation** | ⚠️ Scattered | ⚠️ Multiple sources of truth |
| **Naming Conventions** | ❌ Inconsistent | ❌ No documented standard |
| **Policies** | ❌ Implicit | ❌ Not explicitly documented |
| **Brand Identity** | ⚠️ Partial | ⚠️ Token register exists, not applied everywhere |

### Pain Points (Why We're Rebuilding)

1. **Inconsistent naming** — Files, folders, branches use different conventions
2. **Scattered policies** — Rules exist in AGENTS.md, SYSTEMS_HEALTH.md, comments, and tribal knowledge
3. **No central governance** — SWM business logic is split across repos, Notion, Drive, chat transcripts
4. **Wrong brand application** — Site doesn't match brand identity
5. **Unclear boundaries** — What belongs in this repo vs. elsewhere?
6. **Documentation debt** — Multiple READMEs, incomplete instructions, stale references
7. **No style guide** — Code style, file organization, commit messages all ad-hoc

---

## Rebuild Philosophy

### Core Principles

1. **Single Source of Truth (SSOT)** — Every piece of information has exactly one canonical home
2. **Convention Over Configuration** — Document standards, then follow them religiously
3. **Explicit Over Implicit** — Write down the unwritten rules
4. **Fail Loud, Not Silent** — Systems should break obviously when misused
5. **Agent-First Documentation** — If an AI can't understand it, it's not clear enough
6. **Build for Maintenance** — Optimize for the 100th change, not the 1st
7. **Brand-Driven Design** — Every visual choice traces back to the brand token register

### What "Built Right" Looks Like

**For Documentation:**
- One README per major component
- Clear hierarchy: Repository README → Component README → Module docs
- Every policy explicitly documented with rationale
- Naming conventions in a single canonical doc
- Examples for every rule

**For Code:**
- Consistent naming across files, functions, variables
- Type safety everywhere (TypeScript strict mode)
- Linting enforced in CI, not optional
- Tests exist for non-trivial logic
- Comments explain *why*, not *what*

**For Structure:**
- Logical folder hierarchy matches mental model
- Related files live together
- Clear boundaries between concerns
- No "misc" or "utils" dumping grounds

**For Brand:**
- All colors sourced from brand token register
- Typography, spacing, and visual hierarchy documented
- No hard-coded colors or magic numbers
- Dark mode / light mode decision explicit

---

## Policy Review and Consolidation

### Current Policies (Scattered)

Let me review all current policies across the codebase:

#### From `AGENTS.md`

**Quality Gates:**
- Markdown lint required
- Workflow lint (actionlint) required
- ESLint for local/PR hygiene
- TypeScript for local/PR hygiene
- Build for local/PR hygiene

**Development Workflow:**
- `cp .env.example .env` first time
- `npm install` before running
- `npm run dev` for local server (http://localhost:3000)

**Repository Boundaries:**
- `app/` → Next.js App Router (personal site)
- `content/blog/` → Markdown blog posts
- `lib/` → Shared TypeScript helpers
- `swm-recovery/` → SWM extraction suite (separate concern)
- `rose-rocket-engine/` → Newsletter toolkit mirror (separate concern)
- `docs/` → Systems health + migration planning

**Gotchas (Implicit Policies):**
- `actionlint` is standalone binary, not npm package
- `markdownlint-cli2` is global npm package
- Blog `[slug]` route uses Next.js 16 async params (must await)
- SWM brand sources are Mac-local, need operator ingest
- AGENTS.md must stay truthful (update in same PR as changes)

#### From `docs/SYSTEMS_HEALTH.md`

**Canonical Surfaces (SSOT):**
- Cognitive governance → Notion (Personal Cognitive Charter v1.1)
- Operating posture → `kevlarkia/swm-system` (GOVERNANCE.md)
- Life archive routing → Notion (CLOUT Intake + Routing Controls)
- Drive filing → Notion (Fernandez Filing System v1.0)
- This site + SWM toolkit → AGENTS.md, README.md, swm-recovery/
- TMI / Codex → Terra-Machina-Imperium/codex, UC7.5 AGENTS.md

**Maintenance Cadence:**
- Weekly: CLOUT inbox/triage, Drive inbox, chat captures
- Monthly: AGENTS/CLAUDE truth pass, draft PR purge
- Quarterly: Filing vs actual disk, plugin/skill inventory
- Annually: Cognitive Charter review

**Failure Modes:**
- Agent hallucinating bootstrap status → stale AGENTS.md
- Good work vanishing → no CLOUT intake
- Duplicate instruction docs → parallel copies
- Endless folder redesign → fatigue reorganization
- SWM recovery stuck → Mac paths not ingested

#### From `swm-recovery/README.md`

**Operating Mode:**
- Extraction operation (not verification or canon gate)
- Extract first, reject never (for conflict/age/governance)
- Canon status irrelevant during recovery
- Do not resolve disagreements or invent content
- Process only supplied or authorized sources

**Evidence Labels (Strict Taxonomy):**
- VERBATIM, SOURCE-SUMMARY, RECONSTRUCTED, INFERRED
- REFERENCE-ONLY, CONFLICTING, INCOMPLETE, UNCERTAIN
- DUPLICATE, SUPERSEDED-CLAIM
- Apply exactly one per extracted item

**Scope Boundary:**
- Isolate SWM business from legal/medical/crisis/private
- Do not fabricate prompts, architecture, or facts

#### From `README.md`

**Security Policies:**
- Never commit production secrets
- Use `.env.example` as contract for env vars
- Store real secrets in deployment platform + GitHub secrets

**Development Workflow:**
- Feature branch from `main`
- Focused changes with clear commit messages
- Open PR and ensure checks pass
- Merge after review

**Contact Form Policies:**
- SendGrid optional (degrades gracefully)
- Required: `CONTACT_RECIPIENT_EMAIL`
- Optional: `CONTACT_SENDER_EMAIL`, `CONTACT_SENDGRID_API_KEY`, rate limit vars

#### From Brand Token Register (`swm-recovery/registers/brand-token-register-document-kit-v2.1.md`)

**Color Tokens (Official):**
- INK `#1A1A1A` — Covers, headers, body text
- PAPER `#FFFFFF` — Body ground
- WARM PANEL `#F5F0EC` — Panels, grids
- WARM BORDER `#ECE7E3` — Panel borders, table rules
- SIGNAL BLUE `#2456C8` — Accent (Gate G2, Jul 8 2026) OKRAM blue-dot lineage
- SEMANTIC RED `#8C2B2B` — Critical callouts, anti-fab markers only
- CRITICAL FILL `#F8EFEF` — Critical callout background
- Heritage Cream `#F7F3EA` — Strategic Weekly Memo legacy only

**Document Kit Policies:**
- Signal Blue sealed Jul 8 2026 (Gate G2 closed)
- Archived accents NOT in use: Growth Green, Amber
- Heritage Navy/Gold/Cream for Strategic Weekly Memo only

#### From Migration Plan (`docs/SWM_ENTERPRISE_MIGRATION_PLAN.md`)

**Phased Approach:**
- Finish Phase N before Phase N+1
- Parallel work within phases OK
- No calendar timelines (capability-driven)
- CLOUT intake before large moves
- Update AGENTS.md in same PR as structural changes

**Decision-Making:**
- 4 decision points identified
- Recommendations provided
- Operator approval required

---

## Naming Convention Standard (NEW)

### Repository-Level Naming

**Repositories:**
- `kebab-case` for repo names
- Example: `chefwho.codes`, `swm-system`, `rose-rocket-engine`

**Branches:**
- Format: `<prefix>/<descriptive-name>-<id>`
- Prefixes: `cursor/`, `docs/`, `feature/`, `fix/`, `refactor/`
- Always lowercase
- Example: `cursor/brand-colors-cream-burgundy-8666`

**Tags:**
- Semantic versioning: `vMAJOR.MINOR.PATCH`
- Example: `v1.0.0`, `v0.1.0`

### File and Folder Naming

**Folders:**
- `kebab-case` for multi-word folders
- Single-word lowercase preferred
- Examples: `app/`, `swm-recovery/`, `rose-rocket-engine/`

**Markdown Files:**
- `SCREAMING_SNAKE_CASE` for top-level meta files
- Examples: `README.md`, `AGENTS.md`, `CHANGELOG.md`, `SECURITY.md`
- `kebab-case` for content files
- Examples: `welcome-to-chefwho-codes.md`, `systems-health.md`
- `UPPER_SNAKE_CASE` for registers/templates
- Examples: `SOURCE-META.md`, `AUTHORIZED_SOURCE_INDEX.md`

**TypeScript/JavaScript:**
- `PascalCase` for React components
- Examples: `ContactForm.tsx`, `BlogPost.tsx`
- `camelCase` for functions, variables
- Examples: `getBlogPosts()`, `contactRecipient`
- `kebab-case` for non-component files
- Examples: `page.tsx`, `layout.tsx`, `route.ts`

**CSS:**
- `kebab-case` for class names
- BEM convention: `.block__element--modifier`
- Examples: `.site-header`, `.nav-list`, `.primary-button`

**Env Vars:**
- `SCREAMING_SNAKE_CASE` with namespace prefix
- Examples: `CONTACT_RECIPIENT_EMAIL`, `CONTACT_SENDGRID_API_KEY`

### Commit Message Convention

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation only
- `style:` — Formatting, missing semicolons (no code change)
- `refactor:` — Code change that neither fixes bug nor adds feature
- `test:` — Adding or updating tests
- `chore:` — Maintenance (deps, build, CI)

**Scope (optional):**
- Component or area: `(blog)`, `(contact)`, `(swm-recovery)`, `(ci)`

**Examples:**
```
feat(blog): add RSS feed generation

fix(contact): handle rate limit correctly

docs(agents): update quality gates section

refactor(globals): consolidate color tokens

chore(deps): bump next to 16.2.4
```

---

## Proposed Rebuild Structure

### Directory Structure (After Rebuild)

```
chefwho.codes/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── app/                    # Next.js 16 App Router
│   ├── (pages)/           # Page routes (NEW grouping)
│   │   ├── page.tsx       # Homepage
│   │   ├── about/
│   │   ├── blog/
│   │   └── contact/
│   ├── api/               # API routes
│   ├── components/        # Shared React components (NEW)
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── not-found.tsx      # 404 page
│
├── content/
│   ├── blog/              # Blog post markdown
│   └── pages/             # Static page content (NEW, if needed)
│
├── lib/                   # Shared TypeScript utilities
│   ├── blog.ts           # Blog post utilities
│   ├── contact.ts        # Contact form utilities
│   └── types.ts          # Shared TypeScript types (NEW)
│
├── public/                # Static assets (NEW)
│   ├── images/
│   ├── fonts/ (if custom fonts)
│   └── favicon.ico
│
├── docs/                  # Repository documentation
│   ├── SYSTEMS_HEALTH.md
│   ├── POLICIES.md (NEW)
│   ├── NAMING_CONVENTIONS.md (NEW)
│   ├── STYLE_GUIDE.md (NEW)
│   ├── SWM_ENTERPRISE_MIGRATION_PLAN.md
│   ├── SWM_MIGRATION_QUICK_REF.md
│   ├── SWM_MIGRATION_CHECKLIST.md
│   └── SWM_MIGRATION_VISUAL.md
│
├── swm-recovery/          # SWM extraction suite (unchanged structure)
│   ├── cursor-plugin/
│   ├── prompts/
│   ├── registers/
│   ├── runs/
│   ├── sources/
│   ├── templates/
│   └── README.md
│
├── rose-rocket-engine/    # Newsletter toolkit mirror (unchanged)
│   └── ...
│
├── tests/                 # Test files (NEW, if adding tests)
│   ├── unit/
│   └── integration/
│
├── scripts/               # Utility scripts (NEW, if needed)
│   └── (deployment, data migration, etc.)
│
├── .env.example           # Environment variable contract
├── .editorconfig
├── .gitignore
├── eslint.config.mjs
├── next.config.ts
├── package.json
├── tsconfig.json
├── AGENTS.md              # Cloud agent instructions
├── README.md              # Repository overview
├── CHANGELOG.md (NEW)     # Version history
├── LICENSE
└── SECURITY.md
```

### New Files to Create

1. **`docs/POLICIES.md`** — Consolidated policy document
2. **`docs/NAMING_CONVENTIONS.md`** — Official naming standard
3. **`docs/STYLE_GUIDE.md`** — Code and visual style guide
4. **`CHANGELOG.md`** — Version history (semantic versioning)
5. **`lib/types.ts`** — Shared TypeScript types
6. **`app/components/`** — Extract shared components from pages
7. **`public/`** — Static assets directory (if not exists)

---

## Rebuild Phases

### Phase 0: Documentation Foundation (START HERE)

**Goal:** Document everything before changing anything.

**Tasks:**
1. Create `docs/POLICIES.md` (consolidate all scattered policies)
2. Create `docs/NAMING_CONVENTIONS.md` (this section)
3. Create `docs/STYLE_GUIDE.md` (code style, visual style, brand application)
4. Create `CHANGELOG.md` (start with v1.0.0 as current state)
5. Update `AGENTS.md` to reference new docs
6. Update `README.md` to reference new docs

**Completion Criteria:**
- All policies documented in one place
- Naming conventions explicit and with examples
- Style guide covers code, visual, and brand
- Cloud agents can find any rule in < 2 clicks

### Phase 1: Code Quality Baseline

**Goal:** Enforce code quality before refactoring.

**Tasks:**
1. Enable TypeScript strict mode (`"strict": true` already set ✅)
2. Add ESLint to CI (currently local only)
3. Add TypeScript check to CI (currently local only)
4. Add build check to CI (currently local only)
5. Fix all existing lint/type errors
6. Document code style rules in `docs/STYLE_GUIDE.md`

**Completion Criteria:**
- CI fails on lint/type/build errors
- No existing errors in main branch
- Code style documented

### Phase 2: Repository Structure Refactor

**Goal:** Reorganize files to match proposed structure.

**Tasks:**
1. Create `app/components/` directory
2. Extract shared components from pages
3. Create `lib/types.ts` for shared types
4. Create `public/` directory (if not exists)
5. Organize static assets
6. Update imports throughout codebase
7. Test that site still works

**Completion Criteria:**
- Directory structure matches proposal
- All imports resolved
- Site builds and runs
- No dead code

### Phase 3: Naming Convention Enforcement

**Goal:** Apply naming conventions everywhere.

**Tasks:**
1. Rename files that don't match convention
2. Rename folders that don't match convention
3. Rename CSS classes to follow BEM
4. Rename env vars to follow convention
5. Update all references
6. Document exceptions (if any)

**Completion Criteria:**
- All files follow naming convention
- No naming exceptions without documented reason
- Grep for old names returns zero results

### Phase 4: Brand Application Complete

**Goal:** Apply SWM brand consistently everywhere.

**Tasks:**
1. Merge PR #30 (cream and burgundy colors)
2. Audit all hard-coded colors
3. Replace with CSS variables from brand tokens
4. Document brand application in `docs/STYLE_GUIDE.md`
5. Add brand color reference to README
6. Test all pages for brand consistency

**Completion Criteria:**
- Zero hard-coded colors outside `:root`
- All colors trace back to brand token register
- Visual style documented

### Phase 5: Documentation Audit

**Goal:** Ensure all documentation is accurate and complete.

**Tasks:**
1. Review every README for accuracy
2. Fix stale references
3. Remove duplicate documentation
4. Cross-link related docs
5. Test all documented procedures
6. Update AGENTS.md for truthfulness

**Completion Criteria:**
- No stale documentation
- No duplicate information
- All procedures tested
- AGENTS.md matches reality

### Phase 6: SWM Business Integration (Decision 1 from Migration Plan)

**Goal:** Bring SWM business docs into this repo (if chosen).

**Tasks:**
1. Operator decides on Decision 1 (business docs home)
2. If Option A (public `swm-business/`):
   - Create `swm-business/` directory
   - Define structure (product/, brand/, gtm/, governance/)
   - Migrate content from `kevlarkia/swm-system`
   - Update links and references
3. Document SWM business boundaries
4. Update AGENTS.md with new locations

**Completion Criteria:**
- Decision 1 resolved
- SWM business docs have canonical home
- No content stranded in chat/Notion
- Agents can locate SWM materials

### Phase 7: Testing Infrastructure (Optional but Recommended)

**Goal:** Add automated tests to prevent regressions.

**Tasks:**
1. Create `tests/` directory
2. Add testing framework (Vitest or Jest)
3. Write unit tests for `lib/` utilities
4. Write integration tests for API routes
5. Add test command to `package.json`
6. Add tests to CI
7. Document testing strategy

**Completion Criteria:**
- Testing framework installed
- Key utilities have tests
- Tests pass in CI
- Testing strategy documented

---

## Acceptance Criteria (Overall Rebuild)

The rebuild is complete when:

1. **All policies are documented** — Zero implicit rules, everything in `docs/POLICIES.md`
2. **Naming is consistent** — 100% compliance with `docs/NAMING_CONVENTIONS.md`
3. **Brand is applied** — All colors from brand token register, documented in style guide
4. **Structure is logical** — Directory layout matches mental model
5. **Documentation is truthful** — AGENTS.md and README.md match reality
6. **Quality gates enforced** — CI blocks bad code, not just local linting
7. **No dead code** — Every file has a purpose, no orphaned utilities
8. **No hard-coded magic** — Colors, dimensions, timing all use named constants
9. **SWM business integrated** — Decision 1 resolved, content has home
10. **You can onboard someone new** — They can read docs and contribute without asking

---

## Rollback Plan

If rebuild goes wrong:

1. **Each phase is a separate PR** — Can revert individual phases
2. **Main branch stays stable** — All work in feature branches
3. **Tag before major changes** — `v1.0.0-pre-rebuild` for safety
4. **Test at each phase** — Site must work before moving to next phase
5. **Document blockers** — Stop and ask for operator input if stuck

---

## Next Actions

1. **Operator reviews this plan** — Approve phases and priority
2. **Execute Phase 0** — Document everything (start immediately)
3. **Create tracking system** — Use `docs/SWM_MIGRATION_CHECKLIST.md` or create new rebuild checklist
4. **One phase at a time** — Don't skip ahead, build foundation first

---

**Philosophy:** "Measure twice, cut once. Document everything, then rebuild methodically."

**Timeline:** Capability-driven, not calendar-driven. Each phase completes when acceptance criteria are met.

**Communication:** Update this plan as we learn. If a phase proves wrong, document why and revise.
