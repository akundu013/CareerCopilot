import pytest

from app.services import ai_usage_service
from app.services.ai_usage_service import AIUsageLimitError


def _enable_ai(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.setenv("AI_DAILY_CALL_LIMIT_PER_USER", "3")
    monkeypatch.setenv("AI_MONTHLY_CALL_LIMIT_GLOBAL", "50")
    monkeypatch.setenv("AI_DEMO_MODE_LIVE_AI", "false")


def test_ai_usage_blocks_when_disabled(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "false")

    with pytest.raises(AIUsageLimitError, match="disabled"):
        ai_usage_service.assert_ai_usage_allowed(
            {"uid": "user-1", "email": "user@example.com"},
        )


def test_ai_usage_blocks_demo_live_calls_by_default(monkeypatch):
    _enable_ai(monkeypatch)
    monkeypatch.setenv("DEMO_USER_EMAIL", "demo@example.com")

    with pytest.raises(AIUsageLimitError, match="Demo mode"):
        ai_usage_service.assert_ai_usage_allowed(
            {"uid": "demo-user", "email": "demo@example.com"},
        )


def test_ai_usage_blocks_daily_limit(monkeypatch):
    _enable_ai(monkeypatch)
    monkeypatch.setattr(ai_usage_service, "get_daily_ai_usage_count", lambda user_id: 3)
    monkeypatch.setattr(ai_usage_service, "get_monthly_global_ai_usage_count", lambda: 1)

    with pytest.raises(AIUsageLimitError, match="Daily AI limit"):
        ai_usage_service.assert_ai_usage_allowed(
            {"uid": "user-1", "email": "user@example.com"},
        )


def test_ai_usage_blocks_monthly_limit(monkeypatch):
    _enable_ai(monkeypatch)
    monkeypatch.setattr(ai_usage_service, "get_daily_ai_usage_count", lambda user_id: 1)
    monkeypatch.setattr(ai_usage_service, "get_monthly_global_ai_usage_count", lambda: 50)

    with pytest.raises(AIUsageLimitError, match="Monthly AI limit"):
        ai_usage_service.assert_ai_usage_allowed(
            {"uid": "user-1", "email": "user@example.com"},
        )


def test_ai_usage_allows_user_under_limits(monkeypatch):
    _enable_ai(monkeypatch)
    monkeypatch.setattr(ai_usage_service, "get_daily_ai_usage_count", lambda user_id: 1)
    monkeypatch.setattr(ai_usage_service, "get_monthly_global_ai_usage_count", lambda: 10)

    ai_usage_service.assert_ai_usage_allowed(
        {"uid": "user-1", "email": "user@example.com"},
    )
