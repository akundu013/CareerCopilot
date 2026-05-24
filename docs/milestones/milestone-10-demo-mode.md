# Milestone 10 — Demo Mode

## Status

🚧 Not Started

---

# Objective

Create a recruiter-friendly demo experience so visitors can explore Career Copilot without creating their own account or manually entering data.

The demo account should look populated, polished, and safe to use.

The system should:

- Use the existing demo email/password account
- Seed demo applications
- Seed demo resumes
- Seed demo analyses
- Seed demo interview sessions
- Add a demo login button
- Prevent destructive demo actions
- Allow limited demo experimentation
- Provide a reset strategy for demo data

---

# Existing Demo Account

The project already has a demo account configured.

```txt
demo@careercopilot.dev
```

Use the existing demo credentials from the current environment/configuration.

Do not hardcode secrets in source code.

---

# Demo Usage Rules

The demo account should be recruiter-friendly but controlled.

Recruiters should be able to explore the app and try limited workflows.

## Allowed Demo Actions

Demo users may:

```txt
View seeded applications
View seeded resumes
View seeded analyses
View seeded interview sessions
Create limited new resumes
Create limited new analyses
Try interview preparation in a restricted way
```

## Demo Limits

In addition to seeded demo data, the demo account may create:

```txt
Maximum custom resumes: 2
Maximum analyses per custom resume: 5
```

Interview preparation should be restricted because a future milestone will replace deterministic/hardcoded interview questions with AI-assisted generation.

For Milestone 10, interview prep remains non-AI and limited.

## Protected Demo Data

Seeded demo data should not be permanently destroyed by demo users.

Seeded records should either:

- Be read-only
- Be restored by reset
- Or be blocked from destructive actions

---

# Demo Firestore Structure

Use the existing user-scoped structure:

```txt
users/{demoUid}/applications/{applicationId}
users/{demoUid}/resumes/{resumeId}
users/{demoUid}/analyses/{analysisId}
users/{demoUid}/interviews/{sessionId}
```

Seeded demo records should include metadata fields such as:

```txt
isSeededDemoData: true
createdByDemoSeed: true
```

User-created demo records may include:

```txt
isDemoCreated: true
```

---

# Phase 10.1 — Demo Constants + Guard Utilities

## Goal

Create shared backend utilities to identify demo users and enforce demo restrictions.

## Output Files

```txt
backend/app/config/demo.py
backend/app/services/demo_guard.py
```

## Requirements

- Define demo email from environment or config
- Do not hardcode demo password
- Create helper to detect demo user
- Create helper to detect seeded demo data
- Create helper to enforce demo limits
- Keep logic backend-owned for security

## Suggested Environment Variable

```txt
DEMO_USER_EMAIL=demo@careercopilot.dev
```

## Demo Guard Responsibilities

```python
is_demo_user(user)
is_seeded_demo_record(record)
assert_demo_can_create_resume(user_id)
assert_demo_can_create_analysis(user_id, resume_id)
assert_demo_can_delete_record(record)
```

## Success Criteria

- Backend can identify demo account
- Demo restriction helpers exist
- No frontend-only security assumptions
- No secrets hardcoded

## Commit

```bash
git commit -m "feat(demo): add demo guard utilities"
```

---

# Phase 10.2 — Demo Seed Script

## Goal

Create a repeatable seed script that populates the demo account with realistic data.

## Output Files

```txt
backend/scripts/seed_demo_data.py
backend/app/services/demo_seed_data.py
```

## Seed Data Should Include

```txt
Applications
Resumes
Analyses
Interview Sessions
```

## Recommended Seed Counts

```txt
Applications: 8–12
Resumes: 2
Analyses: 4–6
Interview Sessions: 2–3
```

## Requirements

- Seed data under the existing demo user's UID
- Use realistic but fake companies, roles, resumes, analyses, and sessions
- Mark all seeded records with `isSeededDemoData: true`
- Make script idempotent where possible
- Avoid duplicating seed data on repeated runs
- Do not require frontend interaction

## Example Seed Applications

```txt
Frontend Developer — Applied
Full Stack Developer — Interview
Data Analyst — Rejected
Backend Developer — Saved
Software Consultant — Offer
```

## Success Criteria

- Demo account can be populated from script
- Seed script is repeatable
- Seeded data appears in Firestore
- Seeded data supports existing UI pages

## Commit

```bash
git commit -m "feat(demo): add demo seed script"
```

---

# Phase 10.3 — Demo Login UI

## Goal

Add a recruiter-friendly demo login button.

## Output Files

```txt
frontend/components/auth/DemoLoginButton.tsx
frontend/components/auth/DemoLoginButton.module.scss
```

Modify as needed:

```txt
frontend/app/login/page.tsx
frontend/services/auth-service.ts
```

## Requirements

- Add clear demo login button on login page
- Use existing Firebase demo account
- Do not expose password in UI text
- Use environment variable for demo credentials if needed
- Show loading and error states
- Route user to dashboard after successful demo login

## Suggested Button Text

```txt
Try Demo Account
```

## Suggested Helper Text

```txt
Explore Career Copilot with sample applications, resumes, analyses, and interview prep.
```

## Success Criteria

- Recruiter can log in with one click
- Demo login works without manual signup
- No secrets are committed
- Existing normal login still works

## Commit

```bash
git commit -m "feat(demo): add demo login"
```

---

# Phase 10.4 — Demo Restrictions

## Goal

Prevent destructive or excessive actions in demo mode while allowing limited exploration.

## Output Files

```txt
backend/app/services/demo_guard.py
```

Modify as needed:

```txt
backend/app/api/applications.py
backend/app/api/resumes.py
backend/app/api/analyses.py
backend/app/api/interviews.py
```

## Restrictions

For seeded demo data:

```txt
Block permanent delete
Block destructive updates that damage demo story
Allow read access
```

For demo-created data:

```txt
Allow create within limits
Allow delete if not seeded
Allow update if not seeded
```

## Limits

```txt
Custom demo resumes: max 2
Analyses per custom resume: max 5
Interview prep: restricted or limited
```

## Interview Prep Restriction

Because interview prep will later use AI, keep demo usage limited.

Recommended rule for Milestone 10:

```txt
Demo users can view seeded interview sessions.
Demo users can create at most 1 custom interview session.
Demo users can save answers for custom session.
Seeded interview sessions cannot be deleted.
```

## Error Messages

Return clear messages such as:

```txt
Demo mode protects seeded data from deletion.
Demo mode allows up to 2 custom resumes.
Demo mode allows up to 5 analyses per custom resume.
Demo mode allows limited interview practice.
```

## Success Criteria

- Seeded data cannot be deleted by demo users
- Demo user can create up to 2 custom resumes
- Demo user cannot exceed resume limit
- Demo user can create up to 5 analyses per custom resume
- Demo user cannot exceed analysis limit
- Interview prep is limited
- Normal users are unaffected

## Commit

```bash
git commit -m "feat(demo): enforce demo restrictions"
```

---

# Phase 10.5 — Demo Reset Strategy

## Goal

Create a safe way to restore demo data to a clean recruiter-ready state.

## Output Files

```txt
backend/scripts/reset_demo_data.py
backend/scripts/seed_demo_data.py
```

Optional backend service file:

```txt
backend/app/services/demo_reset_service.py
```

## Reset Behavior

The reset process should:

```txt
Delete demo-created non-seeded records
Restore or recreate seeded records
Preserve demo user account
Avoid touching non-demo users
```

## Recommended Strategy

Use scripts, not public API routes.

Reason:

```txt
Safer
Harder to abuse
No public reset endpoint
Easy to run manually before demos
```

## Commands

Recommended usage:

```bash
cd backend
python scripts/reset_demo_data.py
python scripts/seed_demo_data.py
```

## Success Criteria

- Demo data can be reset before recruiter demos
- Reset does not affect real users
- Seeded data returns to expected state
- Demo-created data can be cleaned up

## Commit

```bash
git commit -m "feat(demo): add demo reset strategy"
```

---

# Phase 10.6 — Demo Polish + Verification

## Goal

Make the demo experience clear, safe, and recruiter-friendly.

## Output Files

```txt
frontend/components/demo/DemoModeBanner.tsx
frontend/components/demo/DemoModeBanner.module.scss
```

Modify as needed:

```txt
frontend/app/dashboard/layout.tsx
frontend/components/**/*.tsx
backend/app/api/**/*.py
```

## UI Requirements

- Show demo mode banner when demo user is logged in
- Explain that seeded demo data is protected
- Show friendly messages when demo limits are reached
- Hide or disable destructive buttons for protected seeded records where practical
- Keep backend enforcement as source of truth

## Suggested Banner Text

```txt
Demo Mode: You are exploring sample data. Seeded demo records are protected, but you can try limited uploads and analyses.
```

## Final Verification Flow

```txt
Click Try Demo Account
↓
Dashboard opens with populated data
↓
Applications are visible
↓
Resumes are visible
↓
Analyses are visible
↓
Interview sessions are visible
↓
Seeded data cannot be deleted
↓
Create up to 2 custom resumes
↓
Create up to 5 analyses per custom resume
↓
Try limited interview preparation
↓
Reset demo data using script
↓
Seeded data is restored
```

## Success Criteria

- Recruiters can explore without setup
- Demo account looks populated
- Demo restrictions are understandable
- Seeded data is protected
- Demo limits work
- Reset strategy works
- Normal user behavior is unaffected
- No console errors

## Commit

```bash
git commit -m "chore(demo): finalize demo mode"
```

---

# Milestone 10 Success Criteria

- [ ] Demo login button works
- [ ] Demo account opens with populated data
- [ ] Demo applications are seeded
- [ ] Demo resumes are seeded
- [ ] Demo analyses are seeded
- [ ] Demo interview sessions are seeded
- [ ] Seeded demo data is protected
- [ ] Demo user can create up to 2 custom resumes
- [ ] Demo user can create up to 5 analyses per custom resume
- [ ] Demo interview prep is restricted
- [ ] Demo reset script works
- [ ] Normal users are unaffected
- [ ] No console errors

---

# Backend Verification

- [ ] Demo user detection works
- [ ] Seed script populates correct user
- [ ] Reset script affects only demo user data
- [ ] Seeded demo records cannot be deleted
- [ ] Demo resume limit enforced
- [ ] Demo analysis limit enforced
- [ ] Demo interview prep restriction enforced
- [ ] Normal users can still use regular workflows

---

# UI Verification

- [ ] Demo login button visible
- [ ] Demo login succeeds
- [ ] Demo mode banner visible
- [ ] Seeded data appears in dashboard pages
- [ ] Protected delete actions show helpful message
- [ ] Resume limit message appears at limit
- [ ] Analysis limit message appears at limit
- [ ] Interview prep restriction message appears when applicable
- [ ] App remains visually polished

---

# Demo Data Policy

Seeded data should be realistic but fake.

Do not include:

```txt
Real personal data
Real recruiter data
Real company confidential data
Real resumes from other people
Private credentials
```

Use fictional or generic sample data.

---

# Codex Prompt Template

```txt
Read:

- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-10-demo-mode.md

Implement Phase 10.X only.

Requirements:
- Use the existing demo account
- Do not hardcode secrets
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
