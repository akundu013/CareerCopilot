from app.config.ai import get_ai_config


def test_ai_config_defaults_to_disabled(monkeypatch):
    for name in [
        "AI_ENABLED",
        "AI_PROVIDER",
        "OPENROUTER_API_KEY",
        "OPENROUTER_MODEL",
        "AI_MAX_OUTPUT_TOKENS",
        "AI_DAILY_CALL_LIMIT_PER_USER",
        "AI_MONTHLY_CALL_LIMIT_GLOBAL",
        "AI_DEMO_MODE_LIVE_AI",
    ]:
        monkeypatch.delenv(name, raising=False)

    config = get_ai_config()

    assert not config.enabled
    assert config.provider == "openrouter"
    assert config.openrouter_api_key is None
    assert config.openrouter_model == "openrouter/free"
    assert config.max_output_tokens == 400
    assert config.daily_call_limit_per_user == 3
    assert config.monthly_call_limit_global == 50
    assert not config.demo_mode_live_ai
    assert not config.is_available


def test_ai_config_reads_backend_environment(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.setenv("AI_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODEL", "openrouter/free")
    monkeypatch.setenv("AI_MAX_OUTPUT_TOKENS", "120")
    monkeypatch.setenv("AI_DAILY_CALL_LIMIT_PER_USER", "2")
    monkeypatch.setenv("AI_MONTHLY_CALL_LIMIT_GLOBAL", "10")
    monkeypatch.setenv("AI_DEMO_MODE_LIVE_AI", "true")

    config = get_ai_config()

    assert config.enabled
    assert config.openrouter_api_key == "test-key"
    assert config.max_output_tokens == 120
    assert config.daily_call_limit_per_user == 2
    assert config.monthly_call_limit_global == 10
    assert config.demo_mode_live_ai
    assert config.is_available
