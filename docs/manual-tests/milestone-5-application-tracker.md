# Milestone 5 Manual Test Checklist

## Setup

- [ ] Start the backend at `http://localhost:8000`.
- [ ] Start the frontend at `http://localhost:3000`.
- [ ] Confirm `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`.
- [ ] Log in with a Firebase account.

## Backend Docs

- [ ] Open `http://localhost:8000/docs`.
- [ ] Confirm these routes appear:
  - `POST /api/applications`
  - `GET /api/applications`
  - `GET /api/applications/{application_id}`
  - `PATCH /api/applications/{application_id}`
  - `DELETE /api/applications/{application_id}`

## Auth Protection

- [ ] Call `GET /api/applications` without an `Authorization` header.
- [ ] Confirm the response is `401`.
- [ ] Call `POST /api/applications` without an `Authorization` header.
- [ ] Confirm the response is `401`.

## Create Application

- [ ] Go to `/dashboard/applications/new`.
- [ ] Submit the form with blank required fields.
- [ ] Confirm validation appears for required fields.
- [ ] Fill in company, role, status, and optional details.
- [ ] Submit the form.
- [ ] Confirm the app redirects to `/dashboard/applications`.

## View And Filter

- [ ] Confirm the created application appears in the table.
- [ ] Confirm the newest applications appear first.
- [ ] Select each status filter:
  - [ ] All
  - [ ] Applied
  - [ ] Interviewing
  - [ ] Offer
  - [ ] Rejected
  - [ ] Withdrawn
- [ ] Confirm the table updates for each filter.
- [ ] Confirm empty states appear when no applications match a filter.

## Edit Application

- [ ] Click `Edit` on an application row.
- [ ] Confirm the edit page loads existing values.
- [ ] Change the status or notes.
- [ ] Save the form.
- [ ] Confirm the app redirects to `/dashboard/applications`.
- [ ] Confirm the updated values appear in the list.

## Delete Application

- [ ] Click `Delete` on an application row.
- [ ] Confirm a confirmation dialog appears.
- [ ] Click `Cancel`.
- [ ] Confirm the application remains in the table.
- [ ] Click `Delete` again.
- [ ] Confirm deletion.
- [ ] Confirm the row disappears from the table.

## Ownership

- [ ] Create an application while logged in as User A.
- [ ] Log out.
- [ ] Log in as User B.
- [ ] Confirm User A's application is not visible.
- [ ] Try to request User A's application ID while authenticated as User B.
- [ ] Confirm the backend does not return User A's application data.

## Dashboard Protection

- [ ] Log out.
- [ ] Visit `/dashboard/applications`.
- [ ] Confirm the app redirects to `/login`.
- [ ] Visit `/dashboard/applications/new`.
- [ ] Confirm the app redirects to `/login`.
