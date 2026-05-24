from collections import Counter
from datetime import datetime, timezone
from typing import Any

from app.schemas.analytics import AnalyticsSummaryResponse

RESPONSE_STATUSES = {"interviewing", "offer", "rejected"}
PARSED_RESUME_STATUS = "parsed"
TOP_REQUIREMENT_LIMIT = 5


def calculate_analytics_summary(
    applications: list[dict[str, Any]],
    resumes: list[dict[str, Any]],
    analyses: list[dict[str, Any]],
    interviews: list[dict[str, Any]],
) -> AnalyticsSummaryResponse:
    total_applications = len(applications)

    return AnalyticsSummaryResponse(
        totalApplications=total_applications,
        applicationsByStatus=_calculate_applications_by_status(applications),
        responseRate=_calculate_response_rate(applications),
        weeklyApplicationActivity=_calculate_weekly_activity(applications),
        totalResumes=len(resumes),
        parsedResumes=_count_parsed_resumes(resumes),
        totalAnalyses=len(analyses),
        averageMatchScore=_calculate_average_match_score(analyses),
        topMissingRequirements=_calculate_top_requirements(
            analyses,
            "missingRequirements",
        ),
        topMatchedRequirements=_calculate_top_requirements(
            analyses,
            "matchedRequirements",
        ),
        totalInterviewSessions=len(interviews),
        savedInterviewAnswers=_count_saved_interview_answers(interviews),
    )


def _calculate_applications_by_status(
    applications: list[dict[str, Any]],
) -> list[dict[str, int | str]]:
    status_counts = Counter(
        status
        for application in applications
        if (status := _normalize_text(application.get("status")))
    )

    return [
        {"status": status, "count": count}
        for status, count in sorted(status_counts.items())
    ]


def _calculate_response_rate(applications: list[dict[str, Any]]) -> float:
    if not applications:
        return 0

    response_count = sum(
        1
        for application in applications
        if _normalize_text(application.get("status")) in RESPONSE_STATUSES
    )

    return round((response_count / len(applications)) * 100, 1)


def _calculate_weekly_activity(
    applications: list[dict[str, Any]],
) -> list[dict[str, int | str]]:
    week_counts: Counter[str] = Counter()

    for application in applications:
        application_date = _parse_date(
            application.get("createdAt") or application.get("dateApplied"),
        )

        if application_date is None:
            continue

        week_start = _get_week_start(application_date)
        week_counts[week_start] += 1

    return [
        {"week": week, "count": count}
        for week, count in sorted(week_counts.items())
    ]


def _count_parsed_resumes(resumes: list[dict[str, Any]]) -> int:
    return sum(
        1
        for resume in resumes
        if _normalize_text(resume.get("status")) == PARSED_RESUME_STATUS
    )


def _calculate_average_match_score(analyses: list[dict[str, Any]]) -> float:
    scores = [
        score
        for analysis in analyses
        if isinstance(score := analysis.get("matchScore"), int | float)
    ]

    if not scores:
        return 0

    return round(sum(scores) / len(scores), 1)


def _calculate_top_requirements(
    analyses: list[dict[str, Any]],
    field_name: str,
) -> list[dict[str, int | str]]:
    requirement_counts: Counter[str] = Counter()

    for analysis in analyses:
        requirements = analysis.get(field_name)

        if not isinstance(requirements, list):
            continue

        for requirement in requirements:
            normalized_requirement = _normalize_requirement(requirement)

            if normalized_requirement:
                requirement_counts[normalized_requirement] += 1

    return [
        {"requirement": requirement, "count": count}
        for requirement, count in requirement_counts.most_common(
            TOP_REQUIREMENT_LIMIT,
        )
    ]


def _count_saved_interview_answers(interviews: list[dict[str, Any]]) -> int:
    saved_answer_count = 0

    for interview in interviews:
        answers = interview.get("answers")

        if not isinstance(answers, list):
            continue

        saved_answer_count += sum(
            1
            for answer in answers
            if isinstance(answer, dict)
            and isinstance(answer.get("answer"), str)
            and answer["answer"].strip()
        )

    return saved_answer_count


def _parse_date(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None

    normalized_value = value.strip().replace("Z", "+00:00")

    try:
        parsed_date = datetime.fromisoformat(normalized_value)
    except ValueError:
        return None

    if parsed_date.tzinfo is None:
        return parsed_date.replace(tzinfo=timezone.utc)

    return parsed_date.astimezone(timezone.utc)


def _get_week_start(value: datetime) -> str:
    week_start = value.date()
    week_start = week_start.fromordinal(week_start.toordinal() - value.weekday())

    return week_start.isoformat()


def _normalize_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""

    return value.strip().lower()


def _normalize_requirement(value: Any) -> str:
    if not isinstance(value, str):
        return ""

    return " ".join(value.split())
