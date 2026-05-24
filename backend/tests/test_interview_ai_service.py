from app.services import interview_ai_service


def test_generate_ai_interview_questions_sends_only_structured_data(monkeypatch):
    captured_payload = {}

    def fake_generate_json_response(system_prompt, user_payload):
        captured_payload.update(user_payload)

        return {
            "technicalQuestions": [
                "How do you structure React components?",
                "How do you test TypeScript code?",
                "How do you debug API failures?",
            ],
            "behavioralQuestions": [
                "Tell us about a time you clarified ambiguity.",
                "Describe a time you improved quality.",
            ],
        }

    monkeypatch.setattr(
        interview_ai_service,
        "generate_json_response",
        fake_generate_json_response,
    )

    result = interview_ai_service.generate_ai_interview_questions(
        {
            "matchedRequirements": ["React", "TypeScript"],
            "missingRequirements": ["Testing"],
            "jobDescription": "This full job description must not be sent.",
        }
    )

    assert len(result["questions"]) == 5
    assert result["questions"][0]["category"] == "technical"
    assert result["questions"][3]["category"] == "behavioral"
    assert captured_payload == {
        "target_role": "Not specified",
        "matched_skills": ["React", "TypeScript"],
        "missing_skills": ["Testing"],
        "experience_level": "junior",
    }


def test_generate_fallback_interview_questions_uses_deterministic_bank():
    result = interview_ai_service.generate_fallback_interview_questions(
        {
            "jobDescription": "Role needs React and testing.",
            "matchedRequirements": ["React"],
            "missingRequirements": ["Testing"],
        }
    )

    assert result["source"] == "deterministic_fallback"
    assert len(result["questions"]) == 5
    assert {question["category"] for question in result["questions"]} == {
        "technical",
        "behavioral",
    }
