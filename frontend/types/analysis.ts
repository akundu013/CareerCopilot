export type MatchScore = number;

export interface Analysis {
  id: string;
  userId: string;
  resumeId: string;
  resumeFileName: string;
  jobDescription: string;
  extractedRequirements: string[];
  matchScore: MatchScore;
  matchedRequirements: string[];
  missingRequirements: string[];
  improvementSuggestions: string[];
  isSeededDemoData?: boolean;
  createdByDemoSeed?: boolean;
  isDemoCreated?: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateAnalysisInput {
  resumeId: string;
  jobDescription: string;
}

export interface AnalysisSummary {
  id: string;
  resumeId: string;
  resumeFileName: string;
  matchScore: MatchScore;
  matchedRequirements: string[];
  missingRequirements: string[];
  isSeededDemoData?: boolean;
  createdByDemoSeed?: boolean;
  isDemoCreated?: boolean;
  createdAt: string;
  updatedAt: string;
}
