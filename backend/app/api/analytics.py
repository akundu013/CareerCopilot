from collections.abc import Callable
import logging
from typing import Any, TypeVar

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.analytics import AnalyticsSummaryResponse
from app.services.analysis_repository import AnalysisRepository
from app.services.analytics_service import calculate_analytics_summary
from app.services.application_repository import ApplicationRepository
from app.services.interview_repository import InterviewRepository
from app.services.resume_repository import ResumeRepository

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
application_repository = ApplicationRepository()
resume_repository = ResumeRepository()
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


def _run_repository_operation(
    operation: Callable[[], RepositoryResult],
) -> RepositoryResult:
    try:
        return operation()
    except Exception as exc:
        logger.exception("Analytics repository operation failed.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Analytics data is unavailable.",
        ) from exc


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AnalyticsSummaryResponse:
    user_id = _get_user_id(current_user)
    applications = _run_repository_operation(
        lambda: application_repository.list(user_id),
    )
    resumes = _run_repository_operation(
        lambda: resume_repository.list(user_id),
    )
    analyses = _run_repository_operation(
        lambda: analysis_repository.list_analyses(user_id),
    )
    interviews = _run_repository_operation(
        lambda: interview_repository.list_sessions(user_id),
    )

    return calculate_analytics_summary(
        applications,
        resumes,
        analyses,
        interviews,
    )
