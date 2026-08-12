# Systems Health audit (operator prompt)

Copy everything below the line into chat, or fill the checklist manually.
Output a filled [`docs/audits/AUDIT_LOG_TEMPLATE.md`](../audits/AUDIT_LOG_TEMPLATE.md)
with lane `systems-health`.

Canonical runbook: [`docs/SYSTEMS_HEALTH.md`](../SYSTEMS_HEALTH.md).

---

Run a **Systems Health audit** against `docs/SYSTEMS_HEALTH.md` Blocks A–D.

**Hard rules:**
- Do not invent Notion/CLOUT, Drive, Linear, or Mac disk state.
- If a surface is unavailable, mark the step `SKIP` / `not observable` and say why.
- Evidence-bound only. Prefer paths, issue IDs, and timestamps.
- Provide a filled Audit Log (lane `systems-health`) as the primary output.
- Verdict: `PASS` only if no FAIL remains; otherwise `PARTIAL` or `FAIL`.

## Checklist

For each step: `PASS` | `FAIL` | `SKIP` + one-line evidence.

### Block A — AI instruction truth
1. Active repos touched this month identified (or `not observable`)
2. `AGENTS.md` / rules match README + stack (package manager, CI, folders)
3. Drift fixed in-repo (not chat-only) — or listed as open finding
4. Abandoned instruction-only draft PRs closed/merged — or `not observable`
5. Cursor plugins/skills paths resolve — or `not observable`

### Block B — Capture & routing
1. Recent chats swept for durable artifacts
2. CLOUT intake rows created (no orphan Notion pages) — or `not observable`
3. Known destinations routed; ambiguous marked Needs Review — or `not observable`
4. Stub Linear issues cancelled / replaced with living work — or `not observable`

### Block C — Disk & Drive tidy
1. Local Inbox → Active → Archive progress — or `not observable` (cloud agents)
2. Fernandez top-level present — or `not observable`
3. SWM ingest script status if brand sources changed — or `n/a`
4. Drive `00_Inbox` batch processed — or `not observable`

### Block D — Close the loop
1. Systems Health runbook updated if a step was wrong/missing — or `n/a`
2. Session logged in CLOUT — or `not observable`
3. Next maintenance date noted

## Cadence note

- **Weekly light:** Blocks B + D only is acceptable; mark A/C `SKIP` with reason.
- **Monthly deep:** all four blocks.
