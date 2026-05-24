import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BACKEND_DIR / ".env")

DEFAULT_AI_PROVIDER = "openrouter"
DEFAULT_OPENROUTER_MODEL = "openrouter/free"
DEFAULT_AI_MAX_OUTPUT_TOKENS = 400
DEFAULT_AI_DAILY_CALL_LIMIT_PER_USER = 3
DEFAULT_AI_MONTHLY_CALL_LIMIT_GLOBAL = 50
DEFAULT_AI_DEMO_MODE_LIVE_AI = False


@dataclass(frozen=True)
class AIConfig:
    enabled: bool
    provider: str
    openrouter_api_key: str | None
    openrouter_model: str
    max_output_tokens: int
    daily_call_limit_per_user: int
    monthly_call_limit_global: int
    demo_mode_live_ai: bool

    @property
    def is_available(self) -> bool:
        return (
            self.enabled
            and self.provider == DEFAULT_AI_PROVIDER
            and bool(self.openrouter_api_key)
        )


def get_ai_config() -> AIConfig:
    return AIConfig(
        enabled=_get_bool_env("AI_ENABLED", False),
        provider=os.getenv("AI_PROVIDER", DEFAULT_AI_PROVIDER).strip().lower(),
        openrouter_api_key=_get_optional_env("OPENROUTER_API_KEY"),
        openrouter_model=os.getenv(
            "OPENROUTER_MODEL",
            DEFAULT_OPENROUTER_MODEL,
        ).strip(),
        max_output_tokens=_get_int_env(
            "AI_MAX_OUTPUT_TOKENS",
            DEFAULT_AI_MAX_OUTPUT_TOKENS,
        ),
        daily_call_limit_per_user=_get_int_env(
            "AI_DAILY_CALL_LIMIT_PER_USER",
            DEFAULT_AI_DAILY_CALL_LIMIT_PER_USER,
        ),
        monthly_call_limit_global=_get_int_env(
            "AI_MONTHLY_CALL_LIMIT_GLOBAL",
            DEFAULT_AI_MONTHLY_CALL_LIMIT_GLOBAL,
        ),
        demo_mode_live_ai=_get_bool_env(
            "AI_DEMO_MODE_LIVE_AI",
            DEFAULT_AI_DEMO_MODE_LIVE_AI,
        ),
    )


def _get_optional_env(name: str) -> str | None:
    value = os.getenv(name)

    if not value:
        return None

    return value.strip() or None


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        parsed_value = int(value)
    except ValueError:
        return default

    return max(0, parsed_value)
