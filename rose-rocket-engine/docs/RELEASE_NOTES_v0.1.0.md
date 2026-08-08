# Rose Rocket Engine v0.1.0 — Release Notes (prep)

Status: **prepared, not tagged yet**.
Cut the `v0.1.0` git tag only after CI is green on `main`.

## Highlights

- End-to-end newsletter scaffold: scrape → generate → (optional) Gmail draft
- Monday / Wednesday / Friday edition routing using local OS time
- Developer-friendly run modes:
  - Production (Gemini + Gmail)
  - `DRY_RUN=1` (Gemini + local artifact, no Gmail)
  - `OFFLINE_DRY_RUN=1` (fixtures only, zero external API calls)
- `FORCE_EDITION=1` bypass for schedule-gated testing
- CI workflow with lint, unit tests, and offline smoke run

## Install

```bash
git clone https://github.com/kevlarkia/rose-rocket-engine.git
cd rose-rocket-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optional, for local CI parity
```

## Quick validation

```bash
# Offline smoke (no API keys required)
export OFFLINE_DRY_RUN=1
export FORCE_EDITION=1
python rose_rocket_engine.py

# Unit tests
pytest -q
```

## Tag checklist (manual)

1. Confirm CI is green on `main`
2. Review `CHANGELOG.md` `[0.1.0]` section
3. Create annotated tag:

   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

4. Publish GitHub Release from the tag using these notes
