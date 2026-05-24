from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore_v1 import CollectionReference, DocumentReference

from app.services.firestore_service import get_user_interviews_collection


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class InterviewRepository:
    def get_collection(self, user_id: str) -> CollectionReference:
        return get_user_interviews_collection(user_id)

    def get_document(self, user_id: str, session_id: str) -> DocumentReference:
        if not session_id:
            raise ValueError("An interview session id is required.")

        return self.get_collection(user_id).document(session_id)

    def get_new_document(self, user_id: str) -> DocumentReference:
        return self.get_collection(user_id).document()

    def create_session(
        self,
        user_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        now = _utc_now()
        document = self.get_new_document(user_id)
        session = {
            **data,
            "id": document.id,
            "userId": user_id,
            "createdAt": now,
            "updatedAt": now,
        }

        document.set(session)

        return session

    def list_sessions(self, user_id: str) -> list[dict[str, Any]]:
        documents = self.get_collection(user_id).stream()
        sessions: list[dict[str, Any]] = []

        for document in documents:
            data = document.to_dict() or {}
            sessions.append({"id": document.id, **data})

        return sessions

    def get_session(
        self,
        user_id: str,
        session_id: str,
    ) -> dict[str, Any] | None:
        document = self.get_document(user_id, session_id).get()

        if not document.exists:
            return None

        data = document.to_dict() or {}

        return {"id": document.id, **data}

    def update_answers(
        self,
        user_id: str,
        session_id: str,
        answers: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        document = self.get_document(user_id, session_id)

        if not document.get().exists:
            return None

        document.update(
            {
                "answers": answers,
                "updatedAt": _utc_now(),
            },
        )

        return self.get_session(user_id, session_id)

    def update_ai_questions(
        self,
        user_id: str,
        session_id: str,
        questions: list[dict[str, Any]],
        source: str,
        generated_at: str,
    ) -> dict[str, Any] | None:
        document = self.get_document(user_id, session_id)

        if not document.get().exists:
            return None

        document.update(
            {
                "aiQuestions": questions,
                "aiQuestionsSource": source,
                "aiQuestionsGeneratedAt": generated_at,
                "updatedAt": _utc_now(),
            },
        )

        return self.get_session(user_id, session_id)

    def delete_session(self, user_id: str, session_id: str) -> bool:
        document = self.get_document(user_id, session_id)

        if not document.get().exists:
            return False

        document.delete()

        return True
