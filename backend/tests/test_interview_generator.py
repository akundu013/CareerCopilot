from app.services.interview_generator import generate_interview_questions


def test_generates_grouped_interview_questions() -> None:
    questions = generate_interview_questions(
        "We need React, CI/CD, and PostgreSQL experience.",
        ["React", "PostgreSQL"],
        ["CI/CD"],
    )

    assert len(questions) == 15
    assert [question["category"] for question in questions[:5]] == [
        "general",
        "general",
        "general",
        "general",
        "general",
    ]
    assert [question["category"] for question in questions[5:10]] == [
        "behavioral",
        "behavioral",
        "behavioral",
        "behavioral",
        "behavioral",
    ]
    assert [question["category"] for question in questions[10:]] == [
        "technical",
        "technical",
        "technical",
        "technical",
        "technical",
    ]


def test_technical_questions_use_matched_and_missing_requirements() -> None:
    questions = generate_interview_questions(
        "We need React, CI/CD, and PostgreSQL experience.",
        ["React", "PostgreSQL"],
        ["CI/CD"],
    )
    prompts = [question["prompt"] for question in questions]

    assert "Explain your experience with React." in prompts
    assert "Explain your experience with PostgreSQL." in prompts
    assert "How would you prepare to discuss CI/CD in an interview?" in prompts


def test_question_generation_is_deterministic() -> None:
    first_result = generate_interview_questions(
        "Customer support role.",
        ["customer support"],
        ["billing issues"],
    )
    second_result = generate_interview_questions(
        "Customer support role.",
        ["customer support"],
        ["billing issues"],
    )

    assert first_result == second_result
