from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore_v1 import CollectionReference, DocumentReference

from app.services.firestore_service import get_user_resumes_collection


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ResumeRepository:
    def get_collection(self, user_id: str) -> CollectionReference:
        return get_user_resumes_collection(user_id)

    def get_document(self, user_id: str, resume_id: str) -> DocumentReference:
        if not resume_id:
            raise ValueError("A resume id is required.")

        return self.get_collection(user_id).document(resume_id)

    def get_new_document(self, user_id: str) -> DocumentReference:
        return self.get_collection(user_id).document()

    def create(self, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        now = _utc_now()
        document = self.get_new_document(user_id)
        resume = {
            **data,
            "id": document.id,
            "userId": user_id,
            "createdAt": now,
            "updatedAt": now,
        }

        document.set(resume)

        return resume

    def list(self, user_id: str) -> list[dict[str, Any]]:
        documents = self.get_collection(user_id).stream()
        resumes: list[dict[str, Any]] = []

        for document in documents:
            data = document.to_dict() or {}
            resumes.append({"id": document.id, **data})

        return resumes

    def get(self, user_id: str, resume_id: str) -> dict[str, Any] | None:
        document = self.get_document(user_id, resume_id).get()

        if not document.exists:
            return None

        data = document.to_dict() or {}

        return {"id": document.id, **data}

    def update(
        self,
        user_id: str,
        resume_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        document = self.get_document(user_id, resume_id)

        if not document.get().exists:
            return None

        document.update({**data, "updatedAt": _utc_now()})

        return self.get(user_id, resume_id)

    def update_parse_result(
        self,
        user_id: str,
        resume_id: str,
        status: str,
        parsed_text: str | None = None,
    ) -> dict[str, Any] | None:
        return self.update(
            user_id,
            resume_id,
            {
                "status": status,
                "parsedText": parsed_text,
            },
        )

    def delete(self, user_id: str, resume_id: str) -> bool:
        document = self.get_document(user_id, resume_id)

        if not document.get().exists:
            return False

        document.delete()

        return True
