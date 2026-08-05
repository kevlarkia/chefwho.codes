# Run 005 — OKRAM Brand Guide + SWM Logo Recovery

SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | 005 |
| Date | 2026-08-05 |
| Focus | OKRAM Brand Guide v0.1 HTML + SWM/OKRAM logo SVG drafts |
| Mode | Recovery-first · Canon gate disabled |
| Trigger | Post–Run 004 next gate (OKRAM HTML + logo hunt) |
| Ingest | SRC-BRAND-010, SRC-BRAND-011 (gitignored content/) |

**Important:** This run surfaces a **parent-brand proposal** that conflicts with
GOVERNANCE.md Tentative (SWM parent · af.style design). Conflicts are preserved,
not resolved.

---

## A. Source Register

| Source ID | Source | Platform | Date | Version | Coverage | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-BRAND-010 | AFSTYLE_05_OKRAM_Brand_Guide_v0.1_...html | AFSTYLE Brand & Identity archive | UNDATED | v0.1 draft | Parent-brand proposal, palette, type, architecture | Same bytes as Downloads/_projects copy |
| SRC-BRAND-011 | SWM SVG set + logo zips | AFSTYLE Brand & Identity archive | UNDATED | EXTERNAL-DRAFT | 4 SWM SVGs + 2 zips | Titles SwM black/white ± dot |

---

## B. Extraction Ledger

| Extraction ID | Category | Extracted Item | Evidence Label | Source ID | Location | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| EXT-B005-001 | Business Identity | Proposes **OKRAM** as public parent brand; SWM as optional legacy phrase / internal doctrine — not the face of the logo | VERBATIM | SRC-BRAND-010 | §00 Judgment | **[CONFLICT]** vs GOVERNANCE SWM parent |
| EXT-B005-002 | Business Identity | Spoken form “Oak Rim”; domain spine okr.am (+ okram.life/live/online/site claimed held) | VERBATIM | SRC-BRAND-010 | Header / Ownership | UNVERIFIED ownership this run |
| EXT-B005-003 | Brand and Publication Standards | Proposed stack: OKRAM parent → SIGNL intelligence → Career Intelligence offers; SWM not logo face | VERBATIM | SRC-BRAND-010 | Protect the sacred name | Conflicts GOVERNANCE af.style design entity under SWM |
| EXT-B005-004 | Brand and Publication Standards | Recommended seal: OKRAM as proper name only (no acronym) for logo & legal face | VERBATIM | SRC-BRAND-010 | §01b | |
| EXT-B005-005 | Brand and Publication Standards | Optional public line: “Opportunity Knowledge Research Authentication Movement” (Assessment→Authentication) | VERBATIM | SRC-BRAND-010 | §01d | Proposal, not sealed |
| EXT-B005-006 | Brand and Publication Standards | Palette hexes include `#2456C8` (Signal Blue) plus earth set: `#101612` `#1A2420` `#2A332E` `#3F6B57` `#7FAF8E` `#D8DED6` `#E7EBE5` `#EEF1EC` `#F7F8F5` `#0088CC` `#A67C52` `#8C2B2B` `#556056` | VERBATIM | SRC-BRAND-010 | CSS | Dual palette vs Doc Kit |
| EXT-B005-007 | Brand and Publication Standards | Type: Fraunces (serif display) + Manrope (sans) + ui-monospace — **not** DejaVu | VERBATIM | SRC-BRAND-010 | CSS font-family | **[CONFLICT]** vs Doc Kit glyph rule |
| EXT-B005-008 | Brand and Publication Standards | Emotional brief: rooted/deliberate/quiet — not “motion,” not “signal blue,” not campaign urgency | VERBATIM | SRC-BRAND-010 | Emotional case | Explicitly distances from Signal Blue mood |
| EXT-B005-009 | Brand and Publication Standards | SWM wordmark SVG drafts: black/white × with-dot/no-dot; titles “SwM — …” | VERBATIM | SRC-BRAND-011 | SVG title/aria | GAP-B003-002 partial close |
| EXT-B005-010 | Brand and Publication Standards | OKRAM logo concepts zip present (unopened internals this pass) | REFERENCE-ONLY | SRC-BRAND-011 | Zip | Next: unzip inventory |

---

## E. Conflict Register

| Conflict ID | Item A | Item B | Nature | Resolution |
| --- | --- | --- | --- | --- |
| CF-B005-001 | GOVERNANCE: SWM parent; af.style = design entity | OKRAM guide: OKRAM parent; SWM legacy/not logo face | Parent brand architecture | DEFERRED — EXTRACTION PHASE |
| CF-B005-002 | Doc Kit: DejaVu only + Signal Blue house mood | OKRAM guide: Fraunces/Manrope + anti–signal-blue emotional brief | Visual system fork | DEFERRED — EXTRACTION PHASE |
| CF-B005-003 | Doc Kit Signal Blue `#2456C8` as THE accent | OKRAM guide includes `#2456C8` yet text rejects “signal blue” feel | Token present vs mood prohibition | DEFERRED — EXTRACTION PHASE |

---

## F. Gap Register

| Gap ID | Item | Status |
| --- | --- | --- |
| GAP-B003-002 | Logo masters | **Partial** — SWM SVG drafts + OKRAM concepts zip ingested |
| GAP-B003-003 | EX003 Style Guide PDF | Still open |
| GAP-B003-004 | EX004 OKRAM Brand System PDF | HTML v0.1 draft recovered; locked 16-page PDF still missing |
| GAP-B005-001 | Unzip OKRAM logo concepts + swm-logo-svg zip manifests | Open |
| GAP-B005-002 | Quiet Voltage / af.style brand book (archive has many drafts) | Noted, not opened this run |

---

## G. Recovery Summary

| Metric | Count |
| --- | --- |
| New sources authorized/ingested | 2 |
| SWM SVG wordmarks | 4 |
| Logo zips | 2 |
| Architecture conflicts vs GOVERNANCE | 1 major (parent brand) |
| Visual system conflicts vs Doc Kit | 2 |

Artifacts:

- `swm-recovery/registers/logo-asset-inventory-run-005.md`
- Drop zones SRC-BRAND-010 / 011 (binaries gitignored)

### Next run gate

1. Unzip logo concept zips → file-level inventory  
2. Spot-check Quiet Voltage / af.style book against GOVERNANCE af.style role  
3. Operator: light Desktop → `00_Inbox` batch  

EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD. NO CANON
STATUS ASSIGNED.
