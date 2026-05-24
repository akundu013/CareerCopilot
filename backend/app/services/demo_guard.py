from typing import Any

from app.config.demo import (
    DEMO_ANALYSES_PER_CUSTOM_RESUME_LIMIT,
    DEMO_CUSTOM_RESUME_LIMIT,
    get_demo_user_email,
)
from app.services.analysis_repository import AnalysisRepository
from app.services.resume_repository import ResumeRepository

resume_repository = ResumeRepository()
analysis_repository = AnalysisRepository()


class DemoModeError(ValueError):
    pass


def is_demo_user(user: dict[str, Any]) -> bool:
    email = str(user.get("email") or "").strip().lower()

    return bool(email) and email == get_demo_user_email()


def is_seeded_demo_record(record: dict[str, Any] | None) -> bool:
    if not record:
        return False

    return bool(
        record.get("isSeededDemoData") or record.get("createdByDemoSeed")
    )


def _is_demo_created_record(record: dict[str, Any]) -> bool:
    return bool(record.get("isDemoCreated")) and not is_seeded_demo_record(record)


def assert_demo_can_create_resume(user_id: str) -> None:
    resumes = resume_repository.list(user_id)
    custom_resume_count = sum(
        1
        for resume in resumes
        if _is_demo_created_record(resume)
    )

    if custom_resume_count >= DEMO_CUSTOM_RESUME_LIMIT:
        raise DemoModeError("Demo mode allows up to 2 custom resumes.")


def assert_demo_can_create_analysis(user_id: str, resume_id: str) -> None:
    analyses = analysis_repository.list_analyses(user_id)
    custom_analysis_count = sum(
        1
        for analysis in analyses
        if analysis.get("resumeId") == resume_id
        and _is_demo_created_record(analysis)
    )

    if custom_analysis_count >= DEMO_ANALYSES_PER_CUSTOM_RESUME_LIMIT:
        raise DemoModeError(
            "Demo mode allows up to 5 analyses per custom resume."
        )


def assert_demo_can_delete_record(record: dict[str, Any] | None) -> None:
    if is_seeded_demo_record(record):
        raise DemoModeError("Demo mode protects seeded data from deletion.")
