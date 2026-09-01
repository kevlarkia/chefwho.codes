# Session Save State (closing prompt)

Copy everything below the line into the active chat when ending a session.

---

I am ending this session. Generate a **Save State** checkpoint from **this conversation only**.

**Hard rules:**
- Evidence-bound only: include nothing not stated or produced here.
- If unknown or not discussed, write `not discussed` — do not invent.
- Prefer paths, branch names, PR/issue IDs, and file names over vague summary.
- Tag each decision `HELD` (locked) or `TENTATIVE` (still open).
- Keep the whole document under ~40 lines.
- Provide **only** the Markdown below (no preamble).

### Metadata
- **Date:** [ISO date]
- **Project / repo:** [name or path]
- **Branch:** [branch or `n/a`]
- **Key paths touched:** [comma-separated paths, or `none`]
- **PR / issue IDs:** [ids or `none`]
- **File this to:** [CLOUT / Linear / path / `operator will file`]

### 1. Project Overview
[1–2 sentences: core project, role, overarching goal]

### 2. Session Achievements
* [Only completed/resolved/built items evidenced in this session]

### 3. Current State & Key Decisions
* [`HELD` or `TENTATIVE`] [decision or structural choice]
* [Brief code/doc state notes with paths if applicable]

### 4. Open Threads & Roadblocks
* [Bugs, unresolved questions, pending decisions — or `none`]

### 5. Next Immediate Steps
* [1–3 specific actionable resume tasks, ordered]
