import { apiRequest } from "@/services/api-client";
import type {
  CreateResumeMetadataInput,
  ResumeDocument,
  UpdateResumeMetadataInput,
} from "@/types/resume";

const RESUMES_PATH = "/api/resumes";

function jsonRequestOptions(
  method: "POST" | "PATCH",
  body: CreateResumeMetadataInput | UpdateResumeMetadataInput,
): RequestInit {
  return {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
}

function resumePath(id: string): string {
  return `${RESUMES_PATH}/${encodeURIComponent(id)}`;
}

export function createResumeMetadata(
  input: CreateResumeMetadataInput,
): Promise<ResumeDocument> {
  return apiRequest<ResumeDocument>(
    RESUMES_PATH,
    jsonRequestOptions("POST", input),
  );
}

export function getResumes(): Promise<ResumeDocument[]> {
  return apiRequest<ResumeDocument[]>(RESUMES_PATH);
}

export function getResumeById(id: string): Promise<ResumeDocument> {
  return apiRequest<ResumeDocument>(resumePath(id));
}

export function updateResume(
  id: string,
  input: UpdateResumeMetadataInput,
): Promise<ResumeDocument> {
  return apiRequest<ResumeDocument>(
    resumePath(id),
    jsonRequestOptions("PATCH", input),
  );
}

export function deleteResume(id: string): Promise<void> {
  return apiRequest<void>(resumePath(id), {
    method: "DELETE",
  });
}
