import { apiRequest } from "@/services/api-client";
import type {
  CreateApplicationInput,
  JobApplication,
  UpdateApplicationInput,
} from "@/types/application";

const APPLICATIONS_PATH = "/api/applications";

function jsonRequestOptions(
  method: "POST" | "PATCH",
  body: CreateApplicationInput | UpdateApplicationInput,
): RequestInit {
  return {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
}

function applicationPath(id: string): string {
  return `${APPLICATIONS_PATH}/${encodeURIComponent(id)}`;
}

export function createApplication(
  input: CreateApplicationInput,
): Promise<JobApplication> {
  return apiRequest<JobApplication>(
    APPLICATIONS_PATH,
    jsonRequestOptions("POST", input),
  );
}

export function getApplications(): Promise<JobApplication[]> {
  return apiRequest<JobApplication[]>(APPLICATIONS_PATH);
}

export function getApplicationById(id: string): Promise<JobApplication> {
  return apiRequest<JobApplication>(applicationPath(id));
}

export function updateApplication(
  id: string,
  input: UpdateApplicationInput,
): Promise<JobApplication> {
  return apiRequest<JobApplication>(
    applicationPath(id),
    jsonRequestOptions("PATCH", input),
  );
}

export function deleteApplication(id: string): Promise<void> {
  return apiRequest<void>(applicationPath(id), {
    method: "DELETE",
  });
}
