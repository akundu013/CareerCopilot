from collections.abc import Callable
import logging
from typing import Any, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_current_user
from app.schemas.resume import (
    CreateResumeRequest,
    ResumeResponse,
    ResumeStatus,
    UpdateResumeRequest,
)
from app.services.resume_parser import (
    ResumeParseError,
    download_resume_file,
    parse_resume_file,
)
from app.services.resume_repository import ResumeRepository
from app.services.firebase_storage_service import delete_resume_file

router = APIRouter(prefix="/api/resumes", tags=["resumes"])
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


def _not_found() -> HTTPException:
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
        logger.exception("Resume repository operation failed.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Resume storage is unavailable.",
        ) from exc


def _run_storage_operation(operation: Callable[[], None]) -> None:
    try:
        operation()
    except Exception as exc:
        logger.exception("Resume file storage operation failed.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Resume file storage is unavailable.",
        ) from exc


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resume(
    payload: CreateResumeRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResumeResponse:
    user_id = _get_user_id(current_user)
    resume = _run_repository_operation(
        lambda: resume_repository.create(
            user_id,
            payload.model_dump(mode="json", exclude_none=True),
        ),
    )

    return ResumeResponse(**resume)


@router.get("", response_model=list[ResumeResponse])
def list_resumes(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[ResumeResponse]:
    user_id = _get_user_id(current_user)
    resumes = _run_repository_operation(
        lambda: resume_repository.list(user_id),
    )

    return [ResumeResponse(**resume) for resume in resumes]


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResumeResponse:
    user_id = _get_user_id(current_user)
    resume = _run_repository_operation(
        lambda: resume_repository.get(user_id, resume_id),
    )

    if resume is None:
        raise _not_found()

    return ResumeResponse(**resume)


def _update_parse_result(
    user_id: str,
    resume_id: str,
    status_value: str,
    parsed_text: str | None = None,
) -> ResumeResponse:
    resume = _run_repository_operation(
        lambda: resume_repository.update_parse_result(
            user_id,
            resume_id,
            status_value,
            parsed_text,
        ),
    )

    if resume is None:
        raise _not_found()

    return ResumeResponse(**resume)


@router.post("/{resume_id}/parse", response_model=ResumeResponse)
def parse_resume(
    resume_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResumeResponse:
    user_id = _get_user_id(current_user)
    resume = _run_repository_operation(
        lambda: resume_repository.get(user_id, resume_id),
    )

    if resume is None:
        raise _not_found()

    try:
        file_bytes = download_resume_file(resume["fileUrl"])
        parsed_text = parse_resume_file(file_bytes, resume["contentType"])
    except ResumeParseError:
        logger.exception("Resume parsing failed.")
        return _update_parse_result(
            user_id,
            resume_id,
            ResumeStatus.PARSE_FAILED.value,
        )

    return _update_parse_result(
        user_id,
        resume_id,
        ResumeStatus.PARSED.value,
        parsed_text,
    )


@router.patch("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: str,
    payload: UpdateResumeRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResumeResponse:
    update_data = payload.model_dump(mode="json", exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one resume field must be provided.",
        )

    user_id = _get_user_id(current_user)
    resume = _run_repository_operation(
        lambda: resume_repository.update(user_id, resume_id, update_data),
    )

    if resume is None:
        raise _not_found()

    return ResumeResponse(**resume)


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> Response:
    user_id = _get_user_id(current_user)
    resume = _run_repository_operation(
        lambda: resume_repository.get(user_id, resume_id),
    )

    if resume is None:
        raise _not_found()

    _run_storage_operation(
        lambda: delete_resume_file(user_id, resume["storagePath"]),
    )
    _run_repository_operation(
        lambda: resume_repository.delete(user_id, resume_id),
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
