# Mirror note for chefwho.codes

This directory is a working mirror of
[kevlarkia/rose-rocket-engine](https://github.com/kevlarkia/rose-rocket-engine)
so the CI / pytest / changelog batch can be reviewed and transferred.

The Cursor cloud agent for this workspace can push to `chefwho.codes` but
does **not** currently have write access to `rose-rocket-engine`.

## One-command apply (preferred)

From a machine with write access to `kevlarkia/rose-rocket-engine`:

```bash
git clone https://github.com/kevlarkia/rose-rocket-engine.git
cd rose-rocket-engine
git checkout -b cursor/ci-pytest-changelog

# Path may be a sibling checkout of chefwho.codes, or clone that PR branch:
#   git clone -b cursor/rose-rocket-ci-pytest-changelog-0530 \
#     https://github.com/kevlarkia/chefwho.codes.git ../chefwho.codes
git apply ../chefwho.codes/rose-rocket-engine/patches/0001-add-ci-pytest-changelog.patch

git add .
git commit -m "Add CI, pytest suite, and v0.1.0 changelog prep"
git push -u origin cursor/ci-pytest-changelog
```

The patch includes:

- `.github/workflows/ci.yml`
- `tests/` + `requirements-dev.txt` + `pyproject.toml`
- `CHANGELOG.md` + `docs/RELEASE_NOTES_v0.1.0.md`
- Hardening for `.gitignore`, `.env.example`, README, and ruff-clean typing

It does **not** include this `UPSTREAM_APPLY.md` file (chefwho.codes-only note).

## Scripted sync (alternative)

```bash
../chefwho.codes/rose-rocket-engine/scripts/sync-to-upstream.sh /path/to/rose-rocket-engine
```

## Verify before merge

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest -q
OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python rose_rocket_engine.py
```

Do not create the `v0.1.0` tag until CI is green on `main`.
