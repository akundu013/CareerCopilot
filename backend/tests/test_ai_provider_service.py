import httpx
import pytest

from app.services import ai_provider_service
from app.services.ai_provider_service import (
    AIRateLimitError,
    AIUnavailableError,
)


def test_generate_json_response_blocks_when_disabled(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "false")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(AIUnavailableError, match="disabled"):
        ai_provider_service.generate_json_response("You are helpful.", {})


def test_generate_json_response_requires_key_when_enabled(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.setenv("AI_PROVIDER", "openrouter")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(AIUnavailableError, match="not configured"):
        ai_provider_service.generate_json_response("You are helpful.", {})


def test_generate_json_response_posts_to_openrouter(monkeypatch):
    captured_request = {}

    def fake_post(url, headers, json, timeout):
        captured_request["url"] = url
        captured_request["headers"] = headers
        captured_request["json"] = json
        captured_request["timeout"] = timeout

        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": '{"summary":"Good fit","tips":[]}',
                        },
                    }
                ],
            },
        )

    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.setenv("AI_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODEL", "openrouter/free")
    monkeypatch.setenv("AI_MAX_OUTPUT_TOKENS", "64")
    monkeypatch.setattr(ai_provider_service.httpx, "post", fake_post)

    response = ai_provider_service.generate_json_response(
        "Return feedback.",
        {"match_score": 80},
    )

    assert response == {"summary": "Good fit", "tips": []}
    assert captured_request["url"].endswith("/chat/completions")
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["json"]["model"] == "openrouter/free"
    assert captured_request["json"]["max_tokens"] == 64


def test_generate_json_response_handles_provider_rate_limit(monkeypatch):
    def fake_post(url, headers, json, timeout):
        return httpx.Response(429, json={"error": "rate limited"})

    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.setenv("AI_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(ai_provider_service.httpx, "post", fake_post)

    with pytest.raises(AIRateLimitError, match="rate limit"):
        ai_provider_service.generate_json_response("Return JSON.", {})
