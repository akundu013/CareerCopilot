from functools import lru_cache

from firebase_admin import firestore
from google.cloud.firestore_v1 import Client, CollectionReference

from app.services.firebase_admin_service import initialize_firebase_admin


def _require_user_id(user_id: str) -> str:
    if not user_id:
        raise ValueError("A user id is required to access user-owned data.")

    return user_id


@lru_cache(maxsize=1)
def get_firestore_client() -> Client:
    initialize_firebase_admin()
    return firestore.client()


def get_user_applications_collection(user_id: str) -> CollectionReference:
    owner_id = _require_user_id(user_id)

    return (
        get_firestore_client()
        .collection("users")
        .document(owner_id)
        .collection("applications")
    )


def get_user_resumes_collection(user_id: str) -> CollectionReference:
    owner_id = _require_user_id(user_id)

    return (
        get_firestore_client()
        .collection("users")
        .document(owner_id)
        .collection("resumes")
    )


def get_user_analyses_collection(user_id: str) -> CollectionReference:
    owner_id = _require_user_id(user_id)

    return (
        get_firestore_client()
        .collection("users")
        .document(owner_id)
        .collection("analyses")
    )
