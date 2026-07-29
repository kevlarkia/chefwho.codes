---
name: swm-recovery-first
description: Run the SWM Recovery-First extraction suite (no canon gate). Use when recovering Smart Workforce Movement / Okram / SigNEL / Hazel / OSH / SDRWM material from authorized sources.
---

# SWM recovery-first extraction

## Trigger

User asks to recover, extract, harvest, or rebuild SWM / Okram / SigNEL /
Hazel Warden / OSH / SDRWM / Career Intelligence material.

## Workflow

1. Confirm authorized sources exist. If none, run Prompt 4 gap assessment only.
2. Execute Prompt 1 (`/swm-extract`) and emit registers A–G.
3. Execute Prompt 2 for prompts/tools/workflows.
4. Execute Prompt 3 for observable architecture only.
5. Execute Prompt 4 to prioritize missing sources.
6. Execute Prompt 5 only when registers exist; never assign canon.

## Output contract

- Begin Prompt 1 with:
  `SWM RECOVERY-FIRST EXTRACTION INITIATED — CANON GATE DISABLED`
- End Prompt 5 with:
  `EXTRACTION COMPLETE — MATERIAL PRESERVED FOR HUMAN-LED REBUILD.`
  `NO CANON STATUS ASSIGNED.`
- Use structured tables; one evidence label per item.
- Conflict resolution values must remain deferred.

## Source of truth

Prefer the versioned suite under `swm-recovery/prompts/` when present in the
workspace.
