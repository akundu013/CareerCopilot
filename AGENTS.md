# AGENTS.md

## Project

Career Copilot

A recruiter-quality full-stack SaaS portfolio project for job search management, resume analysis, and interview preparation.

---

## Tech Stack

### Frontend

- Next.js App Router
- React
- TypeScript
- SCSS Modules
- Firebase Client SDK

### Backend

- FastAPI
- Python
- Pydantic
- Firebase Admin SDK

### Infrastructure

- Firebase Auth
- Firestore
- Firebase Storage
- Vercel
- Render

---

## Core Rules

- Work incrementally by milestone.
- Do not implement future milestones early.
- Explain files before creating or modifying them.
- Keep frontend and backend separated.
- Prefer clarity over cleverness.
- Do not add unnecessary libraries.
- Do not hardcode secrets.
- Do not commit `.env`, `.env.local`, service account JSON, or private keys.

---

## Frontend Rules

- Use TypeScript.
- Use Next.js App Router.
- Use SCSS Modules only.
- Do not use Tailwind.
- Do not use styled-components.
- Do not use inline styles except for unavoidable dynamic values.
- Use `@/*` import aliases.
- Keep pages thin.
- Put reusable UI in `components/`.
- Put Firebase/browser service logic in `services/`.
- Put shared types in `types/`.
- Put reusable hooks in `hooks/`.

### Frontend Structure

```txt
frontend/
├── app/
├── components/
├── hooks/
├── services/
├── styles/
└── types/
```

---

## Backend Rules

- Use FastAPI.
- Use Pydantic schemas for request/response models.
- Keep routes thin.
- Put business logic in `app/services/`.
- Put reusable dependencies/utilities in `app/utils/` or `app/dependencies.py`.
- Use FastAPI dependency injection.
- Do not place Firebase Admin logic directly inside route handlers.

### Backend Structure

```txt
backend/
├── app/
│   ├── api/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── dependencies.py
│   └── main.py
└── tests/
```

---

## Authentication Rules

- Frontend uses Firebase Client SDK.
- Backend uses Firebase Admin SDK.
- Frontend sends Firebase ID token as:

```txt
Authorization: Bearer <token>
```

- Backend verifies the token before protected endpoints.
- Demo credentials must come from environment variables.
- Do not hardcode demo passwords.

---

## Styling Rules

- Use SCSS partials for shared styles.
- Use SCSS Modules for components.
- Keep styles colocated with components.

Example:

```txt
Button.tsx
Button.module.scss
```

Global styles live in:

```txt
frontend/styles/
```

---

## Git Rules

Before committing:

1. Determine the active milestone.
2. Confirm changed files belong to that milestone.
3. Show included files.
4. Show excluded files.
5. Wait for approval before committing or pushing.

Use meaningful commit messages.

Examples:

```bash
chore: initialize project foundation
feat(frontend): implement app shell and UI foundation
feat(auth): configure firebase client
feat(auth): add authentication service layer
feat(api): verify firebase auth tokens
```

---

## Testing Rules

Frontend:

- Vitest
- React Testing Library
- Playwright for core flows

Backend:

- Pytest
- FastAPI TestClient

Prioritize testing:

- Auth utilities
- Backend services
- API endpoints
- Critical user flows

---

## Documentation Rules

Update documentation when architecture changes.

Important docs:

```txt
README.md
ROADMAP.md
ARCHITECTURE.md
docs/milestones/
docs/development-standards.md
```

---

## Cost Constraint

Keep the project runnable for approximately $0–$5/month.

Prefer:

- Vercel free tier
- Render free tier
- Firebase Spark/low Blaze usage
- Mock or cached AI responses where possible

---

## Current Development Style

This project is built step-by-step.

Do not generate the whole application at once.

For every implementation task:

1. Read the relevant milestone document.
2. List files to create.
3. List files to modify.
4. Explain the plan.
5. Implement only the requested phase.
6. Explain how to test it.
7. Stop and wait for review.