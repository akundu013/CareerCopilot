MAX_REQUIREMENT_SUGGESTIONS = 5


def generate_suggestions(
    missing_requirements: list[str],
    matched_requirements: list[str],
    match_score: int,
) -> list[str]:
    if not missing_requirements:
        return [_generate_summary_suggestion(matched_requirements, match_score)]

    suggestions = [
        _generate_missing_requirement_suggestion(requirement)
        for requirement in missing_requirements[:MAX_REQUIREMENT_SUGGESTIONS]
        if requirement.strip()
    ]

    if len(missing_requirements) > MAX_REQUIREMENT_SUGGESTIONS:
        suggestions.append(
            "Prioritize the remaining missing requirements that are most relevant "
            "to your real experience, and add specific examples if applicable.",
        )

    if match_score < 50:
        suggestions.append(
            "Consider tailoring your resume summary and recent role bullets more "
            "closely to the job description before applying.",
        )

    return suggestions


def _generate_missing_requirement_suggestion(requirement: str) -> str:
    normalized_requirement = _normalize_requirement(requirement)

    if not normalized_requirement:
        return (
            "Add a resume bullet that addresses this missing requirement, "
            "if it reflects your real experience."
        )

    return (
        "Add resume bullets that demonstrate experience with "
        f"{normalized_requirement}, if applicable."
    )


def _generate_summary_suggestion(
    matched_requirements: list[str],
    match_score: int,
) -> str:
    if matched_requirements and match_score >= 80:
        return (
            "Your resume appears to cover the detected requirements well. "
            "Strengthen it further with measurable results where applicable."
        )

    if matched_requirements:
        return (
            "Your resume matches some detected requirements. Add more specific "
            "examples and outcomes for the strongest matches, if applicable."
        )

    return (
        "No missing requirements were provided. Review the job description and "
        "add concrete resume examples for relevant experience, if applicable."
    )


def _normalize_requirement(requirement: str) -> str:
    return " ".join(requirement.lower().split())
