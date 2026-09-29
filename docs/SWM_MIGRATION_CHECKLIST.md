# SWM Enterprise Migration — Implementation Checklist

**Full Plan:** `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md`  
**Quick Ref:** `docs/SWM_MIGRATION_QUICK_REF.md`  
**Status:** Planning complete — Phase 2 ready to start

Use this checklist to track migration progress. Update as tasks complete.

## Phase 1: Documentation and Planning

- [x] Create migration plan document
- [x] Create quick reference guide
- [ ] **Operator review** — Review full plan and provide feedback
- [ ] Document current SWM assets (repos, Notion DBs, Drive folders)
- [ ] Identify external dependencies (APIs, services, credentials)
- [ ] Create tracking system (CLOUT rows or Linear issues)

**Completion Criteria:**

- [ ] Migration plan approved by operator
- [ ] All SWM assets cataloged
- [ ] Stakeholders informed

---

## Phase 2: Content Migration

### Phase 2.1: Brand Asset Ingestion

- [ ] **OPERATOR ACTION: Run brand ingest script on Mac**
  - Script: `swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh`
  - Location: `/Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE/`
- [ ] Commit ingested metadata (content stays gitignored)
- [ ] Create recovery run log (`swm-recovery/runs/007-brand-full-ingest.md`)
- [ ] Verify brand token register completeness
- [ ] Update `AGENTS.md` § Gotchas when ingest complete

**Completion Criteria:**

- [ ] Cloud agents can access brand metadata
- [ ] Brand token register is current
- [ ] Recovery status updated in `swm-recovery/README.md`

### Phase 2.2: SWM Business Documentation Consolidation

**DECISION 1 REQUIRED:** Choose business docs home (see migration plan)

- [ ] **Operator decides:** Business docs location (A/B/C/D)
- [ ] Implement chosen documentation structure
- [ ] Migrate/link core SWM materials:
  - [ ] Product vision and architecture
  - [ ] Operating posture (`GOVERNANCE.md` from `kevlarkia/swm-system`)
  - [ ] Brand guidelines (from brand asset extraction)
  - [ ] GTM strategy and positioning
  - [ ] Legal/compliance boundaries documentation
- [ ] Update `AGENTS.md` with new canonical locations
- [ ] Update `docs/SYSTEMS_HEALTH.md` with new locations
- [ ] Archive or redirect old locations

**Completion Criteria:**

- [ ] All SWM business docs have clear canonical home
- [ ] Agents can locate docs via `AGENTS.md`
- [ ] No active work stranded in chat transcripts

### Phase 2.3: Repository Consolidation

**DECISION 2 REQUIRED:** Per-repo merge vs. link strategy

- [ ] Complete repository inventory (all SWM-related repos)
- [ ] Known repos to evaluate:
  - [ ] `kevlarkia/swm-system` (private governance)
  - [ ] `kevlarkia/rose-rocket-engine` (upstream mirror)
  - [ ] (add others discovered during inventory)
- [ ] For each secondary repo, decide: Merge / Link / Archive
- [ ] Execute repo consolidation plan
- [ ] Update `rose-rocket-engine/UPSTREAM_APPLY.md` if needed
- [ ] Migrate/archive GitHub Issues, Projects, Discussions
- [ ] Update all internal links (README, AGENTS.md, Notion, etc.)

**Completion Criteria:**

- [ ] Repository architecture is stable
- [ ] All SWM repos under SWa Works enterprise or archived
- [ ] No broken cross-repo links

---

## Phase 3: Systems and Access

### Phase 3.1: Enterprise Access Controls

- [ ] Review enterprise member list
- [ ] Define team structure (SWM Core, Brand, External, etc.)
- [ ] Configure repository access policies
- [ ] Set up GitHub Actions runner policies
- [ ] Configure SSO/SAML if required (likely not needed yet)

**Completion Criteria:**

- [ ] Team structure matches operational needs
- [ ] Repository access follows least-privilege
- [ ] Cloud agents can access required repos

### Phase 3.2: Secrets and Environment Variables

- [ ] Audit all secrets currently in use (local, CI, deployed)
- [ ] Migrate secrets to appropriate vaults:
  - [ ] Cursor Cloud secrets (for cloud agent runs)
  - [ ] GitHub organization secrets (for CI/CD)
  - [ ] Deployment platform secrets (for production)
- [ ] Document secret rotation policy
- [ ] Update `AGENTS.md` and `README.md` with secrets guidance

**Completion Criteria:**

- [ ] All secrets documented and stored properly
- [ ] No secrets in git history
- [ ] Cloud agents can access required secrets
- [ ] Rotation procedures documented

### Phase 3.3: CI/CD and Quality Gates

**DECISION 3 OPTIONAL:** Extend CI/CD with automated tests?

- [ ] Review existing CI/CD pipelines (`.github/workflows/`)
- [ ] Extend quality gates (if desired):
  - [ ] Add automated tests (if tests exist)
  - [ ] Add build checks to CI (currently local only)
  - [ ] Add coverage reporting
- [ ] Configure branch protection rules for `main`
- [ ] Set up deployment pipeline (if hosting changes)
- [ ] Document CI/CD expectations in `AGENTS.md`

**Completion Criteria:**

- [ ] Quality gates match documented standards
- [ ] CI/CD runs successfully on all active branches
- [ ] Branch protection prevents direct pushes to `main`

---

## Phase 4: Operational Readiness

### Phase 4.1: Maintenance Runbooks

- [ ] Create `docs/SWM_OPERATIONS.md` covering:
  - [ ] Routine maintenance (weekly, monthly, quarterly)
  - [ ] Incident response procedures
  - [ ] Backup and recovery procedures
  - [ ] Onboarding checklist for new team members
- [ ] Integrate SWM ops into `docs/SYSTEMS_HEALTH.md` cadence
- [ ] Document escalation paths and on-call (if applicable)
- [ ] Update `AGENTS.md` with operational context

**Completion Criteria:**

- [ ] SWM operational procedures documented
- [ ] Maintenance cadence defined
- [ ] New team members can onboard from docs

### Phase 4.2: Communication and Collaboration

- [ ] Set up team communication channels (Slack/Discord)
- [ ] Create SWM project board (GitHub Projects/Linear)
- [ ] Define issue triage and PR review process
- [ ] Document meeting cadence and decision-making
- [ ] Set up status update cadence (if multi-person)

**Completion Criteria:**

- [ ] Team collaboration tools are live
- [ ] Communication norms documented
- [ ] Status visibility for all stakeholders

### Phase 4.3: Monitoring and Observability

- [ ] Set up repository health monitoring (CI rate, PR latency)
- [ ] Configure alerting for critical failures
- [ ] Implement website analytics (if desired)
- [ ] Set up SWM-specific metrics (extraction runs, recovery coverage)
- [ ] Document monitoring strategy

**Completion Criteria:**

- [ ] Key metrics tracked
- [ ] Alerts configured for critical paths
- [ ] Monitoring strategy documented

---

## Success Metrics (Overall)

- [ ] **Completeness:** All SWM assets have documented home
- [ ] **Agent readiness:** Cloud agents can locate content via `AGENTS.md`
- [ ] **Operational hygiene:** `AGENTS.md` and `README.md` match reality
- [ ] **Collaboration readiness:** Team can onboard from docs alone
- [ ] **No regressions:** Site, toolkit, and Rose Rocket mirror still work

---

## Tracking

**Current Phase:** 1 (Planning) → 2 (Content Migration)  
**Last Updated:** 2026-08-13  
**Next Review:** After Phase 2.1 completion

**Notes:**

- Use this checklist in conjunction with CLOUT intake or Linear issues
- Update completion status as tasks finish
- Document blockers inline and escalate to operator

---

**See Also:**

- `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md` — Full migration plan
- `docs/SWM_MIGRATION_QUICK_REF.md` — Quick reference
