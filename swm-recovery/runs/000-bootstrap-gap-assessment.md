# Run 000 — Bootstrap Gap Assessment

SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED

## Run metadata

| Field | Value |
| --- | --- |
| Run ID | 000 |
| Date | 2026-07-25 |
| Mode | Recovery-first · Canon gate disabled |
| Authorized sources supplied | None |
| Platforms checked (environment) | Local repo (`chefwho.codes`), Slack (keyword search), Box MCP (unauthenticated), Notion MCP (unauthenticated), Linear MCP (unauthenticated) |
| Extraction confidence overall | N/A — no SWM source corpus available |

## A. Source Register

| Source ID | Source | Platform | Date | Version | Coverage | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-ENV-001 | chefwho.codes repository working tree | GitHub | 2026-07-25 | HEAD | Site scaffold only | No SWM/Okram/SigNEL/Hazel/OSH/SDRWM content found |
| SRC-ENV-002 | Slack workspace search | Slack | 2026-07-25 | live | Keyword scan | Zero hits for SWM / Smart Workforce / Okram / SigNEL / Hazel Warden / SDRWM |
| SRC-ENV-003 | Box MCP | Box | — | — | Unavailable | Server requires authentication |
| SRC-ENV-004 | Notion MCP | Notion | — | — | Unavailable | Server requires authentication |
| SRC-ENV-005 | Linear MCP | Linear | — | — | Unavailable | Server requires authentication |
| SRC-META-001 | Refined SWM Extraction Prompt Suite (user-supplied) | Cursor agent message | 2026-07-25 | Recovery-First Edition | Methodology only | Operational prompts; not SWM business source material |

## B. Extraction Ledger

| Extraction ID | Category | Extracted Item | Evidence Label | Source ID | Location | Date | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXT-001 | Gaps and Unresolved Material | No authorized SWM source corpus present in current environment | VERBATIM | SRC-ENV-001 | /workspace grep | 2026-07-25 | Blocks Prompts 1–3 and 5 |
| EXT-002 | AI Systems | Named systems in scope: Okram AI, SigNEL, Hazel Warden, OSH, SDRWM, Career Intelligence | REFERENCE-ONLY | SRC-META-001 | Prompt suite objective | 2026-07-25 | Names referenced by suite; no source definitions recovered |
| EXT-003 | Prompts and Instructions | Five recovery prompts (extraction, harvester, architecture, gap recovery, handoff) | VERBATIM | SRC-META-001 | User message / `swm-recovery/prompts/` | 2026-07-25 | Methodology artifacts only |

## C. Prompt & Tool Register

| Item ID | Name | Type | Purpose | Input | Output | Dependencies | Source | Completeness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PT-META-001 | Prompt 1 Complete Source Extraction | Prompt | Multi-domain SWM extraction | Authorized sources | Registers A–G | Sources required | SRC-META-001 | Complete (methodology) |
| PT-META-002 | Prompt 2 Prompt/Tool/Workflow Harvester | Prompt | Verbatim prompt archaeology | Authorized sources | Item profiles + 4 lists | Prompt 1 ledgers helpful | SRC-META-001 | Complete (methodology) |
| PT-META-003 | Prompt 3 Architecture Reconstruction | Prompt | Observable architecture only | Authorized sources | Inventory/maps | No hallucination | SRC-META-001 | Complete (methodology) |
| PT-META-004 | Prompt 4 Source Gap Recovery | Prompt | Prioritized source hunt | Ledgers + gaps | Recovery table | Prior registers | SRC-META-001 | Complete (methodology) |
| PT-META-005 | Prompt 5 Rebuild Handoff Compiler | Prompt | Neutral handoff package | Completed registers | Volumes 1–10 | Decisions deferred | SRC-META-001 | Complete (methodology) |

## D. Architecture Register

| Component | Type | Function | Connected Components | Source | Status in Source |
| --- | --- | --- | --- | --- | --- |
| Okram AI | AI agent (referenced) | Unknown — not recovered | Unknown | SRC-META-001 | REFERENCE-ONLY |
| SigNEL | AI/system (referenced) | Unknown — not recovered | Unknown | SRC-META-001 | REFERENCE-ONLY |
| Hazel Warden | AI/system (referenced) | Unknown — not recovered | Unknown | SRC-META-001 | REFERENCE-ONLY |
| OSH | System (referenced) | Unknown — not recovered | Unknown | SRC-META-001 | REFERENCE-ONLY |
| SDRWM | System (referenced) | Unknown — not recovered | Unknown | SRC-META-001 | REFERENCE-ONLY |
| Career Intelligence | Methodology (referenced) | Unknown — not recovered | Unknown | SRC-META-001 | REFERENCE-ONLY |

## E. Conflict Register

| Conflict ID | Item A | Item B | Nature of Conflict | Sources | Resolution |
| --- | --- | --- | --- | --- | --- |
| — | — | — | No conflicts detectable without source corpus | — | DEFERRED — EXTRACTION PHASE |

## F. Gap Register

| Gap ID | Missing/Unclear Item | Evidence | Required Source | Impact |
| --- | --- | --- | --- | --- |
| GAP-001 | Authorized SWM source corpus | Repo/Slack empty; Box/Notion/Linear unauthenticated | User-authorized exports, Drive/Box folders, chat archives, prior GPTs/projects | Blocks all recovery |
| GAP-002 | Core program architecture definitions | Systems named only in prompt suite | Architecture docs, system maps, agent specs | Cannot rebuild Level 1–3 |
| GAP-003 | Product/service/pricing definitions | No product docs located | Offer sheets, packages, client SOWs (redacted as needed) | Blocks business model recovery |
| GAP-004 | Career-Intelligence methodology | No methodology docs located | Signal/skills/scoring specs | Blocks methodology rebuild |
| GAP-005 | Production prompts and tool chains | No prompt libraries located | Prompt libraries, agent configs, tool permission matrices | Blocks Prompt 2 harvest |
| GAP-006 | Workflow / QA / delivery SOPs | No ops docs located | Intake→delivery SOPs, QA checklists | Blocks workflow map |
| GAP-007 | Brand and publication standards | No brand kit located | Logo/type/layout standards | Blocks Volume 7 |
| GAP-008 | Evidence / pilots / corrections | No results corpus located | Pilot notes, testimonials, failure logs | Blocks validation evidence |

## G. Recovery Summary

| Metric | Count |
| --- | --- |
| Authorized SWM business sources processed | 0 |
| Environment probes executed | 5 |
| Extraction ledger items | 3 (meta/gap only) |
| SWM prompts/tools recovered (business) | 0 |
| Architecture components confirmed | 0 |
| Architecture components REFERENCE-ONLY | 6 |
| Conflicts recorded | 0 |
| Gaps opened | 8 |
| Canon status assigned | None |

## Prompt 4 — Prioritized recovery actions

| Priority | Gap ID | Missing Source | Likely Location | Search Terms | Date Range | Substitute Evidence | Recovery Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GAP-001 / GAP-002 | Core SWM architecture + agent specs | Box / Notion / local exports / ChatGPT-Claude projects | `SWM`, `Okram`, `SigNEL`, `Hazel Warden`, `OSH`, `SDRWM`, `architecture`, `agent` | All available history | Partial chat fragments | Authenticate Box/Notion; authorize folder/export dump into `swm-recovery/sources/` |
| 2 | GAP-003 | Business model + product definitions | Offer docs, decks, client packs | `package`, `pricing`, `Career Intelligence`, `service level` | Prefer latest + retain superseded | Marketing copy drafts | Export product/offer materials; do not discard older names |
| 3 | GAP-004 | Methodology specs | Internal methodology docs / prompts | `signal`, `skills mapping`, `scoring`, `employer analysis` | All versions | Worked examples | Recover scoring/signal docs even if incomplete |
| 4 | GAP-005 | Prompt/tool libraries | Custom GPTs, Cursor rules, agent configs | `system prompt`, `tool permission`, `Hazel`, `Okram` | All versions | Invocation command lists | Dump verbatim prompt files; preserve duplicates |
| 5 | GAP-006 | Workflow/QA SOPs | Ops docs, checklists, SOPs | `intake`, `QA`, `delivery`, `versioning` | All versions | Ticket/run logs | Export workflow docs and sample run artifacts |
| 6 | GAP-007 | Brand standards | Brand kits, templates | `logo`, `typography`, `document hierarchy` | Prefer current + prior | Published PDFs | Collect brand kit + sample publications |
| 7 | GAP-008 | Pilots/results | Case notes, testimonials | `pilot`, `testimonial`, `correction`, `failure` | All available | Anonymized summaries | Collect evidence with privacy redaction as needed |

## Next run gate

Do not execute Prompts 2, 3, or 5 for business content until at least one authorized SWM source is supplied.

Recommended next run: `001` — Prompt 1 against the first authorized source bundle placed in `swm-recovery/sources/`.

EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD. NO CANON STATUS ASSIGNED.
