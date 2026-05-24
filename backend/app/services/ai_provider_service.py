import json
from typing import Any

import httpx

from app.config.ai import DEFAULT_AI_PROVIDER, get_ai_config

OPENROUTER_CHAT_COMPLETIONS_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)
DEFAULT_TIMEOUT_SECONDS = 20


class AIProviderError(RuntimeError):
    pass


class AIUnavailableError(AIProviderError):
    pass


class AIRateLimitError(AIProviderError):
    pass


def generate_json_response(
    system_prompt: str,
    user_payload: dict[str, Any],
) -> dict[str, Any]:
    config = get_ai_config()

    if not config.enabled:
        raise AIUnavailableError("AI is disabled for this environment.")

    if config.provider != DEFAULT_AI_PROVIDER:
        raise AIUnavailableError("Configured AI provider is not supported.")

    if not config.openrouter_api_key:
        raise AIUnavailableError("AI provider is not configured.")

    response = _post_openrouter_chat_completion(
        api_key=config.openrouter_api_key,
        model=config.openrouter_model,
        max_output_tokens=config.max_output_tokens,
        system_prompt=system_prompt,
        user_payload=user_payload,
    )

    return _extract_json_response(response)


def _post_openrouter_chat_completion(
    api_key: str,
    model: str,
    max_output_tokens: int,
    system_prompt: str,
    user_payload: dict[str, Any],
) -> dict[str, Any]:
    try:
        response = httpx.post(
            OPENROUTER_CHAT_COMPLETIONS_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            f"{system_prompt}\n"
                            "Return only concise valid JSON. Do not include "
                            "markdown, commentary, or code fences."
                        ),
                    },
                    {
                        "role": "user",
                        "content": json.dumps(user_payload),
                    },
                ],
                "max_tokens": max_output_tokens,
                "response_format": {"type": "json_object"},
            },
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        raise AIUnavailableError("AI provider is currently unavailable.") from exc

    if response.status_code == 429:
        raise AIRateLimitError("AI provider rate limit reached.")

    if response.status_code >= 400:
        raise AIUnavailableError(
            f"AI provider returned status {response.status_code}."
        )

    try:
        return response.json()
    except ValueError as exc:
        raise AIUnavailableError("AI provider returned invalid JSON.") from exc


def _extract_json_response(response: dict[str, Any]) -> dict[str, Any]:
    choices = response.get("choices")

    if not isinstance(choices, list) or not choices:
        raise AIUnavailableError("AI provider returned no choices.")

    first_choice = choices[0]

    if not isinstance(first_choice, dict):
        raise AIUnavailableError("AI provider returned an invalid choice.")

    message = first_choice.get("message")

    if not isinstance(message, dict):
        raise AIUnavailableError("AI provider returned an invalid message.")

    content = message.get("content")

    if isinstance(content, dict):
        return content

    if isinstance(content, str):
        try:
            return httpx.Response(200, content=content).json()
        except ValueError as exc:
            raise AIUnavailableError(
                "AI provider returned non-JSON content."
            ) from exc

    raise AIUnavailableError("AI provider returned empty content.")
