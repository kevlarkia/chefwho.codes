---
name: swm-recovery-first
description: Run the SWM Recovery-First extraction suite (no canon gate). Use when recovering Smart Workforce Movement / Okram / SigNEL / Hazel / OSH / SDRWM material from authorized sources.
---

# SWM recovery-first extraction

## Trigger

User asks to recover, extract, harvest, or rebuild SWM / Okram / SigNEL /
Hazel Warden / OSH / SDRWM / Career Intelligence material.

## NON-FABRICATION RULE

If an item cannot be extracted, summarized, or reconstructed from supplied
evidence, do not invent it. Primary labels only: VERBATIM · SOURCE-SUMMARY ·
RECONSTRUCTED · INFERRED · REFERENCE-ONLY. RECONSTRUCTED/INFERRED must cite
`SWM-EX-######` fragments.

## Workflow

1. Confirm authorized sources exist. If none, run Prompt 4 gap assessment only.
2. Execute Prompt 1 (`/swm-extract`) and emit registers A–I including
   Relationship and Timeline registers.
3. Execute Prompt 2 for prompts/tools/workflows + Dependency Register;
   preserve exact formatting.
4. Execute Prompt 3 for observable architecture only; apply formal confidence
   rules; emit Relationship + Timeline.
5. Execute Prompt 4 to prioritize missing sources (Gap Confidence required).
6. Execute Prompt 5 only when registers exist; never assign canon; state
   Rebuild Priority 1–6.

## Output contract

- Begin Prompt 1 with:
  `SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED`
- End Prompt 5 with:
  `EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD.`
  `NO CANON STATUS ASSIGNED.`
- Use structured tables; permanent IDs `SWM-EX-######`; Evidence Type field.
- Conflict resolution values must remain deferred.

## Source of truth

Prefer the versioned suite under `swm-recovery/prompts/` when present in the
workspace.
