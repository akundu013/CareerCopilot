# Career Copilot Architecture

Career Copilot is split into a Next.js frontend and a FastAPI backend. The
frontend owns user interaction, routing, Firebase client authentication, and
presentation. The backend owns business logic, validation, Firebase Admin
access, deterministic analysis, analytics, and optional AI actions.

## Core Flow

```text
Browser
  -> Next.js App Router
  -> Firebase Auth
  -> FastAPI with Bearer token
  -> Firebase Admin verification
  -> Firestore / Firebase Storage
```

Backend routes stay thin. Shared behavior lives in `backend/app/services/`,
schemas live in `backend/app/schemas/`, and authentication dependencies live in
`backend/app/dependencies.py`.

## AI Boundary

AI is an optional enhancement layer, not the source of truth.

Allowed AI actions:

- Generate short match feedback from saved match results.
- Generate tailored interview practice questions from structured analysis data.

AI never:

- Calculates the match score.
- Replaces the deterministic match engine.
- Parses resumes.
- Receives uploaded files or full parsed resume text.
- Runs automatically on page load.
- Exposes provider, model, or API key controls to users.

## AI Flow

```text
User clicks AI action
  -> Frontend calls FastAPI
  -> Backend checks AI config and usage limits
  -> Backend sends sanitized structured data to OpenRouter
  -> Backend stores AI output on the existing record
  -> Repeated requests return saved output
```

OpenRouter configuration is backend-only:

```env
AI_ENABLED=false
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openrouter/free
AI_MAX_OUTPUT_TOKENS=400
AI_DAILY_CALL_LIMIT_PER_USER=3
AI_MONTHLY_CALL_LIMIT_GLOBAL=50
AI_DEMO_MODE_LIVE_AI=false
```

If AI is disabled or unavailable, the core product continues to work. Interview
questions fall back to the deterministic local question bank. Demo mode defaults
to saved seeded AI output and does not consume live AI quota.
