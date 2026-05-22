from typing import Any

from fastapi import Header, HTTPException, status

from app.utils.auth import TokenVerificationError, verify_firebase_token


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    if not authorization:
        raise _unauthorized()

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise _unauthorized()

    try:
        return verify_firebase_token(token)
    except TokenVerificationError as exc:
        raise _unauthorized() from exc
