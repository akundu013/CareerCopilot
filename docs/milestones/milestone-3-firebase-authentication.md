# Milestone 3 — Firebase Authentication

## Status

🚧 In Progress

---

## Objective

Add real user authentication to Career Copilot using Firebase Authentication.

This milestone adds:

- Firebase client configuration
- Email/password authentication
- Auth service layer
- Auth provider
- Login and signup pages
- Logout flow
- Protected dashboard routes
- Demo account support

---

## Scope

### Included

- Firebase Authentication
- Email/password auth
- Frontend Firebase config
- Auth service
- Auth provider
- `useAuth` hook
- Login page
- Signup page
- Logout
- Protected dashboard
- Demo account login

### Excluded

- Firestore writes
- Firebase Storage
- Backend JWT verification
- Application tracker
- Resume uploads
- Job match analysis

---

# Phase 3.1 — Firebase Client Configuration

## Goal

Connect the frontend app to Firebase.

## Tasks

- [ ] Confirm Firebase project exists
- [ ] Confirm web app is registered
- [ ] Confirm Email/Password auth is enabled
- [ ] Add Firebase config to `frontend/.env.local`
- [ ] Add safe placeholders to `frontend/.env.example`
- [ ] Install Firebase SDK
- [ ] Create `frontend/services/firebase.ts`
- [ ] Export Firebase `app`
- [ ] Export Firebase `auth`
- [ ] Prevent duplicate initialization

## Files

```txt
frontend/services/firebase.ts
frontend/.env.example
frontend/package.json
frontend/package-lock.json
```

## Commands

```bash
cd frontend
npm install firebase
```

## Acceptance Criteria

- Firebase SDK is installed
- Firebase initializes without errors
- `auth` can be imported from `@/services/firebase`
- No secrets are committed

## Commit Message

```bash
git commit -m "feat(auth): configure firebase client"
```

---

# Phase 3.2 — Auth Service Layer

## Goal

Create a project-specific wrapper around Firebase Auth.

## Tasks

- [ ] Create `frontend/services/auth-service.ts`
- [ ] Add signup function
- [ ] Add login function
- [ ] Add logout function
- [ ] Add auth state listener
- [ ] Map Firebase errors to readable messages

## Required Methods

```ts
signUpWithEmail(email, password)
signInWithEmail(email, password)
signOutUser()
onAuthStateChangedListener(callback)
```

## Files

```txt
frontend/services/auth-service.ts
```

## Acceptance Criteria

- UI does not call Firebase directly
- Firebase auth logic is isolated in service layer
- Service functions are reusable

## Commit Message

```bash
git commit -m "feat(auth): add authentication service layer"
```

---

# Phase 3.3 — Auth Provider and Hook

## Goal

Create global authentication state for the React app.

## Tasks

- [ ] Create `AuthProvider`
- [ ] Create `AuthContext`
- [ ] Create `useAuth` hook
- [ ] Track `user`
- [ ] Track `loading`
- [ ] Track `isAuthenticated`
- [ ] Wrap app with `AuthProvider`

## Files

```txt
frontend/components/auth/AuthProvider.tsx
frontend/hooks/useAuth.ts
frontend/types/auth.ts
frontend/app/layout.tsx
```

## Acceptance Criteria

- Components can access auth state using `useAuth`
- App waits while Firebase checks auth state
- Auth state persists on refresh

## Commit Message

```bash
git commit -m "feat(auth): add auth provider and context"
```

---

# Phase 3.4 — Login Page

## Goal

Allow existing users to log in.

## Tasks

- [ ] Create `/login` route
- [ ] Add email input
- [ ] Add password input
- [ ] Add submit button
- [ ] Show loading state
- [ ] Show error state
- [ ] Redirect to `/dashboard` after login
- [ ] Link to signup page

## Files

```txt
frontend/app/login/page.tsx
frontend/components/auth/AuthForm/
```

## Acceptance Criteria

- User can log in
- Invalid credentials show an error
- Successful login redirects to dashboard

## Commit Message

```bash
git commit -m "feat(auth): implement login page"
```

---

# Phase 3.5 — Signup Page

## Goal

Allow new users to create an account.

## Tasks

- [ ] Create `/signup` route
- [ ] Add email input
- [ ] Add password input
- [ ] Add confirm password input
- [ ] Validate password length
- [ ] Validate password confirmation
- [ ] Show loading state
- [ ] Show error state
- [ ] Redirect to `/dashboard` after signup
- [ ] Link to login page

## Files

```txt
frontend/app/signup/page.tsx
frontend/components/auth/AuthForm/
```

## Acceptance Criteria

- User can sign up
- Weak password shows an error
- Mismatched passwords show an error
- Successful signup redirects to dashboard

## Commit Message

```bash
git commit -m "feat(auth): implement signup page"
```

---

# Phase 3.6 — Protected Routes

## Goal

Prevent unauthenticated users from accessing private app routes.

## Tasks

- [ ] Create `ProtectedRoute`
- [ ] Protect `/dashboard`
- [ ] Redirect logged-out users to `/login`
- [ ] Avoid redirect flicker while auth state loads
- [ ] Redirect logged-in users away from `/login` and `/signup`

## Files

```txt
frontend/components/auth/ProtectedRoute.tsx
frontend/app/dashboard/page.tsx
frontend/app/login/page.tsx
frontend/app/signup/page.tsx
```

## Acceptance Criteria

- Logged-out users cannot access dashboard
- Logged-in users can access dashboard
- Auth loading state prevents flicker

## Commit Message

```bash
git commit -m "feat(auth): add protected routes"
```

---

# Phase 3.7 — Logout Flow

## Goal

Allow authenticated users to log out.

## Tasks

- [ ] Add logout action to header/app shell
- [ ] Call auth service logout method
- [ ] Redirect user to `/login`
- [ ] Clear auth state

## Files

```txt
frontend/components/layout/Header/*
frontend/components/layout/AppShell/*
```

## Acceptance Criteria

- User can log out
- User is redirected to login page
- Dashboard becomes inaccessible after logout

## Commit Message

```bash
git commit -m "feat(auth): add logout flow"
```

---

# Phase 3.8 — Demo Account

## Goal

Allow recruiters to explore the app quickly.

## Tasks

- [ ] Create demo account in Firebase Console
- [ ] Add demo email to env
- [ ] Add demo password to env locally only
- [ ] Add demo login button
- [ ] Do not commit real password

## Environment Variables

```env
NEXT_PUBLIC_DEMO_EMAIL=demo@careercopilot.dev
NEXT_PUBLIC_DEMO_PASSWORD=
```

## Files

```txt
frontend/app/login/page.tsx
frontend/.env.example
```

## Acceptance Criteria

- Demo login button exists
- Demo login works locally
- Demo password is not committed

## Commit Message

```bash
git commit -m "feat(auth): add demo account login"
```

---

# Final Milestone Acceptance Criteria

Milestone 3 is complete when:

- [ ] Firebase client is configured
- [ ] User can sign up
- [ ] User can log in
- [ ] User can log out
- [ ] Dashboard is protected
- [ ] Demo account works
- [ ] `.env.local` is not committed
- [ ] `.env.example` is committed
- [ ] README/ROADMAP are updated if needed

---

# Recommended Codex Workflow

Do not ask Codex to implement the whole milestone at once.

Use this pattern:

```txt
Read AGENTS.md and docs/milestones/milestone-3-firebase-authentication.md.

Implement Phase 3.1 only.

Do not implement future phases.

Before coding:
1. List files to create
2. List files to modify
3. Explain why

After coding:
1. Explain what changed
2. Explain how to test it
3. Stop and wait for review
```

---

# Next Milestone

➡️ Milestone 4 — Backend Auth Verification

Focus:

- Firebase Admin SDK
- FastAPI token verification
- Protected backend endpoints