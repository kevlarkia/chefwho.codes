# Naming Conventions

**Last Updated:** 2026-08-13  
**Status:** Official standard for all new code

This document defines the official naming conventions for the `chefwho.codes` repository. All new code MUST follow these conventions. Existing code will be migrated during the rebuild (Phase 3).

---

## Core Principles

1. **Consistency Over Cleverness** — Boring names are better than creative names
2. **Searchability** — Names should be easy to grep
3. **Context-Appropriate** — Use the convention for the context (file vs. variable vs. CSS)
4. **No Abbreviations** — Spell it out (exception: widely-known acronyms like HTTP, API, URL)
5. **Avoid Ambiguity** — `getData` is bad, `getBlogPosts` is good

---

## Repository-Level Naming

### Repository Names

**Convention:** `kebab-case`

**Examples:**
- ✅ `chefwho.codes`
- ✅ `swm-system`
- ✅ `rose-rocket-engine`
- ❌ `ChefWhoCodes` (PascalCase not allowed)
- ❌ `chefwho_codes` (snake_case not allowed)

### Branch Names

**Convention:** `<prefix>/<descriptive-name>-<id>`

**Prefixes:**
- `cursor/` — Cloud agent branches
- `docs/` — Documentation-only changes
- `feature/` — New features
- `fix/` — Bug fixes
- `refactor/` — Code refactoring
- `chore/` — Maintenance (deps, tooling)
- `test/` — Test additions/updates

**Rules:**
- Always lowercase
- Use hyphens, not underscores or spaces
- Cloud agents append `-8666` suffix
- Keep descriptive name short but clear (3-5 words max)

**Examples:**
- ✅ `cursor/brand-colors-cream-burgundy-8666`
- ✅ `docs/swm-migration-plan`
- ✅ `feature/rss-feed`
- ✅ `fix/contact-form-validation`
- ❌ `Feature/RSS-Feed` (uppercase not allowed)
- ❌ `fix_contact_form` (underscores not allowed)
- ❌ `cursor/update` (too vague)

### Git Tags

**Convention:** Semantic versioning `vMAJOR.MINOR.PATCH`

**Examples:**
- ✅ `v1.0.0`
- ✅ `v0.1.0`
- ✅ `v2.3.1`
- ❌ `1.0.0` (missing `v` prefix)
- ❌ `v1.0` (incomplete semver)

---

## File and Folder Naming

### Folders

**Convention:** `kebab-case` for multi-word, single-word lowercase preferred

**Examples:**
- ✅ `app/`
- ✅ `swm-recovery/`
- ✅ `rose-rocket-engine/`
- ✅ `content/`
- ❌ `swmRecovery/` (camelCase not allowed)
- ❌ `SWM_Recovery/` (mixed case not allowed)

**Exception:** Framework conventions (Next.js route groups use parentheses: `(pages)/`)

### Markdown Files

**Convention:** Depends on file type

**Top-Level Meta Files:** `SCREAMING_SNAKE_CASE.md`
- ✅ `README.md`
- ✅ `AGENTS.md`
- ✅ `CHANGELOG.md`
- ✅ `SECURITY.md`
- ✅ `LICENSE`

**Content Files:** `kebab-case.md`
- ✅ `systems-health.md`
- ✅ `welcome-to-chefwho-codes.md`
- ✅ `swm-migration-plan.md`

**Registers and Templates:** `UPPER_SNAKE_CASE.md`
- ✅ `SOURCE-META.md`
- ✅ `AUTHORIZED_SOURCE_INDEX.md`
- ✅ `INGEST_FROM_MAC.sh`

**Rationale:** Top-level meta files shout "I'm important." Content files are lowercase for readability. Registers/templates follow SWM extraction convention.

### TypeScript and JavaScript Files

**React Components:** `PascalCase.tsx`
- ✅ `ContactForm.tsx`
- ✅ `BlogPost.tsx`
- ✅ `NavBar.tsx`
- ❌ `contactForm.tsx` (wrong case)
- ❌ `contact-form.tsx` (wrong case)

**Next.js Special Files:** `kebab-case.tsx`
- ✅ `page.tsx`
- ✅ `layout.tsx`
- ✅ `route.ts`
- ✅ `not-found.tsx`
- ❌ `Page.tsx` (Next.js requires lowercase)

**Utility Files:** `kebab-case.ts`
- ✅ `blog.ts`
- ✅ `contact.ts`
- ✅ `types.ts`
- ✅ `api-client.ts`
- ❌ `blogUtils.ts` (camelCase not allowed for files)

**Test Files:** Match source file with `.test.ts` or `.spec.ts` suffix
- ✅ `blog.test.ts` (for `blog.ts`)
- ✅ `ContactForm.spec.tsx` (for `ContactForm.tsx`)

### CSS Files

**Convention:** `kebab-case.css`

**Examples:**
- ✅ `globals.css`
- ✅ `contact-form.css` (if using CSS modules)
- ❌ `globalStyles.css` (camelCase not allowed)

---

## Code-Level Naming

### TypeScript/JavaScript

**Variables and Functions:** `camelCase`
```typescript
// ✅ Good
const blogPosts = getBlogPosts();
function formatDate(date: Date): string { }

// ❌ Bad
const blog_posts = get_blog_posts(); // snake_case
const BlogPosts = GetBlogPosts();    // PascalCase
```

**Constants:** `SCREAMING_SNAKE_CASE` (for true constants only)
```typescript
// ✅ Good
const MAX_POSTS_PER_PAGE = 10;
const API_BASE_URL = 'https://api.example.com';

// ❌ Bad (not a constant, it's config)
const maxPostsPerPage = 10; // Should be SCREAMING_SNAKE_CASE
```

**Types and Interfaces:** `PascalCase`
```typescript
// ✅ Good
interface BlogPost {
  title: string;
  date: Date;
}

type ContactFormData = {
  name: string;
  email: string;
};

// ❌ Bad
interface blog_post { }  // snake_case
type contactFormData = { } // camelCase
```

**Enums:** `PascalCase` for enum name, `SCREAMING_SNAKE_CASE` for values
```typescript
// ✅ Good
enum PostStatus {
  DRAFT = 'DRAFT',
  PUBLISHED = 'PUBLISHED',
  ARCHIVED = 'ARCHIVED',
}

// ❌ Bad
enum postStatus { }           // camelCase name
enum PostStatus {
  draft = 'draft',            // lowercase value
}
```

**Private Members:** Prefix with `_` (TypeScript convention)
```typescript
// ✅ Good
class BlogService {
  private _cache: Map<string, BlogPost>;
  
  private _fetchFromCache(slug: string) { }
}
```

### CSS Class Names

**Convention:** `kebab-case` with BEM methodology

**BEM Pattern:** `.block__element--modifier`

**Examples:**
```css
/* ✅ Good - BEM */
.site-header { }
.site-header__logo { }
.site-header__nav { }
.nav-list { }
.nav-list__item { }
.nav-list__item--active { }

/* ✅ Good - Utility classes */
.container { }
.stack { }
.card { }

/* ❌ Bad */
.siteHeader { }           // camelCase
.site_header { }          // snake_case
.SiteHeader { }           // PascalCase
.nav-list-item-active { } // Not BEM (missing __ and --)
```

**State Classes:** Prefix with `is-` or `has-`
```css
.button { }
.button.is-loading { }
.button.is-disabled { }
.card.has-image { }
```

### CSS Custom Properties (Variables)

**Convention:** `--kebab-case`

**Examples:**
```css
/* ✅ Good */
:root {
  --bg: #F7F3EA;
  --text: #1A1A1A;
  --accent: #8C2B2B;
  --border-radius: 0.8rem;
}

/* ❌ Bad */
:root {
  --backgroundColor: #F7F3EA;  // camelCase
  --text_color: #1A1A1A;       // snake_case
}
```

---

## Environment Variables

**Convention:** `SCREAMING_SNAKE_CASE` with namespace prefix

**Pattern:** `<NAMESPACE>_<DESCRIPTION>`

**Examples:**
```bash
# ✅ Good
CONTACT_RECIPIENT_EMAIL=
CONTACT_SENDGRID_API_KEY=
NEXT_PUBLIC_API_URL=
DATABASE_URL=

# ❌ Bad
contactRecipient=           # camelCase
contact-recipient-email=    # kebab-case
RECIPIENTEMAIL=            # No namespace
```

**Namespace Rules:**
- Contact form: `CONTACT_`
- Public (client-side): `NEXT_PUBLIC_`
- Database: `DATABASE_`
- Third-party service: `<SERVICE>_` (e.g., `SENDGRID_`, `STRIPE_`)

---

## URL and Route Naming

**Convention:** `kebab-case`

**Examples:**
```
✅ /blog
✅ /blog/welcome-to-chefwho-codes
✅ /about
✅ /contact
✅ /api/contact

❌ /Blog                    // uppercase
❌ /blog/WelcomeToBlog     // PascalCase
❌ /blog/welcome_to_blog   // snake_case
```

---

## Database Naming (Future)

**Tables:** `snake_case` (plural)
```sql
-- ✅ Good
blog_posts
contact_submissions
users

-- ❌ Bad
BlogPosts    -- PascalCase
blogPost     -- camelCase, singular
```

**Columns:** `snake_case`
```sql
-- ✅ Good
CREATE TABLE blog_posts (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  published_at TIMESTAMP,
  author_id INTEGER
);

-- ❌ Bad
CREATE TABLE blog_posts (
  Id SERIAL PRIMARY KEY,          -- PascalCase
  Title TEXT NOT NULL,            -- PascalCase
  publishedAt TIMESTAMP,          -- camelCase
  AuthorID INTEGER                -- Mixed case
);
```

---

## Commit Message Naming

**Convention:** Conventional Commits

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation only
- `style` — Formatting, no code change
- `refactor` — Code restructuring
- `test` — Test additions/updates
- `chore` — Maintenance

**Scope (optional):**
- Component or area: `blog`, `contact`, `swm-recovery`, `ci`

**Subject:**
- Lowercase, no period at end
- Imperative mood: "add" not "added" or "adds"
- Max 50 characters

**Examples:**
```
✅ feat(blog): add RSS feed generation
✅ fix(contact): validate email format
✅ docs(agents): update quality gates
✅ refactor(globals): consolidate color tokens
✅ chore(deps): bump next to 16.2.4

❌ Added RSS feed                   // Wrong tense
❌ Fix bug                          // Too vague
❌ feat(Blog): Add RSS Feed         // Wrong case
❌ docs: updated the AGENTS.md file to reflect new quality gates and CI config // Too long
```

---

## Exceptions and Special Cases

### Framework Conventions Take Precedence

When framework (Next.js, React) requires specific naming, follow framework convention:
- Next.js route groups: `(pages)/`
- Next.js special files: `page.tsx`, `layout.tsx`, `route.ts`
- React component files: `PascalCase.tsx`

### Acronyms

**Rule:** Treat acronyms as words, not all-caps

```typescript
// ✅ Good
class ApiClient { }
function parseHtml() { }
const apiUrl = 'https://...';

// ❌ Bad
class APIClient { }
function parseHTML() { }
const APIURL = 'https://...';
```

**Exception:** Environment variables always `SCREAMING_SNAKE_CASE`
```bash
API_URL=
HTML_PARSER_ENABLED=
```

### Numbers in Names

**Rule:** Numbers are allowed but avoid starting with number

```typescript
// ✅ Good
const option1 = ...;
const button2 = ...;

// ❌ Bad
const 1stOption = ...; // Syntax error
const 2ndButton = ...; // Syntax error

// ✅ Better (spell out ordinals when possible)
const firstOption = ...;
const secondButton = ...;
```

---

## Migration Strategy

### For Existing Code

**Phase 3 of Rebuild Plan:** Rename all files to match conventions

**Process:**
1. Audit all files with `find` and `grep`
2. Create rename script
3. Test that all imports still resolve
4. Update references in documentation
5. Commit with message: `refactor: apply naming conventions`

**Do NOT:** Rename piecemeal. Do it all at once in one PR to avoid confusion.

### For New Code

**Effective Immediately:** All new files and code MUST follow these conventions.

**Enforcement:**
- Code review checks naming
- Linter rules (where possible)
- CI check for file naming (Phase 1 of Rebuild)

---

## Tooling Support

### ESLint Rules

Configure ESLint to enforce naming:
```json
{
  "rules": {
    "@typescript-eslint/naming-convention": [
      "error",
      {
        "selector": "variable",
        "format": ["camelCase", "UPPER_CASE"]
      },
      {
        "selector": "typeLike",
        "format": ["PascalCase"]
      }
    ]
  }
}
```

### File Name Linter

Custom script to check file naming (to be added in Phase 1):
```bash
# Check for PascalCase component files
find app -name "*.tsx" ! -name "*[a-z]*.tsx" 

# Check for kebab-case utility files
find lib -name "*.ts" ! -name "*[A-Z]*.ts"
```

---

## Questions and Clarifications

**Q: What if I need a name that doesn't fit these patterns?**  
A: Document the exception in this file with rationale. Do NOT silently violate convention.

**Q: What about third-party code?**  
A: Third-party code (node_modules) is exempt. Only our code must follow conventions.

**Q: Can I use abbreviations?**  
A: No, except for widely-known acronyms (API, URL, HTTP, HTML, CSS, SQL). Spell out everything else.

---

## Related Documentation

- `docs/POLICIES.md` — Repository policies
- `docs/STYLE_GUIDE.md` — Code and visual style
- `docs/COMPREHENSIVE_REBUILD_PLAN.md` — Rebuild strategy

---

**Philosophy:** Boring, consistent names make code easier to navigate. Creativity belongs in problem-solving, not in naming.
