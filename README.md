# Career Copilot

Career Copilot is a recruiter-focused full-stack app for managing job applications, analyzing resume fit, and practicing interviews.

## Live App

Public deployment:

- https://career-copilot-ruddy.vercel.app/

## Demo Access

Use Demo Sign In on the login page to explore the app quickly.

## Core Features

- Authentication with protected routes
- Application tracking and status management
- Resume management and parsing
- Job match analysis with improvement suggestions
- Interview preparation and saved practice sessions
- Analytics dashboard for job search progress

## Tech Stack

- Frontend: Next.js, React, TypeScript, SCSS Modules
- Backend: FastAPI, Pydantic, Python
- Infrastructure: Firebase Auth, Firestore, Firebase Storage
- Deployment: Vercel (frontend), Render (backend)

## Run Locally

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## Documentation

See docs/ for architecture, roadmap, and development standards.
