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
  aiQuestions?: InterviewQuestion[] | null;
  aiQuestionsSource?: string | null;
  aiQuestionsGeneratedAt?: string | null;
  isSeededDemoData?: boolean;
  createdByDemoSeed?: boolean;
  isDemoCreated?: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateInterviewSessionInput {
  analysisId: string;
}

export interface SaveInterviewAnswersInput {
  answers: InterviewAnswer[];
}

export interface AIInterviewQuestions {
  questions: InterviewQuestion[];
  source: string;
  generatedAt: string;
  message: string;
}
