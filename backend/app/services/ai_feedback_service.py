from datetime import datetime, timezone
from typing import Any

from app.services.ai_provider_service import generate_json_response

MAX_FEEDBACK_TIPS = 3
MAX_SUMMARY_LENGTH = 420
MAX_TIP_LENGTH = 220


class AIFeedbackFormatError(ValueError):
    pass


def generate_ai_feedback(analysis: dict[str, Any]) -> dict[str, Any]:
    response = generate_json_response(
        "You write short, practical resume-to-job match feedback.",
        _build_feedback_payload(analysis),
    )

    return _normalize_feedback_response(response)


def generate_fallback_feedback(analysis: dict[str, Any]) -> dict[str, Any]:
    match_score = int(analysis.get("matchScore") or 0)
    matched_requirements = _clean_string_list(
        analysis.get("matchedRequirements") or [],
    )
    missing_requirements = _clean_string_list(
        analysis.get("missingRequirements") or [],
    )

    if match_score >= 80:
        summary = (
            "This is a strong match. The saved analysis shows that the resume "
            "already covers most of the detected role requirements."
        )
    elif matched_requirements:
        summary = (
            "This is a partial match. The resume has useful overlap with the "
            "role, but the missing requirements should be reviewed before applying."
        )
    else:
        summary = (
            "This match needs more tailoring. The resume should be adjusted with "
            "clearer evidence for the detected job requirements."
        )

    tips = [
        f"Strengthen evidence for {requirement} if it reflects real experience."
        for requirement in missing_requirements[:MAX_FEEDBACK_TIPS]
    ]

    if not tips and matched_requirements:
        tips.append(
            "Add measurable outcomes for the strongest matched requirements."
        )

    return {
        "summary": summary,
        "tips": tips,
        "generatedAt": _utc_now(),
        "source": "deterministic_fallback",
    }


def _build_feedback_payload(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "target_role": "Not specified",
        "match_score": analysis.get("matchScore", 0),
        "matched_skills": _clean_string_list(
            analysis.get("matchedRequirements") or [],
        ),
        "missing_skills": _clean_string_list(
            analysis.get("missingRequirements") or [],
        ),
        "job_keywords": _clean_string_list(
            analysis.get("extractedRequirements") or [],
        ),
    }


def _normalize_feedback_response(response: dict[str, Any]) -> dict[str, Any]:
    summary = _clean_text(response.get("summary"), MAX_SUMMARY_LENGTH)
    tips_source = response.get("tips") or response.get("improvement_tips") or []

    if not summary:
        raise AIFeedbackFormatError("AI feedback did not include a summary.")

    if not isinstance(tips_source, list):
        raise AIFeedbackFormatError("AI feedback tips must be a list.")

    tips = [
        tip
        for tip in (
            _clean_text(tip, MAX_TIP_LENGTH)
            for tip in tips_source[:MAX_FEEDBACK_TIPS]
        )
        if tip
    ]

    return {
        "summary": summary,
        "tips": tips,
        "generatedAt": _utc_now(),
        "source": "openrouter",
    }


def _clean_string_list(values: list[Any]) -> list[str]:
    cleaned_values: list[str] = []

    for value in values:
        cleaned_value = _clean_text(value, 80)

        if cleaned_value:
            cleaned_values.append(cleaned_value)

    return cleaned_values[:12]


def _clean_text(value: Any, max_length: int) -> str:
    if not isinstance(value, str):
        return ""

    return " ".join(value.split())[:max_length].strip()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
