"""Minimal tests for schedule gating and dry-run mode paths."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import rose_rocket_engine as engine


@pytest.fixture(autouse=True)
def _isolate_cooldown_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    cooldown = tmp_path / "feature_cooldowns.json"
    cooldown.write_text('{"last_used": {}}', encoding="utf-8")
    monkeypatch.setattr(engine, "COOLDOWN_FILE", cooldown)
    yield


@pytest.fixture(autouse=True)
def _clear_mode_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        engine.FORCE_EDITION_ENV,
        engine.DRY_RUN_ENV,
        engine.OFFLINE_DRY_RUN_ENV,
        "GEMINI_API_KEY",
    ):
        monkeypatch.delenv(name, raising=False)


def test_force_edition_bypasses_schedule(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(engine.FORCE_EDITION_ENV, "1")
    assert engine._edition_for_today() == "Forced Test Edition"


@pytest.mark.parametrize(
    ("when", "edition"),
    [
        (datetime(2026, 8, 3, 12, 0, 0), "Monday Market Radar"),  # Monday
        (datetime(2026, 8, 5, 18, 0, 0), "Wednesday Builder Brief"),  # Wednesday
        (datetime(2026, 8, 7, 9, 0, 0), "Friday Frontier Signals"),  # Friday
    ],
)
def test_edition_routing_on_publish_days(
    monkeypatch: pytest.MonkeyPatch, when: datetime, edition: str
) -> None:
    monkeypatch.setattr(engine, "_now_local", lambda: when)
    assert engine._edition_for_today() == edition


@pytest.mark.parametrize(
    "when",
    [
        datetime(2026, 8, 4, 12, 0, 0),  # Tuesday
        datetime(2026, 8, 6, 12, 0, 0),  # Thursday
        datetime(2026, 8, 8, 12, 0, 0),  # Saturday
        datetime(2026, 8, 9, 12, 0, 0),  # Sunday
    ],
)
def test_edition_raises_on_non_publish_days(
    monkeypatch: pytest.MonkeyPatch, when: datetime
) -> None:
    monkeypatch.setattr(engine, "_now_local", lambda: when)
    with pytest.raises(RuntimeError, match="Monday/Wednesday/Friday"):
        engine._edition_for_today()


def test_content_filter_blocks_banned_words() -> None:
    with pytest.raises(ValueError, match="banned words"):
        engine._validate_content_filter("This is pure clickbait nonsense.")


def test_content_filter_allows_clean_text() -> None:
    engine._validate_content_filter("Operator-focused brief with clear takeaways.")


def test_offline_dry_run_skips_gemini_and_gmail(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv(engine.OFFLINE_DRY_RUN_ENV, "1")
    monkeypatch.setenv(engine.FORCE_EDITION_ENV, "1")
    monkeypatch.setattr(engine, "OUTPUT_DIR", tmp_path / "output")
    monkeypatch.setattr(
        engine,
        "MOCK_STORIES_PATH",
        Path(__file__).resolve().parents[1] / "fixtures" / "mock_stories.json",
    )

    with (
        patch("rose_rocket_engine.fetch_hn_ai_stories") as mock_fetch,
        patch("rose_rocket_engine.create_gmail_draft") as mock_gmail,
        patch.object(engine.genai, "GenerativeModel") as mock_model,
    ):
        engine.run()

    mock_fetch.assert_not_called()
    mock_gmail.assert_not_called()
    mock_model.assert_not_called()

    out = capsys.readouterr().out
    assert "OFFLINE_DRY_RUN enabled" in out
    assert "skipping Gemini and Gmail" in out

    artifacts = list((tmp_path / "output").glob("newsletter-*.md"))
    assert len(artifacts) == 1
    assert "Forced Test Edition" in artifacts[0].read_text(encoding="utf-8")


def test_dry_run_skips_gmail_but_uses_gemini(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv(engine.DRY_RUN_ENV, "1")
    monkeypatch.setenv(engine.FORCE_EDITION_ENV, "1")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(engine, "OUTPUT_DIR", tmp_path / "output")

    mock_response = MagicMock()
    mock_response.text = "Clean dry-run newsletter body without banned terms."
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with (
        patch(
            "rose_rocket_engine.fetch_hn_ai_stories",
            return_value=[{"title": "AI tooling update", "url": "https://example.com/ai"}],
        ),
        patch("rose_rocket_engine.create_gmail_draft") as mock_gmail,
        patch.object(engine.genai, "configure"),
        patch.object(engine.genai, "GenerativeModel", return_value=mock_model),
    ):
        engine.run()

    mock_gmail.assert_not_called()
    mock_model.generate_content.assert_called_once()

    out = capsys.readouterr().out
    assert "DRY_RUN enabled: skipping Gmail draft creation." in out
    artifacts = list((tmp_path / "output").glob("newsletter-*.md"))
    assert len(artifacts) == 1


def test_truthy_env_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SAMPLE_FLAG", "yes")
    assert engine._is_truthy_env("SAMPLE_FLAG") is True
    monkeypatch.setenv("SAMPLE_FLAG", "0")
    assert engine._is_truthy_env("SAMPLE_FLAG") is False
