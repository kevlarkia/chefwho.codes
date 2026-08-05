# Run 004 — Document Kit Brand Token Dump

SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | 004 |
| Date | 2026-08-05 |
| Focus | Brand tokens from sealed Document Kit v2.1 |
| Mode | Recovery-first · Canon gate disabled |
| Trigger | Post–CHE-6; next gate from Run 003 option 2 |
| Primary source | `kevlarkia/swm-system` → `swm-document-kit.zip` (`SKILL.md`, `base.css`) |
| Artifact | `swm-recovery/registers/brand-token-register-document-kit-v2.1.md` |

## A. Source Register

| Source ID | Source | Platform | Date | Version | Coverage | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-KIT-001 | swm-document-kit.zip | swm-system private repo | 2026-07-08 pack | v2.1 (skill) / CSS header still says v2.0 | Color, type, layout, components | Accent sealed G2 Jul 8 |

## B. Extraction Ledger (Brand & Publication Standards)

| Extraction ID | Category | Extracted Item | Evidence Label | Source ID | Location | Date | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXT-B004-001 | Brand and Publication Standards | SIGNAL BLUE `#2456C8` is THE accent; Gate G2 closed Jul 8 2026; OKRAM blue-dot lineage | VERBATIM | SRC-KIT-001 | SKILL.md Color tokens | 2026-07-08 | Closes hex gap for house format |
| EXT-B004-002 | Brand and Publication Standards | Full token set: INK `#1A1A1A`, PAPER `#FFFFFF`, WARM PANEL `#F5F0EC`, WARM BORDER `#ECE7E3`, SEMANTIC RED `#8C2B2B`, critical fill `#F8EFEF` | VERBATIM | SRC-KIT-001 | SKILL.md + base.css | 2026-07-08 | See register |
| EXT-B004-003 | Brand and Publication Standards | Verification tag colors: VERIFIED `#3D6B3F`, CONFIRM `#B08D3C`, RECLASSIFIED `#8C2B2B`, RECON FIRST `#666` | VERBATIM | SRC-KIT-001 | SKILL.md | 2026-07-08 | |
| EXT-B004-004 | Brand and Publication Standards | Heritage Navy/Gold/Cream rescoped to Strategic Weekly Memo-style briefings only | VERBATIM | SRC-KIT-001 | SKILL.md | 2026-07-08 | |
| EXT-B004-005 | Brand and Publication Standards | Archived accents not in use: Growth Green `#2E7D5B`, Amber `#C8772A` | VERBATIM | SRC-KIT-001 | SKILL.md | 2026-07-08 | |
| EXT-B004-006 | Brand and Publication Standards | Glyph rule: DejaVu Sans only; no emoji | VERBATIM | SRC-KIT-001 | SKILL.md | 2026-07-08 | |
| EXT-B004-007 | Brand and Publication Standards | Typography scale (kicker → footer) as in register | SOURCE-SUMMARY | SRC-KIT-001 | SKILL.md Typography | 2026-07-08 | |
| EXT-B004-008 | Brand and Publication Standards | Render pipeline WeasyPrint → pdfplumber → pdftoppm page-1 check | VERBATIM | SRC-KIT-001 | SKILL.md intro | 2026-07-08 | |
| EXT-B004-009 | Brand and Publication Standards | Attribution footer string with AF.Style Holdings LLC + Charter v1.1 | VERBATIM | SRC-KIT-001 | SKILL.md Layout | 2026-07-08 | Legal footer still untouched per GOVERNANCE |
| EXT-B004-010 | Gaps and Unresolved Material | CSS file header still labels "Document Kit v2.0" while skill is v2.1 | CONFLICTING | SRC-KIT-001 | base.css L1 vs SKILL title | 2026-07-08 | DEFERRED |

## C–D. Prompt / Architecture

| Component | Type | Function | Source | Status |
| --- | --- | --- | --- | --- |
| Document Kit v2.1 | Design system / skill | House format for SWM-family PDFs | SRC-KIT-001 | Recovered tokens |
| Brand token register | Recovery artifact | Portable hex/type table | This run | Written |

## E. Conflict Register

| Conflict ID | Item A | Item B | Nature | Sources | Resolution |
| --- | --- | --- | --- | --- | --- |
| CF-B004-001 | base.css banner "v2.0" | SKILL "v2.1" / G2 sealed | Version label drift | SRC-KIT-001 | DEFERRED — EXTRACTION PHASE |
| CF-B004-002 | Brand Manual color families | Kit hex tokens | Coarse vs sealed tokens | Run 003 vs 004 | DEFERRED — EXTRACTION PHASE |

## F. Gap Register

| Gap ID | Missing/Unclear Item | Evidence | Required Source | Impact |
| --- | --- | --- | --- | --- |
| GAP-B003-001 | Exact hex/type for kit | Previously incomplete | Document Kit | **Closed this run** |
| GAP-B003-002 | Logo masters | Still absent | Brand kit / EX004 | Open |
| GAP-B003-003 | EX003 Sanitized Style Guide PDF | Not found on Mac probe | Install pack | Open |
| GAP-B003-004 | EX004 OKRAM Brand System PDF | HTML draft `OKRAM_Brand_Guide_v0.1` exists under Downloads/_projects — not the LOCKED 16-page PDF | Authorize HTML or find PDF | Partial lead |
| GAP-B003-006 | af.style entity in kit | Absent | GOVERNANCE write-through | Open |

## G. Recovery Summary

| Metric | Count |
| --- | --- |
| Kit sources read | 1 zip (2 files) |
| Brand ledger items | 10 |
| Hex tokens recovered | 14+ |
| Logo masters | 0 |
| Conflicts | 2 deferred |
| Gaps closed | 1 (kit hex/type) |

### Next run gate

1. Authorize + extract local `OKRAM_Brand_Guide_v0.1.html` (or locate EX004 PDF).
2. Logo master hunt (GAP-B003-002).
3. Light Desktop → Drive `00_Inbox` batch (CHE-6 leftover; structure ready).

EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD. NO CANON
STATUS ASSIGNED.
