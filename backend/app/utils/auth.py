from typing import Any

from firebase_admin import auth
from firebase_admin import exceptions as firebase_exceptions

from app.services.firebase_admin_service import initialize_firebase_admin


class TokenVerificationError(Exception):
    pass


def verify_firebase_token(token: str) -> dict[str, Any]:
    if not token:
        raise TokenVerificationError("Firebase ID token is required.")

    initialize_firebase_admin()

    try:
        decoded_token = auth.verify_id_token(token)
    except (
        auth.ExpiredIdTokenError,
        auth.InvalidIdTokenError,
        auth.RevokedIdTokenError,
        firebase_exceptions.FirebaseError,
        ValueError,
    ) as exc:
        raise TokenVerificationError("Invalid or expired Firebase ID token.") from exc

    uid = decoded_token.get("uid")

    if not uid:
        raise TokenVerificationError("Firebase ID token is missing a user id.")

    return {
        "uid": uid,
        "email": decoded_token.get("email"),
        "email_verified": decoded_token.get("email_verified"),
    }
