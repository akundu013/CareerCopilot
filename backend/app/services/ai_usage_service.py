from datetime import datetime, timezone
from typing import Any

from firebase_admin import firestore

from app.config.ai import get_ai_config
from app.services.demo_guard import is_demo_user
from app.services.firestore_service import get_firestore_client

AI_USAGE_COLLECTION = "ai_usage"
USER_DAILY_USAGE_COLLECTION = "ai_daily_usage"
GLOBAL_USAGE_DOCUMENT = "global"


class AIUsageLimitError(RuntimeError):
    pass


def assert_ai_usage_allowed(user: dict[str, Any]) -> None:
    config = get_ai_config()

    if not config.enabled:
        raise AIUsageLimitError("AI is disabled for this environment.")

    if is_demo_user(user) and not config.demo_mode_live_ai:
        raise AIUsageLimitError("Demo mode uses saved AI output, not live AI calls.")

    user_id = _get_user_id(user)
    daily_count = get_daily_ai_usage_count(user_id)
    monthly_count = get_monthly_global_ai_usage_count()

    if daily_count >= config.daily_call_limit_per_user:
        raise AIUsageLimitError("Daily AI limit reached for this user.")

    if monthly_count >= config.monthly_call_limit_global:
        raise AIUsageLimitError("Monthly AI limit reached for this app.")


def record_ai_usage(user_id: str) -> None:
    safe_user_id = _require_user_id(user_id)
    client = get_firestore_client()
    date_key = _get_utc_date_key()
    month_key = _get_utc_month_key()
    user_usage_document = (
        client.collection("users")
        .document(safe_user_id)
        .collection(USER_DAILY_USAGE_COLLECTION)
        .document(date_key)
    )
    monthly_usage_document = (
        client.collection(AI_USAGE_COLLECTION)
        .document(GLOBAL_USAGE_DOCUMENT)
        .collection("monthly")
        .document(month_key)
    )
    now = _utc_now()

    user_usage_document.set(
        {
            "userId": safe_user_id,
            "date": date_key,
            "count": firestore.Increment(1),
            "updatedAt": now,
        },
        merge=True,
    )
    monthly_usage_document.set(
        {
            "month": month_key,
            "count": firestore.Increment(1),
            "updatedAt": now,
        },
        merge=True,
    )


def get_daily_ai_usage_count(user_id: str) -> int:
    safe_user_id = _require_user_id(user_id)
    document = (
        get_firestore_client()
        .collection("users")
        .document(safe_user_id)
        .collection(USER_DAILY_USAGE_COLLECTION)
        .document(_get_utc_date_key())
        .get()
    )

    if not document.exists:
        return 0

    data = document.to_dict() or {}

    return _coerce_count(data.get("count"))


def get_monthly_global_ai_usage_count() -> int:
    document = (
        get_firestore_client()
        .collection(AI_USAGE_COLLECTION)
        .document(GLOBAL_USAGE_DOCUMENT)
        .collection("monthly")
        .document(_get_utc_month_key())
        .get()
    )

    if not document.exists:
        return 0

    data = document.to_dict() or {}

    return _coerce_count(data.get("count"))


def _get_user_id(user: dict[str, Any]) -> str:
    return _require_user_id(str(user.get("uid") or ""))


def _require_user_id(user_id: str) -> str:
    if not user_id:
        raise AIUsageLimitError("Authenticated user is missing a user id.")

    return user_id


def _coerce_count(value: Any) -> int:
    if isinstance(value, int):
        return max(0, value)

    return 0


def _get_utc_date_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _get_utc_month_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
