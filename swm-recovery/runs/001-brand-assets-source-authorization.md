# Run 001 — Brand Assets Source Authorization

SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | 001 |
| Date | 2026-07-25 |
| Focus | Brand Assets (Logos & Visuals) |
| Mode | Recovery-first · Canon gate disabled |
| Authorized paths supplied | 9 (Mac absolute paths) |
| Bytes ingested into workspace | 0 |
| Blocking condition | Paths are on operator Mac; cloud VM cannot read `/Users/fcaf/...` |

## A. Source Register

| Source ID | Source | Platform | Date | Version | Coverage | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-BRAND-001 | 08_SWM_Brand_Standards_Manual_v1.0.md | Local Downloads / Institutional Suite | v1.0 claim | v1.0 | Brand standards (expected) | P1 primary; PENDING ingest |
| SRC-BRAND-002 | SWM-Setup-05-Trademark-Brand.pdf | AFSTYLE archive / Local_Files | Unknown | Unknown | Trademark/brand setup (expected) | P1 primary; PENDING ingest |
| SRC-BRAND-003 | 05_SWM_Investor_Pitch_Deck_v1.0.md | Cursor bundle / iCloud | v1.0 claim | v1.0 | Visual motifs (expected) | P2; PENDING ingest |
| SRC-BRAND-004 | 02_SWM_Master_Business_Plan_v1.0.md | Local_Files / iCloud | v1.0 claim | v1.0 | Identity narrative (expected) | P2; PENDING ingest |
| SRC-BRAND-005 | SWM Business OS v0.1 INTERNAL.pdf | Cursor bundle / iCloud | v0.1 claim | v0.1 | Internal UI/brand (expected) | P2; INTERNAL flag; PENDING ingest |
| SRC-BRAND-006 | AFS-REC-000793 SWM AI Governance Manual | AFSTYLE Corporate/Legal | UNDATED | v1.0 canon-candidate | Governance; brand-adjacent | P3; canon label ignored; PENDING ingest |
| SRC-BRAND-007 | SWM_EX002_INST-002_RPRT_20260509.docx | afstyle-install-20260509-v1 | 2026-05-09 | Unknown | Report; brand uncertain | P3; PENDING ingest |
| SRC-BRAND-008 | SWM-Universal-Recovery-Sweep-Prompt-v1.0.zip | SWM-RECON-20260724-01 | v1.0 claim | v1.0 | Prompt pack | P3; PENDING ingest |
| SRC-BRAND-009 | swm-standing-rules.zip | SWM_Skills_Pack | Unknown | Unknown | Standing rules pack | P3; PENDING ingest |

## B. Extraction Ledger (Brand & Publication Standards)

| Extraction ID | Category | Extracted Item | Evidence Label | Source ID | Location | Date | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXT-B-001 | Brand and Publication Standards | Institutional suite includes dedicated Brand Standards Manual as document 08 | INFERRED | SRC-BRAND-001 | Filename + suite path | 2026-07-25 | Content unread |
| EXT-B-002 | Brand and Publication Standards | Trademark/brand setup artifact exists as SWM-Setup-05 | INFERRED | SRC-BRAND-002 | Filename | 2026-07-25 | Content unread |
| EXT-B-003 | Brand and Publication Standards | Investor pitch deck v1.0 likely carries logo/visual system examples | INFERRED | SRC-BRAND-003 | Filename + suite doc 05 | 2026-07-25 | Content unread |
| EXT-B-004 | Business Identity | Master Business Plan v1.0 exists in Institutional Suite as doc 02 | REFERENCE-ONLY | SRC-BRAND-004 | Filename | 2026-07-25 | Brand-adjacent |
| EXT-B-005 | Brand and Publication Standards | SWM Business OS v0.1 INTERNAL may embed product UI branding | INFERRED | SRC-BRAND-005 | Filename + INTERNAL claim | 2026-07-25 | Content unread |
| EXT-B-006 | Workflows and Operations | AI Governance Manual flagged CANON-CANDIDATE / UNDATED / vUnknown | VERBATIM | SRC-BRAND-006 | Filename tokens | 2026-07-25 | Canon status not used for inclusion |
| EXT-B-007 | Gaps and Unresolved Material | All 9 authorized brand sources unreachable from cloud workspace | VERBATIM | SRC-ENV | Path probe 2026-07-25 | 2026-07-25 | Blocks logo/visual verbatim recovery |
| EXT-B-008 | Program Architecture | Institutional Documentation Suite v1.0 contains at least docs 02, 05, 08 | INFERRED | SRC-BRAND-001/003/004 | Shared suite path | 2026-07-25 | Implies fuller suite elsewhere |
| EXT-B-009 | Prompts and Instructions | Universal Recovery Sweep Prompt pack v1.0 and standing-rules zip authorized | REFERENCE-ONLY | SRC-BRAND-008/009 | Filenames | 2026-07-25 | Not brand-primary |

### Not recovered (content required)

Logos (SVG/PNG/PDF masters), typography tokens, color palette, visual motifs,
clearspace/usage rules, document hierarchy standards, trademark classes,
incorrect-use examples — all **REFERENCE-ONLY / missing** until P1 files ingest.

## C. Prompt & Tool Register

| Item ID | Name | Type | Purpose | Input | Output | Dependencies | Source | Completeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PT-B-001 | Universal Recovery Sweep Prompt pack | Prompt pack (zip) | Recovery sweep | Zip contents | Unknown | Unzip + ingest | SRC-BRAND-008 | Unrecovered |
| PT-B-002 | SWM standing rules | Rules pack (zip) | Standing operating rules | Zip contents | Unknown | Unzip + ingest | SRC-BRAND-009 | Unrecovered |

## D. Architecture Register (brand-related)

| Component | Type | Function | Connected Components | Source | Status in Source |
| --- | --- | --- | --- | --- | --- |
| SWM Institutional Documentation Suite v1.0 | Document suite | Institutional canon-candidate docs | Brand Manual, Pitch Deck, Business Plan | SRC-BRAND-001/003/004 | REFERENCE-ONLY |
| SWM Business OS v0.1 | Internal product surface | Business OS (INTERNAL) | Brand system (unknown) | SRC-BRAND-005 | REFERENCE-ONLY |
| Brand Standards Manual | Brand component | Logo/visual standards (expected) | Pitch deck, OS, reports | SRC-BRAND-001 | PENDING ingest |
| Trademark Brand Setup (05) | Legal/brand component | Trademark/brand setup | Brand Standards Manual | SRC-BRAND-002 | PENDING ingest |

## E. Conflict Register

| Conflict ID | Item A | Item B | Nature of Conflict | Sources | Resolution |
| --- | --- | --- | --- | --- | --- |
| CF-B-001 | Institutional Suite copies under Downloads | Same suite under Cursor bundle / Local_Files iCloud paths | Possible duplicate versions of suite docs across preservation roots | SRC-BRAND-001 vs 003/004 paths | DEFERRED — EXTRACTION PHASE |
| CF-B-002 | AI Governance Manual CANON-CANDIDATE label | Recovery-first inclusion rule | Filename claims canon-candidate; recovery ignores canon gating | SRC-BRAND-006 | DEFERRED — EXTRACTION PHASE |

## F. Gap Register

| Gap ID | Missing/Unclear Item | Evidence | Required Source | Impact |
| --- | --- | --- | --- | --- |
| GAP-B-001 | Verbatim Brand Standards Manual body | Path authorized; file absent in VM | SRC-BRAND-001 content ingest | Blocks Volume 7 primary |
| GAP-B-002 | Trademark/brand PDF text + embedded marks | Path authorized; file absent in VM | SRC-BRAND-002 content ingest | Blocks logo/legal mark recovery |
| GAP-B-003 | Actual logo master files (SVG/PNG/PDF) | Not listed in authorized path set | Brand kit / logo export folder | May remain missing even after manuals ingest |
| GAP-B-004 | Pitch deck visual specs | Path authorized; unread | SRC-BRAND-003 | Blocks motif examples |
| GAP-B-005 | Business OS UI brand tokens | Path authorized; unread | SRC-BRAND-005 | Blocks product UI brand rebuild |
| GAP-B-006 | Full Institutional Suite inventory (docs 01–N) | Only 02, 05, 08 path-attested | Suite root folder ingest | Incomplete suite coverage |
| GAP-B-007 | Standing rules / sweep pack internals | Zips unread | SRC-BRAND-008/009 unzip | May hold brand constraints |

## G. Recovery Summary

| Metric | Count |
| --- | --- |
| Paths authorized this run | 9 |
| Sources ingested (bytes readable) | 0 |
| Brand ledger items (metadata-level) | 9 |
| Verbatim logo/visual rules recovered | 0 |
| Conflicts opened | 2 (deferred) |
| Gaps opened | 7 |
| Canon status assigned | None |

## Prompt 4 — Prioritized brand recovery actions

| Priority | Gap ID | Missing Source | Likely Location | Search Terms | Date Range | Substitute Evidence | Recovery Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GAP-B-001 | Brand Standards Manual v1.0 body | Operator Downloads Institutional Suite | `08_SWM_Brand_Standards` | Suite v1.0 | Pitch deck visuals | Copy into `SRC-BRAND-001/.../content/` |
| 2 | GAP-B-002 | Trademark Brand PDF | AFSTYLE Local_Files Downloads | `SWM-Setup-05-Trademark-Brand` | Unknown | Brand manual trademark section | Copy into `SRC-BRAND-002/.../content/` |
| 3 | GAP-B-003 | Logo masters | Brand kit / Design folders / iCloud SWM | `logo`, `.svg`, `.png`, `wordmark` | All | Raster embeds in PDF/DOCX | Locate and authorize logo folder |
| 4 | GAP-B-004/005 | Pitch deck + Business OS | Cursor bundle 2026-07-21 | `Investor_Pitch`, `Business OS` | 2026-07 bundle | Published PDFs | Copy SRC-BRAND-003 and 005 |
| 5 | GAP-B-006 | Remaining Institutional Suite docs | Same suite roots as 02/05/08 | `SWM_Institutional_Documentation_Suite` | v1.0 | Partial docs already listed | Authorize full suite folder |
| 6 | GAP-B-007 | Zips (rules/prompts) | SWM-RECON consolidation | `standing-rules`, `Recovery-Sweep` | 2026-07-24 recon | None | Copy + unzip SRC-BRAND-008/009 |

## Next run gate

Run `002` only after at least **SRC-BRAND-001** and **SRC-BRAND-002** are
present under their `content/` folders (or attached in-chat). Then execute
Prompt 1 brand-focused verbatim extraction and Prompt 2 for any brand rules
inside the zips.

EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD. NO CANON STATUS ASSIGNED.
