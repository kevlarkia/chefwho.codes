# Rose Rocket Engine

Automated AI newsletter scaffold with:

- Hacker News AI scraping
- Gemini-powered draft assembly
- M/W/F edition routing
- feature cooldown rotation
- banned-word content filter (pre-final output)
- Gmail draft creation via Gmail API

## Files

- `rose_rocket_engine.py` — main orchestration engine
- `ai_news_scraper.py` — Hacker News scraper filtered for AI keywords
- `gmail_draft_creator.py` — Gmail draft creation module
- `feature_cooldowns.json` — persisted legacy feature rotation state
- `fixtures/mock_stories.json` — deterministic local stories for offline mode
- `requirements.txt` — pinned Python dependencies
- `requirements-dev.txt` — pytest + ruff for local CI parity
- `tests/` — schedule gate and mode-path unit tests
- `.github/workflows/ci.yml` — lint + pytest + offline smoke
- `CHANGELOG.md` — version history
- `docs/RELEASE_NOTES_v0.1.0.md` — tag prep notes (tag not created yet)

## Requirements

- Python 3.10+
- A Google Cloud project with Gmail API enabled
- OAuth client credentials downloaded as `credentials.json`
- Gemini API key

## Environment & credentials

Set environment variable:

```bash
export GEMINI_API_KEY="your_key_here"
```

Place your Gmail OAuth credentials file in project root:

- `credentials.json`

On first run, OAuth flow stores `token.json` locally.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Optional for local CI parity:
pip install -r requirements-dev.txt
```

## Local CI parity

```bash
ruff check .
pytest -q
OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python rose_rocket_engine.py
```

## Run

```bash
python rose_rocket_engine.py
```

If run on a non-publish day (not Monday/Wednesday/Friday), the engine exits with a schedule error by design.

## Environment variables

- `GEMINI_API_KEY` (required in normal and DRY_RUN modes): Gemini API key.
- `FORCE_EDITION` (optional): If truthy (`1`, `true`, `yes`, `on`), bypasses Monday/Wednesday/Friday schedule gate.
- `DRY_RUN` (optional): If truthy (`1`, `true`, `yes`, `on`), skips Gmail draft creation but still calls Gemini.
- `OFFLINE_DRY_RUN` (optional): If truthy (`1`, `true`, `yes`, `on`), skips both Gemini and Gmail and uses local fixtures.

## Testing modes

### 1) Production path (live APIs)

```bash
unset DRY_RUN
unset OFFLINE_DRY_RUN
export FORCE_EDITION=1
python rose_rocket_engine.py
```

Expected:

- Gemini is called.
- Gmail draft is created successfully.
- Console prints draft ID.

### 2) DRY_RUN path (live Gemini, no Gmail)

```bash
export DRY_RUN=1
unset OFFLINE_DRY_RUN
export FORCE_EDITION=1
python rose_rocket_engine.py
```

Expected:

- Gemini is called.
- Gmail draft is skipped.
- Console prints `DRY_RUN enabled: skipping Gmail draft creation.`
- File written to `output/newsletter-<local-date>.md`.

### 3) OFFLINE_DRY_RUN path (no external API calls)

```bash
unset DRY_RUN
export OFFLINE_DRY_RUN=1
export FORCE_EDITION=1
python rose_rocket_engine.py
```

Expected:

- Gemini is skipped.
- Gmail draft is skipped.
- Local fixture stories are loaded from `fixtures/mock_stories.json`.
- Console prints `OFFLINE_DRY_RUN enabled: skipping Gemini and Gmail API calls.`
- File written to `output/newsletter-<local-date>.md`.

## Offline fixture format

`fixtures/mock_stories.json` supports either:

- an object with `stories` key:

```json
{
  "stories": [
    {"title": "Story A", "url": "https://example.com/a"},
    {"title": "Story B", "url": "https://example.com/b"}
  ]
}
```

- or a direct list:

```json
[
  {"title": "Story A", "url": "https://example.com/a"},
  {"title": "Story B", "url": "https://example.com/b"}
]
```

If fixture parsing fails or the file is empty, the engine falls back to built-in mock stories.

## Key constraints implemented

- Output is enforced under **30,000 characters**.
- A **banned-word content filter** runs before final output.
- Publishing route supports **Monday/Wednesday/Friday** with distinct edition types.
