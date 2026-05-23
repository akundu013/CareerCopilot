# Project Milestones

## Project: Career Copilot

A full-stack SaaS-style portfolio project built with Next.js, React, TypeScript, SCSS Modules, FastAPI, and Firebase.

---

## Milestone 1 — Project Foundation

### Goal

Set up the base monorepo and confirm that both frontend and backend run locally.

### Tasks

- [x] Create project root
- [x] Create Next.js frontend
- [x] Create FastAPI backend
- [x] Add root documentation
- [x] Add `.gitignore`
- [x] Run frontend locally
- [x] Run backend locally
- [ ] Make first Git commit

### Success Criteria

- Frontend runs at `http://localhost:3000`
- Backend runs at `http://localhost:8000`
- FastAPI docs work at `http://localhost:8000/docs`

---

## Milestone 2 — Frontend App Shell

### Goal

Create the first professional-looking SaaS interface structure.

### Tasks

- [x] Create global SCSS setup
- [x] Create SCSS variables
- [x] Create reusable layout components
- [x] Create reusable UI components
- [x] Create landing page
- [x] Create dashboard route
- [x] Add basic navigation

### Success Criteria

- `/` renders a clean landing page
- `/dashboard` renders a dashboard shell
- Styling uses SCSS Modules
- No Firebase or business logic yet

---

## Milestone 3 — Firebase Authentication

### Goal

Add real authentication and protected routes.

### Tasks

- [ ] Create Firebase project
- [ ] Add Firebase client config
- [ ] Create auth service
- [ ] Create auth provider
- [ ] Create login page
- [ ] Create signup page
- [ ] Add logout flow
- [ ] Protect dashboard routes
- [ ] Create demo account

### Success Criteria

- User can sign up
- User can log in
- User can log out
- Dashboard requires authentication
- Demo account works

---

## Milestone 4 — Backend Auth Verification

### Goal

Connect frontend authentication to backend authorization.

### Tasks

- [ ] Add Firebase Admin SDK to backend
- [ ] Verify Firebase ID tokens
- [ ] Create auth dependency
- [ ] Add protected test endpoint
- [ ] Connect frontend API client with auth token

### Success Criteria

- Backend rejects unauthenticated requests
- Backend accepts valid Firebase users
- Frontend can call protected backend routes

---

## Milestone 5 — Application Tracker

### Goal

Build the first real product feature.

### Tasks

- [x] Design application data model
- [x] Create Firestore collection structure
- [x] Create application TypeScript types
- [x] Create FastAPI application schemas
- [x] Create application CRUD endpoints
- [x] Create application form
- [x] Create application list/table
- [x] Add status filters
- [x] Add edit functionality
- [x] Add delete functionality

### Success Criteria

- User can create a job application
- User can view applications
- User can update application status
- User can delete application
- Data is associated with authenticated user

---

## Milestone 6 — Resume Management

### Goal

Allow users to upload and manage resumes.

### Tasks

- [ ] Add Firebase Storage setup
- [ ] Create resume upload UI
- [ ] Store resume metadata
- [ ] Create resume list page
- [ ] Add backend resume parsing service
- [ ] Extract text from uploaded resumes
- [ ] Store parsed resume text

### Success Criteria

- User can upload a resume
- Resume file is stored
- Resume metadata is saved
- Backend can parse resume text

---

## Milestone 7 — Job Match Analysis

### Goal

Build the core portfolio feature: resume-to-job matching.

### Tasks

- [ ] Create job description input form
- [ ] Create match engine service
- [ ] Compare resume skills to job description
- [ ] Generate match score
- [ ] Detect missing skills
- [ ] Generate improvement suggestions
- [ ] Save analysis result
- [ ] Display analysis history

### Success Criteria

- User can select a resume
- User can paste a job description
- App returns match score
- App shows matched skills
- App shows missing skills
- App shows suggested improvements

---

## Milestone 8 — Interview Preparation

### Goal

Help users prepare for interviews based on the role and job description.

### Tasks

- [ ] Create interview preparation page
- [ ] Generate role-based questions
- [ ] Generate behavioral questions
- [ ] Generate technical questions
- [ ] Allow users to save answers
- [ ] Store interview sessions

### Success Criteria

- User can generate interview questions
- User can save practice answers
- User can review previous sessions

---

## Milestone 9 — Analytics Dashboard

### Goal

Create a recruiter-impressive dashboard with useful insights.

### Tasks

- [ ] Show applications by status
- [ ] Show response rate
- [ ] Show weekly application activity
- [ ] Show top missing skills
- [ ] Add charts
- [ ] Add summary cards

### Success Criteria

- Dashboard gives useful job search insights
- Charts render correctly
- Analytics are based on user data

---

## Milestone 10 — Demo Mode

### Goal

Create a recruiter-friendly demo experience.

### Tasks

- [ ] Seed demo applications
- [ ] Seed demo resumes
- [ ] Seed demo analyses
- [ ] Seed demo interview sessions
- [ ] Add demo login button
- [ ] Prevent destructive demo actions
- [ ] Add demo reset strategy

### Success Criteria

- Recruiters can explore without setup
- Demo account looks populated
- Demo data is safe from accidental deletion

---

## Milestone 11 — Testing

### Goal

Add professional test coverage.

### Tasks

- [ ] Add backend unit tests
- [ ] Test match engine
- [ ] Test analytics service
- [ ] Test FastAPI endpoints
- [ ] Add frontend component tests
- [ ] Add form validation tests
- [ ] Add Playwright E2E tests

### Success Criteria

- Core backend logic is tested
- Main user flow is tested
- Tests can run from terminal

---

## Milestone 12 — Deployment

### Goal

Deploy the full application.

### Tasks

- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render
- [ ] Add production environment variables
- [ ] Configure CORS for production
- [ ] Verify Firebase production setup
- [ ] Test deployed demo account

### Success Criteria

- Frontend has public URL
- Backend has public URL
- Demo account works in production
- README includes live demo link

---

## Milestone 13 — Portfolio Polish

### Goal

Make the project recruiter-ready.

### Tasks

- [ ] Improve UI polish
- [ ] Add loading states
- [ ] Add error states
- [ ] Add empty states
- [ ] Add architecture diagram
- [ ] Improve README
- [ ] Add screenshots
- [ ] Record demo video
- [ ] Final code cleanup

### Success Criteria

- GitHub repository looks professional
- Live demo works
- README explains architecture clearly
- Project can be discussed confidently in interviews

---

## Current Status

```text
Current Milestone: Milestone 5 — Application Tracker complete
Next Milestone: Milestone 6 — Resume Management
```
