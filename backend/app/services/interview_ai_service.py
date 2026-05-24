from datetime import datetime, timezone
from typing import Any

from app.schemas.interview import InterviewQuestionCategory
from app.services.ai_provider_service import generate_json_response
from app.services.interview_generator import generate_interview_questions

AI_TECHNICAL_QUESTION_COUNT = 3
AI_BEHAVIORAL_QUESTION_COUNT = 2
MAX_PROMPT_LENGTH = 240


class AIInterviewQuestionFormatError(ValueError):
    pass


def generate_ai_interview_questions(
    analysis: dict[str, Any],
) -> dict[str, Any]:
    response = generate_json_response(
        "You create concise interview practice questions from structured data.",
        _build_interview_payload(analysis),
    )
    questions = _normalize_ai_questions(response)
    generated_at = _utc_now()

    return {
        "questions": questions,
        "source": "openrouter",
        "generatedAt": generated_at,
        "message": "AI interview questions generated.",
    }


def generate_fallback_interview_questions(
    analysis: dict[str, Any],
) -> dict[str, Any]:
    generated_questions = generate_interview_questions(
        analysis.get("jobDescription") or "",
        analysis.get("matchedRequirements") or [],
        analysis.get("missingRequirements") or [],
    )
    questions = _select_fallback_questions(generated_questions)

    return {
        "questions": questions,
        "source": "deterministic_fallback",
        "generatedAt": _utc_now(),
        "message": "AI is unavailable, so standard tailored questions were used.",
    }


def _build_interview_payload(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "target_role": "Not specified",
        "matched_skills": _clean_string_list(
            analysis.get("matchedRequirements") or [],
        ),
        "missing_skills": _clean_string_list(
            analysis.get("missingRequirements") or [],
        ),
        "experience_level": "junior",
    }


def _normalize_ai_questions(response: dict[str, Any]) -> list[dict[str, str]]:
    technical_prompts = _extract_prompt_list(
        response,
        ("technicalQuestions", "technical_questions"),
        AI_TECHNICAL_QUESTION_COUNT,
    )
    behavioral_prompts = _extract_prompt_list(
        response,
        ("behavioralQuestions", "behavioral_questions"),
        AI_BEHAVIORAL_QUESTION_COUNT,
    )

    if len(technical_prompts) < AI_TECHNICAL_QUESTION_COUNT:
        raise AIInterviewQuestionFormatError(
            "AI response did not include enough technical questions."
        )

    if len(behavioral_prompts) < AI_BEHAVIORAL_QUESTION_COUNT:
        raise AIInterviewQuestionFormatError(
            "AI response did not include enough behavioral questions."
        )

    return [
        *_build_questions(
            InterviewQuestionCategory.TECHNICAL.value,
            technical_prompts,
        ),
        *_build_questions(
            InterviewQuestionCategory.BEHAVIORAL.value,
            behavioral_prompts,
        ),
    ]


def _extract_prompt_list(
    response: dict[str, Any],
    keys: tuple[str, ...],
    limit: int,
) -> list[str]:
    values: Any = None

    for key in keys:
        values = response.get(key)

        if values is not None:
            break

    if not isinstance(values, list):
        return []

    prompts = [
        prompt
        for prompt in (_clean_text(value, MAX_PROMPT_LENGTH) for value in values)
        if prompt
    ]

    return prompts[:limit]


def _select_fallback_questions(
    questions: list[dict[str, str]],
) -> list[dict[str, str]]:
    technical_questions = [
        question
        for question in questions
        if question.get("category") == InterviewQuestionCategory.TECHNICAL.value
    ][:AI_TECHNICAL_QUESTION_COUNT]
    behavioral_questions = [
        question
        for question in questions
        if question.get("category") == InterviewQuestionCategory.BEHAVIORAL.value
    ][:AI_BEHAVIORAL_QUESTION_COUNT]

    return [
        *_rebuild_question_ids(
            InterviewQuestionCategory.TECHNICAL.value,
            technical_questions,
        ),
        *_rebuild_question_ids(
            InterviewQuestionCategory.BEHAVIORAL.value,
            behavioral_questions,
        ),
    ]


def _build_questions(
    category: str,
    prompts: list[str],
) -> list[dict[str, str]]:
    return [
        {
            "id": f"ai-{category}-{index}",
            "category": category,
            "prompt": prompt,
        }
        for index, prompt in enumerate(prompts, start=1)
    ]


def _rebuild_question_ids(
    category: str,
    questions: list[dict[str, str]],
) -> list[dict[str, str]]:
    return _build_questions(
        category,
        [
            question["prompt"]
            for question in questions
            if question.get("prompt")
        ],
    )


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
