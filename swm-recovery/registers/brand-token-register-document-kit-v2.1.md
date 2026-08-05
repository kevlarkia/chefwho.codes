# Brand Token Register — Document Kit v2.1

Source: `kevlarkia/swm-system` → `swm-document-kit.zip`  
Extracted: 2026-08-05 (Run 004)  
Mode: Recovery-first · Canon gate disabled  
Posture: GOVERNANCE.md Tentative (skill "SEALED" language = Tentative)

## Color tokens

| Token | Hex | Role |
| --- | --- | --- |
| INK | `#1A1A1A` | Covers, headers, body text |
| PAPER | `#FFFFFF` | Body ground |
| WARM PANEL | `#F5F0EC` | Panels, grids |
| WARM BORDER | `#ECE7E3` | Panel borders, table rules |
| SIGNAL BLUE | `#2456C8` | Accent (Gate G2, Jul 8 2026) · OKRAM blue-dot lineage |
| SEMANTIC RED | `#8C2B2B` | Critical callouts · anti-fab markers only |
| CRITICAL FILL | `#F8EFEF` | Critical callout background |
| VERIFIED | `#3D6B3F` | Verification tag |
| CONFIRM | `#B08D3C` | Verification tag |
| RECLASSIFIED | `#8C2B2B` | Verification tag |
| RECON FIRST | `#666666` | Verification tag (CSS `#666`) |
| Heritage Navy | `#1B2A4A` | Strategic Weekly Memo legacy only |
| Heritage Gold | `#B08D3C` | Strategic Weekly Memo legacy only |
| Heritage Cream | `#F7F3EA` | Strategic Weekly Memo legacy only |

Archived accents (not in use): Growth Green `#2E7D5B`, Amber `#C8772A`.

## Typography

| Element | Spec |
| --- | --- |
| Font family | DejaVu Sans only (glyph rule — no emoji) |
| Safe symbols | ▸ ◆ ▼ ✓ · ⚠ |
| Kicker | 6.5–7pt caps, 3–4px letter-spacing |
| Title | 21–24pt bold, sentence case, max two lines |
| Section numeral | 18–20pt bold accent, two digits; 00 = provenance |
| Section subtitle | 6.8pt caps, 3px spacing, grey |
| Micro-label | 6.3pt caps, 2.5px spacing, grey |
| Body | 9–9.5pt, 1.5 line-height |
| Footer | Letterspaced kit/version/date left; PAGE 0X/0Y right |

## Layout (short)

- Full-bleed INK cover band → audience device → executive read (WARM panel,
  accent left border) → provenance note → body → attribution footer
- Attribution: Clinton Fernandez · AF.Style Holdings LLC · Charter v1.1
- Pipeline: HTML+CSS → WeasyPrint → PDF → pdfplumber page count → pdftoppm
  page-1 visual check

## Notes vs GOVERNANCE / Run 003

- Hex/type gap from Run 003 (GAP-B003-001) **closed** for Document Kit surface
- Logo masters and EX003/EX004 install PDFs still open
- Brand Manual color *families* (navy/blue/emerald) remain coarser than these
  tokens — CF-B003-005 still deferred
- af.style design-entity language still absent from kit text (GAP-B003-006)
