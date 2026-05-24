# Milestone 11 — AI Patching & Cost Controls

## Goal

Add a small optional AI layer to Career Copilot using **OpenRouter `/free` models**.

AI must improve the existing app without becoming the core feature, creating unexpected cost, or exposing provider control to users.

The app owner controls AI through backend environment variables. Users can only trigger approved AI actions when the backend allows it.

---

## Boundaries

AI is allowed only for:

- generating short match feedback from existing match results
- generating tailored interview questions from role and skills data

AI must not:

- calculate the match score
- replace the match engine
- parse resumes
- receive full CV text
- receive uploaded resume files
- receive personal contact details
- run automatically on page load
- be configurable by the user

The app must work when AI is disabled.

---

## Environment Configuration

Use OpenRouter as the first provider.

```env
AI_ENABLED=true
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=openrouter/free
AI_MAX_OUTPUT_TOKENS=400

AI_DAILY_CALL_LIMIT_PER_USER=3
AI_MONTHLY_CALL_LIMIT_GLOBAL=50
AI_DEMO_MODE_LIVE_AI=false
```

Important rules:

- `OPENROUTER_API_KEY` is stored only in the backend environment.
- Never expose the key in frontend code.
- Never use `NEXT_PUBLIC_OPENROUTER_API_KEY`.
- Users cannot choose the model.
- The model is controlled only by backend environment variables.
- Demo mode should use seeded AI output, not live AI calls.

---

## Step 1 — Add AI Configuration

### Goal

Make AI controlled from backend environment variables.

### Tasks

- Add AI variables to `.env.example`
- Read AI config in backend settings
- Support `AI_ENABLED=false`
- Support `AI_PROVIDER=openrouter`
- Support `OPENROUTER_MODEL=openrouter/free`
- Ensure missing API key does not crash the app when AI is disabled

### Success Criteria

- AI can be turned on or off by the app owner
- User cannot control AI availability
- Backend knows whether AI is available
- App still works without an AI key when AI is disabled

---

## Step 2 — Create AI Provider Service

### Goal

Create one backend service responsible for AI calls.

### Files

```text
backend/app/services/ai_provider_service.py
```

### Tasks

- Create OpenRouter client call
- Use `OPENROUTER_API_KEY` from backend environment
- Use `OPENROUTER_MODEL` from backend environment
- Cap output with `AI_MAX_OUTPUT_TOKENS`
- Request concise JSON responses
- Return safe errors when AI is disabled, unavailable, or rate-limited

### Success Criteria

- Frontend never calls OpenRouter directly
- API key stays private
- Model can be changed without changing feature code
- Provider failure does not break the main app

---

## Step 3 — Add Usage Limits

### Goal

Prevent abuse and protect the free quota.

### Files

```text
backend/app/services/ai_usage_service.py
```

### Tasks

- Track daily AI calls per user
- Track monthly global AI calls
- Block calls after limits are reached
- Block live AI calls for demo users when `AI_DEMO_MODE_LIVE_AI=false`
- Return clear limit messages

### Success Criteria

- Each user has a small daily limit
- The whole app has a monthly limit
- Demo account does not consume live AI calls
- Free quota is protected even if AI has no direct cost

---

## Step 4 — Add AI Match Feedback

### Goal

Generate short feedback from existing match analysis results.

### Files

```text
backend/app/services/ai_feedback_service.py
```

### Input Allowed

```json
{
  "target_role": "Frontend Developer",
  "match_score": 72,
  "matched_skills": ["React", "TypeScript", "REST APIs"],
  "missing_skills": ["Testing", "Next.js App Router"],
  "job_keywords": ["React", "Next.js", "CI/CD"]
}
```

### Tasks

- Send only sanitized structured match data
- Do not send full resume text
- Generate one short summary
- Generate up to three improvement tips
- Store generated feedback with the analysis result
- Return saved feedback if it already exists

### Success Criteria

- AI does not calculate the score
- Full CV content is never sent
- Repeated requests reuse saved output
- Match analysis works without AI

---

## Step 5 — Add AI Interview Questions

### Goal

Generate a small set of tailored interview questions.

### Files

```text
backend/app/services/interview_ai_service.py
```

### Input Allowed

```json
{
  "target_role": "Frontend Developer",
  "matched_skills": ["React", "TypeScript", "REST APIs"],
  "missing_skills": ["Testing", "Next.js App Router"],
  "experience_level": "junior"
}
```

### Tasks

- Generate 3 technical questions
- Generate 2 behavioral questions
- Store generated questions with the interview session
- Return saved questions if they already exist
- Fall back to hardcoded question bank when AI is unavailable

### Success Criteria

- Interview prep works without AI
- AI questions are optional
- Full resume text is not sent
- Repeated requests do not create repeated API calls

---

## Step 6 — Add Frontend Actions and Documentation

### Goal

Expose AI as controlled user actions, not user settings.

### Frontend Actions

Allowed buttons:

```text
Generate AI Feedback
Generate AI Interview Questions
```

### Tasks

- Add buttons only where AI output is useful
- Do not trigger AI automatically
- Show loading state
- Show disabled or limit-reached state
- Display saved AI output when available
- Update README with AI setup
- Update ARCHITECTURE.md with AI flow and boundaries

### Success Criteria

- User can trigger AI only when backend allows it
- User cannot enable, disable, or choose AI provider/model
- AI key is documented as backend-only
- Documentation explains free model usage and cost boundaries

---

## Final Success Criteria

Milestone 11 is complete when:

- OpenRouter `/free` is configured through backend environment variables
- AI match feedback works from sanitized data
- AI interview questions work from sanitized data
- AI calls are manually triggered
- AI output is stored and reused
- full resume text is never sent to AI
- demo mode does not use live AI
- app-side usage limits exist
- app works with `AI_ENABLED=false`
- frontend never exposes the OpenRouter API key

---

## Portfolio Explanation

Career Copilot integrates AI as a controlled enhancement layer. The backend first performs deterministic matching and interview preparation using application logic. AI is then optionally used through OpenRouter `/free` to generate concise feedback and tailored questions from sanitized structured data. The user cannot choose the provider or model. AI is backend-controlled, usage-limited, cached, disabled for demo mode by default, and safe to turn off completely.
