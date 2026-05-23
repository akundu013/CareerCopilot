import os
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import App, credentials

BACKEND_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BACKEND_DIR / ".env")


def _get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


def _normalize_private_key(private_key: str) -> str:
    return private_key.strip().replace("\\n", "\n")


def initialize_firebase_admin() -> App:
    try:
        return firebase_admin.get_app()
    except ValueError:
        project_id = _get_required_env("FIREBASE_PROJECT_ID")
        client_email = _get_required_env("FIREBASE_CLIENT_EMAIL")
        private_key = _normalize_private_key(
            _get_required_env("FIREBASE_PRIVATE_KEY")
        )

        certificate = credentials.Certificate(
            {
                "type": "service_account",
                "project_id": project_id,
                "private_key": private_key,
                "client_email": client_email,
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        )

        return firebase_admin.initialize_app(
            certificate,
            {"projectId": project_id},
        )
