import { apiRequest } from "@/services/api-client";
import type { AnalyticsSummary } from "@/types/analytics";

const ANALYTICS_SUMMARY_PATH = "/api/analytics/summary";

export function getAnalyticsSummary(): Promise<AnalyticsSummary> {
  return apiRequest<AnalyticsSummary>(ANALYTICS_SUMMARY_PATH);
}
