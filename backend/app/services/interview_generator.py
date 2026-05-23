from app.schemas.interview import InterviewQuestionCategory


GENERAL_QUESTION_TEMPLATES = (
    "Tell us about yourself and the experience you would bring to this role.",
    "Why are you interested in this position?",
    "What makes you a strong candidate for this job?",
    "Which part of the job description feels most aligned with your background?",
    "What would you want the interview team to remember about you?",
)

BEHAVIORAL_QUESTION_TEMPLATES = (
    "Tell us about a time you handled a challenging project or responsibility.",
    "Describe a time you had to learn something quickly for work.",
    "Tell us about a time you worked with others to solve a problem.",
    "Describe a situation where you received feedback and acted on it.",
    "Tell us about a time you had to manage competing priorities.",
)

TECHNICAL_FALLBACK_QUESTIONS = (
    "Walk us through how you would approach the main responsibilities in this role.",
    "What tools or methods would you use to succeed in this position?",
    "How do you validate the quality of your work?",
    "How do you troubleshoot when something does not work as expected?",
    "What would you prepare before starting in this role?",
)

QUESTION_COUNT_PER_CATEGORY = 5


def generate_interview_questions(
    job_description: str,
    matched_requirements: list[str],
    missing_requirements: list[str],
) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []

    questions.extend(
        _build_questions(
            InterviewQuestionCategory.GENERAL.value,
            GENERAL_QUESTION_TEMPLATES,
        ),
    )
    questions.extend(
        _build_questions(
            InterviewQuestionCategory.BEHAVIORAL.value,
            _build_behavioral_questions(matched_requirements),
        ),
    )
    questions.extend(
        _build_questions(
            InterviewQuestionCategory.TECHNICAL.value,
            _build_technical_questions(
                job_description,
                matched_requirements,
                missing_requirements,
            ),
        ),
    )

    return questions


def _build_questions(
    category: str,
    prompts: tuple[str, ...] | list[str],
) -> list[dict[str, str]]:
    return [
        {
            "id": f"{category}-{index}",
            "category": category,
            "prompt": prompt,
        }
        for index, prompt in enumerate(
            prompts[:QUESTION_COUNT_PER_CATEGORY],
            start=1,
        )
    ]


def _build_behavioral_questions(matched_requirements: list[str]) -> list[str]:
    prompts: list[str] = []

    for requirement in _clean_requirements(matched_requirements):
        prompts.append(
            f"Tell us about a time you demonstrated experience with {requirement}.",
        )

    prompts.extend(BEHAVIORAL_QUESTION_TEMPLATES)

    return _deduplicate_prompts(prompts)[:QUESTION_COUNT_PER_CATEGORY]


def _build_technical_questions(
    job_description: str,
    matched_requirements: list[str],
    missing_requirements: list[str],
) -> list[str]:
    prompts: list[str] = []

    for requirement in _clean_requirements(matched_requirements):
        prompts.append(f"Explain your experience with {requirement}.")

    for requirement in _clean_requirements(missing_requirements):
        prompts.append(
            f"How would you prepare to discuss {requirement} in an interview?",
        )

    if job_description.strip():
        prompts.append(
            "Which requirement from the job description would you discuss first, and why?",
        )

    prompts.extend(TECHNICAL_FALLBACK_QUESTIONS)

    return _deduplicate_prompts(prompts)[:QUESTION_COUNT_PER_CATEGORY]


def _clean_requirements(requirements: list[str]) -> list[str]:
    cleaned_requirements: list[str] = []

    for requirement in requirements:
        cleaned_requirement = " ".join(requirement.split())

        if cleaned_requirement:
            cleaned_requirements.append(cleaned_requirement)

    return cleaned_requirements


def _deduplicate_prompts(prompts: list[str]) -> list[str]:
    unique_prompts: list[str] = []
    seen: set[str] = set()

    for prompt in prompts:
        normalized_prompt = prompt.casefold()

        if normalized_prompt in seen:
            continue

        seen.add(normalized_prompt)
        unique_prompts.append(prompt)

    return unique_prompts
