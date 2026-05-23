# Resume Data Model

## Firestore Structure

Resume metadata belongs to one authenticated Firebase user and lives under that user's document:

```txt
users/{uid}/resumes/{resumeId}
```

Example:

```txt
users/
  firebaseUserUid123/
    resumes/
      resumeDocId456
```

This structure keeps resume metadata scoped by Firebase UID and prepares backend repository methods to query only the current user's resumes.

## Firebase Storage Path

Resume files are stored under the owning user's namespace:

```txt
users/{uid}/resumes/{resumeId}/{fileName}
```

Example:

```txt
users/firebaseUserUid123/resumes/resumeDocId456/arnob-resume.pdf
```

The storage path is stored in Firestore as `storagePath` so future backend parsing can locate the uploaded file.

## Status Values

Allowed resume statuses:

```txt
uploaded
parsed
parse_failed
```

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `id` | Yes | Resume metadata document ID returned to clients. |
| `userId` | Yes | Firebase UID for the owning user. |
| `fileName` | Yes | Original uploaded file name. |
| `fileUrl` | Yes | Download URL or accessible file URL saved after upload. |
| `storagePath` | Yes | Firebase Storage path for the uploaded file. |
| `contentType` | Yes | MIME type of the uploaded resume file. |
| `sizeBytes` | Yes | File size in bytes. |
| `status` | Yes | One of the allowed resume status values. |
| `parsedText` | No | Extracted resume text after backend parsing succeeds. |
| `createdAt` | Yes | Creation timestamp, stored as an ISO datetime string in API responses. |
| `updatedAt` | Yes | Last update timestamp, stored as an ISO datetime string in API responses. |

## Create Metadata Input

Required fields:

```txt
fileName
fileUrl
storagePath
contentType
sizeBytes
status
```

The backend will derive `id`, `userId`, `createdAt`, and `updatedAt`.

## Update Metadata Input

Updates may include any editable metadata or parsing field:

```txt
fileName
fileUrl
storagePath
contentType
sizeBytes
status
parsedText
```

The backend will preserve ownership fields and update `updatedAt`.

## Phase Boundaries

This phase defines the domain model only. Firebase Storage setup, upload UI, backend metadata schemas, repository methods, and parsing are implemented in later Milestone 6 phases.
