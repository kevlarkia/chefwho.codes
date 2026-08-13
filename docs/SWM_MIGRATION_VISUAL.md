# SWM Enterprise Migration — Visual Overview

**Last Updated:** 2026-08-13  
**Status:** Phase 1 Complete → Phase 2 Ready

This document provides a visual/conceptual overview of the SWM enterprise migration. For detailed information, see the [full migration plan](SWM_ENTERPRISE_MIGRATION_PLAN.md).

## Migration Flow (High Level)

```text
┌─────────────────────────────────────────────────────────────┐
│                    SWa Works Enterprise                     │
│              https://github.com/enterprises/swa-works       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─ Member Org: Chefwho.Codes
                              ├─ (Future orgs can be added)
                              └─ Unified billing & access
                              
                              ↓
                              
┌─────────────────────────────────────────────────────────────┐
│            kevlarkia/chefwho.codes (this repo)              │
│                    UNIFIED OPERATIONAL HOME                 │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ↓                     ↓                     ↓
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  Personal Site │  │  SWM Recovery  │  │ Rose Rocket    │
│  (chefwho.     │  │  Toolkit       │  │ Engine Mirror  │
│   codes)       │  │                │  │                │
└────────────────┘  └────────────────┘  └────────────────┘
        │                     │                     │
        ↓                     ↓                     ↓
  Marketing         Brand recovery       Newsletter
  presence         & extraction          toolkit CI
```

## Current State → Target State

### Before (Pre-Migration)

```text
Scattered SWM Assets:
├── kevlarkia/chefwho.codes
│   ├── Personal site (Next.js)
│   └── swm-recovery/ (already here)
│
├── kevlarkia/swm-system (separate repo)
│   └── GOVERNANCE.md (operating posture)
│
├── Notion (scattered)
│   ├── CLOUT intake
│   ├── Product specs
│   └── Various business docs
│
├── Google Drive (scattered)
│   ├── Brand assets
│   └── Business documents
│
├── Mac-local (/Users/fcaf/...)
│   └── SWM brand sources (authorized but not ingested)
│
└── Chat transcripts
    └── Stranded work artifacts
```

### After (Post-Migration)

```text
Unified SWM Home (kevlarkia/chefwho.codes):
├── app/ (Next.js site)
├── content/blog/
├── lib/
│
├── swm-recovery/ (extraction toolkit)
│   ├── prompts/
│   ├── templates/
│   ├── registers/
│   ├── runs/
│   ├── sources/ ← Brand assets ingested
│   └── cursor-plugin/
│
├── swm-business/ (NEW — Decision 1)
│   ├── GOVERNANCE.md ← From kevlarkia/swm-system
│   ├── product/
│   ├── brand/
│   └── gtm/
│
├── rose-rocket-engine/ (newsletter mirror)
├── docs/
│   ├── SYSTEMS_HEALTH.md
│   ├── SWM_ENTERPRISE_MIGRATION_PLAN.md ← You are here
│   ├── SWM_MIGRATION_QUICK_REF.md
│   └── SWM_MIGRATION_CHECKLIST.md
│
├── AGENTS.md ← Updated with SWM context
└── README.md ← Updated with enterprise context

External Systems (Linked, Not Migrated):
├── Notion (CLOUT) ← Still used for intake/routing
├── Google Drive ← Archive only; active work here
└── Mac-local ← Source of truth for brand originals
```

## Phase Progression

```text
Phase 1: Planning (✅ COMPLETE)
═══════════════════════════════════════════════════════════
│ ✅ Migration plan created
│ ✅ Quick reference created
│ ✅ Implementation checklist created
│ ✅ AGENTS.md updated
│ ✅ README.md updated
│ ⏸️  Operator review pending
└─────────────────────────────────────────────────────────

Phase 2: Content Migration (⚠️ READY — Operator Actions Required)
═══════════════════════════════════════════════════════════
│
├─ 2.1: Brand Asset Ingest
│  │ ⚠️  Operator: Run ingest script on Mac
│  │ ⏸️  Commit metadata
│  │ ⏸️  Create recovery run log
│  │ ⏸️  Update AGENTS.md
│
├─ 2.2: Business Documentation Consolidation
│  │ 🔴 DECISION 1: Choose docs home (A/B/C/D)
│  │ ⏸️  Implement structure
│  │ ⏸️  Migrate/link materials
│  │ ⏸️  Update agent instructions
│
└─ 2.3: Repository Consolidation
   │ ⏸️  Complete repo inventory
   │ 🔴 DECISION 2: Merge vs. link per repo
   │ ⏸️  Execute consolidation
   │ ⏸️  Update cross-repo links
   └─────────────────────────────────────────────────────

Phase 3: Systems & Access (⏸️ WAITING FOR PHASE 2)
═══════════════════════════════════════════════════════════
│ 3.1: Enterprise Access Controls
│ 3.2: Secrets & Environment Variables
│ 3.3: CI/CD & Quality Gates
└─────────────────────────────────────────────────────────

Phase 4: Operational Readiness (⏸️ WAITING FOR PHASE 3)
═══════════════════════════════════════════════════════════
│ 4.1: Maintenance Runbooks
│ 4.2: Communication & Collaboration
│ 4.3: Monitoring & Observability
└─────────────────────────────────────────────────────────
```

## Decision Tree (Critical Path)

```text
START: Operator receives migration plan
│
├─ Decision 1: SWM Business Docs Home?
│  ├─ Option A: swm-business/ in this repo (public) ✓ RECOMMENDED
│  ├─ Option B: swm-business/ in this repo (private)
│  ├─ Option C: Keep kevlarkia/swm-system separate
│  └─ Option D: Notion as SSOT; sync to repo
│
├─ Decision 2: Repository Consolidation Strategy?
│  ├─ First: Complete inventory
│  ├─ Then: Decide per-repo (merge vs. link)
│  └─ Recommendation: Small/coupled → merge; large/independent → link
│
├─ Decision 3: Extend CI/CD with Tests? (OPTIONAL)
│  ├─ Defer unless tests exist ✓ RECOMMENDED
│  └─ Adding test infra is separate project
│
└─ Decision 4: Keep Repo Public?
   ├─ Yes (transparency aligns with brand) ✓ RECOMMENDED
   └─ No (go private — requires justification)
```

## Immediate Action Items (Top 3)

```text
1. OPERATOR REVIEW
   └─ Read: docs/SWM_ENTERPRISE_MIGRATION_PLAN.md
   └─ Decide: Decision 1 (business docs home)
   └─ Decide: Decision 4 (public vs. private)
   
2. BRAND INGEST (Phase 2.1)
   └─ On Mac: Run swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh
   └─ On Mac: Ensure /Users/fcaf/Documents/... is accessible
   └─ Commit: Ingested metadata (content stays gitignored)
   
3. REPO INVENTORY (Phase 2.3 Prep)
   └─ List: All SWM-related repos
   └─ Assess: kevlarkia/swm-system (governance)
   └─ Assess: kevlarkia/rose-rocket-engine (already mirrored)
   └─ Assess: Any others discovered
```

## Risk Heat Map

```text
HIGH IMPACT, HIGH LIKELIHOOD:
  🔴 Scope creep in Phase 2.2 (business docs consolidation)
     → Mitigation: Use phased approach; defer non-critical items

MEDIUM IMPACT, MEDIUM LIKELIHOOD:
  🟡 Brand asset ingest delayed
     → Mitigation: Simple execution task; operator action
  
  🟡 Repository merge complexity (git history conflicts)
     → Mitigation: Inventory first; merge small repos only
  
  🟡 Stale AGENTS.md after migration
     → Mitigation: Update in same PR as structural changes

LOW IMPACT, LOW LIKELIHOOD:
  🟢 Secrets exposure during migration
     → Mitigation: Audit first; use secret scanning
  
  🟢 Lost work during consolidation
     → Mitigation: CLOUT intake before large moves
```

## Success Criteria (At a Glance)

| Criterion | Measure |
| --- | --- |
| **Completeness** | All SWM assets have documented home |
| **Agent Readiness** | Cloud agents can locate content via AGENTS.md |
| **Operational Hygiene** | AGENTS.md and README.md match reality |
| **Collaboration Readiness** | Team can onboard from docs alone |
| **No Regressions** | Site, toolkit, Rose Rocket still work |

## Key Principles

- **Capability-driven, not calendar-driven** — No artificial deadlines; complete when ready
- **Phased approach** — Finish Phase N before starting Phase N+1
- **Parallel work within phases** — Tasks in same phase can often proceed concurrently
- **CLOUT intake** — Capture work before large structural changes
- **Update AGENTS.md in same PR** — Keep agent instructions truthful

## Documentation Suite

| Document | Purpose | Audience |
| --- | --- | --- |
| `SWM_ENTERPRISE_MIGRATION_PLAN.md` | Comprehensive strategy | Operator (review & decision) |
| `SWM_MIGRATION_QUICK_REF.md` | One-page summary | Operator (rapid reference) |
| `SWM_MIGRATION_CHECKLIST.md` | Task tracking | Operator + Agents (execution) |
| `SWM_MIGRATION_VISUAL.md` | Visual overview | Everyone (orientation) |

---

**Next Action:** Operator review of [full migration plan](SWM_ENTERPRISE_MIGRATION_PLAN.md), then execute Phase 2.1 (brand ingest).

**Questions?** File issues in this repo or discuss via preferred channel (Slack, Linear, Notion).
