# SWM Enterprise Migration — Quick Reference

**Status:** Planning complete — Ready for Phase 2 execution  
**Full Plan:** See `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md`

## What's Happening

The **SWa Works** GitHub enterprise has been created, and this repository
(`kevlarkia/chefwho.codes`) will become the unified home for:

- **SWM Recovery Toolkit** (already here under `swm-recovery/`)
- **SWM Business Operations** (brand, product, governance)
- **Personal Site** (chefwho.codes)
- **Rose Rocket Engine** (newsletter mirror)

## Immediate Actions Required

### 1. Brand Asset Ingest (Operator Action)

**Current blocker:** SWM brand sources are Mac-local and not yet ingested.

**Action:**

```bash
cd /Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE
/path/to/chefwho.codes/swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh
```

Then commit ingested metadata and create recovery run log
(`swm-recovery/runs/007-brand-full-ingest.md`).

### 2. Decide on Business Docs Home (Decision 1)

**Question:** Where should SWM business docs (product vision, architecture,
GTM) live?

**Options:**

- **A:** `swm-business/` in this repo (public, recommended)
- **B:** `swm-business/` in this repo (private)
- **C:** Keep separate `kevlarkia/swm-system` repo
- **D:** Notion as SSOT; sync to repo for agents

**Recommended:** Option A (public with clear boundaries)

### 3. Repository Inventory (Phase 2.3 Prep)

**Action:** List all SWM-related repos and decide merge vs. link strategy.

**Known repos:**

- `kevlarkia/chefwho.codes` (this one, primary)
- `kevlarkia/swm-system` (private governance)
- `kevlarkia/rose-rocket-engine` (upstream mirror)

**Unknown:** Complete the inventory.

## Migration Phases (High Level)

| Phase | Status | Key Blocker |
| --- | --- | --- |
| **Phase 1: Planning** | ✅ Complete | (this document) |
| **Phase 2: Content Migration** | ⚠️ Ready | Brand ingest, Decision 1 |
| **Phase 3: Systems & Access** | ⏸️ Waiting | Phase 2 completion |
| **Phase 4: Operational Readiness** | ⏸️ Waiting | Phase 3 completion |

## Key Principles

- **No calendar timelines** — this is capability-driven, not date-driven
- **Phased approach** — complete Phase 2 before Phase 3
- **Parallel work** — within phases, many tasks can proceed concurrently
- **CLOUT intake** — capture any work artifacts before large structural changes
- **Update AGENTS.md** — keep agent instructions truthful in same PR as
  changes

## Next Steps (Priority Order)

1. **Review this plan** — Operator reviews
   `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md`
2. **Run brand ingest** — Execute Phase 2.1 (operator action on Mac)
3. **Answer Decision 1** — Choose business docs home (enables Phase 2.2)
4. **Complete repo inventory** — Unblock Phase 2.3
5. **Execute Phase 2** — Content migration (can parallelize 2.1, 2.2, 2.3)

## Questions or Issues

File issues in this repo or discuss in your preferred channel (Slack, Linear,
Notion, etc.). Tag @kevlarkia for operator decisions.

---

**Created:** 2026-08-13

**Documentation Suite:**

- `docs/SWM_ENTERPRISE_MIGRATION_PLAN.md` — Comprehensive strategy
- `docs/SWM_MIGRATION_QUICK_REF.md` — This document (quick reference)
- `docs/SWM_MIGRATION_CHECKLIST.md` — Checkbox tracking
- `docs/SWM_MIGRATION_VISUAL.md` — Visual overview and diagrams
