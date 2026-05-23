# Career Copilot

A recruiter-focused full-stack SaaS application that helps job seekers manage applications, analyze resume-job fit, and prepare for interviews.

The project is designed to demonstrate strong software engineering fundamentals across frontend development, backend architecture, database design, authentication, testing, deployment, and documentation.

---

## Goals

This project is being built to showcase:

- React fundamentals
- Next.js App Router
- TypeScript
- SCSS architecture
- FastAPI backend development
- Firebase Authentication
- Firestore data modeling
- Firebase Storage
- REST API design
- Service-layer architecture
- Testing strategy
- System design and documentation

---

## Features

### Authentication

- Firebase Authentication
- Protected routes
- User profiles

### Application Tracker

- Create applications
- View and filter applications by status
- Edit application details and status
- Delete applications with confirmation
- Store user-owned application data in Firestore

### Resume Management

- Upload resumes
- Resume versioning
- Resume parsing

### Job Match Analysis

- Resume-to-job matching
- Missing skill detection
- Resume improvement suggestions

### Interview Preparation

- Interview question generation
- Saved practice sessions

### Analytics Dashboard

- Application statistics
- Response rate tracking
- Job search insights

### Demo Mode

- Pre-seeded demo account
- Recruiter-friendly walkthrough experience

---

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- SCSS Modules

### Backend

- FastAPI
- Pydantic
- Python

### Infrastructure

- Firebase Auth
- Firestore
- Firebase Storage

### Deployment

- Vercel (Frontend)
- Render (Backend)

### Testing

#### Frontend

- Vitest
- React Testing Library
- Playwright

#### Backend

- Pytest

---

## Architecture

High-level architecture:

```text
User
  ↓
Next.js Frontend
  ↓
Firebase Authentication
  ↓
FastAPI Backend
  ↓
Firestore + Firebase Storage
```

Business logic lives inside backend services.

Frontend is responsible for:

- UI
- Forms
- Routing
- Authentication state

Backend is responsible for:

- Business logic
- Resume analysis
- Data validation
- Analytics

---

## Project Structure

```text
CARRER-COPILOT/
│
├── frontend/
├── backend/
├── docs/
│
├── README.md
├── ARCHITECTURE.md
├── ROADMAP.md
└── .gitignore
```

---

## Development Principles

- TypeScript everywhere on the frontend
- SCSS Modules only
- Service-layer architecture
- Thin API routes
- Strong typing
- Incremental development
- Documentation-first approach

---

## Local Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on:

```text
http://localhost:3000
```

### Backend

```bash
cd backend

# activate virtual environment

uvicorn app.main:app --reload --port 8000
```

Runs on:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Documentation

Additional documentation can be found in:

```text
docs/
```

Including:

- Architecture decisions
- API contracts
- Database schema
- Deployment notes
- Development standards


---

## Status

🚧 Active Development

This project is currently being built incrementally with a focus on maintainable architecture, testing, and production-quality engineering practices.
