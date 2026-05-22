# Milestone 5 — Application Tracker

## Status

🚧 Not Started

---

## Objective

Build the first real product feature for Career Copilot: a job application tracker.

At the end of this milestone, authenticated users should be able to:

- Create job applications
- View their applications
- Update application details
- Update application status
- Delete applications
- Filter applications by status

All application data must belong to the authenticated user.

---

## Business Context

Career Copilot helps job seekers manage their job search.

The application tracker is the core foundation for future features such as:

- Resume-job matching
- Interview preparation
- Analytics
- Follow-up reminders
- Demo account activity

This milestone turns the project from infrastructure into a real SaaS product.

---

## Scope

### Included

- Application data model
- Firestore collection structure
- Backend application schemas
- Backend CRUD endpoints
- Frontend application API client
- Application form
- Application list/table
- Status filters
- Edit flow
- Delete flow
- User-owned data

### Excluded

- Resume uploads
- Job match analysis
- Interview prep
- Analytics charts
- Notifications
- Email integration
- Demo usage limits

---

# Phase 5.1 — Application Domain Model

## Goal

Define the shape of a job application across frontend, backend, and database.

## Tasks

- [ ] Define application status values
- [ ] Define frontend TypeScript types
- [ ] Document Firestore data structure
- [ ] Decide required and optional fields

## Application Status Values

```txt
applied
interviewing
offer
rejected
withdrawn
```

## Recommended Fields

```txt
id
userId
company
role
status
location
jobUrl
salaryRange
notes
dateApplied
createdAt
updatedAt
```

## Frontend File

```txt
frontend/types/application.ts
```

## Suggested Types

```ts
export type ApplicationStatus =
  | "applied"
  | "interviewing"
  | "offer"
  | "rejected"
  | "withdrawn";

export interface JobApplication {
  id: string;
  userId: string;
  company: string;
  role: string;
  status: ApplicationStatus;
  location?: string;
  jobUrl?: string;
  salaryRange?: string;
  notes?: string;
  dateApplied?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateApplicationInput {
  company: string;
  role: string;
  status: ApplicationStatus;
  location?: string;
  jobUrl?: string;
  salaryRange?: string;
  notes?: string;
  dateApplied?: string;
}

export type UpdateApplicationInput = Partial<CreateApplicationInput>;
```

## Acceptance Criteria

- Application status enum/type exists
- Application TypeScript types exist
- Data model is documented
- No backend API yet
- No UI yet

## Commit Message

```bash
git commit -m "feat(applications): define application domain model"
```

---

# Phase 5.2 — Firestore Service Layer

## Goal

Create backend Firestore infrastructure for user-scoped application data.

## Firestore Collection Structure

```txt
users/{userId}/applications/{applicationId}
```

## Why This Structure

This keeps each user’s applications isolated under their Firebase UID.

Example:

```txt
users/
  abc123/
    applications/
      app001
      app002

  xyz789/
    applications/
      app003
```

## Tasks

- [ ] Install or confirm Firebase Admin Firestore support
- [ ] Create Firestore service
- [ ] Create application repository
- [ ] Scope all application queries by user ID
- [ ] Avoid cross-user access

## Backend Files

```txt
backend/app/services/firestore_service.py
backend/app/services/application_repository.py
```

## Acceptance Criteria

- Firestore client is available through service layer
- Application repository can target `users/{uid}/applications`
- No API routes yet
- No frontend changes yet

## Commit Message

```bash
git commit -m "feat(applications): add firestore repository layer"
```

---

# Phase 5.3 — Backend Application Schemas

## Goal

Define Pydantic schemas for application requests and responses.

## Tasks

- [ ] Create create request schema
- [ ] Create update request schema
- [ ] Create response schema
- [ ] Validate status values
- [ ] Validate required fields
- [ ] Support optional fields

## Backend File

```txt
backend/app/schemas/application.py
```

## Required Schemas

```txt
ApplicationStatus
CreateApplicationRequest
UpdateApplicationRequest
ApplicationResponse
```

## Validation Rules

- `company` is required
- `role` is required
- `status` must be valid
- `jobUrl` should be optional
- `notes` should be optional
- `dateApplied` should be optional

## Acceptance Criteria

- Pydantic schemas exist
- Invalid status values fail validation
- Required fields are enforced
- No routes yet

## Commit Message

```bash
git commit -m "feat(applications): add application schemas"
```

---

# Phase 5.4 — Backend CRUD API

## Goal

Create authenticated FastAPI endpoints for job applications.

## Endpoints

```txt
POST   /api/applications
GET    /api/applications
GET    /api/applications/{application_id}
PATCH  /api/applications/{application_id}
DELETE /api/applications/{application_id}
```

## Requirements

- All routes must require `get_current_user`
- All data must be scoped to `current_user["uid"]`
- Users cannot access another user's applications
- Routes should stay thin
- Business logic should live in repository/service layer

## Backend Files

```txt
backend/app/api/applications.py
backend/app/main.py
```

## Response Behavior

### Create

Returns created application.

### List

Returns all applications for the current user.

### Get One

Returns application if it belongs to current user.

### Update

Updates only current user's application.

### Delete

Deletes only current user's application.

## Acceptance Criteria

- CRUD endpoints exist
- Endpoints appear in `/docs`
- Endpoints require authentication
- Ownership is enforced
- No frontend UI yet

## Commit Message

```bash
git commit -m "feat(applications): implement application CRUD endpoints"
```

---

# Phase 5.5 — Frontend Application API Client

## Goal

Create frontend service functions for calling application endpoints.

## Tasks

- [ ] Create application API service
- [ ] Reuse authenticated API client from Milestone 4
- [ ] Add create method
- [ ] Add list method
- [ ] Add update method
- [ ] Add delete method
- [ ] Type all request and response payloads

## Frontend File

```txt
frontend/services/application-api.ts
```

## Required Methods

```ts
createApplication(input)
getApplications()
getApplicationById(id)
updateApplication(id, input)
deleteApplication(id)
```

## Acceptance Criteria

- Frontend has typed API methods
- API methods attach Firebase ID token
- No UI yet

## Commit Message

```bash
git commit -m "feat(applications): add frontend application api"
```

---

# Phase 5.6 — Application Form

## Goal

Allow users to create a job application from the UI.

## Route

```txt
/dashboard/applications/new
```

## Fields

```txt
Company
Role
Status
Location
Job URL
Salary Range
Date Applied
Notes
```

## Components

```txt
frontend/components/applications/ApplicationForm.tsx
frontend/components/applications/ApplicationForm.module.scss
```

## Requirements

- Use controlled form state
- Validate required fields
- Show loading state
- Show error state
- Submit through `createApplication`
- Redirect to `/dashboard/applications` after success
- Use SCSS Modules

## Acceptance Criteria

- User can submit application form
- Application is persisted through backend
- User is redirected after success
- Form handles errors

## Commit Message

```bash
git commit -m "feat(applications): add application creation form"
```

---

# Phase 5.7 — Application List and Filters

## Goal

Display user applications in a dashboard table.

## Route

```txt
/dashboard/applications
```

## Components

```txt
frontend/components/applications/ApplicationTable.tsx
frontend/components/applications/ApplicationTable.module.scss
frontend/components/applications/ApplicationRow.tsx
frontend/components/applications/StatusBadge.tsx
frontend/components/applications/ApplicationFilters.tsx
```

## Requirements

- Fetch applications for current user
- Show loading state
- Show empty state
- Show error state
- Display table/list
- Filter by status
- Sort newest first
- Link to create page

## Filters

```txt
All
Applied
Interviewing
Offer
Rejected
Withdrawn
```

## Acceptance Criteria

- Applications render in table/list
- Empty state appears if no data
- Status filters work
- Create button links to new application page

## Commit Message

```bash
git commit -m "feat(applications): add application list and filters"
```

---

# Phase 5.8 — Edit Application Flow

## Goal

Allow users to update existing applications.

## Options

Choose one:

```txt
Option A: Edit page
/dashboard/applications/{id}/edit

Option B: Edit modal
```

For this project, prefer:

```txt
Option A: Edit page
```

because it is easier to reason about and test.

## Tasks

- [ ] Create edit route
- [ ] Load existing application
- [ ] Reuse ApplicationForm
- [ ] Submit through `updateApplication`
- [ ] Redirect after success

## Route

```txt
/dashboard/applications/[id]/edit
```

## Acceptance Criteria

- User can edit application
- Existing values prefill form
- Updates persist
- User returns to application list after save

## Commit Message

```bash
git commit -m "feat(applications): add application edit flow"
```

---

# Phase 5.9 — Delete Application Flow

## Goal

Allow users to delete applications safely.

## Tasks

- [ ] Add delete action to application row
- [ ] Add confirmation UI
- [ ] Call `deleteApplication`
- [ ] Refresh list after deletion
- [ ] Prevent accidental deletion

## Requirements

- Show confirmation before delete
- Show loading state during delete
- Show error if delete fails

## Acceptance Criteria

- User can delete application
- User must confirm deletion
- Deleted application disappears from list
- Backend deletes only current user's application

## Commit Message

```bash
git commit -m "feat(applications): add application delete flow"
```

---

# Phase 5.10 — Milestone Polish

## Goal

Clean up and finalize the application tracker.

## Tasks

- [ ] Update ROADMAP.md
- [ ] Update README if needed
- [ ] Add manual test checklist
- [ ] Check `/docs` for backend routes
- [ ] Run frontend lint
- [ ] Run backend manually
- [ ] Verify auth protection
- [ ] Verify ownership behavior

## Manual Testing Checklist

- [ ] Create application
- [ ] View application list
- [ ] Filter by status
- [ ] Edit application
- [ ] Delete application
- [ ] Log out and verify dashboard protection
- [ ] Try API without token and confirm 401
- [ ] Confirm app data is scoped to current user

## Commit Message

```bash
git commit -m "chore(applications): finalize application tracker milestone"
```

---

# Final Success Criteria

Milestone 5 is complete when:

- [ ] User can create a job application
- [ ] User can view their job applications
- [ ] User can update an application
- [ ] User can delete an application
- [ ] User can filter applications by status
- [ ] Application data is scoped to authenticated user
- [ ] Backend routes require valid Firebase token
- [ ] Backend routes appear in FastAPI docs
- [ ] Frontend UI is usable and styled consistently

---

# Component Tree After Milestone 5

```txt
DashboardApplicationsPage
└── ProtectedRoute
    └── AppShell
        ├── Sidebar
        ├── Header
        └── PageContainer
            ├── ApplicationFilters
            ├── ApplicationTable
            │   └── ApplicationRow[]
            │       ├── StatusBadge
            │       ├── EditLink
            │       └── DeleteButton
            └── EmptyState

NewApplicationPage
└── ProtectedRoute
    └── AppShell
        └── PageContainer
            └── ApplicationForm

EditApplicationPage
└── ProtectedRoute
    └── AppShell
        └── PageContainer
            └── ApplicationForm
```

---

# Backend Flow

```txt
Request
  ↓
FastAPI Route
  ↓
get_current_user
  ↓
Firebase Token Verification
  ↓
Application Repository
  ↓
Firestore users/{uid}/applications
  ↓
Response
```

---

# Frontend Flow

```txt
Application Page
  ↓
Application API Service
  ↓
Authenticated API Client
  ↓
Firebase ID Token
  ↓
FastAPI Endpoint
  ↓
Firestore
```

---

# Recommended Codex Workflow

Use this pattern for every phase:

```txt
Read:
- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-5-application-tracker.md

Implement Phase 5.X only.

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

➡️ Milestone 6 — Resume Management

Focus:

- Resume upload
- Firebase Storage
- Resume metadata
- Resume parsing