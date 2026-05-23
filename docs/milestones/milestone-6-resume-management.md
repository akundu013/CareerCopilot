# Milestone 6 — Resume Management

## Status

🚧 Not Started

---

## Objective

Allow authenticated users to upload, store, view, and parse resumes.

At the end of this milestone, users should be able to:

- Upload a resume file
- Store the file in Firebase Storage
- Save resume metadata in Firestore
- View uploaded resumes
- Parse resume text through the FastAPI backend
- Store parsed resume text for future job matching

---

## Business Context

Resume management is the foundation for Career Copilot’s core AI-style feature: resume-to-job matching.

Before the app can analyze a user’s fit for a job posting, it needs access to:

- The uploaded resume file
- Resume metadata
- Extracted resume text

This milestone prepares the system for Milestone 7 — Job Match Analysis.

---

## Scope

### Included

- Firebase Storage setup
- Resume upload UI
- Resume metadata model
- Resume list page
- Backend resume parsing service
- Parsed text extraction
- Parsed text storage
- User-scoped resume data

### Excluded

- AI job matching
- Resume rewriting
- Cover letter generation
- Multiple resume comparison
- PDF preview
- Resume version diffing
- Payment limits
- Demo quota enforcement

---

# Phase 6.1 — Resume Domain Model

## Goal

Define the resume data model across frontend, backend, and Firestore.

## Tasks

- [ ] Define resume TypeScript types
- [ ] Define resume status values
- [ ] Document Firebase Storage path
- [ ] Document Firestore structure

## Resume Status Values

```txt
uploaded
parsed
parse_failed
```

## Firestore Structure

```txt
users/{uid}/resumes/{resumeId}
```

## Firebase Storage Path

```txt
users/{uid}/resumes/{resumeId}/{fileName}
```

## Recommended Fields

```txt
id
userId
fileName
fileUrl
storagePath
contentType
sizeBytes
status
parsedText
createdAt
updatedAt
```

## Frontend File

```txt
frontend/types/resume.ts
```

## Acceptance Criteria

- Resume TypeScript types exist
- Storage path strategy is documented
- Firestore structure is documented
- No upload UI yet
- No backend parsing yet

## Commit Message

```bash
git commit -m "feat(resumes): define resume domain model"
```

---

# Phase 6.2 — Firebase Storage Setup

## Goal

Enable Firebase Storage and configure frontend access.

## Console Setup

In Firebase Console:

```txt
Build → Storage → Get Started
```

Choose:

```txt
Production Mode
```

Use the same region family as Firestore when possible.

## Tasks

- [ ] Enable Firebase Storage
- [ ] Confirm frontend Firebase config includes storage bucket
- [ ] Export Firebase Storage instance from `firebase.ts`
- [ ] Update `.env.example` if needed

## Frontend File

```txt
frontend/services/firebase.ts
```

## Acceptance Criteria

- Firebase Storage is enabled
- Frontend exports `storage`
- App still runs without errors

## Commit Message

```bash
git commit -m "feat(resumes): configure firebase storage"
```

---

# Phase 6.3 — Resume Metadata Backend Schemas

## Goal

Define Pydantic schemas for resume metadata.

## Tasks

- [ ] Create resume status enum
- [ ] Create create metadata request schema
- [ ] Create update metadata request schema
- [ ] Create resume response schema

## Backend File

```txt
backend/app/schemas/resume.py
```

## Required Schemas

```txt
ResumeStatus
CreateResumeRequest
UpdateResumeRequest
ResumeResponse
```

## Acceptance Criteria

- Pydantic schemas exist
- Status values are validated
- Required metadata fields are enforced

## Commit Message

```bash
git commit -m "feat(resumes): add resume schemas"
```

---

# Phase 6.4 — Resume Repository Layer

## Goal

Create backend Firestore repository for user-scoped resume metadata.

## Firestore Structure

```txt
users/{uid}/resumes/{resumeId}
```

## Tasks

- [ ] Create resume repository
- [ ] Create metadata save method
- [ ] Create list resumes method
- [ ] Create get resume by id method
- [ ] Create update resume method
- [ ] Scope all operations by authenticated UID

## Backend File

```txt
backend/app/services/resume_repository.py
```

## Acceptance Criteria

- Resume metadata can be saved
- Resumes are scoped to current user
- Repository does not expose cross-user data

## Commit Message

```bash
git commit -m "feat(resumes): add resume repository layer"
```

---

# Phase 6.5 — Resume Metadata API

## Goal

Create authenticated backend endpoints for resume metadata.

## Endpoints

```txt
POST   /api/resumes
GET    /api/resumes
GET    /api/resumes/{resume_id}
PATCH  /api/resumes/{resume_id}
DELETE /api/resumes/{resume_id}
```

## Requirements

- All routes require `get_current_user`
- Routes use resume repository
- Routes only access current user’s resumes
- Routes appear in FastAPI docs

## Backend Files

```txt
backend/app/api/resumes.py
backend/app/main.py
```

## Acceptance Criteria

- Resume metadata endpoints exist
- Endpoints require authentication
- Endpoints are visible at `/docs`

## Commit Message

```bash
git commit -m "feat(resumes): add resume metadata api"
```

---

# Phase 6.6 — Frontend Resume API Client

## Goal

Create frontend service functions for resume metadata APIs.

## Tasks

- [ ] Create resume API service
- [ ] Reuse authenticated API client
- [ ] Add create resume metadata method
- [ ] Add list resumes method
- [ ] Add get resume method
- [ ] Add update resume method
- [ ] Add delete resume method

## Frontend File

```txt
frontend/services/resume-api.ts
```

## Required Methods

```ts
createResumeMetadata(input)
getResumes()
getResumeById(id)
updateResume(id, input)
deleteResume(id)
```

## Acceptance Criteria

- Frontend can call resume metadata endpoints
- Firebase ID token is sent automatically
- No upload UI yet

## Commit Message

```bash
git commit -m "feat(resumes): add frontend resume api"
```

---

# Phase 6.7 — Resume Upload UI

## Goal

Allow users to upload a resume file from the UI.

## Route

```txt
/dashboard/resumes
```

## Components

```txt
frontend/components/resumes/ResumeUploader.tsx
frontend/components/resumes/ResumeUploader.module.scss
```

## Supported File Types

```txt
PDF
DOCX
TXT
```

## Requirements

- File input
- File type validation
- File size validation
- Upload progress state
- Error state
- Success state
- Upload file to Firebase Storage
- Save resume metadata through backend API

## Suggested File Size Limit

```txt
5 MB
```

## Upload Flow

```txt
User selects file
  ↓
Frontend validates file
  ↓
Frontend uploads file to Firebase Storage
  ↓
Frontend gets storage path / download URL
  ↓
Frontend calls FastAPI to save metadata
  ↓
Resume appears in resume list
```

## Acceptance Criteria

- User can upload a resume
- File appears in Firebase Storage
- Metadata appears in Firestore
- UI shows success/error states

## Commit Message

```bash
git commit -m "feat(resumes): add resume upload ui"
```

---

# Phase 6.8 — Resume List Page

## Goal

Display uploaded resumes.

## Route

```txt
/dashboard/resumes
```

## Components

```txt
frontend/components/resumes/ResumeList.tsx
frontend/components/resumes/ResumeCard.tsx
frontend/components/resumes/ResumeStatusBadge.tsx
```

## Requirements

- Fetch resumes for current user
- Show loading state
- Show empty state
- Show error state
- Show file name
- Show status
- Show upload date
- Show parse status

## Acceptance Criteria

- Uploaded resumes appear in list
- Empty state appears when user has no resumes
- UI is consistent with app shell

## Commit Message

```bash
git commit -m "feat(resumes): add resume list page"
```

---

# Phase 6.9 — Backend Resume Parsing Service

## Goal

Extract text from uploaded resumes.

## Supported Parsing

```txt
PDF
DOCX
TXT
```

## Backend Dependencies

Recommended:

```txt
pypdf
python-docx
```

## Install

```bash
cd backend
pip install pypdf python-docx
pip freeze > requirements.txt
```

## Backend File

```txt
backend/app/services/resume_parser.py
```

## Required Methods

```python
parse_resume_file(file_bytes, content_type)
parse_pdf(file_bytes)
parse_docx(file_bytes)
parse_txt(file_bytes)
```

## Acceptance Criteria

- PDF text can be extracted
- DOCX text can be extracted
- TXT text can be extracted
- Unsupported files fail cleanly

## Commit Message

```bash
git commit -m "feat(resumes): add resume parsing service"
```

---

# Phase 6.10 — Resume Parse API

## Goal

Allow backend to parse uploaded resume files.

## Endpoint

```txt
POST /api/resumes/{resume_id}/parse
```

## Requirements

- Endpoint requires authentication
- Endpoint loads resume metadata
- Endpoint downloads file from Firebase Storage or accepts file upload depending on implementation
- Endpoint parses file text
- Endpoint updates resume document:
  - status: parsed
  - parsedText
  - updatedAt
- If parsing fails:
  - status: parse_failed

## Backend Files

```txt
backend/app/api/resumes.py
backend/app/services/resume_parser.py
backend/app/services/resume_repository.py
```

## Acceptance Criteria

- Resume can be parsed from backend
- Parsed text is saved to Firestore
- Parse failures are handled gracefully

## Commit Message

```bash
git commit -m "feat(resumes): add resume parse endpoint"
```

---

# Phase 6.11 — Frontend Parse Action

## Goal

Allow user to trigger resume parsing from the UI.

## Tasks

- [ ] Add parse button to ResumeCard
- [ ] Call parse endpoint
- [ ] Show parsing state
- [ ] Show parsed status after success
- [ ] Refresh resume list

## Frontend Files

```txt
frontend/components/resumes/ResumeCard.tsx
frontend/services/resume-api.ts
```

## Acceptance Criteria

- User can click Parse Resume
- UI shows loading state
- Resume status updates to parsed
- Parse failures show error message

## Commit Message

```bash
git commit -m "feat(resumes): add frontend parse action"
```

---

# Phase 6.12 — Milestone Polish and UI Verification

## Goal

Verify the full resume management flow.

## End-of-Milestone UI Check

- [ ] User can open `/dashboard/resumes`
- [ ] User can upload a resume
- [ ] Invalid file types are rejected
- [ ] Oversized files are rejected
- [ ] Uploaded file appears in Firebase Storage
- [ ] Resume metadata appears in Firestore
- [ ] Resume list updates after upload
- [ ] User can trigger parsing
- [ ] Resume status changes to parsed
- [ ] Parsed text is stored in Firestore
- [ ] No console errors
- [ ] No broken navigation links
- [ ] UI matches existing app style

## Backend Verification

- [ ] Resume endpoints appear in `/docs`
- [ ] Protected endpoints reject unauthenticated requests
- [ ] Resume metadata is scoped to current user
- [ ] Parser handles PDF/DOCX/TXT
- [ ] Parser fails gracefully for unsupported files

## Commit Message

```bash
git commit -m "chore(resumes): finalize resume management milestone"
```

---

# Final Success Criteria

Milestone 6 is complete when:

- [ ] User can upload a resume
- [ ] Resume file is stored in Firebase Storage
- [ ] Resume metadata is saved in Firestore
- [ ] User can view uploaded resumes
- [ ] Backend can parse resume text
- [ ] Parsed text is saved to Firestore
- [ ] UI flow works end-to-end

---

# Component Tree After Milestone 6

```txt
ResumesPage
└── ProtectedRoute
    └── AppShell
        └── PageContainer
            ├── ResumeUploader
            └── ResumeList
                └── ResumeCard[]
                    ├── ResumeStatusBadge
                    ├── ParseResumeButton
                    └── DeleteResumeButton
```

---

# Backend Flow

```txt
Upload Metadata Request
  ↓
FastAPI Resume API
  ↓
get_current_user
  ↓
Resume Repository
  ↓
Firestore users/{uid}/resumes

Parse Resume Request
  ↓
FastAPI Resume API
  ↓
get_current_user
  ↓
Resume Repository
  ↓
Firebase Storage File
  ↓
Resume Parser Service
  ↓
Parsed Text
  ↓
Firestore users/{uid}/resumes/{resumeId}
```

---

# Frontend Flow

```txt
User selects resume
  ↓
Frontend validates file
  ↓
Firebase Storage upload
  ↓
Frontend sends metadata to FastAPI
  ↓
FastAPI saves metadata in Firestore
  ↓
Resume list refreshes
  ↓
User clicks Parse
  ↓
FastAPI extracts text
  ↓
Firestore stores parsed text
```

---

# Recommended Codex Workflow

Use this pattern for every phase:

```txt
Read:
- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-6-resume-management.md

Implement Phase 6.X only.

Do not implement future phases.

Before coding:
1. List files to create
2. List files to modify
3. Explain the plan

After coding:
1. Explain what changed
2. Explain how to test
3. Stop and wait for review
```

---

# Next Milestone

➡️ Milestone 7 — Job Match Analysis

Focus:

- Select resume
- Paste job description
- Compare resume text to job description
- Generate match score
- Show missing skills
- Save analysis result