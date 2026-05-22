You are helping me build a recruiter-quality full-stack SaaS project.

Project Name:
Career Copilot

Goal:
Build a portfolio-quality application that demonstrates strong understanding of:

- React
- Next.js App Router
- TypeScript
- SCSS Modules
- FastAPI
- Firebase Auth
- Firestore
- Firebase Storage
- API Design
- Database Modeling
- Testing
- System Architecture

This project is intended to impress software engineering recruiters.

Important:
Do NOT generate the entire application at once.

Work incrementally.

For every task:
1. Explain the goal.
2. Explain the architecture decision.
3. List files that will be created or modified.
4. Generate only the code required for the current task.
5. Explain how the code works.
6. Wait for the next instruction.

--------------------------------------------------
CURRENT PROJECT STRUCTURE
--------------------------------------------------

CARRER-COPILOT/
│
├── backend/
├── docs/
├── frontend/
│
├── .gitignore
├── README.md
├── ARCHITECTURE.md
└── AGENTS.md

Frontend was created using:

- Next.js
- TypeScript
- App Router
- React Compiler
- ESLint
- Turbopack

Styling:
- SCSS Modules only

Do NOT use:
- Tailwind
- Styled Components
- Emotion

--------------------------------------------------
ARCHITECTURE PRINCIPLES
--------------------------------------------------

Frontend responsibilities:

- UI
- Forms
- Authentication state
- Dashboard
- Charts
- Routing

Backend responsibilities:

- Business logic
- Resume parsing
- Match scoring
- Analytics
- Data validation

Routes should be thin.

Business logic belongs inside services.

--------------------------------------------------
FRONTEND STANDARDS
--------------------------------------------------

Use:

@/* import aliases

Example:

import { Button } from "@/components/Button";

Component structure:

components/
hooks/
services/
types/
styles/

Keep components small.

Prefer:

- reusable components
- custom hooks
- feature organization

Use TypeScript everywhere.

--------------------------------------------------
BACKEND STANDARDS
--------------------------------------------------

FastAPI

Structure:

app/
│
├── api/
├── services/
├── schemas/
├── utils/
└── main.py

Routes should:

- validate input
- call services
- return responses

Business logic belongs in:

app/services

All request/response models must use Pydantic.

--------------------------------------------------
DATABASE
--------------------------------------------------

Firebase Firestore

Collections:

users
applications
resumes
analyses
interview_sessions

Design schemas before implementation.

--------------------------------------------------
AUTHENTICATION
--------------------------------------------------

Firebase Auth

Frontend:
- login
- logout
- auth provider

Backend:
- verify Firebase JWT
- protected endpoints

--------------------------------------------------
TESTING
--------------------------------------------------

Frontend:
- Vitest
- React Testing Library
- Playwright

Backend:
- Pytest

Focus testing on:

- business logic
- API endpoints
- critical user flows

--------------------------------------------------
HOSTING
--------------------------------------------------

Frontend:
Vercel

Backend:
Render

Database:
Firebase

Target monthly cost:
Under $5

--------------------------------------------------
PROJECT FEATURES
--------------------------------------------------

Phase 1

- Authentication
- Dashboard shell
- Application tracker

Phase 2

- Resume uploads
- Firebase Storage

Phase 3

- Resume parsing
- Job description analysis
- Match scoring

Phase 4

- Interview preparation

Phase 5

- Analytics dashboard

--------------------------------------------------
DEMO ACCOUNT
--------------------------------------------------

Application should include:

demo@carrercopilot.dev

with seeded data.

The demo account should allow recruiters to explore the product immediately.

--------------------------------------------------
CODE GENERATION RULES
--------------------------------------------------

Never create unnecessary abstractions.

Prefer clarity over cleverness.

Always explain:

- why the code exists
- where it fits in the architecture
- how it interacts with the rest of the system

If a better architecture choice exists, explain the tradeoff before generating code.
