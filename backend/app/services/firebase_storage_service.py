import os
from pathlib import Path

from dotenv import load_dotenv
from firebase_admin import storage
from google.api_core.exceptions import NotFound

from app.services.firebase_admin_service import initialize_firebase_admin

BACKEND_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BACKEND_DIR / ".env")


def _get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


def _validate_resume_storage_path(user_id: str, storage_path: str) -> str:
    expected_prefix = f"users/{user_id}/resumes/"

    if not storage_path or not storage_path.startswith(expected_prefix):
        raise ValueError("Resume storage path is not scoped to the user.")

    return storage_path


def delete_resume_file(user_id: str, storage_path: str) -> None:
    initialize_firebase_admin()
    bucket_name = _get_required_env("FIREBASE_STORAGE_BUCKET")
    safe_storage_path = _validate_resume_storage_path(user_id, storage_path)
    blob = storage.bucket(bucket_name).blob(safe_storage_path)

    try:
        blob.delete()
    except NotFound:
        return
