from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore_v1 import CollectionReference, DocumentReference

from app.services.firestore_service import get_user_applications_collection


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ApplicationRepository:
    def get_collection(self, user_id: str) -> CollectionReference:
        return get_user_applications_collection(user_id)

    def get_document(self, user_id: str, application_id: str) -> DocumentReference:
        if not application_id:
            raise ValueError("An application id is required.")

        return self.get_collection(user_id).document(application_id)

    def get_new_document(self, user_id: str) -> DocumentReference:
        return self.get_collection(user_id).document()

    def create(self, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        now = _utc_now()
        document = self.get_new_document(user_id)
        application = {
            **data,
            "id": document.id,
            "userId": user_id,
            "createdAt": now,
            "updatedAt": now,
        }

        document.set(application)

        return application

    def list(self, user_id: str) -> list[dict[str, Any]]:
        documents = self.get_collection(user_id).stream()
        applications: list[dict[str, Any]] = []

        for document in documents:
            data = document.to_dict() or {}
            applications.append({"id": document.id, **data})

        return applications

    def get(self, user_id: str, application_id: str) -> dict[str, Any] | None:
        document = self.get_document(user_id, application_id).get()

        if not document.exists:
            return None

        data = document.to_dict() or {}

        return {"id": document.id, **data}

    def update(
        self,
        user_id: str,
        application_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        document = self.get_document(user_id, application_id)

        if not document.get().exists:
            return None

        document.update({**data, "updatedAt": _utc_now()})

        return self.get(user_id, application_id)

    def delete(self, user_id: str, application_id: str) -> bool:
        document = self.get_document(user_id, application_id)

        if not document.get().exists:
            return False

        document.delete()

        return True
