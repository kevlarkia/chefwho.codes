# Systems Health Runbook

Operational checklist for keeping the **entire AI + file ecosystem**
clear, current, and easy for both humans and agents. Scope is wider than
SWM: Cursor, Claude, Codex/TMI, Notion/CLOUT, Linear, Drive, and local
disk.

Governing altitude: Systems Architect Mode (Personal Cognitive Charter
v1.1). Prefer load-bearing design over decorative reorganization.

## Why this exists

Agents move fastest when:

1. Repo instruction files match reality.
2. Durable artifacts are routed through CLOUT (not stranded in chat).
3. Active work has one obvious home; archives are frozen, not endlessly
   reorganized.
4. Draft / stale PR and instruction branches are closed or merged.

## Canonical surfaces (do not invent duplicates)

| Surface | Location | Purpose |
| --- | --- | --- |
| Cognitive governance | Notion — Personal Cognitive Charter v1.1 | Tone, reasoning, anti-fabrication |
| Life archive routing | Notion — CLOUT Intake + Routing Controls | Capture → route → archive |
| Drive filing | Notion — Fernandez Filing System v1.0 | Google Drive top-level structure |
| This site + SWM toolkit | `AGENTS.md`, `README.md`, `swm-recovery/` | Repo-local agent pass-through |
| TMI / Codex | `Terra-Machina-Imperium/codex`, UC7.5 `AGENTS.md` / `CLAUDE.md` | Mythos + product AI guides |

If a new instruction file is tempting, first ask: which row above does
it update?

## Two-hour maintenance block

Use this sequence. Stop when time is up; leave unfinished items as
CLOUT intake + Linear issues.

### Block A — AI instruction truth (≈40 min)

1. Open each active repo you touched this month.
2. Diff `AGENTS.md` / `CLAUDE.md` / Cursor rules against README + actual
   stack (package manager, CI, env vars, major folders).
3. Fix drift in-repo. Do not leave corrected text only in a chat.
4. Close or merge abandoned draft PRs that only update instructions.
5. Confirm Cursor plugins/skills still resolve (paths match files).

**Pass test:** A cold-start agent can answer "what is this repo?" and
"how do I lint/build?" without inventing bootstrap status.

### Block B — Capture & routing (≈30 min)

1. Sweep recent chat threads for artifacts worth preserving.
2. Create CLOUT Universal Intake Queue rows first (Status = Captured or
   Routed). Do not create orphan Notion pages.
3. Route known destinations; mark ambiguous items Needs Review.
4. Cancel Linear onboarding stubs if they are not real work; replace
   with living systems-health issues.

**Pass test:** Nothing important from today's sessions exists only inside
a chat transcript.

### Block C — Disk & Drive tidy (≈40 min)

Local Mac (operator-only; cloud agents cannot see `/Users/...`):

1. Inbox → Active → Archive. Do not deep-organize Unsorted-Legacy in
   this block.
2. Confirm Fernandez top-level exists: `00_Inbox`, `01_Active`,
   `02_Reference`, `Archive`.
3. For SWM brand recovery: run
   `swm-recovery/sources/brand-assets/INGEST_FROM_MAC.sh` when sources
   are reachable, then record a new run under `swm-recovery/runs/`.
4. Prefer search over creating new folder taxonomies mid-session.

Drive:

1. Process `00_Inbox` in batch.
2. Move completed Active matters toward year Archive only when truly
   inactive.

**Pass test:** You can find today's working set in under 30 seconds
without opening random Desktop dumps.

### Block D — Close the loop (≈10 min)

1. Update this runbook if a step proved wrong or missing.
2. Log the session in CLOUT (Domain: AI / Prompting or Website /
   Publishing as appropriate).
3. Note next maintenance date (weekly light sweep; deeper monthly).

## Recurring cadence

| Cadence | Focus |
| --- | --- |
| Weekly | CLOUT inbox/triage; Drive inbox; stale chat captures |
| Monthly | AGENTS/CLAUDE truth pass across active repos; draft PR purge |
| Quarterly | Filing System vs actual disk; plugin/skill inventory |
| Annually | Cognitive Charter review (or after major life-structure change) |

## Failure modes to watch

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Agent says "bootstrap / no package.json" on a live app | Stale `AGENTS.md` | Update in same PR as reality change |
| Good work vanishes after a session | No CLOUT intake | Intake before session end |
| Duplicate instruction docs | Parallel CLAUDE/AGENTS/Notion copies | Pick one canonical surface; link others |
| Endless folder redesign | Fatigue reorganization | Archive aggressively; search > browse |
| SWM recovery stuck | Mac paths not ingested | Operator ingest script + new run note |

## Out of scope for this runbook

- Legal/medical/crisis private materials (stay out of public remotes)
- Full Unsorted-Legacy archaeology in a two-hour block
- Inventing a second filing ontology beside Fernandez + CLOUT

## Related links

- `AGENTS.md` — this repository's agent contract
- `swm-recovery/README.md` — SWM extraction operating mode
- Notion: Personal Cognitive Charter v1.1
- Notion: CLOUT Intake and Routing Controls
- Notion: Fernandez Filing System v1.0
