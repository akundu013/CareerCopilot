from enum import Enum

from pydantic import BaseModel, Field


class InterviewQuestionCategory(str, Enum):
    GENERAL = "general"
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"


class InterviewQuestion(BaseModel):
    id: str = Field(min_length=1)
    category: InterviewQuestionCategory
    prompt: str = Field(min_length=1)


class InterviewAnswer(BaseModel):
    questionId: str = Field(min_length=1)
    answer: str = ""


class CreateInterviewSessionRequest(BaseModel):
    analysisId: str = Field(min_length=1)


class UpdateInterviewAnswersRequest(BaseModel):
    answers: list[InterviewAnswer]


class InterviewSessionResponse(BaseModel):
    id: str
    userId: str
    analysisId: str
    resumeId: str
    resumeFileName: str
    questions: list[InterviewQuestion]
    answers: list[InterviewAnswer]
    aiQuestions: list[InterviewQuestion] | None = None
    aiQuestionsSource: str | None = None
    aiQuestionsGeneratedAt: str | None = None
    isSeededDemoData: bool | None = None
    createdByDemoSeed: bool | None = None
    isDemoCreated: bool | None = None
    createdAt: str
    updatedAt: str


class InterviewAIQuestionsResponse(BaseModel):
    questions: list[InterviewQuestion]
    source: str
    generatedAt: str
    message: str
