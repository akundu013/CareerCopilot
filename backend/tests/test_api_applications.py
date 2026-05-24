from typing import Any

from fastapi.testclient import TestClient

from app.api import applications as applications_api
from app.dependencies import get_current_user
from app.main import app

client = TestClient(app)


class FakeApplicationRepository:
    def __init__(self) -> None:
        self.records: dict[str, dict[str, Any]] = {}
        self.next_id = 1

    def create(self, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        application_id = f"application-{self.next_id}"
        self.next_id += 1
        application = {
            "id": application_id,
            "userId": user_id,
            "company": data["company"],
            "role": data["role"],
            "status": data["status"],
            "location": data.get("location"),
            "jobUrl": data.get("jobUrl"),
            "salaryRange": data.get("salaryRange"),
            "notes": data.get("notes"),
            "dateApplied": data.get("dateApplied"),
            "createdAt": "2026-05-18T10:00:00+00:00",
            "updatedAt": "2026-05-18T10:00:00+00:00",
        }
        self.records[application_id] = application

        return application

    def list(self, user_id: str) -> list[dict[str, Any]]:
        return [
            application
            for application in self.records.values()
            if application["userId"] == user_id
        ]

    def get(self, user_id: str, application_id: str) -> dict[str, Any] | None:
        application = self.records.get(application_id)

        if application is None or application["userId"] != user_id:
            return None

        return application

    def update(
        self,
        user_id: str,
        application_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        application = self.get(user_id, application_id)

        if application is None:
            return None

        application.update(data)
        application["updatedAt"] = "2026-05-18T11:00:00+00:00"

        return application

    def delete(self, user_id: str, application_id: str) -> bool:
        application = self.get(user_id, application_id)

        if application is None:
            return False

        del self.records[application_id]

        return True


def test_application_crud_endpoints_use_authenticated_user() -> None:
    fake_repository = FakeApplicationRepository()
    original_repository = applications_api.application_repository
    applications_api.application_repository = fake_repository
    app.dependency_overrides[get_current_user] = lambda: {
        "uid": "user-123",
        "email": "user@example.com",
        "email_verified": True,
    }

    try:
        create_response = client.post(
            "/api/applications",
            json={
                "company": "Acme",
                "role": "Frontend Developer",
                "status": "applied",
                "location": "Remote",
            },
        )
        application_id = create_response.json()["id"]

        list_response = client.get("/api/applications")
        update_response = client.patch(
            f"/api/applications/{application_id}",
            json={"status": "interviewing"},
        )
        delete_response = client.delete(f"/api/applications/{application_id}")
        missing_response = client.get(f"/api/applications/{application_id}")
    finally:
        applications_api.application_repository = original_repository
        app.dependency_overrides.clear()

    assert create_response.status_code == 201
    assert create_response.json()["userId"] == "user-123"
    assert create_response.json()["company"] == "Acme"

    assert list_response.status_code == 200
    assert [application["id"] for application in list_response.json()] == [
        application_id,
    ]

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "interviewing"

    assert delete_response.status_code == 204
    assert missing_response.status_code == 404
