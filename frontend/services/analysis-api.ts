import { apiRequest } from "@/services/api-client";
import type {
  Analysis,
  AnalysisSummary,
  CreateAnalysisInput,
} from "@/types/analysis";

const ANALYSES_PATH = "/api/analyses";

function jsonRequestOptions(
  method: "POST",
  body: CreateAnalysisInput,
): RequestInit {
  return {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
}

function analysisPath(id: string): string {
  return `${ANALYSES_PATH}/${encodeURIComponent(id)}`;
}

export function createAnalysis(input: CreateAnalysisInput): Promise<Analysis> {
  return apiRequest<Analysis>(
    ANALYSES_PATH,
    jsonRequestOptions("POST", input),
  );
}

export function getAnalyses(): Promise<AnalysisSummary[]> {
  return apiRequest<AnalysisSummary[]>(ANALYSES_PATH);
}

export function getAnalysis(id: string): Promise<Analysis> {
  return apiRequest<Analysis>(analysisPath(id));
}

export function deleteAnalysis(id: string): Promise<void> {
  return apiRequest<void>(analysisPath(id), {
    method: "DELETE",
  });
}
