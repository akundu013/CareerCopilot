from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore_v1 import CollectionReference, DocumentReference

from app.services.firestore_service import get_user_analyses_collection


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AnalysisRepository:
    def get_collection(self, user_id: str) -> CollectionReference:
        return get_user_analyses_collection(user_id)

    def get_document(self, user_id: str, analysis_id: str) -> DocumentReference:
        if not analysis_id:
            raise ValueError("An analysis id is required.")

        return self.get_collection(user_id).document(analysis_id)

    def get_new_document(self, user_id: str) -> DocumentReference:
        return self.get_collection(user_id).document()

    def create_analysis(self, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        now = _utc_now()
        document = self.get_new_document(user_id)
        analysis = {
            **data,
            "id": document.id,
            "userId": user_id,
            "createdAt": now,
            "updatedAt": now,
        }

        document.set(analysis)

        return analysis

    def list_analyses(self, user_id: str) -> list[dict[str, Any]]:
        documents = self.get_collection(user_id).stream()
        analyses: list[dict[str, Any]] = []

        for document in documents:
            data = document.to_dict() or {}
            analyses.append({"id": document.id, **data})

        return analyses

    def get_analysis(self, user_id: str, analysis_id: str) -> dict[str, Any] | None:
        document = self.get_document(user_id, analysis_id).get()

        if not document.exists:
            return None

        data = document.to_dict() or {}

        return {"id": document.id, **data}

    def update_ai_feedback(
        self,
        user_id: str,
        analysis_id: str,
        feedback: dict[str, Any],
    ) -> dict[str, Any] | None:
        document = self.get_document(user_id, analysis_id)

        if not document.get().exists:
            return None

        document.update(
            {
                "aiFeedback": feedback,
                "updatedAt": _utc_now(),
            },
        )

        return self.get_analysis(user_id, analysis_id)

    def delete_analysis(self, user_id: str, analysis_id: str) -> bool:
        document = self.get_document(user_id, analysis_id)

        if not document.get().exists:
            return False

        document.delete()

        return True
