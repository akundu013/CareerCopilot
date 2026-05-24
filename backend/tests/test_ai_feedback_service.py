from app.services import ai_feedback_service


def test_generate_ai_feedback_sends_only_sanitized_match_data(monkeypatch):
    captured_payload = {}

    def fake_generate_json_response(system_prompt, user_payload):
        captured_payload.update(user_payload)

        return {
            "summary": "Strong fit for the role.",
            "tips": ["Emphasize TypeScript impact.", "Add testing examples."],
        }

    monkeypatch.setattr(
        ai_feedback_service,
        "generate_json_response",
        fake_generate_json_response,
    )

    feedback = ai_feedback_service.generate_ai_feedback(
        {
            "matchScore": 82,
            "matchedRequirements": ["TypeScript", "React"],
            "missingRequirements": ["Testing"],
            "extractedRequirements": ["TypeScript", "React", "Testing"],
            "jobDescription": "This full job description must not be sent.",
            "parsedText": "This resume text must not be sent.",
        }
    )

    assert feedback["summary"] == "Strong fit for the role."
    assert feedback["tips"] == [
        "Emphasize TypeScript impact.",
        "Add testing examples.",
    ]
    assert captured_payload == {
        "target_role": "Not specified",
        "match_score": 82,
        "matched_skills": ["TypeScript", "React"],
        "missing_skills": ["Testing"],
        "job_keywords": ["TypeScript", "React", "Testing"],
    }


def test_generate_ai_feedback_limits_tips(monkeypatch):
    monkeypatch.setattr(
        ai_feedback_service,
        "generate_json_response",
        lambda system_prompt, user_payload: {
            "summary": "Useful summary.",
            "tips": ["One", "Two", "Three", "Four"],
        },
    )

    feedback = ai_feedback_service.generate_ai_feedback(
        {
            "matchScore": 60,
            "matchedRequirements": [],
            "missingRequirements": [],
            "extractedRequirements": [],
        }
    )

    assert feedback["tips"] == ["One", "Two", "Three"]


def test_generate_fallback_feedback_uses_saved_match_data():
    feedback = ai_feedback_service.generate_fallback_feedback(
        {
            "matchScore": 55,
            "matchedRequirements": ["React"],
            "missingRequirements": ["Testing", "CI/CD"],
        }
    )

    assert feedback["source"] == "deterministic_fallback"
    assert "partial match" in feedback["summary"].lower()
    assert feedback["tips"] == [
        "Strengthen evidence for Testing if it reflects real experience.",
        "Strengthen evidence for CI/CD if it reflects real experience.",
    ]
