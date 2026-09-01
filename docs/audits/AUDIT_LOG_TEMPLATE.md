# Audit Log — [AUDIT-ID]

Copy this template for every pressure test or audit. Use one log per
lane run. Prefer evidence paths over narrative.

| Field | Value |
| --- | --- |
| Audit ID | AUDIT-YYYYMMDD-NN (e.g. AUDIT-20260812-01) |
| Date | ISO date |
| Lane | `repo-pressure` \| `systems-health` \| `swm-forensic` |
| Operator | name or agent id |
| Verdict | `PASS` \| `FAIL` \| `PARTIAL` |
| File to | CLOUT / Linear / `docs/audits/runs/` / `swm-recovery/runs/` |

## Findings

| ID | Severity | Finding | Evidence path | Fix |
| --- | --- | --- | --- | --- |
| F-001 | high \| medium \| low \| info | | | |

## Notes

- Mark unavailable surfaces `not observable` — do not invent state.
- `PARTIAL` = some checks passed, blockers remain; list them in Findings.
- Save filled logs under `docs/audits/runs/` (or `swm-recovery/runs/` for
  Lane 3 when the audit is SWM-run scoped).
