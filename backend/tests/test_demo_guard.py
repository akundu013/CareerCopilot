import pytest

from app.services import demo_guard
from app.services.demo_guard import DemoModeError


class FakeResumeRepository:
    def __init__(self, records):
        self.records = records

    def list(self, user_id):
        return self.records


class FakeAnalysisRepository:
    def __init__(self, records):
        self.records = records

    def list_analyses(self, user_id):
        return self.records


class FakeInterviewRepository:
    def __init__(self, records):
        self.records = records

    def list_sessions(self, user_id):
        return self.records


def test_is_demo_user_uses_configured_email(monkeypatch):
    monkeypatch.setenv("DEMO_USER_EMAIL", "demo@example.com")

    assert demo_guard.is_demo_user({"email": "Demo@Example.com"})
    assert not demo_guard.is_demo_user({"email": "user@example.com"})


def test_seeded_demo_record_detection():
    assert demo_guard.is_seeded_demo_record({"isSeededDemoData": True})
    assert demo_guard.is_seeded_demo_record({"createdByDemoSeed": True})
    assert not demo_guard.is_seeded_demo_record({"isDemoCreated": True})


def test_seeded_demo_record_cannot_be_deleted():
    with pytest.raises(DemoModeError, match="protects seeded data"):
        demo_guard.assert_demo_can_delete_record({"isSeededDemoData": True})


def test_demo_resume_limit(monkeypatch):
    monkeypatch.setattr(
        demo_guard,
        "resume_repository",
        FakeResumeRepository(
            [
                {"isDemoCreated": True},
                {"isDemoCreated": True},
                {"isSeededDemoData": True},
            ]
        ),
    )

    with pytest.raises(DemoModeError, match="up to 2 custom resumes"):
        demo_guard.assert_demo_can_create_resume("demo-user")


def test_demo_analysis_limit_is_scoped_to_resume(monkeypatch):
    monkeypatch.setattr(
        demo_guard,
        "analysis_repository",
        FakeAnalysisRepository(
            [
                {"resumeId": "resume-1", "isDemoCreated": True},
                {"resumeId": "resume-1", "isDemoCreated": True},
                {"resumeId": "resume-1", "isDemoCreated": True},
                {"resumeId": "resume-1", "isDemoCreated": True},
                {"resumeId": "resume-1", "isDemoCreated": True},
                {"resumeId": "resume-2", "isDemoCreated": True},
            ]
        ),
    )

    with pytest.raises(DemoModeError, match="up to 5 analyses"):
        demo_guard.assert_demo_can_create_analysis("demo-user", "resume-1")

    demo_guard.assert_demo_can_create_analysis("demo-user", "resume-2")


def test_demo_interview_session_limit(monkeypatch):
    monkeypatch.setattr(
        demo_guard,
        "interview_repository",
        FakeInterviewRepository(
            [
                {"isDemoCreated": True},
                {"isSeededDemoData": True},
            ]
        ),
    )

    with pytest.raises(DemoModeError, match="limited interview practice"):
        demo_guard.assert_demo_can_create_interview_session("demo-user")
