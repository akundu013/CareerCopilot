from collections.abc import Callable
import logging
from typing import Any, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_current_user
from app.schemas.application import (
    ApplicationResponse,
    CreateApplicationRequest,
    UpdateApplicationRequest,
)
from app.services.application_repository import ApplicationRepository
from app.services.demo_guard import (
    DemoModeError,
    assert_demo_can_delete_record,
    assert_demo_can_update_record,
    is_demo_user,
)

router = APIRouter(prefix="/api/applications", tags=["applications"])
application_repository = ApplicationRepository()
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
        detail="Application not found.",
    )


def _run_repository_operation(
    operation: Callable[[], RepositoryResult],
) -> RepositoryResult:
    try:
        return operation()
    except Exception as exc:
        logger.exception("Application repository operation failed.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application storage is unavailable.",
        ) from exc


def _raise_demo_error(error: DemoModeError) -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(error),
    ) from error


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    payload: CreateApplicationRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ApplicationResponse:
    user_id = _get_user_id(current_user)
    application_data = payload.model_dump(mode="json", exclude_none=True)

    if is_demo_user(current_user):
        application_data["isDemoCreated"] = True

    application = _run_repository_operation(
        lambda: application_repository.create(
            user_id,
            application_data,
        ),
    )

    return ApplicationResponse(**application)


@router.get("", response_model=list[ApplicationResponse])
def list_applications(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[ApplicationResponse]:
    user_id = _get_user_id(current_user)
    applications = _run_repository_operation(
        lambda: application_repository.list(user_id),
    )

    return [ApplicationResponse(**application) for application in applications]


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ApplicationResponse:
    user_id = _get_user_id(current_user)
    application = _run_repository_operation(
        lambda: application_repository.get(user_id, application_id),
    )

    if application is None:
        raise _not_found()

    return ApplicationResponse(**application)


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: str,
    payload: UpdateApplicationRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ApplicationResponse:
    update_data = payload.model_dump(mode="json", exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one application field must be provided.",
        )

    user_id = _get_user_id(current_user)

    if is_demo_user(current_user):
        existing_application = _run_repository_operation(
            lambda: application_repository.get(user_id, application_id),
        )

        if existing_application is None:
            raise _not_found()

        try:
            assert_demo_can_update_record(existing_application)
        except DemoModeError as error:
            _raise_demo_error(error)

    application = _run_repository_operation(
        lambda: application_repository.update(
            user_id,
            application_id,
            update_data,
        ),
    )

    if application is None:
        raise _not_found()

    return ApplicationResponse(**application)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> Response:
    user_id = _get_user_id(current_user)

    if is_demo_user(current_user):
        application = _run_repository_operation(
            lambda: application_repository.get(user_id, application_id),
        )

        if application is None:
            raise _not_found()

        try:
            assert_demo_can_delete_record(application)
        except DemoModeError as error:
            _raise_demo_error(error)

    deleted = _run_repository_operation(
        lambda: application_repository.delete(user_id, application_id),
    )

    if not deleted:
        raise _not_found()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
