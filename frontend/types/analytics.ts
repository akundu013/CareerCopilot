export interface ApplicationsByStatusItem {
  status: string;
  count: number;
}

export interface WeeklyApplicationActivityItem {
  week: string;
  count: number;
}

export interface RequirementFrequencyItem {
  requirement: string;
  count: number;
}

export interface AnalyticsSummary {
  totalApplications: number;
  applicationsByStatus: ApplicationsByStatusItem[];
  responseRate: number;
  weeklyApplicationActivity: WeeklyApplicationActivityItem[];
  totalResumes: number;
  parsedResumes: number;
  totalAnalyses: number;
  averageMatchScore: number;
  topMissingRequirements: RequirementFrequencyItem[];
  topMatchedRequirements: RequirementFrequencyItem[];
  totalInterviewSessions: number;
  savedInterviewAnswers: number;
}
