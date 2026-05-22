from typing import Any

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.schemas.auth import AuthenticatedUserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/me", response_model=AuthenticatedUserResponse)
def read_current_user(
    user: dict[str, Any] = Depends(get_current_user),
) -> AuthenticatedUserResponse:
    return AuthenticatedUserResponse(**user)
