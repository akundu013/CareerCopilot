# Milestone 7 — Job Match Analysis

## Status

🚧 Not Started

---

# Objective

Allow users to compare an uploaded resume against a job description and receive:

- Match score
- Matched skills
- Missing skills
- Improvement suggestions
- Saved analysis history
- Analysis deletion and cleanup

This milestone delivers Career Copilot's primary value proposition.

---

# Business Context

Users upload resumes in Milestone 6.

Milestone 7 transforms resume data into actionable job matching insights.

The system compares:

```txt
Resume Parsed Text
vs
Job Description
```

and generates a structured analysis.

This becomes the foundation for future AI-powered features.

---

# Scope

## Included

- Resume selection
- Job description input
- Rule-based skill extraction
- Match scoring
- Missing skill detection
- Improvement suggestions
- Analysis persistence
- Analysis history
- Analysis deletion

## Excluded

- AI-generated resume rewriting
- Cover letter generation
- GPT integration
- ATS optimization
- Skill embeddings
- Semantic search
- Vector databases

---

# Firestore Structure

```txt
users/{uid}/analyses/{analysisId}
```

---

# Analysis Domain Model

Recommended fields:

```txt
id
userId
resumeId
jobDescription
matchScore
matchedSkills
missingSkills
improvementSuggestions
createdAt
updatedAt
```

---

# Phase 7.1 — Analysis Domain Model

## Goal

Define analysis data types.

### Frontend File

```txt
frontend/types/analysis.ts
```

### Tasks

- [ ] Create MatchScore type
- [ ] Create Analysis interface
- [ ] Create CreateAnalysisInput
- [ ] Create AnalysisSummary

### Acceptance Criteria

- Types exist
- Shared contract established

### Commit

```bash
git commit -m "feat(analysis): define analysis domain model"
```

---

# Phase 7.2 — Backend Analysis Schemas

## Goal

Create Pydantic schemas.

### Backend File

```txt
backend/app/schemas/analysis.py
```

### Schemas

```txt
CreateAnalysisRequest
AnalysisResponse
AnalysisSummaryResponse
```

### Commit

```bash
git commit -m "feat(analysis): add analysis schemas"
```

---

# Phase 7.3 — Analysis Repository

## Goal

Persist analysis results.

### Backend File

```txt
backend/app/services/analysis_repository.py
```

### Methods

```python
create_analysis()
get_analysis()
list_analyses()
delete_analysis()
```

### Delete Behavior

Analysis deletion should remove the Firestore analysis document:

```txt
users/{uid}/analyses/{analysisId}
```

The delete method must be scoped by authenticated user ID and must not allow cross-user deletion.

### Firestore Path

```txt
users/{uid}/analyses/{analysisId}
```

### Commit

```bash
git commit -m "feat(analysis): add repository layer"
```

---

# Phase 7.4 — Skill Extraction Service

## Goal

Extract skills from text.

### Backend File

```txt
backend/app/services/skill_extractor.py
```

### Strategy

Use predefined skill keywords.

Example:

```txt
React
TypeScript
Python
FastAPI
Docker
AWS
Firebase
Git
PostgreSQL
```

### Methods

```python
extract_skills(text)
```

### Acceptance Criteria

- Skills detected from resume text
- Skills detected from job description

### Commit

```bash
git commit -m "feat(analysis): add skill extraction service"
```

---

# Phase 7.5 — Match Engine Service

## Goal

Compare resume skills against job requirements.

### Backend File

```txt
backend/app/services/match_engine.py
```

### Inputs

```txt
resume skills
job skills
```

### Outputs

```txt
match score
matched skills
missing skills
```

### Scoring Formula

```txt
matchedSkills / jobSkills * 100
```

### Commit

```bash
git commit -m "feat(analysis): add match engine"
```

---

# Phase 7.6 — Improvement Suggestion Service

## Goal

Generate actionable recommendations.

### Backend File

```txt
backend/app/services/improvement_service.py
```

### Commit

```bash
git commit -m "feat(analysis): add improvement suggestions"
```

---

# Phase 7.7 — Analysis API

## Goal

Create analysis endpoint.

### Endpoint

```txt
POST /api/analyses
```

### Additional Endpoints

```txt
GET /api/analyses
GET /api/analyses/{id}
DELETE /api/analyses/{id}
```

### Workflow

```txt
User selects resume
↓
Resume loaded
↓
Parsed text loaded
↓
Skill extraction
↓
Match engine
↓
Suggestions generated
↓
Save analysis
↓
Return result
```

### Commit

```bash
git commit -m "feat(analysis): add analysis api"
```

---

# Phase 7.8 — Frontend Analysis API Client

### File

```txt
frontend/services/analysis-api.ts
```

### Methods

```ts
createAnalysis()
getAnalyses()
getAnalysis()
deleteAnalysis()
```

### Commit

```bash
git commit -m "feat(analysis): add frontend analysis api"
```

---

# Phase 7.9 — Job Match Form UI

## Route

```txt
/dashboard/analysis
```

### Components

```txt
AnalysisForm
ResumeSelector
JobDescriptionInput
```

### Requirements

- Select resume
- Paste job description
- Submit analysis

### Commit

```bash
git commit -m "feat(analysis): add analysis form"
```

---

# Phase 7.10 — Analysis Result UI

## Components

```txt
AnalysisResult
MatchScoreCard
MatchedSkillsList
MissingSkillsList
ImprovementSuggestions
```

### Commit

```bash
git commit -m "feat(analysis): add analysis result ui"
```

---

# Phase 7.11 — Analysis History

## Goal

Display previous analyses.

### Route

```txt
/dashboard/analysis/history
```

### Components

```txt
AnalysisHistory
AnalysisHistoryCard
```

### Requirements

- List analyses
- View analysis
- Delete analysis
- Require confirmation before delete
- Show deleting/loading state
- Remove deleted analysis from UI without page reload when possible
- Show error state if delete fails

### Delete Flow

```txt
User clicks Delete Analysis
↓
Confirmation dialog
↓
DELETE /api/analyses/{id}
↓
Backend deletes Firestore document
↓
Frontend refreshes analysis history
```

### Acceptance Criteria

- User can delete an analysis from history
- Deleted analysis disappears from the list
- Firestore document is removed from `users/{uid}/analyses/{analysisId}`
- Page refresh does not restore deleted analysis
- Delete errors show a clear message
- No console errors

### Commit

```bash
git commit -m "feat(analysis): add analysis history"
```

---

# Phase 7.12 — Milestone Polish

## End-to-End Flow

```txt
Upload Resume
↓
Parse Resume
↓
Open Analysis Page
↓
Select Resume
↓
Paste Job Description
↓
Generate Match
↓
View Score
↓
View Missing Skills
↓
View Suggestions
↓
Save Analysis
↓
View History
```

## UI Verification

- [ ] Resume selector works
- [ ] Job description input works
- [ ] Analysis created successfully
- [ ] Match score displayed
- [ ] Matched skills displayed
- [ ] Missing skills displayed
- [ ] Suggestions displayed
- [ ] Analysis saved to Firestore
- [ ] History page displays results
- [ ] Analysis deletion works
- [ ] Deleted analysis disappears after refresh
- [ ] No console errors
- [ ] Protected routes work

## Backend Verification

- [ ] Analysis endpoints appear in `/docs`
- [ ] User-scoped data enforced
- [ ] Skill extraction works
- [ ] Match engine works
- [ ] Analysis persistence works
- [ ] Analysis deletion is user-scoped
- [ ] Deleted analyses are removed from Firestore

### Commit

```bash
git commit -m "chore(analysis): finalize job match analysis milestone"
```
