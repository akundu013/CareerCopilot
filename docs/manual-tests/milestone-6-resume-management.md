# Milestone 6 Manual Test — Resume Management

Use this checklist before committing Milestone 6.

## Required Local Setup

- Frontend running at `http://localhost:3000`
- Backend running at `http://localhost:8000`
- Backend uses `backend/.venv`
- Firebase Auth user exists and can log in
- Firebase Storage is enabled
- Firestore is enabled
- `frontend/.env.local` has the real Firebase Storage bucket
- `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
- `backend/.env` has Firebase Admin credentials

## Firebase Storage Rules

Use authenticated, user-scoped Storage rules for resume files:

```js
rules_version = '2';

service firebase.storage {
  match /b/{bucket}/o {
    match /users/{userId}/resumes/{resumeId}/{fileName} {
      allow read: if request.auth != null
        && request.auth.uid == userId;

      allow write: if request.auth != null
        && request.auth.uid == userId
        && request.resource.size <= 5 * 1024 * 1024
        && request.resource.contentType.matches(
          'application/pdf|application/vnd.openxmlformats-officedocument.wordprocessingml.document|text/plain'
        );
    }
  }
}
```

## Frontend UI Check

- [ ] Log in successfully.
- [ ] Open `/dashboard/resumes` from the browser URL.
- [ ] Open `/dashboard/resumes` from the sidebar `Resumes` link.
- [ ] Confirm the page renders inside the app shell with no layout overlap.
- [ ] Confirm the empty state appears when the account has no resumes.
- [ ] Upload a valid TXT resume under 5 MB.
- [ ] Confirm upload progress appears.
- [ ] Confirm upload success appears.
- [ ] Confirm the resume appears in the resume list without refreshing.
- [ ] Confirm the resume card shows file name, status, upload date, updated date, size, and type.
- [ ] Confirm `Open file` opens the uploaded file.
- [ ] Upload a valid PDF or DOCX resume under 5 MB.
- [ ] Try uploading an unsupported file type and confirm the UI rejects it.
- [ ] Try uploading a file larger than 5 MB and confirm the UI rejects it.
- [ ] Click `Parse resume` on a TXT resume.
- [ ] Confirm the button changes to `Parsing...`.
- [ ] Confirm duplicate parse actions are disabled while parsing.
- [ ] Confirm the resume status changes to `Parsed` after a successful parse.
- [ ] Confirm parsed resume text is stored in Firestore as `parsedText`.
- [ ] Confirm a scanned/image-only PDF fails gracefully with `parse_failed` if no text can be extracted.
- [ ] Click `Delete` on a resume.
- [ ] Confirm the delete confirmation dialog appears.
- [ ] Confirm cancelling the dialog leaves the resume in the list.
- [ ] Click `Delete` again and confirm deletion.
- [ ] Confirm the delete button shows a loading state.
- [ ] Confirm the resume disappears from the list after deletion.
- [ ] Refresh `/dashboard/resumes` and confirm the deleted resume does not return.
- [ ] Confirm the browser console has no app errors after upload, list refresh, and parse.
- [ ] Confirm dashboard/sidebar navigation links are not broken.
- [ ] Confirm `/dashboard` copy reflects resume management as an available feature.

## Firebase Verification

- [ ] In Firebase Storage, confirm the uploaded file exists at `users/{uid}/resumes/{resumeId}/{fileName}`.
- [ ] In Firestore, confirm metadata exists at `users/{uid}/resumes/{resumeId}`.
- [ ] Confirm metadata includes `fileName`, `fileUrl`, `storagePath`, `contentType`, `sizeBytes`, `status`, `createdAt`, and `updatedAt`.
- [ ] After parsing, confirm `status` is `parsed` for text resumes.
- [ ] After parsing, confirm `parsedText` contains extracted resume text.
- [ ] After deletion, confirm the Firebase Storage file is removed.
- [ ] After deletion, confirm the Firestore metadata document is removed.

## Backend Verification

- [ ] Open `http://localhost:8000/docs`.
- [ ] Confirm these endpoints appear:
  - `POST /api/resumes`
  - `GET /api/resumes`
  - `GET /api/resumes/{resume_id}`
  - `PATCH /api/resumes/{resume_id}`
  - `DELETE /api/resumes/{resume_id}`
  - `POST /api/resumes/{resume_id}/parse`
- [ ] Call `GET /api/resumes` without a token and confirm `401`.
- [ ] Call `POST /api/resumes/{resume_id}/parse` without a token and confirm `401`.
- [ ] Call resume endpoints with a valid Firebase ID token and confirm user-scoped data only.
- [ ] Confirm TXT parsing succeeds.
- [ ] Confirm PDF parsing succeeds for text-based PDFs.
- [ ] Confirm DOCX parsing succeeds for valid DOCX files.
- [ ] Confirm unsupported or unreadable files fail cleanly as `parse_failed`.
- [ ] Call `DELETE /api/resumes/{resume_id}` with a valid Firebase ID token and confirm `204`.
- [ ] Confirm backend deletion removes both the Firestore document and Firebase Storage file.

## Automated Checks

Run from `frontend/`:

```bash
npm run lint
npx tsc --noEmit
```

Run from `backend/`:

```bash
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall app
```
