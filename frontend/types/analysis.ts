export type MatchScore = number;

export interface Analysis {
  id: string;
  userId: string;
  resumeId: string;
  jobDescription: string;
  matchScore: MatchScore;
  matchedSkills: string[];
  missingSkills: string[];
  improvementSuggestions: string[];
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
  matchScore: MatchScore;
  matchedSkills: string[];
  missingSkills: string[];
  createdAt: string;
  updatedAt: string;
}
