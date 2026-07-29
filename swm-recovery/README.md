# SWM Extraction Prompt Suite

Recovery-First Edition · No Canon Gate

Operational toolkit for Smart Workforce Movement (SWM) system archaeology
and legacy data recovery. Optimized for AI processing: token-efficient
prompts, strict table schemas, and hard boundaries against hallucination.

## Operating mode

This is an **extraction** operation, not verification, approval,
canonization, or publication.

- Extract first; do not reject material for conflict, age, or governance labels.
- Canon status is irrelevant during recovery.
- Do not resolve disagreements or invent missing content.
- Process only supplied or specifically authorized sources.

## Prompt order

| Step | Prompt | Purpose |
| --- | --- | --- |
| 1 | [Complete Source Extraction Engine](prompts/01-complete-source-extraction.md) | Full multi-domain extraction ledgers |
| 2 | [Prompt, Tool, and Workflow Harvester](prompts/02-prompt-tool-workflow-harvester.md) | Verbatim prompt/tool recovery |
| 3 | [Program Architecture Reconstruction](prompts/03-program-architecture-reconstruction.md) | Observable architecture only |
| 4 | [Source Gap Recovery](prompts/04-source-gap-recovery.md) | Prioritized missing-source hunt |
| 5 | [Rebuild Handoff Compiler](prompts/05-rebuild-handoff-compiler.md) | Neutral handoff package |

## How to run

1. Authorize source materials (exports, docs, chats, files).
2. Paste Prompt 1 with the authorized sources attached or linked.
3. Feed Prompt 1 outputs into Prompts 2–4 as needed.
4. Run Prompt 5 only after registers exist.
5. Store each run under `runs/` using the next numeric prefix.

## Evidence labels

Apply exactly one label per extracted item:

`VERBATIM` · `SOURCE-SUMMARY` · `RECONSTRUCTED` · `INFERRED` ·
`REFERENCE-ONLY` · `CONFLICTING` · `INCOMPLETE` · `UNCERTAIN` ·
`DUPLICATE` · `SUPERSEDED-CLAIM`

## Register templates

Empty table scaffolds live in [`templates/`](templates/).

## Cursor plugin

AI-invocable commands live in [`cursor-plugin/`](cursor-plugin/).

Install locally:

```bash
mkdir -p ~/.cursor/plugins/local
cp -a swm-recovery/cursor-plugin ~/.cursor/plugins/local/swm-extraction
```

Commands: `/swm-extract`, `/swm-harvest-prompts`,
`/swm-reconstruct-architecture`, `/swm-gap-recovery`, `/swm-handoff`.

## Current recovery status

| Run | Focus | Status |
| --- | --- | --- |
| [`000`](runs/000-bootstrap-gap-assessment.md) | Bootstrap environment probe | Complete — no sources then |
| [`001`](runs/001-brand-assets-source-authorization.md) | Brand Assets (9 Mac paths) | Authorized; **pending ingest** |

Brand source index:
[`sources/brand-assets/AUTHORIZED_SOURCE_INDEX.md`](sources/brand-assets/AUTHORIZED_SOURCE_INDEX.md)

## Scope boundary

Isolate SWM business material from legal, medical, crisis, or private
relationship material. Do not fabricate missing prompts, architecture, or
business facts.
