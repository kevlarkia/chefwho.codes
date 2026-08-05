# Brand Assets — Authorized Source Index

Category focus: **Brand Assets (Logos & Visuals)**  
Authorization date: 2026-07-25  
Last ingest: 2026-08-05 (Run 002)  
Operating mode: Recovery-first · Canon gate disabled

These paths were authorized by the operator for SWM brand/logo/visual
recovery. They reside on the operator Mac (`/Users/fcaf/...`) and are
copied into each source's gitignored `content/` folder via
`INGEST_FROM_MAC.sh`.

| Source ID | Priority | Brand relevance | Local path (authorized) | Ingest status |
| --- | --- | --- | --- | --- |
| SRC-BRAND-001 | P1 Core | Brand standards manual (primary) | `.../08_SWM_Brand_Standards_Manual_v1.0.md` | INGESTED 2026-08-05 (3811 B) |
| SRC-BRAND-002 | P1 Core | Trademark / brand setup PDF | `.../SWM-Setup-05-Trademark-Brand.pdf` | INGESTED 2026-08-05 (23374 B) |
| SRC-BRAND-003 | P2 Visual | Investor pitch deck (visual motifs) | `.../05_SWM_Investor_Pitch_Deck_v1.0.md` | INGESTED 2026-08-05 (4590 B) |
| SRC-BRAND-004 | P2 Identity | Master business plan (identity narrative) | `.../02_SWM_Master_Business_Plan_v1.0.md` | INGESTED 2026-08-05 (6385 B) |
| SRC-BRAND-005 | P2 System UI | SWM Business OS v0.1 INTERNAL PDF | `.../SWM Business OS v0.1 INTERNAL.pdf` | INGESTED 2026-08-05 (156416 B) |
| SRC-BRAND-006 | P3 Adjacent | AI Governance Manual (may cite brand rules) | `.../AFS-REC-000793_...SWM_AI_Governance_Manual_v1.0_...md` | INGESTED 2026-08-05 (4693 B) |
| SRC-BRAND-007 | P3 Adjacent | EX002 INST-002 report DOCX | `.../SWM_EX002_INST-002_RPRT_20260509.docx` | INGESTED 2026-08-05 (12259 B) |
| SRC-BRAND-008 | P3 Pack | Universal Recovery Sweep Prompt zip | `.../SWM-Universal-Recovery-Sweep-Prompt-v1.0.zip` | INGESTED 2026-08-05 (14928 B) |
| SRC-BRAND-009 | P3 Pack | Standing rules zip (skills pack) | `.../swm-standing-rules.zip` | INGESTED 2026-08-05 (1981 B) |

## Ingest instruction

From the Mac (repo root):

```bash
bash swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh
```

Do not commit proprietary originals to the public remote;
`content/` is gitignored (except `content/README.md`).
