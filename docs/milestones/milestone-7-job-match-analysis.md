# Milestone 7 — Job Match Analysis

## Status

🚧 Not Started

---

# Objective

Allow users to compare an uploaded resume against a job description and receive:

- Match score
- Matched requirements
- Missing requirements
- Improvement suggestions
- Saved analysis history
- Analysis deletion and cleanup

This milestone delivers Career Copilot's primary value proposition.

---

# Business Context

Users upload and parse resumes in Milestone 6.

Milestone 7 transforms parsed resume data into actionable job matching insights.

The system compares:

```txt
Resume Parsed Text
vs
Job Description
```

and generates a structured analysis.

This milestone should work across industries and roles. It should not be limited to software engineering jobs.

This becomes the foundation for future AI-powered features.

---

# Scope

## Included

- Resume selection
- Job description input
- Dynamic requirement extraction from job descriptions
- Deterministic resume-to-job matching
- Match scoring
- Missing requirement detection
- Improvement suggestions
- Analysis persistence
- Analysis history
- Analysis deletion

## Excluded

- AI-generated resume rewriting
- Cover letter generation
- Claude/OpenAI/GPT integration
- ATS optimization
- Skill embeddings
- Semantic search
- Vector databases
- Hardcoded industry-only skill catalogs

---

# Architecture Decision

Milestone 7 will use a deterministic, rule-based matching engine.

The first version should not use Claude, OpenAI, embeddings, or external AI services.

Reason:

- No AI API cost
- Easier to test
- Easier to explain in interviews
- Predictable output
- Stronger backend/service-layer demonstration
- Works as a baseline before future AI enhancement

Future milestone idea:

```txt
Milestone 8 — AI Match Enhancement
```

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
resumeFileName
jobDescription
extractedRequirements
matchScore
matchedRequirements
missingRequirements
improvementSuggestions
createdAt
updatedAt
```

---

# Important Dependency

Milestone 7 depends on Milestone 6.

Before running a job match analysis, the selected resume must have:

```txt
status = parsed
parsedText exists
```

If a resume is not parsed yet, the UI should guide the user to parse it first.

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

# Phase 7.4 — Requirement Extraction Service

## Goal

Extract job-relevant requirements dynamically from job descriptions without relying on a hardcoded skill catalog.

This service must work across industries and roles, not only software jobs.

The extractor should identify important requirements from the job description itself, then normalize them so the match engine can compare them against resume text.

---

## Backend File

```txt
backend/app/services/requirement_extractor.py
```

---

## Strategy

Use deterministic text processing instead of AI or a fixed skill list.

The service should:

- Normalize text
- Split job description into sentences
- Detect requirement-heavy sentences
- Extract meaningful phrases
- Remove common stopwords and filler phrases
- Remove duplicate requirements
- Return stable normalized requirement phrases

---

## Requirement Signals

Prioritize sentences containing phrases such as:

```txt
required
requirements
preferred
qualifications
skills
experience with
experience in
responsible for
must have
nice to have
ability to
familiar with
knowledge of
proficiency in
certification
license
degree
```

The extractor should also handle bullet-heavy job descriptions where every bullet may represent a requirement, even if the bullet does not contain one of the signal phrases.

---

## Example

Job Description:

```txt
We are looking for a customer support specialist with experience handling Zendesk tickets, resolving billing issues, and communicating with enterprise clients.
```

Extracted Requirements:

```json
[
  "customer support",
  "zendesk tickets",
  "billing issues",
  "enterprise clients",
  "communication"
]
```

---

## Required Methods

```python
normalize_text(text: str) -> str

split_into_sentences(text: str) -> list[str]

is_requirement_sentence(sentence: str) -> bool

extract_candidate_phrases(sentence: str) -> list[str]

deduplicate_requirements(requirements: list[str]) -> list[str]

extract_requirements(text: str) -> list[str]
```

---

## Implementation Notes

Start simple.

Do not add external NLP libraries yet unless necessary.

Use Python standard library tools such as:

```txt
re
string
collections
```

Recommended phrase extraction approach:

1. Lowercase text
2. Remove excessive punctuation
3. Split text into sentences and bullet fragments
4. Keep sentences with requirement signals
5. Treat bullet points as candidate requirement fragments
6. Split sentence fragments by commas, semicolons, bullets, slashes, and conjunctions
7. Remove very short fragments
8. Remove generic filler phrases
9. Deduplicate normalized requirements
10. Return normalized unique phrases

---

## Stopword/Filler Handling

Remove generic terms that do not help matching, such as:

```txt
we are looking for
the ideal candidate
candidate should
you will
responsible for
must have
nice to have
required
preferred
experience with
experience in
ability to
knowledge of
familiar with
proficiency in
```

The goal is to keep the meaningful part.

Example:

```txt
experience with resolving billing issues
```

should become:

```txt
resolving billing issues
```

or:

```txt
billing issues
```

---

## Output Shape

Return a flat list of normalized requirement phrases:

```json
[
  "customer support",
  "billing issues",
  "enterprise clients"
]
```

Do not group by industry in this milestone.

Reason:

- Industry grouping requires classification
- Classification can be inaccurate without AI
- Flat requirement matching is simpler and more reliable for the first version

---

## Acceptance Criteria

- Extracts requirements from arbitrary job descriptions
- Does not depend on a hardcoded skill catalog
- Works for software, healthcare, education, marketing, finance, operations, and general roles
- Handles bullet-heavy job descriptions
- Handles paragraph-style job descriptions
- Removes duplicate requirements
- Removes low-value filler phrases
- Returns stable normalized requirement phrases
- Has unit-testable pure functions

---

## Testing Guidance

Test with multiple job types:

```txt
Software Engineer
Customer Support Specialist
Teacher
Nurse
Marketing Coordinator
Finance Assistant
Operations Manager
Warehouse Associate
Sales Representative
Administrative Assistant
```

Verify that the extractor returns meaningful requirements for each role.

Suggested test cases:

- Bullet-heavy job description
- Paragraph-heavy job description
- Job description with required/preferred sections
- Job description with no obvious requirements
- Very short job description
- Empty job description

---

## Codex Prompt

```txt
Read:

- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-7-job-match-analysis.md

Implement Phase 7.4 only.

Create:

backend/app/services/requirement_extractor.py

Requirements:

1. Build a deterministic requirement extraction service.
2. Do not use Claude, OpenAI, embeddings, external AI APIs, or hardcoded industry-only skill catalogs.
3. Extract requirements dynamically from the job description text itself.
4. Implement pure functions:
   - normalize_text
   - split_into_sentences
   - is_requirement_sentence
   - extract_candidate_phrases
   - deduplicate_requirements
   - extract_requirements
5. Handle both bullet-heavy and paragraph-style job descriptions.
6. Remove filler phrases and duplicate requirements.
7. Return a flat list of normalized requirement phrases.

Do not implement the match engine.
Do not implement API routes.
Do not modify frontend files.
Do not implement future phases.

Before coding:
- List files to create
- Explain the plan

After coding:
- Explain changes
- Explain how to test
- Stop.
```

---

## Commit Message

```bash
git commit -m "feat(analysis): add requirement extraction service"
```

---

# Phase 7.5 — Match Engine Service

## Goal

Compare extracted job requirements against parsed resume text and generate a deterministic match result.

The match engine should not rely on a hardcoded skill catalog.

It should compare:

```txt
Extracted job requirements
vs
Parsed resume text
```

and return:

- Match score
- Matched requirements
- Missing requirements

---

## Backend File

```txt
backend/app/services/match_engine.py
```

---

## Inputs

```txt
resume_text
job_requirements
```

Where:

```txt
resume_text = parsedText from users/{uid}/resumes/{resumeId}
job_requirements = output from requirement_extractor.extract_requirements(jobDescription)
```

---

## Outputs

```txt
matchScore
matchedRequirements
missingRequirements
```

---

## Matching Strategy

Use deterministic text matching.

Recommended approach:

1. Normalize resume text
2. Normalize each requirement
3. Check whether each requirement or important words from the requirement appear in resume text
4. Mark requirement as matched or missing
5. Calculate score

---

## Scoring Formula

```txt
matchedRequirements / totalJobRequirements * 100
```

Example:

```txt
6 matched requirements
10 total requirements
= 60%
```

If no requirements are extracted, return:

```txt
matchScore = 0
matchedRequirements = []
missingRequirements = []
```

and let the API return a clear message that the job description did not contain enough detectable requirements.

---

## Example

Job Requirements:

```json
[
  "customer support",
  "zendesk tickets",
  "billing issues",
  "enterprise clients"
]
```

Resume Text:

```txt
Handled customer support requests and resolved billing issues for B2B customers.
```

Result:

```json
{
  "matchScore": 50,
  "matchedRequirements": [
    "customer support",
    "billing issues"
  ],
  "missingRequirements": [
    "zendesk tickets",
    "enterprise clients"
  ]
}
```

---

## Required Methods

```python
normalize_text(text: str) -> str

get_meaningful_words(text: str) -> list[str]

requirement_matches_resume(requirement: str, resume_text: str) -> bool

calculate_match_score(
    matched_count: int,
    total_count: int
) -> int

analyze_match(
    resume_text: str,
    job_requirements: list[str]
) -> dict
```

---

## Matching Rules

A requirement should count as matched when:

- The full normalized phrase appears in resume text

or

- Most meaningful words from the requirement appear in resume text

Example:

```txt
Requirement:
enterprise client communication

Resume:
communicated with enterprise clients
```

This should count as a match.

Avoid overly loose matching.

For example:

```txt
Requirement:
project management

Resume:
project
```

This should not automatically count as a match.

---

## Recommended Word Matching Threshold

For multi-word requirements:

```txt
2-word requirement:
both meaningful words should match

3+ word requirement:
at least 70% of meaningful words should match
```

For 1-word requirements:

```txt
the exact normalized word should appear in resume text
```

---

## Acceptance Criteria

- Compares resume text against extracted job requirements
- Produces deterministic match score
- Returns matched requirements
- Returns missing requirements
- Handles empty resume text safely
- Handles empty requirement list safely
- Does not use Claude, OpenAI, or external AI services
- Does not rely on a hardcoded skill catalog
- Avoids overly loose single-word matches
- Has unit-testable pure functions

---

## Testing Guidance

Test with:

- Strong match
- Partial match
- No match
- Empty resume text
- Empty job requirements
- Bullet-heavy job description requirements
- Paragraph-heavy job description requirements
- Non-software job descriptions

Suggested examples:

```txt
Customer Support Specialist
Teacher
Nurse
Marketing Coordinator
Finance Assistant
Operations Manager
Software Engineer
```

---

## Codex Prompt

```txt
Read:

- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-7-job-match-analysis.md

Implement Phase 7.5 only.

Create:

backend/app/services/match_engine.py

Requirements:

1. Build a deterministic match engine.
2. Compare parsed resume text against extracted job requirements.
3. Do not use Claude, OpenAI, embeddings, external AI APIs, or hardcoded skill catalogs.
4. Implement pure functions:
   - normalize_text
   - get_meaningful_words
   - requirement_matches_resume
   - calculate_match_score
   - analyze_match
5. Return:
   - matchScore
   - matchedRequirements
   - missingRequirements
6. Handle empty resume text safely.
7. Handle empty requirement lists safely.
8. Avoid overly loose matches.

Do not implement requirement extraction.
Do not implement API routes.
Do not modify frontend files.
Do not implement future phases.

Before coding:
- List files to create
- Explain the plan

After coding:
- Explain changes
- Explain how to test
- Stop.
```

---

## Commit Message

```bash
git commit -m "feat(analysis): add match engine"
```

---

# Phase 7.6 — Improvement Suggestion Service

## Goal

Generate deterministic improvement suggestions based on missing requirements.

This service should not use AI in Milestone 7.

It should convert missing requirements into clear, actionable user guidance.

---

## Backend File

```txt
backend/app/services/improvement_service.py
```

---

## Inputs

```txt
missingRequirements
matchedRequirements
matchScore
```

---

## Outputs

```txt
improvementSuggestions
```

---

## Strategy

Use template-based suggestions.

Examples:

```txt
Missing requirement:
billing issues

Suggestion:
Add resume bullets that demonstrate experience with billing issues, if applicable.
```

```txt
Missing requirement:
enterprise clients

Suggestion:
Highlight any experience working with enterprise clients or similar high-value customers.
```

---

## Required Methods

```python
generate_suggestions(
    missing_requirements: list[str],
    matched_requirements: list[str],
    match_score: int
) -> list[str]
```

---

## Acceptance Criteria

- Generates suggestions from missing requirements
- Handles empty missing requirements
- Produces user-friendly language
- Does not hallucinate experience
- Uses cautious phrasing such as "if applicable"
- Does not use Claude, OpenAI, or external AI services

---

## Commit Message

```bash
git commit -m "feat(analysis): add improvement suggestions"
```

---

# Phase 7.7 — Analysis API

## Goal

Create authenticated backend endpoints for job match analysis.

---

## Backend Files

```txt
backend/app/api/analyses.py
backend/app/main.py
```

---

## Endpoints

```txt
POST   /api/analyses
GET    /api/analyses
GET    /api/analyses/{analysis_id}
DELETE /api/analyses/{analysis_id}
```

---

## POST /api/analyses Workflow

```txt
User selects resume
↓
Backend verifies authenticated user
↓
Backend loads resume metadata from users/{uid}/resumes/{resumeId}
↓
Backend verifies resume belongs to current user
↓
Backend verifies resume status is parsed
↓
Backend reads parsedText
↓
Backend extracts requirements from job description
↓
Backend compares requirements against parsedText
↓
Backend generates improvement suggestions
↓
Backend saves analysis to users/{uid}/analyses/{analysisId}
↓
Backend returns saved analysis
```

---

## Requirements

- All routes require `get_current_user`
- Analysis creation requires a parsed resume
- Analysis data is scoped to authenticated UID
- Users cannot analyze another user's resume
- Users cannot read or delete another user's analyses
- Routes appear in FastAPI docs
- API returns clear errors for:
  - missing resume
  - unparsed resume
  - empty job description
  - no detectable requirements

---

## Commit Message

```bash
git commit -m "feat(analysis): add analysis api"
```

---

# Phase 7.8 — Frontend Analysis API Client

## Goal

Create frontend service functions for analysis APIs.

---

## Frontend File

```txt
frontend/services/analysis-api.ts
```

---

## Methods

```ts
createAnalysis(input)
getAnalyses()
getAnalysis(id)
deleteAnalysis(id)
```

---

## Requirements

- Reuse authenticated API client
- Firebase ID token is sent automatically
- Return typed analysis responses
- Handle API errors clearly

---

## Acceptance Criteria

- Frontend can create analysis
- Frontend can list analysis history
- Frontend can read one analysis
- Frontend can delete an analysis
- No UI yet

---

## Commit Message

```bash
git commit -m "feat(analysis): add frontend analysis api"
```

---

# Phase 7.9 — Job Match Form UI

## Goal

Create the UI where users select a parsed resume and paste a job description.

---

## Route

```txt
/dashboard/analysis
```

---

## Components

```txt
frontend/components/analysis/AnalysisForm.tsx
frontend/components/analysis/AnalysisForm.module.scss
frontend/components/analysis/ResumeSelector.tsx
frontend/components/analysis/ResumeSelector.module.scss
frontend/components/analysis/JobDescriptionInput.tsx
frontend/components/analysis/JobDescriptionInput.module.scss
```

---

## Requirements

- Show parsed resumes only
- Display clear message if no parsed resumes exist
- Allow user to select one resume
- Allow user to paste job description
- Validate that job description is not empty
- Submit analysis request
- Show loading state
- Show error state
- Keep page consistent with existing app shell

---

## Acceptance Criteria

- User can open `/dashboard/analysis`
- User can select a parsed resume
- User can paste a job description
- User can submit form
- Unparsed resumes are not selectable
- Empty job description is rejected
- API errors are shown clearly

---

## Commit Message

```bash
git commit -m "feat(analysis): add analysis form"
```

---

# Phase 7.10 — Analysis Result UI

## Goal

Display the generated analysis result after submission.

---

## Components

```txt
frontend/components/analysis/AnalysisResult.tsx
frontend/components/analysis/AnalysisResult.module.scss
frontend/components/analysis/MatchScoreCard.tsx
frontend/components/analysis/MatchScoreCard.module.scss
frontend/components/analysis/MatchedRequirementsList.tsx
frontend/components/analysis/MatchedRequirementsList.module.scss
frontend/components/analysis/MissingRequirementsList.tsx
frontend/components/analysis/MissingRequirementsList.module.scss
frontend/components/analysis/ImprovementSuggestions.tsx
frontend/components/analysis/ImprovementSuggestions.module.scss
```

---

## Display

```txt
Match Score: 72%

Matched Requirements:
✓ customer support
✓ billing issues
✓ communication

Missing Requirements:
✗ zendesk tickets
✗ enterprise clients

Suggestions:
• Add resume bullets that demonstrate experience with Zendesk tickets, if applicable.
• Highlight any experience working with enterprise clients or similar high-value customers.
```

---

## Requirements

- Show match score
- Show matched requirements
- Show missing requirements
- Show improvement suggestions
- Show empty states when lists are empty
- Make result readable and recruiter-demo friendly

---

## Acceptance Criteria

- Result appears after successful analysis
- Score is clearly visible
- Matched requirements are visible
- Missing requirements are visible
- Suggestions are visible
- UI handles empty matched/missing lists cleanly

---

## Commit Message

```bash
git commit -m "feat(analysis): add analysis result ui"
```

---

# Phase 7.11 — Analysis History

## Goal

Display previous analyses and allow users to delete saved analyses.

---

## Route

```txt
/dashboard/analysis/history
```

---

## Components

```txt
frontend/components/analysis/AnalysisHistory.tsx
frontend/components/analysis/AnalysisHistory.module.scss
frontend/components/analysis/AnalysisHistoryCard.tsx
frontend/components/analysis/AnalysisHistoryCard.module.scss
frontend/components/analysis/DeleteAnalysisButton.tsx
frontend/components/analysis/DeleteAnalysisButton.module.scss
```

---

## Requirements

- List analyses
- View analysis summary
- Show resume file name if available
- Show match score
- Show created date
- Delete analysis
- Require confirmation before delete
- Show deleting/loading state
- Remove deleted analysis from UI without page reload when possible
- Show error state if delete fails

---

## Delete Flow

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

---

## Acceptance Criteria

- User can open `/dashboard/analysis/history`
- Previous analyses are listed
- Empty state appears when no analyses exist
- User can delete an analysis from history
- Deleted analysis disappears from the list
- Firestore document is removed from `users/{uid}/analyses/{analysisId}`
- Page refresh does not restore deleted analysis
- Delete errors show a clear message
- No console errors

---

## Commit Message

```bash
git commit -m "feat(analysis): add analysis history"
```

---

# Phase 7.12 — Milestone Polish

## Goal

Verify the full job match analysis workflow.

---

## End-to-End Flow

```txt
Upload Resume
↓
Parse Resume
↓
Open Analysis Page
↓
Select Parsed Resume
↓
Paste Job Description
↓
Generate Match
↓
View Score
↓
View Matched Requirements
↓
View Missing Requirements
↓
View Suggestions
↓
Save Analysis
↓
View History
↓
Delete Analysis
```

---

# UI Verification

- [ ] User can open `/dashboard/analysis`
- [ ] Resume selector works
- [ ] Only parsed resumes are selectable
- [ ] Empty parsed-resume state works
- [ ] Job description input works
- [ ] Empty job description is rejected
- [ ] Analysis created successfully
- [ ] Match score displayed
- [ ] Matched requirements displayed
- [ ] Missing requirements displayed
- [ ] Suggestions displayed
- [ ] Analysis saved to Firestore
- [ ] User can open `/dashboard/analysis/history`
- [ ] History page displays results
- [ ] Analysis deletion works
- [ ] Deleted analysis disappears after refresh
- [ ] No console errors
- [ ] Protected routes work
- [ ] UI matches existing app style

---

# Backend Verification

- [ ] Analysis endpoints appear in `/docs`
- [ ] Protected endpoints reject unauthenticated requests
- [ ] User-scoped data enforced
- [ ] Users cannot analyze another user's resume
- [ ] Users cannot read another user's analyses
- [ ] Users cannot delete another user's analyses
- [ ] Requirement extraction works for multiple job types
- [ ] Match engine works for strong/partial/no-match cases
- [ ] Improvement suggestions are generated
- [ ] Analysis persistence works
- [ ] Analysis deletion is user-scoped
- [ ] Deleted analyses are removed from Firestore

---

# Firestore Verification

Check:

```txt
users/{uid}/analyses/{analysisId}
```

Verify saved analysis includes:

```txt
id
userId
resumeId
resumeFileName
jobDescription
extractedRequirements
matchScore
matchedRequirements
missingRequirements
improvementSuggestions
createdAt
updatedAt
```

---

# Final Success Criteria

Milestone 7 is complete when:

- [ ] User can select a parsed resume
- [ ] User can paste a job description
- [ ] App extracts job requirements dynamically
- [ ] App returns match score
- [ ] App shows matched requirements
- [ ] App shows missing requirements
- [ ] App shows suggested improvements
- [ ] Analysis result is saved
- [ ] Analysis history is displayed
- [ ] Analysis can be deleted
- [ ] All data is user-scoped
- [ ] Full flow works from UI

---

# Component Tree After Milestone 7

```txt
AnalysisPage
└── ProtectedRoute
    └── AppShell
        └── PageContainer
            ├── AnalysisForm
            │   ├── ResumeSelector
            │   └── JobDescriptionInput
            └── AnalysisResult
                ├── MatchScoreCard
                ├── MatchedRequirementsList
                ├── MissingRequirementsList
                └── ImprovementSuggestions

AnalysisHistoryPage
└── ProtectedRoute
    └── AppShell
        └── PageContainer
            └── AnalysisHistory
                └── AnalysisHistoryCard[]
                    └── DeleteAnalysisButton
```

---

# Backend Flow

```txt
POST /api/analyses
  ↓
get_current_user
  ↓
load resume from users/{uid}/resumes/{resumeId}
  ↓
verify resume.status == parsed
  ↓
read resume.parsedText
  ↓
requirement_extractor.extract_requirements(jobDescription)
  ↓
match_engine.analyze_match(parsedText, requirements)
  ↓
improvement_service.generate_suggestions(missingRequirements)
  ↓
analysis_repository.create_analysis()
  ↓
Firestore users/{uid}/analyses/{analysisId}
```

---

# Frontend Flow

```txt
User opens /dashboard/analysis
  ↓
Frontend loads parsed resumes
  ↓
User selects resume
  ↓
User pastes job description
  ↓
Frontend calls createAnalysis()
  ↓
Backend returns analysis result
  ↓
Frontend displays score, matched requirements, missing requirements, and suggestions
  ↓
Analysis is visible in /dashboard/analysis/history
```

---

# Recommended Codex Workflow

Use this pattern for every phase:

```txt
Read:
- AGENTS.md
- docs/development-standards.md
- docs/milestones/milestone-7-job-match-analysis.md

Implement Phase 7.X only.

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

# Final Commit

```bash
git commit -m "chore(analysis): finalize job match analysis milestone"
```

---

# Next Milestone

➡️ Milestone 8 — AI Match Enhancement

Possible focus:

- Claude/OpenAI-generated feedback
- Better requirement extraction
- Semantic matching
- Resume improvement recommendations
- Cover letter generation
