# Run 003 — Brand-Focused Source Extraction

SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | 003 |
| Date | 2026-08-05 |
| Focus | Brand Assets — verbatim extraction (Prompt 1 brand-primary) |
| Mode | Recovery-first · Canon gate disabled |
| Trigger | CHE-6 after Run 002 ingest + Drive folder mkdir |
| Sources read | SRC-BRAND-001…009 (content present) |
| Primary depth | 001, 002, 003, 004, 005 (brand page), 006, 007, 009 |
| Light pass | 008 (manifest only; full sweep prompt not re-executed) |

Governing posture for *interpretation* (not exclusion): `GOVERNANCE.md` v1.0
Tentative — conflicts preserved with DEFERRED resolution.

---

## A. Source Register

| Source ID | Source | Platform | Date | Version | Coverage | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-BRAND-001 | 08_SWM_Brand_Standards_Manual_v1.0.md | Ingested Mac / Institutional Suite | 2026-07-09 | v1.0 RC1 | Brand foundation → governance | Short manual; color/type [TO BE COMPLETED] |
| SRC-BRAND-002 | SWM-Setup-05-Trademark-Brand.pdf | Ingested Mac / Setup Series | 2026-07-10 | v1.0 | Trademark + interim brand protection | One-pager; Bloom logo mark parked |
| SRC-BRAND-003 | 05_SWM_Investor_Pitch_Deck_v1.0.md | Ingested Mac / Institutional Suite | 2026-07-09 | v1.0 RC1 | Slide narrative; architecture names | Visual design [TO BE COMPLETED] |
| SRC-BRAND-004 | 02_SWM_Master_Business_Plan_v1.0.md | Ingested Mac / Institutional Suite | 2026-07-09 | v1.0 RC1 | Identity + products + positioning | DBA details incomplete |
| SRC-BRAND-005 | SWM Business OS v0.1 INTERNAL.pdf | Ingested Mac | Unknown (v0.1) | v0.1 | Brand & Positioning §04 sealed Jun 27 lines | INTERNAL |
| SRC-BRAND-006 | SWM AI Governance Manual v1.0.md | Ingested Mac / Corporate Legal | 2026-07-09 | v1.0 RC1 | AI system brand roles | Brand-adjacent |
| SRC-BRAND-007 | SWM_EX002_INST-002_RPRT_20260509.docx | Ingested Mac / install pack | 2026-05-09 | Install 002 | Document registry; points to style/brand guides | Registry only |
| SRC-BRAND-008 | Universal Recovery Sweep Prompt zip | Ingested Mac | 2026-07-22 | v1.0 | Methodology pack | Not brand-primary |
| SRC-BRAND-009 | swm-standing-rules.zip → SKILL.md | Ingested Mac | 2026-07-08 | pre-rev-4 skill | Naming, attribution, footer | Stale vs GOVERNANCE Tentative |

---

## B. Extraction Ledger (Brand & Publication Standards + identity)

| Extraction ID | Category | Extracted Item | Evidence Label | Source ID | Location | Date | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXT-B003-001 | Brand and Publication Standards | Brand promise line: "Better Intelligence. Better Decisions. Better Futures." | VERBATIM | SRC-BRAND-001 | §1 Brand Foundation | 2026-07-09 | Canon salvage Jul 9 parked this line — [CONFLICT] with later park |
| EXT-B003-002 | Business Identity | Mission framing: improve workforce outcomes via intelligence, education, responsible AI, enterprise governance | SOURCE-SUMMARY | SRC-BRAND-001 | §1 | 2026-07-09 | |
| EXT-B003-003 | Brand and Publication Standards | Parent brand named SWM; product brands listed: Career Intelligence, Employer Intelligence, Workforce Intelligence, Compassion Package, Lighthouse, OKRAM AI, SIGNL, Bloom, Hazel Warden, OSH | VERBATIM | SRC-BRAND-001 | §2 Brand Architecture | 2026-07-09 | "Compassion Package" spelling [CONFLICT] with standing rules "Compassionate Package" |
| EXT-B003-004 | Brand and Publication Standards | Personality: intelligent, trustworthy, professional, optimistic, analytical, practical, human-centered, innovative, responsible | VERBATIM | SRC-BRAND-001 | §3 | 2026-07-09 | |
| EXT-B003-005 | Brand and Publication Standards | Voice: clear, confident, precise, empathetic, evidence-based, professional, plain-language, data-informed, future-focused | VERBATIM | SRC-BRAND-001 | §4 | 2026-07-09 | |
| EXT-B003-006 | Brand and Publication Standards | Logo principles: intelligence, movement, growth, structure, trust | VERBATIM | SRC-BRAND-001 | §6 | 2026-07-09 | No master files |
| EXT-B003-007 | Brand and Publication Standards | Color families: deep navy, intelligent blue, emerald green, white, slate gray — exact values [TO BE COMPLETED] | VERBATIM / INCOMPLETE | SRC-BRAND-001 | §6 | 2026-07-09 | Hex tokens absent |
| EXT-B003-008 | Brand and Publication Standards | Typography specifications [TO BE COMPLETED] | INCOMPLETE | SRC-BRAND-001 | §6 | 2026-07-09 | |
| EXT-B003-009 | Brand and Publication Standards | Every document includes logo, version, classification, publication date, footer, page numbering, revision history, source refs when applicable | VERBATIM | SRC-BRAND-001 | §8 | 2026-07-09 | |
| EXT-B003-010 | Brand and Publication Standards | Marketing: verified claims, educational value, evidence-based messaging, customer outcomes, responsible AI | VERBATIM | SRC-BRAND-001 | §10 | 2026-07-09 | |
| EXT-B003-011 | Brand and Publication Standards | Social categories: workforce insights, AI education, career intelligence, employer intelligence, permitted customer stories, research, community | VERBATIM | SRC-BRAND-001 | §11 | 2026-07-09 | |
| EXT-B003-012 | Workflows and Operations | Brand governance cadence: annual audit, quarterly content review, trademark monitoring, style-guide updates, template maintenance, asset management, pre-pub brand review | VERBATIM | SRC-BRAND-001 | §12 | 2026-07-09 | |
| EXT-B003-013 | Brand and Publication Standards | Federal word-mark strategy: SMART WORKFORCE MOVEMENT; Class 35 core; $350/class ID Manual; use-based after first SWM LLC client engagement; Bloom logo mark later wave | VERBATIM | SRC-BRAND-002 | Executive read + steps | 2026-07-10 | Class strategy CONFIRM attorney |
| EXT-B003-014 | Brand and Publication Standards | Interim mark use: ™ now; ® only after registration; Setup 03 domain + Bloom-branded use build common-law record | VERBATIM | SRC-BRAND-002 | Step 05 | 2026-07-10 | |
| EXT-B003-015 | Brand and Publication Standards | Later wave PARK: Bloom logo mark, OKRAM AI / SIGNL marks, Class 42 SaaS | VERBATIM | SRC-BRAND-002 | Step 06 | 2026-07-10 | |
| EXT-B003-016 | Brand and Publication Standards | Attribution on Setup 05: Clinton Fernandez · AF.Style Holdings LLC · Charter v1.1 | VERBATIM | SRC-BRAND-002 | Footer | 2026-07-10 | Aligns with standing-rules footer; legal line untouched per GOVERNANCE |
| EXT-B003-017 | Program Architecture | Six divisions: Career, Learning, Business, Community, Labs, Foundation; platforms OKRAM AI, SIGNL, Bloom, Hazel Warden, OSH, Lighthouse | VERBATIM | SRC-BRAND-003 | Slide 5 | 2026-07-09 | |
| EXT-B003-018 | Brand and Publication Standards | Pitch deck visual branding [TO BE COMPLETED] | INCOMPLETE | SRC-BRAND-003 | Design Notes | 2026-07-09 | |
| EXT-B003-019 | Business Identity | SWM under AF.Style Holdings LLC; DBA/legal details [TO BE COMPLETED] | VERBATIM / INCOMPLETE | SRC-BRAND-004 | §2 | 2026-07-09 | [CONFLICT] vs GOVERNANCE Tentative SWM parent / af.style design entity |
| EXT-B003-020 | Products and Services | Product list includes Lighthouse/Compassion Package initiatives | VERBATIM | SRC-BRAND-004 | §6 | 2026-07-09 | Spelling conflict again |
| EXT-B003-021 | Brand and Publication Standards | Brand positioning label: Workforce Intelligence | VERBATIM | SRC-BRAND-004 | §8 | 2026-07-09 | |
| EXT-B003-022 | Brand and Publication Standards | Sealed Jun 27 brand statement: "Empowering Human Potential Through Intelligent Technology" | VERBATIM | SRC-BRAND-005 | §04 Brand & Positioning | OS v0.1 | |
| EXT-B003-023 | Brand and Publication Standards | Tagline: "Human Potential. Amplified by AI." (evolution path AI → Technology → Intelligence) | VERBATIM | SRC-BRAND-005 | §04 | OS v0.1 | |
| EXT-B003-024 | Brand and Publication Standards | Voice (OS): Clear · Optimistic · Practical · Inclusive · Modern · Trusted · Intelligent without being intimidating | VERBATIM | SRC-BRAND-005 | §04 | OS v0.1 | Partial overlap with Brand Manual §4 |
| EXT-B003-025 | Brand and Publication Standards | House format lives in swm-document-kit skill v2.1 (colors, type, components, taxonomy) | VERBATIM | SRC-BRAND-005 | §06 SOP index | OS v0.1 | Kit not re-opened this run |
| EXT-B003-026 | AI Systems | Brand-role map: Hazel Warden = executive intelligence; OKRAM = enterprise; SIGNL = reporting; Bloom = learning; OSH = governance; Lighthouse = strategic | VERBATIM | SRC-BRAND-006 | §3 | 2026-07-09 | |
| EXT-B003-027 | Brand and Publication Standards | Install registry cites LOCKED: SWM_EX003 Sanitized Style Guide (11-page PDF); SWM_EX004 OKRAM Brand System Guide (16-page PDF) | VERBATIM | SRC-BRAND-007 | Registry table | 2026-05-09 | Files not in authorized ingest set — GAP |
| EXT-B003-028 | Brand and Publication Standards | Naming convention for case docs: [CASE]_[EXHIBIT]_[ORDER]_[TYPE]_[DATE] under AF.Style Holdings LLC | VERBATIM | SRC-BRAND-007 | Body | 2026-05-09 | |
| EXT-B003-029 | Brand and Publication Standards | Standing rules: SWM sole meaning; Compassionate Package spelling; footer AF.Style Holdings LLC; anti-fabrication; sealed decisions stated flat | VERBATIM | SRC-BRAND-009 | SKILL.md | 2026-07-08 | "SEALED" language = Tentative under GOVERNANCE |

---

## C. Prompt & Tool Register

| Item ID | Name | Type | Purpose | Input | Output | Dependencies | Source | Completeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PT-B003-001 | swm-standing-rules skill | Rules skill | Non-negotiable naming/attribution/separation | SWM outputs | Constrained deliverables | Mounted in Claude | SRC-BRAND-009 | Recovered (pre-rev-4 text) |
| PT-B003-002 | Universal Recovery Sweep Prompt pack | Prompt pack | Recovery sweep methodology | Zip | Sweep outputs | Unzip | SRC-BRAND-008 | Present; not re-run |
| PT-B003-003 | Document Kit v2.1 (referenced) | Design system | Colors, type, components | Kit skill/repo | Rendered docs | swm-system zip | SRC-BRAND-005 | REFERENCE-ONLY this run |

---

## D. Architecture Register (brand-related)

| Component | Type | Function | Connected Components | Source | Status in Source |
| --- | --- | --- | --- | --- | --- |
| Brand Standards Manual v1.0 RC1 | Brand system doc | Enterprise brand system outline | Pitch, Business Plan, OS | SRC-BRAND-001 | INCOMPLETE (tokens) |
| Trademark Setup 05 | Legal/brand step-map | Word-mark filing path | Bloom logo later; domains | SRC-BRAND-002 | Operational / CONFIRM |
| Bloom | Visual / product brand | Logo mark + learning platform (dual mention) | Trademark later wave; AI arch | 002, 003, 006 | Logo not recovered |
| Document Kit v2.1 | House format | Visual tokens + components | Standing rules, CIE | SRC-BRAND-005 | Referenced sealed |
| EX003 Style Guide | Locked install asset | Sanitized style guide PDF | Install registry | SRC-BRAND-007 | Missing from ingest |
| EX004 OKRAM Brand System | Locked install asset | OKRAM brand guide PDF | Install registry | SRC-BRAND-007 | Missing from ingest |
| af.style (GOVERNANCE) | Style/design entity under SWM | Tentative architecture v1.0 | SWM parent brand | GOVERNANCE.md | Not in these sources |

---

## E. Conflict Register

| Conflict ID | Item A | Item B | Nature of Conflict | Sources | Resolution |
| --- | --- | --- | --- | --- | --- |
| CF-B003-001 | Brand Manual: "Compassion Package" | Standing rules: "Compassionate Package" | Spelling / product name | 001 vs 009 | DEFERRED — EXTRACTION PHASE |
| CF-B003-002 | Brand Manual promise: Better Intelligence… | Canon salvage Jul 9: brand promise PARKED | Live vs parked claim | 001 vs Canon memory | DEFERRED — EXTRACTION PHASE |
| CF-B003-003 | Docs place SWM under AF.Style Holdings LLC | GOVERNANCE Tentative: SWM parent; af.style = design entity | Legal vs market architecture | 001/004/002 vs GOVERNANCE | DEFERRED — EXTRACTION PHASE (footer untouched) |
| CF-B003-004 | Brand Manual voice list | Business OS voice list | Overlap incomplete; not identical | 001 vs 005 | DEFERRED — EXTRACTION PHASE |
| CF-B003-005 | Brand Manual color families (navy/blue/emerald…) | Doc Kit Signal Blue #2456C8 (not in these files) | Token set may have moved | 001 vs kit (external) | DEFERRED — EXTRACTION PHASE |

---

## F. Gap Register

| Gap ID | Missing/Unclear Item | Evidence | Required Source | Impact |
| --- | --- | --- | --- | --- |
| GAP-B003-001 | Exact hex / type tokens | Manual marks [TO BE COMPLETED] | Design kit / sealed Document Kit dump | Blocks production brand rebuild |
| GAP-B003-002 | Logo masters (SVG/PNG/PDF) | Trademark parks Bloom logo; no files | Brand kit / EX004 / design folder | Blocks mark recovery |
| GAP-B003-003 | SWM_EX003 Sanitized Style Guide PDF | Registry LOCKED 11-page | Authorize + ingest | Likely primary visual rules |
| GAP-B003-004 | SWM_EX004 OKRAM Brand System Guide PDF | Registry LOCKED 16-page | Authorize + ingest | OKRAM visual system |
| GAP-B003-005 | Pitch deck designed visuals | Design notes incomplete | Designed PPTX/PDF | Motif examples |
| GAP-B003-006 | af.style entity language in source corpus | Absent from 001–009 | New brand architecture write-up | Align sources with GOVERNANCE |

---

## G. Recovery Summary

| Metric | Count |
| --- | --- |
| Sources with readable content | 9/9 |
| Brand ledger items this run | 29 |
| Verbatim visual token values (hex/fonts) | 0 |
| Logo masters recovered | 0 |
| Conflicts opened | 5 (deferred) |
| New gaps | 6 |
| Canon status assigned | None |

### CHE-6 operator side (same session)

| Item | Status |
| --- | --- |
| Run 002 / PR #21 | Merged |
| Drive folders created on My Drive | `00_Inbox`, `01_Active`, `02_Reference`, `Archive` (empty) |
| Desktop/Downloads → Inbox batch | Still deferred (structure ready) |

### Next run gate

Run **004** candidates (pick one):

1. Authorize + ingest EX003 Style Guide + EX004 OKRAM Brand System (closes GAP-B003-003/004).
2. Dump Document Kit v2.1 tokens from `swm-document-kit.zip` into a brand token register.
3. Light Desktop → `00_Inbox` batch (operator preference).

EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD. NO CANON
STATUS ASSIGNED.
