# Milestone 8 — Interview Preparation

## Status

🚧 Not Started

---

# Objective

Help users prepare for interviews using an existing Job Match Analysis.

The system should:

- Generate interview questions
- Group questions by category
- Allow users to save answers
- Store interview sessions
- Allow users to review previous sessions
- Allow users to delete interview sessions

This milestone builds directly on Milestone 7.

---

# Dependency

Required:

```txt
Milestone 6 completed
Milestone 7 completed
```

Users must have at least one completed Job Match Analysis before creating an interview session.

---

# Architecture

Interview preparation is generated from:

```txt
Resume
+
Job Description
+
Job Match Analysis
```

Milestone 8 remains deterministic.

No OpenAI.

No Claude.

No external AI providers.

Future AI enhancements can be added in a later milestone.

---

# Firestore Structure

```txt
users/{uid}/interviews/{sessionId}
```

---

# Interview Session Model

```txt
id
userId
analysisId
resumeId
resumeFileName
questions
answers
createdAt
updatedAt
```

---

# Question Categories

```txt
general
behavioral
technical
```

---

# Phase 8.1 — Interview Domain + Repository

## Goal

Create interview session models and persistence layer.

## Output Files

```txt
backend/app/schemas/interview.py
backend/app/services/interview_repository.py
```

## Repository Methods

```python
create_session()
get_session()
list_sessions()
update_answers()
delete_session()
```

## Firestore Path

```txt
users/{uid}/interviews/{sessionId}
```

## Requirements

- Create Pydantic schemas for interview sessions
- Create schemas for questions and answers
- Create Firestore repository
- Scope all reads/writes/deletes by authenticated user ID
- Do not expose cross-user data

## Success Criteria

- Interview schemas exist
- Repository exists
- Session CRUD operations work
- Answer update operation works
- User ownership is enforced

## Commit

```bash
git commit -m "feat(interview): add interview repository"
```

---

# Phase 8.2 — Question Generation Service

## Goal

Generate interview questions from analysis results.

## Output File

```txt
backend/app/services/interview_generator.py
```

## Inputs

```txt
Job Description
Matched Requirements
Missing Requirements
```

## Generated Output

```txt
5 General Questions
5 Behavioral Questions
5 Technical Questions
```

## Example Output

```txt
General
- Tell us about yourself.
- Why are you interested in this role?
- What makes you a strong candidate for this position?

Behavioral
- Describe a challenging project you worked on.
- Tell us about a time you handled conflict.
- Tell us about a time you had to learn something quickly.

Technical
- Explain your experience with React.
- Explain how you use CI/CD pipelines.
- How have you worked with PostgreSQL?
```

## Requirements

- Generate deterministic questions
- Use matched requirements for experience-based questions
- Use missing requirements for preparation-focused questions
- Group questions into general, behavioral, and technical categories
- Do not use AI APIs

## Success Criteria

- Questions are generated consistently
- Technical questions reflect job requirements
- Questions are grouped correctly
- Output is stable and testable

## Commit

```bash
git commit -m "feat(interview): add interview generator"
```

---

# Phase 8.3 — Interview API

## Goal

Create backend interview endpoints.

## Output Files

```txt
backend/app/api/interviews.py
backend/app/main.py
```

## Endpoints

```txt
POST   /api/interviews
GET    /api/interviews
GET    /api/interviews/{session_id}
PUT    /api/interviews/{session_id}/answers
DELETE /api/interviews/{session_id}
```

## Workflow

```txt
User selects analysis
↓
Backend verifies authenticated user
↓
Backend loads analysis from users/{uid}/analyses/{analysisId}
↓
Backend generates questions
↓
Backend saves interview session
↓
Backend returns session
```

## Requirements

- All routes require authentication
- Session creation requires an existing analysis
- Users cannot create sessions from another user's analysis
- Users cannot read another user's sessions
- Users cannot update another user's answers
- Users cannot delete another user's sessions
- Routes appear in FastAPI docs

## Success Criteria

- Session creation works
- Session retrieval works
- Session list works
- Answer saving works
- Session deletion works
- Ownership is enforced

## Commit

```bash
git commit -m "feat(interview): add interview api"
```

---

# Phase 8.4 — Frontend Interview Services

## Goal

Create frontend API layer.

## Output File

```txt
frontend/services/interview-api.ts
```

## Methods

```ts
createInterviewSession()
getInterviewSessions()
getInterviewSession()
saveInterviewAnswers()
deleteInterviewSession()
```

## Requirements

- Reuse authenticated API client
- Send Firebase ID token automatically
- Return typed responses
- Handle API errors clearly
- Do not build UI yet

## Success Criteria

- Frontend can create interview session
- Frontend can fetch sessions
- Frontend can fetch one session
- Frontend can save answers
- Frontend can delete session

## Commit

```bash
git commit -m "feat(interview): add frontend interview api"
```

---

# Phase 8.5 — Interview Practice UI

## Goal

Allow users to generate interview sessions and practice answers.

## Route

```txt
/dashboard/interview
```

## Output Files

```txt
frontend/app/dashboard/interview/page.tsx

frontend/components/interview/InterviewPage.tsx
frontend/components/interview/QuestionSection.tsx
frontend/components/interview/QuestionCard.tsx
frontend/components/interview/AnswerEditor.tsx

frontend/components/interview/InterviewPage.module.scss
frontend/components/interview/QuestionSection.module.scss
frontend/components/interview/QuestionCard.module.scss
frontend/components/interview/AnswerEditor.module.scss
```

## Features

```txt
Select Analysis
Generate Session
View Questions
Write Answers
Save Answers
```

## Display Sections

```txt
General Questions
Behavioral Questions
Technical Questions
```

## Requirements

- User can select a completed analysis
- User can generate an interview session
- Questions display grouped by category
- User can write answers
- User can save answers
- UI shows loading, empty, and error states
- UI follows existing app styling

## Success Criteria

- `/dashboard/interview` opens
- Analysis selector works
- Questions display correctly
- Answers are editable
- Save works
- Errors are displayed clearly
- No console errors

## Commit

```bash
git commit -m "feat(interview): add interview practice ui"
```

---

# Phase 8.6 — Interview History + Milestone Completion

## Goal

Allow users to review and manage previous interview sessions.

## Route

```txt
/dashboard/interview/history
```

## Output Files

```txt
frontend/app/dashboard/interview/history/page.tsx

frontend/components/interview/InterviewHistory.tsx
frontend/components/interview/InterviewHistoryCard.tsx
frontend/components/interview/DeleteInterviewButton.tsx

frontend/components/interview/InterviewHistory.module.scss
frontend/components/interview/InterviewHistoryCard.module.scss
frontend/components/interview/DeleteInterviewButton.module.scss
```

## Features

```txt
List Sessions
Open Session
Review Answers
Delete Session
```

## Requirements

- Show previous interview sessions
- Show resume file name
- Show session date
- Show question count
- Allow opening a saved session
- Allow deleting a session
- Require confirmation before delete
- Refresh list after delete
- Preserve saved answers after reload

## Verification Flow

```txt
Create Session
↓
Generate Questions
↓
Write Answers
↓
Save Answers
↓
Reload Page
↓
Answers Persist
↓
Open History
↓
Review Session
↓
Delete Session
↓
Confirm Session Removed
```

## Success Criteria

- History page is visible
- Previous sessions appear
- Answers persist
- Sessions are removable
- User ownership is enforced
- No console errors

## Commit

```bash
git commit -m "feat(interview): finalize interview preparation milestone"
```

---

# Milestone 8 Success Criteria

- [ ] User can generate interview questions
- [ ] Questions are grouped by category
- [ ] Technical questions reflect job requirements
- [ ] User can save answers
- [ ] User can edit answers
- [ ] User can review previous sessions
- [ ] User can delete sessions
- [ ] All data is user-scoped
- [ ] Protected routes work
- [ ] No console errors

---

# Backend Verification

- [ ] Interview endpoints appear in `/docs`
- [ ] Protected endpoints reject unauthenticated requests
- [ ] Users cannot access another user's sessions
- [ ] Users cannot create sessions from another user's analyses
- [ ] Answer updates are user-scoped
- [ ] Session deletion is user-scoped

---

# UI Verification

- [ ] Open `/dashboard/interview`
- [ ] Select analysis
- [ ] Generate interview session
- [ ] View grouped questions
- [ ] Write answers
- [ ] Save answers
- [ ] Reload page
- [ ] Confirm answers persist
- [ ] Open `/dashboard/interview/history`
- [ ] Review previous session
- [ ] Delete session
- [ ] Confirm deleted session does not reappear

---

# Codex Prompt Template

```txt
Read:

- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-8-interview-preparation.md

Implement Phase 8.X only.

Requirements:
- Follow existing repository pattern
- Follow existing API structure
- Follow existing Firestore structure
- Use TypeScript on frontend
- Use SCSS Modules only
- Do not use AI APIs
- Do not implement future phases

Before coding:
1. Explain plan
2. List files to create
3. List files to modify

After coding:
1. Explain changes
2. Explain how to test
3. Stop
```
