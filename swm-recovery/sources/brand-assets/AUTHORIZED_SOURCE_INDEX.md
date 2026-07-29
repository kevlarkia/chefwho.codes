# Brand Assets — Authorized Source Index

Category focus: **Brand Assets (Logos & Visuals)**  
Authorization date: 2026-07-25  
Operating mode: Recovery-first · Canon gate disabled

These paths were authorized by the operator for SWM brand/logo/visual
recovery. They reside on the operator Mac (`/Users/fcaf/...`) and are
**not mounted** in the cloud agent environment until copied into each
source's `content/` folder.

| Source ID | Priority | Brand relevance | Local path (authorized) | Ingest status |
| --- | --- | --- | --- | --- |
| SRC-BRAND-001 | P1 Core | Brand standards manual (primary) | `.../08_SWM_Brand_Standards_Manual_v1.0.md` | PENDING — file not in workspace |
| SRC-BRAND-002 | P1 Core | Trademark / brand setup PDF | `.../SWM-Setup-05-Trademark-Brand.pdf` | PENDING — file not in workspace |
| SRC-BRAND-003 | P2 Visual | Investor pitch deck (visual motifs) | `.../05_SWM_Investor_Pitch_Deck_v1.0.md` | PENDING — file not in workspace |
| SRC-BRAND-004 | P2 Identity | Master business plan (identity narrative) | `.../02_SWM_Master_Business_Plan_v1.0.md` | PENDING — file not in workspace |
| SRC-BRAND-005 | P2 System UI | SWM Business OS v0.1 INTERNAL PDF | `.../SWM Business OS v0.1 INTERNAL.pdf` | PENDING — file not in workspace |
| SRC-BRAND-006 | P3 Adjacent | AI Governance Manual (may cite brand rules) | `.../AFS-REC-000793_...SWM_AI_Governance_Manual_v1.0_...md` | PENDING — file not in workspace |
| SRC-BRAND-007 | P3 Adjacent | EX002 INST-002 report DOCX | `.../SWM_EX002_INST-002_RPRT_20260509.docx` | PENDING — file not in workspace |
| SRC-BRAND-008 | P3 Pack | Universal Recovery Sweep Prompt zip | `.../SWM-Universal-Recovery-Sweep-Prompt-v1.0.zip` | PENDING — file not in workspace |
| SRC-BRAND-009 | P3 Pack | Standing rules zip (skills pack) | `.../swm-standing-rules.zip` | PENDING — file not in workspace |

## Ingest instruction

From the Mac, copy each file into the matching folder:

```bash
# Example (run locally, then sync/upload into this repo workspace)
BASE="swm-recovery/sources/brand-assets"
cp "/Users/fcaf/Downloads/SWM_Institutional_Documentation_Suite_v1.0/08_SWM_Brand_Standards_Manual_v1.0.md" \
  "$BASE/SRC-BRAND-001-brand-standards-manual/content/"
```

Or attach/upload the nine files into this cloud agent chat / workspace.
Do not commit proprietary originals to the public remote unless intended;
`content/` is gitignored.
