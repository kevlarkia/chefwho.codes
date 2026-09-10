import json

import pytest

from forensic_archive.llm import (
    AnthropicLLMClient,
    DummyLLMClient,
    OpenAILLMClient,
    VertexLLMClient,
    client_from_env,
)
from forensic_archive.prompts import (
    ArchiveProfile,
    render_primary_prompt,
    render_secondary_prompt,
)


def test_client_from_env_defaults_to_dummy(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FORENSIC_LLM_PROVIDER", raising=False)
    client = client_from_env()
    assert client.name == "dummy"


def test_client_from_env_requires_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORENSIC_LLM_PROVIDER", "anthropic")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        client_from_env()


def test_anthropic_wrapper_posts_messages(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    def fake_post(url, headers, payload):
        captured["url"] = url
        captured["headers"] = headers
        captured["payload"] = payload
        return {"content": [{"type": "text", "text": "ok"}]}

    monkeypatch.setattr("forensic_archive.llm.post_json", fake_post)
    client = AnthropicLLMClient(api_key="test-key", model="claude-test")
    assert client.complete("hello", system="sys") == "ok"
    assert captured["url"].endswith("/v1/messages")
    assert captured["headers"]["x-api-key"] == "test-key"
    assert captured["payload"]["system"] == "sys"


def test_openai_and_vertex_wrappers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "forensic_archive.llm.post_json",
        lambda url, headers, payload: {
            "choices": [{"message": {"content": "from-openai"}}],
            "candidates": [{"content": {"parts": [{"text": "from-vertex"}]}}],
        },
    )
    assert OpenAILLMClient("k", "gpt-test").complete("q") == "from-openai"
    vertex = VertexLLMClient("proj", "us-central1", "gemini-test", "token")
    assert vertex.complete("q") == "from-vertex"


def test_dummy_secondary_emits_exclusions_json() -> None:
    profile = ArchiveProfile(id="generic", addendum="")
    source = "A complete sentence about the reading room log.\n\nTBD later."
    client = DummyLLMClient()
    primary = client.complete(render_primary_prompt(source, profile).text)
    secondary = client.complete(render_secondary_prompt(source, primary, profile).text)
    payload = json.loads(secondary.split("```json")[-1].split("```")[0])
    assert "exclusions" in payload
    assert any(item["rule"] == "placeholder" for item in payload["exclusions"])
