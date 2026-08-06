# Mirror note for chefwho.codes

This directory is a working mirror of
[kevlarkia/rose-rocket-engine](https://github.com/kevlarkia/rose-rocket-engine)
so the CI / pytest / changelog batch can be reviewed and transferred.

The Cursor cloud agent for this workspace can push to `chefwho.codes` but
does **not** currently have write access to `rose-rocket-engine`. To land
these changes upstream:

```bash
# From a machine with write access to kevlarkia/rose-rocket-engine:
git clone https://github.com/kevlarkia/rose-rocket-engine.git
cd rose-rocket-engine
git checkout -b cursor/ci-pytest-changelog

# Copy new/updated files from this mirror:
cp -R ../chefwho.codes/rose-rocket-engine/.github .
cp -R ../chefwho.codes/rose-rocket-engine/tests .
cp ../chefwho.codes/rose-rocket-engine/requirements-dev.txt .
cp ../chefwho.codes/rose-rocket-engine/CHANGELOG.md .
cp ../chefwho.codes/rose-rocket-engine/docs/RELEASE_NOTES_v0.1.0.md docs/
cp ../chefwho.codes/rose-rocket-engine/.env.example .
cp ../chefwho.codes/rose-rocket-engine/.gitignore .
cp ../chefwho.codes/rose-rocket-engine/README.md .

git add .
git commit -m "Add CI, pytest suite, and v0.1.0 changelog prep"
git push -u origin cursor/ci-pytest-changelog
```

Do not create the `v0.1.0` tag until CI is green on `main`.
