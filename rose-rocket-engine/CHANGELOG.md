# Changelog

All notable changes to Rose Rocket Engine are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Create git tag `v0.1.0` after CI is green on `main`
- Expand test coverage beyond schedule/mode guards

## [0.1.0] - 2026-08-06

### Added

- Core newsletter orchestration (`rose_rocket_engine.py`)
- Hacker News AI scraper (`ai_news_scraper.py`)
- Gmail draft creator (`gmail_draft_creator.py`)
- Feature cooldown persistence (`feature_cooldowns.json`)
- `FORCE_EDITION` env override for out-of-schedule test runs
- Local-time edition routing (OS wall clock)
- `DRY_RUN` mode (Gemini on, Gmail skipped, local markdown artifact)
- `OFFLINE_DRY_RUN` mode (no Gemini/Gmail; fixture-driven output)
- Sample offline fixtures (`fixtures/mock_stories.json`)
- Builder implementation checklist (`docs/builder-implementation-checklist.md`)
- GitHub Actions CI (lint + pytest + offline smoke)
- Minimal pytest suite for schedule gating and mode paths
- Dev dependencies (`requirements-dev.txt`: pytest, ruff)

### Security

- `.gitignore` covers `.env`, OAuth tokens, virtualenvs, and `output/` artifacts
- `.env.example` documents required and optional environment variables

[Unreleased]: https://github.com/kevlarkia/rose-rocket-engine/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/kevlarkia/rose-rocket-engine/releases/tag/v0.1.0
