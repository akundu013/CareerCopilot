from typing import Any

from fastapi.testclient import TestClient

from app.api import analytics as analytics_api
from app.dependencies import get_current_user
from app.main import app

client = TestClient(app)


class FakeApplicationRepository:
    def list(self, user_id: str) -> list[dict[str, Any]]:
        return [
            {
                "id": "application-1",
                "userId": user_id,
                "company": "Acme",
                "role": "Frontend Developer",
                "status": "applied",
                "createdAt": "2026-05-18T10:00:00+00:00",
            },
            {
                "id": "application-2",
                "userId": user_id,
                "company": "Beta",
                "role": "Backend Developer",
                "status": "interviewing",
                "createdAt": "2026-05-19T10:00:00+00:00",
            },
        ]


class FakeResumeRepository:
    def list(self, user_id: str) -> list[dict[str, Any]]:
        return [
            {"id": "resume-1", "userId": user_id, "status": "parsed"},
            {"id": "resume-2", "userId": user_id, "status": "uploaded"},
        ]


class FakeAnalysisRepository:
    def list_analyses(self, user_id: str) -> list[dict[str, Any]]:
        return [
            {
                "id": "analysis-1",
                "userId": user_id,
                "matchScore": 80,
                "matchedRequirements": ["React", "TypeScript"],
                "missingRequirements": ["Docker"],
            },
            {
                "id": "analysis-2",
                "userId": user_id,
                "matchScore": 60,
                "matchedRequirements": ["React"],
                "missingRequirements": ["AWS"],
            },
        ]


class FakeInterviewRepository:
    def list_sessions(self, user_id: str) -> list[dict[str, Any]]:
        return [
            {
                "id": "interview-1",
                "userId": user_id,
                "answers": [
                    {"questionId": "question-1", "answer": "STAR answer"},
                    {"questionId": "question-2", "answer": ""},
                ],
            },
        ]


def test_analytics_summary_endpoint_returns_aggregated_metrics() -> None:
    original_application_repository = analytics_api.application_repository
    original_resume_repository = analytics_api.resume_repository
    original_analysis_repository = analytics_api.analysis_repository
    original_interview_repository = analytics_api.interview_repository

    analytics_api.application_repository = FakeApplicationRepository()
    analytics_api.resume_repository = FakeResumeRepository()
    analytics_api.analysis_repository = FakeAnalysisRepository()
    analytics_api.interview_repository = FakeInterviewRepository()
    app.dependency_overrides[get_current_user] = lambda: {
        "uid": "user-123",
        "email": "user@example.com",
        "email_verified": True,
    }

    try:
        response = client.get("/api/analytics/summary")
    finally:
        analytics_api.application_repository = original_application_repository
        analytics_api.resume_repository = original_resume_repository
        analytics_api.analysis_repository = original_analysis_repository
        analytics_api.interview_repository = original_interview_repository
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["totalApplications"] == 2
    assert data["applicationsByStatus"] == [
        {"status": "applied", "count": 1},
        {"status": "interviewing", "count": 1},
    ]
    assert data["responseRate"] == 50
    assert data["totalResumes"] == 2
    assert data["parsedResumes"] == 1
    assert data["totalAnalyses"] == 2
    assert data["averageMatchScore"] == 70
    assert data["topMatchedRequirements"][0] == {
        "requirement": "React",
        "count": 2,
    }
    assert data["totalInterviewSessions"] == 1
    assert data["savedInterviewAnswers"] == 1
