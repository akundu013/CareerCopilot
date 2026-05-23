export type InterviewQuestionCategory = "general" | "behavioral" | "technical";

export interface InterviewQuestion {
  id: string;
  category: InterviewQuestionCategory;
  prompt: string;
}

export interface InterviewAnswer {
  questionId: string;
  answer: string;
}

export interface InterviewSession {
  id: string;
  userId: string;
  analysisId: string;
  resumeId: string;
  resumeFileName: string;
  questions: InterviewQuestion[];
  answers: InterviewAnswer[];
  createdAt: string;
  updatedAt: string;
}

export interface CreateInterviewSessionInput {
  analysisId: string;
}

export interface SaveInterviewAnswersInput {
  answers: InterviewAnswer[];
}
