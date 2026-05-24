from app.services.analytics_service import calculate_analytics_summary


def test_empty_data_returns_zero_state_summary() -> None:
    summary = calculate_analytics_summary([], [], [], [])

    assert summary.model_dump() == {
        "totalApplications": 0,
        "applicationsByStatus": [],
        "responseRate": 0,
        "weeklyApplicationActivity": [],
        "totalResumes": 0,
        "parsedResumes": 0,
        "totalAnalyses": 0,
        "averageMatchScore": 0,
        "topMissingRequirements": [],
        "topMatchedRequirements": [],
        "totalInterviewSessions": 0,
        "savedInterviewAnswers": 0,
    }


def test_calculates_application_metrics() -> None:
    applications = [
        {
            "status": "applied",
            "createdAt": "2026-05-18T10:00:00+00:00",
        },
        {
            "status": "interviewing",
            "createdAt": "2026-05-19T10:00:00+00:00",
        },
        {
            "status": "offer",
            "createdAt": "2026-05-25T10:00:00+00:00",
        },
        {
            "status": "rejected",
            "createdAt": "2026-05-25T12:00:00+00:00",
        },
    ]

    summary = calculate_analytics_summary(applications, [], [], [])

    assert summary.totalApplications == 4
    assert summary.responseRate == 75
    assert [
        item.model_dump()
        for item in summary.applicationsByStatus
    ] == [
        {"status": "applied", "count": 1},
        {"status": "interviewing", "count": 1},
        {"status": "offer", "count": 1},
        {"status": "rejected", "count": 1},
    ]
    assert [
        item.model_dump()
        for item in summary.weeklyApplicationActivity
    ] == [
        {"week": "2026-05-18", "count": 2},
        {"week": "2026-05-25", "count": 2},
    ]


def test_calculates_resume_analysis_and_interview_metrics() -> None:
    resumes = [
        {"status": "uploaded"},
        {"status": "parsed"},
        {"status": "parsed"},
    ]
    analyses = [
        {
            "matchScore": 70,
            "missingRequirements": ["CI/CD", "PostgreSQL"],
            "matchedRequirements": ["React", "TypeScript"],
        },
        {
            "matchScore": 90,
            "missingRequirements": ["CI/CD"],
            "matchedRequirements": ["React", "Node.js"],
        },
    ]
    interviews = [
        {
            "answers": [
                {"questionId": "general-1", "answer": "Prepared answer"},
                {"questionId": "general-2", "answer": " "},
            ],
        },
        {
            "answers": [
                {"questionId": "technical-1", "answer": "Another answer"},
            ],
        },
    ]

    summary = calculate_analytics_summary([], resumes, analyses, interviews)

    assert summary.totalResumes == 3
    assert summary.parsedResumes == 2
    assert summary.totalAnalyses == 2
    assert summary.averageMatchScore == 80
    assert [
        item.model_dump()
        for item in summary.topMissingRequirements
    ] == [
        {"requirement": "CI/CD", "count": 2},
        {"requirement": "PostgreSQL", "count": 1},
    ]
    assert [
        item.model_dump()
        for item in summary.topMatchedRequirements
    ] == [
        {"requirement": "React", "count": 2},
        {"requirement": "TypeScript", "count": 1},
        {"requirement": "Node.js", "count": 1},
    ]
    assert summary.totalInterviewSessions == 2
    assert summary.savedInterviewAnswers == 2
