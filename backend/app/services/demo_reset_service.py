from app.services.demo_guard import is_seeded_demo_record
from app.services.demo_seed_data import get_demo_user_uid, seed_demo_data
from app.services.firebase_storage_service import delete_resume_file
from app.services.firestore_service import get_firestore_client

DEMO_COLLECTIONS = ("applications", "resumes", "analyses", "interviews")


def reset_demo_data() -> dict[str, int]:
    demo_user_id = get_demo_user_uid()
    user_document = (
        get_firestore_client()
        .collection("users")
        .document(demo_user_id)
    )
    deleted_counts: dict[str, int] = {}

    for collection_name in DEMO_COLLECTIONS:
        deleted_counts[collection_name] = 0
        collection = user_document.collection(collection_name)

        for document in collection.stream():
            record = document.to_dict() or {}

            if is_seeded_demo_record(record):
                continue

            if collection_name == "resumes" and record.get("storagePath"):
                delete_resume_file(demo_user_id, record["storagePath"])

            document.reference.delete()
            deleted_counts[collection_name] += 1

    seeded_counts = seed_demo_data()

    return {
        "deletedApplications": deleted_counts["applications"],
        "deletedResumes": deleted_counts["resumes"],
        "deletedAnalyses": deleted_counts["analyses"],
        "deletedInterviews": deleted_counts["interviews"],
        "seededApplications": seeded_counts["applications"],
        "seededResumes": seeded_counts["resumes"],
        "seededAnalyses": seeded_counts["analyses"],
        "seededInterviews": seeded_counts["interviews"],
    }
