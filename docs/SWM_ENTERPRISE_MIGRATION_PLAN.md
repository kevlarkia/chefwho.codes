# SWM Enterprise Migration Plan

**Target State:** Consolidate Smart Workforce Movement (SWM) operations into
the **chefwho.codes** repository under the **SWa Works** GitHub enterprise.

**Created:** 2026-08-13  
**Status:** Draft — Ready for execution  
**Owner:** @kevlarkia

## Executive Summary

This repository (`kevlarkia/chefwho.codes`) will become the unified home for:

1. **SWM Recovery Toolkit** (already present under `swm-recovery/`)
2. **SWM Business Operations** (brand, product, governance)
3. **Personal Site** (chefwho.codes marketing presence)
4. **Rose Rocket Engine** (AI newsletter toolkit mirror)

The **SWa Works enterprise** on GitHub provides the organizational container
for multi-repository collaboration, shared billing, and centralized access
controls as the business scales.

## Current State Assessment

### What exists today

| Component | Location | Status |
| --- | --- | --- |
| chefwho.codes website | This repo (`kevlarkia/chefwho.codes`) | ✅ Production ready |
| SWM Recovery Toolkit | This repo (`swm-recovery/`) | ✅ Operational |
| Rose Rocket Engine mirror | This repo (`rose-rocket-engine/`) | ✅ CI/pytest staging |
| SWa Works Enterprise | <https://github.com/enterprises/swa-works> | ✅ Created |
| Brand source materials | Mac-local (`/Users/fcaf/...`) | ⚠️ Authorized but not ingested |
| SWM business materials | Scattered (Notion, Drive, chat transcripts) | ⚠️ Needs consolidation |

### Repository structure (as-is)

```text
chefwho.codes/
├── app/                    # Next.js 16 App Router
├── content/blog/           # Markdown blog posts
├── lib/                    # Shared TypeScript helpers
├── swm-recovery/           # SWM extraction suite
│   ├── prompts/            # Recovery prompts 01–05
│   ├── templates/          # Register scaffolds
│   ├── registers/          # Completed extraction ledgers
│   ├── runs/               # Recovery run logs
│   ├── sources/            # Authorized source index + ingest scripts
│   └── cursor-plugin/      # AI-invocable commands
├── rose-rocket-engine/     # Newsletter toolkit mirror
├── docs/                   # Systems health + runbooks
├── AGENTS.md               # Cloud agent instructions
└── README.md               # Repository overview
```

### GitHub Enterprise configuration

- **Enterprise:** SWa Works (<https://github.com/enterprises/swa-works>)
- **Member org:** Chefwho.Codes (<https://github.com/Chefwho-Codes>)
- **Primary repository:** `kevlarkia/chefwho.codes`
- **Ownership:** All previous Chefwho.Codes org owners are now SWa Works
  enterprise owners
- **Billing:** Transferred from Chefwho.Codes org to SWa Works enterprise

## Migration Phases

Migration is structured into **four phases** with clear completion criteria.
Each phase builds on the previous one. Phases can overlap when dependencies
allow.

### Phase 1: Documentation and Planning (READY)

**Goal:** Establish the migration plan, document current state, and prepare
communication materials.

**Tasks:**

- [x] Create `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md` (this document)
- [ ] Review with stakeholders (operator review)
- [ ] Document current SWM-related repositories, Notion databases, and Drive folders
- [ ] Identify external dependencies (APIs, services, credentials)
- [ ] Create migration checklist (track completion in CLOUT or Linear)

**Completion Criteria:**

- Migration plan approved
- All SWM assets cataloged
- Stakeholders informed

**Estimated Complexity:** Simple — one planning document, one review cycle,
basic inventory.

### Phase 2: Content Migration (IN PROGRESS)

**Goal:** Move all SWM business content, brand assets, and operational
materials into this repository or linked systems under unified governance.

#### 2.1 Brand Asset Ingestion

**Current State:**

- 11 brand source packages authorized (see
  `swm-recovery/sources/brand-assets/AUTHORIZED_SOURCE_INDEX.md`)
- Sources are Mac-local (`/Users/fcaf/Documents/...`)
- Metadata structures exist; content awaits ingest

**Tasks:**

- [ ] **Operator action:** Run
  `swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh` on Mac with sources
  accessible
- [ ] Commit ingested metadata (content stays gitignored per existing rules)
- [ ] Create new recovery run log (e.g., `swm-recovery/runs/007-brand-full-ingest.md`)
- [ ] Verify brand token register completeness
- [ ] Update `AGENTS.md` § Gotchas when ingest is complete

**Completion Criteria:**

- Cloud agents can access brand metadata
- Brand token register is current
- Recovery status updated in `swm-recovery/README.md`

**Estimated Complexity:** Moderate — operator must run Mac-side script, then
cloud agent documents results. Ingest script already exists; it's execution,
not design.

#### 2.2 SWM Business Documentation Consolidation

**Current State:**

- Governance, operating posture, and product architecture are in
  `kevlarkia/swm-system` (separate repo, not public)
- Business artifacts scattered across Notion (CLOUT), Google Drive, and chat
  transcripts
- No single source of truth for SWM product specs, roadmap, or GTM strategy

**Tasks:**

- [ ] Decide on documentation home:
  - **Option A:** Create `swm-business/` directory in this repo (public or
    private repo decision required)
  - **Option B:** Keep separate `kevlarkia/swm-system` repo; link from here
  - **Option C:** Use Notion as SSOT; sync to repo for agent access only
- [ ] Migrate/link core SWM materials:
  - [ ] Product vision and architecture
  - [ ] Operating posture (`GOVERNANCE.md` from `kevlarkia/swm-system`)
  - [ ] Brand guidelines (output from brand asset extraction)
  - [ ] GTM strategy and positioning
  - [ ] Legal/compliance boundaries (what stays private)
- [ ] Update `AGENTS.md` and `docs/SYSTEMS_HEALTH.md` with new canonical
  locations
- [ ] Archive or redirect old locations

**Completion Criteria:**

- All SWM business docs have a clear canonical home
- Agents can locate SWM governance, brand, and product docs via `AGENTS.md`
- No active SWM work remains stranded in chat transcripts

**Estimated Complexity:** Complex — requires operator decisions on
public/private boundaries, multi-tool coordination (repo, Notion, Drive),
and high risk of scope creep. Breaking into smaller sub-phases is
recommended.

#### 2.3 Repository Consolidation

**Current State:**

- Primary repo: `kevlarkia/chefwho.codes` (this one)
- Secondary repos:
  - `kevlarkia/swm-system` (private, operational governance)
  - `kevlarkia/rose-rocket-engine` (upstream newsletter engine)
  - Potentially others (TBD during inventory)

**Tasks:**

- [ ] Complete repository inventory (identify all SWM-related repos)
- [ ] For each secondary repo, decide:
  - **Merge** into this repo (if small, closely related)
  - **Link** from this repo (if large, independent lifecycle)
  - **Archive** (if obsolete)
- [ ] Update `rose-rocket-engine/UPSTREAM_APPLY.md` if upstream repo access
  changes
- [ ] Migrate or archive GitHub Issues, Projects, and Discussions from
  secondary repos
- [ ] Update all internal links (README files, AGENTS.md, Notion, etc.)

**Completion Criteria:**

- Repository architecture is stable
- All SWM repos are under SWa Works enterprise or explicitly archived
- No broken cross-repo links

**Estimated Complexity:** Moderate to Complex — depends on number of repos
and their entanglement. Merging repos with active history requires careful
git work.

### Phase 3: Systems and Access (READY)

**Goal:** Configure enterprise-level permissions, CI/CD, secrets management,
and shared services.

#### 3.1 Enterprise Access Controls

**Tasks:**

- [ ] Review enterprise member list (owners, billing managers, members)
- [ ] Define team structure (e.g., SWM Core, Brand, External Collaborators)
- [ ] Configure repository access policies for SWa Works enterprise
- [ ] Set up GitHub Actions runner policies (self-hosted or GitHub-hosted)
- [ ] Configure SSO/SAML if required (enterprise feature, likely not needed yet)

**Completion Criteria:**

- Team structure matches operational needs
- Repository access follows least-privilege principle
- Cloud agents can access all required repos via enterprise permissions

**Estimated Complexity:** Simple to Moderate — depends on team size and
enterprise feature usage. Current state (single operator) is simple; scales
with team growth.

#### 3.2 Secrets and Environment Variables

**Current State:**

- `.env.example` defines contract for local development
- SendGrid API key (contact form) is optional
- No secrets required for local development
- Cloud agent secrets managed via Cursor Dashboard (Cloud Agents > Secrets)

**Tasks:**

- [ ] Audit all secrets currently in use (local, CI, deployed)
- [ ] Migrate secrets to appropriate vault:
  - **Cursor Cloud secrets:** for cloud agent runs
  - **GitHub organization secrets:** for CI/CD across repos
  - **Deployment platform secrets:** (Vercel, Netlify, etc.) for production
- [ ] Document secret rotation policy
- [ ] Update `AGENTS.md` and `README.md` with secrets guidance

**Completion Criteria:**

- All secrets documented and properly stored
- No secrets in git history or local `.env` files committed
- Cloud agents can access required secrets
- Secret rotation procedures documented

**Estimated Complexity:** Simple — current surface area is small (one
optional API key). Complexity grows with additional services.

#### 3.3 CI/CD and Quality Gates

**Current State:**

- GitHub Actions runs Markdown linting and workflow linting (actionlint)
- ESLint, TypeScript, and build checks are local/PR hygiene only
- No automated tests or coverage tracking

**Tasks:**

- [ ] Review existing CI/CD pipelines (`.github/workflows/`)
- [ ] Extend quality gates:
  - [ ] Add automated tests (if/when tests exist)
  - [ ] Add build checks to CI (currently local only)
  - [ ] Add coverage reporting (if desired)
- [ ] Configure branch protection rules for `main`
- [ ] Set up deployment pipeline (if hosting changes)
- [ ] Document CI/CD expectations in `AGENTS.md`

**Completion Criteria:**

- Quality gates match documented standards
- CI/CD pipelines run successfully on all active branches
- Branch protection prevents direct pushes to `main`

**Estimated Complexity:** Simple to Moderate — depends on whether automated
testing infrastructure is added. Current CI is lightweight and working.

### Phase 4: Operational Readiness (NOT STARTED)

**Goal:** Establish ongoing maintenance practices, monitoring, and
communication channels for SWM operations.

#### 4.1 Maintenance Runbooks

**Current State:**

- `docs/SYSTEMS_HEALTH.md` covers AI instruction hygiene, CLOUT routing,
  Drive/disk tidy
- `swm-recovery/README.md` covers extraction operation mode
- No dedicated SWM operational playbook

**Tasks:**

- [ ] Create `docs/SWM_OPERATIONS.md` (or similar) covering:
  - [ ] Routine maintenance tasks (weekly, monthly, quarterly)
  - [ ] Incident response procedures
  - [ ] Backup and recovery procedures
  - [ ] Onboarding checklist for new team members
- [ ] Integrate SWM operations into `docs/SYSTEMS_HEALTH.md` cadence
- [ ] Document escalation paths and on-call procedures (if applicable)
- [ ] Update `AGENTS.md` with operational context

**Completion Criteria:**

- SWM operational procedures documented
- Maintenance cadence defined
- New team members can onboard from docs alone

**Estimated Complexity:** Moderate — requires synthesizing tribal knowledge
into written procedures. Easier with single operator; scales with team.

#### 4.2 Communication and Collaboration

**Tasks:**

- [ ] Set up team communication channels (Slack, Discord, or equivalent)
- [ ] Create SWM project board (GitHub Projects, Linear, or equivalent)
- [ ] Define issue triage and PR review process
- [ ] Document meeting cadence and decision-making process
- [ ] Set up status update cadence (if multi-person team)

**Completion Criteria:**

- Team collaboration tools are live
- Communication norms documented
- Status visibility for all stakeholders

**Estimated Complexity:** Simple for single operator; Moderate to Complex
for multi-person teams.

#### 4.3 Monitoring and Observability

**Tasks:**

- [ ] Set up repository health monitoring (CI pass rate, PR merge latency)
- [ ] Configure alerting for critical failures
- [ ] Implement analytics for chefwho.codes website (if desired)
- [ ] Set up SWM-specific metrics (extraction runs, recovery coverage, etc.)
- [ ] Document monitoring strategy

**Completion Criteria:**

- Key metrics tracked
- Alerts configured for critical paths
- Monitoring strategy documented

**Estimated Complexity:** Moderate — depends on observability requirements
and tooling choices.

## Risk Assessment and Mitigation

| Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- |
| **Brand asset ingest delayed** | Recovery toolkit incomplete | Medium | Operator runs Mac-side script; task is simple execution |
| **Scope creep in content consolidation** | Migration drags on | High | Use phased approach; defer non-critical items to Phase 4 |
| **Repository merge complexity** | Git history conflicts, broken links | Medium | Inventory first; merge small repos only; link large ones |
| **Secrets exposure during migration** | Security incident | Low | Audit first; use secret scanning; rotate if needed |
| **Stale AGENTS.md after migration** | Cloud agents hallucinate setup | Medium | Update AGENTS.md in same PR as structural changes |
| **Lost work during consolidation** | Business continuity failure | Low | CLOUT intake before large moves; maintain parallel systems until cutover |

## Decision Points Requiring Operator Input

The following decisions block progress and require operator clarification:

### Decision 1: SWM Business Documentation Home

**Question:** Where should SWM business docs (product vision, architecture,
GTM strategy) live?

**Options:**

- **A:** Create `swm-business/` in this repo (public); sensitive material
  stays in Notion/private repo
- **B:** Create `swm-business/` in this repo (private repo made public
  later or kept private)
- **C:** Keep `kevlarkia/swm-system` separate; link from here
- **D:** Use Notion as SSOT; sync to repo for agent access only

**Recommendation:** Option A — public `swm-business/` with clear boundaries.
SWM is a public product; operating transparently builds trust. Keep legal,
medical, and private relationship material out of public repos.

**Blocking:** Phase 2.2 tasks

### Decision 2: Repository Consolidation Strategy

**Question:** Should secondary SWM repos be merged into this one or linked?

**Recommendation:** Inventory first (Phase 2.3), then decide per-repo. Small,
tightly coupled repos (e.g., SWM plugins, tooling) should merge. Large,
independently versioned repos (e.g., upstream `rose-rocket-engine`) should
link.

**Blocking:** Phase 2.3 tasks

### Decision 3: Automated Testing and Coverage

**Question:** Should CI/CD be extended to include automated tests and
coverage reporting?

**Recommendation:** Defer to Phase 3.3 unless tests already exist. Adding
test infrastructure is a separate project from migration.

**Blocking:** Phase 3.3 tasks (optional)

### Decision 4: Public vs. Private for chefwho.codes Repo

**Current State:** Repository is public (confirmed via GitHub URL structure).

**Question:** Should this repo remain public as SWM business content is added?

**Recommendation:** Remain public. SWM is a public product, and transparency
aligns with brand values. Sensitive material (credentials, private business
data, personal info) should never be committed; use `.gitignore` and secret
vaults.

**Blocking:** No blocker, but affirms Phase 2.2 approach.

## Timeline and Sequencing

Phases are presented in logical order, but tasks within phases can often
proceed in parallel. This is a **capability-driven plan**, not a
calendar-driven one. The timeline depends on operator availability and
decision velocity.

### Critical Path

```text
Phase 1 (Planning)
  ↓
Phase 2.1 (Brand ingest) — OPERATOR ACTION REQUIRED
  ↓
Phase 2.2 (Business docs) — DECISION 1 REQUIRED
  ↓
Phase 2.3 (Repo consolidation) — DECISION 2 REQUIRED
  ↓
Phase 3.1 (Access controls)
  ↓
Phase 3.2 (Secrets)
  ↓
Phase 3.3 (CI/CD)
  ↓
Phase 4.1 (Runbooks)
  ↓
Phase 4.2 (Communication)
  ↓
Phase 4.3 (Monitoring)
```

### Parallel Work Opportunities

- **Phase 2.1 and 2.2** can proceed in parallel (brand ingest is independent
  of business docs)
- **Phase 3.1, 3.2, 3.3** can proceed in parallel after Phase 2 completes
- **Phase 4.1, 4.2, 4.3** can proceed in parallel

### Immediate Next Steps (Top 3)

1. **Operator review:** Review this plan and provide input on Decision 1 and
   Decision 4
2. **Brand ingest:** Run
   `swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh` on Mac (Phase 2.1)
3. **Repository inventory:** List all SWM-related repos and their status
   (Phase 2.3 prerequisite)

## Success Metrics

Migration success is measured by:

- **Completeness:** All SWM assets have a documented home
- **Agent readiness:** Cloud agents can locate SWM content via `AGENTS.md`
- **Operational hygiene:** `AGENTS.md` and `README.md` match reality
- **Collaboration readiness:** Team can onboard and contribute from docs
  alone
- **No regressions:** chefwho.codes website, SWM toolkit, and Rose Rocket
  mirror continue to function

## Rollback Plan

If migration encounters critical blockers:

1. **Document blocker** in this plan or as a GitHub issue
2. **Pause migration work** on affected phase
3. **Maintain parallel systems** (e.g., old repo + new repo) until resolved
4. **No destructive actions** until confident (no force-pushes, no permanent
   deletes)
5. **CLOUT intake** for any work done in failed migration attempts

## Related Documentation

- `AGENTS.md` — Cloud agent instructions (this repo)
- `README.md` — Repository overview (this repo)
- `docs/SYSTEMS_HEALTH.md` — Ecosystem maintenance runbook
- `swm-recovery/README.md` — SWM extraction toolkit operating mode
- `rose-rocket-engine/UPSTREAM_APPLY.md` — Upstream sync procedures
- `kevlarkia/swm-system` → `GOVERNANCE.md` — Operating posture (external
  repo, if kept separate)

## Changelog

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-13 | Initial draft | Cloud Agent (cursor/swm-enterprise-migration-plan-8666) |

---

**Next Action:** Operator review of this plan, then execute Phase 2.1 (brand
ingest).
