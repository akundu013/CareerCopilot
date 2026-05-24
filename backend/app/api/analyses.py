from collections.abc import Callable
import logging
from typing import Any, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_current_user
from app.schemas.analysis import (
    AnalysisResponse,
    AnalysisSummaryResponse,
    CreateAnalysisRequest,
)
from app.schemas.resume import ResumeStatus
from app.services.analysis_repository import AnalysisRepository
from app.services.demo_guard import (
    DemoModeError,
    assert_demo_can_create_analysis,
    assert_demo_can_delete_record,
    is_demo_user,
)
from app.services.improvement_service import generate_suggestions
from app.services.match_engine import analyze_match
from app.services.requirement_extractor import extract_requirements
from app.services.resume_repository import ResumeRepository

router = APIRouter(prefix="/api/analyses", tags=["analyses"])
analysis_repository = AnalysisRepository()
resume_repository = ResumeRepository()
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


def _analysis_not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Analysis not found.",
    )


def _resume_not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resume not found.",
    )


def _run_repository_operation(
    operation: Callable[[], RepositoryResult],
) -> RepositoryResult:
    try:
        return operation()
    except Exception as exc:
        logger.exception("Analysis repository operation failed.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Analysis storage is unavailable.",
        ) from exc


def _raise_demo_error(error: DemoModeError) -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(error),
    ) from error


@router.post(
    "",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_analysis(
    payload: CreateAnalysisRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AnalysisResponse:
    job_description = payload.jobDescription.strip()

    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description is required.",
        )

    user_id = _get_user_id(current_user)
    resume = _run_repository_operation(
        lambda: resume_repository.get(user_id, payload.resumeId),
    )

    if resume is None:
        raise _resume_not_found()

    if resume.get("status") != ResumeStatus.PARSED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected resume must be parsed before analysis.",
        )

    parsed_text = (resume.get("parsedText") or "").strip()

    if not parsed_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected resume does not have parsed text.",
        )

    if is_demo_user(current_user):
        try:
            assert_demo_can_create_analysis(user_id, payload.resumeId)
        except DemoModeError as error:
            _raise_demo_error(error)

    extracted_requirements = extract_requirements(job_description)

    if not extracted_requirements:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description did not contain enough detectable requirements.",
        )

    match_result = analyze_match(parsed_text, extracted_requirements)
    improvement_suggestions = generate_suggestions(
        match_result["missingRequirements"],
        match_result["matchedRequirements"],
        match_result["matchScore"],
    )
    analysis = _run_repository_operation(
        lambda: analysis_repository.create_analysis(
            user_id,
            {
                "resumeId": payload.resumeId,
                "resumeFileName": resume["fileName"],
                "jobDescription": job_description,
                "extractedRequirements": extracted_requirements,
                "matchScore": match_result["matchScore"],
                "matchedRequirements": match_result["matchedRequirements"],
                "missingRequirements": match_result["missingRequirements"],
                "improvementSuggestions": improvement_suggestions,
                **({"isDemoCreated": True} if is_demo_user(current_user) else {}),
            },
        ),
    )

    return AnalysisResponse(**analysis)


@router.get("", response_model=list[AnalysisSummaryResponse])
def list_analyses(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[AnalysisSummaryResponse]:
    user_id = _get_user_id(current_user)
    analyses = _run_repository_operation(
        lambda: analysis_repository.list_analyses(user_id),
    )

    return [AnalysisSummaryResponse(**analysis) for analysis in analyses]


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AnalysisResponse:
    user_id = _get_user_id(current_user)
    analysis = _run_repository_operation(
        lambda: analysis_repository.get_analysis(user_id, analysis_id),
    )

    if analysis is None:
        raise _analysis_not_found()

    return AnalysisResponse(**analysis)


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(
    analysis_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> Response:
    user_id = _get_user_id(current_user)

    if is_demo_user(current_user):
        analysis = _run_repository_operation(
            lambda: analysis_repository.get_analysis(user_id, analysis_id),
        )

        if analysis is None:
            raise _analysis_not_found()

        try:
            assert_demo_can_delete_record(analysis)
        except DemoModeError as error:
            _raise_demo_error(error)

    deleted = _run_repository_operation(
        lambda: analysis_repository.delete_analysis(user_id, analysis_id),
    )

    if not deleted:
        raise _analysis_not_found()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
