from google.cloud.firestore_v1 import CollectionReference, DocumentReference

from app.services.firestore_service import get_user_applications_collection


class ApplicationRepository:
    def get_collection(self, user_id: str) -> CollectionReference:
        return get_user_applications_collection(user_id)

    def get_document(self, user_id: str, application_id: str) -> DocumentReference:
        if not application_id:
            raise ValueError("An application id is required.")

        return self.get_collection(user_id).document(application_id)

    def get_new_document(self, user_id: str) -> DocumentReference:
        return self.get_collection(user_id).document()
