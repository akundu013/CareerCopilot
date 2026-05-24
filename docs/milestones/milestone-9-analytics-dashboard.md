# Milestone 9 — Analytics Dashboard

## Status

🚧 Not Started

---

# Objective

Create a recruiter-impressive analytics dashboard that gives users useful job search insights based on their own application, resume, analysis, and interview preparation data.

The dashboard should help users quickly understand:

- Application pipeline health
- Application activity over time
- Response rate
- Resume/job match trends
- Most common missing requirements
- Interview preparation progress

---

# Dependency

Required:

```txt
Milestone 5 completed
Milestone 6 completed
Milestone 7 completed
Milestone 8 completed
```

Milestone 9 uses data from:

```txt
users/{uid}/applications
users/{uid}/resumes
users/{uid}/analyses
users/{uid}/interviews
```

---

# Architecture

Analytics should be calculated from user-scoped Firestore data.

For Milestone 9, keep the system simple:

```txt
Frontend requests analytics
↓
Backend loads user-scoped data
↓
Backend calculates analytics summary
↓
Frontend renders cards and charts
```

Do not introduce external analytics tools.

Do not use AI.

Do not use paid services.

---

# Dashboard Route

```txt
/dashboard/analytics
```

---

# Analytics Data Sources

## Applications

Used for:

```txt
Applications by status
Response rate
Weekly application activity
Total applications
```

## Analyses

Used for:

```txt
Average match score
Top missing requirements
Most matched requirements
Analysis count
```

## Resumes

Used for:

```txt
Uploaded resume count
Parsed resume count
```

## Interviews

Used for:

```txt
Interview session count
Saved answer count
```

---

# Phase 9.1 — Analytics Domain + Backend Service

## Goal

Create analytics response schemas and backend calculation service.

## Output Files

```txt
backend/app/schemas/analytics.py
backend/app/services/analytics_service.py
```

## Analytics Response Shape

```txt
totalApplications
applicationsByStatus
responseRate
weeklyApplicationActivity
totalResumes
parsedResumes
totalAnalyses
averageMatchScore
topMissingRequirements
topMatchedRequirements
totalInterviewSessions
savedInterviewAnswers
```

## Requirements

- Create Pydantic response schemas
- Create analytics calculation service
- Use user-scoped data only
- Return safe defaults when no data exists
- Keep calculations deterministic and testable

## Success Criteria

- Analytics schemas exist
- Analytics service exists
- Empty user data returns valid zero-state response
- Calculations are user-scoped

## Commit

```bash
git commit -m "feat(analytics): add analytics service"
```

---

# Phase 9.2 — Analytics API

## Goal

Expose analytics data through an authenticated backend endpoint.

## Output Files

```txt
backend/app/api/analytics.py
backend/app/main.py
```

## Endpoint

```txt
GET /api/analytics/summary
```

## Workflow

```txt
Frontend requests analytics
↓
Backend verifies authenticated user
↓
Backend loads user data
↓
Backend calculates analytics
↓
Backend returns summary
```

## Requirements

- Endpoint requires authentication
- Endpoint uses current user ID
- Users cannot access another user's analytics
- Endpoint appears in FastAPI docs
- API handles empty data cleanly

## Success Criteria

- `/api/analytics/summary` works
- Unauthenticated requests are rejected
- Empty user data returns valid response
- User-scoped data enforced

## Commit

```bash
git commit -m "feat(analytics): add analytics api"
```

---

# Phase 9.3 — Frontend Analytics API + Types

## Goal

Create frontend types and API service for analytics.

## Output Files

```txt
frontend/types/analytics.ts
frontend/services/analytics-api.ts
```

## Required Method

```ts
getAnalyticsSummary()
```

## Requirements

- Define TypeScript analytics types
- Reuse authenticated API client
- Firebase ID token is sent automatically
- Return typed analytics summary
- Handle API errors clearly

## Success Criteria

- Frontend can fetch analytics summary
- Types match backend response
- No UI yet

## Commit

```bash
git commit -m "feat(analytics): add frontend analytics api"
```

---

# Phase 9.4 — Analytics Dashboard UI

## Goal

Create the analytics dashboard page with summary cards and charts.

## Route

```txt
/dashboard/analytics
```

## Output Files

```txt
frontend/app/dashboard/analytics/page.tsx

frontend/components/analytics/AnalyticsDashboard.tsx
frontend/components/analytics/SummaryCard.tsx
frontend/components/analytics/ApplicationsByStatusChart.tsx
frontend/components/analytics/WeeklyActivityChart.tsx
frontend/components/analytics/RequirementsChart.tsx

frontend/components/analytics/AnalyticsDashboard.module.scss
frontend/components/analytics/SummaryCard.module.scss
frontend/components/analytics/ApplicationsByStatusChart.module.scss
frontend/components/analytics/WeeklyActivityChart.module.scss
frontend/components/analytics/RequirementsChart.module.scss
```

## Summary Cards

Show:

```txt
Total Applications
Response Rate
Average Match Score
Parsed Resumes
Interview Sessions
Saved Interview Answers
```

## Charts

Show:

```txt
Applications by Status
Weekly Application Activity
Top Missing Requirements
```

## Requirements

- Show loading state
- Show error state
- Show empty state
- Render charts from backend analytics data
- Use existing app shell and styling
- Use SCSS Modules only
- Do not use Tailwind
- Do not use external paid charting tools

## Success Criteria

- `/dashboard/analytics` opens
- Summary cards render
- Charts render
- Empty data state works
- No console errors

## Commit

```bash
git commit -m "feat(analytics): add analytics dashboard ui"
```

---

# Phase 9.5 — Dashboard Polish + Verification

## Goal

Finalize dashboard UX and verify analytics accuracy.

## Output Files

```txt
frontend/components/analytics/AnalyticsEmptyState.tsx
frontend/components/analytics/AnalyticsEmptyState.module.scss
```

Modify as needed:

```txt
frontend/components/analytics/AnalyticsDashboard.tsx
frontend/components/analytics/*.tsx
frontend/components/analytics/*.module.scss
```

## Requirements

- Improve empty states
- Improve chart readability
- Add helpful labels and descriptions
- Ensure all analytics are based on current user's data
- Verify numbers manually against Firestore
- Ensure dashboard is recruiter-demo friendly

## Verification Flow

```txt
Create applications with multiple statuses
↓
Create parsed resumes
↓
Create job match analyses
↓
Create interview sessions
↓
Open /dashboard/analytics
↓
Verify summary cards
↓
Verify charts
↓
Verify empty/error/loading states
```

## Success Criteria

- Dashboard gives useful job search insights
- Charts render correctly
- Analytics are accurate
- Empty state is helpful
- No console errors
- Protected route works

## Commit

```bash
git commit -m "chore(analytics): finalize analytics dashboard"
```

---

# Milestone 9 Success Criteria

- [ ] User can open `/dashboard/analytics`
- [ ] Dashboard shows total applications
- [ ] Dashboard shows applications by status
- [ ] Dashboard shows response rate
- [ ] Dashboard shows weekly application activity
- [ ] Dashboard shows average match score
- [ ] Dashboard shows top missing requirements
- [ ] Dashboard shows resume and interview preparation counts
- [ ] Charts render correctly
- [ ] Empty states work
- [ ] Analytics are based only on current user's data
- [ ] No console errors

---

# Backend Verification

- [ ] Analytics endpoint appears in `/docs`
- [ ] Protected endpoint rejects unauthenticated requests
- [ ] User-scoped data enforced
- [ ] Empty user data returns safe defaults
- [ ] Response rate calculation is correct
- [ ] Weekly activity calculation is correct
- [ ] Top missing requirements calculation is correct

---

# UI Verification

- [ ] Open `/dashboard/analytics`
- [ ] Summary cards visible
- [ ] Applications by status chart visible
- [ ] Weekly activity chart visible
- [ ] Top missing requirements chart visible
- [ ] Loading state works
- [ ] Error state works
- [ ] Empty state works
- [ ] Refresh page and data persists
- [ ] No console errors

---

# Analytics Calculation Notes

## Response Rate

Recommended formula:

```txt
responses / totalApplications * 100
```

Responses can include statuses such as:

```txt
interview
offer
rejected
```

Do not count statuses like:

```txt
saved
applied
```

as responses.

## Weekly Application Activity

Group applications by creation date week.

Return data such as:

```json
[
  {
    "week": "2026-05-18",
    "count": 4
  }
]
```

## Top Missing Requirements

Use all saved analyses.

Count frequency of each missing requirement.

Return top 5.

Example:

```json
[
  {
    "requirement": "CI/CD",
    "count": 3
  },
  {
    "requirement": "test automation",
    "count": 2
  }
]
```

## Average Match Score

Use saved analyses.

If there are no analyses, return:

```txt
0
```

---

# Codex Prompt Template

```txt
Read:

- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-9-analytics-dashboard.md

Implement Phase 9.X only.

Requirements:
- Follow existing repository pattern
- Follow existing API structure
- Follow existing Firestore structure
- Use TypeScript on frontend
- Use SCSS Modules only
- Do not use AI APIs
- Do not use paid analytics tools
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
