import { apiRequest } from "@/services/api-client";
import type {
  AIInterviewQuestions,
  CreateInterviewSessionInput,
  InterviewSession,
  SaveInterviewAnswersInput,
} from "@/types/interview";

const INTERVIEWS_PATH = "/api/interviews";

function jsonRequestOptions(
  method: "POST" | "PUT",
  body: CreateInterviewSessionInput | SaveInterviewAnswersInput,
): RequestInit {
  return {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
}

function interviewPath(id: string): string {
  return `${INTERVIEWS_PATH}/${encodeURIComponent(id)}`;
}

export function createInterviewSession(
  input: CreateInterviewSessionInput,
): Promise<InterviewSession> {
  return apiRequest<InterviewSession>(
    INTERVIEWS_PATH,
    jsonRequestOptions("POST", input),
  );
}

export function getInterviewSessions(): Promise<InterviewSession[]> {
  return apiRequest<InterviewSession[]>(INTERVIEWS_PATH);
}

export function getInterviewSession(id: string): Promise<InterviewSession> {
  return apiRequest<InterviewSession>(interviewPath(id));
}

export function saveInterviewAnswers(
  id: string,
  input: SaveInterviewAnswersInput,
): Promise<InterviewSession> {
  return apiRequest<InterviewSession>(
    `${interviewPath(id)}/answers`,
    jsonRequestOptions("PUT", input),
  );
}

export function deleteInterviewSession(id: string): Promise<void> {
  return apiRequest<void>(interviewPath(id), {
    method: "DELETE",
  });
}

export function generateAIInterviewQuestions(
  id: string,
): Promise<AIInterviewQuestions> {
  return apiRequest<AIInterviewQuestions>(`${interviewPath(id)}/ai-questions`, {
    method: "POST",
  });
}
