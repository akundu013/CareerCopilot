from collections.abc import Callable
import logging
from typing import Any, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_current_user
from app.schemas.interview import (
    CreateInterviewSessionRequest,
    InterviewAIQuestionsResponse,
    InterviewAnswer,
    InterviewSessionResponse,
    UpdateInterviewAnswersRequest,
)
from app.services.ai_provider_service import AIProviderError
from app.services.ai_usage_service import (
    AIUsageLimitError,
    assert_ai_usage_allowed,
    record_ai_usage,
)
from app.services.analysis_repository import AnalysisRepository
from app.services.demo_guard import (
    DemoModeError,
    assert_demo_can_create_interview_session,
    assert_demo_can_delete_record,
    assert_demo_can_update_record,
    is_demo_user,
    is_seeded_demo_record,
)
from app.services.interview_generator import generate_interview_questions
from app.services.interview_ai_service import (
    AIInterviewQuestionFormatError,
    generate_ai_interview_questions,
    generate_fallback_interview_questions,
)
from app.services.interview_repository import InterviewRepository

router = APIRouter(prefix="/api/interviews", tags=["interviews"])
analysis_repository = AnalysisRepository()
interview_repository = InterviewRepository()
RepositoryResult = TypeVar("RepositoryResult")
logger = logging.getLogger(__name__)


def _get_user_id(user: dict[str, Any]) -> str:
    user_id = user.get("uid")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user is missing a user id.",
        )

    return user_id


def _session_not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Interview session not found.",
    )


def _analysis_not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Analysis not found.",
    )


def _run_repository_operation(
    operation: Callable[[], RepositoryResult],
) -> RepositoryResult:
    try:
        return operation()
    except Exception as exc:
        logger.exception("Interview repository operation failed.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Interview storage is unavailable.",
        ) from exc


def _raise_demo_error(error: DemoModeError) -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(error),
    ) from error


def _raise_ai_usage_error(error: AIUsageLimitError) -> None:
    detail = str(error)
    status_code = (
        status.HTTP_429_TOO_MANY_REQUESTS
        if "limit" in detail.lower()
        else status.HTTP_403_FORBIDDEN
    )

    raise HTTPException(status_code=status_code, detail=detail) from error


@router.post(
    "",
    response_model=InterviewSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview_session(
    payload: CreateInterviewSessionRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> InterviewSessionResponse:
    user_id = _get_user_id(current_user)
    analysis = _run_repository_operation(
        lambda: analysis_repository.get_analysis(user_id, payload.analysisId),
    )

    if analysis is None:
        raise _analysis_not_found()

    if is_demo_user(current_user):
        try:
            assert_demo_can_create_interview_session(user_id)
        except DemoModeError as error:
            _raise_demo_error(error)

    questions = generate_interview_questions(
        analysis.get("jobDescription") or "",
        analysis.get("matchedRequirements") or [],
        analysis.get("missingRequirements") or [],
    )
    answers = [
        {
            "questionId": question["id"],
            "answer": "",
        }
        for question in questions
    ]
    session = _run_repository_operation(
        lambda: interview_repository.create_session(
            user_id,
            {
                "analysisId": payload.analysisId,
                "resumeId": analysis["resumeId"],
                "resumeFileName": analysis["resumeFileName"],
                "questions": questions,
                "answers": answers,
                **({"isDemoCreated": True} if is_demo_user(current_user) else {}),
            },
        ),
    )

    return InterviewSessionResponse(**session)


@router.post(
    "/{session_id}/ai-questions",
    response_model=InterviewAIQuestionsResponse,
)
def generate_session_ai_questions(
    session_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> InterviewAIQuestionsResponse:
    user_id = _get_user_id(current_user)
    session = _run_repository_operation(
        lambda: interview_repository.get_session(user_id, session_id),
    )

    if session is None:
        raise _session_not_found()

    saved_questions = session.get("aiQuestions")

    if isinstance(saved_questions, list) and saved_questions:
        return InterviewAIQuestionsResponse(
            questions=saved_questions,
            source=session.get("aiQuestionsSource") or "saved",
            generatedAt=session.get("aiQuestionsGeneratedAt")
            or session.get("updatedAt"),
            message="Saved AI interview questions loaded.",
        )

    analysis = _run_repository_operation(
        lambda: analysis_repository.get_analysis(user_id, session["analysisId"]),
    )

    if analysis is None:
        raise _analysis_not_found()

    should_record_usage = False

    try:
        assert_ai_usage_allowed(current_user)
        ai_question_result = generate_ai_interview_questions(analysis)
        should_record_usage = True
    except AIUsageLimitError as error:
        if "limit" in str(error).lower():
            _raise_ai_usage_error(error)

        ai_question_result = generate_fallback_interview_questions(analysis)
    except (
        AIProviderError,
        AIInterviewQuestionFormatError,
    ):
        ai_question_result = generate_fallback_interview_questions(analysis)

    should_store_questions = not (
        is_demo_user(current_user) and is_seeded_demo_record(session)
    )

    if should_store_questions:
        updated_session = _run_repository_operation(
            lambda: interview_repository.update_ai_questions(
                user_id,
                session_id,
                ai_question_result["questions"],
                ai_question_result["source"],
                ai_question_result["generatedAt"],
            ),
        )

        if updated_session is None:
            raise _session_not_found()

    if should_record_usage:
        _run_repository_operation(lambda: record_ai_usage(user_id))

    return InterviewAIQuestionsResponse(**ai_question_result)


@router.get("", response_model=list[InterviewSessionResponse])
def list_interview_sessions(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[InterviewSessionResponse]:
    user_id = _get_user_id(current_user)
    sessions = _run_repository_operation(
        lambda: interview_repository.list_sessions(user_id),
    )

    return [InterviewSessionResponse(**session) for session in sessions]


@router.get("/{session_id}", response_model=InterviewSessionResponse)
def get_interview_session(
    session_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> InterviewSessionResponse:
    user_id = _get_user_id(current_user)
    session = _run_repository_operation(
        lambda: interview_repository.get_session(user_id, session_id),
    )

    if session is None:
        raise _session_not_found()

    return InterviewSessionResponse(**session)


@router.put(
    "/{session_id}/answers",
    response_model=InterviewSessionResponse,
)
def update_interview_answers(
    session_id: str,
    payload: UpdateInterviewAnswersRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> InterviewSessionResponse:
    user_id = _get_user_id(current_user)
    session = _run_repository_operation(
        lambda: interview_repository.get_session(user_id, session_id),
    )

    if session is None:
        raise _session_not_found()

    if is_demo_user(current_user):
        try:
            assert_demo_can_update_record(session)
        except DemoModeError as error:
            _raise_demo_error(error)

    answers = _validate_answers(payload.answers, session)
    updated_session = _run_repository_operation(
        lambda: interview_repository.update_answers(
            user_id,
            session_id,
            answers,
        ),
    )

    if updated_session is None:
        raise _session_not_found()

    return InterviewSessionResponse(**updated_session)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview_session(
    session_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> Response:
    user_id = _get_user_id(current_user)

    if is_demo_user(current_user):
        session = _run_repository_operation(
            lambda: interview_repository.get_session(user_id, session_id),
        )

        if session is None:
            raise _session_not_found()

        try:
            assert_demo_can_delete_record(session)
        except DemoModeError as error:
            _raise_demo_error(error)

    deleted = _run_repository_operation(
        lambda: interview_repository.delete_session(user_id, session_id),
    )

    if not deleted:
        raise _session_not_found()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _validate_answers(
    answers: list[InterviewAnswer],
    session: dict[str, Any],
) -> list[dict[str, str]]:
    allowed_question_ids = {
        question["id"]
        for question in session.get("questions", [])
        if question.get("id")
    }
    submitted_question_ids: set[str] = set()
    validated_answers: list[dict[str, str]] = []

    for answer in answers:
        if answer.questionId not in allowed_question_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Answer references an unknown interview question.",
            )

        if answer.questionId in submitted_question_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate answers for the same question are not allowed.",
            )

        submitted_question_ids.add(answer.questionId)
        validated_answers.append(answer.model_dump())

    return validated_answers
