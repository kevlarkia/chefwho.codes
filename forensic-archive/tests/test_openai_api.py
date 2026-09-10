"""Official OpenAI API overview contract for the forensic-archive client."""

from __future__ import annotations

import json
from email.message import Message
from io import BytesIO
from urllib.error import HTTPError
from urllib.request import Request

import pytest

from forensic_archive.errors import LLMHttpError
from forensic_archive.llm import (
    CLIENT_REQUEST_ID_MAX,
    OPENAI_CHAT_URL,
    OPENAI_RESPONSES_URL,
    OpenAILLMClient,
    assert_header_budget,
    client_from_env,
    extract_openai_text,
    request_json,
    validate_client_request_id,
)
from forensic_archive.pipeline import ForensicArchiver


def _message_headers(pairs: dict[str, str]) -> Message:
    headers = Message()
    for key, value in pairs.items():
        headers[key] = value
    return headers


class FakeResponse:
    def __init__(self, payload: dict, headers: dict[str, str], status: int = 200) -> None:
        self._payload = json.dumps(payload).encode("utf-8")
        self.headers = _message_headers(headers)
        self.status = status

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *args: object) -> bool:
        return False


def test_openai_defaults_to_responses_surface(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    def fake_request(url, headers, payload, client_request_id=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["payload"] = payload
        captured["client_request_id"] = client_request_id
        return _ok_result(client_request_id=client_request_id)

    monkeypatch.setattr("forensic_archive.llm.request_json", fake_request)
    client = OpenAILLMClient("sk-test", "gpt-4.1")
    text = client.complete("archive this", system="Keep exclusions as JSON.")
    assert text == "from-responses"
    assert captured["url"] == OPENAI_RESPONSES_URL
    assert captured["payload"]["model"] == "gpt-4.1"
    assert captured["payload"]["input"] == "archive this"
    assert captured["payload"]["instructions"] == "Keep exclusions as JSON."
    assert captured["payload"]["store"] is False
    assert captured["headers"]["Authorization"] == "Bearer sk-test"
    assert captured["headers"]["Content-Type"] == "application/json"
    assert captured["headers"]["X-Client-Request-Id"] == captured["client_request_id"]
    assert "OpenAI-Organization" not in captured["headers"]
    assert client.last_trace.provider_request_id == "req_test"
    assert client.last_trace.surface == "responses"


def test_openai_sends_org_project_and_client_request_id(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    def fake_request(url, headers, payload, client_request_id=None):
        captured["headers"] = headers
        captured["client_request_id"] = client_request_id
        return _ok_result(
            headers={
                "x-request-id": "req_abc",
                "openai-organization": "org-live",
                "openai-processing-ms": "42",
                "openai-version": "2020-10-01",
                "x-ratelimit-remaining-requests": "9",
                "x-ratelimit-remaining-tokens": "1000",
            },
            body={"id": "resp_1", "output_text": "ok"},
            client_request_id=client_request_id,
        )

    monkeypatch.setattr("forensic_archive.llm.request_json", fake_request)
    client = OpenAILLMClient(
        "sk-test",
        "gpt-4.1",
        organization="org-from-env",
        project="proj_123",
    )
    client.complete("q", client_request_id="run-1:primary")
    assert captured["headers"]["OpenAI-Organization"] == "org-from-env"
    assert captured["headers"]["OpenAI-Project"] == "proj_123"
    assert captured["headers"]["X-Client-Request-Id"] == "run-1:primary"
    assert captured["client_request_id"] == "run-1:primary"
    assert client.last_trace.provider_request_id == "req_abc"
    assert client.last_trace.organization == "org-live"
    assert client.last_trace.processing_ms == "42"
    assert client.last_trace.api_version == "2020-10-01"
    assert client.last_trace.rate_limits["x-ratelimit-remaining-requests"] == "9"


def test_openai_chat_surface_uses_chat_completions(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    def fake_request(url, headers, payload, client_request_id=None):
        captured["url"] = url
        captured["payload"] = payload
        return _ok_result(
            body={"choices": [{"message": {"content": "from-chat"}}]},
            client_request_id=client_request_id,
        )

    monkeypatch.setattr("forensic_archive.llm.request_json", fake_request)
    client = OpenAILLMClient("sk-test", "gpt-4.1", surface="chat")
    assert client.complete("q", system="sys") == "from-chat"
    assert captured["url"] == OPENAI_CHAT_URL
    assert captured["payload"]["messages"][0] == {"role": "system", "content": "sys"}


def test_openai_from_env_reads_overview_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORENSIC_LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_ACCESS_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY or OPENAI_ACCESS_TOKEN"):
        client_from_env()

    monkeypatch.setenv("OPENAI_ACCESS_TOKEN", "wif-token")
    monkeypatch.setenv("OPENAI_ORGANIZATION", "org-abc")
    monkeypatch.setenv("OPENAI_PROJECT", "proj-1")
    monkeypatch.setenv("OPENAI_API_SURFACE", "responses")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4.1-2025-04-14")
    client = client_from_env()
    assert isinstance(client, OpenAILLMClient)
    assert client.api_key == "wif-token"
    assert client.organization == "org-abc"
    assert client.project == "proj-1"
    assert client.surface == "responses"
    assert client.store is False
    assert client.model == "gpt-4.1-2025-04-14"


def test_openai_from_env_rejects_unknown_surface(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OPENAI_API_SURFACE", "realtime")
    with pytest.raises(ValueError, match="OPENAI_API_SURFACE"):
        OpenAILLMClient.from_env()


def test_extract_openai_text_from_output_items() -> None:
    payload = {
        "id": "resp_1",
        "output": [
            {
                "type": "message",
                "content": [
                    {"type": "output_text", "text": "PRIMARY"},
                    {"type": "output_text", "text": " TAIL"},
                ],
            }
        ],
    }
    assert extract_openai_text(payload) == "PRIMARY TAIL"
    assert extract_openai_text({"output_text": "helper"}, surface="responses") == "helper"
    assert (
        extract_openai_text(
            {"choices": [{"message": {"content": "chat"}}]},
            surface="chat",
        )
        == "chat"
    )


def test_client_request_id_must_be_ascii_and_short() -> None:
    assert validate_client_request_id("run-1:primary") == "run-1:primary"
    with pytest.raises(ValueError, match="ASCII"):
        validate_client_request_id("run-1:primárý")
    with pytest.raises(ValueError, match="512"):
        validate_client_request_id("x" * (CLIENT_REQUEST_ID_MAX + 1))
    with pytest.raises(ValueError, match="empty"):
        validate_client_request_id("")


def test_header_budget_rejects_oversized_custom_values() -> None:
    assert_header_budget(
        {
            "Authorization": "Bearer sk-test",
            "Content-Type": "application/json",
            "X-Client-Request-Id": "abc",
        }
    )
    with pytest.raises(ValueError, match="60 KiB"):
        assert_header_budget({"X-Custom": "x" * (60 * 1024 + 1)})


def test_http_error_includes_request_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    headers = _message_headers({"x-request-id": "req_failed", "x-ratelimit-remaining-requests": "0"})

    def boom(request: Request, timeout: float = 0):
        raise HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            headers,
            BytesIO(b'{"error":{"message":"invalid_api_key"}}'),
        )

    monkeypatch.setattr("forensic_archive.llm.urlopen", boom)
    with pytest.raises(LLMHttpError, match="HTTP 401") as excinfo:
        request_json(
            OPENAI_RESPONSES_URL,
            {
                "Authorization": "Bearer sk-bad",
                "Content-Type": "application/json",
                "X-Client-Request-Id": "client-9",
            },
            {"model": "gpt-4.1", "input": "hi"},
            client_request_id="client-9",
        )
    err = excinfo.value
    assert err.status == 401
    assert err.request_id == "req_failed"
    assert err.client_request_id == "client-9"
    assert "x-request-id=req_failed" in str(err)
    assert "X-Client-Request-Id=client-9" in str(err)
    assert "invalid_api_key" in err.body


def test_request_json_captures_overview_response_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: Request, timeout: float = 0):
        sent = {key.lower(): value for key, value in request.header_items()}
        assert sent.get("x-client-request-id") == "trace-1"
        assert sent.get("authorization") == "Bearer sk-test"
        return FakeResponse(
            {"output_text": "ok", "id": "resp_live"},
            {
                "x-request-id": "req_live",
                "openai-organization": "org-1",
                "openai-processing-ms": "15",
                "openai-version": "2020-10-01",
                "x-ratelimit-limit-requests": "100",
            },
        )

    monkeypatch.setattr("forensic_archive.llm.urlopen", fake_urlopen)
    result = request_json(
        OPENAI_RESPONSES_URL,
        {
            "Authorization": "Bearer sk-test",
            "Content-Type": "application/json",
            "X-Client-Request-Id": "trace-1",
        },
        {"model": "gpt-4.1", "input": "hi"},
        client_request_id="trace-1",
    )
    assert result.body["output_text"] == "ok"
    assert result.request_id == "req_live"
    assert result.headers["openai-processing-ms"] == "15"


def test_pipeline_records_client_request_ids(tmp_path) -> None:
    source = tmp_path / "src.md"
    source.write_text("A complete sentence for the reading room ledger.\n", encoding="utf-8")
    result = ForensicArchiver(provider="dummy").run(source, tmp_path / "out")
    archive = json.loads(result.archive_path.read_text(encoding="utf-8"))
    assert archive["llm"]["primary_extraction"]["client_request_id"] == f"{result.run_id}:primary"
    assert archive["llm"]["secondary_validation"]["client_request_id"] == f"{result.run_id}:secondary"

    import sqlite3

    conn = sqlite3.connect(result.ledger_path)
    rows = conn.execute(
        "SELECT role, client_request_id FROM llm_calls WHERE run_id = ? ORDER BY id",
        (result.run_id,),
    ).fetchall()
    conn.close()
    assert rows == [
        ("primary_extraction", f"{result.run_id}:primary"),
        ("secondary_validation", f"{result.run_id}:secondary"),
    ]


def _ok_result(*, headers: dict | None = None, body: dict | None = None, client_request_id: str | None = None):
    from forensic_archive.llm import HttpJsonResult

    return HttpJsonResult(
        body=body or {"output_text": "from-responses"},
        status=200,
        headers=headers or {"x-request-id": "req_test"},
        client_request_id=client_request_id,
    )
