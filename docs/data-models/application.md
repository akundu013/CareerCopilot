# Application Data Model

## Firestore Structure

Application records belong to one authenticated Firebase user and live under that user's document:

```txt
users/{userId}/applications/{applicationId}
```

Example:

```txt
users/
  firebaseUserUid123/
    applications/
      applicationDocId456
```

This structure keeps application data scoped by Firebase UID and prepares the backend repository layer to query only the current user's records.

## Status Values

Allowed application statuses:

```txt
applied
interviewing
offer
rejected
withdrawn
```

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `id` | Yes | Application document ID returned to clients. |
| `userId` | Yes | Firebase UID for the owning user. |
| `company` | Yes | Company name. |
| `role` | Yes | Job title or role name. |
| `status` | Yes | One of the allowed application status values. |
| `location` | No | Job location or remote/hybrid note. |
| `jobUrl` | No | Link to the job posting. |
| `salaryRange` | No | User-entered compensation range. |
| `notes` | No | Freeform notes about the application. |
| `dateApplied` | No | Date the user applied, stored as an ISO date string. |
| `createdAt` | Yes | Creation timestamp, stored as an ISO datetime string in API responses. |
| `updatedAt` | Yes | Last update timestamp, stored as an ISO datetime string in API responses. |

## Create Input

Required fields:

```txt
company
role
status
```

Optional fields:

```txt
location
jobUrl
salaryRange
notes
dateApplied
```

The backend will derive `id`, `userId`, `createdAt`, and `updatedAt`.

## Update Input

Updates may include any editable create-input field:

```txt
company
role
status
location
jobUrl
salaryRange
notes
dateApplied
```

The backend will preserve ownership fields and update `updatedAt`.
