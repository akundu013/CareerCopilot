from fastapi.testclient import TestClient

from app.dependencies import get_current_user
from app.main import app

client = TestClient(app)


def test_get_current_user_endpoint_requires_authentication() -> None:
    app.dependency_overrides.clear()

    response = client.get("/api/auth/me")

    assert response.status_code == 401


def test_get_current_user_endpoint_returns_verified_user() -> None:
    app.dependency_overrides[get_current_user] = lambda: {
        "uid": "user-123",
        "email": "user@example.com",
        "email_verified": True,
    }

    try:
        response = client.get("/api/auth/me")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "uid": "user-123",
        "email": "user@example.com",
        "email_verified": True,
    }
