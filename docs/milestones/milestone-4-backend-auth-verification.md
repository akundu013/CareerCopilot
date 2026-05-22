# Milestone 4 — Backend Auth Verification

## Status

🚧 Not Started

---

## Objective

Connect Firebase frontend authentication to FastAPI backend authorization.

At the end of this milestone:

- Frontend users authenticate with Firebase.
- Frontend sends Firebase ID tokens to FastAPI.
- FastAPI verifies tokens using Firebase Admin SDK.
- Protected endpoints reject unauthenticated users.
- Protected endpoints know the authenticated user's identity.

---

## Business Context

Career Copilot stores user-specific data:

- Applications
- Resumes
- Interview sessions
- Analytics

The backend must verify user identity before accessing or modifying any user data.

This milestone establishes the security foundation for all future backend features.

---

## Scope

### Included

- Firebase Admin SDK
- Firebase service account configuration
- Token verification
- FastAPI auth dependency
- Protected test endpoint
- Frontend API token forwarding

### Excluded

- Firestore CRUD
- Resume uploads
- Analytics
- Role-based permissions
- Team accounts
- Admin dashboards

---

# Phase 4.1 — Firebase Admin SDK Setup

## Goal

Allow FastAPI to communicate securely with Firebase.

## Tasks

- [ ] Install Firebase Admin SDK
- [ ] Create service account credentials
- [ ] Add backend environment variables
- [ ] Create Firebase Admin initialization service

## Required Files

```txt
backend/app/services/firebase_admin_service.py
backend/.env.example
```

## Environment Variables

```env
FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=
```

Never commit:

```txt
service-account.json
backend/.env
```

## Acceptance Criteria

- Firebase Admin initializes successfully
- Credentials load from environment variables
- No secrets committed

## Commit Message

```bash
git commit -m "feat(api): configure firebase admin sdk"
```

---

# Phase 4.2 — Token Verification Utility

## Goal

Create reusable Firebase token verification logic.

## Tasks

- [ ] Create token verification utility
- [ ] Verify Firebase ID tokens
- [ ] Extract authenticated user information
- [ ] Handle invalid tokens
- [ ] Handle expired tokens

## Required Files

```txt
backend/app/utils/auth.py
```

## Output

Verification should return:

```python
{
    "uid": "...",
    "email": "...",
}
```

## Acceptance Criteria

- Valid tokens pass
- Invalid tokens fail
- Expired tokens fail

## Commit Message

```bash
git commit -m "feat(api): add firebase token verification"
```

---

# Phase 4.3 — Authentication Dependency

## Goal

Create a reusable FastAPI dependency.

## Tasks

- [ ] Create get_current_user dependency
- [ ] Read Authorization header
- [ ] Extract Bearer token
- [ ] Verify Firebase token
- [ ] Return authenticated user

## Required Files

```txt
backend/app/dependencies.py
```

## Example

```python
@router.get("/protected")
def protected_route(
    user=Depends(get_current_user)
):
    return {"uid": user["uid"]}
```

## Acceptance Criteria

- Dependency works on multiple endpoints
- User object is available in routes

## Commit Message

```bash
git commit -m "feat(api): add auth dependency"
```

---

# Phase 4.4 — Protected Test Endpoint

## Goal

Verify backend authentication works.

## Tasks

- [ ] Create protected endpoint
- [ ] Return authenticated user data
- [ ] Reject unauthorized requests

## Endpoint

```txt
GET /api/auth/me
```

## Responses

### Authorized

```json
{
  "uid": "...",
  "email": "..."
}
```

### Unauthorized

```json
{
  "detail": "Unauthorized"
}
```

## Required Files

```txt
backend/app/api/auth.py
backend/app/schemas/auth.py
```

## Acceptance Criteria

- Endpoint rejects anonymous users
- Endpoint returns authenticated user

## Commit Message

```bash
git commit -m "feat(api): add protected auth endpoint"
```

---

# Phase 4.5 — Frontend API Client Integration

## Goal

Send Firebase ID token with backend requests.

## Tasks

- [ ] Create API client
- [ ] Retrieve current Firebase token
- [ ] Add Authorization header
- [ ] Call protected endpoint

## Required Files

```txt
frontend/services/api-client.ts
```

## Request Example

```http
Authorization: Bearer eyJhbGci...
```

## Acceptance Criteria

- Frontend sends token
- Backend validates token
- Protected endpoint responds successfully

## Commit Message

```bash
git commit -m "feat(api): send firebase auth token"
```

---

# Authentication Flow

```txt
User Login
    ↓
Firebase Auth
    ↓
Firebase ID Token
    ↓
Frontend API Client
    ↓
Authorization Header
    ↓
FastAPI
    ↓
Firebase Admin SDK
    ↓
Verified User
```

---

# Testing Plan

## Manual Tests

### Test 1

Login from frontend.

Expected:

```txt
User authenticated
```

### Test 2

Call:

```txt
GET /api/auth/me
```

with token.

Expected:

```json
{
  "uid": "...",
  "email": "..."
}
```

### Test 3

Call endpoint without token.

Expected:

```json
{
  "detail": "Unauthorized"
}
```

### Test 4

Call endpoint with invalid token.

Expected:

```json
{
  "detail": "Unauthorized"
}
```

---

# Acceptance Criteria

### Backend

- [ ] Firebase Admin configured
- [ ] Tokens verified
- [ ] Auth dependency created
- [ ] Protected endpoint created

### Frontend

- [ ] API client created
- [ ] Firebase token attached

### Integration

- [ ] Backend accepts valid Firebase users
- [ ] Backend rejects invalid users

---

# Exit Criteria

Milestone 4 is complete when:

- Firebase ID tokens are verified.
- Protected FastAPI endpoints work.
- Frontend successfully authenticates backend requests.
- Project is ready for user-specific Firestore data.

---

# Next Milestone

➡️ Milestone 5 — Application Tracker

Focus:

- Firestore data model
- CRUD endpoints
- User-specific application management
- Dashboard integration