# Backend Testing Guide

This backend uses `pytest` with FastAPI `TestClient`.

Run backend tests from the `backend/` folder with the project virtual environment.

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest
```

Run a single test file:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_match_engine.py
```

Run one test by name:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_api_auth.py -k "returns_verified_user"
```

## Test Files

`tests/test_health.py`

Checks that the FastAPI health endpoint responds successfully.

`tests/test_api_auth.py`

Tests the protected auth endpoint. It verifies that `/api/auth/me` rejects unauthenticated requests and returns the current user when the auth dependency is overridden with a verified user.

`tests/test_api_applications.py`

Tests application CRUD endpoints through FastAPI routing. It replaces the real repository with an in-memory fake repository, then checks create, list, update, delete, and not-found behavior.

`tests/test_api_analytics.py`

Tests the analytics summary API endpoint. It replaces repositories with fakes and verifies that the endpoint returns aggregated application, resume, analysis, and interview metrics.

`tests/test_analytics_service.py`

Tests pure analytics calculations, including application status counts, response rate, parsed resume counts, average match score, and requirement frequency output.

`tests/test_match_engine.py`

Tests deterministic job/resume matching. It covers exact matches, technical aliases, conservative related-term matching, missing requirements, and empty-input safety.

`tests/test_requirement_extractor.py`

Tests job requirement extraction cleanup. It checks noisy phrase removal, technology extraction, dish attendant requirements, and normalized requirement output.

`tests/test_interview_generator.py`

Tests deterministic interview question generation from analysis and job context.

`tests/test_demo_guard.py`

Tests demo-mode write protection rules so seeded demo data cannot be modified or deleted incorrectly.

`tests/test_ai_config.py`

Tests AI provider configuration loading and validation without exposing real secrets.

`tests/test_ai_provider_service.py`

Tests OpenRouter provider request handling with mocked network calls.

`tests/test_ai_feedback_service.py`

Tests AI feedback generation behavior, including fallback behavior when AI responses are malformed or unavailable.

`tests/test_ai_usage_service.py`

Tests AI usage tracking and daily limit behavior.

`tests/test_interview_ai_service.py`

Tests AI-assisted interview answer feedback behavior with mocked AI provider responses.

## Notes

- Tests should not require real Firebase, Firestore, Firebase Storage, or OpenRouter calls.
- Endpoint tests should override FastAPI dependencies and repository objects instead of hitting live services.
- Keep route tests focused on request validation, status codes, response shape, and dependency wiring.
- Keep service tests focused on pure business logic and edge cases.
