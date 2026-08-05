# Run 002 — Brand Assets Mac Ingest

SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | 002 |
| Date | 2026-08-05 |
| Focus | Brand Assets (Logos & Visuals) — Mac ingest |
| Mode | Recovery-first · Canon gate disabled |
| Trigger | CHE-6 (Systems Health) |
| Authorized paths supplied | 9 (Mac absolute paths from Run 001) |
| Bytes ingested into workspace | 228437 |
| Script | `swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh` |
| Blocking condition | Cleared for SRC-BRAND-001…009 content drop zones |

## Ingest results

| Source ID | Result | Bytes | Destination (gitignored) |
| --- | --- | --- | --- |
| SRC-BRAND-001 | OK | 3811 | `.../SRC-BRAND-001-.../content/08_SWM_Brand_Standards_Manual_v1.0.md` |
| SRC-BRAND-002 | OK | 23374 | `.../SRC-BRAND-002-.../content/SWM-Setup-05-Trademark-Brand.pdf` |
| SRC-BRAND-003 | OK | 4590 | `.../SRC-BRAND-003-.../content/05_SWM_Investor_Pitch_Deck_v1.0.md` |
| SRC-BRAND-004 | OK | 6385 | `.../SRC-BRAND-004-.../content/02_SWM_Master_Business_Plan_v1.0.md` |
| SRC-BRAND-005 | OK | 156416 | `.../SRC-BRAND-005-.../content/SWM Business OS v0.1 INTERNAL.pdf` |
| SRC-BRAND-006 | OK | 4693 | `.../SRC-BRAND-006-.../content/AFS-REC-000793_...md` |
| SRC-BRAND-007 | OK | 12259 | `.../SRC-BRAND-007-.../content/SWM_EX002_INST-002_RPRT_20260509.docx` |
| SRC-BRAND-008 | OK | 14928 | `.../SRC-BRAND-008-.../content/SWM-Universal-Recovery-Sweep-Prompt-v1.0.zip` |
| SRC-BRAND-009 | OK | 1981 | `.../SRC-BRAND-009-.../content/swm-standing-rules.zip` |

**9/9 OK · 0 MISS · 228437 bytes total.**

Proprietary originals stay gitignored under `swm-recovery/sources/**/content/**`
(README.md only is tracked).

## Gate check (from Run 001)

Run 001 required SRC-BRAND-001 and SRC-BRAND-002 under `content/` before
verbatim extraction. **Gate satisfied.**

## Operator Drive / Desktop notes (same CHE-6 pass)

| Check | Status |
| --- | --- |
| Fernandez Filing System top-level (`00_Inbox`, `01_Active`, `02_Reference`, `Archive`) on Google Drive My Drive | **NOT FOUND** at Drive root (My Drive is unstructured takeout/chat dumps) |
| Shared drives present | `SWM Shared Drive `, `chefwho.codes shared drive` — filing folders not confirmed this pass |
| Desktop item count | 49 |
| Downloads item count | 108 |
| Desktop/Downloads → Inbox batch | **Deferred** — no `00_Inbox` to receive into until filing structure is confirmed/created |

## Next run gate

Run **003** = Prompt 1 brand-focused verbatim extraction against ingested
`content/` (start with SRC-BRAND-001 + SRC-BRAND-002), then Prompt 2 for
zip internals (SRC-BRAND-008/009). Still out of scope until authorized:
logo master folder (GAP-B-003).

EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD. NO CANON
STATUS ASSIGNED.
