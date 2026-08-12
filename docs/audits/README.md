# Audits & pressure tests

Thin first-wave checks for this repo and the broader Systems Health
surface. Canonical runbook: [`docs/SYSTEMS_HEALTH.md`](../SYSTEMS_HEALTH.md).
Do not invent a parallel filing ontology — file durable results to CLOUT
or Linear after the log exists.

## Shared contract

Every run fills [`AUDIT_LOG_TEMPLATE.md`](AUDIT_LOG_TEMPLATE.md) and
stores the filled note under [`runs/`](runs/).

| Lane | Tool | When |
| --- | --- | --- |
| `repo-pressure` | `npm run pressure-test` | Monthly; after AGENTS/docs/CI changes |
| `systems-health` | [`docs/prompts/systems-health-audit.md`](../prompts/systems-health-audit.md) | Weekly light; monthly deep |
| `swm-forensic` | [`swm-recovery/prompts/06-forensic-integrity-audit.md`](../../swm-recovery/prompts/06-forensic-integrity-audit.md) | Before SWM handoff; after major register runs |

## Cadence

| Cadence | Lanes |
| --- | --- |
| Weekly | systems-health (light — Blocks B + D) |
| Monthly | repo-pressure + systems-health (full A–D) |
| Before SWM handoff | swm-forensic |

## Runs folder

Filled logs: `docs/audits/runs/AUDIT-YYYYMMDD-NN-<lane>.md`

SWM-scoped forensic audits may instead land as a run note under
`swm-recovery/runs/` and link back to an audit id in the log header.
